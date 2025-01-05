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
    Research Manager : Provide directives to the web search agent
    Web search agent: Searches for information
    Critic: Provide feedbacks on the plan
    Redactor : Write the comprehensive and detailed human response

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

redactor_prompt = """
You are a redactor agent

You consolidated all information to create a human setp by step comprehensive report of information found by the team
You have the following capabilities:
1. You are able to categorize information found by the team.
2. You are able to categorize information in a table sorted by their importance
3. You can write a summary of found information
4. You are able to add samples and detailed information

You generate at the end a markdown page with the summary and the table.
"""

research_manager_prompt = """
You are a research manager, you are harsh, you are relentless.
You will work task by task.

You will firstly try to generate 2 actions web search agent can take to find the information needed.

Try to avoid G2, or other gated website that don't allow srcabing

You will reviewed the result from the researcher, and always push back if researcher didin't find the information.
Be persistent, say "No, you have to find the information, try again and propose 1 next method to try, if the researcher want to get away.

Only after researcher found the information needed, you will say "TERMINATE"
"""

researcher_prompt = """
You are a world class researcher, who can do detailed research on any topic and produce facts based results;
you do not make things up, you will try as hard as possible to gather facts & data to back up the research

Your only tool is search_tool - use it to find information.
You make only one search call at a time.
Once you have the results, you never do calculations based on them.

Please make sure you complete the objective above with the following rules:
1/ You should do enough research to gather as much information as possible about the objective
2/ If there are url of relevant links & articles, you will scrape it to gather more information
3/ After scraping & search, you should think "is there any new things i should search & scraping based on the data I collected to increase research quality?" If answer is yes, continue; But don't do this more than 3 iteratins
4/ You should not make things up, you should only write facts & data that you have gathered
5/ In the final output, You should include all reference data & links to back up your research; You should include all reference data & links to back up your research
6/ In the final output, You should include all reference data & links to back up your research; You should include all reference data & links to back up your research
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
        system_message=researcher_prompt,
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

    # Create the redactor agent.
    redactor_agent = AssistantAgent(
        "redactor",
        model_client=llm,
        system_message=redactor_prompt,
    )

    # Create the research manager
    research_manager_agent = AssistantAgent(
        "research_manager",
        model_client=llm,
        system_message=research_manager_prompt,
    )


    # response = await user_proxy_agent.on_messages(
    #         [TextMessage(content="What is your name? ", source="user")], cancellation_token=CancellationToken()
    # )

    # print(f"Your name is {response.chat_message.content}")

    text_mention_termination = TextMentionTermination("TERMINATE")
    max_messages_termination = MaxMessageTermination(max_messages=25)
    termination = text_mention_termination | max_messages_termination

    team = SelectorGroupChat(
        [research_manager_agent, web_search_agent],
        model_client=llm,
        termination_condition=termination,
    )

    search_task = "How to get started with 'magentic one' which is an application built thanks to Microsoft Autogen 0.4"
    # Use `asyncio.run(Console(reflection_team.run_stream(task="Write a short poem about fall season.")))` when running in a script.
    await Console(
        team.run_stream(task=search_task)
    )  # Stream the messages to the console.

if __name__ == "__main__":
    asyncio.run(main())
