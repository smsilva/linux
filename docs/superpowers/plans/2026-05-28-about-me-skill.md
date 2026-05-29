# About-Me Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a Claude Code skill `about-me` that loads Silvio's professional context (timeline, stack, credentials, preferences) on demand via a pointer table.

**Architecture:** Skill lives at `claude/skills/about-me/` with a thin `SKILL.md` entry point and four reference files (`timeline.md`, `stack.md`, `credentials.md`, `preferences.md`). Each reference loads only when its task type matches. Content is in English; conversation with the user stays pt-BR.

**Tech Stack:** Plain Markdown. No build step. Symlink from `~/.claude/skills/about-me/` is created by the existing `install.sh` flow (already symlinks the entire `claude/skills/` tree).

**Reference spec:** `docs/superpowers/specs/2026-05-28-about-me-skill-design.md`

---

## File Structure

| File | Responsibility |
|---|---|
| `claude/skills/about-me/SKILL.md` | Entry point: frontmatter, identity paragraph, current focus, pointer table |
| `claude/skills/about-me/timeline.md` | Career 1997–present, one section per role, newest first |
| `claude/skills/about-me/stack.md` | Categorized technical stack with confidence levels |
| `claude/skills/about-me/credentials.md` | Education + active/expired certifications |
| `claude/skills/about-me/preferences.md` | Tone, language, methods (summary of `CLAUDE.md`) |

All files small and focused. No file expected over ~150 lines.

---

### Task 1: Create skill directory and SKILL.md entry point

**Files:**
- Create: `claude/skills/about-me/SKILL.md`

- [ ] **Step 1: Create the directory**

Run:
```bash
mkdir -p /home/silvios/git/linux/claude/skills/about-me
```

- [ ] **Step 2: Write SKILL.md**

Create `claude/skills/about-me/SKILL.md` with this exact content:

```markdown
---
name: about-me
description: Use when writing a CV, bio, LinkedIn post, or talk abstract for Silvio; when calibrating technical recommendations to Silvio's experience ("do I have experience with X?"); or when an introduction or speaker section is needed. Loads timeline, stack, credentials, and preferences on demand via the pointer table.
---

# About Silvio

**Who:** Silvio Silva — Developer Master at CI&T (since 11/2019) — Belo Horizonte/MG, Brazil. Portuguese (native), English (professional).

**Current focus (2025–2026):** Cloud Engineering on Azure and AWS; Crossplane with KCL; Claude Code, MCP, and agent skills; Python; Backstage; Terraform Stacks.

**Long-running domains:** Healthcare (15+ years — telemedicine, health insurance, population risk management, telehealth), retail automation, microservices, GitOps.

## How to use this skill

Read this file first. Then read ONLY the reference file(s) listed in the pointer table for the current task. Do not load all references unless the task spans multiple dimensions (e.g., a full CV needs timeline + stack + credentials).

| Task | File |
|---|---|
| CV, chronological bio, career journey, "I worked at X" | `timeline.md` |
| Calibrate technical recommendation, "do I know X?", current stack | `stack.md` |
| Certifications, education, "am I certified in X?" | `credentials.md` |
| Tone, language, working style, methods | `preferences.md` |
```

- [ ] **Step 3: Verify the file**

Run:
```bash
head -5 /home/silvios/git/linux/claude/skills/about-me/SKILL.md
```
Expected: starts with `---` then `name: about-me`.

- [ ] **Step 4: Commit**

```bash
cd /home/silvios/git/linux
git add claude/skills/about-me/SKILL.md
git commit -m "feat(claude/skills/about-me): add SKILL.md entry point"
```

---

### Task 2: Write timeline.md (career history)

**Files:**
- Create: `claude/skills/about-me/timeline.md`

- [ ] **Step 1: Write the file**

Create `claude/skills/about-me/timeline.md` with this exact content:

````markdown
# Career timeline

Newest first. English summary bullets are canonical; original pt-BR bullets from LinkedIn are preserved in collapsible appendices for direct quoting.

## CI&T — Developer Master (09/2022 – Present, Belo Horizonte/MG, Hybrid)

- Cloud Operations team; strategic initiatives in cloud infra, automation, AI integration, and cost optimization.
- Azure services delivered: Cosmos DB (MongoDB), PostgreSQL, Container Apps, API Management, B2C.
- Azure Monitor rollout — centralized audit logs, observability, proactive monitoring.
- AWS: design and provisioning of a multi-tenant SaaS platform on EKS — ALB, Istio Service Mesh, WAF, Amazon Cognito, DynamoDB, federated auth with multiple Identity Providers.
- Crossplane with KCL for cloud resource provisioning and Composition authoring.
- Uses Claude Code (Anthropic) in development and learning workflows — accelerates automation, code generation, and problem-solving.

<details><summary>Original (pt-BR)</summary>

- Como Developer Master no time de Cloud Operations, contribuo com iniciativas estratégicas nas áreas de infraestrutura em nuvem, automação, integração de IA e otimização de custos.
- Participei da implementação de serviços Azure como Cosmos DB (MongoDB), PostgreSQL, Container Apps, API Management e B2C.
- Atuei no projeto de implantação do Azure Monitor, centralizando logs de auditoria, habilitando observabilidade e monitoramento proativo.
- No contexto da AWS, tenho atuado em projetos que incluem o design e provisionamento de uma plataforma SaaS multi-tenant no EKS, com ALB, Istio Service Mesh, WAF, Amazon Cognito e DynamoDB incluindo autenticação federada com múltiplos Identity Providers.
- Apoio a implementação e uso do Crossplane no provisionamento de recursos em nuvem com KCL (Constraint-based Record & Functional Language) para gerenciamento de configurações e criação de Compositions.
- Uso o Claude Code (Anthropic) nos fluxos de desenvolvimento e aprendizado, acelerando a automação, geração de código e resolução de problemas técnicos.

</details>

## CI&T — Systems Architect (04/2021 – 09/2022, Belo Horizonte/MG)

- Architect role on Global B2B initiatives.
- Terraform Stacks adoption; authored `tf-packager`.
- Spoke at TDC (The Developer's Conference).

## CI&T — Software Engineer (11/2019 – 04/2021, Belo Horizonte)

- Cloud Engineer in a Cloud Engineering Squad.
- Stack: Spring Boot, Kubernetes (AKS, Minikube, Kind), Helm, Istio Service Mesh, Envoy, Telepresence, ETCD, Docker, Vagrant, Multipass, Python, microservices, Robot Framework, Appium, Bash, JMeter, tmux, SQL Server, MongoDB (Azure Cosmos DB and Mongo Atlas), Azure DevOps, Azure Front Door, Imperva, New Relic, JIRA, Mockito, Clean Architecture.
- Obtained CKA (Certified Kubernetes Administrator) certification in 12/2020.

## Optum — Senior Software Developer / Tech Lead (05/2016 – 11/2019, Belo Horizonte/MG)

- Drove DevOps adoption and task automation using Ansible, OpenStack, Docker, and Kubernetes.
- Standardized Git + Maven builds; created reusable projects for core company features versioned independently.
- Built RESTful microservices for service integration, including mission-critical internal systems to monitor diabetic patients and centralized SMS/email delivery with scheduled dynamic reports.
- Contributed to health-program goal tracking by producing cross-system reports that helped supervision focus on the most relevant patient, team, and business issues.
- Acted as Scrum Master and technical specialist across multiple project teams.

<details><summary>Original (pt-BR)</summary>

- Incentivei a adoção de práticas DevOps e automação de tarefas usando Ansible, OpenStack, Docker e Kubernetes.
- Implementei o uso de Git e Maven para controlar os builds criando projetos reutilizáveis para as principais funcionalidades da empresa organizados em diferentes versões.
- Implementei microservices RESTFul para integração de vários serviços incluindo os de missão crítica internos para monitorar pacientes diabéticos e serviços essenciais à operação como envio automático e centralizado de sms e e-mails com relatórios dinâmicos e periódicos previamente agendados.
- Contribuí para o controle e alcance das metas das ações de saúde com elaboração de relatórios mesclando dados de vários sistemas auxiliando a supervisão a focar em questões relevantes para os pacientes, a equipe e o negócio.
- Participei de projetos como Scrum Master, Especialista Técnico e em outros papéis para auxiliar os times a se organizar e alcançar os objetivos de negócio.

</details>

## MedAlliance Net — Senior Systems Analyst (02/2009 – 04/2016, Recife)

- Analysis, implementation, integration, and support of systems.
- Built an integration routine processing millions of transactions per day via Web Services or SFTP, eliminating delays and failures from the previous manual process.
- Helped open the Belo Horizonte branch and contributed to telemedicine projects with large telecom and healthcare companies.
- Integrated partners like Zenvia to deliver SMS-based health programs — e.g., the Sweet Talk project for diabetes patients.
- Active contributor on Central Sentinela and VivaMais (chronic-patient risk management) — multidisciplinary teams, remote patient monitoring, cross-system integration.

<details><summary>Original (pt-BR)</summary>

- Responsável pela análise, implementação, integração e sustentação de sistemas.
- Contribuí com o desenvolvimento da rotina de integração capaz de processar milhões de transações por dia através de Web Services ou SFTP eliminando atrasos e falhas no processo de integração que anteriormente era manual e com gerenciamento limitado.
- Colaborei em vários processos estratégicos como a implantação da filial em Belo Horizonte e em projetos na área de Telemedicina envolvendo grandes empresas da área de telecomunicação e saúde.
- Através de integrações de parceiros como a Zenvia, implementamos vários serviços que aliavam o uso de SMS a programas de saúde como o projeto Sweet Talk direcionado a portadores de diabetes.
- Participei ativamente dos projetos Central Sentinela e VivaMais (Gestão de Risco de pacientes crônicos) que envolveram equipes multidisciplinares, monitoramento remoto de pacientes e integração de vários sistemas.

</details>

## CSI — Comércio Soluções Inteligentes — Technical Lead (02/2008 – 01/2009, Recife)

- Senior Systems Analyst and Technical Lead of the support team for the P2K software (retail automation, Java + object-oriented and relational databases).
- Owned the client relationship for the maintenance cell; tracked and supported the team across all open work.

## OPS Planos de Saúde — Development Coordinator (01/2006 – 01/2008, Recife)

- Business Analyst and Coordinator of the software development team; helped adopt agile methodologies using XPlanner for use-case tracking.
- Led the migration of the management-system database from Informix IDS 7 to Oracle 10g R2, stabilizing the entire operation within one week.
- Built batch routines for bank and partner integrations using variable-data PostScript files for print-service bureaus.

## Inteligência Informática — Programmer (2003 – 2005, Recife)

- Maintained a Delphi/Informix management-information system and implemented an ERP (Oracle Forms and Reports) at Policlínica Santa Clara.

## Apply Solutions — Programmer (2002 – 2003, Recife)

- Developed the Point of Sale (POS) system (Delphi/Oracle) for a large retail company; implemented multithreading for receipt and invoice generation, significantly cutting checkout wait times.

## Policlínica Santa Clara — Programmer (1999 – 2002, Recife)

- Part of the team that built the "Health Insurance", "Laboratory", and "Medical Billing" modules using Delphi and Informix.

## Layout Informática — Instructor (06/1997 – 04/1999, Recife)

- First professional experience. Instructor for technology courses (Microsoft Office, CorelDRAW, PageMaker/Adobe InDesign); teaching assistant in Clipper and Delphi programming courses.

---

## Career arc

Recife (1997–2008) → Belo Horizonte (2009–present). Healthcare domain throughout (Policlínica Santa Clara → OPS → MedAlliance → Optum → CI&T healthcare clients). Pivoted to cloud engineering at CI&T (2019), then to AI-assisted development and agentic tooling from 2025 onward.
````

- [ ] **Step 2: Verify**

Run:
```bash
wc -l /home/silvios/git/linux/claude/skills/about-me/timeline.md
grep -c "^## " /home/silvios/git/linux/claude/skills/about-me/timeline.md
```
Expected: line count > 100; heading count == 11 (one per role) + 1 (Career arc) = 12.

- [ ] **Step 3: Commit**

```bash
cd /home/silvios/git/linux
git add claude/skills/about-me/timeline.md
git commit -m "feat(claude/skills/about-me): add career timeline reference"
```

---

### Task 3: Write stack.md (technical stack with levels)

**Files:**
- Create: `claude/skills/about-me/stack.md`

- [ ] **Step 1: Write the file**

Create `claude/skills/about-me/stack.md` with this exact content:

```markdown
# Technical stack

Confidence levels: **expert** (years of production use), **strong** (multiple projects, recent), **familiar** (used in projects but not primary), **learning** (current focus, not yet deep).

Rationale (which role gave the experience) lives in `timeline.md`, not here.

## Cloud

- **Azure** (expert) — AKS, Cosmos DB, PostgreSQL, Container Apps, API Management, B2C, Front Door, DevOps, Monitor
- **AWS** (strong) — EKS, ALB, WAF, Cognito, DynamoDB
- **OpenStack** (familiar) — legacy from Optum

## Kubernetes & platform

- **Kubernetes** (expert) — production AKS, Istio Service Mesh, KEDA autoscalers, Helm, Envoy
- **Crossplane + KCL** (learning) — current focus at CI&T
- **Backstage**, **GitHub Enterprise**, **Bitbucket** — platform engineering surface

## Infrastructure as Code

- **Terraform / Stacks** (expert) — authored `tf-packager`
- **Ansible** (strong) — DevOps standardization at Optum

## Languages

- **Java / J2EE** (expert) — 15+ years
- **Bash** (expert) — scripts under `~/git/linux/scripts/bin/`
- **Python** (strong, growing focus)
- **SQL / PL-SQL** (strong)
- **Delphi** (legacy) — early career, no longer active

## AI & agents (2026 focus)

- Claude Code, MCP, Anthropic agent skills
- RAG, Agno, Pydantic
- Prompt engineering, AI-assisted development workflows

## Messaging & integration

- Apache Kafka + Spring Integration + KEDA Kafka autoscaler
- JMS / ActiveMQ

## Observability

- Prometheus, New Relic, Azure Monitor

## Domain expertise

- **Healthcare** (15+ years) — telemedicine, health insurance, telehealth, population risk management
- **Retail automation** — POS, sales
- **Multi-tenant B2B SaaS** — federated identity, global rollouts
```

- [ ] **Step 2: Verify**

Run:
```bash
grep -c "^## " /home/silvios/git/linux/claude/skills/about-me/stack.md
```
Expected: 8 category headings.

- [ ] **Step 3: Commit**

```bash
cd /home/silvios/git/linux
git add claude/skills/about-me/stack.md
git commit -m "feat(claude/skills/about-me): add technical stack reference"
```

---

### Task 4: Write credentials.md (education + certifications)

**Files:**
- Create: `claude/skills/about-me/credentials.md`

- [ ] **Step 1: Write the file**

Create `claude/skills/about-me/credentials.md` with this exact content:

```markdown
# Credentials

## Education

- **Postgraduate, Agile Project Management** — CESAR EDU, 2011–2012
- **Bachelor, Business Administration** — Universidade Salgado de Oliveira, 2002–2005

## Active certifications (2026)

| Certification | Issuer | Date | Credential |
|---|---|---|---|
| Claude 101 | Anthropic | 05/2026 | `mb6zh3by927b` ([verify](https://verify.skilljar.com/c/mb6zh3by927b)) |
| Introduction to agent skills | Anthropic | 05/2026 | `a367ac9hzjoi` |
| Introduction to Model Context Protocol | Anthropic | 05/2026 | `w6bg5oyo4aky` |
| Claude Code in Action | Anthropic | 05/2026 | `xishdw9jh24j` |
| Desenvolvendo Agentes de IA | Visie | 04/2026 | `FnkJHF` ([verify](https://certificados.visie.com.br/c/FnkJHF)) |

## Expired

- **CKA — Certified Kubernetes Administrator** — Linux Foundation, 12/2020 → 12/2023 (expired)

## Alura courses

34 courses, ~400h total — Java fundamentals, EJB, Maven, SOLID, Design Patterns, Java 8 streams/lambdas, Android. Full list on LinkedIn.
```

- [ ] **Step 2: Verify**

Run:
```bash
grep -c "Anthropic" /home/silvios/git/linux/claude/skills/about-me/credentials.md
```
Expected: 4 (one per Anthropic cert row).

- [ ] **Step 3: Commit**

```bash
cd /home/silvios/git/linux
git add claude/skills/about-me/credentials.md
git commit -m "feat(claude/skills/about-me): add credentials reference"
```

---

### Task 5: Write preferences.md (tone, language, methods)

**Files:**
- Create: `claude/skills/about-me/preferences.md`

- [ ] **Step 1: Write the file**

Create `claude/skills/about-me/preferences.md` with this exact content:

```markdown
# Working preferences

> Canonical source: `~/.claude/CLAUDE.md`. This is a summary scoped to introductions and recommendations. If they diverge, `CLAUDE.md` wins.

## Communication

- Concise, actionable; no preamble ("Sure!", "Great question!"); no hedging ("Note that…", "Keep in mind…").
- Don't restate the question. Explain only non-obvious logic.

## Languages

- **Conversation:** pt-BR.
- **Written artifacts** (skills, docs, code comments): English.
- Never translate technical terms (API, endpoint, commit, push, pull request, cache, parse, GitOps).

## Methods

- **Walk Skeleton** — ship a thin end-to-end slice early for feedback.
- **TDD** when applicable.
- **Conventional Commits** — enforced by the git `commit-msg` hook.

## Tooling

- Bash scripts under `~/git/linux/scripts/bin/` (conventions in the `bash-scripts` skill).
- Claude Code as primary AI dev tool.
- Ubuntu 24.04.
```

- [ ] **Step 2: Verify**

Run:
```bash
test -f /home/silvios/git/linux/claude/skills/about-me/preferences.md && echo OK
```
Expected: `OK`.

- [ ] **Step 3: Commit**

```bash
cd /home/silvios/git/linux
git add claude/skills/about-me/preferences.md
git commit -m "feat(claude/skills/about-me): add preferences reference"
```

---

### Task 6: Verify the symlink target resolves

**Files:**
- None (verification only)

Background: `claude/skills/` is already symlinked to `~/.claude/skills/` by the project's `install.sh`. We only need to confirm the new directory is reachable.

- [ ] **Step 1: Check the symlink chain**

Run:
```bash
ls -la /home/silvios/.claude/skills/about-me/
```
Expected: lists `SKILL.md`, `timeline.md`, `stack.md`, `credentials.md`, `preferences.md`.

If the directory does NOT exist (because `~/.claude/skills/` is symlinked file-by-file rather than as a whole), run:
```bash
ls -la /home/silvios/.claude/skills/ | grep about-me
```
If empty, re-run `install.sh` from the repo root:
```bash
cd /home/silvios/git/linux && ./install.sh
```
Then re-run the first check.

- [ ] **Step 2: Verify SKILL.md is readable through the symlink**

Run:
```bash
head -3 /home/silvios/.claude/skills/about-me/SKILL.md
```
Expected: `---` / `name: about-me` / `description: …`.

- [ ] **Step 3: No commit needed** — this is verification only.

---

### Task 7: Acceptance test — manually verify discovery and routing

**Files:**
- None (manual smoke test)

These three checks correspond to the acceptance criteria in the spec.

- [ ] **Step 1: Verify the skill appears in Claude Code's skill list**

Start a new Claude Code session (`/clear` in current session, or new terminal). Ask:
> "Quais skills você tem disponíveis com `about` no nome?"

Expected: `about-me` listed.

- [ ] **Step 2: Routing test — stack question**

Ask:
> "What's my background with Crossplane?"

Expected: Claude invokes `about-me`, reads `SKILL.md`, then reads `stack.md` (and optionally `timeline.md` for context), reports `Crossplane + KCL (learning)` with the CI&T Developer Master context.

- [ ] **Step 3: Routing test — credentials question**

Ask:
> "Do I have a CKA?"

Expected: Claude reads `credentials.md`, reports the CKA as expired in 12/2023.

- [ ] **Step 4: Routing test — short bio**

Ask:
> "Write me a 3-sentence bio for a TDC talk submission."

Expected: bio mentions Developer Master at CI&T + cloud/AI focus + healthcare background, read from `SKILL.md` alone (no need to load all references).

- [ ] **Step 5: Negative test — irrelevant context**

Ask something unrelated:
> "Como leio um arquivo em bash?"

Expected: `about-me` is NOT invoked. (If it is, the SKILL.md description is too broad — revisit.)

- [ ] **Step 6: Commit the final state if anything was tweaked**

```bash
cd /home/silvios/git/linux
git status
```
If there are uncommitted tweaks from the acceptance run:
```bash
git add claude/skills/about-me/
git commit -m "fix(claude/skills/about-me): refine description after acceptance test"
```

---

### Task 8: Merge to main and push

**Files:**
- None (git workflow)

- [ ] **Step 1: Inspect the branch**

Run:
```bash
cd /home/silvios/git/linux
git log --oneline main..skill/about-me
```
Expected: 6 commits (1 spec + 5 skill files), plus any acceptance fix-up commit.

- [ ] **Step 2: Push branch and open PR (if PR flow is used) OR merge locally**

Local merge (no PR required for personal repo):
```bash
git checkout main
git merge --no-ff skill/about-me -m "feat(claude/skills/about-me): add about-me skill"
git push origin main
```

Or, if you prefer a PR:
```bash
git push -u origin skill/about-me
gh pr create --title "feat(claude/skills/about-me): add about-me skill" --body "Implements docs/superpowers/specs/2026-05-28-about-me-skill-design.md per docs/superpowers/plans/2026-05-28-about-me-skill.md"
```

- [ ] **Step 3: Confirm completion**

Run:
```bash
git log --oneline -1
```
Expected: latest commit is the merge (or the last skill commit if fast-forwarded).
