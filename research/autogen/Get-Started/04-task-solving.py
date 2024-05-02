from dotenv import load_dotenv
import os
import autogen
from autogen import ConversableAgent
from modules.logging import *

def main():

    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AZURE_OPENAI_API_ENDPOINT')
        ai_key = os.getenv('AZURE_OPENAI_API_KEY')

        # Start logging
        logging_session_id = autogen.runtime_logging.start(config={"dbname": "logs.db"})
        print("Logging session ID: " + str(logging_session_id))

        # Define LLM Config list
        llm_config_list = {
            "config_list": [
                {
                    "model": "gpt-4",
                    "api_type": "azure",
                    "api_key": ai_key,
                    "base_url": ai_endpoint,
                    "api_version": "2024-02-15-preview"
                }
            ]
        }

        # create an AssistantAgent named "assistant"
        assistant = autogen.AssistantAgent(
            name="assistant",
            llm_config={
                "cache_seed": 41,  # seed for caching and reproducibility
                "config_list": llm_config_list[ "config_list"],  # a list of OpenAI API configurations
                "temperature": 0,  # temperature for sampling
            },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
        )

        # create a UserProxyAgent instance named "user_proxy"
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={
                "work_dir": "coding",
                "use_docker": False,  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
            },
        )

        # the assistant receives a message from the user_proxy, which contains the task description
        chat_res = user_proxy.initiate_chat(
            assistant,
            # message="""What date is today? Compare the year-to-date gain for META and TESLA.""",
            message="""
            Can you summarize this page https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/445972706/Get+started+with+a+Single+Tenant to know what we have to think to deploy unique Finance GPT?
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