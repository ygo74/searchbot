# https://microsoft.github.io/autogen/docs/topics/retrieval_augmentation

from dotenv import load_dotenv
import os
from autogen import ConversableAgent
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent

import chromadb

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
        solution_architect_system_message = """
        Welcome to our AI solution architect! I'm here to help you navigate the vast possibilities of artificial intelligence. As a specialized LLM, my primary goal is to assist you in creating innovative and efficient AI systems that can solve complex problems and improve user experiences. Whether you're looking to develop a chatbot for customer service or a recommendation engine for e-commerce, I'm here to guide you through the process with precision and accuracy.
        My language model is trained on a diverse range of texts related to AI and machine learning, including research papers, industry reports, and cutting-edge technologies. This allows me to provide informed and insightful suggestions tailored to your specific needs. I can help you brainstorm ideas, evaluate potential solutions, and refine your designs for maximum impact.
        However, my capabilities go beyond mere suggestion-making. I can also assist in the development of custom algorithms and models, leveraging my understanding of AI concepts and techniques to create tailored solutions that suit your requirements. Whether you're looking to develop a neural network for image recognition or an RNN for natural language processing, I'm here to help you every step of the way.
        So, what can I do for you today? Do you have a specific AI project in mind? Let me know, and I'll be happy to assist you in any way possible.
        """

        assistant = RetrieveAssistantAgent(
            name="prompt_engineer",
            system_message=solution_architect_system_message,
            llm_config={
                "timeout": 600,
                "cache_seed": 42,
                "config_list": llm_config_list[ "config_list" ],
            }
        )

        ragproxyagent = RetrieveUserProxyAgent(
            name="ragproxyagent",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=3,
            retrieve_config={
                "task": "code",
                "docs_path": [
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/445907062/Analytics",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/446267562/Benchmarking",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/446234809/Ingestion",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/445776007/Theming",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/476905480/RAG+Assessment+and+Improvement",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/445743355/Recording",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/445612496/Sharepoint+Connector",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/445579339",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/445251891",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/445808866/Secure+Software+Development+Lifecycle",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/446267478/Concepts",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/445743377/Architecture",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/446136370/Deployment+models",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/445907150/Platform+as+a+Service",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/445808926/Single+Tenant",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/445972706/Get+started+with+a+Single+Tenant",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/446202003/Service+Level+Agreement+-+Single+Tenant",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/446234783/Infrastructure+requirements",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/446234728/Releases",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/445612477/Creating+scopes+via+API",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/445775988/Incorporate+Company-Specific+Terminology",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/445251913/IAM+configuration",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/445775966/Assistant+module+settings",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/457441304/Co-Development+Governance+Framework",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/458260493/Solution+Design+for+Code+Implementation",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/457441332/GitHub+Code+Contribution+Guide",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/445612410/Security+Compliance",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/444957005/Compliance+layer",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/470024216",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/470679594/Organisation+User+Access+(OUA)+Request",
                    "https://unique-ch.atlassian.net/wiki/spaces/PUB/pages/446038288/Frequently+Asked+Questions+FaQ",
                    os.path.join(os.path.abspath(""), "..", "website", "docs"),
                ],
                "custom_text_types": ["mdx"],
                "chunk_token_size": 2000,
                "model": llm_config_list[ "config_list" ][0]["model"],
                "client": chromadb.PersistentClient(path="/tmp/chromadb"),
                "embedding_model": "all-mpnet-base-v2",
                # set to False if you don't want to reuse an existing collection, but you'll need to remove the collection manually
                "get_or_create": True,
            },
            code_execution_config=False,  # set to False if you don't want to execute the code
        )

        code_problem = "How can I use FinanceGPT to deploy ChatGPT solution to my enterprise."
        ragproxyagent.initiate_chat(
            assistant, message=ragproxyagent.message_generator, problem=code_problem
        )

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
