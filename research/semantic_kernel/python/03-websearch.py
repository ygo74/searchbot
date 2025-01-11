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

RESEARCHER_MANAGER = "Manager"
SEARCHER_NAME = "Web_Searcher"

TERMINATION_KEYWORD = "TERMINATE"

from lib.websearch import google_search, google_search_with_article
from typing import Annotated

class WebSearchPlugin:
    @kernel_function(description="Search the web for information based on a query.")
    def search(self, query: str, num_results: int = 2, max_chars: int = 0) -> Annotated[str, "Returns the web site pages links and body."]:

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
    kernel = _create_kernel_with_services()

    settings = kernel.get_prompt_execution_settings_from_service_id(service_id=SEARCHER_NAME)
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    research_manager = ChatCompletionAgent(
        service_id=RESEARCHER_MANAGER,
        kernel=kernel,
        name=RESEARCHER_MANAGER,
        instructions=f"""
            You are a research manager, you are harsh, you are relentless.
            You will work task by task.

            Analyze the user's query and understantd the goal of the user's query.
            If the query is unclear, ask the user for clarification before proceeding.

            You will firstly try to generate 2 actions {SEARCHER_NAME} agent can take to find the information needed by the user's query.
            - Try to avoid G2, or other gated website that don't allow srcabing
            - Define a precise query to search.
            - Define the objective of the search.
            - Define clear criteria for determining when the step is complete.


            You will reviewed the result from the {SEARCHER_NAME}, and always push back if {SEARCHER_NAME} didin't find the information.
            Be persistent, say "No, you have to find the information, try again and propose 1 next method to try, if the {SEARCHER_NAME} want to get away.

            You will compile all results from {SEARCHER_NAME} and generate a comprehensive report of information found by the team.
            the report will contain facts, links and samples.

            When wou gathered all information, you will say "TERMINATE"
        """,
    )

    agent_searcher = ChatCompletionAgent(
        service_id=SEARCHER_NAME,
        kernel=kernel,
        name=SEARCHER_NAME,
        instructions=f"""
            You are a world class researcher, who can do detailed research on any topic and produce facts based results;
            Execute the provided requested searches by performing precise web searches.
            you do not make things up, you will try as hard as possible to gather facts & data to back up the {RESEARCHER_MANAGER}

            You make only one web search call at a time.
            Once you have the results, you never do calculations based on them.
            You never try to generate reports, you only return the search results to your {RESEARCHER_MANAGER}

            Please make sure you complete the objective above with the following rules:
            1/ You should do enough research to gather as much information as possible about the objective
            2/ If there are url of relevant links & articles, you will scrape it to gather more information
            3/ After scraping & search, you should think "is there any new things i should search & scraping based on the data I collected to increase research quality?" If answer is yes, continue; But don't do this more than 3 iteratins
            4/ You should not make things up, you should only write facts & data that you have gathered
            5/ In the final output, You should include all reference data & links to back up your {RESEARCHER_MANAGER};
        """,
        execution_settings=settings,
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
        - After user input, it is {RESEARCHER_MANAGER}'s turn.
        - After {RESEARCHER_MANAGER} defines search queries, {SEARCHER_NAME} searches it.
        - After {SEARCHER_NAME} presents findings, {RESEARCHER_MANAGER} reviews them and compile them.

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
        agents=[research_manager, agent_searcher],
        # selection_strategy=KernelFunctionSelectionStrategy(
        #     function=selection_function,
        #     kernel=kernel,
        #     result_parser=lambda result: str(result.value[0]) if result.value is not None else RESEARCHER_MANAGER,
        #     agent_variable_name="agents",
        #     history_variable_name="history",
        # ),
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
