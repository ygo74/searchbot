---
layout: default
parent: Azure
title: Azure containers
nav_order: 2
has_children: true
---

## Keyphrase

Source : https://mcr.microsoft.com/product/azure-cognitive-services/textanalytics/keyphrase/about

Pull :  docker pull mcr.microsoft.com/azure-cognitive-services/textanalytics/keyphrase

How-to : https://learn.microsoft.com/fr-fr/azure/ai-services/language-service/overview#deploy-on-premises-using-docker-containers

Quick start : https://learn.microsoft.com/fr-fr/azure/ai-services/language-service/key-phrase-extraction/quickstart?pivots=programming-language-csharp

Create language resource : https://portal.azure.com/#create/Microsoft.CognitiveServicesTextAnalytics

``` powershell

$endPointUri = ""
$apiKey = ""

docker run --rm -it -p 5000:5000 --memory 4g --cpus 1 `
mcr.microsoft.com/azure-cognitive-services/textanalytics/keyphrase `
Eula=accept `
Billing=$endPointUri `
ApiKey=$apiKey

```

Test : http://localhost:5000/swagger/index.html

