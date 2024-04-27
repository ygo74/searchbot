---
layout: default
parent: Azure
title: Azure containers
nav_order: 2
has_children: true
---

## Keyphrase

Source : <https://mcr.microsoft.com/product/azure-cognitive-services/textanalytics/keyphrase/about>{:target="_blank"}

Pull :  docker pull mcr.microsoft.com/azure-cognitive-services/textanalytics/keyphrase

How-to : <https://learn.microsoft.com/fr-fr/azure/ai-services/language-service/overview#deploy-on-premises-using-docker-containers>{:target="_blank"}

Quick start : <https://learn.microsoft.com/fr-fr/azure/ai-services/language-service/key-phrase-extraction/quickstart?pivots=programming-language-csharp>{:target="_blank"}

Create language resource : <https://portal.azure.com/#create/Microsoft.CognitiveServicesTextAnalytics>{:target="_blank"}

``` powershell

$endPointUri = ""
$apiKey = ""

docker run --rm -it -p 5000:5000 --memory 4g --cpus 1 \
mcr.microsoft.com/azure-cognitive-services/textanalytics/keyphrase \
Eula=accept \
Billing=$endPointUri \
ApiKey=$apiKey

```

Test : <http://localhost:5000/swagger/index.html>{:target="_blank"}

## Text Analytics Summarization

Source : <https://mcr.microsoft.com/product/azure-cognitive-services/textanalytics/summarization/about>{:target="_blank"}

``` bash
docker pull mcr.microsoft.com/azure-cognitive-services/textanalytics/summarization:cpu
```

## Text Analytics Custom NER

Source : <https://mcr.microsoft.com/product/azure-cognitive-services/textanalytics/customner/about>{:target="_blank"}

``` bash
docker pull mcr.microsoft.com/azure-cognitive-services/textanalytics/customner:3.0.72991232-onprem-amd64
```

## Text Analytics Named Entity Recognition

Source : <https://mcr.microsoft.com/product/azure-cognitive-services/textanalytics/ner/about>{:target="_blank"}

``` bash
docker pull mcr.microsoft.com/azure-cognitive-services/textanalytics/ner:latest
```

## Document Intelligence service

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