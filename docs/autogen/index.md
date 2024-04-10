---
layout: default
title: AutoGen
nav_order: 2
has_children: true
---

others
https://github.com/microsoft/promptflow

## Web site

- <https://microsoft.github.io/autogen/>

## Get started

/usr/bin/python3 -m venv linux_venv
source ./linux_venv/bin/activate

pip install pyautogen
pip install python-dotenv

pip install pyautogen[retrievechat]

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

## Autogen studio

https://github.com/microsoft/autogen/blob/main/samples/apps/autogen-studio/README.md

pip install autogenstudio
autogenstudio ui --port 8081


## Samples

- GPT-researchers

    <https://www.youtube.com/watch?v=AVInhYBUnKs>
    <https://github.com/evagency/research-agents/blob/main/app.py>

- Group chat research

    <https://microsoft.github.io/autogen/docs/notebooks/agentchat_groupchat_research>