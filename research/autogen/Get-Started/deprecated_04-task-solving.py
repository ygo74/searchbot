from dotenv import load_dotenv
import os
import sys
import autogen
from autogen import ConversableAgent
from modules.logging import *
import argparse

def termination_msg(x):
    '''
    Define the termination message
    '''
    return isinstance(x, dict) and x.get("content", "").rstrip().endswith("TERMINATE")

def main():

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

        # Laod the list of models
        llm_config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")

        if args.model_tag is not None and args.model_tag != '':
            print(f"\tFilter models with tags : {args.model_tag}")
            filter_dict = {"tags": [args.model_tag]}
            llm_config_list = autogen.filter_config(llm_config_list, filter_dict)

        # Ensure we have a configuration list of models
        assert len(llm_config_list) > 0
        llm_config = {"config_list": llm_config_list}

        # Start logging
        logging_session_id = autogen.runtime_logging.start(config={"dbname": "logs.db"})
        print("Logging session ID: " + str(logging_session_id))

        # create an AssistantAgent named "assistant"
        assistant = autogen.AssistantAgent(
            name="assistant",
            # system_message="""
            # if you need to retrieve additional information on Internet, you can generate the code to retrieve it.
            # Generated code van be executed by the user_proxy agent.
            # Return 'TERMINATE' when the task is done.
            # """,
            llm_config={
                "cache_seed": 41,  # seed for caching and reproducibility
                "config_list": llm_config[ "config_list"],  # a list of OpenAI API configurations
                "temperature": 0,  # temperature for sampling
            },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
            is_termination_msg=termination_msg,
        )

        # create a UserProxyAgent instance named "user_proxy"
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=termination_msg,
            code_execution_config={
                "work_dir": "coding",
                "use_docker": True,  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
            },
        )

        # the assistant receives a message from the user_proxy, which contains the task description
        chat_res = user_proxy.initiate_chat(
            assistant,
            # message="""What date is today? Compare the year-to-date gain for META and TESLA.""",
            # message="""
            # Can you summarize this page https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/445972706/Get+started+with+a+Single+Tenant to know what we have to think to deploy unique Finance GPT?
            # """,
            message="""
            Can you summarize this repository stored in https://github.com/ygo74/searchbot?
            Can you give information on the programmation language used in the repository ?
            Can you also inform what libraries are used for this application ?
            """,
            summary_method="reflection_with_llm",
        )

        autogen.runtime_logging.stop()

        # Write logs
        log_data = get_log()
        log_data_df = parse_detailed_logs(log_data)
        # write_detailed_logs(log_data_df)
        write_summarized_logs(log_data_df, logging_session_id)

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()