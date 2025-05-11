---
layout: default
parent: LLM basic
title: MCP Servers
nav_order: 4
has_children: false
---

<https://modelcontextprotocol.io/quickstart/server>

# install uv

``` powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
$env:Path = "C:\Users\Administrator\.local\bin;$env:Path"

```

``` bash
curl -LsSf https://astral.sh/uv/install.sh | sh

```

# Init project

``` powershell

# init project
uv init --name demo_mcp_server --directory src/

# init venv
uv venv venv/demo_cp_server
 & .\venv\demo_cp_server\Scripts\activate

# Install dependencies
cd .\src\
uv add "mcp[cli]" httpx --active

```
