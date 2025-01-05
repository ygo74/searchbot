# Copyright (c) Microsoft. All rights reserved.

import asyncio
import os
from dotenv import load_dotenv
from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent
from semantic_kernel.agents.strategies.selection.kernel_function_selection_strategy import (
    KernelFunctionSelectionStrategy,
)
from semantic_kernel.agents.strategies.termination.kernel_function_termination_strategy import (
    KernelFunctionTerminationStrategy,
)
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.search_engine import GoogleConnector
from semantic_kernel.core_plugins import WebSearchEnginePlugin
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.functions.kernel_function_from_prompt import KernelFunctionFromPrompt
from semantic_kernel.kernel import Kernel

from openai import AsyncAzureOpenAI

###################################################################
# This sample demonstrates how to create a complex agent group   #
# chat that includes a Critic and a Compiler agent in addition   #
# to Planner and Searcher agents.                               #
###################################################################

PLANNER_NAME = "Planner"
SEARCHER_NAME = "Searcher"
CRITIC_NAME = "Critic"
COMPILER_NAME = "Compiler"

TERMINATION_KEYWORD = "TERMINATE"

import httpx

def _create_kernel_with_services() -> Kernel:

    # Configure a custom HTTP client with a timeout
    http_client = httpx.AsyncClient(timeout=httpx.Timeout(300.0))
    client = AsyncAzureOpenAI(
        http_client=http_client,
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        max_retries=3
    )

    kernel = Kernel()
    kernel.add_service(AzureChatCompletion(service_id=PLANNER_NAME, async_client=client))
    kernel.add_service(AzureChatCompletion(service_id=SEARCHER_NAME, async_client=client))
    kernel.add_service(AzureChatCompletion(service_id=CRITIC_NAME, async_client=client))
    kernel.add_service(AzureChatCompletion(service_id=COMPILER_NAME, async_client=client))

    # Add the Google Search connector
    google_connector = GoogleConnector(api_key=os.getenv("GOOGLE_SEARCH_API_KEY"),
                                        search_engine_id=os.getenv("GOOGLE_SEARCH_CENTER_CONNECTION_ID"))
    kernel.add_plugin(WebSearchEnginePlugin(google_connector), "WebSearch")

    return kernel

async def main():
    kernel = _create_kernel_with_services()

    settings = kernel.get_prompt_execution_settings_from_service_id(service_id=SEARCHER_NAME)
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    agent_planner = ChatCompletionAgent(
        service_id=PLANNER_NAME,
        kernel=kernel,
        name=PLANNER_NAME,
        instructions="""
            You are a planning expert. Analyze the user's query and generate a detailed, step-by-step plan to gather accurate and specific information.
            Ensure the plan is actionable, with each step containing:
            - A precise query to search.
            - The objective of the search.
            - Clear criteria for determining when the step is complete.

            If the query is unclear, ask the user for clarification before proceeding.
        """,
    )

    agent_searcher = ChatCompletionAgent(
        service_id=SEARCHER_NAME,
        kernel=kernel,
        name=SEARCHER_NAME,
        instructions="""
            You are a web search assistant. Execute the provided plan by performing precise web searches.
            Extract relevant and credible information while citing sources.
            For each step:
            - Report the query used.
            - Summarize the results concisely.
            - Highlight the most relevant findings.

            If the results are insufficient, notify the user or planner for adjustments.
        """,
        execution_settings=settings,
    )

    agent_critic = ChatCompletionAgent(
        service_id=CRITIC_NAME,
        kernel=kernel,
        name=CRITIC_NAME,
        instructions="""
            You are a critical reviewer. Evaluate the quality and accuracy of the plans and search results provided.
            For plans, identify any missing steps, unclear instructions, or potential issues.
            For search results, identify any missing, inconsistent, or irrelevant information.
            Suggest improvements or confirm that the plans and results are comprehensive and reliable.

            If any agent's response is unsatisfactory, explicitly direct that agent to revise and retry.
        """,
    )

    agent_compiler = ChatCompletionAgent(
        service_id=COMPILER_NAME,
        kernel=kernel,
        name=COMPILER_NAME,
        instructions="""
            You are a content compiler. Collect all relevant search results and feedback.
            Generate a single markdown document summarizing all the findings, structured as follows:
            - Title: Summary of Findings
            - Subsections for each query and its results.
            - A concluding section with overall insights and key takeaways.

            If any feedback or results are incomplete, notify the appropriate agent for corrections.
        """,
    )

    selection_function = KernelFunctionFromPrompt(
        function_name="selection",
        prompt=f"""
        Determine the next participant in a conversation based on the most recent participant's action.
        State only the name of the next participant to take the turn.

        Choose from these participants:
        - {PLANNER_NAME}
        - {SEARCHER_NAME}
        - {CRITIC_NAME}
        - {COMPILER_NAME}

        Rules:
        - After user input, it is {PLANNER_NAME}'s turn.
        - After {PLANNER_NAME} submits a plan, {CRITIC_NAME} reviews it.
        - If {CRITIC_NAME} approves the plan, {SEARCHER_NAME} searches.
        - If {CRITIC_NAME} disapproves, {PLANNER_NAME} revises the plan.
        - After {SEARCHER_NAME} presents findings, {CRITIC_NAME} reviews them.
        - If {CRITIC_NAME} approves the findings, {COMPILER_NAME} compiles the results.
        - If {CRITIC_NAME} disapproves the findings, {SEARCHER_NAME} revises the search.
        - After {COMPILER_NAME} compiles the response, {CRITIC_NAME} reviews it.
        - If {CRITIC_NAME} approves the response, the conversation ends.
        - If {CRITIC_NAME} disapproves, {COMPILER_NAME} revises the response.

        History:
        {{{{$history}}}}
        """,
    )

    termination_function = KernelFunctionFromPrompt(
        function_name="termination",
        prompt=f"""
            Examine the RESPONSE and determine whether the content has been deemed satisfactory.
            If content is satisfactory, respond with a single word without explanation: {TERMINATION_KEYWORD}.
            If specific suggestions are being provided, it is not satisfactory.
            If no correction is suggested, it is satisfactory.

            RESPONSE:
            {{{{$history}}}}
            """,
    )

    chat = AgentGroupChat(
        agents=[agent_planner, agent_searcher, agent_critic, agent_compiler],
        selection_strategy=KernelFunctionSelectionStrategy(
            function=selection_function,
            kernel=kernel,
            result_parser=lambda result: str(result.value[0]) if result.value is not None else PLANNER_NAME,
            agent_variable_name="agents",
            history_variable_name="history",
        ),
        termination_strategy=KernelFunctionTerminationStrategy(
            agents=[agent_compiler],
            function=termination_function,
            kernel=kernel,
            result_parser=lambda result: TERMINATION_KEYWORD in str(result.value).lower(),
            history_variable_name="history",
            maximum_iterations=10,
        ),
    )

    is_complete: bool = False
    while not is_complete:
        user_input = input("User:> ")
        if not user_input:
            continue

        if user_input.lower() == "exit":
            is_complete = True
            break

        if user_input.lower() == "reset":
            await chat.reset()
            print("[Conversation has been reset]")
            continue

        if user_input.startswith("@") and len(user_input) > 1:
            file_path = user_input[1:]
            try:
                if not os.path.exists(file_path):
                    print(f"Unable to access file: {file_path}")
                    continue
                with open(file_path) as file:
                    user_input = file.read()
            except Exception:
                print(f"Unable to access file: {file_path}")
                continue

        await chat.add_chat_message(ChatMessageContent(role=AuthorRole.USER, content=user_input))

        async for response in chat.invoke():
            print(f"# {response.role} - {response.name or '*'}: '{response.content}'")

        if chat.is_complete:
            is_complete = True
            break

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
