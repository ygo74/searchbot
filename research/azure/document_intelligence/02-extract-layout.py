import os
from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult

# Get Configuration Settings
load_dotenv()
endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]

print(endpoint)
print(key)


path_to_sample_documents="/mnt/c/Users/Administrator/Documents/repas.pdf"


document_intelligence_client = DocumentIntelligenceClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

with open(path_to_sample_documents, "rb") as f:
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout", analyze_request=f, content_type="application/octet-stream"
    )
result: AnalyzeResult = poller.result()

if result.styles and any([style.is_handwritten for style in result.styles]):
    print("Document contains handwritten content")
else:
    print("Document does not contain handwritten content")

for page in result.pages:
    print(f"----Analyzing layout from page #{page.page_number}----")
    print(f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}")

    if page.lines:
        for line_idx, line in enumerate(page.lines):
            words = get_words(page, line)
            print(
                f"...Line # {line_idx} has word count {len(words)} and text '{line.content}' "
                f"within bounding polygon '{line.polygon}'"
            )

            for word in words:
                print(f"......Word '{word.content}' has a confidence of {word.confidence}")

    if page.selection_marks:
        for selection_mark in page.selection_marks:
            print(
                f"Selection mark is '{selection_mark.state}' within bounding polygon "
                f"'{selection_mark.polygon}' and has a confidence of {selection_mark.confidence}"
            )

if result.tables:
    for table_idx, table in enumerate(result.tables):
        print(f"Table # {table_idx} has {table.row_count} rows and " f"{table.column_count} columns")
        if table.bounding_regions:
            for region in table.bounding_regions:
                print(f"Table # {table_idx} location on page: {region.page_number} is {region.polygon}")
        for cell in table.cells:
            print(f"...Cell[{cell.row_index}][{cell.column_index}] has text '{cell.content}'")
            if cell.bounding_regions:
                for region in cell.bounding_regions:
                    print(f"...content on page {region.page_number} is within bounding polygon '{region.polygon}'")

print("----------------------------------------")