# KYC-Agent

## 📐 Phase 1 Infrastructure – Progress Log (Steps 0 → 3)

| Step | When | What we did | Why it matters |
|------|------|-------------|----------------|
| **0  Repo bootstrap** | 2025-06-13 | • `git init kyc-agent/`<br>• Created directories `agent/ bot/ infra/ docs/`<br>• Added proposal & design PDFs in `docs/`<br>• Committed skeleton to GitHub | Gives every contributor a single source-of-truth and a clean workspace layout. |
| **1  Toolchain setup** | 2025-06-13 | • Installed AWS CLI v2, Node 18 LTS, CDK v2, Python 3.12<br>• Configured local virtual-env in `infra/.venv` | Ensures deterministic builds; no leaking global packages. |
| **2  CDK app scaffold** | 2025-06-13 | • `cdk init app --language python` inside `infra/`<br>• Added lint workflow (`.github/workflows/ci.yml`) | Establishes automated synth/lint on every push. |
| **3-A Dependencies** | 2025-06-13 | `pip install aws-cdk-lib constructs` in venv | CDK runtime libs pinned for reproducibility. |
| **3-B Stacks** | 2025-06-13 | **MessagingStack**<br>  ↳ `TriggerQueue` + DLQ (SQS)<br>  ↳ Weekly EventBridge rule<br>**PersistenceStack**<br>  ↳ `KycIndex` (DynamoDB)<br>  ↳ `RawArtifacts` (S3, versioned)<br>**ComputeStack**<br>  ↳ Stub Lambda **TriggerManager** (Python 3.12) | Clean 3-tier separation:<br>• Messaging = event intake<br>• Persistence = durable state<br>• Compute = code that scales/changes often |
| **3-C Stub Lambda** | 2025-06-13 | Added `infra/agent_lambda_stub/handler.py` (prints “hello”) | Allows CDK to deploy a real Lambda so logs/permissions are validated before we add business logic. |
| **3-D app.py wiring** | 2025-06-13 | `app.py` imports the three stack classes (`infra.messaging_stack`, …) | CDK can now synth all stacks in one command. |
| **3-E Synth test** | 2025-06-13 | `cd infra && cdk synth` → success | Proved local compile works; template stored in `infra/cdk.out/`. |
| **3-F Bootstrap + Deploy** | 2025-06-13 | • Fixed AWS profile region (`us-east-1`)<br>• `cdk bootstrap --profile kyc-dev`<br>• `cdk deploy --all --profile kyc-dev` | Provisioned bootstrap resources & deployed our three stacks to the **dev AWS account**.<br/>Verified in console: SQS, DynamoDB, S3, Lambda all live. |
| **3-G Git push** | 2025-06-13 | Committed stacks, stub Lambda, updated `.gitignore`, removed unused scaffold files | Repo history now contains a reproducible, deployable infra baseline. |

### ✅ Current state

* **Infra**: Messaging, Persistence, and Compute stacks running in *dev* (us-east-1).  
* **Lambda**: placeholder `TriggerManager` logging “hello”.  
* **CI**: Black/flake8 lint job green on every push.

### ⏭️ Next up (Step 4)

1. Replace stub **TriggerManager** with real code: HTTP webhook → normalize event → push to `TriggerQueue`.  
2. Add first data collector (HubSpot) & wire Orchestrator logic.  
3. Extend CDK to include new Lambdas and IAM perms.



### Complete flow is below

## 🚧 Project Build Milestones

| Step | Focus | What we added (conceptually) | Why it matters |
|------|-------|------------------------------|----------------|
| **0 — Repo & Tooling** | Foundation | • `git init` skeleton (`agent/ bot/ infra/ docs/`).<br>• Added proposal & design PDFs.<br>• Installed AWS CLI v2, Node 18 LTS, Python 3.12, CDK v2; created local `.venv`. | Gives every contributor a clean, version-controlled workspace and deterministic build tools. |
| **1 — CDK Scaffold** | Infra bootstrap | • `cdk init app --language python` inside `infra/`.<br>• CI workflow (`black` lint) on every push. | Establishes automated synth/lint and a baseline CDK project. |
| **2 — Dependencies** | Prep | `pip install aws-cdk-lib constructs` in virtual-env. | Pins library versions for reproducible deploys. |
| **3 — Core Stacks** | Infrastructure baseline | • **MessagingStack** → `TriggerQueue` + DLQ (SQS) + weekly EventBridge rule.<br>• **PersistenceStack** → `KycIndex` (DynamoDB) + `RawArtifacts` (S3, versioned).<br>• **ComputeStack** → stub **TriggerManager** Lambda (Python 3.12). | Clean 3-tier split:<br>Messaging = event intake; Persistence = durable state; Compute = code that changes often. |
| **4 — TriggerManager** | Event ingress | • Replace stub with real Lambda.<br>• API Gateway REST endpoint `/webhook` → TriggerManager.<br>• Normalizes incoming payloads and pushes jobs onto `TriggerQueue`. | Turns external webhooks (DAY2 signup, Jira, Teams) into uniform SQS jobs for downstream fan-out. |
| **5 — Orchestrator + Collectors** | Data fan-out & gathering | • **Orchestrator Lambda** (SQS → async fan-out).<br>• Collector plug-ins (start with **HubSpot** for website/LinkedIn/contacts).<br>• Persist every raw payload to `S3/RawArtifacts`. | Builds a “bundle” of fresh customer facts per trigger; isolates API secrets; supports individual retries/back-off. |
| **6 — Summarizer & Validator (LLM-1 / LLM-2)** | AI processing & quality gate | • **Summarizer Lambda** calls GPT-4o to convert raw JSON → structured KYC JSON.<br>• **Validator Lambda** (2nd GPT-4o) checks hallucinations/citations → returns **VALID** or **FLAGGED**. | Produces human-readable insights while enforcing a double-LLM guard-rail so bad data never auto-publishes. |
| **7 — PageManager & Notifier** | Publish & notify | • Render Jinja2 template → **draft** Confluence page.<br>• Save `pageId` ↔ `customerId` in DynamoDB.<br>• **Notifier Lambda** posts Approve/Reject Adaptive Card to Teams. | Keeps an audit trail and gives humans final sign-off before a page is published. |
| **8 — Jira & Metabase Updaters** | Event-driven refresh | • Jira webhook → Collector updates **Priority Asks** table rows.<br>• Metabase Collector + LinkedIn/news refresh on weekly cron. | Keeps KYC pages living documents instead of static snapshots. |
| **9 — Teams Slash-Commands** | Human-triggered updates | • Extend Teams bot: `/update <customer>` queues a **TeamsCommand** trigger.<br>• `/notes` uploads meeting transcript → MeetingNotes Collector. | Lets CS / PAB kick off ad-hoc updates without leaving Teams. |
| **10 — Observability & Guard-Rails** | Stability | • AWS Powertools structured logs + X-Ray tracing.<br>• CloudWatch alarms on DLQ length & Lambda error rate.<br>• Cost & latency dashboards. | Detects failures quickly and prevents runaway spend. |
| **11 — Docs & Handoff** | Enable other users | • `docs/dev-setup.md` for engineers.<br>• `docs/cs-playbook.md` for Customer Success.<br>• Architecture & sequence diagrams checked in. | Makes the system maintainable and easy to onboard new team members. |

> **Current status:** Steps 0 → 3 are complete and deployed in the *dev* AWS account (us-east-1) — stub TriggerManager prints “hello”.  
> **Next up:** Implement Step 4 – real TriggerManager Lambda + API Gateway ingress.

