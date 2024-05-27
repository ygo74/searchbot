import ai_assistants.solution_architect_assistant
import argparse
import os
import sys
import autogen
import chromadb
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from ai_assistants.solution_architect_assistant import load_config_file, termination_msg

def main():
    print("Start Solution Architect Assistant")

    parser = argparse.ArgumentParser()
    parser.add_argument("--model_tag", help="models tag to filter used models", default="")
    parser.add_argument("--model_config_file", help="Models configuration file path", default="")
    parser.add_argument("--application_documentation_path", help="Application documentation path", default="")
    args = parser.parse_args()

    model_config_file=args.model_config_file
    if model_config_file is None or model_config_file == '':
        main_script_path = os.path.abspath(sys.argv[0])
        model_config_file = os.path.join(os.path.dirname(main_script_path), "solution_architect_assistant.json")

    print(f"\tLoad models configuration file from : {model_config_file}")
    config_list = load_config_file(model_config_file)

    if args.model_tag is not None and args.model_tag != '':
        print(f"\tFilter models with tags : {args.model_tag}")
        filter_dict = {"tags": [args.model_tag]}
        config_list = autogen.filter_config(config_list, filter_dict)

    # Ensure we have a configuration list of models
    assert len(config_list) > 0
    print(config_list)



    assistant = RetrieveAssistantAgent(
        name="assistant",
        system_message="You are a helpful assistant.",
        llm_config={
            "timeout": 600,
            "cache_seed": 42,
            "config_list": config_list,
        },
    )

    ragproxyagent = RetrieveUserProxyAgent(
        name="ragproxyagent",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=3,
        retrieve_config={
            "task": "code",
            "docs_path": [
                "https://raw.githubusercontent.com/microsoft/FLAML/main/website/docs/Examples/Integrate%20-%20Spark.md",
                "https://raw.githubusercontent.com/microsoft/FLAML/main/website/docs/Research.md",
                os.path.join(os.path.abspath(""), "..", "website", "docs"),
            ],
            "custom_text_types": ["mdx"],
            "chunk_token_size": 2000,
            "model": config_list[0]["model"],
            "client": chromadb.PersistentClient(path="/tmp/chromadb"),
            "embedding_model": "all-mpnet-base-v2",
            "get_or_create": True,  # set to False if you don't want to reuse an existing collection, but you'll need to remove the collection manually
        },
        code_execution_config=False,  # set to False if you don't want to execute the code
    )

    # reset the assistant. Always reset the assistant before starting a new conversation.
    assistant.reset()

    # given a problem, we use the ragproxyagent to generate a prompt to be sent to the assistant as the initial message.
    # the assistant receives the message and generates a response. The response will be sent back to the ragproxyagent for processing.
    # The conversation continues until the termination condition is met, in RetrieveChat, the termination condition when no human-in-loop is no code block detected.
    # With human-in-loop, the conversation will continue until the user says "exit".
    code_problem = "How can I use FLAML to perform a classification task and use spark to do parallel training. Train 30 seconds and force cancel jobs if time limit is reached."
    chat_result = ragproxyagent.initiate_chat(
        assistant, message=ragproxyagent.message_generator, problem=code_problem, search_string="spark"
    )  # search_string is used as an extra filter for the embeddings search, in this case, we only want to search documents that contain "spark".

if __name__ == "__main__":
    main()