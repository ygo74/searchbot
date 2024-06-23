---
layout: default
parent: LLM Hosting
title: Azure
nav_order: 8
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

Azure OpenAI Service provides REST API access to OpenAI's powerful language models including the GPT-4, GPT-4 Turbo with Vision, GPT-3.5-Turbo, and Embeddings model series.

## Demo

- <https://github.com/Azure-Samples/azure-search-openai-demo/>{:target="_blank"}

## Architecture

- <https://learn.microsoft.com/en-us/azure/architecture/ai-ml/openai/idea/search-and-query-using-openai-service>{:target="_blank"}
- <https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/conversational-bot>{:target="_blank"}

## Sources

- <https://learn.microsoft.com/en-us/azure/ai-services/openai/>{:target="_blank"}

- <https://techcommunity.microsoft.com/t5/ai-machine-learning-blog/deploy-large-language-models-responsibly-with-azure-ai/ba-p/3876792>{:target="_blank"}
- <https://techcommunity.microsoft.com/t5/azure-ai-services-blog/revolutionize-your-enterprise-data-with-chatgpt-next-gen-apps-w/ba-p/3762087>{:target="_blank"}
- <https://medium.com/@imicknl/how-to-create-a-private-chatgpt-with-your-own-data-15754e6378a1>{:target="_blank"}

- EDGE MEC application solution accelerator : <https://github.com/Azure/mec-app-solution-accelerator#mec-application-solution-accelerator-example-reference-application-for-edgemec>{:target="_blank"}

## Training

- <https://learn.microsoft.com/en-us/training/modules/build-faq-chatbot-qna-maker-azure-bot-service/>{:target="_blank"}
- <https://microsoftlearning.github.io/mslearn-ai-fundamentals/Instructions/Labs/07-question-answering.html>{:target="_blank"}

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
