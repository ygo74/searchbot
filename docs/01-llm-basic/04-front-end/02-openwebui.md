---
layout: default
grand_parent: LLM basic
parent: Webchat front-end
title: Open Webui
nav_order: 1
has_children: false
---


defaut embedded models :
- phi3
- arena models (random model)
- sentence-transformers/all-MiniLM-L6-v2

UI features
- stop button : yes
- scroll down arrow : yes
- full control on model configuration

MCP Servers

``` powershell
docker run --rm -it -p 8000:8000 --name mcpo `
       -v c:/devel/searchbot/research/openwebui/mcp/config.json:/mcp/config.json `
       ghcr.io/open-webui/mcpo:main --api-key "top-secret" --config /mcp/config.json
```

Scalability

https://github.com/danielrosehill/OpenWebUI-Postgres-Qdrant/tree/main
https://docs.openwebui.com/getting-started/env-configuration