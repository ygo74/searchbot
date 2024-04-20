from dotenv import load_dotenv
import os
import fnmatch
import yaml
import autogen
from autogen import ConversableAgent
from autogen import register_function
from modules.logging import *
from modules.search.exception import *
from modules.search.googlesearch import *
from typing import Any, List

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

    try:
        # Get Configuration Settings
        load_dotenv("/mnt/c/devel/searchbot/autogen/.env")
        ai_endpoint = os.getenv('AZURE_OPENAI_API_ENDPOINT')
        ai_key = os.getenv('AZURE_OPENAI_API_KEY')
        google_key = os.getenv('GOOGLE_SEARCH_API_KEY')
        google_engine_id = os.getenv('GOOGLE_SEARCH_CENTER_CONNECTION_ID')

        # # Google search
        # results = search_internet(connexion_id=google_engine_id,
        #                          api_key=google_key,
        #                          query="'Yannick GOBERT'")

        current_path = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(current_path, 'prompts')
        prompts = load_prompts(prompt_path=prompt_path)

        for result in prompts:
            print( prompts[ result ] )


        # Define LLM Config list
        llm_config_list = [
            {
                "model": "gpt-35-turbo-16k",
                "api_type": "azure",
                "api_key": ai_key,
                "base_url": ai_endpoint,
                "api_version": "2024-02-15-preview"
            },
            {
                "model": "gpt-4-32k",
                "api_type": "azure",
                "api_key": ai_key,
                "base_url": ai_endpoint,
                "api_version": "2024-02-15-preview"
            }
        ]

        filter_dict = {"model": ["gpt-35-turbo-16k"]}
        llm_config_lits_gpt3 = autogen.filter_config(llm_config_list, filter_dict)
        assert len(llm_config_lits_gpt3) >= 1

        filter_dict = {"model": ["gpt-4-32k"]}
        llm_config_lits_gpt4 = autogen.filter_config(llm_config_list, filter_dict)
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

        # user_proxy = autogen.UserProxyAgent(
        #     name= prompts[ "admin" ][ "assistant_name" ],
        #     system_message=prompts[ "admin" ][ "prompt" ],
        #     code_execution_config=False,
        # )

        # engineer = autogen.AssistantAgent(
        #     name=prompts[ "engineer" ][ "assistant_name" ],
        #     llm_config=gpt4_config,
        #     system_message=prompts[ "engineer" ][ "prompt" ],
        # )

        # scientist = autogen.AssistantAgent(
        #     name=prompts[ "scientist" ][ "assistant_name" ],
        #     llm_config=gpt4_config,
        #     system_message=prompts[ "scientist" ][ "prompt" ],
        # )

        # planner = autogen.AssistantAgent(
        #     name=prompts[ "planner" ][ "assistant_name" ],
        #     llm_config=gpt4_config,
        #     system_message=prompts[ "planner" ][ "prompt" ],
        # )

        # executor = autogen.UserProxyAgent(
        #     name=prompts[ "executor" ][ "assistant_name" ],
        #     system_message=prompts[ "executor" ][ "prompt" ],
        #     human_input_mode="NEVER",
        #     code_execution_config={
        #         "last_n_messages": 3,
        #         "work_dir": "paper",
        #         "use_docker": False,
        #     },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
        # )

        # critic = autogen.AssistantAgent(
        #     name=prompts[ "critic" ][ "assistant_name" ],
        #     llm_config=gpt4_config,
        #     system_message=prompts[ "critic" ][ "prompt" ],
        # )


        # engineer = autogen.AssistantAgent(
        #     name="Engineer",
        #     llm_config=gpt4_config,
        #     system_message="""Engineer. You follow an approved plan. You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
        # Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
        # If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
        # """,
        # )

        # scientist = autogen.AssistantAgent(
        #     name="Scientist",
        #     llm_config=gpt4_config,
        #     system_message="""Scientist. You follow an approved plan. You are able to categorize papers after seeing their abstracts printed. You don't write code.""",
        # )
        # planner = autogen.AssistantAgent(
        #     name="Planner",
        #     system_message="""Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
        # The plan may involve an engineer who can write code and a scientist who doesn't write code.
        # Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
        # """,
        #     llm_config=gpt4_config,
        # )
        # executor = autogen.UserProxyAgent(
        #     name="Executor",
        #     system_message="Executor. Execute the code written by the engineer and report the result.",
        #     human_input_mode="NEVER",
        #     code_execution_config={
        #         "last_n_messages": 3,
        #         "work_dir": "paper",
        #         "use_docker": False,
        #     },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
        # )
        # critic = autogen.AssistantAgent(
        #     name="Critic",
        #     system_message="Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.",
        #     llm_config=gpt4_config,
        # )


        # groupchat = autogen.GroupChat(
        #     agents=[user_proxy, engineer, scientist, planner, executor, critic], messages=[], max_round=50
        # )
        # manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

        user_proxy = autogen.UserProxyAgent(
            name=prompts[ "admin" ][ "assistant_name" ],
            system_message=prompts[ "admin" ][ "prompt" ],
            code_execution_config=False,
        )

        planner = autogen.AssistantAgent(
            name=prompts[ "planner" ][ "assistant_name" ],
            llm_config={
                "cache_seed": 42,  # change the cache_seed for different trials
                "temperature": prompts[ "planner" ][ "temperature" ],
                "config_list": llm_config_lits_gpt3,
                "timeout": 120,
            },
            system_message=prompts[ "planner" ][ "prompt" ],
            description="This is the planner agent"
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
            llm_config=gpt4_config,
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
            description="This is the critic agent"
        )

        register_function(
            search_internet,
            caller=researcher,
            executor=executor,
            name="google_search",
            description="search keywords with google search")


        groupchat = autogen.GroupChat(
            # agents=[user_proxy, planner, scientist, researcher, researcher_manager, executor], messages=[], max_round=50
            agents=[user_proxy, planner, critic ],
            messages=[
                "Start to work with the planner"
            ], max_round=50
        )
        group_chat_manager  = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt3_config)


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