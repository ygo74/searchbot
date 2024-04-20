


https://github.com/Azure/gpt-rag
https://github.com/Azure/gpt-rag-ingestion


## Langchain Microsoft integration

https://python.langchain.com/docs/integrations/platforms/microsoft/


### Parse word documents

``` bash
pip install --upgrade --quiet  docx2txt # requied for Docx2txtLoader
pip install unstructured # required for UnstructuredWordDocumentLoader
pip install python-docx # required for UnstructuredWordDocumentLoader
pip install langchain_community
```

https://python.langchain.com/docs/integrations/document_loaders/microsoft_word/

``` python
from langchain_community.document_loaders import Docx2txtLoader
loader = Docx2txtLoader("example_data/fake.docx")
data = loader.load()
print(data)
```