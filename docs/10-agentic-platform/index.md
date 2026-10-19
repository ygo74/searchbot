---
layout: default
title: Agentic Platform
nav_order: 10
has_children: true
---

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

# AI Agent Platform Charter – Development and Hosting Requirements

**Status:** Draft v1  \|  **Scope:** on-premise AI platform  \|  **Level:** rules only, no technology choices.
**MUST** = blocking for production. **SHOULD** = recommended, deviation must be justified. Classification: C1/C2 = standard; C3/C4, I3/I4, A3/A4 = secret or critical.

## 1. Principles

| ID  | Principle                                                                                                                                             |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| P1  | **Bring Your Own Agent**: any team may bring an agent, whatever the framework. The platform prescribes how an agent behaves, not how it is written.   |
| P2  | The contract prevails over the framework: a framework is admitted only if agents built with it meet the mandatory requirements.                       |
| P3  | An agent is an autonomous microservice with its own identity. Its logic never lives inside a third-party product; chatbots and M365 are thin clients. |
| P4  | Zero trust: the agent verifies the user identity and makes its own authorization decisions.                                                           |
| P5  | Everything goes through the platform: models (AI Gateway), tools (MCP Gateway), agents (Agents Gateway), discovery (Agent Registry).                  |
| P6  | No deployment without proven compliance; checks are automated, not declarative.                                                                       |
| P7  | Cloud ready by design: agents tolerate failures of their dependencies.                                                                                |
| P8  | Access is explicit: who can call an agent and what it can reach (including the Internet) is validated and recorded, never implicit.                   |

## 2. Framework governance

| Status       | Meaning                                                                                                               |
|--------------|-----------------------------------------------------------------------------------------------------------------------|
| Supported    | Platform library, template, CI pipeline and documentation provided.                                                   |
| Admitted     | Framework validated by Security and passed the conformance suite; no dedicated library; the agent team is autonomous. |
| Experimental | Development and test only; never in production.                                                                       |

**Admission criteria (all required):** configurable model base URL (can target the AI Gateway without patching); no hidden outbound telemetry or imposed SaaS; MCP client; streaming and progress events; OpenTelemetry instrumentation; Python, Java or .NET; compatible and maintained licence with a vulnerability process; runs in a non-root container; no embedded code-execution sandbox in production.
**Process:** request with justification, conformance PoC, Architecture and Security decision, revalidation on major changes and yearly review.

| Language | Common library | Framework adapters                           |
|----------|----------------|----------------------------------------------|
| Python   | Yes            | LangChain, CrewAI, Microsoft Agent Framework |
| .NET     | Yes            | Microsoft Agent Framework                    |
| Java     | Yes            | To be validated                              |

Platform libraries are **optional**. An agent that does not use them must pass the conformance suite and its framework must be validated by Security.

## 3. Requirements

### A. Exposure contract and protocols

| ID  | Requirement                                                                                                                                                                                                                                                                               | Level |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
| A1  | Every agent exposes all of the following endpoints, whatever its type: OpenAI-compatible (chat/completions and /responses), Anthropic-compatible (/messages) and MCP. Each endpoint is correctly mapped to the agent’s input and output, so the agent can be called by different clients. | MUST  |
| A2  | Support A2A: publish an Agent Card, receive and send tasks.                                                                                                                                                                                                                               | MUST  |
| A3  | Support AG-UI for user interface interaction (events, shared state, progress, human-in-the-loop).                                                                                                                                                                                         | MUST  |
| A4  | Support streaming on all exposed protocols.                                                                                                                                                                                                                                               | MUST  |
| A5  | Expose liveness, readiness and version.                                                                                                                                                                                                                                                   | MUST  |
| A6  | Publish OpenAPI or a manifest; the Agent Card states capabilities, version, required authentication and maximum classification.                                                                                                                                                           | MUST  |
| A7  | Protocol versions (A2A, AG-UI, MCP, compatible APIs) are not frozen.                                                                                                                                                                                                                      | –     |
| A8  | The conformance suite raises a non-blocking warning when a protocol version is obsolete, deprecated or unknown.                                                                                                                                                                           | MUST  |

*Rationale (A1): any client can call any agent without custom integration. The cost of universal compatibility is accepted and carried by the platform libraries.*

### B. Identity and security

| ID  | Requirement                                                                                                                                                                                                                                                                  | Level |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
| B1  | Validate the user JWT (signature, expiry, audience, issuer).                                                                                                                                                                                                                 | MUST  |
| B2  | Enforce authorization inside the agent (roles, groups, scopes).                                                                                                                                                                                                              | MUST  |
| B3  | Propagate the user identity (delegated token) to tools and data sources.                                                                                                                                                                                                     | MUST  |
| B4  | No secret in code or image; secrets come from the secret vault.                                                                                                                                                                                                              | MUST  |
| B5  | Respect the declared data classification; a C3/C4 agent never calls a cloud model.                                                                                                                                                                                           | MUST  |
| B6  | Treat all results returned by MCP services (and any tool output) as untrusted data, never as instructions, and apply least privilege on tools. Prompt-injection and content filtering are provided by the platform guardrails placed in front of the models (see section 5). | MUST  |
| B7  | Scan dependencies and container image (CVE, SBOM) in CI.                                                                                                                                                                                                                     | MUST  |

### C. Platform integration and network

| ID  | Requirement                                                                                                                                                                                                                                                                                                                                                      | Level   |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| C1  | All LLM calls go through the AI Gateway.                                                                                                                                                                                                                                                                                                                         | MUST    |
| C2  | All tool calls go through the MCP Gateway.                                                                                                                                                                                                                                                                                                                       | MUST    |
| C3a | The network profile (*Internal* by default, or *Internet-enabled*) is declared in the Registry. An agent never accesses the Internet directly: its network egress is limited to the platform gateways (including the MCP Gateway), enforced by network egress policy. *Internet-enabled* means the agent uses at least one MCP service that has Internet access. | MUST    |
| C3b | An Internet-enabled agent may be called directly. It accesses the Internet only through MCP services, behind the MCP Gateway.                                                                                                                                                                                                                                    | Allowed |
| C3c | An agent calling an Internet-enabled agent is authorized per use case by Architecture and Security, through the caller list (J4).                                                                                                                                                                                                                                | MUST    |
| C3d | Caller list entries state the maximum classification of data that may be transmitted.                                                                                                                                                                                                                                                                            | MUST    |
| C3e | An agent may combine C3/C4 data and Internet access only with an explicit decision by Security and Architecture, recorded on the agent page (N5).                                                                                                                                                                                                                | MUST    |
| C3f | The caller list of such agents is restricted and reviewed regularly; it is the primary control.                                                                                                                                                                                                                                                                  | MUST    |
| C3g | MCP services with Internet access are limited by allowlist (authorized destinations).                                                                                                                                                                                                                                                                            | MUST    |
| C3h | Data minimization: only what is strictly necessary is sent outside, by the agent to the MCP service and by the MCP service to the destination.                                                                                                                                                                                                                   | MUST    |
| C3i | Outbound flows are logged by the MCP service and the MCP Gateway (destination, volume, caller identity) without storing sensitive content in application logs.                                                                                                                                                                                                   | MUST    |
| C3j | The external provider is validated (contract, location, data handling) before production.                                                                                                                                                                                                                                                                        | MUST    |
| C3k | The Internet-enabled profile can be activated in the Registry only if a valid decision is referenced.                                                                                                                                                                                                                                                            | MUST    |
| C3l | MCP services with Internet access are declared with their allowlist and approved by Security. The MCP Gateway lets only agents with a valid Internet-enabled decision call them.                                                                                                                                                                                 | MUST    |
| C4  | Content retrieved from the Internet is untrusted and must not trigger side-effect actions without control (human-in-the-loop).                                                                                                                                                                                                                                   | MUST    |
| C5  | Models are selected through logical aliases, never hard-coded provider names.                                                                                                                                                                                                                                                                                    | MUST    |
| C6  | Handle quota, rate-limit and fallback responses from the Gateway.                                                                                                                                                                                                                                                                                                | SHOULD  |
| C7  | An agent never accesses external data sources directly (databases, document stores, vector stores, business or external APIs). All data access goes through an MCP service via the MCP Gateway. Exceptions: model calls (C1) and the agent’s declared state store (F5).                                                                                          | MUST    |

*Note:* C3/C4 data combined with Internet access is a formal derogation from the on-premise sovereignty principle, not a general rule.

### D. Observability

| ID  | Requirement                                                                                                                                                              | Level  |
|-----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| D1  | Structured logs, metrics and traces through OpenTelemetry.                                                                                                               | MUST   |
| D2  | Propagate trace ID and a correlation identifier (user, agent, version).                                                                                                  | MUST   |
| D3  | Report tokens, cost, latency and tools called (OpenTelemetry GenAI conventions).                                                                                         | MUST   |
| D4  | No sensitive data in logs (masking and retention by classification).                                                                                                     | MUST   |
| D5  | Audit, technical logs and metrics are stored in a common service and contain metadata and identifiers only, no business data.                                            | MUST   |
| D6  | Content traces (prompts, responses, tool arguments and results) are business data: stored separately by classification (C3/C4 vs C1/C2) and, for C3/C4, by jurisdiction. | MUST   |
| D7  | Content traces have their own retention period and access control, aligned with classification, and follow erasure rules (M7).                                           | MUST   |
| D8  | Audit records reference a content trace by identifier without copying its content.                                                                                       | MUST   |
| D9  | Content capture can be disabled per agent or classification.                                                                                                             | SHOULD |

### E. Governance and lifecycle

| ID  | Requirement                                                                                                                                                                                                                                                           | Level  |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| E1  | Declare the agent in the Registry before go-live (owner, framework, version, classification, models, tools, contact) with a reference to its catalog page.                                                                                                            | MUST   |
| E2  | Name a business owner and a technical owner; an owner change updates the page and the Registry.                                                                                                                                                                       | MUST   |
| E3  | Semantic versioning and rollback capability.                                                                                                                                                                                                                          | MUST   |
| E4  | Evaluation covers: business quality; RAG quality (source relevance, citations); security (rights, resistance to injection, leaks); reliability (timeout, tool error, unavailable dependency); performance and cost; action safety (approvals required and respected). | MUST   |
| E4a | Acceptance thresholds are defined per use case in the agent evaluation policy (N3).                                                                                                                                                                                   | MUST   |
| E4b | The test set is versioned and includes adversarial scenarios.                                                                                                                                                                                                         | MUST   |
| E4c | Production release is conditional on meeting the thresholds; a successful technical run is not sufficient.                                                                                                                                                            | MUST   |
| E5  | Standard CI/CD pipeline and infrastructure-as-code deployment; no manual deployment.                                                                                                                                                                                  | MUST   |
| E6  | Periodic recertification, based on the catalog review (N8).                                                                                                                                                                                                           | SHOULD |

### F. Packaging and execution

| ID  | Requirement                                                                                                                                                                                                                    | Level |
|-----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
| F1  | Deliver an OCI container image running as non-root.                                                                                                                                                                            | MUST  |
| F2  | Production target is the managed container platform; standalone container allowed in development.                                                                                                                              | MUST  |
| F3  | Configuration is provided at runtime from outside the container image (no environment-specific values in code or image). Secrets are handled separately (B4). The same image must be deployable unchanged across environments. | MUST  |
| F4  | Declare CPU and memory requests/limits. No direct GPU access: inference goes through the AI Gateway.                                                                                                                           | MUST  |
| F5  | Stateless, or state externalized in a declared store.                                                                                                                                                                          | MUST  |

### G. User interaction and human-in-the-loop

| ID  | Requirement                                                                                                                                                              | Level                       |
|-----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------|
| G1  | Progress notifications through the response stream or a standardized separate channel.                                                                                   | MUST (long tasks)           |
| G2  | Standardized human-in-the-loop (clarification, validation, approval) for any side-effect action.                                                                         | MUST (irreversible actions) |
| G2a | HITL works through chat/completions, /responses, /messages, A2A and AG-UI.                                                                                               | MUST                        |
| G2b | Each protocol has a documented mapping for pausing the task to ask the human and for continuing it once the human has answered, provided once by the platform libraries. | MUST                        |
| G2c | Pending-request state is externalized (agent stays stateless) and identified by a correlation identifier.                                                                | MUST                        |
| G2d | The answer is bound to identity: only the originating user or an explicitly designated approver may answer the pending request and let the task continue.                | MUST                        |
| G2e | A pending request expires; on expiry the action is abandoned, never executed by default.                                                                                 | MUST                        |
| G2f | Approvals are traced (who, when, what, agent version).                                                                                                                   | MUST                        |
| G2g | If the client does not support structured HITL, degrade to textual dialogue rather than execute the action.                                                              | SHOULD                      |
| G3  | Cite sources for RAG-based answers.                                                                                                                                      | MUST                        |

### I. Agent identity

| ID  | Requirement                                                                                                                                                                                                                                                                         | Level |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
| I1  | Each agent has its own workload identity, issued by any compliant OIDC provider when it is declared in the Registry.                                                                                                                                                                | MUST  |
| I2  | A call carries two verifiable identities: the calling agent and the originating user.                                                                                                                                                                                               | MUST  |
| I3  | Agent credentials are held in the secret vault with automatic rotation and central revocation.                                                                                                                                                                                      | MUST  |
| I4  | The agent identity is used for authorization, quotas, cost tracking (FinOps) and audit.                                                                                                                                                                                             | MUST  |
| I5  | No impersonation: an agent never presents another agent’s or a user’s credentials as its own. When acting for a user, it uses a delegated (on-behalf-of) token that identifies both the agent and the user and is restricted to the audience of the next hop.                       | MUST  |
| I6  | Libraries and configuration rely only on standard OIDC discovery (issuer, JWKS) and documented claims; changing provider requires no code change.                                                                                                                                   | MUST  |
| I7  | Required claims are defined in a provider-independent platform claims profile.                                                                                                                                                                                                      | MUST  |
| I8  | If a target system does not accept the delegated identity, the MCP service itself applies the user’s rights before calling the system with a restricted service identity. A technical identity never grants more rights than the user has. This case is declared on the agent page. | MUST  |

### J. Agent-to-agent calls and discovery

| ID  | Requirement                                                                                                                                       | Level |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------|-------|
| J1  | An agent calls another agent through the Agents Gateway only.                                                                                     | MUST  |
| J2  | Endpoint and availability come from the Agent Registry; no hard-coded URLs.                                                                       | MUST  |
| J3  | The agent registers and publishes its state (version, health, endpoint) automatically through the pipeline.                                       | MUST  |
| J4  | Each agent has an explicit list of authorized callers stored in the Registry; this list is the single source of truth.                            | MUST  |
| J5  | Dual control on the same list: the Gateway blocks any call not authorized for the requesting client, and the called agent re-verifies the caller. | MUST  |
| J6  | Loop protection: maximum chain depth, cycle detection via trace ID, and a token/duration budget inherited along the chain.                        | MUST  |
| J7  | The originating user identity is propagated along the whole chain.                                                                                | MUST  |
| J8  | The list is versioned and signed, or served by an authenticated API, so integrity can be verified.                                                | MUST  |
| J9  | Changes to the list follow an approval workflow by Architecture and Security, are audited, and are justified on the agent page.                   | MUST  |
| J10 | If the Registry is unavailable, use the last valid cached list for a platform-configured maximum duration, then deny (fail closed).               | MUST  |

### K. Resilience

| ID  | Requirement                                                                                                                                 | Level  |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------|--------|
| K1  | Retry with exponential backoff, jitter and a maximum on all calls to the AI, MCP and Agents Gateways.                                       | MUST   |
| K2  | Circuit breaker on the same dependencies, with a defined degraded behavior.                                                                 | MUST   |
| K3  | Explicit timeouts on every call.                                                                                                            | MUST   |
| K4  | Retry only transient errors (429, 5xx, timeout); side-effect operations are replayed only if idempotent or protected by an idempotency key. | MUST   |
| K5  | Honor rate-limit and Retry-After headers from the Gateway.                                                                                  | MUST   |
| K6  | Stateless, multiple instances, graceful shutdown.                                                                                           | MUST   |
| K7  | Expose circuit-breaker state and retries as metrics.                                                                                        | SHOULD |

### L. Code execution

*Former section H is merged here.*

| ID  | Requirement                                                                                                                                                              | Level |
|-----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
| L1  | Model-generated code runs only in the platform code-execution service, exposed to agents as a standard tool through the MCP Gateway.                                     | MUST  |
| L2  | Framework-native code-execution mechanisms are disabled in production.                                                                                                   | MUST  |
| L3  | Each execution is isolated from the host and from other executions, ephemeral, with resource limits (CPU, memory, duration, storage).                                    | MUST  |
| L4  | No network egress by default; only destinations explicitly authorized by the platform are reachable (for example the internal artifact repository to install a library). | MUST  |
| L5  | The authorized egress list is managed centrally after Security validation; neither the agent nor the generated code can change it.                                       | MUST  |
| L6  | Authorized egress is restricted to its intended use (for example read-only access to approved packages) and logged; it never opens general Internet access.              | MUST  |
| L7  | Execution is bound to the agent and originating user identities (audit, quotas).                                                                                         | MUST  |
| L8  | The sandbox receives no platform secret or credential; data enters and leaves as explicitly provided files.                                                              | MUST  |
| L9  | C3/C4 data is processed only by the dedicated on-premise C3/C4 instance.                                                                                                 | MUST  |
| L10 | The service is covered by the emergency stop (S1–S8).                                                                                                                    | MUST  |
| L11 | One common service for C1/C2 and one separate instance for C3/C4, with no split by jurisdiction.                                                                         | MUST  |
| L12 | The C3/C4 instance is isolated from the C1/C2 instance (infrastructure, network, artifact storage, administration); no data or artifact crosses between them.            | MUST  |
| L13 | Routing is decided by the platform from the classification declared in the Registry, never by the agent; a C3/C4 request to the C1/C2 instance is refused.               | MUST  |
| L14 | Authorized egress is defined per instance.                                                                                                                               | MUST  |
| L15 | Each instance can be stopped independently (S5).                                                                                                                         | MUST  |

### M. Vector data and retrieval

| ID  | Requirement                                                                                                                                                                                                              | Level               |
|-----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------|
| M1  | The platform provides managed vector infrastructure and a reference retrieval API, exposed as an MCP service.                                                                                                            | Platform commitment |
| M2  | An agent may use its own vector database if it meets M3–M11; it is declared as an agent dependency in the Registry and is accessed through an MCP service (C7). Platform support covers the managed infrastructure only. | MUST                |
| M3  | User rights (identity, groups, document ACL) are applied on every search, not only the agent’s rights.                                                                                                                   | MUST                |
| M4  | Access-control metadata is synchronized with the source; a revocation at the source propagates within a platform-configured delay.                                                                                       | MUST                |
| M5  | C3/C4 data never shares an instance with C1/C2 data; C3/C4 data is separated by jurisdiction (X2).                                                                                                                       | MUST                |
| M6  | C3/C4, I3/I4 and A3/A4 data is hosted on-premise.                                                                                                                                                                        | MUST                |
| M7  | Effective deletion of vectors and associated source documents, with traceability.                                                                                                                                        | MUST                |
| M8  | Encryption at rest and in transit; backup and restore according to classification.                                                                                                                                       | MUST                |
| M9  | Access is controlled and traced: only the declared agent (or the retrieval MCP service) may query the database.                                                                                                          | MUST                |
| M10 | A responsible owner is named (data, operations, lifecycle) and the database is covered by the emergency stop.                                                                                                            | MUST                |
| M11 | Infrastructure-level isolation between C3/C4 and C1/C2, and between jurisdictions for C3/C4.                                                                                                                             | MUST                |
| M12 | Reranking and hybrid search, when offered, follow the same access and observability rules.                                                                                                                               | SHOULD              |

### N. Agent catalog and documentation

| ID  | Requirement                                                                                                                                                                                                                                                               | Level  |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| N1  | Each agent has a dedicated page in the agent catalog (Confluence), created before production.                                                                                                                                                                             | MUST   |
| N2  | The page is kept up to date by the agent owner; an outdated page is a non-compliance.                                                                                                                                                                                     | MUST   |
| N3  | The page contains at least: business and technical owner, purpose, capabilities, deployment status, data sources connected via MCP, evaluation policy for MFC quality controls, classification and jurisdictions, network profile, and related decisions and derogations. | MUST   |
| N4  | The global catalog (all agents with owner, purpose, capabilities, status, MCP sources, evaluation policy) is visible to all employees.                                                                                                                                    | MUST   |
| N5  | Any Internet-access decision and any derogation (C3/C4 agent with Internet) is approved by Security and Architecture and recorded on the agent page (date, decision makers, reason, scope, authorized destinations, validity).                                            | MUST   |
| N6  | Any change to N3 information (new MCP source, capabilities, classification, network profile) is updated before deployment.                                                                                                                                                | MUST   |
| N7  | The evaluation policy on the page is consistent with the controls actually run (E4) and with MFC requirements.                                                                                                                                                            | MUST   |
| N8  | The catalog is reviewed periodically; agents without an active owner, recent update or usage are flagged for recertification or retirement.                                                                                                                               | SHOULD |
| N9  | The Registry is authoritative for what is technically enforced; the page is authoritative for decisions and justifications. They reference each other and the conformance suite checks common fields (classification, network profile, MCP sources, owner, status).       | MUST   |

### R. Responsibilities and trust boundaries

| ID  | Requirement                                                                                                                                    | Level |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------|-------|
| R1  | Being reachable through MCP does not mean being authorized. Every tool call is explicitly authorized.                                          | MUST  |
| R2  | Gateways apply platform policy but do not replace authorization by the component that executes the action.                                     | MUST  |
| R3  | The final decision on a sensitive action belongs to the component that executes it (MCP service or target system), after the gateway controls. | MUST  |

**Responsibility matrix (basis for discussion):**

| Operation                    | Authenticates  | Authorizes                                                                                  | Executes     | Logs                                                            |
|------------------------------|----------------|---------------------------------------------------------------------------------------------|--------------|-----------------------------------------------------------------|
| User → agent                 | Agents Gateway | Gateway (authorized client, Registry list) + agent (user rights)                            | Agent        | Gateway + agent                                                 |
| Agent → model                | AI Gateway     | AI Gateway (model allowed for the agent and classification, quotas)                         | Model        | AI Gateway (metadata) + content-trace storage by classification |
| Agent → tool or data         | MCP Gateway    | MCP Gateway (agent allowed for this service, Internet decision) + MCP service (user rights) | MCP service  | MCP Gateway + service                                           |
| Agent → agent                | Agents Gateway | Gateway + called agent (same Registry list)                                                 | Called agent | Gateway + both agents                                           |
| Model input/output filtering | –              | AI Gateway (guardrails)                                                                     | AI Gateway   | AI Gateway                                                      |

### O. Service objectives

| ID  | Requirement                                                                                                                                                                                                                              | Level |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
| O1  | The platform defines and publishes service objectives for: gateway availability and latency, GPU capacity and quotas, revocation propagation delay, disaster recovery (RTO/RPO), retention and effective deletion. Values are set later. | MUST  |
| O2  | A budget (tokens, cost) is defined per agent and per classification; exceeding it is blocked or flagged.                                                                                                                                 | MUST  |

### S. Emergency stop

| ID  | Requirement                                                                                                                                                                                                               | Level |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
| S1  | Any agent can be stopped immediately by the platform, without the cooperation of the agent or its team.                                                                                                                   | MUST  |
| S2  | The Registry holds a lifecycle state (active, suspended, revoked); moving to suspended automatically triggers all actions below.                                                                                          | MUST  |
| S3  | Independent blocking layers: Agents Gateway refuses inbound calls; AI and MCP Gateways refuse outbound calls; credentials and tokens are revoked; network egress is cut (including Internet); the workload is terminated. | MUST  |
| S4  | Gateways check the state on every request (no long cache) and agent tokens are short-lived; durations are platform-configured.                                                                                            | MUST  |
| S5  | Granularity: one agent, one version, all agents of a framework or library, all Internet-enabled agents, or all agents.                                                                                                    | MUST  |
| S6  | In-flight requests are cancelled and pending HITL requests are suspended; agents must tolerate abrupt stops (idempotent or compensable operations).                                                                       | MUST  |
| S7  | Security, platform on-call and the agent owner can stop an agent without prior approval; restarting requires validation.                                                                                                  | MUST  |
| S8  | Every stop is traced (who, when, why) and raises an alert.                                                                                                                                                                | MUST  |
| S9  | The stop is immediate and platform-driven: gateway blocking is instantaneous, followed by credential revocation and clean termination of the agent. No numeric target is set.                                             | MUST  |
| S10 | An incident runbook exists, with contacts, and stop drills are run regularly.                                                                                                                                             | MUST  |

### X. Data separation (cross-cutting)

| ID  | Requirement                                                                                                                                                                                                                                                                                 | Level |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
| X1  | Storage of business data (document content, vectors, prompt and response content) is separated by classification: C3/C4 vs C1/C2.                                                                                                                                                           | MUST  |
| X2  | For C3/C4, this storage is additionally separated by jurisdiction; no data crosses this boundary.                                                                                                                                                                                           | MUST  |
| X3  | Components that do not store business data (execution, audit, technical logs, metrics) are separated only by classification where necessary, not by jurisdiction.                                                                                                                           | MUST  |
| X4  | Derived data (summaries, transcriptions, embeddings, tool results, traces) inherits at least the classification of its source, unless formally declassified with an approved decision. When sources of different classifications are combined, the result takes the highest classification. | MUST  |

## 4. Reinforced requirements by classification

| Classification      | Additional requirements                                                                                                                                                                                                                                                       |
|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| C1/C2               | Sections A–N apply. Cloud models allowed through the AI Gateway.                                                                                                                                                                                                              |
| C3/C4, I3/I4, A3/A4 | On-premise models only; isolated network; logs without content; Security review before production; traced and recertified access; formal review of the framework used; dedicated code-execution instance (L9); content traces and vector data separated by jurisdiction (X2). |

## 5. Platform commitments

- Templates and common libraries (JWT, OpenTelemetry, Gateway calls, Registry declaration, identity, resilience) for the supported languages and frameworks.
- A conformance test suite runnable locally and in CI: protocols, JWT and dual identity, gateway usage, retry and circuit-breaker behavior (fault injection), Registry consistency, undeclared outbound calls, emergency-stop test.
- Guardrails in front of the models (prompt-injection and content filtering) at the AI Gateway level.
- Development, test and production environments with the same contracts.
- Model catalog with aliases, quotas and cost tracking per agent (FinOps).
- Managed vector infrastructure with a retrieval API exposed as an MCP service, a code-execution service, an agent catalog, documentation and support with a defined SLA.

## 6. Open points

| \#  | Open point                                                                                                                          | Owner                   |
|-----|-------------------------------------------------------------------------------------------------------------------------------------|-------------------------|
| 1   | Validate the Java framework adapter (Spring AI or LangChain4j) after consulting Java developers.                                    | To be assigned          |
| 2   | Define the mapping of HITL pausing and continuing for each protocol (G2b).                                                          | To be assigned          |
| 3   | Discuss with Security whether J10 (fail closed when the Registry is unavailable) applies to all calls or only to sensitive actions. | Security / Architecture |
| 4   | Agree the responsibility matrix (section R) and the handling of derived data classification (section X).                            | Security / Architecture |