---
name: architecture-characteristics
description: "Use when deciding which architecture characteristics (-ilities) should drive a service, component, or change; when weighing trade-offs between them; when writing or reviewing an ADR or technical decision; when scoping a new microservice, agent tool, or infrastructure component; or when a request asks to improve a quality without naming a measurable characteristic (\"make X more reliable\", \"melhorar a confiabilidade\", \"quais os trade-offs\", \"vale a pena colocar cache\", \"o que estamos abrindo mão\", \"which -ilities matter\"). Tuned for aws-saas-platform and wasp-agent. Upstream of evolutionary-architecture."
---

# Architecture Characteristics

Choose and trade off architecture characteristics, following *Fundamentals of Software Architecture* (Richards, Ford). This skill decides **what** matters; `evolutionary-architecture` decides **how to measure and guard it**. A characteristic with no fitness function is aspirational, not architectural.

## Core rules

1. **At most three dominant characteristics per quantum.** Others may be tracked but do not drive design.
2. **Every choice names its cost.** No trade-off named = no decision made.
3. **Every choice must be measurable.** If no fitness function is imaginable, the characteristic was not chosen — a vibe was.
4. **Decompose composites.** "Agility" → Deployability + Testability + Modularity. "Operability" → Supportability + Recoverability. Colloquial "reliability"/"confiabilidade" → pick among Availability, Reliability, Robustness, Recoverability. "Production-grade", "modern", "cloud-native" → reject or decompose.
5. **The quantum is the unit of choice.** Each service may have different dominants; do not force one set across the platform.
6. **Floors are not dominants.** Security, Authentication, Authorization, and Tenant isolation are non-negotiable floors in every scope; they need fitness functions but do not consume one of the three slots unless they drive the design.

## Taxonomy

Use these names verbatim; `evolutionary-architecture` uses the same names in fitness-function ids. Map any other term back to one of them. Signal sources marked *(planned)* do not exist yet — see Project context.

**Operational** — runtime behavior

| Characteristic | Question | Typical signal |
|---|---|---|
| Availability | What fraction of time do we serve requests? | Success rate at ALB / Istio ingress |
| Continuity | Do we survive an AZ/region loss? | Multi-AZ spread; DynamoDB Global Tables *(planned)* |
| Performance | How fast is one request? | p50/p95/p99 at Istio ingress, OTel span duration |
| Recoverability | How fast do we restore after failure? | MTTR, rollback duration |
| Reliability | Correct under stress? | Error-budget burn, saturation |
| Robustness | Tolerates bad input / degraded dependencies? | 5xx vs 4xx ratio, circuit-breaker trips |
| Scalability | Does performance hold as load grows? | Throughput vs latency curve |
| Elasticity | Does capacity follow spikes in seconds? | Node provisioning latency (Karpenter *(planned)*) |

**Structural** — code and delivery

| Characteristic | Question | Typical signal |
|---|---|---|
| Configurability | Change behavior per tenant without redeploy? | Tenant config table, feature flags |
| Deployability | Ship safely and often? | Deploy frequency, change failure rate |
| Extensibility | Add features without modifying existing ones? | Plugin/provider pattern use |
| Installability | Provision a new instance/tenant easily? | `waspctl` / onboarding time |
| Maintainability | Easy to change? | PR cycle time, churn hotspots |
| Modularity | Clear, low-coupled boundaries? | Afferent/efferent coupling |
| Portability | Runs on another cloud/runtime? | Count of cloud-specific API calls |
| Supportability | Easy to debug in production? | Structured-log coverage, trace completeness |
| Testability | Easy to verify? | Coverage, e2e pass rate, test duration |
| Upgradeability | Smooth version transitions? | Backwards-compat test pass rate |

**Cross-cutting**

| Characteristic | Question | Typical signal |
|---|---|---|
| Authentication | Do we know who is calling? | Token validation failures |
| Authorization | Do we enforce what they may do? | Policy decision audit |
| Cost | Is spend proportional to value? | $/tenant/month, idle node ratio |
| Evolvability | Can the architecture change safely? | % of chosen characteristics with a fitness function |
| Legal / Compliance | LGPD, SOC 2, EU AI Act? | Control coverage |
| Observability | Can we see what is happening? | % requests fully traced, RED metric coverage |
| Privacy | PII minimized and isolated? | Data-classification scan, retention/TTL coverage |
| Security | Overall protection posture | WAF block rate, CVE count, secret-scan results |
| Tenant isolation | Can one tenant ever read or affect another? | Cross-tenant access audit, tenant-scoped keys |
| Usability | Can users reach their goal? | Task-completion rate |

Tenant isolation is a domain-specific characteristic for multi-tenant systems, not a composite — it is directly measurable. "Simplicity" is not in the taxonomy; use it only as a **cost** in trade-offs.

## Workflow

1. **Name the scope** — one quantum from Project context. A decision spanning several quanta is either a wrong boundary or a platform-level decision (`shared-infra`); say which.
2. **List candidates** from the taxonomy. Completeness first, no filtering.
3. **Cut to ≤3.** For each cut candidate, one line on why (already covered, or conflicts with a higher priority).
4. **Name each cost.** E.g., "Performance for `discovery` via cache costs tenant isolation risk (stale or cross-tenant entries) and simplicity (invalidation on tenant onboarding)."
5. **Draft the decision record** with the template below, in the location the repo uses.
6. **Hand off**: "These characteristics need fitness functions — use `evolutionary-architecture`." List one line per characteristic.

## Decision record template

```markdown
# ADR-<id>: <decision title>

## Status
Proposed | Accepted | Superseded by ADR-<id>

## Context
<what is being decided and why now>

## Quantum / scope
<one scope from Project context>

## Dominant characteristics (≤3)
1. <taxonomy name> — <one-line justification>
2. <taxonomy name> — <one-line justification>
3. <taxonomy name> — <one-line justification>

## Trade-offs
- Gaining <X> costs <Y>: <explanation>

## Fitness functions
- <ff-id or Good Citizen check id> (existing | scheduled in <ISSUE-KEY> | pending evolutionary-architecture) — covers <characteristic>

## Status gate
Stays Proposed until every dominant characteristic has at least one existing or scheduled fitness function.
```

The **Fitness functions** section is filled by `evolutionary-architecture`; until then write `pending evolutionary-architecture` per characteristic. An existing Good Citizen check (e.g., `OBS-001`) counts as a fitness function.

## Project context

Verify against the repo before relying on any item; these are snapshots, not live state.

**`aws-saas-platform`** — multi-tenant SaaS lab on EKS: ALB (TLS) → WAF → Istio ingress → FastAPI services, Cognito federation, DynamoDB `tenant-registry`.

- Scopes: `discovery`, `platform-frontend`, `callback-handler`, `tenant-frontend`, `shared-infra` (ALB, WAF, Istio, Cognito, DynamoDB, EKS).
- Live vs planned: ArgoCD (P1), Karpenter/PDB and Prometheus/Grafana/tracing (P2), DynamoDB Global Tables and CI/CD (P3) are **planned** in `docs/well-architected-framework/README.md`. Check that roadmap before naming a signal source.
- Decision records: `docs/technical-decisions.md` (`**Status:**` per entry) and `docs/well-architected-framework/<pillar>/changes/<name>/` (`proposal.md`, `design.md`, `tasks.md`). Map ADR `Proposed`/`Accepted` to `pending decision`/`decision made`.
- Jira: `PLTF` (`.jira/config.md`).

**`wasp-agent`** — agno agent (Claude via Bedrock) that provisions infrastructure from Telegram/Discord by committing Crossplane manifests to `wasp-gitops`; ArgoCD reconciles; a watcher notifies when ready. Exports OTel traces and Prometheus metrics. Not an MCP server today (MCP is a future option in `docs/sdlc/01-exploration/wasp-agent-extensibility-brief.md`).

- Scope: `wasp-agent` (one quantum).
- Decision records: specs in `docs/sdlc/02-design/` (`Status`: `Idea`, `Draft`, `Approved`, `Implemented`, `Deferred`); map ADR `Proposed`/`Accepted` to `Draft`/`Approved`. Do not create a parallel ADR tree.
- Production readiness: `docs/references/production-readiness-checklist.md` and the Good Citizen Test spec (`docs/sdlc/02-design/2026-05-30-good-citizen-test.md`) already define cluster-citizenship checks — reuse them, do not re-derive.

## Starting defaults per scope

Hypotheses to confirm or override, not commitments. When the request targets a specific quality, that quality's characteristics replace defaults.

| Scope | Likely dominants | Typical cost |
|---|---|---|
| `discovery` | Availability (every login depends on it), Tenant isolation (wrong lookup = cross-tenant login), Performance | Simplicity of caching/invalidation; per-tenant key design |
| `platform-frontend` | Performance, Availability, Usability | Feature scope — keep it a thin login entry point |
| `callback-handler` | Security (handles OAuth codes and tokens), Availability, Reliability | Simplicity (secret management, strict validation), latency of extra checks |
| `tenant-frontend` | No default — derive from its current purpose in `docs/` | — |
| `shared-infra` | Security, Continuity, Recoverability | Portability (AWS-coupled), cost of multi-AZ/multi-region |
| `wasp-agent` | Evolvability, Observability, Supportability | Interface stability — agent tools will churn; Authorization must still hold as a non-dominant floor |

## Push back when

- More than three dominants → force a cut.
- A characteristic without a cost → ask what it costs.
- "Make it more X" with no quantum → ask which service.
- Vague composites → decompose or reject.
- A record marked Accepted (or `Approved` / `decision made`) whose characteristics have no fitness function → flag the status-gate violation.
- A new `wasp-agent` tool or service without named dominants → block until named.

## Response shape

1. Scope. 2. Candidates considered. 3. Chosen ≤3 with justification. 4. Cost of each. 5. Decision-record draft — only when a decision is being recorded; for an exploratory question, stop at 4 and offer the draft. 6. Hand-off list for `evolutionary-architecture`.

Keep it tight: a decision artifact, not a book report.
