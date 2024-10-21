---
layout: default
title: LLM evaluation
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

dataset : <https://huggingface.co/datasets/rajpurkar/squad>

## products

https://www.helicone.ai/blog/best-langsmith-alternatives

### Comet opic

Source : <https://www.comet.com/docs/opik/>


``` powershell
git clone https://github.com/comet-ml/opik.git
cd opik/deployment/docker-compose
docker compose up --detach
```

``` powershell
pip install opik
```

### PromptFlow

Source : <https://microsoft.github.io/promptflow/>

``` powershell
# Install the latest stable version
pip install promptflow --upgrade

```

## Proof of concept

``` powershell
python -m venv .\venv\unittests_venv
& .\venv\unittests_venv\Scripts\activate
pip install python-dotenv langchain openai datasets pytest
pip install langchain-openai langchain_community
```