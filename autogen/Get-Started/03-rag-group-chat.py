# https://microsoft.github.io/autogen/docs/topics/retrieval_augmentation

from dotenv import load_dotenv
import os
import autogen
from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from typing_extensions import Annotated

import chromadb

def termination_msg(x):
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

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


        boss = autogen.UserProxyAgent(
            name="Boss",
            is_termination_msg=termination_msg,
            human_input_mode="NEVER",
            code_execution_config=False,  # we don't want to execute code in this case.
            default_auto_reply="Reply `TERMINATE` if the task is done.",
            description="The boss who ask questions and give tasks.",
        )

        boss_aid  = RetrieveUserProxyAgent(
            name="Boss_Assistant",
            is_termination_msg=termination_msg,
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


        coder = AssistantAgent(
            name="Senior_Python_Engineer",
            is_termination_msg=termination_msg,
            system_message="""
            You are a senior python engineer, you provide python code to answer questions.
            Reply `TERMINATE` in the end when everything is done.
            """,
            llm_config={
                "config_list": llm_config_list[ "config_list" ],
                "timeout": 60,
                "temperature": 0
            },
            description="Senior Python Engineer who can write code to solve problems and answer questions.",
        )

        # Define prompt engineer prompt
        solution_architect_system_message = """
        Welcome to our AI solution architect! I'm here to help you navigate the vast possibilities of artificial intelligence.

        As a specialized LLM, my primary goal is to assist you in creating innovative and efficient AI systems that can solve complex problems and improve user experiences. Whether you're looking to develop a chatbot for customer service or a recommendation engine for e-commerce, I'm here to guide you through the process with precision and accuracy.

        My language model is trained on a diverse range of texts related to AI and machine learning, including research papers, industry reports, and cutting-edge technologies. This allows me to provide informed and insightful suggestions tailored to your specific needs. I can help you brainstorm ideas, evaluate potential solutions, and refine your designs for maximum impact.

        However, my capabilities go beyond mere suggestion-making. I can also assist in the development of custom algorithms and models, leveraging my understanding of AI concepts and techniques to create tailored solutions that suit your requirements. Whether you're looking to develop a neural network for image recognition or an RNN for natural language processing, I'm here to help you every step of the way.
        So, what can I do for you today? Do you have a specific AI project in mind? Let me know, and I'll be happy to assist you in any way possible.

        Reply `TERMINATE` in the end when everything is done.
        """

        solution_architect_system_message2 = """
        You are a product manager. Reply `TERMINATE` in the end when everything is done."
        """

        solution_architect = autogen.AssistantAgent(
            name="Solution_Architect",
            is_termination_msg=termination_msg,
            system_message=solution_architect_system_message2,
            llm_config={
                "config_list": llm_config_list[ "config_list" ],
                "timeout": 60,
                "temperature": 0
            },
            description="Product Manager who can design and plan the project.",
        )

        reviewer = autogen.AssistantAgent(
            name="Code_Reviewer",
            is_termination_msg=termination_msg,
            system_message="You are a code reviewer. Reply `TERMINATE` in the end when everything is done.",
            llm_config={
                "config_list": llm_config_list[ "config_list" ],
                "timeout": 60,
                "temperature": 0
            },
            description="Code Reviewer who can review the code.",
        )

        # In this case, we will have multiple user proxy agents and we don't initiate the chat
        # with RAG user proxy agent.
        # In order to use RAG user proxy agent, we need to wrap RAG agents in a function and call
        # it from other agents.
        def retrieve_content(
            message: Annotated[
                str,
                "Refined message which keeps the original meaning and can be used to retrieve content for code generation and question answering.",
            ],
            n_results: Annotated[int, "number of results"] = 3,
        ) -> str:
            boss_aid.n_results = n_results  # Set the number of results to be retrieved.
            # Check if we need to update the context.
            update_context_case1, update_context_case2 = boss_aid._check_update_context(message)
            if (update_context_case1 or update_context_case2) and boss_aid.update_context:
                boss_aid.problem = message if not hasattr(boss_aid, "problem") else boss_aid.problem
                _, ret_msg = boss_aid._generate_retrieve_user_reply(message)
            else:
                _context = {"problem": message, "n_results": n_results}
                ret_msg = boss_aid.message_generator(boss_aid, None, _context)
            return ret_msg if ret_msg else message

        # Start
        boss_aid.human_input_mode = "NEVER"  # Disable human input for boss_aid since it only retrieves content.

        for caller in [solution_architect, coder, reviewer]:
            d_retrieve_content = caller.register_for_llm(
                description="retrieve content for code generation and question answering.", api_style="function"
            )(retrieve_content)

        for executor in [boss, solution_architect]:
            executor.register_for_execution()(d_retrieve_content)

        groupchat = autogen.GroupChat(
            agents=[boss, solution_architect, coder, reviewer],
            messages=[],
            max_round=12,
            speaker_selection_method="round_robin",
            allow_repeat_speaker=False,
        )

        manager = autogen.GroupChatManager(
            groupchat=groupchat,
            llm_config={
                "config_list": llm_config_list[ "config_list" ],
                "timeout": 60,
                "temperature": 0
            },
        )

        # Start chatting with the boss as this is the user proxy agent.
        code_problem = "How can I use FinanceGPT to deploy ChatGPT solution to my enterprise."
        boss.initiate_chat(
            manager,
            message=code_problem,
        )

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
