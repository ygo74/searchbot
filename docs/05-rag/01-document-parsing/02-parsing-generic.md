---
layout: default
grand_parent: Retrieval Augmented Generation
parent: Documents parsing
title: Parsing All type of files
nav_order: 2
has_children: false
---

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Langchain Unstructured

Sources :

- <https://python.langchain.com/v0.2/docs/integrations/providers/unstructured/>{:target="_blank"}
- <https://github.com/Unstructured-IO/unstructured/>{:target="_blank"}

### Prerequisites

``` bash
sudo apt update

sudo apt-get install libmagic-dev
sudo apt-get install poppler-utils
sudo apt install tesseract-ocr
sudo apt install tesseract-lang
sudo apt install libtesseract-dev
sudo apt install pandoc
sudo apt install libreoffice

```

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
