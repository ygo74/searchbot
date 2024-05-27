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

# NOTE: this ReAct prompt is adapted from Langchain's ReAct agent: https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain/agents/react/agent.py#L79
ReAct_prompt = """
Answer the following questions as best you can. You have access to tools provided.

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take
Action Input: the input to the action
Observation: the result of the action
... (this process can repeat multiple times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!
Question: {input}
"""

# Define the ReAct prompt message. Assuming a "question" field is present in the context
def react_prompt_message(sender, recipient, context):
    return ReAct_prompt.format(input=context["question"])


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

user_proxy = UserProxyAgent(
    name="User",
    is_termination_msg=termination_msg,
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=10,
    code_execution_config={"executor": code_executor},
)

assistant = AssistantAgent(
    name="Assistant",
    system_message="Only use the tools you have been provided with. Reply TERMINATE when the task is done.",
    llm_config={
        "config_list": llm_config[ "config_list"],
        "cache_seed": None
    },
)

# Register the search tool.
register_function(
    search_tool,
    caller=assistant,
    executor=user_proxy,
    name="search_tool",
    description="Search the web for the given query",
)

# Cache LLM responses. To get different responses, change the cache_seed value.
with Cache.disk(cache_seed=None) as cache:
    user_proxy.initiate_chat(
        assistant,
        message=react_prompt_message,
        question="""
        comment tester les réponses d'un LLM ?
        """,
        cache=cache,
    )
