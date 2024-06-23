---
layout: default
grand_parent: AI Services
parent: Azure AI Services
title: Document Intelligence
nav_order: 1
has_children: true
---

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

Azure AI Document Intelligence (formerly Form Recognizer) is a cloud-based Azure AI service that uses machine-learning models to automate your data processing in applications and workflows. Document Intelligence is essential for enhancing data-driven strategies and enriching document search capabilities.

## Available models


## Azure Deployment



## Local Deployment

Source : <https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/containers/install-run?view=doc-intel-3.0.0&preserve-view=true&tabs=business-card>{:target="_blank"}


``` bash
# Read
pip install python-dotenv
pip install azure-ai-formrecognizer

docker pull mcr.microsoft.com/azure-cognitive-services/form-recognizer/read-3.0


# General
docker pull mcr.microsoft.com/azure-cognitive-services/form-recognizer/document-3.0

# Layout
docker pull mcr.microsoft.com/azure-cognitive-services/form-recognizer/layout-3.0

```


``` bash

endpointUri = ""
apiKey = ""

docker run --rm -it -p 5000:5000 --cpus 1 \
-e Eula=accept \
-e Billing=$endpointUri \
-e ApiKey=$apiKey \
-e Logging:Console:LogLevel:Default=Debug \
mcr.microsoft.com/azure-cognitive-services/form-recognizer/read-3.0

```

``` bash

endpointUri = ""
apiKey = ""

docker run --rm -it -p 5000:5000 --cpus 1 \
-e Eula=accept \
-e Billing=$endpointUri \
-e ApiKey=$apiKey \
-e Logging:Console:LogLevel:Default=Debug \
mcr.microsoft.com/azure-cognitive-services/form-recognizer/layout-3.0

```

## Sources

- <https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence>{:target="_blank"}

source : <https://learn.microsoft.com/en-us/python/api/overview/azure/ai-formrecognizer-readme?view=azure-python&viewFallbackFrom=doc-intel-3.0.0#examples&preserve-view=true>{:target="_blank"}

``` bash
pip install azure-ai-formrecognizer
```
