---
name: evolutionary-architecture
description: "Use when a named architecture characteristic needs a fitness function, guardrail, threshold, or CI/runtime gate; when asking whether the architecture is drifting or getting worse over time; when reviewing the health of existing fitness functions or Good Citizen checks; or when designing agent tools that report architecture health (\"fitness function para latência p95\", \"isso deveria ser um gate?\", \"como medir isso\", \"drift\", \"is this evolvable\"). Tuned for aws-saas-platform and wasp-agent. Downstream of architecture-characteristics."
---

# Evolutionary Architecture

Define, place, and maintain fitness functions, following *Building Evolutionary Architectures* (Ford, Parsons, Kua). This skill is downstream of `architecture-characteristics`: that one chooses **what** matters, this one **measures and guards** it.

## Entry check

Proceed only when the request names a characteristic from the `architecture-characteristics` taxonomy (Performance, Availability, Tenant isolation, ...). If it names none, or only a vague goal ("more reliable", "better"), switch to `architecture-characteristics` first and return with its hand-off list.

If the characteristic is named but no decision record makes it dominant (or a floor) for the quantum, proceed and state that the function is unanchored until a record selects it.

## Classification

| Axis | Values |
|---|---|
| Scope | **atomic** (one characteristic) · **holistic** (a combination, e.g., Security + Performance) |
| Cadence | **triggered** (on commit/PR/deploy) · **continual** (runtime, always on) · **temporal** (scheduled) |
| Result | **static** (pass/fail) · **dynamic** (threshold over a sliding window) |
| Invocation | **automated** (default) · **manual** (only with a follow-up to automate) |

## Reuse before you create

`wasp-agent` already specifies cluster-citizenship fitness functions: the Good Citizen Test (`docs/sdlc/02-design/2026-05-30-good-citizen-test.md`, check ids `HLT-`, `OBS-`, `RES-`, `SEC-`, `CFG-`, `DEP-`, `REL-`, `OWN-`). Before writing a new fitness function:

1. If an existing Good Citizen check covers the characteristic — same characteristic and quantum, with an enforced check — cite its id in the decision record and stop. A related check that only declares something (e.g., an SLO is declared) is a prerequisite: cite it alongside the new `ff-*`.
2. Otherwise create an `ff-*` definition. Fitness functions about workload manifests belong in the Good Citizen catalog; propose them there, not as a parallel list.

Vocabulary mapping — use it when citing Good Citizen checks:

| Good Citizen | This skill |
|---|---|
| tier `static` | triggered + static (manifest inspection) |
| tier `behavioral` | triggered + static or dynamic (ephemeral namespace) |
| tier `attestation` | manual, revalidated on a temporal cadence |
| class `gate` | `action_on_breach: block-deploy` |
| class `score` | `action_on_breach: warn`; feeds the Bronze/Prata/Ouro level |
| exception ledger (`exceptions.yaml`, TTL) | the only accepted way to waive a breach |

## Fitness function schema

```yaml
id: ff-<characteristic>-<short-name>   # characteristic in kebab-case, e.g. ff-performance-callback-p95
characteristic: <taxonomy name from architecture-characteristics>
quantum: <scope from architecture-characteristics>
description: <what it protects, in business terms>
scope: atomic | holistic
cadence: triggered | continual | temporal
result_type: static | dynamic
invocation: automated | manual
metric_source: <PromQL | OTel metric | Istio telemetry | k8s API | CI step | CloudWatch>
source_status: live | planned (<roadmap item>)
threshold:
  operator: < | <= | > | >= | ==
  value: <number or expression>
  window: <5m | 24h | per-deploy>
action_on_breach: block-deploy | page-oncall | open-issue | warn
owner: <team or person>
related_decision: <ADR id, spec path, or WAF change path>
```

`source_status: planned` keeps the function honest when the signal depends on unbuilt infrastructure; the decision record stays Proposed until the source is live or the work is scheduled.

Without a baseline, mark the threshold `# proposed — calibrate after <N> days` and start with `action_on_breach: warn`; promote to `block-deploy` or `page-oncall` once calibrated.

## Workflow

1. **Confirm the characteristic and quantum** (Entry check).
2. **Reuse or define**: cite a Good Citizen id, or write the YAML above.
3. **Classify** along the four axes.
4. **Place it**:
   - triggered → CI on the PR (GitHub Actions) or an ArgoCD PreSync hook; static failures block the merge.
   - continual → metric emitted by the service, scraped by Prometheus, alert routed through the existing stack.
   - temporal → Kubernetes CronJob or scheduled CI job; results go to a weekly report.
5. **Wire the breach action.** A fitness function without an action is decoration.
6. **Close the status gate**: list the ids in the **Fitness functions** section of the decision record (location per repo: see Project context in `architecture-characteristics`). Relaxing a threshold also needs a record update.

## Portfolio review (temporal, suggested weekly)

- Never breached → threshold too loose, or redundant.
- Always breached → threshold too tight, or silent drift was accepted.
- Dominant characteristic without an active function → uncovered; open an issue.
- Expired exceptions → gate fails until renewed or fixed.

## Project context

Verify against the repo before relying on any item; these are snapshots.

**`aws-saas-platform`**

- Organize fitness functions by AWS Well-Architected pillar, matching `docs/well-architected-framework/<pillar>/changes/`. Reference the change path in `related_decision`.
- Signal sources: Prometheus/Grafana/tracing (P2), ArgoCD (P1), and CI/CD (P3) are **planned** — check `docs/well-architected-framework/README.md` and mark `source_status` accordingly. Live today: ALB/WAF metrics and logs in CloudWatch, Istio in the mesh.
- Each FastAPI service is its own quantum. A fitness function that requires deploying two services together signals coupling — surface it.
- Tenant isolation: `tenant-registry` is keyed by `pk = domain#<domain>` by design (domain → tenant lookup). For tenant-owned data, a triggered static check must reject any access pattern that is not scoped by `tenant_id`.
- Breach issues: Jira project `PLTF`.

**`wasp-agent`**

- Fitness functions about running workloads → Good Citizen catalog (`waspctl good-citizen`, exit codes `0`/`1`/`2`).
- Health exposed to the agent: as an agno tool today (MCP is future-only). Name tools `get_<characteristic>_<aspect>` (e.g., `get_performance_p95_by_service`); never a generic `query_metrics` or raw PromQL pass-through. Return `{value, threshold, verdict: pass|warn|fail, window, source}` so the agent acts on the verdict.
- The agent's own fitness functions: tool-call p95 latency, % of health tools returning a verdict, payload schema conformance, LLM token cost per request.
- CI lives in `.github/workflows/` (`ci.yaml`, `pull-request.yaml`). Breach issues: GitHub issues or `HANDOFF.md` Backlog.

## Push back when

- "Just add an alert" with no characteristic → ask which characteristic.
- Raw-PromQL tool → reshape into a semantic, verdict-returning tool.
- `invocation: manual` without a follow-up to automate → require the issue.
- A new `ff-*` duplicating a Good Citizen check → cite the existing id instead.
- A cross-service fitness function implying the quanta should merge → flag the coupling.

## Response shape

1. Characteristic and quantum. 2. Existing Good Citizen id **or** new YAML. 3. Classification. 4. Where it lives. 5. Action on breach. 6. One or two sentences ready to paste into the decision record's **Fitness functions** section.

Keep it tight; skip book theory unless asked.
