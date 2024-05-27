# https://microsoft.github.io/autogen/docs/topics/task_decomposition
# Approach 1. Two-agent chat with function call for task decomposition

import os
from datetime import datetime
from typing import Callable, Dict, Literal, Optional, Union

from typing_extensions import Annotated

import autogen
from autogen import (
    Agent,
    AssistantAgent,
    ConversableAgent,
    GroupChat,
    GroupChatManager,
    UserProxyAgent,
    config_list_from_json,
    register_function,
)
from autogen.agentchat.contrib import agent_builder
from autogen.cache import Cache
from autogen.coding import DockerCommandLineCodeExecutor, LocalCommandLineCodeExecutor

from dotenv import load_dotenv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--model_tag", help="models tag to filter used models", default="gpt35")
args = parser.parse_args()

# Get Configuration Settings
print("Load azure environment variables")
load_dotenv()
ai_endpoint = os.getenv('AZURE_OPENAI_API_ENDPOINT')
ai_key = os.getenv('AZURE_OPENAI_API_KEY')

print(f"AZURE_OPENAI_API_ENDPOINT : {ai_endpoint}")

available_config_list = [
    {
        "model": "gpt-35-turbo-16k",
        "api_type": "azure",
        "api_key": ai_key,
        "base_url": ai_endpoint,
        "api_version": "2024-02-15-preview",
        "tags": ["gpt35","openai"]
    },
    {
        "model": "gpt-4-32k",
        "api_type": "azure",
        "api_key": ai_key,
        "base_url": ai_endpoint,
        "api_version": "2024-02-15-preview",
        "tags": ["gpt4","openai"]
    },
]

filter_dict = {"tags": [args.model_tag]}
config_list = autogen.filter_config(available_config_list, filter_dict)
assert len(config_list) > 0


gpt4_config = {
    "cache_seed": 42,  # change the cache_seed for different trials
    "temperature": 0,
    "config_list": config_list,
    "timeout": 120,
}

user_proxy = autogen.UserProxyAgent(
    name="Admin",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    system_message="""A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.
Only say APPROVED in most cases, and say EXIT when nothing is to be done further. Do not say others.
""",
    code_execution_config=False,
    default_auto_reply="Approved",
    human_input_mode="NEVER",
    llm_config={
        "cache_seed": 42,  # change the cache_seed for different trials
        "temperature": 0,
        "config_list": [available_config_list[1]],
        "timeout": 120,
    },
)

engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=gpt4_config,
    system_message="""Engineer. You follow an approved plan. You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
""",
)

scientist = autogen.AssistantAgent(
    name="Scientist",
    llm_config=gpt4_config,
    system_message="""Scientist. You follow an approved plan. You are able to categorize papers after seeing their abstracts printed. You don't write code.""",
)

planner = autogen.AssistantAgent(
    name="Planner",
    system_message="""Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
The plan may involve an engineer who can write code and a scientist who doesn't write code.
Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
""",
    llm_config=gpt4_config,
)


os.makedirs("paper", exist_ok=True)

executor = autogen.UserProxyAgent(
    name="Executor",
    system_message="Executor. Execute the code written by the engineer and report the result.",
    human_input_mode="NEVER",
    code_execution_config={
        "last_n_messages": 3,
        "executor": DockerCommandLineCodeExecutor(work_dir="paper"),
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
)

critic = autogen.AssistantAgent(
    name="Critic",
    is_termination_msg=lambda x: "content" in x
        and x["content"] is not None
        and (x["content"].rstrip().endswith("TERMINATE") or x["content"].rstrip().endswith("EXIT")),
    system_message="Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.",
    llm_config=gpt4_config,
)
groupchat = autogen.GroupChat(
    agents=[user_proxy, engineer, scientist, planner, executor, critic],
    messages=[],
    max_round=50
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

user_proxy.initiate_chat(
    manager,
    message="""
find papers on LLM applications from arxiv in the last week, create a markdown table of different domains.
""",
)