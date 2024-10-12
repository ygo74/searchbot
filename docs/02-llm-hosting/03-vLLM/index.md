---
layout: default
title: vLLM
parent: LLM Hosting
nav_order: 3
has_children: false
---

## Install

### Install for CPU

``` bash
docker build -f Dockerfile.cpu -t vllm-cpu-env --shm-size=4g .
```


### Install from source

``` bash
# Install vLLM with CUDA 11.8.
export VLLM_VERSION=0.2.4
export PYTHON_VERSION=310
pip install https://github.com/vllm-project/vllm/releases/download/v${VLLM_VERSION}/vllm-${VLLM_VERSION}+cu118-cp${PYTHON_VERSION}-cp${PYTHON_VERSION}-manylinux1_x86_64.whl

# Re-install PyTorch with CUDA 11.8.
pip uninstall torch -y
pip install torch --upgrade --index-url https://download.pytorch.org/whl/cu118

# Re-install xFormers with CUDA 11.8.
pip uninstall xformers -y
pip install --upgrade xformers --index-url https://download.pytorch.org/whl/cu118

```

## Serve Model

### Serve from CPU container

1. Start server OpenAPI

    ``` bash
    docker run --rm -it \
        -v ~/.cache/huggingface:/root/.cache/huggingface \
        --env "HUGGING_FACE_HUB_TOKEN=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" \
        -e VLLM_CPU_KVCACHE_SPACE=4 \
        -e VLLM_CPU_OMP_THREADS_BIND=0-1 \
        --ipc host \
        -p 8000:8000 \
        vllm-cpu-env:latest \
        --model microsoft/Phi-3-mini-4k-instruct

    ```

2. check server is running

    ``` bash
    curl http://localhost:8000/v1/models
    ```

## Microsoft semantic kernel

### Workaround

to be tested !!!

``` csharp
using Azure.AI.OpenAI;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using System.Reflection;

var builder = Kernel.CreateBuilder();
var aiclietn =  new OpenAIClient(
            new Uri("http://127.0.0.1:8000/v1"),
            new Azure.AzureKeyCredential("empty")
        );
// _isConfiguredForAzureOpenAI
var field = typeof(OpenAIClient).GetField("_isConfiguredForAzureOpenAI", BindingFlags.NonPublic | BindingFlags.Instance);
// _isConfiguredForAzureOpenAI
if (field != null)
{
    field.SetValue(aiclietn, false);
}

builder.AddOpenAIChatCompletion("qwen",aiclietn);

```

## Sources

- <https://blog.octo.com/comment-utiliser-un-llm-open-source-1>{:target="_blank"}
- <https://docs.vllm.ai/en/stable/getting_started/installation.html>{:target="_blank"}