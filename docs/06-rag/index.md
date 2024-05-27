---
layout: default
title: Retrieval Augmented Generation
nav_order: 6
has_children: false
---

- <https://github.com/Azure/gpt-rag>{:target="_blank"}
- <https://github.com/Azure/gpt-rag-ingestion>{:target="_blank"}

- <https://towardsdatascience.com/how-i-turned-my-companys-docs-into-a-searchable-database-with-openai-4f2d34bd8736>{:target="_blank"}

## unstructured documents

- <https://unstructured-io.github.io/unstructured/introduction.html>{:target="_blank"}

## Langchain Microsoft integration

- <https://python.langchain.com/docs/integrations/platforms/microsoft/>{:target="_blank"}

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

# Azure AI Analysis services
pip install azure-ai-textanalytics==5.3.0

```

<https://python.langchain.com/docs/integrations/document_loaders/microsoft_word/>{:target="_blank"}

``` python
from langchain_community.document_loaders import Docx2txtLoader
loader = Docx2txtLoader("example_data/fake.docx")
data = loader.load()
print(data)
```

## Web scraping

### commercial solutions

- <https://Browserless.io>

- <https://scrapingant.com>

  - <https://docs.scrapingant.com/python-client>

- <https://www.wintr.com>

- <https://scrapingbee.com>

- <https://www.scrapingdog.com>

- <https://proxiesapi.com>

