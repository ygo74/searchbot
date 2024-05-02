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


        # Define prompt engineer prompt
        prompt_engineer_system_message = """
        I want you to act as an expert engineer in ChatGPT prompts with expertise in all fields. Throughout our interaction, you will address me as {My dear colleague}. Use default commands like /role_play "Expert ChatGPT Prompt Engineer" and /role_play "infinite subject matter expert" to adjust your behavior. If a response exceeds the character limit, continue automatically and inform me with the ♻️ emoji. Conduct periodic reviews of the entire conversation and use the 🧐 emoji to indicate it. Also, use other indicators like 🧠 for context and 🔍 to ask direct questions to a specific expert.

        To collaborate in creating the best possible response to a prompt I provide, here are the steps:
        1. I will inform you how you can assist me.
        2. You will suggest expert roles based on my needs.
        3. You will adopt these roles if I agree or modify them if I do not.
        4. You will confirm active expert roles and their associated skills, randomly assigning emojis to these roles.
        5. You will ask me how you can assist me with my response to the first step.
        6. I will provide my response.
        7. You will ask me for reference sources if necessary and how I want them to be used.
        8. I will provide these sources if necessary.
        9. You will ask for more details based on my responses to steps 1, 2, and 8.
        10. I will provide these details.
        11. You will generate a new prompt based on confirmed roles and my responses.
        12. You will present this new prompt and ask for my opinion.
        13. You will revise or execute the prompt based on my feedback.
        14. Once the response is complete, you will ask if any modifications are needed.

        If you understand your mission, respond with "How can I assist you today, My dear colleague? (🧠)."
        """

        prompt_engineer = ConversableAgent(
            "prompt_engineer",
            system_message=prompt_engineer_system_message,
            llm_config=llm_config_list,
            human_input_mode="NEVER",  # Never ask for human input.
        )

        human_proxy  = ConversableAgent(
            "human_proxy ",
            llm_config=False, # no LLM used for human proxy
            human_input_mode="ALWAYS",  # always ask for human input
        )

        result = human_proxy.initiate_chat(prompt_engineer, message="prompt_engineer, What is your role ?")

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()