from dotenv import load_dotenv
import os
import sys
import fnmatch
import yaml
import autogen
from autogen import Agent, ConversableAgent, GroupChat
from autogen import register_function
from autogen.coding import DockerCommandLineCodeExecutor, LocalCommandLineCodeExecutor
from autogen.cache import Cache
from modules.logging import *
from modules.search.exception import *
from modules.search.googlesearch import *
from typing import Any, List, Annotated
import argparse
from tavily import TavilyClient

import json


def search_internet(query:  Annotated[str, "The search query"]) -> Annotated[str, "The search results"]:

    # Get Configuration Settings
    load_dotenv()
    google_key = os.getenv('GOOGLE_SEARCH_API_KEY')
    google_engine_id = os.getenv('GOOGLE_SEARCH_CENTER_CONNECTION_ID')

    customSearch = CustomSearch(apikey=google_key, engine_id=google_engine_id)
    results = customSearch.search(query)

    result_dict=[]
    for result in results:
        result_dict.append({
            "url": result.url,
            "title": result.title
        })

    result = json.dumps(result_dict)
    return result


def load_prompts(prompt_path: str) -> dict:
    """
    Read all prompts from an existing folder and return the dict with available prompts
    the key is the filename without extensions
    """
    results = {}
    files = os.listdir(prompt_path)
    for file in files:
        if os.path.isfile(os.path.join(prompt_path, file)) and fnmatch.fnmatch(file, '*.y*ml'):
            with open(os.path.join(prompt_path, file), 'r') as f:
                contenu = yaml.safe_load(f)

            assistant_name = contenu[ "assistant_name" ]
            results[assistant_name] = contenu
    return results



def main():

    def search_tool(query: Annotated[str, "The search query"]) -> Annotated[str, "The search results"]:
        return tavily.get_search_context(query=query, search_depth="advanced")

    try:
        # Script identification
        main_script_id = os.path.abspath(sys.argv[0])
        main_script_name = os.path.basename(main_script_id)
        print(f"Start python script : {main_script_name}")

        # Parse arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("--model_tag", help="models tag to filter used models", default="gpt35")
        args = parser.parse_args()

        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AZURE_OPENAI_API_ENDPOINT')
        ai_key = os.getenv('AZURE_OPENAI_API_KEY')
        google_key = os.getenv('GOOGLE_SEARCH_API_KEY')
        google_engine_id = os.getenv('GOOGLE_SEARCH_CENTER_CONNECTION_ID')
        print(f"AI ENDPOINT : {ai_endpoint}")

        # Load the list of models
        available_llm_config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")

        if args.model_tag is not None and args.model_tag != '':
            print(f"\tFilter models with tags : {args.model_tag}")
            filter_dict = {"tags": [args.model_tag]}
            llm_config_list = autogen.filter_config(available_llm_config_list, filter_dict)

        # Ensure we have a configuration list of models
        assert len(llm_config_list) > 0
        llm_config = {"config_list": llm_config_list}

        # Load assistant configuration
        current_path = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(current_path, 'prompts')
        prompts = load_prompts(prompt_path=prompt_path)

        for result in prompts:
            print( prompts[ result ] )


        # Create Tabily client
        print("Declare search client")
        tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

        print("Declare agents")
        user_proxy = autogen.UserProxyAgent(
            name=prompts[ "admin" ][ "assistant_name" ],
            system_message=prompts[ "admin" ][ "prompt" ],
            code_execution_config=False,
        )

        researcher_manager = autogen.AssistantAgent(
            name=prompts[ "researcher_manager" ][ "assistant_name" ],
            llm_config={
                "config_list": llm_config[ "config_list"],  # a list of OpenAI API configurations
                "temperature": 0,  # temperature for sampling
            },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
            system_message=prompts[ "researcher_manager" ][ "prompt" ],
            human_input_mode="ALWAYS",  # Never ask for human input.
            description="This is the researcher_manager agent"
        )

        researcher = autogen.AssistantAgent(
            name=prompts[ "researcher" ][ "assistant_name" ],
            llm_config={
                "config_list": llm_config[ "config_list"],  # a list of OpenAI API configurations
                "temperature": 0,  # temperature for sampling
            },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
            system_message=prompts[ "researcher" ][ "prompt" ],
            description="This is the researcher agent"
        )

        # Setting up code executor.
        os.makedirs("coding", exist_ok=True)
        code_executor = LocalCommandLineCodeExecutor(work_dir="coding")

        executor = autogen.UserProxyAgent(
            name="Executor",
            system_message="Executor. Execute the code written by the researcher and report the result.",
            human_input_mode="NEVER",
            code_execution_config={
                "executor": code_executor,
                "last_n_messages": 3,
            }
        )

        register_function(
            search_internet,
            caller=researcher,
            executor=executor,
            name="google_search",
            description="search keywords with google search")


        groupchat = autogen.GroupChat(
            # agents=[user_proxy, planner, scientist, researcher, researcher_manager, executor], messages=[], max_round=50
            agents=[user_proxy, researcher, researcher_manager, executor],
            messages=[
                "Start to work with the researcher_manager"
            ],
            # speaker_selection_method=custom_speaker_selection_func,
            # allowed_or_disallowed_speaker_transitions=graph_dict,
            # speaker_transitions_type="allowed",
            max_round=5
        )

        gpt_config = {
            "temperature": 0,
            "config_list": llm_config_list,
            "timeout": 120,
        }

        group_chat_manager  = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt_config)

        print("Start the chat")

        # Cache LLM responses. To get different responses, change the cache_seed value.
        # with Cache.disk(cache_seed=43) as cache:
        user_proxy.initiate_chat(
            group_chat_manager ,
            # message="""
            # find contribution for code from Yannick GOBERT a devops engineer on internet, he can be known with his alias ygo or ygo74
            # """,
            # message="""
            # I want to hire a new employee, I need to know if this person can fit with my objectives to develop a dotnet microservices application.
            # This application will follow Domain driven Design approach, It uses Graphql, fluentvalidation, mediator libraries.
            # It is deployed on Azure Kubernetes servies.
            # Can you confirm that Yannick GOBERT fits this role ?
            # """,
            message="""
            find how to start with Microsoft autogen
            """,
        )



    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()