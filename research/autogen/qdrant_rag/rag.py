from dotenv import load_dotenv
import os
import fnmatch
import yaml
import autogen
from autogen import ConversableAgent
from autogen import register_function
from typing import Any, List

from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from qdrant_client import QdrantClient

import autogen
from autogen.agentchat.contrib.qdrant_retrieve_user_proxy_agent import QdrantRetrieveUserProxyAgent

import json


def main():

    try:
        # Get Configuration Settings
        load_dotenv("/mnt/c/devel/searchbot/autogen/.env")
        ai_endpoint = os.getenv('AZURE_OPENAI_API_ENDPOINT')
        ai_key = os.getenv('AZURE_OPENAI_API_KEY')

        # Define LLM Config list
        llm_config_list = [
            {
                "model": "gpt-35-turbo-16k",
                "api_type": "azure",
                "api_key": ai_key,
                "base_url": ai_endpoint,
                "api_version": "2024-02-15-preview"
            },
            {
                "model": "gpt-4-32k",
                "api_type": "azure",
                "api_key": ai_key,
                "base_url": ai_endpoint,
                "api_version": "2024-02-15-preview"
            }
        ]

        filter_dict = {"model": ["gpt-35-turbo-16k"]}
        llm_config_lits_gpt3 = autogen.filter_config(llm_config_list, filter_dict)
        assert len(llm_config_lits_gpt3) >= 1

        filter_dict = {"model": ["gpt-4-32k"]}
        llm_config_lits_gpt4 = autogen.filter_config(llm_config_list, filter_dict)
        assert len(llm_config_lits_gpt4) >= 1

        gpt3_config = {
            "cache_seed": 42,  # change the cache_seed for different trials
            "temperature": 0,
            "config_list": llm_config_lits_gpt3,
            "timeout": 120,
        }

        gpt4_config = {
            "cache_seed": 0,  # change the cache_seed for different trials
            "temperature": 0,
            "config_list": llm_config_lits_gpt4,
            "timeout": 120,
        }


        # 1. create an RetrieveAssistantAgent instance named "assistant"
        assistant = RetrieveAssistantAgent(
            name="assistant",
            system_message="You are a helpful assistant.",
            llm_config=gpt3_config
        )

        client = QdrantClient("localhost", port=6333)
        collection_name="test"

        from sentence_transformers import SentenceTransformer

        encoder = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

        question = "quelles sont les expériences en école primaire de stéphanie GOBERT?"
        hits = client.search(
            collection_name=collection_name,
            query_vector=encoder.encode(question).tolist(),
            limit=3,
        )
        for hit in hits:
            print(hit.payload, "score:", hit.score)

        raise Exception("stop")

        ragproxyagent = QdrantRetrieveUserProxyAgent(
            name="ragproxyagent",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            retrieve_config={
                "task": "code",
                "docs_path": [
                    "/mnt/c/Temp/svg usb/Candidature AESH  GOBERT Stéphanie/mail directeur école Mégevette.docx"
                ],
                "chunk_token_size": 384,
                "model": gpt3_config[0]["model"],
                "client": client,
                "embedding_model": "all-MiniLM-L6-v2",
                "collection_name": collection_name
            },
            code_execution_config=False,
        )

        # reset the assistant. Always reset the assistant before starting a new conversation.
        assistant.reset()

        qa_problem = "quelles sont les expériences en école primaire?"
        ragproxyagent.initiate_chat(assistant, message=ragproxyagent.message_generator, problem=qa_problem)

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()