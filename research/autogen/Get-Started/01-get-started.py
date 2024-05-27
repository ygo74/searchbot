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
        llm_config_list = [
            {
                "model": "gpt-35-turbo-16k",
                "api_type": "azure",
                "api_key": ai_key,
                "base_url": ai_endpoint,
                "api_version": "2024-02-15-preview",
                "tags": "openai"
            },
            {
                "model": "Phi-3-mini-4k-instruct-q4",
                "base_url": "http://127.0.0.1:8000/v1",
                "api_type": "openai",
                "api_key": "nothing",
                "tags": "phi3"
            }
        ]


        filter_dict = {"tags": ["openai"]}
        config_list = autogen.filter_config(llm_config_list, filter_dict)

        cathy = ConversableAgent(
            "cathy",
            system_message="Your name is Cathy and you are a part of a duo of comedians.",
            llm_config={
                "config_list": config_list,  # a list of OpenAI API configurations
            },
            human_input_mode="NEVER",  # Never ask for human input.
        )

        joe = ConversableAgent(
            "joe",
            system_message="Your name is Joe and you are a part of a duo of comedians.",
            llm_config={
                "config_list": config_list,  # a list of OpenAI API configurations
            },
            human_input_mode="NEVER",  # Never ask for human input.
        )

        result = joe.initiate_chat(cathy, message="Cathy, tell me a joke.", max_turns=2)

        autogen.runtime_logging.stop()

        # Write logs
        log_data = get_log()
        log_data_df = parse_detailed_logs(log_data)
        write_detailed_logs(log_data_df)
        write_summarized_logs(log_data_df, logging_session_id)

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()