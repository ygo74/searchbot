---
layout: default
grand_parent: AI Services
parent: Azure AI Services
title: Language Services
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

Azure AI Language is a cloud-based service that provides Natural Language Processing (NLP) features for understanding and analyzing text. Use this service to help build intelligent applications using the web-based Language Studio, REST APIs, and client libraries.

## Capabilities

| Capabilities | Link |
|:------------ |:---- |
| Custom text classification | <https://learn.microsoft.com/en-us/azure/ai-services/language-service/custom-text-classification/overview>{:target="_blank"} |
| Conversational language understanding | <https://learn.microsoft.com/en-us/azure/ai-services/language-service/conversational-language-understanding/overview>{:target="_blank"} |
| Entity linking | <https://learn.microsoft.com/en-us/azure/ai-services/language-service/entity-linking/overview>{:target="_blank"} |
| Language detection | <https://learn.microsoft.com/en-us/azure/ai-services/language-service/language-detection/overview>{:target="_blank"} |
| Key phrase extraction | <https://learn.microsoft.com/en-us/azure/ai-services/language-service/key-phrase-extraction/overview>{:target="_blank"} |
| Named Entity Recognition | <https://learn.microsoft.com/en-us/azure/ai-services/language-service/named-entity-recognition/overview>{:target="_blank"} |
| Orchestration workflow | <https://learn.microsoft.com/en-us/azure/ai-services/language-service/orchestration-workflow/overview>{:target="_blank"} |
| Personal Identifiable Information detection | <https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/overview>{:target="_blank"} |
| Custom question answering | <https://learn.microsoft.com/en-us/azure/ai-services/language-service/question-answering/overview>{:target="_blank"} |
| Sentiment Analysis | <https://learn.microsoft.com/en-us/azure/ai-services/language-service/sentiment-opinion-mining/overview?tabs=prebuilt>{:target="_blank"} |
| Text Analysis for health | <https://learn.microsoft.com/en-us/azure/ai-services/language-service/text-analytics-for-health/overview?tabs=ner>{:target="_blank"} |
| Summarization | <https://learn.microsoft.com/en-us/azure/ai-services/language-service/summarization/overview?tabs=text-summarization>{:target="_blank"} |

## Azure Deployment

Create language resource : <https://portal.azure.com/#create/Microsoft.CognitiveServicesTextAnalytics>{:target="_blank"}

## Local deployment

### How-to

- Use container : <https://learn.microsoft.com/fr-fr/azure/ai-services/language-service/overview#deploy-on-premises-using-docker-containers>{:target="_blank"}
- Quick start : <https://learn.microsoft.com/fr-fr/azure/ai-services/language-service/key-phrase-extraction/quickstart?pivots=programming-language-csharp>{:target="_blank"}

``` powershell

$endPointUri = ""
$apiKey = ""

docker run --rm -it -p 5000:5000 --memory 4g --cpus 1 \
mcr.microsoft.com/azure-cognitive-services/textanalytics/keyphrase \
Eula=accept \
Billing=$endPointUri \
ApiKey=$apiKey

```

``` bash

endpointUri=""
apiKey=""

docker run --rm -it -p 5000:5000 --cpus 1 \
-e Eula=accept \
-e Billing=$endpointUri \
-e ApiKey=$apiKey \
-e Logging:Console:LogLevel:Default=Debug \
mcr.microsoft.com/azure-cognitive-services/textanalytics/keyphrase

```

Test : <http://localhost:5000/swagger/index.html>{:target="_blank"}


### Available containers

| Capabilities                                | Link |
|:------------------------------------------- |:---- |
| Custom text classification                  |  |
| Conversational language understanding       |  |
| Entity linking                              |  |
| Language detection                          |  |
| Key phrase extraction                       | docker pull mcr.microsoft.com/azure-cognitive-services/textanalytics/keyphrase |
| Named Entity Recognition                    | docker pull mcr.microsoft.com/azure-cognitive-services/textanalytics/ner:latest <br/>docker pull mcr.microsoft.com/azure-cognitive-services/textanalytics/customner:3.0.72991232-onprem-amd64 |
| Orchestration workflow                      |  |
| Personal Identifiable Information detection |  |
| Custom question answering                   |  |
| Sentiment Analysis                          |  |
| Text Analysis for health                    |  |
| Summarization                               | docker pull mcr.microsoft.com/azure-cognitive-services/textanalytics/summarization:cpu |
