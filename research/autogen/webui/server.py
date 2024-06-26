from dotenv import load_dotenv
import panel as pn
import autogen
import os
import argparse
import sys
from autogen.coding import DockerCommandLineCodeExecutor, LocalCommandLineCodeExecutor


# Script identification
main_script_id = os.path.abspath(sys.argv[0])
main_script_name = os.path.basename(main_script_id)
print(f"Start python script : {main_script_name}")


# Parse arguments
model_tag="gpt4"

# Get Configuration Settings
load_dotenv()
ai_endpoint = os.getenv('AZURE_OPENAI_API_ENDPOINT')
ai_key = os.getenv('AZURE_OPENAI_API_KEY')
google_key = os.getenv('GOOGLE_SEARCH_API_KEY')
google_engine_id = os.getenv('GOOGLE_SEARCH_CENTER_CONNECTION_ID')
print(f"AI ENDPOINT : {ai_endpoint}")

# Load the list of models
available_llm_config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")

if model_tag is not None and model_tag != '':
    print(f"\tFilter models with tags : {model_tag}")
    filter_dict = {"tags": [model_tag]}
    llm_config_list = autogen.filter_config(available_llm_config_list, filter_dict)

# Ensure we have a configuration list of models
assert len(llm_config_list) > 0
llm_config = {"config_list": llm_config_list}

gpt4_config = {
    "cache_seed": 42,  # change the cache_seed for different trials
    "temperature": 0,
    "config_list": llm_config_list,
    "timeout": 120,
}
user_proxy = autogen.UserProxyAgent(
    name="Admin",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    system_message="""A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.
    Only say APPROVED in most cases, and say EXIT when nothing is to be done further. Do not say others.""",
    code_execution_config=False,
    default_auto_reply="Approved",
    human_input_mode="NEVER",
    llm_config=gpt4_config,
    max_consecutive_auto_reply=1
)

engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=gpt4_config,
    system_message="""Engineer. You follow an approved plan. You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
""",
    max_consecutive_auto_reply=1
)
scientist = autogen.AssistantAgent(
    name="Scientist",
    llm_config=gpt4_config,
    system_message="""Scientist. You follow an approved plan. You are able to categorize papers after seeing their abstracts printed. You don't write code.""",
    max_consecutive_auto_reply=1
)
planner = autogen.AssistantAgent(
    name="Planner",
    system_message="""Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
The plan may involve an engineer who can write code and a scientist who doesn't write code.
Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
""",
    llm_config=gpt4_config,
    max_consecutive_auto_reply=1
)

# Setting up code executor.
os.makedirs("coding", exist_ok=True)
# Use docker executor for running code in a container if you have docker installed.
code_executor = DockerCommandLineCodeExecutor(work_dir="coding")
# code_executor = LocalCommandLineCodeExecutor(work_dir="coding")

executor = autogen.UserProxyAgent(
    name="Executor",
    system_message="Executor. Execute the code written by the engineer and report the result.",
    human_input_mode="NEVER",
    code_execution_config={
        "last_n_messages": 3,
        "executor": code_executor
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    max_consecutive_auto_reply=1
)

critic = autogen.AssistantAgent(
    name="Critic",
    system_message="Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.",
    llm_config=gpt4_config,
    max_consecutive_auto_reply=1
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, engineer, scientist, planner, executor, critic], messages=[], max_round=10
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)


# Import and define the style of widgets to “materials”.
pn.extension(design="material")

# The enabler of the chatbot is to add a callback to handle the user’s input,
# any return of a message string or structured object will be automatically displayed on the conversation interface

def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    user_proxy.initiate_chat(manager, message=contents)

avatar = {user_proxy.name:"👨‍💼", engineer.name:"👩‍💻", scientist.name:"👩‍🔬", planner.name:"🗓", executor.name:"🛠", critic.name:'📝'}

def print_messages(recipient, messages, sender, config):

    chat_interface.send(messages[-1]['content'], user=messages[-1]['name'], avatar=avatar[messages[-1]['name']], respond=False)
    print(f"Messages from: {sender.name} sent to: {recipient.name} | num messages: {len(messages)} | message: {messages[-1]}")
    return False, None  # required to ensure the agent communication flow continues

user_proxy.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages,
    config={"callback": None},
)

engineer.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages,
    config={"callback": None},
)
scientist.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages,
    config={"callback": None},
)
planner.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages,
    config={"callback": None},
)

executor.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages,
    config={"callback": None},
)
critic.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages,
    config={"callback": None},
)
# Create a chat_interface that initials the Panel’s chat components implicitly.
chat_interface = pn.chat.ChatInterface(callback=callback)
chat_interface.send(
    "Enter a message in the TextInput below and receive an echo!",
    user="System",
    respond=False,
)
chat_interface.servable()
