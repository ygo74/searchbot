from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

import argparse
import os

system_prompt= """
You are an address validation assistant using the GPT-4o model.
Your task is to receive postal addresses and validate their formatting.
You always must answer with a Json structure.
The Json structure will always contain the input address in the field input.
The Json structure must contain a field with the address status which must contain "OK", "KO" or "Unknown"
you will receive only the address to validate
If the address is not correctly formatted, you will try to correct the address and give the corrected address in the field output.
You will follow the country rules to format the address according its country.
If the address is correctly formatted, you will return the same address in the field output.


Exemples :
1. Correct Address
Prompt: "1600 Amphitheatre Parkway, Mountain View, CA 94043"
Expected result:
{{
    "status": "OK",
    "input": "1600 Amphitheatre Parkway, Mountain View, CA 94043",
    "output": "1600 Amphitheatre Parkway, Mountain View, CA 94043"
}}

2.  Wrong Address
Prompt: "Amphitheatre rd Parkway 1600, Mountain View, CA 94043"
Expected result:
{{
    "status": "KO",
    "input": "Amphitheatre rd Parkway 1600, Mountain View, CA 94043",
    "output": "1600 road Amphitheatre Parkway, Mountain View, CA 94043"
}}
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env_file_path", help="Environment file to connect to azure", default="./research/chat_completion/02-langchain/python/.env_openai")
    parser.add_argument("--model", help="Model's name as defined in Azure Deployment model", default="gpt-4o")
    parser.add_argument("--address", help="Addresse to validate", required=True)
    args = parser.parse_args()

    # Load environment variables from .venv
    load_dotenv(dotenv_path=args.env_file_path)
    azure_open_ai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

    print(f"Script will use the model : {args.model}")
    print(f"Script will use the Azure Openai endpoint: {azure_open_ai_endpoint}")

    # Initialize model
    print("Initialize llm")
    llm = AzureChatOpenAI(
        azure_deployment=args.model,
        api_version="2024-02-01",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )


    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            ("human", "{input}"),
        ]
    )

    chain = prompt | llm

    print("Invoke llm")
    result = chain.invoke(
        {
            "input": args.address,
        }
    )
    print(result)

if __name__ == "__main__":
    main()
