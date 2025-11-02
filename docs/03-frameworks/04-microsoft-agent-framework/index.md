---
layout: default
parent: Frameworks
title: Microsoft Agent Framework
nav_order: 4
has_children: false
---

## Microsoft Agent Framework

- <https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview>{:target="_blank"}

    Microsoft Agent Framework is an open-source development kit for building AI agents and multi-agent workflows for .NET and Python. It brings together and extends ideas from Semantic Kernel and AutoGen projects, combining their strengths while adding new capabilities

- <https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio&ssr=false#overview>{:target="_blank"}

    AI Toolkit is a powerful extension for Visual Studio Code that streamlines agent development. With AI Toolkit, you can:

    🔍 Explore and evaluate models from a wide range of providers—including Anthropic, OpenAI, GitHub—or run models locally using ONNX and Ollama.
    ⚡ Build and test agents in minutes with prompt generation, quick starters, and seamless MCP tool integrations.


- <https://devblogs.microsoft.com/foundry/introducing-microsoft-agent-framework-the-open-source-engine-for-agentic-ai-apps/?utm_source=chatgpt.com>{:target="_blank"}

## Installation

``` powershell
python -m venv .\venv\windows_venv_maf
& .\venv\windows_venv_maf\Scripts\activate

pip install agent-framework
pip install python-dotenv

# For specific use case : Due diligence
pip install qdrant-client openpyxl pandas pydantic

```
