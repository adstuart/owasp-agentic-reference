"""Content for all 10 OWASP Agentic Top-10 threat videos.

Each entry has:
  id         — ASI identifier (also the folder name)
  title      — threat name
  accent     — 'blue' (default) or 'red' (ASI07, ASI08, ASI10 — new attack surface)
  pred_name  — OWASP LLM 2025 predecessor
  pred_text  — one-sentence explainer of the predecessor
  evolution  — dict with 'from_label', 'to_label', and 3 bullet points
  mitigations — list of {product, name, why} (1-2 entries)
  script     — narration text (≈140-160 words for ~60s at rate -5%)

The single-source-of-truth. `build_compositions.py` reads this to emit
each ASI folder's script.txt and index.html.
"""

THREATS = [
    {
        "id": "ASI01",
        "title": "Agent Goal Hijack",
        "accent": "blue",
        "pred_name": "Prompt Injection",
        "pred_text": "A crafted input tricks a model into ignoring its instructions, and a human chooses what to do with the wrong answer.",
        "evolution": {
            "from_label": "Single model reasons, human decides",
            "to_label": "Agent autonomously chains actions",
            "bullets": [
                "No human in the loop between the poisoned instruction and the side-effect",
                "The agent calls tools, writes to memory, and messages peer agents",
                "One injection fans out into a cascade of real-world actions",
            ],
        },
        "mitigations": [
            {
                "product": "Azure AI Content Safety",
                "name": "Prompt Shields",
                "why": "Detects both direct jailbreaks and indirect injections hidden in retrieved documents — before the agent reasons over the input.",
            },
            {
                "product": "Microsoft Defender for Cloud",
                "name": "AI Threat Protection",
                "why": "Runtime anomaly and jailbreak detection on the live agent for when a new attack pattern slips past filters.",
            },
        ],
        "script": (
            "Welcome to the OWASP Agentic AI Top Ten, where we map each new agentic risk back to its LLM predecessor and pick the top Microsoft mitigation.\n\n"
            "First up: Agent Goal Hijack.\n\n"
            "Previously, in the 2025 LLM Top Ten, this was prompt injection. A crafted input tricked the model into ignoring its instructions, and a human decided what to do with the wrong answer.\n\n"
            "In the agentic world, no human is in the loop. The agent autonomously chains tool calls, updates memory, and talks to other agents, so a single poisoned instruction triggers a cascade of real-world actions before anyone notices.\n\n"
            "My top Microsoft mitigation here is Azure AI Content Safety Prompt Shields. It detects both direct jailbreaks and indirect injections hidden in retrieved documents, and it runs before the agent reasons over the input.\n\n"
            "Back that up with Defender for Cloud AI threat protection for runtime anomaly detection on the live agent."
        ),
    },
    {
        "id": "ASI02",
        "title": "Tool Misuse and Exploitation",
        "accent": "blue",
        "pred_name": "Sensitive Information Disclosure",
        "pred_text": "The model inadvertently reveals PII, credentials, or proprietary training data in its output.",
        "evolution": {
            "from_label": "Model leaks sensitive strings in text",
            "to_label": "Agent weaponises authorised tools",
            "bullets": [
                "Agents are deliberately granted real tools — APIs, file systems, email",
                "They abuse those tools in ways the developer never modelled",
                "A tool call that succeeds technically can still cause a catastrophic side-effect",
            ],
        },
        "mitigations": [
            {
                "product": "Azure API Management",
                "name": "GenAI Gateway",
                "why": "Request validation, rate limiting and policy enforcement turn every tool call into a governed, logged, policy-checked transaction.",
            },
            {
                "product": "Microsoft Purview",
                "name": "Data Loss Prevention",
                "why": "Stops agents exfiltrating sensitive data through legitimate tools like email, SharePoint or a database connector.",
            },
        ],
        "script": (
            "Threat number two: Tool Misuse and Exploitation.\n\n"
            "In the 2025 LLM Top Ten this sat under Sensitive Information Disclosure, where the model accidentally leaked P I I, credentials, or proprietary training data in its text output.\n\n"
            "Agents change the shape of the problem. They are given real tools on purpose — A P Is, file systems, mail, databases — and they abuse those tools in ways the developer never modelled. The call succeeds, the logs look clean, and the agent has just emailed your customer list to an attacker.\n\n"
            "My top mitigation is Azure A P I Management, configured as a GenAI gateway. Every tool call is validated, rate-limited, and policy-checked, and it gives you a single point of observability.\n\n"
            "Pair that with Microsoft Purview data loss prevention, so even a legitimate tool call cannot exfiltrate sensitive content."
        ),
    },
    {
        "id": "ASI03",
        "title": "Identity and Privilege Abuse",
        "accent": "blue",
        "pred_name": "Supply Chain Vulnerabilities",
        "pred_text": "Compromised models, datasets, or third-party plugins slip in through the build pipeline.",
        "evolution": {
            "from_label": "Static supply-chain components",
            "to_label": "Agents inherit, escalate and re-use identity",
            "bullets": [
                "Agents carry OAuth tokens, session cookies and API keys across long workflows",
                "A single over-privileged agent is a lateral-movement accelerant",
                "Shared service principals make attribution and revocation painful",
            ],
        },
        "mitigations": [
            {
                "product": "Microsoft Entra",
                "name": "Agent ID",
                "why": "A unique, auditable identity per agent — so every action is attributed, and you can revoke one agent without tearing down the fleet.",
            },
            {
                "product": "Defender for Cloud",
                "name": "CIEM",
                "why": "Surfaces over-privileged agent identities and stale permissions so you can right-size before an attacker abuses them.",
            },
        ],
        "script": (
            "Threat number three: Identity and Privilege Abuse.\n\n"
            "In the 2025 LLM list this was supply chain vulnerabilities — compromised models, datasets, or plugins sneaking in through the build pipeline.\n\n"
            "With agents, identity itself is the supply chain. Agents carry OAuth tokens, session cookies, and A P I keys across long-running workflows. One over-privileged agent becomes a lateral-movement accelerant, and shared service principals make attribution and revocation extremely painful.\n\n"
            "My top mitigation is Microsoft Entra Agent I D. It gives every agent a unique, auditable identity, so each action is attributed and you can revoke a single agent without taking down the fleet.\n\n"
            "Then layer Defender for Cloud C I E M on top. It surfaces over-privileged agent identities and stale permissions, so you can right-size before an attacker does."
        ),
    },
    {
        "id": "ASI04",
        "title": "Agentic Supply Chain",
        "accent": "blue",
        "pred_name": "Data and Model Poisoning",
        "pred_text": "Malicious manipulation of training or fine-tuning data skews a model's behaviour.",
        "evolution": {
            "from_label": "Poisoned training data",
            "to_label": "Poisoned plugins, MCP servers, orchestrators",
            "bullets": [
                "Your agent stack now includes third-party MCP servers and tool registries",
                "A compromised plugin runs with the agent's privileges, not the user's",
                "Orchestration frameworks themselves are a new, under-audited attack surface",
            ],
        },
        "mitigations": [
            {
                "product": "Azure API Center",
                "name": "AI Registry",
                "why": "A vetted, governed catalog of approved M C P servers and tools — agents can only discover and consume what has been reviewed.",
            },
            {
                "product": "GitHub Advanced Security",
                "name": "Dependency and Secret Scanning",
                "why": "Catches compromised packages and leaked credentials in agent source and orchestration code before they ship.",
            },
        ],
        "script": (
            "Threat number four: the Agentic Supply Chain.\n\n"
            "In the 2025 list, supply chain risk was about poisoned training data and malicious model weights.\n\n"
            "An agent's supply chain is much wider. It now includes third-party M C P servers, plugin registries, and orchestration frameworks. A compromised plugin runs with the agent's privileges, not the user's, and those orchestration libraries are a new, largely unaudited attack surface.\n\n"
            "My top mitigation here is the Azure A P I Center A I Registry. It gives you a vetted, governed catalog of approved M C P servers and tools. Agents can only discover and call what you have reviewed.\n\n"
            "Support that with GitHub Advanced Security. Dependency and secret scanning on your agent source code catches compromised packages and leaked credentials before they ship to production."
        ),
    },
    {
        "id": "ASI05",
        "title": "Unexpected Code Execution",
        "accent": "blue",
        "pred_name": "Improper Output Handling",
        "pred_text": "Unvalidated model output is executed downstream as code, SQL, or markup.",
        "evolution": {
            "from_label": "Unsafe output passed to an interpreter",
            "to_label": "Agent generates and runs its own code",
            "bullets": [
                "Code-interpreter tools are now a standard part of the agent toolbelt",
                "The agent writes, executes and iterates on code with minimal oversight",
                "One bad plan means remote code execution or a sandbox escape on your infra",
            ],
        },
        "mitigations": [
            {
                "product": "Azure Container Apps",
                "name": "Dynamic Sessions",
                "why": "Hyper-V isolated, disposable sandboxes for agent-generated code — every session is fresh, scoped, and torn down after use.",
            },
            {
                "product": "Defender for Cloud",
                "name": "Runtime Threat Detection",
                "why": "Watches the sandboxed compute for anomalous process, network and file activity as a second line of defence.",
            },
        ],
        "script": (
            "Threat number five: Unexpected Code Execution.\n\n"
            "In the 2025 LLM Top Ten this was improper output handling — unvalidated model output executed downstream as code, S Q L, or markup.\n\n"
            "With agents, code execution is a feature, not a bug. Code-interpreter tools are a standard part of the agent toolbelt. The agent writes, runs and iterates on code with minimal oversight, and one bad plan means remote code execution or a sandbox escape on your infrastructure.\n\n"
            "My top mitigation is Azure Container Apps Dynamic Sessions. It gives you Hyper-V isolated, disposable sandboxes for agent-generated code. Every session is fresh, tightly scoped, and torn down after use.\n\n"
            "Add Defender for Cloud runtime threat detection over the top, so anomalous process, network, and file activity in the sandbox gets surfaced as an incident."
        ),
    },
    {
        "id": "ASI06",
        "title": "Memory and Context Poisoning",
        "accent": "blue",
        "pred_name": "Excessive Agency",
        "pred_text": "The model is granted more autonomy or permissions than the task actually requires.",
        "evolution": {
            "from_label": "Over-permissioned stateless model",
            "to_label": "Persistent memory and RAG stores poisoned",
            "bullets": [
                "Agents now have long-term memory — vector stores, session state, preference files",
                "Attackers plant adversarial content that the agent retrieves later",
                "Poisoned context bypasses content filters because it looks like trusted history",
            ],
        },
        "mitigations": [
            {
                "product": "Azure AI Content Safety",
                "name": "Groundedness Detection",
                "why": "Flags agent outputs that drift from the retrieved source — an early signal of poisoned memory or a poisoned RAG index.",
            },
            {
                "product": "Microsoft Purview",
                "name": "Information Protection",
                "why": "Sensitivity labels and DLP on documents entering RAG pipelines stop untrusted content becoming trusted context.",
            },
        ],
        "script": (
            "Threat number six: Memory and Context Poisoning.\n\n"
            "In 2025 we worried about excessive agency — a model granted more autonomy or permissions than the task actually required.\n\n"
            "In 2026, agents carry that autonomy forward through persistent memory. Vector stores, session state, preference files. Attackers now plant adversarial content that the agent retrieves days or weeks later. Poisoned context bypasses content filters because it already looks like trusted history.\n\n"
            "My top mitigation is Azure A I Content Safety Groundedness Detection. It flags agent outputs that drift from the retrieved source, giving you an early signal that memory or a R A G index has been poisoned.\n\n"
            "Combine that with Microsoft Purview Information Protection. Sensitivity labels and D L P on documents entering R A G pipelines stop untrusted content becoming trusted context."
        ),
    },
    {
        "id": "ASI07",
        "title": "Insecure Inter-Agent Communication",
        "accent": "red",
        "pred_name": "System Prompt Leakage",
        "pred_text": "The system prompt itself leaks to the user, exposing instructions, guardrails or secrets.",
        "evolution": {
            "from_label": "Single model, single prompt",
            "to_label": "Fleets of agents messaging each other",
            "bullets": [
                "Agent-to-agent messaging is a brand-new attack surface",
                "Spoofing, replay and man-in-the-middle work across the mesh",
                "There is no TLS-by-default convention yet for A2A and MCP",
            ],
        },
        "mitigations": [
            {
                "product": "Microsoft Entra",
                "name": "Agent ID Mutual Auth",
                "why": "Gives every agent a cryptographic identity so inter-agent calls can be mutually authenticated, not just trusted by name.",
            },
            {
                "product": "Azure API Management",
                "name": "mTLS and JWT Validation",
                "why": "Enforces mutual TLS and signed tokens on inter-agent calls — the gateway becomes the single enforcement point for the mesh.",
            },
        ],
        "script": (
            "Threat number seven: Insecure Inter-Agent Communication. This is a brand-new attack surface with no direct L L M equivalent.\n\n"
            "The closest 2025 risk was system prompt leakage, where the model's own system prompt leaked to the user and exposed instructions or secrets.\n\n"
            "Agents escalate that by talking to each other. Fleets of agents now send messages across A two A and M C P, and that mesh is a fresh attack surface. Spoofing, replay and agent-in-the-middle attacks all work, and there is no T L S by default convention yet.\n\n"
            "My top mitigation is Microsoft Entra Agent I D. Every agent gets a cryptographic identity, so inter-agent calls are mutually authenticated, not just trusted by name.\n\n"
            "Back it with Azure A P I Management enforcing m T L S and J W T validation on every inter-agent hop."
        ),
    },
    {
        "id": "ASI08",
        "title": "Cascading Failures",
        "accent": "red",
        "pred_name": "Vector and Embedding Weaknesses",
        "pred_text": "Weaknesses in vector embeddings and retrieval allow adversarial inputs to distort results.",
        "evolution": {
            "from_label": "A single retrieval query goes wrong",
            "to_label": "One bad input propagates across the fleet",
            "bullets": [
                "Agents chain into other agents — failures compound, not isolate",
                "One bad output becomes another agent's trusted input",
                "Without circuit breakers, a small glitch scales into a systemic outage",
            ],
        },
        "mitigations": [
            {
                "product": "Azure API Management",
                "name": "Circuit Breakers",
                "why": "Circuit-breaker and retry-backoff policies stop a single misbehaving agent from pulling the whole mesh down with it.",
            },
            {
                "product": "Microsoft Defender XDR",
                "name": "Correlated Detection",
                "why": "Correlates signals across workflows so you see the cascade as one incident, not ten separate unrelated alerts.",
            },
        ],
        "script": (
            "Threat number eight: Cascading Failures. Another brand-new attack surface.\n\n"
            "The 2025 analogue was vector and embedding weaknesses — adversarial inputs distorting retrieval results for a single query.\n\n"
            "In an agentic system, agents chain into other agents. Failures compound, they do not isolate. One bad output becomes the next agent's trusted input. Without circuit breakers, a small glitch scales into a systemic outage across your entire fleet in seconds.\n\n"
            "My top mitigation is Azure A P I Management. Circuit-breaker and retry-backoff policies on inter-agent calls stop a single misbehaving agent from pulling the whole mesh down with it.\n\n"
            "Pair that with Microsoft Defender X D R. It correlates signals across workflows, so the cascade shows up as one incident, not ten disconnected alerts."
        ),
    },
    {
        "id": "ASI09",
        "title": "Human-Agent Trust Exploitation",
        "accent": "blue",
        "pred_name": "Misinformation",
        "pred_text": "A plausible but wrong model output gets treated as fact by a downstream human or system.",
        "evolution": {
            "from_label": "User reads the wrong answer",
            "to_label": "User approves the wrong action",
            "bullets": [
                "Agents speak in fluent, confident, professional tone",
                "Users rubber-stamp approvals on actions they didn't really verify",
                "Social engineering now happens agent-to-human, at scale",
            ],
        },
        "mitigations": [
            {
                "product": "Azure AI Foundry",
                "name": "Evaluations",
                "why": "Automated relevance, coherence and completeness scoring catches plausible-but-wrong answers before users learn to over-trust them.",
            },
            {
                "product": "Microsoft Copilot Studio",
                "name": "Human-in-the-Loop",
                "why": "Built-in approval flows ensure sensitive actions pause for explicit human confirmation, not a glanced-at summary.",
            },
        ],
        "script": (
            "Threat number nine: Human-Agent Trust Exploitation.\n\n"
            "In the 2025 L L M Top Ten this was misinformation — a plausible but wrong output treated as fact by a human or downstream system.\n\n"
            "With agents the stakes jump. Users no longer just read the wrong answer, they approve the wrong action. Agents speak in fluent, confident, professional tone, and users rubber-stamp approvals on work they have not actually verified. Social engineering is now agent-to-human, at scale.\n\n"
            "My top mitigation is Azure A I Foundry Evaluations. Automated relevance, coherence and completeness scoring catches plausible-but-wrong answers before your users learn to over-trust them.\n\n"
            "Pair that with Copilot Studio human-in-the-loop. Built-in approval flows make sensitive actions pause for explicit confirmation."
        ),
    },
    {
        "id": "ASI10",
        "title": "Rogue Agents",
        "accent": "red",
        "pred_name": "Unbounded Consumption",
        "pred_text": "A model is driven into unbounded resource consumption — token floods, runaway costs, denial of wallet.",
        "evolution": {
            "from_label": "Excess tokens and runaway cost",
            "to_label": "Agents that escape guardrails entirely",
            "bullets": [
                "Agents spawn sub-agents, self-replicate, or run outside defined boundaries",
                "Shadow agents appear that nobody registered",
                "Anomalous consumption is an early rogue-agent signal, not just a bill problem",
            ],
        },
        "mitigations": [
            {
                "product": "Microsoft Defender for Cloud",
                "name": "AI Threat Protection",
                "why": "Fifteen plus detection types for rogue behaviour — guardrail evasion, self-replication, and off-policy tool use all surface as alerts.",
            },
            {
                "product": "Microsoft Entra",
                "name": "Agent ID Lifecycle and Shadow Discovery",
                "why": "Registers every known agent and proactively surfaces shadow agents running without authorisation.",
            },
        ],
        "script": (
            "Threat number ten: Rogue Agents. The third of the new attack surfaces.\n\n"
            "The 2025 predecessor was unbounded consumption. Token floods, runaway costs, denial of wallet attacks on a single model.\n\n"
            "Rogue agents go further. They escape guardrails, spawn sub-agents, self-replicate, or operate outside their defined boundaries entirely. Shadow agents appear that nobody registered. Anomalous consumption is now an early rogue-agent signal, not just a surprise invoice.\n\n"
            "My top mitigation is Defender for Cloud A I threat protection. It ships fifteen plus detection types for rogue behaviour — guardrail evasion, self-replication, and off-policy tool use all surface as alerts.\n\n"
            "Combine with Entra Agent I D lifecycle management and shadow agent discovery, so unauthorised agents get caught before they act.\n\n"
            "That's the OWASP Agentic Top Ten. Full mapping is on GitHub."
        ),
    },
]
