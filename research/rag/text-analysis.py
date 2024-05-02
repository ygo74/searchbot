from dotenv import load_dotenv
import os

# import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from langchain_community.document_loaders import UnstructuredFileLoader

def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Create client using endpoint and key
        credential = AzureKeyCredential(ai_key)
        ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

        # Analyze each text file in the reviews folder
        file_path = "/mnt/c/Temp/ACTE DE CAUTIONNEMENT.docx"
        loader = UnstructuredFileLoader(file_path)
        data = loader.load()
        print(data[0].page_content)


        for doc in data:
            # Read the file contents
            print('\n-------------\n' + doc.metadata["source"])
            print('\n' + doc.page_content)

            # Get language
            detectedLanguage = ai_client.detect_language(documents=[doc.page_content])[0]
            print('\nLanguage: {}'.format(detectedLanguage.primary_language.name))

            # Get sentiment


            # Get key phrases
            phrases = ai_client.extract_key_phrases(documents=[doc.page_content])[0].key_phrases
            if len(phrases) > 0:
                print("\nKey Phrases:")
                for phrase in phrases:
                    print('\t{}'.format(phrase))

            # Get entities


            # Get linked entities



    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()