from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader

# Parse with Docx2txtLoader
loader = Docx2txtLoader("/mnt/c/Temp/ACTE DE CAUTIONNEMENT.docx")
data = loader.load()
print(data)

# Parse with UnstructuredWordDocumentLoader
loader = UnstructuredWordDocumentLoader("/mnt/c/Temp/ACTE DE CAUTIONNEMENT.docx")
data = loader.load()
print(data)

