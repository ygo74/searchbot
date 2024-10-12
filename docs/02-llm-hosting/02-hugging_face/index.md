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

## Install huggingface-cli

1. Create python env
2. Install huggingface-hub

``` powershell
python -m venv .\venv\huggingface_venv
& .\venv\huggingface_venv\Scripts\activate

pip install huggingface-hub
huggingface-cli --help
```

## Get Models

``` bash
pip install 'huggingface-hub>=0.17.1'

# requires your hugging face token
huggingface-cli login

# Download a model
huggingface-cli download microsoft/Phi-3-mini-4k-instruct-gguf Phi-3-mini-4k-instruct-q4.gguf --local-dir . --local-dir-use-symlinks False

```