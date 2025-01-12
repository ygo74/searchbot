# Copyright (c) Microsoft. All rights reserved.

import asyncio
import os
import logging
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

RESEARCHER_MANAGER = "Manager"
SEARCHER_NAME = "Web_Searcher"

TERMINATION_KEYWORD = "TERMINATE"

from lib.websearch import google_search, google_search_with_article
from typing import Annotated

class WebSearchPlugin:
    @kernel_function(description="Search the web for information based on a query.")
    def search(self, query: str, num_results: int = 2, max_chars: int = 25000) -> Annotated[str, "Returns the web site pages links and body."]:

        print(f"Searching the web for information based on the query: {query}")
        search_results = google_search_with_article(query=query, num_results=num_results, max_chars=max_chars)
        result=""
        for search_result in search_results:
            result += f"Title : {search_result['title']}\n"
            result += f"Link : {search_result['link']}\n"
            result += f"Snippet : {search_result['snippet']}\n"
            result += f"Body : {search_result['body']}\n\n"

        print("====================================")
        print(result)
        print("")
        print("====================================")
        print("")
        return result


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
    kernel.add_service(AzureChatCompletion(service_id=RESEARCHER_MANAGER, async_client=client))
    kernel.add_service(AzureChatCompletion(service_id=SEARCHER_NAME, async_client=client))

    # Add the Google Search connector
    # google_connector = GoogleConnector(api_key=os.getenv("GOOGLE_SEARCH_API_KEY"),
    #                                     search_engine_id=os.getenv("GOOGLE_SEARCH_CENTER_CONNECTION_ID"))
    # kernel.add_plugin(WebSearchEnginePlugin(google_connector), "WebSearch")

    kernel.add_plugin(WebSearchPlugin(), plugin_name="WebSearch")

    return kernel

async def main():
    # Set the logging level for  semantic_kernel.kernel to DEBUG.
    logging.getLogger("kernel").setLevel(logging.DEBUG)

    kernel = _create_kernel_with_services()

    searcher_settings = kernel.get_prompt_execution_settings_from_service_id(service_id=SEARCHER_NAME)
    searcher_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    searcher_settings.max_tokens = 10000

    manager_settings = kernel.get_prompt_execution_settings_from_service_id(service_id=RESEARCHER_MANAGER)
    manager_settings.max_tokens = 10000


    research_manager = ChatCompletionAgent(
        service_id=RESEARCHER_MANAGER,
        kernel=kernel,
        name=RESEARCHER_MANAGER,
        instructions=f"""
        You are an AI agent acting as a manager for an internet research agent.

        Your tasks are as follows:
        1. Understand the user's question and break it down into multiple distinct research objectives.
        2. Communicate these objectives one by one to the internet research agent, ensuring each objective is clear and precise, using the following JSON format:
        ```json
        {{
            "objective": "Describe the specific research goal",
            "criteria": {{
            "success": "Describe what constitutes a successful result",
            "site_filter": "Specify if results should come from a specific site (optional)",
            "keywords_required": ["List", "of", "mandatory", "keywords"],
            "keywords_excluded": ["List", "of", "excluded", "keywords"]
            }}
        }}
        ```
        Example:
        ```json
        {{
            "objective": "Find recent articles on AI advancements",
            "criteria": {{
            "success": "Articles published in the last year discussing major AI breakthroughs",
            "site_filter": "site:example.com",
            "keywords_required": ["AI", "breakthroughs", "2024"],
            "keywords_excluded": ["opinion", "advertisement"]
            }}
        }}
        ```
        3. For each objective:
        - Define specific success criteria.
        - Review the results provided by the research agent and evaluate their relevance.
        - If the results do not meet the criteria, instruct the research agent to repeat the search, specifying the necessary adjustments in the JSON format.

        4. Continue this iterative discussion until all objectives have been successfully met.
        5. Once all objectives are achieved, compile a comprehensive final response for the user, including:
        - The titles of the pages found.
        - The links to these pages.
        - The relevant content extracted from each page.
        - Say {TERMINATION_KEYWORD} to end the conversation.
        """,
        execution_settings=manager_settings
    )

    agent_searcher = ChatCompletionAgent(
        service_id=SEARCHER_NAME,
        kernel=kernel,
        name=SEARCHER_NAME,
        instructions=f"""
        You are an Internet Research Specialist AI. Your role is to assist in finding the best possible page that meets the given research objectives and success criteria. Here's how you will perform your tasks:

        1. **Understanding Objectives**: Receive the research objective and success criteria from the manager AI in JSON format.
        2. **Site-Specific Searches**: If the objective specifies searching within a particular site, include a filter in your search query to restrict results to that site (e.g., use `site:<fqdn>`).
        3. **Advanced Search Techniques**: Utilize advanced search techniques to refine your results:
        - Include required words by prefixing them with `+`.
        - Exclude undesired words by prefixing them with `-`.
        - Apply other advanced search methods to optimize the query and improve the relevance of your findings.
        4. **Executing the Search**: Use an internet search tool to find multiple pages related to the objective.
        5. **Analyzing Results**: Review each page individually and extract the parts which matches the objectives and the success criteria.
        6. **Iterative Refinement**: If the manager AI requests further refinement or additional searches, repeat the process until the criteria are fully met.

        """,

        execution_settings=searcher_settings,
    )


    selection_function = KernelFunctionFromPrompt(
        function_name="selection",
        prompt=f"""
        Determine the next participant in a conversation based on the most recent participant's action.
        State only the name of the next participant to take the turn.

        Choose from these participants:
        - {RESEARCHER_MANAGER}
        - {SEARCHER_NAME}

        Rules:
        - After user input, it is {RESEARCHER_MANAGER}'s turn to break down the user's question into research objectives and define search queries.
        - After {RESEARCHER_MANAGER} defines search queries, it is {SEARCHER_NAME}'s turn to execute the search and present the findings (title, link, and content).
        - After {SEARCHER_NAME} presents findings, it is {RESEARCHER_MANAGER}'s turn to review the results, compile them, and provide feedback or finalize the response.

        History:
        {{{{$history}}}}
        """,
    )

    termination_function = KernelFunctionFromPrompt(
        function_name="termination",
        prompt=f"""
        Examine the RESPONSE and determine whether the content has been deemed satisfactory based on the most recent interactions.

        - If no specific suggestions for improvement are provided, the content is deemed satisfactory.
        - If specific suggestions or corrections are still being provided, the content is not satisfactory.

        Respond with a single word without explanation: {TERMINATION_KEYWORD} if the content is satisfactory.

        RESPONSE:
        {{{{$history}}}}
        """,
    )

    chat = AgentGroupChat(
        agents=[research_manager, agent_searcher],
        selection_strategy=KernelFunctionSelectionStrategy(
            function=selection_function,
            kernel=kernel,
            result_parser=lambda result: str(result.value[0]) if result.value is not None else RESEARCHER_MANAGER,
            agent_variable_name="agents",
            history_variable_name="history",
        ),
        termination_strategy=KernelFunctionTerminationStrategy(
            agents=[research_manager],
            function=termination_function,
            kernel=kernel,
            result_parser=lambda result: TERMINATION_KEYWORD in str(result.value).lower(),
            history_variable_name="history",
            maximum_iterations=10,
        ),
    )

    user_input = """
        How to start with semantic kernel AgentGroupChat in python?
        Provides a full detailed real implementation sample of two agents which search results on Internet thanks to a custom plugin.
    """
    await chat.add_chat_message(ChatMessageContent(role=AuthorRole.USER, content=user_input))

    async for response in chat.invoke():
        print(f"# {response.role} - {response.name or '*'}: '{response.content}'")

    # is_complete: bool = False
    # while not is_complete:
    #     user_input = input("User:> ")
    #     if not user_input:
    #         continue

    #     if user_input.lower() == "exit":
    #         is_complete = True
    #         break

    #     if user_input.lower() == "reset":
    #         await chat.reset()
    #         print("[Conversation has been reset]")
    #         continue

    #     if user_input.startswith("@") and len(user_input) > 1:
    #         file_path = user_input[1:]
    #         try:
    #             if not os.path.exists(file_path):
    #                 print(f"Unable to access file: {file_path}")
    #                 continue
    #             with open(file_path) as file:
    #                 user_input = file.read()
    #         except Exception:
    #             print(f"Unable to access file: {file_path}")
    #             continue

    #     await chat.add_chat_message(ChatMessageContent(role=AuthorRole.USER, content=user_input))

    #     async for response in chat.invoke():
    #         print(f"# {response.role} - {response.name or '*'}: '{response.content}'")

    #     if chat.is_complete:
    #         is_complete = True
    #         break

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
