---
layout: default
grand_parent: Retrieval Augmented Generation
parent: Out-of-the-box services
title: Kernel Memory
nav_order: 1
has_children: false
---

Kernel Memory (KM) is a multi-modal AI Service specialized in the efficient indexing of datasets through custom continuous data hybrid pipelines, with support for Retrieval Augmented Generation (RAG), synthetic memory, prompt engineering, and custom semantic memory processing.

{: .warning }
> kernel Memory is a demonstration and is not an officially supported Microsoft offering.

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Sources

- <https://github.com/microsoft/kernel-memory/tree/main>{:target="_blank"}
- <https://microsoft.github.io/kernel-memory/>{:target="_blank"}

## Execution environment

### Kernel Memory Service configuration

The Kernel memory services can be configured thanks to the asp.net configuration file. You can find a sample in the repository [here](https://github.com/ygo74/searchbot/blob/main/research/semantic_kernel/backends/appsettings.Development.sample.json){:target="_blank"}.
You can also configure it with the setup tools in the Kernel Memory repository.

1. Text Generation Service

    1. Configure the service used for Text generation

        - key : TextGeneratorType

          value: Service name (e.g. AzureOpenAIText)

        ``` json
        {
            "KernelMemory": {
                "Service": {
                    "RunWebService": true,
                    "RunHandlers": true,
                    "OpenApiEnabled": true,
                    "Handlers": {
                        ...
                    }
                },
                "ContentStorageType": "",
                "DocumentStorageType": "SimpleFileStorage",
                "TextGeneratorType": "AzureOpenAIText"
            }
        }
        ```

    1. Configure the service

        ``` json
        {
            "KernelMemory": {
                "Services": {
                    "AzureOpenAIText": {
                        "APIType": "ChatCompletion",
                        "Auth": "ApiKey",
                        "Endpoint": "<YOUR AZURE OPEANAI URL>",
                        "Deployment": "<YOUR AZURE OPEANAI DEPLOYMENT MODEL NAME>",
                        "APIKey": "<YOUR AZURE OPEANAI API KEY>",
                        "MaxRetries": 10
                    },
                }
            }
        }
        ```

1. Text embedding service

    1. Configure the service

        ``` json
        {
            "KernelMemory": {
                "Services": {
                    "AzureOpenAIEmbedding": {
                        "Auth": "ApiKey",
                        "Endpoint": "<YOUR AZURE OPEANAI URL>",
                        "APIKey": "<YOUR AZURE OPEANAI API KEY>",
                        "Deployment": "<YOUR AZURE OPEANAI EMBEDDING DEPLOYMENT MODEL NAME>",
                        "MaxTokenTotal": 8191,
                        "EmbeddingDimensions": null,
                        "APIType": "EmbeddingGeneration"
                    },
                }
            }
        }
        ```

1. Data Ingestion

    ``` json
    {
        "KernelMemory": {
            "DataIngestion": {
            "OrchestrationType": "Distributed",
            "DistributedOrchestration": {
                "QueueType": "RabbitMQ"
            },
            "EmbeddingGenerationEnabled": true,
            "EmbeddingGeneratorTypes": [
                "AzureOpenAIEmbedding"
            ],
            "MemoryDbTypes": [
                "Qdrant"
            ],
            "MemoryDbUpsertBatchSize": 1,
            "ImageOcrType": "None",
            "TextPartitioning": {
                "MaxTokensPerParagraph": 1000,
                "MaxTokensPerLine": 300,
                "OverlappingTokens": 100
            },
            "DefaultSteps": []
            },
        }
    }

    ```

1. Retrieval

    ``` json
    {
        "KernelMemory": {
            "Retrieval": {
            "MemoryDbType": "Qdrant",
            "EmbeddingGeneratorType": "AzureOpenAIEmbedding",
            "SearchClient": {
                "MaxAskPromptSize": -1,
                "MaxMatchesCount": 100,
                "AnswerTokens": 8191,
                "EmptyAnswer": "INFO NOT FOUND",
                "Temperature": 0.0,
                "TopP": 0.0,
                "PresencePenalty": 0.0,
                "FrequencyPenalty": 0.0,
                "StopSequences": [],
                "TokenSelectionBiases": {}
            }
            },
        }
    }

    ```

### Docker

1. Create network

    ``` powershell
    docker network create kmnet
    ```

2. Start Qdrant

    ``` bash
    docker run --rm -it \
               -p 6333:6333 -p 6334:6334 \
               -v $(pwd)/qdrant_storage:/qdrant/storage:z \
               --network kmnet \
               --name qdrant \
               qdrant/qdrant

    ```

3. Start RabbitMQ

    ``` bash
    docker run -it --rm \
               -p 5672:5762 -p 15672:15672 \
               --name rabbitmq \
               --network kmnet \
               rabbitmq:3-management-alpine

    ```

4. Start Kernel Memory services

    ``` powershell
    docker run -it --rm `
               -v .\kernel-memory\service\Service\appsettings.Development.json:/app/appsettings.Production.json `
               -p 9001:9001 `
               --network kmnet `
               kernelmemory/service

    ```

### Docker compose

``` bash
docker compose -f docker-compose.yml up -d
```

{: .note }
> If services doesn't start, you can check the health state logs
>
> ``` bash
> docker inspect --format "{{json .State.Health }}" backends-rabbitmq-1
> ```
