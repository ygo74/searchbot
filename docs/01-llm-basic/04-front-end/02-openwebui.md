---
layout: default
grand_parent: LLM basic
parent: Webchat front-end
title: Open Webui
nav_order: 1
has_children: false
---

Community:
- https://openwebui.com/prompts
- https://openwebui.com/tools
- https://openwebui.com/functions

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
       -v "c:/devel/mcp servers/python2:/mcp_servers" `
       ghcr.io/open-webui/mcpo:main --api-key "top-secret" --config /mcp/config.json
```

Playwrgight

``` powershell
docker run --rm -it -p 3025:3025 --name playwright `
        mcr.microsoft.com/playwright:v1.49.1-noble npx -y playwright@1.49.1 run-server --port 3025 --host 0.0.0.0

```

``` yaml
services:
  playwright:
    image: mcr.microsoft.com/playwright:v1.49.1-noble # Version must match requirements.txt
    container_name: playwright
    command: npx -y playwright@1.49.1 run-server --port 3000 --host 0.0.0.0

  open-webui:
    environment:
      - 'WEB_LOADER_ENGINE=playwright'
      - 'PLAYWRIGHT_WS_URL=ws://playwright:3000'
```

Scalability

https://github.com/danielrosehill/OpenWebUI-Postgres-Qdrant/tree/main
https://docs.openwebui.com/getting-started/env-configuration

postgres : OK
qdrant : OK