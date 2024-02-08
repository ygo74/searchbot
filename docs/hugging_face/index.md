---
layout: default
title: Hugging Face
nav_order: 2
has_children: true
---

## Web site

- https://huggingface.co/

## Get started

Source : [Self deployment vLLM](https://docs.mistral.ai/self-deployment/vllm/)

``` powershell
$HF_TOKEN=""

docker run --gpus all `
    -e HF_TOKEN=$HF_TOKEN -p 8000:8000 `
    ghcr.io/mistralai/mistral-src/vllm:latest `
    --host 0.0.0.0 `
    --model mistralai/Mistral-7B-Instruct-v0.2
```

