from dotenv import load_dotenv
import os
import sys
import fnmatch
import yaml
import autogen
from autogen import Agent, ConversableAgent, GroupChat
from autogen import register_function
from modules.logging import *
from modules.search.exception import *
from modules.search.googlesearch import *
from typing import Any, List, Annotated
import argparse
from tavily import TavilyClient

import json


def search_internet(query: str):

    # Get Configuration Settings
    load_dotenv("/mnt/d/devel/github/searchbot/autogen/.env")
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

    return result_dict

def search_tool(query: Annotated[str, "The search query"]) -> Annotated[str, "The search results"]:
    return tavily.get_search_context(query=query, search_depth="advanced")


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

    def custom_speaker_selection_func(last_speaker: Agent, groupchat: GroupChat):
        """Define a customized speaker selection function.
        A recommended way is to define a transition for each speaker in the groupchat.

        Returns:
            Return an `Agent` class or a string from ['auto', 'manual', 'random', 'round_robin'] to select a default method to use.
        """
        messages = groupchat.messages

        if len(messages) <= 1:
            # first, let the engineer retrieve relevant data
            return planner

        if last_speaker is planner:
            # if the last message is from planner, let the engineer to write code
            return critic
        elif last_speaker is user_proxy:
            if messages[-1]["content"].strip() == "OK" or messages[-1]["content"].strip() == "":
                return researcher_manager
            if messages[-1]["content"].strip() != "":
                # If the last message is from user and is not empty, let the writer to continue
                return planner

        # elif last_speaker is engineer:
        #     if "```python" in messages[-1]["content"] or "pip install" in messages[-1]["content"]:
        #         # If the last message is a python code block, let the executor to speak
        #         return code_executor
        #     else:
        #         # Otherwise, let the engineer to continue
        #         return engineer

        # elif last_speaker is code_executor:
        #     if "exitcode: 1" in messages[-1]["content"]:
        #         # If the last message indicates an error, let the engineer to improve the code
        #         return engineer
        #     else:
        #         # Otherwise, let the writer to speak
        #         return writer

        elif last_speaker is critic:
            # Always let the user to speak after the writer
            return user_proxy

        else:
            # default to auto speaker selection method
            return "auto"


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

        # # Google search
        # results = search_internet(connexion_id=google_engine_id,
        #                          api_key=google_key,
        #                          query="'Yannick GOBERT'")


        print("Additional filter")
        filter_dict = {"model": ["gpt-35-turbo-16k"]}
        llm_config_lits_gpt3 = autogen.filter_config(available_llm_config_list, filter_dict)
        print(llm_config_lits_gpt3)
        assert len(llm_config_lits_gpt3) >= 1

        filter_dict = {"model": ["gpt-4-32k"]}
        llm_config_lits_gpt4 = autogen.filter_config(available_llm_config_list, filter_dict)
        print(llm_config_lits_gpt4)
        assert len(llm_config_lits_gpt4) >= 1

        gpt3_config = {
            "cache_seed": 42,  # change the cache_seed for different trials
            "temperature": 0,
            "config_list": llm_config_lits_gpt3,
            "timeout": 120,
        }

        gpt4_config = {
            "cache_seed": 0,  # change the cache_seed for different trials
            "temperature": 0,
            "config_list": llm_config_lits_gpt4,
            "timeout": 120,
        }


        print("Declare agents")
        user_proxy = autogen.UserProxyAgent(
            name=prompts[ "admin" ][ "assistant_name" ],
            system_message=prompts[ "admin" ][ "prompt" ],
            code_execution_config=False,
        )

        planner = autogen.AssistantAgent(
            name=prompts[ "planner" ][ "assistant_name" ],
            llm_config={
                # "cache_seed": 42,  # change the cache_seed for different trials
                "temperature": prompts[ "planner" ][ "temperature" ],
                "config_list": llm_config_lits_gpt3,
                "timeout": 120,
            },
            system_message=prompts[ "planner" ][ "prompt" ],
            description="This is the planner agent",
            is_termination_msg=lambda x: "content" in x
                and x["content"] is not None
                and (x["content"].rstrip().endswith("TERMINATE") or x["content"].rstrip().endswith("EXIT")),
            max_consecutive_auto_reply=1

        )

        researcher_manager = autogen.AssistantAgent(
            name=prompts[ "researcher_manager" ][ "assistant_name" ],
            llm_config=gpt3_config,
            system_message=prompts[ "researcher_manager" ][ "prompt" ],
            human_input_mode="ALWAYS",  # Never ask for human input.
            description="This is the researcher_manager agent"
        )

        researcher = autogen.AssistantAgent(
            name=prompts[ "researcher" ][ "assistant_name" ],
            llm_config=gpt3_config,
            system_message=prompts[ "researcher" ][ "prompt" ],
            description="This is the researcher agent"
        )

        scientist = autogen.AssistantAgent(
            name=prompts[ "scientist" ][ "assistant_name" ],
            llm_config={
                "cache_seed": 42,  # change the cache_seed for different trials
                "temperature": prompts[ "scientist" ][ "temperature" ],
                "config_list": llm_config_lits_gpt3,
                "timeout": 120,
            },
            system_message=prompts[ "scientist" ][ "prompt" ],
            description="This is the scientist agent"
        )

        executor = autogen.UserProxyAgent(
            name="Executor",
            system_message="Executor. Execute the code written by the engineer and report the result.",
            human_input_mode="NEVER",
            code_execution_config={
                "last_n_messages": 3,
                "work_dir": "paper",
                "use_docker": False,
            },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
        )

        critic = autogen.AssistantAgent(
            name=prompts[ "critic" ][ "assistant_name" ],
            system_message=prompts[ "critic" ][ "prompt" ],
            llm_config={
                "temperature": prompts[ "critic" ][ "temperature" ],
                "config_list": llm_config_lits_gpt3,
            },
            description="This is the critic agent",
            is_termination_msg=lambda x: "content" in x
                and x["content"] is not None
                and (x["content"].rstrip().endswith("TERMINATE") or x["content"].rstrip().endswith("EXIT")),
            max_consecutive_auto_reply=1
        )

        register_function(
            search_internet,
            caller=researcher,
            executor=executor,
            name="google_search",
            description="search keywords with google search")


        graph_dict = {}
        graph_dict[user_proxy] = [planner]
        graph_dict[planner] = [critic, user_proxy]
        graph_dict[critic] = [planner]

        groupchat = autogen.GroupChat(
            # agents=[user_proxy, planner, scientist, researcher, researcher_manager, executor], messages=[], max_round=50
            agents=[user_proxy, researcher, researcher_manager ],
            messages=[
                "Start to work with the researcher_manager"
            ],
            # speaker_selection_method=custom_speaker_selection_func,
            allowed_or_disallowed_speaker_transitions=graph_dict,
            speaker_transitions_type="allowed",
            max_round=5
        )
        group_chat_manager  = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt3_config)

        print("Start the chat")
        user_proxy.initiate_chat(
            group_chat_manager ,
            # message="""
            # find contribution for code from Yannick GOBERT a devops engineer on internet, he can be known with his alias ygo or ygo74
            # """,
            message="""
            I want to hire a new employee, I need to know if this person can fit with my objectives to develop a dotnet microservices application.
            This application will follow Domain driven Design approach, It uses Graphql, fluentvalidation, mediator libraries.
            It is deployed on Azure Kubernetes servies.
            Can you confirm that Yannick GOBERT fits this role ?
            """,
        )



    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()