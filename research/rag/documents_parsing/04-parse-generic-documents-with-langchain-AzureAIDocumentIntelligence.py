# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
import os
import argparse
import logging

from dotenv import load_dotenv
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader


def main():

    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", help="file path")
    args = parser.parse_args()


    # Chemin du fichier PDF
    file_path = args.file_path
    filename = os.path.splitext(os.path.basename(file_path))[0]
    print(f"File Path : {file_path}")
    print(f"File Name : {filename}")

    endpoint = os.getenv("DI_SERVICE_ENDPOINT")
    key = os.getenv("DI_SERVICE_KEY")

    print(f"Endpoint : {endpoint}")

    loader = AzureAIDocumentIntelligenceLoader(
        api_endpoint=endpoint,
        api_key=key,
        file_path=file_path,
        api_model="prebuilt-layout",
        api_version="2024-02-29-preview"
    )

    documents = loader.load()
    print(documents)


if __name__ == "__main__":
    main()
