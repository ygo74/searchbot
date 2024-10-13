from langchain_community.llms import VLLMOpenAI
from dotenv import load_dotenv

import argparse




def main():
    # Load environment variables from .venv
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="Model's name as defined in vLLM Server", default="microsoft/Phi-3-mini-4k-instruct")
    parser.add_argument("--api_base_url", help="Model's name as defined in vLLM", default="http://localhost:8000/v1")
    args = parser.parse_args()
    print(f"Script will use the model, {args.model}!")

    # Initialize model
    print("Initialize llm")
    llm = VLLMOpenAI(
        openai_api_key="EMPTY",
        openai_api_base=args.api_base_url,
        model_name=args.model,
        model_kwargs={"stop": ["."]},
    )
    print(llm.invoke("Rome is"))

    # from langchain_core.prompts import ChatPromptTemplate
    # prompt = ChatPromptTemplate.from_messages([
    #     ("user", "{input}")
    # ])
    # chain = prompt | llm

    # while True:
    #     llm_question = input("What is your question ? ")
    #     if llm_question.lower() == "/bye":
    #         print("Program end.")
    #         break
    #     else:
    #         llm_response = chain.invoke({"input": llm_question })
    #         print(llm_response)

if __name__ == "__main__":
    main()
