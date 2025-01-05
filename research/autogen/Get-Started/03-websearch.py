from dotenv import load_dotenv
import os
import asyncio
import argparse

from lib.llm import get_azure_model
from lib.websearch import google_search

from autogen_agentchat.agents import AssistantAgent

from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

import logging

from autogen_core import TRACE_LOGGER_NAME

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(TRACE_LOGGER_NAME)
logger.setLevel(logging.DEBUG)

planning_agent_prompt = """
You are a planning agent.
Your job is to break down complex tasks into smaller, manageable subtasks.
Your team members are:
    Web search agent: Searches for information
    Critic: Provide feedbacks on the plan

You only plan and delegate tasks - you do not execute them yourself.

When assigning tasks, use this format:
1. <agent> : <task>

After all tasks are complete, summarize the findings and end with "TERMINATE".
"""

web_search_agent_prompt = """
You are a web search agent.
Your only tool is search_tool - use it to find information.
You make only one search call at a time.
Once you have the results, you never do calculations based on them.
"""

async def main():

    # Get Configuration Settings
    load_dotenv()

    # Get the llm model
    llm = get_azure_model(
        deployment_name="gpt-4o",
        model_name="gpt-4o-2024-08-06"
    )

    # Create the planning agent
    planning_agent = AssistantAgent(
        name="PlanningAgent",
        description="An agent for planning tasks, this agent should be the first to engage when given a new task.",
        model_client=llm,
        system_message=planning_agent_prompt
    )

    # Create the web search agent
    web_search_agent = AssistantAgent(
        name="WebSearchAgent",
        description="A web search agent.",
        tools=[google_search],
        model_client=llm,
        system_message=web_search_agent_prompt,
    )


    # Create the critic agent.
    critic_agent = AssistantAgent(
        "critic",
        model_client=llm,
        system_message="""
        Critic. Double check plan, claims, code from other agents and provide feedback.
        Check whether the plan includes adding verifiable info such as source URL.
        """,
    )

    # response = await user_proxy_agent.on_messages(
    #         [TextMessage(content="What is your name? ", source="user")], cancellation_token=CancellationToken()
    # )

    # print(f"Your name is {response.chat_message.content}")

    text_mention_termination = TextMentionTermination("TERMINATE")
    max_messages_termination = MaxMessageTermination(max_messages=25)
    termination = text_mention_termination | max_messages_termination

    team = SelectorGroupChat(
        [planning_agent, web_search_agent, critic_agent],
        model_client=llm,
        termination_condition=termination,
    )

    search_task = "How to get started with autogen magentic one"
    # Use `asyncio.run(Console(reflection_team.run_stream(task="Write a short poem about fall season.")))` when running in a script.
    await Console(
        team.run_stream(task=search_task)
    )  # Stream the messages to the console.

if __name__ == "__main__":
    asyncio.run(main())
