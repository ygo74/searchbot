from dotenv import load_dotenv
import os

from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
from langchain_community.document_loaders import UnstructuredFileLoader

try:
    from unstructured.partition.auto import partition

    HAS_UNSTRUCTURED = True
except ImportError:
    HAS_UNSTRUCTURED = False

TEXT_FORMATS = [
    "txt",
    "json",
    "csv",
    "tsv",
    "md",
    "html",
    "htm",
    "rtf",
    "rst",
    "jsonl",
    "log",
    "xml",
    "yaml",
    "yml",
    "pdf",
]
UNSTRUCTURED_FORMATS = [
    "doc",
    "docx",
    "epub",
    "msg",
    "odt",
    "org",
    "pdf",
    "ppt",
    "pptx",
    "rtf",
    "rst",
    "xlsx",
]  # These formats will be parsed by the 'unstructured' library, if installed.
if HAS_UNSTRUCTURED:
    TEXT_FORMATS += UNSTRUCTURED_FORMATS
    TEXT_FORMATS = list(set(TEXT_FORMATS))



# Document
file_path = "/mnt/c/Temp/ACTE DE CAUTIONNEMENT.docx"

# # Parse with Docx2txtLoader => Good result time
# print("".ljust(80,"="))
# print("Parse with Docx2txtLoader")
# print("".ljust(80,"="))
# loader = Docx2txtLoader(file_path)
# data = loader.load()
# print(data)

# # Parse with UnstructuredWordDocumentLoader => longer than Docx2txtLoader
# print("")
# print("".ljust(80,"="))
# print("Parse with UnstructuredWordDocumentLoader")
# print("".ljust(80,"="))
# loader = UnstructuredWordDocumentLoader(file_path)
# data = loader.load()
# print(data)

# # Parse with Document Intelligence Service East US, West US2, West Europe
# # Get Configuration Settings
# print("")
# print("".ljust(80,"="))
# print("Parse with Document Intelligence Service")
# print("".ljust(80,"="))
# load_dotenv()
# endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
# key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

# loader = AzureAIDocumentIntelligenceLoader(
#     api_endpoint=endpoint, api_key=key, file_path=file_path, api_model="prebuilt-layout"
# )

# documents = loader.load()

# print("")
# print("".ljust(80,"="))
# print("Parse with AutoGen retrieve utils")
# print("".ljust(80,"="))
# from autogen.retrieve_utils import TEXT_FORMATS, get_files_from_dir, split_files_to_chunks

# files=get_files_from_dir(dir_path='/mnt/c/Temp/', types=['docx'],recursive=False)
# print(files)
# chunks, sources = split_files_to_chunks(files=files,
#                                         max_tokens=400,
#                                         chunk_mode="multi_lines",
#                                         must_break_at_empty_line=False)

# for chunk_item in chunks:
#     print(chunk_item)


# Parse with UnstructuredFileLoader
# https://unstructured-io.github.io/unstructured/integrations.html#integration-with-langchain
print("".ljust(80,"="))
print("Parse with UnstructuredFileLoader")
print("".ljust(80,"="))
loader = UnstructuredFileLoader(file_path)
data = loader.load()
print(data)


# embeddings
# https://python.langchain.com/docs/integrations/text_embedding/sentence_transformers/

print("".ljust(80,"="))
print("embeddings")
print("".ljust(80,"="))

from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
embedding_size = encoder.get_sentence_embedding_dimension()
print(f"embeddings size : {embedding_size}")


# https://qdrant.tech/documentation/examples/rag-chatbot-scaleway/
print("".ljust(80,"="))
print("splits documents")
print("".ljust(80,"="))

from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=embedding_size, chunk_overlap=200)
chunks = text_splitter.split_documents(data)

i = 0
for split in chunks:
    i += 1
    print(f"split : {i}")
    print(split.page_content)


# embeddings
# https://python.langchain.com/docs/integrations/text_embedding/sentence_transformers/

# print("".ljust(80,"="))
# print("embeddings")
# print("".ljust(80,"="))

# from langchain_community.embeddings import HuggingFaceEmbeddings
# from sentence_transformers import SentenceTransformer
# from langchain_community.embeddings import SentenceTransformerEmbeddings
# from langchain_community.vectorstores import Qdrant

# encoder = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
# embeddings = encoder.encode(
#     [split.page_content for split in chunks],
#     show_progress_bar=True)

# i = 0
# for vector in embeddings:
#     i += 1
#     print(f"vector : {i}")
#     print(vector)


print("".ljust(80,"="))
print("qdrant storage")
print("".ljust(80,"="))

import logging

try:
    import fastembed
    from qdrant_client import QdrantClient, models
    from qdrant_client.fastembed_common import QueryResponse
except ImportError as e:
    logging.logger.fatal("Failed to import qdrant_client with fastembed. Try running 'pip install qdrant_client[fastembed]'")
    raise e

collection = None
client = QdrantClient("localhost", port=6333)
collection_name="test"

client.recreate_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=encoder.get_sentence_embedding_dimension(),  # Vector size is defined by used model
        distance=models.Distance.COSINE,
    ),
)

# Indexer les embeddings avec des métadonnées
from qdrant_client import QdrantClient, models

metadatas=[]
for i, chunk in enumerate(chunks):
    # Créer les métadonnées
    metadata = {"texte": chunk.page_content, "source": chunk.metadata[ "source" ]}
    metadatas.append(metadata)


client.upload_records(
    collection_name=collection_name,
    records=[
        models.Record(
            id=idx, vector=encoder.encode(doc["texte"]).tolist(), payload=doc
        )
        for idx, doc in enumerate(metadatas)
    ],
)

raise Exception("stop")


embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", device="cpu")

for split in splits:
    i += 1
    print(f"embedding for split : {i}")
    doc_result = embeddings.embed_documents([ split["page_content"] ])
    print(doc_result)


# import logging

# try:
#     import fastembed
#     from qdrant_client import QdrantClient, models
#     from qdrant_client.fastembed_common import QueryResponse
# except ImportError as e:
#     logging.logger.fatal("Failed to import qdrant_client with fastembed. Try running 'pip install qdrant_client[fastembed]'")
#     raise e

# collection = None
# client = QdrantClient("localhost", port=6333)
# collection_name="test"

# doc_store = Qdrant(
#     client=client, collection_name=collection_name,
#     embeddings=embeddings,
# )

# qdrant = Qdrant.from_documents(
#     docs,
#     embeddings,
#     collection_name=collection_name,
# )