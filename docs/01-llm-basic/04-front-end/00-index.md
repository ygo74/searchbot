---
layout: default
parent: LLM basic
title: Webchat front-end
nav_order: 4
has_children: true
---

# Comparison

## Internet comparison

Source: <https://openalternative.co/>{:target="_blank"}

- LibreChat vs Open WebUI: <https://openalternative.co/compare/librechat/vs/open-webui>{:target="_blank"}

  Comparable except for Community and Popularity where Open WebUI wins.

- LibreChat vs Anything LLM: <https://openalternative.co/compare/anythingllm/vs/librechat>{:target="_blank"}

  Comparable except for Community and Popularity where Anything LLM wins.

- Anything LLM: vs Open WebUI: <https://openalternative.co/compare/anythingllm/vs/open-webui>{:target="_blank"}

  Comparable except for Community and Popularity where Open WebUI wins.

## Custom comparison

{: .note-title }
> Title
>
> text

{: .important-title }
> Title
>
> text

{: .warning-title }
> Title
>
> text

:+1: :+1: :+1: :+1:
✅
❌
☑️

## Web UI

| Topic                    | Priority | OpenWebUI       | LibreChat            | Anything LLM  |
| ------------------------ |:--------:|:---------------:|:--------------------:|:-------------:|
| End user perception      | 1        | :+1: :+1: :+1:  | :+1: :+1: :+1: :+1:  |               |
| Transparent SSO OIDC     | 1        | ✅              | ✅                  |               |
| Style customization      | 1        | ☑️ (1)          | ✅                  |               |
| Theme support            | 2        |                 | ✅ (Light / dark)   |               |


- **(1)** Requires the enterprise license

### Comparison conclusion

:point_right:


## Chat Experience

| Topic                    | Priority | OpenWebUI       | LibreChat            | Anything LLM  |
| ------------------------ |:--------:|:---------------:|:--------------------:|:-------------:|
|                          | 1        |                 |                      |               |
| Websearch                | 1        |                 | :+1: :+1: (1)        |               |

- **(1)** Web search experience is different betwenn standard chat and agent chat.

  - Agent chat uses plugin such as Google Search / Tavily
  - Standard chat uses other search platform

## RAG

| Topic                    | Priority | OpenWebUI       | LibreChat            | Anything LLM  |
| ------------------------ |:--------:|:---------------:|:--------------------:|:-------------:|
|                          | 1        |                 |                      |               |

## Security

| Topic                    | Priority | OpenWebUI       | LibreChat            | Anything LLM  |
| ------------------------ |:--------:|:---------------:|:--------------------:|:-------------:|
| OIDC support             | 1        | ✅              | ✅                  | ☑️ (1)        |
| RBAC models              | 1        |                 |                      |               |


- **(1)** Requires to delegate to a reverse proxy
