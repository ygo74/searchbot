---
layout: default
title: Ollama
nav_order: 2
has_children: true
---


## Sources

- <https://github.com/ollama/ollama>
- <https://ollama.com/>

## Configuration

### Windows on Ollama

1. Bind to all ip

  ``` powershell
  $env:OLLAMA_HOST="0.0.0.0"
  ollama start
  ```

### Ollama on WSL

1. Install

  ``` bash
  curl https://ollama.ai/install.sh | sh

  ```

## Interacting with model

### From bash

``` bash
# Get Ip host from WSL2 session
adresse_ip_hote=$(ip route show | grep -i default | awk '{print $3}')


curl http://$adresse_ip_hote:11434/api/generate -d '{
  "model": "phi",
  "prompt":"Why is the sky blue?"
}'
```

### From Python

Source : <https://python.langchain.com/docs/get_started/quickstart#langsmith>



ls__52807b41512a47b5a963b5c9885c33f1

## Customize a custom model

``` DockerFile
FROM phi

# set the temperature to 1 [higher is more creative, lower is more coherent]
PARAMETER temperature 1

# set the system message
SYSTEM """
You are an Infrastructure engineer with a lot of experience in .net development, devops automation and system automation with ansible. Answer as an Infrastructure engineer, the assistant, only.
"""

```

