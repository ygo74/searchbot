


https://github.com/Azure/gpt-rag
https://github.com/Azure/gpt-rag-ingestion



https://towardsdatascience.com/how-i-turned-my-companys-docs-into-a-searchable-database-with-openai-4f2d34bd8736


## unstructured documents

https://unstructured-io.github.io/unstructured/introduction.html


## Langchain Microsoft integration

https://python.langchain.com/docs/integrations/platforms/microsoft/


### Parse word documents

``` bash
pip install --upgrade langchain
pip install langchain_community
pip install docx2txt # requied for Docx2txtLoader
pip install unstructured # required for UnstructuredWordDocumentLoader
pip install python-docx # required for UnstructuredWordDocumentLoader
pip install azure-ai-documentintelligence


# embeddings
pip install sentence_transformers
pip install qdrant_client[fastembed]

```

https://python.langchain.com/docs/integrations/document_loaders/microsoft_word/

``` python
from langchain_community.document_loaders import Docx2txtLoader
loader = Docx2txtLoader("example_data/fake.docx")
data = loader.load()
print(data)
```