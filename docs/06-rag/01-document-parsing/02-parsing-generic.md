---
layout: default
grand_parent: Retrieval Augmented Generation
parent: Documents parsing
title: Parsing All type of files
nav_order: 2
has_children: false
---

## Langchain Unstructured

### Python packages

``` bash
pip install langchain langchain-community
pip install unstructured
pip install unstructured[pdf]
```

### Research sample

File : research/rag/documents_parsing/03-parse-generic-documents-with-langchain-unstructured.py

``` bash

input_file_path="/tmp/my pdf file.pdf"
python research/rag/documents_parsing/03-parse-generic-documents-with-langchain-unstructured.py --file_path "$input_file_path"
```

## Langchain Azure Document Intelligence Service

Sources :

- <https://python.langchain.com/v0.2/docs/integrations/document_loaders/azure_document_intelligence/>{:target="_blank"}
- <https://azure.microsoft.com/fr-fr/pricing/details/ai-document-intelligence/>{:target="_blank"}


### Prerequisites

{: .warning }
> An Azure AI Document Intelligence resource in one of the 3 preview regions: East US, West US2, West Europe


### Python packages

``` bash
pip install langchain langchain-community azure-ai-documentintelligence
```


### Research sample

File : research/rag/documents_parsing/04-parse-generic-documents-with-langchain-AzureAIDocumentIntelligence.py

``` bash
input_file_path="/tmp/my pdf file.pdf"



```

