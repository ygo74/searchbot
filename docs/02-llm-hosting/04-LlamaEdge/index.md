---
layout: default
title: LlamaEdge
parent: LLM Hosting
nav_order: 4
has_children: false
---


## Sources

- <https://llamaedge.com/>{:target="_blank"}
- <https://www.secondstate.io/articles/llama-3-8b/>{:target="_blank"}
- <https://www.secondstate.io/articles/selfhost-huggingface-llms/>{:target="_blank"}
- <https://techcommunity.microsoft.com/t5/microsoft-developer-community/getting-started-generative-ai-with-phi-3-mini-a-guide-to/ba-p/4121315>{:target="_blank"}

## Install binaries

``` bash
curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash -s -- --plugin wasi_nn-ggml

curl -LO https://github.com/LlamaEdge/LlamaEdge/releases/latest/download/llama-api-server.wasm

curl -LO https://github.com/LlamaEdge/chatbot-ui/releases/latest/download/chatbot-ui.tar.gz

tar xzf chatbot-ui.tar.gz
```

