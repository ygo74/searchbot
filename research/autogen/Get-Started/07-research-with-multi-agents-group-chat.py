import os
import sys
from typing import Annotated

from dotenv import load_dotenv
from modules.logging  import *
import argparse
from modules.assistant_configuration import load_prompts

import autogen
from autogen import ConversableAgent
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json, register_function
from autogen.agentchat.contrib.capabilities import teachability
from autogen.cache import Cache
from autogen.coding import DockerCommandLineCodeExecutor, LocalCommandLineCodeExecutor

from tavily import TavilyClient

def termination_msg(x):
    '''
    Define the termination message
    '''
    return isinstance(x, dict) and x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE")


def search_tool(query: Annotated[str, "The search query"]) -> Annotated[str, "The search results"]:
    return tavily.get_search_context(query=query, search_depth="advanced")

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

# Laod the list of models
llm_config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")

if args.model_tag is not None and args.model_tag != '':
    print(f"\tFilter models with tags : {args.model_tag}")
    filter_dict = {"tags": [args.model_tag]}
    llm_config_list = autogen.filter_config(llm_config_list, filter_dict)

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
tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

# Setting up code executor.
os.makedirs("coding", exist_ok=True)
# Use docker executor for running code in a container if you have docker installed.
# code_executor = DockerCommandLineCodeExecutor(work_dir="coding")
code_executor = LocalCommandLineCodeExecutor(work_dir="coding")

gpt_config = {
    "cache_seed": 42,  # change the cache_seed for different trials
    "temperature": 0,
    "config_list": llm_config_list,
    "timeout": 120,
}

user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="""
    A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.
    """,
    code_execution_config=False,
)

engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=gpt_config,
    system_message="""
    Engineer. You follow an approved plan. You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
    Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
    If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
    """,
)

scientist = autogen.AssistantAgent(
    name="Scientist",
    llm_config=gpt_config,
    system_message="""
    Scientist. You follow an approved plan. You are able to categorize papers after seeing their abstracts printed.
    You don't write code.
    """,
)
planner = autogen.AssistantAgent(
    name="Planner",
    system_message="""
    Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
    The plan may involve an engineer who can write code and a scientist who doesn't write code.
    Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
    """,
    llm_config=gpt_config,
)

executor = autogen.UserProxyAgent(
    name="Executor",
    system_message="Executor. Execute the code written by the engineer and report the result.",
    human_input_mode="NEVER",
    code_execution_config={
        "executor": code_executor,
        "last_n_messages": 3,
    },
)

critic = autogen.AssistantAgent(
    name="Critic",
    system_message="""
    Critic. Double check plan, claims, code from other agents and provide feedback.
    Check whether the plan includes adding verifiable info such as source URL.
    """,
    llm_config=gpt_config,
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, engineer, scientist, planner, executor, critic], messages=[], max_round=10
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt_config)

# Cache LLM responses. To get different responses, change the cache_seed value.
with Cache.disk(cache_seed=43) as cache:
    user_proxy.initiate_chat(
        manager,
        # message="""
        # I want to hire a new employee, I need to know if this person can fit with my objectives to develop a dotnet microservices application.
        # This application will follow Domain driven Design approach, It uses Graphql, fluentvalidation, mediator libraries.
        # It is deployed on Azure Kubernetes servies.
        # Can you confirm that Yannick GOBERT fits this role ?
        # """,
        message="""
        Find dotnet coding level of ygo74 who has repositories in github.com ?
        Determine if he is a junior developer, senior developer or solution architect.
        """,
        cache=cache,
    )
