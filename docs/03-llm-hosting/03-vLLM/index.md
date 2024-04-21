---
layout: default
title: vLLM
parent: LLM Hosting
nav_order: 3
has_children: false
---

## Install

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