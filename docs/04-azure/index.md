---
layout: default
title: Azure
nav_order: 4
has_children: true
---

## Demo

- <https://github.com/Azure-Samples/azure-search-openai-demo/>{:target="_blank"}

## LangChain Integration

Sources:

- <https://python.langchain.com/v0.2/docs/integrations/text_embedding/azureopenai/>{:target="_blank"}

## Sources

- <https://techcommunity.microsoft.com/t5/ai-machine-learning-blog/deploy-large-language-models-responsibly-with-azure-ai/ba-p/3876792>{:target="_blank"}
- <https://techcommunity.microsoft.com/t5/azure-ai-services-blog/revolutionize-your-enterprise-data-with-chatgpt-next-gen-apps-w/ba-p/3762087>{:target="_blank"}
- <https://medium.com/@imicknl/how-to-create-a-private-chatgpt-with-your-own-data-15754e6378a1>{:target="_blank"}

- Architectures :

  - <https://learn.microsoft.com/en-us/azure/architecture/ai-ml/openai/idea/search-and-query-using-openai-service>{:target="_blank"}
  - <https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/conversational-bot>{:target="_blank"}

- EDGE MEC application solution accelerator : <https://github.com/Azure/mec-app-solution-accelerator#mec-application-solution-accelerator-example-reference-application-for-edgemec>{:target="_blank"}

## Learn

- <https://learn.microsoft.com/en-us/training/modules/build-faq-chatbot-qna-maker-azure-bot-service/>{:target="_blank"}

- <https://microsoftlearning.github.io/mslearn-ai-fundamentals/Instructions/Labs/07-question-answering.html>{:target="_blank"}

## Semantic-Kernel

- <https://github.com/microsoft/semantic-kernel>{:target="_blank"}


## Get started

source : <https://learn.microsoft.com/en-us/python/api/overview/azure/ai-formrecognizer-readme?view=azure-python&viewFallbackFrom=doc-intel-3.0.0#examples&preserve-view=true>{:target="_blank"}

``` bash
pip install azure-ai-formrecognizer
```

## Monitoring

- <https://demiliani.com/2023/12/19/monitoring-your-azure-openai-usage>

  ``` kusto
  AzureDiagnostics
  | where ResourceProvider contains "MICROSOFT.COGNITIVESERVICES"
  | where Category contains "RequestResponse"
  ```

- <https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/monitoring>

  ``` kusto
  AzureMetrics
  | take 100
  | project TimeGenerated, MetricName, Total, Count, Maximum, Minimum, Average, TimeGrain, UnitName
  ```
