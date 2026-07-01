---
layout: default
parent: Frameworks
title: AutoGen
nav_order: 2
has_children: false
---

## others

- <https://github.com/microsoft/promptflow>{:target="_blank"}

## Web site

- <https://microsoft.github.io/autogen/>{:target="_blank"}

## Get started

/usr/bin/python3 -m venv linux_venv
source ./linux_venv/bin/activate

pip install ag2
pip install python-dotenv

pip install ag2[retrievechat]

## LLM Configuration

- Source : <https://microsoft.github.io/autogen/docs/topics/llm_configuration>{:target="_blank"}

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

- <https://github.com/microsoft/autogen/blob/main/samples/apps/autogen-studio/README.md>{:target="_blank"}

pip install autogenstudio
autogenstudio ui --port 8081


## Autogen playground in huggingface

- <https://huggingface.co/spaces/thinkall/AutoGen_Playground>{:target="_blank"}

## Web search

Source :

- <https://console.cloud.google.com/apis/>{:target="_blank"}

  Custom Search API

  ``` bash
  cx=
  key=
  term=

  curl \
  'https://customsearch.googleapis.com/customsearch/v1?cx=$cx&q=$term&key=$key' \
  --header 'Accept: application/json' \
  --compressed

  ```

## Samples

- GPT-researchers

  - <https://www.youtube.com/watch?v=AVInhYBUnKs>{:target="_blank"}
  - <https://github.com/evagency/research-agents/blob/main/app.py>{:target="_blank"}

- Group chat research

  - <https://microsoft.github.io/autogen/docs/notebooks/agentchat_groupchat_research>{:target="_blank"}

## Web UI

https://yeyu.substack.com/p/how-to-create-a-web-ui-for-autogen

pip install --upgrade panel


panel serve source_code.py