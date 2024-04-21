---
layout: default
title: Hugging Face
parent: LLM Hosting
nav_order: 2
has_children: false
---

## Web site

- <https://huggingface.co/>{:target="_blank"}

## Get started

Source : [Self deployment vLLM](https://docs.mistral.ai/self-deployment/vllm/){:target="_blank"}

``` powershell
$HF_TOKEN=""

docker run --gpus all `
    -e HF_TOKEN=$HF_TOKEN -p 8000:8000 `
    ghcr.io/mistralai/mistral-src/vllm:latest `
    --host 0.0.0.0 `
    --model mistralai/Mistral-7B-Instruct-v0.2
```

