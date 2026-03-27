# OWASP LLM Top 10 vs Agentic AI Top 10 — with Microsoft Mitigations

Personal reference: mapping the OWASP Top 10 for LLM Applications (2025) against the newer Top 10 for Agentic Applications (2026), with relevant Microsoft tooling for each agentic risk.

> The Agentic list **complements** (not replaces) the LLM list. The LLM Top 10 secures a single model's inputs/outputs; the Agentic Top 10 secures autonomous **systems** that plan, use tools, have memory, and communicate with other agents.

## Comparison Table

| # | LLM Top 10 (2025) | Agentic AI Top 10 (2026) | Microsoft Mitigation Tooling |
|---|---|---|---|
| 1 | Prompt Injection | **[Agent Goal Hijack (ASI01)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** — prompt injection but the agent autonomously chains actions on it | **Azure AI Content Safety — Prompt Shields** (direct + indirect injection detection), Spotlighting for RAG scenarios, **Defender for Cloud AI Threat Protection** (runtime jailbreak/anomaly detection) |
| 2 | Sensitive Information Disclosure | **[Tool Misuse & Exploitation (ASI02)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** — agents abuse authorised tools (APIs, file systems, email) in unintended ways | **Microsoft Entra ID** (Conditional Access), **Azure API Management** (request validation, rate limiting, policy enforcement), **Purview DLP** (prevent agents exfiltrating sensitive data via authorised tools), **Azure API Center** (AI Registry — only approved tools are discoverable/consumable by agents) |
| 3 | Supply Chain Vulnerabilities | **[Identity & Privilege Abuse (ASI03)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** — agents inherit/escalate privileges via tokens, sessions, keys | **Microsoft Entra Agent ID** (unique auditable identity per agent), **Entra Workload ID** + Conditional Access, **Entra Permissions Management** (CIEM — detect over-privileged agent identities), **Entra ID Governance access packages** (time-bound agent permissions with auto-expiration and review) |
| 4 | Data & Model Poisoning | **[Agentic Supply Chain (ASI04)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** — compromised plugins, MCP servers, orchestration layers | **Defender for Cloud AI-SPM** (attack-path analysis across AI supply chain), **GitHub Advanced Security** (dependency scanning, secret scanning on agent code), **Azure API Center** (AI Registry — vetted catalog of approved MCP servers, plugins, and tools) |
| 5 | Improper Output Handling | **[Unexpected Code Execution (ASI05)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** — agents generate and run code, risking RCE / sandbox escape | **Azure Container Apps Dynamic Sessions** (sandboxed code execution), **Defender for Cloud** runtime threat detection on compute |
| 6 | Excessive Agency | **[Memory & Context Poisoning (ASI06)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** — persistent memory (RAG, vector stores) gets poisoned with malicious data | **Azure AI Content Safety — Groundedness Detection**, **Purview Information Protection** (sensitivity labels on documents entering RAG pipelines), **Purview DLP** on RAG store ingestion, **Azure AI Foundry Evaluations** (automated batch groundedness scoring — detects RAG output drift from poisoned sources over time) |
| 7 | System Prompt Leakage | **[Insecure Inter-Agent Communication (ASI07)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** — spoofing, replay, agent-in-the-middle attacks between agents | **Entra Agent ID** (mutual authentication between agents), **Azure API Management** (mTLS, JWT validation on inter-agent calls), **Azure Service Bus** (authenticated messaging), **Private endpoints + NSGs** (network-level isolation — inter-agent traffic stays off public networks) |
| 8 | Vector & Embedding Weaknesses | **[Cascading Failures (ASI08)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** — one bad input propagates across interconnected agent systems | **Azure API Management** (circuit-breaker policies, retry/back-off), **Defender XDR** (correlated detection across agent workflows), **Azure Monitor + App Insights**, **Azure Chaos Studio** (resilience testing of agent chains) |
| 9 | Misinformation | **[Human-Agent Trust Exploitation (ASI09)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** — users overtrust agent outputs, enabling social engineering | **Azure AI Content Safety** (harm categories for manipulative content), **Purview Compliance** (audit trails on agent-initiated actions), human-in-the-loop patterns in **Copilot Studio**, **Azure AI Foundry Evaluations** (relevance, coherence, completeness metrics — catches plausible-but-wrong answers that enable overtrust) |
| 10 | Unbounded Consumption | **[Rogue Agents (ASI10)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)** — agents escape guardrails, self-replicate, or act outside boundaries | **Defender for Cloud AI threat protection** (15+ detection types), **Entra Agent ID lifecycle management**, **APIM quotas**, **Azure Cost Management + token-based charging alerts** (detect runaway agent consumption), **Foundry Control Plane fleet operations** (agent fleet visibility + behavioural anomaly detection), **Entra ID shadow agent discovery** (detect unregistered agents) |

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
*Last updated: March 2026*
