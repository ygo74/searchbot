from dotenv import load_dotenv
import os
from autogen import ConversableAgent

def main():

    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AZURE_OPENAI_API_ENDPOINT')
        ai_key = os.getenv('AZURE_OPENAI_API_KEY')

        # Define LLM Config list
        llm_config_list = {
            "config_list": [
                {
                    "model": "gpt-35-turbo-16k",
                    "api_type": "azure",
                    "api_key": ai_key,
                    "base_url": ai_endpoint,
                    "api_version": "2024-02-15-preview"
                }
            ]
        }

        cathy = ConversableAgent(
            "cathy",
            system_message="Your name is Cathy and you are a part of a duo of comedians.",
            llm_config=llm_config_list,
            human_input_mode="NEVER",  # Never ask for human input.
        )

        joe = ConversableAgent(
            "joe",
            system_message="Your name is Joe and you are a part of a duo of comedians.",
            llm_config=llm_config_list,
            human_input_mode="NEVER",  # Never ask for human input.
        )

        result = joe.initiate_chat(cathy, message="Cathy, tell me a joke.", max_turns=2)

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()