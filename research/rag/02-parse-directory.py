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


# embeddings
# https://python.langchain.com/docs/integrations/text_embedding/sentence_transformers/

print("".ljust(80,"="))
print("embeddings")
print("".ljust(80,"="))

from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
embedding_size = encoder.get_sentence_embedding_dimension()
print(f"embeddings size : {embedding_size}")


print("".ljust(80,"="))
print("parse files")
print("".ljust(80,"="))

from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=embedding_size, chunk_overlap=200)


from autogen.retrieve_utils import TEXT_FORMATS, get_files_from_dir, split_files_to_chunks
dir_path = "/mnt/c/Temp/"
files = get_files_from_dir(dir_path=dir_path, types=["docx"], recursive=True)

metadatas=[]

for i, file in enumerate(files):
    print(f'file {i} : {file}')

    # Parse with UnstructuredFileLoader
    # https://unstructured-io.github.io/unstructured/integrations.html#integration-with-langchain
    print(f"\tParse with UnstructuredFileLoader : {file}")
    loader = UnstructuredFileLoader(file)
    data = loader.load()

    # https://qdrant.tech/documentation/examples/rag-chatbot-scaleway/
    print(f"\tsplit document : {file}")

    chunks = text_splitter.split_documents(data)

    for i, chunk in enumerate(chunks):
        # Créer les métadonnées
        metadata = {"texte": chunk.page_content, "source": chunk.metadata[ "source" ]}
        metadatas.append(metadata)


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

client.upload_records(
    collection_name=collection_name,
    records=[
        models.Record(
            id=idx, vector=encoder.encode(doc["texte"]).tolist(), payload=doc
        )
        for idx, doc in enumerate(metadatas)
    ],
)
print("\tqdrant storage : OK")
