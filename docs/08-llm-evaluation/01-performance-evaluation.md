---
layout: default
parent: LLM evaluation
title: Performance evaluation tools
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

# GuideLLM

Source: <https://github.com/vllm-project/guidellm>{:target="_blank"}


## Installation

### Command line

:warning: Only run on linux

``` bash
pip install guidellm

```

### Docker

Use ghcr.io/vllm-project/guidellm:latest

## Run benchmark

### Command line

``` bash
read -sp "API KEY:" AI_GATEWAY_API_KEY
AI_GATEWAY_URL="http://172.19.144.1:8000/v1"
AI_MODEL="gpt-5-chat"

BACKEND_KWARGS=$(jq -n \
  --arg api_key "$AI_GATEWAY_API_KEY" \
  '{api_key: $api_key}')

```

1. Run a Synchronous test


``` bash

guidellm benchmark run --backend openai_http --target $AI_GATEWAY_URL \
         --backend-kwargs "$BACKEND_KWARGS" \
         --model gpt-5-chat --profile synchronous \
         --data kind=synthetic_text,prompt_tokens=256,output_tokens=128  --max-seconds 10 \
         --processor Qwen/Qwen-7B \
         --processor-args '{"trust_remote_code":true}' \
         --warmup 5 --cooldown 5

```

1. Run a Constant test


``` bash

guidellm benchmark run --backend openai_http --target $AI_GATEWAY_URL \
         --backend-kwargs "$BACKEND_KWARGS" \
         --model gpt-5-chat --profile constant --rate 2 \
         --data kind=synthetic_text,prompt_tokens=256,output_tokens=128  --max-seconds 10 \
         --processor Qwen/Qwen-7B \
         --processor-args '{"trust_remote_code":true}' \
         --warmup 5 --cooldown 5

```

1. Run a Constant test from huggingface dataset

``` bash

guidellm benchmark run --backend openai_http --target $AI_GATEWAY_URL \
         --backend-kwargs "$BACKEND_KWARGS" \
         --model gpt-5-chat --profile constant --rate 2 \
         --data abisee/cnn_dailymail \
         --data-args '{"name":"3.0.0", "split":"test"}' \
         --data-column-mapper  '{"text_column": "article"}' \
         --max-seconds 10   --max-requests 100 \
         --warmup 5 --cooldown 5

```



``` bash
podman run \
  --rm -it \
  -v "./results:/results:rw" \
  -e GUIDELLM__SPEC__BACKEND='{"kind": "openai_http", "target": "http://localhost:8000"}' \
  -e GUIDELLM__SPEC__PROFILE='{"kind": "sweep"}' \
  -e GUIDELLM__SPEC__CONSTRAINTS='[{"kind": "max_duration", "seconds": 30}]' \
  -e GUIDELLM__SPEC__DATA='[{"kind": "synthetic_text", "prompt_tokens": 256, "output_tokens": 128}]' \
  ghcr.io/vllm-project/guidellm:latest

```