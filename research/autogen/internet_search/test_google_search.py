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

from scrapingant_client import ScrapingAntClient
from bs4 import BeautifulSoup

import json


from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureChatOpenAI
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain

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


def scrape_website(url: Annotated[str, "The url to scrape"]) -> Annotated[str, "The scrape result"]:
    # scrape website, and also will summarize the content based on objective if the content is too large
    # objective is the original objective & task that user give to the agent, url is the url of the website to be scraped

    print("Scraping website...")
    # Get Configuration Settings
    load_dotenv()
    scrapingant_api_key = os.getenv('SCRAPINGANT_API_KEY')
    print(f"api key : {scrapingant_api_key}")

    client = ScrapingAntClient(token=scrapingant_api_key)
    # Scrape the example.com site.
    result = client.general_request(url=url)
    # print(result.status_code)
    # print(result.content)
    # print(result.text)

    # # Define the headers for the request
    # headers = {
    #     'Cache-Control': 'no-cache',
    #     'Content-Type': 'application/json',
    # }

    # # Define the data to be sent in the request
    # data = {
    #     "url": url
    # }

    # # Convert Python object to JSON string
    # data_json = json.dumps(data)

    # # Send the POST request
    # post_url = f"https://chrome.browserless.io/content?token={brwoserless_api_key}"
    # response = requests.post(post_url, headers=headers, data=data_json)

    # Check the response status code
    if result.status_code == 200:
        soup = BeautifulSoup(result.content, "html.parser")
        text = soup.get_text()
        # print("CONTENTTTTTT:", text)

        if len(text) > 10000:

            output = summary("a research purpose", text)
            # print("SUMMARY:", output)
            return output
        else:
            return text
    else:
        print(f"HTTP request failed with status code {result.status_code}")

def summary(objective, content):
    llm = AzureChatOpenAI(
        temperature=0,
        model="gpt-35-turbo-16k",
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        azure_endpoint=os.getenv('AZURE_OPENAI_API_ENDPOINT'),
        openai_api_version="2024-02-15-preview"
    )

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=10000, chunk_overlap=500)
    docs = text_splitter.create_documents([content])
    map_prompt = """
    Write a summary of the following text for {objective}:
    "{text}"
    SUMMARY:
    """
    map_prompt_template = PromptTemplate(
        template=map_prompt, input_variables=["text", "objective"])

    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type='map_reduce',
        map_prompt=map_prompt_template,
        combine_prompt=map_prompt_template,
        verbose=True
    )

    input_args = {
        'input_documents': docs,
        'objective': objective
    }
    output = summary_chain.invoke(input=input_args)

    return output["output_text"]

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

def termination_msg(x):
    '''
    Define the termination message
    '''
    return isinstance(x, dict) and x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE")


def main():

    def search_tool(query: Annotated[str, "The search query"]) -> Annotated[str, "The search results"]:
        return tavily.get_search_context(query=query, search_depth="advanced")

    try:
        # Script identification
        main_script_id = os.path.abspath(sys.argv[0])
        main_script_name = os.path.basename(main_script_id)
        print(f"Start python script : {main_script_name}")


        # Call scrapingant
        # content = scrape_website("a research purpose", "https://www.promptingguide.ai/techniques/prompt_chaining")
        # print(content)
        # return

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
            human_input_mode="NEVER",  # Never ask for human input.
            description="This is the researcher_manager agent",
            is_termination_msg=termination_msg
        )

        researcher = autogen.AssistantAgent(
            name=prompts[ "researcher" ][ "assistant_name" ],
            llm_config={
                "config_list": llm_config[ "config_list"],  # a list of OpenAI API configurations
                "temperature": 0,  # temperature for sampling
            },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
            system_message=prompts[ "researcher" ][ "prompt" ],
            description="This is the researcher agent",
            is_termination_msg=termination_msg

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


        register_function(
            scrape_website,
            caller=researcher,
            executor=executor,
            name="scrape_website",
            description="scrape website content")


        graph_dict = {}
        graph_dict[user_proxy] = [researcher_manager]
        graph_dict[researcher_manager] = [researcher]
        graph_dict[researcher] = [researcher_manager]
        graph_dict[executor] = [researcher]


        groupchat = autogen.GroupChat(
            # agents=[user_proxy, planner, scientist, researcher, researcher_manager, executor], messages=[], max_round=50
            agents=[user_proxy, researcher, researcher_manager, executor],
            messages=[
                "Start to work with the researcher_manager"
            ],
            # speaker_selection_method=custom_speaker_selection_func,
            allowed_or_disallowed_speaker_transitions=graph_dict,
            speaker_transitions_type="allowed",
            max_round=20
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
            Find information for Microsoft Semantic Kernel and how to start with this framework
            """,
        )



    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()