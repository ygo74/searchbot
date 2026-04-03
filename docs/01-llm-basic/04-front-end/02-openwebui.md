---
layout: default
grand_parent: LLM basic
parent: Webchat front-end
title: Open Webui
nav_order: 1
has_children: false
---

<details open markdown="block">
  <summary>Table of contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

# Installation

- Doc: <https://docs.openwebui.com/getting-started/quick-start/#example-docker-composeyml>{:target="_blank"}
- Source: <https://github.com/open-webui/open-webui>{:target="_blank"}

Deployment is done via Docker Compose. The file is located at `research/openwebui/docker-compose.yml`.

The web interface is exposed on port **3001** (`3001:8080`).

# Configuration

## Admin Account

The following variables automatically create the admin account on first startup:

| Variable | Description |
|---|---|
| `WEBUI_SECRET_KEY` | Secret key used to sign JWT tokens |
| `WEBUI_ADMIN_NAME` | Admin display name |
| `WEBUI_ADMIN_EMAIL` | Admin account email |
| `WEBUI_ADMIN_PASSWORD` | Admin account password |

## Model Configuration (OpenAI API)

Source: <https://docs.openwebui.com/reference/env-configuration#openai>{:target="_blank"}

Model access is exclusively through the OpenAI-compatible API (Ollama is disabled). The endpoint points to `host.docker.internal:8000`, allowing connection to a model server running on the host machine (e.g., LiteLLM, vLLM, or any OpenAI-compatible proxy).

| Variable | Value | Description |
|---|---|---|
| `ENABLE_OLLAMA_API` | `false` | Disables the built-in Ollama API |
| `ENABLE_OPENAI_API` | `true` | Enables the OpenAI-compatible API |
| `OPENAI_API_BASE_URL` | `http://host.docker.internal:8000/v1` | Base URL of the model server on the host |
| `OPENAI_API_KEY` | *(secret via .env)* | API key for authentication |

Default embedded models in Open WebUI:
- phi3
- arena models (random model selection)
- sentence-transformers/all-MiniLM-L6-v2

## PostgreSQL Database

Source: <https://docs.openwebui.com/reference/env-configuration#database-pool>{:target="_blank"}

By default, Open WebUI uses SQLite. For scalability, this configuration uses PostgreSQL as an external database (via the `postgres` service on the `shared-db` network).

| Variable | Value | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql://openwebui:***@postgres:5432/openwebui` | PostgreSQL connection string |
| `ENABLE_DB_MIGRATIONS` | `true` | Automatically runs schema migrations on startup |

## Observability (OpenTelemetry)

Source: <https://docs.openwebui.com/reference/env-configuration#opentelemetry-configuration>{:target="_blank"}

Observability is enabled via OpenTelemetry, exporting traces, metrics, and logs to an OTLP collector (on the `shared-observability` network).

| Variable | Value | Description |
|---|---|---|
| `ENABLE_OTEL` | `true` | Enables OpenTelemetry instrumentation |
| `ENABLE_OTEL_METRICS` | `true` | Enables metrics export |
| `ENABLE_OTEL_LOGS` | `true` | Enables logs export |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://otel-collector:4317` | gRPC endpoint of the OTLP collector |
| `OTEL_EXPORTER_OTLP_INSECURE` | `true` | Disables TLS for collector communication |

The global log level is set to `DEBUG` via `GLOBAL_LOG_LEVEL`.

Logging source: <https://docs.openwebui.com/reference/env-configuration#logging>{:target="_blank"}

## OAuth2 / OIDC Authentication (Keycloak)

Sources:
- OAuth configuration: <https://docs.openwebui.com/reference/env-configuration/#openid-oidc>{:target="_blank"}
- Keycloak integration: <https://docs.openwebui.com/features/access-security/auth/sso/keycloak>{:target="_blank"}

Authentication is delegated to **Keycloak** via the OpenID Connect protocol. The local login form is disabled in favor of SSO.

### General OAuth Settings

| Variable | Value | Description |
|---|---|---|
| `ENABLE_OAUTH_PERSISTENT_CONFIG` | `false` | OAuth config is defined by environment variables (not stored in DB) |
| `WEBUI_URL` | `http://localhost:3001` | Public URL of Open WebUI |
| `ENABLE_OAUTH_SIGNUP` | `true` | Allows account creation via OAuth on first login |
| `ENABLE_LOGIN_FORM` | `false` | Disables the local login form (email/password) |
| `DEFAULT_USER_ROLE` | `user` | Default role assigned to new users |

### Keycloak Settings

| Variable | Value | Description |
|---|---|---|
| `OAUTH_CLIENT_ID` | `open-webui` | Keycloak client ID |
| `OAUTH_CLIENT_SECRET` | *(secret via .env)* | Keycloak client secret |
| `OPENID_PROVIDER_URL` | `http://keycloak:8080/realms/localhost_backends/.well-known/openid-configuration` | OIDC discovery URL for the Keycloak realm |
| `OAUTH_PROVIDER_NAME` | `Keycloak` | Label displayed on the SSO button |
| `OPENID_REDIRECT_URI` | `http://localhost:3001/oauth/oidc/callback` | OAuth callback URL |

### Group Synchronization

| Variable | Value | Description |
|---|---|---|
| `ENABLE_OAUTH_GROUP_MANAGEMENT` | `true` | Enables group synchronization from the OIDC token |
| `ENABLE_OAUTH_GROUP_CREATION` | `true` | Automatically creates groups if they don't exist (Just-In-Time) |
| `OAUTH_GROUP_CLAIM` | `groups` | Token claim name containing the groups |

### Logout

| Variable | Description |
|---|---|
| `OPENID_PROVIDER_LOGOUT_URL` | Keycloak logout URL with redirect back to Open WebUI after logout |

## Web Search (Tavily)

Source: <https://docs.openwebui.com/reference/env-configuration#web-search>{:target="_blank"}

Web search is enabled using the **Tavily** engine. This allows models to perform web searches to enrich their responses (web RAG).

| Variable | Value | Description |
|---|---|---|
| `ENABLE_WEB_SEARCH` | `true` | Enables the web search feature |
| `ENABLE_SEARCH_QUERY_GENERATION` | `true` | The model automatically generates search queries |
| `WEB_SEARCH_TRUST_ENV` | `false` | Does not use proxy variables (`http_proxy`, `https_proxy`) for search |
| `WEB_SEARCH_RESULT_COUNT` | `3` | Number of results returned per search |
| `WEB_SEARCH_CONCURRENT_REQUESTS` | `0` | No limit on concurrent search requests |
| `WEB_LOADER_CONCURRENT_REQUESTS` | `10` | Maximum number of concurrent requests for page content loading |
| `WEB_SEARCH_ENGINE` | `tavily` | Search engine used |
| `TAVILY_API_KEY` | *(secret via .env)* | Tavily API key |
| `WEB_LOADER_ENGINE` | `tavily` | Engine used to load web page content |

## Redis (Scalability & WebSockets)

Sources:
- Redis configuration: <https://docs.openwebui.com/reference/env-configuration#redis>{:target="_blank"}
- Scaling: <https://docs.openwebui.com/getting-started/advanced-topics/scaling#step-2--add-redis>{:target="_blank"}
- Redis tutorial: <https://docs.openwebui.com/tutorials/integrations/redis>{:target="_blank"}

Redis is configured in **cluster** mode to support horizontal scaling of Open WebUI (multiple instances) and WebSocket management.

| Variable | Value | Description |
|---|---|---|
| `REDIS_URL` | `redis://redis-node-1:6379/0` | Redis node connection URL |
| `REDIS_CLUSTER` | `true` | Enables Redis cluster mode |
| `REDIS_SOCKET_CONNECT_TIMEOUT` | `5` | Connection timeout in seconds |
| `ENABLE_WEBSOCKET_SUPPORT` | `true` | Enables WebSocket support |
| `WEBSOCKET_MANAGER` | `redis` | Uses Redis as the WebSocket management backend |
| `WEBSOCKET_REDIS_URL` | `redis://redis-node-1:6379/0` | Dedicated Redis URL for WebSockets |
| `WEBSOCKET_REDIS_CLUSTER` | `true` | Cluster mode for WebSockets |
| `REDIS_KEY_PREFIX` | `open-webui` | Redis key prefix to avoid collisions |

## MCP Servers (Model Context Protocol)

Sources:
- <https://github.com/open-webui/mcpo>{:target="_blank"}
- <https://github.com/open-webui/openapi-servers>{:target="_blank"}

The **mcpo** service (MCP-to-OpenAPI proxy) exposes MCP servers as OpenAPI endpoints consumable by Open WebUI.

MCP server configuration is done via the `mcp/config.json` file mounted into the container.

Manual launch example:

``` powershell
docker run --rm -it -p 8000:8000 --name mcpo `
       -v c:/devel/searchbot/research/openwebui/mcp/config.json:/mcp/config.json `
       -v "c:/devel/mcp servers/python2:/mcp_servers" `
       ghcr.io/open-webui/mcpo:main --api-key "top-secret" --config /mcp/config.json
```

## Docker Networks

The configuration uses several external shared networks with other infrastructure services:

| Network | Usage |
|---|---|
| `shared-observability` | Communication with the OpenTelemetry collector |
| `shared-db` | Communication with PostgreSQL |
| `shared-auth` | Communication with Keycloak |
| `shared-redis` | Communication with the Redis cluster |
| `openwebui-net` | Internal network between Open WebUI and mcpo |

# UI Features

- Stop button: yes
- Scroll down arrow: yes
- Full control over model configuration

# To Explore

## Playwright (Web Loader)

{: .label .label-yellow }
Not yet configured

Playwright can replace the default web loader to fetch page content using a full headless browser.

``` powershell
docker run --rm -it -p 3025:3025 --name playwright `
        mcr.microsoft.com/playwright:v1.49.1-noble npx -y playwright@1.49.1 run-server --port 3025 --host 0.0.0.0
```

``` yaml
services:
  playwright:
    image: mcr.microsoft.com/playwright:v1.49.1-noble
    container_name: playwright
    command: npx -y playwright@1.49.1 run-server --port 3000 --host 0.0.0.0

  open-webui:
    environment:
      - 'WEB_LOADER_ENGINE=playwright'
      - 'PLAYWRIGHT_WS_URL=ws://playwright:3000'
```

## Qdrant (Vector Store)

{: .label .label-yellow }
Not yet configured

Sources:
- <https://github.com/danielrosehill/OpenWebUI-Postgres-Qdrant/tree/main>{:target="_blank"}
- <https://docs.openwebui.com/getting-started/env-configuration>{:target="_blank"}

## Community

- Prompts: <https://openwebui.com/prompts>{:target="_blank"}
- Tools: <https://openwebui.com/tools>{:target="_blank"}
- Functions: <https://openwebui.com/functions>{:target="_blank"}