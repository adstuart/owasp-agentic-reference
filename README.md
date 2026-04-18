# OWASP LLM Top 10 vs Agentic AI Top 10 — with Microsoft Mitigations

Personal reference: mapping the OWASP Top 10 for LLM Applications (2025) against the newer Top 10 for Agentic Applications (2026), with relevant Microsoft tooling for each agentic risk.

> The Agentic list **complements** (not replaces) the LLM list. The LLM Top 10 secures a single model's inputs/outputs; the Agentic Top 10 secures autonomous **systems** that plan, use tools, have memory, and communicate with other agents.

## Architecture

```mermaid
graph LR
    subgraph LLM["OWASP LLM Top 10 (2025)"]
        L1[Prompt Injection]
        L2[Sensitive Info Disclosure]
        L3[Supply Chain]
        L4[Data Poisoning]
        L5[Improper Output]
        L6[Excessive Agency]
    end

    subgraph AGT["OWASP Agentic Top 10 (2026)"]
        A1[Agent Goal Hijack]
        A2[Tool Misuse]
        A3[Identity & Privilege Abuse]
        A4[Agentic Supply Chain]
        A5[Unexpected Code Exec]
        A6[Memory Poisoning]
        A7[Insecure Inter-Agent Comms]
        A8[Cascading Failures]
        A9[Human Trust Exploitation]
        A10[Rogue Agents]
    end

    subgraph MS["Microsoft Mitigations"]
        M1[AI Content Safety]
        M2[Microsoft Entra]
        M3[Azure API Management]
        M4[Defender for Cloud]
        M5[Microsoft Purview]
        M6[Azure API Center]
        M7[GitHub Advanced Security]
        M8[Container Apps Sessions]
        M9[Defender XDR + Monitor]
        M10[Azure AI Foundry]
        M11[Copilot Studio]
    end

    L1 -->|evolves to| A1
    L2 -->|splits into| A2
    L2 -->|splits into| A3
    L3 -->|evolves to| A4
    L5 -->|evolves to| A5
    L4 -->|evolves to| A6
    L6 -->|evolves to| A2

    A1 -.-> M1
    A1 -.-> M4
    A2 -.-> M3
    A2 -.-> M6
    A3 -.-> M2
    A3 -.-> M4
    A4 -.-> M7
    A4 -.-> M6
    A5 -.-> M8
    A5 -.-> M4
    A6 -.-> M1
    A6 -.-> M5
    A6 -.-> M10
    A7 -.-> M2
    A7 -.-> M3
    A8 -.-> M3
    A8 -.-> M9
    A9 -.-> M5
    A9 -.-> M10
    A9 -.-> M11
    A10 -.-> M4
    A10 -.-> M2

    style A7 fill:#c62828,stroke:#b71c1c,color:#fff
    style A8 fill:#c62828,stroke:#b71c1c,color:#fff
    style A10 fill:#c62828,stroke:#b71c1c,color:#fff
    classDef msBlue fill:#0078d4,stroke:#005a9e,color:#fff
    class M1,M2,M3,M4,M5,M6,M7,M8,M9,M10,M11 msBlue

    click L1 callback "Crafted inputs that trick a model into ignoring instructions or leaking data"
    click L2 callback "Model inadvertently reveals PII, credentials, or proprietary training data"
    click L3 callback "Compromised models, datasets, or third-party plugins introduced via the build pipeline"
    click L4 callback "Malicious manipulation of training or fine-tuning data to skew model behaviour"
    click L5 callback "Unvalidated model output executed downstream as code, SQL, or markup"
    click L6 callback "Model granted more autonomy or permissions than the task requires"

    click A1 callback "Prompt injection that hijacks an autonomous agent into chaining harmful actions"
    click A2 callback "Agents abuse legitimately granted tools in unintended or dangerous ways"
    click A3 callback "Agents inherit, escalate, or misuse identity tokens and access privileges"
    click A4 callback "Compromised plugins, MCP servers, or orchestration layers in the agent stack"
    click A5 callback "Agents dynamically generate and execute code, risking RCE or sandbox escape"
    click A6 callback "Persistent agent memory or RAG stores poisoned with adversarial content"
    click A7 callback "Spoofing, replay, or man-in-the-middle attacks on agent-to-agent messaging"
    click A8 callback "A single bad input propagates unchecked across interconnected agent systems"
    click A9 callback "Users blindly trust agent outputs, enabling social engineering and manipulation"
    click A10 callback "Agents escape guardrails, self-replicate, or operate outside defined boundaries"

    click M1 callback "Prompt Shields, groundedness detection, and harm-category classifiers for AI I/O"
    click M2 callback "Agent ID, Workload ID, Conditional Access, and CIEM for agent identity governance"
    click M3 callback "GenAI Gateway with rate limiting, JWT validation, circuit-breaker, and mTLS policies"
    click M4 callback "AI threat protection, AI-SPM attack-path analysis, and runtime anomaly detection"
    click M5 callback "DLP, sensitivity labels, information protection, and audit trails for data governance"
    click M6 callback "AI Registry — vetted catalog of approved MCP servers, plugins, and agent tools"
    click M7 callback "Dependency scanning, secret scanning, and code scanning on agent source code"
    click M8 callback "Sandboxed Hyper-V code interpreter sessions for safe dynamic code execution"
    click M9 callback "Correlated cross-workflow threat detection, distributed tracing, and observability"
    click M10 callback "Automated evaluations for groundedness, coherence, and agent fleet control plane"
    click M11 callback "Low-code agent builder with built-in human-in-the-loop approval workflows"
```

> **Red** = new attack surfaces with no direct LLM equivalent. **Blue** = Microsoft mitigation tooling. Solid arrows show risk evolution; dotted arrows show primary mitigations (see table below for full mapping). Hover over any node for a one-liner description.

## Comparison Table

> 🎬 **New:** each threat below has a 60-second explainer video. Click the 🎬 link in each row to jump to the embedded player, or browse all videos in the [Threat Videos](#threat-videos) section.

| # | LLM Top 10 (2025) | Agentic AI Top 10 (2026) | Microsoft Mitigation Tooling | 🎬 |
|---|---|---|---|---|
| 1 | Prompt Injection | **Agent Goal Hijack (ASI01)** — prompt injection but the agent autonomously chains actions on it | **[Azure AI Content Safety — Prompt Shields](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection)** (direct + indirect injection detection), [Spotlighting](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection) for RAG scenarios, **[Defender for Cloud AI Threat Protection](https://learn.microsoft.com/en-us/azure/defender-for-cloud/ai-threat-protection)** (runtime jailbreak/anomaly detection) | [▶](#asi01) |
| 2 | Sensitive Information Disclosure | **Tool Misuse & Exploitation (ASI02)** — agents abuse authorised tools (APIs, file systems, email) in unintended ways | **[Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/conditional-access/workload-identity)** (Conditional Access), **[Azure API Management](https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities)** (request validation, rate limiting, policy enforcement), **[Purview DLP](https://learn.microsoft.com/en-us/purview/dlp-learn-about-dlp)** (prevent agents exfiltrating sensitive data via authorised tools), **[Azure API Center](https://learn.microsoft.com/en-us/azure/api-center/agent-to-agent-overview)** (AI Registry — only approved tools are discoverable/consumable by agents) | [▶](#asi02) |
| 3 | Supply Chain Vulnerabilities | **Identity & Privilege Abuse (ASI03)** — agents inherit/escalate privileges via tokens, sessions, keys | **[Microsoft Entra Agent ID](https://learn.microsoft.com/en-us/entra/agent-id/identity-platform/agent-identities)** (unique auditable identity per agent), **[Entra Workload ID](https://learn.microsoft.com/en-us/entra/id-protection/concept-workload-identity-risk)** + Conditional Access, **[Defender for Cloud CIEM](https://learn.microsoft.com/en-us/azure/defender-for-cloud/permissions-management)** (detect over-privileged agent identities), **[Entra ID Governance access packages](https://learn.microsoft.com/en-us/entra/id-governance/entitlement-management-overview)** (time-bound agent permissions with auto-expiration and review), **[APIM per-model access control](https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities)** (gateway enforces which models each agent/use-case is authorised to call — unauthorised model requests return 403) | [▶](#asi03) |
| 4 | Data & Model Poisoning | **Agentic Supply Chain (ASI04)** — compromised plugins, MCP servers, orchestration layers | **[Defender for Cloud AI-SPM](https://learn.microsoft.com/en-us/azure/defender-for-cloud/ai-security-posture)** (attack-path analysis across AI supply chain), **[GitHub Advanced Security](https://docs.github.com/en/code-security/concepts/supply-chain-security/about-supply-chain-security)** (dependency scanning, secret scanning on agent code), **[Azure API Center](https://learn.microsoft.com/en-us/azure/api-center/agent-to-agent-overview)** (AI Registry — vetted catalog of approved MCP servers, plugins, and tools), **[APIM as MCP gateway](https://learn.microsoft.com/en-us/azure/api-management/expose-api-as-mcp-tool)** (policy enforcement, throttling, and auth on MCP tool calls — agents access MCP servers through the gateway rather than directly, enabling per-tool access control and monitoring) | [▶](#asi04) |
| 5 | Improper Output Handling | **Unexpected Code Execution (ASI05)** — agents generate and run code, risking RCE / sandbox escape | **[Azure Container Apps Dynamic Sessions](https://learn.microsoft.com/en-us/azure/container-apps/sessions-code-interpreter)** (sandboxed code execution), **[Defender for Cloud](https://learn.microsoft.com/en-us/azure/defender-for-cloud/alerts-reference)** runtime threat detection on compute | [▶](#asi05) |
| 6 | Excessive Agency | **Memory & Context Poisoning (ASI06)** — persistent memory (RAG, vector stores) gets poisoned with malicious data | **[Azure AI Content Safety — Groundedness Detection](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/groundedness)**, **[Purview Information Protection](https://learn.microsoft.com/en-us/purview/sensitivity-labels)** (sensitivity labels on documents entering RAG pipelines), **[Purview DLP](https://learn.microsoft.com/en-us/purview/dlp-learn-about-dlp)** on RAG store ingestion, **[Azure AI Foundry Evaluations](https://learn.microsoft.com/en-us/azure/foundry/how-to/evaluate-generative-ai-app)** (automated batch groundedness scoring — detects RAG output drift from poisoned sources over time) | [▶](#asi06) |
| 7 | System Prompt Leakage | **Insecure Inter-Agent Communication (ASI07)** — spoofing, replay, agent-in-the-middle attacks between agents | **[Entra Agent ID](https://learn.microsoft.com/en-us/entra/agent-id/identity-platform/agent-identities)** (mutual authentication between agents), **[Azure API Management](https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities)** (mTLS, JWT validation on inter-agent calls), **[APIM Credential Manager](https://learn.microsoft.com/en-us/azure/api-management/credentials-overview)** (gateway brokers OAuth2 flows to downstream services on behalf of agents — agents never hold third-party credentials directly), **[Azure Service Bus](https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-authentication-and-authorization)** (authenticated messaging), **[Private endpoints + NSGs](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/ai/platform/networking)** (network-level isolation — inter-agent traffic stays off public networks) | [▶](#asi07) |
| 8 | Vector & Embedding Weaknesses | **Cascading Failures (ASI08)** — one bad input propagates across interconnected agent systems | **[Azure API Management](https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities)** (circuit-breaker policies, retry/back-off), **[Defender XDR](https://learn.microsoft.com/en-us/defender-xdr/alerts-incidents-correlation)** (correlated detection across agent workflows), **[Azure Monitor + App Insights](https://learn.microsoft.com/en-us/azure/azure-monitor/app/agents-view)**, **[Azure Chaos Studio](https://learn.microsoft.com/en-us/azure/chaos-studio/chaos-studio-chaos-experiments)** (resilience testing of agent chains) | [▶](#asi08) |
| 9 | Misinformation | **Human-Agent Trust Exploitation (ASI09)** — users overtrust agent outputs, enabling social engineering | **[Azure AI Content Safety](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/harm-categories)** (harm categories for manipulative content), **[Purview Audit](https://learn.microsoft.com/en-us/purview/audit-solutions-overview)** (audit trails on agent-initiated actions), human-in-the-loop patterns in **[Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/flows-request-for-information)**, **[Azure AI Foundry Evaluations](https://learn.microsoft.com/en-us/azure/foundry/how-to/evaluate-generative-ai-app)** (relevance, coherence, completeness metrics — catches plausible-but-wrong answers that enable overtrust) | [▶](#asi09) |
| 10 | Unbounded Consumption | **Rogue Agents (ASI10)** — agents escape guardrails, self-replicate, or act outside boundaries | **[Defender for Cloud AI threat protection](https://learn.microsoft.com/en-us/azure/defender-for-cloud/ai-threat-protection)** (15+ detection types), **[Entra Agent ID lifecycle management](https://learn.microsoft.com/en-us/entra/id-governance/agent-id-governance-overview)**, **[APIM quotas](https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities)**, **[Azure Cost Management](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/cost-mgt-alerts-monitor-usage-spending) + token-based charging alerts** (detect runaway agent consumption), **APIM chargeback dashboards** (per-use-case token consumption tracking — anomalous spikes in a specific agent's usage serve as an early rogue-agent detection signal), **[Foundry Control Plane fleet operations](https://learn.microsoft.com/en-us/azure/foundry/control-plane/overview)** (agent fleet visibility + behavioural anomaly detection), **[Entra ID shadow agent discovery](https://learn.microsoft.com/en-us/entra/id-governance/agent-id-governance-overview)** (detect unregistered agents) | [▶](#asi10) |

## Threat Videos

Each video is ~60 seconds and covers: the 2025 LLM predecessor → how it evolves in the agentic world → top Microsoft mitigation. Generated with [HyperFrames](https://github.com/heygen-com/hyperframes) and a Custom Neural Voice trained on my own narration — pipeline sources in [`video-pipeline/`](./video-pipeline/).

<a id="asi01"></a>
### ASI01 — Agent Goal Hijack

https://github.com/adstuart/owasp-agentic-reference/raw/master/videos/ASI01.mp4

<a id="asi02"></a>
### ASI02 — Tool Misuse & Exploitation

https://github.com/adstuart/owasp-agentic-reference/raw/master/videos/ASI02.mp4

<a id="asi03"></a>
### ASI03 — Identity & Privilege Abuse

https://github.com/adstuart/owasp-agentic-reference/raw/master/videos/ASI03.mp4

<a id="asi04"></a>
### ASI04 — Agentic Supply Chain

https://github.com/adstuart/owasp-agentic-reference/raw/master/videos/ASI04.mp4

<a id="asi05"></a>
### ASI05 — Unexpected Code Execution

https://github.com/adstuart/owasp-agentic-reference/raw/master/videos/ASI05.mp4

<a id="asi06"></a>
### ASI06 — Memory & Context Poisoning

https://github.com/adstuart/owasp-agentic-reference/raw/master/videos/ASI06.mp4

<a id="asi07"></a>
### ASI07 — Insecure Inter-Agent Communication

https://github.com/adstuart/owasp-agentic-reference/raw/master/videos/ASI07.mp4

<a id="asi08"></a>
### ASI08 — Cascading Failures

https://github.com/adstuart/owasp-agentic-reference/raw/master/videos/ASI08.mp4

<a id="asi09"></a>
### ASI09 — Human-Agent Trust Exploitation

https://github.com/adstuart/owasp-agentic-reference/raw/master/videos/ASI09.mp4

<a id="asi10"></a>
### ASI10 — Rogue Agents

https://github.com/adstuart/owasp-agentic-reference/raw/master/videos/ASI10.mp4

## Key Takeaways

- **New attack surfaces with no LLM equivalent**: Inter-agent communication (ASI07), cascading failures (ASI08), and rogue agents (ASI10).
- **Evolution of existing risks**: Prompt Injection → Goal Hijack (now the agent *acts* on it). Excessive Agency → Tool Misuse + Identity Abuse (more granular). Data Poisoning → Memory/Context Poisoning (persistent RAG stores).
- **Microsoft's defence-in-depth** spans identity (Entra Agent ID), data governance (Purview), runtime protection (Defender for Cloud), content filtering (AI Content Safety), and API control (APIM).

## References

- [OWASP Top 10 for Agentic Applications (2026)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [OWASP Top 10 for LLM Applications (2025)](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/)
- [OWASP GenAI Security Project — Agentic Security Initiative](https://genai.owasp.org/initiatives/agentic-security-initiative/)
- [OWASP Announcement — Dec 2025](https://genai.owasp.org/2025/12/09/owasp-genai-security-project-releases-top-10-risks-and-mitigations-for-agentic-ai-security/)
- [Microsoft Defender for Cloud — AI threat protection](https://learn.microsoft.com/en-us/azure/defender-for-cloud/ai-threat-protection)
- [Azure AI Content Safety — Prompt Shields](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection)
- [Microsoft Entra Agent ID](https://learn.microsoft.com/en-us/entra/identity/agents/overview)

---
> **Footnote — Foundry Citadel**: Many of the APIM-based mitigations above (unified AI gateway, per-model access control, MCP gateway, credential brokering, chargeback dashboards) ship together as a deployable landing zone accelerator called [Foundry Citadel](https://aka.ms/ai-hub-gateway) (citadel-v1 branch). It provides a one-click hub-spoke architecture with centralised governance for LLMs, agents, and tools.

*Last updated: April 2026*
