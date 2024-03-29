from langchain_community.llms import Ollama

import argparse




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="Model's name as defined in Ollama", default="prompt_engineer")
    parser.add_argument("--ollama_base_url", help="Model's name as defined in Ollama", default="http://172.19.144.1:11434")
    args = parser.parse_args()
    print(f"Script will use the model, {args.model}!")

    # Initialize model
    print("Initialize llm")
    llm = Ollama(model=args.model, base_url=args.ollama_base_url)

    from langchain_core.prompts import ChatPromptTemplate
    prompt = ChatPromptTemplate.from_messages([
        ("user", "{input}")
    ])
    chain = prompt | llm

    while True:
        llm_question = input("What is your question ? ")
        if llm_question.lower() == "/bye":
            print("Program end.")
            break
        else:
            llm_response = chain.invoke({"input": llm_question })
            print(llm_response)

if __name__ == "__main__":
    main()
