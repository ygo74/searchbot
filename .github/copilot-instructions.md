# Copilot Instructions — searchbot

## Project Overview

This is an **AI/LLM research monorepo** for enterprise search, exploring multiple frameworks (AutoGen, Semantic Kernel, LangChain, CrewAI) and infrastructure (vector DBs, RAG, hosting). It is NOT a single application — it's a collection of research experiments, a docs site, and a small packaged library.

## Repository Layout

- **`research/`** — Independent research areas, each with its own `.env`, dependencies, and `lib/` utilities. The primary work area.
- **`src/ai_assistants/`** — Older packaged library using `pyautogen` (built via `pyproject.toml` at root). Largely inactive.
- **`samples/`** — Runnable sample scripts that import from `src/ai_assistants/`.
- **`docs/`** — Jekyll site (just-the-docs theme) published to GitHub Pages at `ygo74.github.io/searchbot`.
- **`hosting/`** — Model files and configs for local LLM hosting (LlamaEdge, GGUF).

## Key Conventions

### Environment & Secrets
- Every research area has its own `.env` file (never committed). Azure OpenAI is the primary LLM backend.
- Core env vars: `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`, `AZURE_OPENAI_API_VERSION`.
- AutoGen uses `OAI_CONFIG_LIST` pointing to a JSON file (e.g., `autogen_models_list.json`) for model selection with tag-based filtering.
- Load env with `python-dotenv`: `load_dotenv()` at the top of scripts.

### Python Script Patterns
- Files are **numbered** (`01-`, `02-`, `03-`) to indicate progressive complexity within each area.
- Standard entry point: `asyncio.run(main())` inside `if __name__ == "__main__":` block.
- Each research area may have a local `lib/` folder with shared helpers (LLM factory, web search). These are **duplicated** across areas, not centralized.
- When adding new research scripts, follow the numbering convention and create a `.env` from existing templates in sibling folders.

### Framework Usage
- **AutoGen** (`research/autogen/`): Uses v0.4 dev (`autogen-agentchat`, `autogen-core`, `autogen-ext`). Config via `OAI_CONFIG_LIST` JSON, `AzureOpenAIChatCompletionClient` factory in `lib/llm.py`.
- **Semantic Kernel** (`research/semantic_kernel/python/`): `Kernel` as central orchestrator, `add_service()` for LLM, `@kernel_function` decorator for plugins. Custom HTTP client with 300s timeout.
- **LangChain** (`research/chat_completion/02-langchain/`): `AzureChatOpenAI` with `ChatPromptTemplate`. Also used in the evaluation test harness.
- **CrewAI** (`research/crewai/`): Standard scaffold with YAML-driven agent/task configs, `uv` for deps, LiteLLM format model strings (`azure/<deployment>`).

### Docker Compose
- Infrastructure services (Qdrant, Milvus, PostgreSQL/PostGIS, Open WebUI) each have their own `docker-compose.yml` in the relevant research folder.
- Pattern: named networks, health checks on infra services, volume mounts for persistence.
- Some use external shared networks (`shared-observability`, `shared-db`).

### Testing & Evaluation
- Tests live in `research/evaluation/unit_tests/` using **pytest** with a custom LLM evaluation harness.
- Test data is YAML-based (`dataset/generic.yml`) with `prompts:` containing `name`, `user_prompt`, `expected_answer`.
- Custom `conftest.py` provides dynamic parametrization from YAML, session-scoped LLM chain fixtures, and DB result persistence.
- Two evaluation types: content-filter checks and LLM-as-judge comparison (GPT-4o scores, threshold > 0.8).
- Run tests: `pytest research/evaluation/unit_tests/ --model_config_file=<path> --dataset_folder=<path>`.

### Documentation (Jekyll)
- Docs in `docs/` use **just-the-docs** theme with numbered folders matching `nav_order`.
- Frontmatter requires: `layout`, `title`, `nav_order`; parent pages add `has_children: true`.
- Content mixes French and English (French user-facing text, English technical terms).
- TOC pattern: `<details><summary>Table of contents</summary>` with `{:toc}`.

## Dependency Management
- Root `pyproject.toml`: builds the `ai_assistants` package (setuptools). Rarely touched.
- Research areas use **separate** `requirements.txt` or `pyproject.toml` files with isolated venvs.
- CrewAI uses `uv` (`research/crewai/latest_ai_development/.venv/`).
- Root `requirements_*.txt` files are pip-freeze snapshots for specific venvs (autogen, langchain, unit tests).

## Important Notes
- This is a **research repo** — code may be experimental, scripts may have hardcoded paths or region-specific endpoints (Swiss Azure region `oai-ygo74-switzerland`).
- When creating new research areas, replicate the structure of existing ones: numbered scripts, local `lib/`, `.env` template, own `requirements.txt`.
- Azure Bicep files exist in `research/azure/` for provisioning Azure AI services.
