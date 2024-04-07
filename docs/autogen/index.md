---
layout: default
title: AutoGen
nav_order: 2
has_children: true
---

## Web site

- <https://microsoft.github.io/autogen/>

## Get started

/usr/bin/python3 -m venv linux_venv
source ./linux_venv/bin/activate

pip install pyautogen
pip install python-dotenv

## LLM Configuration

- Source : <https://microsoft.github.io/autogen/docs/topics/llm_configuration>

    ``` python
    [
        {
            "model": "gpt-4",
            "api_type": "azure",
            "api_key": os.environ['AZURE_OPENAI_API_KEY'],
            "base_url": "https://ENDPOINT.openai.azure.com/",
            "api_version": "2024-02-15-preview"
        }
    ]
    ```