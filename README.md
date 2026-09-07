# AI Workbench Workflow

A Codex-native development workflow for projects that need durable product authority, deterministic execution, resumable state and bounded specialist agents.

## Canonical hierarchy

**North → Bird → Wing → Feather**

A **Feather is the terminal executable unit**. It contains the complete bounded execution contract and takes action directly. Implementation details may live inside a Feather as ordinary steps or checklists, but they are not another hierarchy level and do not receive separate IDs, lifecycles, review gates or documents.

See `WORKFLOW.md` for the current workflow authority.

## Execution model

One explicitly activated Wing is the normal product execution boundary.

Within that Wing, dependency-ready Feathers run through implementation, targeted verification, commit, independent adversarial review and bounded remediation. After all required Feathers verify, a separate Wing Integration Review judges the assembled result.

**Wing Integration Review PASS → Wing verified → STOP.**

The runtime must never infer permission to activate another Wing. Technical verification never equals human acceptance.

## Runtime design

v0.2 introduced:

- declarative workflow definition and project overlays;
- durable per-run state and resume;
- append-only event journal and atomic snapshots;
- deterministic `dispatch`, `record-result` and `record-review`;
- Codex custom agents and JIT execution steps;
- structured worker/reviewer result contracts;
- human-only approval gates;
- frozen Wing/Feather intent hashes;
- `PATCH / BAD_SPEC / INTENT_GAP / CORRECT_COURSE / DEFER` review routing;
- rollback-before-upstream-reroute;
- bounded remediation loops;
- baseline/commit boundaries;
- installer/doctor support and multiple durable runs.

The parent Codex thread is the **Control Tower**. It asks the runtime for the current state and eligible transition rather than inventing orchestration.

## Current installation status

The repository retains the tested **v0.2.0** source package as seven compact historical release parts. That artifact was published under MIT and remains available for reproducibility.

However, v0.2.0 may inject superseded `Task`/`Tasks` hierarchy wording. Current authority ends at Feather. To prevent the old wording from contaminating a live project, the bootstrap installer now **refuses normal installation of v0.2.0 by default** until a corrected package is published.

Inspect the historical source safely:

```bash
python3 install.py --extract-source ./source
```

A deliberate legacy reproduction can still use:

```bash
python3 install.py /path/to/project --allow-legacy-v0-2
```

Do **not** use that legacy override as the current Personal AI Workbench workflow installation path.

## Runtime commands in an installed workflow

```bash
python3 .agents/skills/workbench-workflow/scripts/workflow.py doctor
python3 .agents/skills/workbench-workflow/scripts/workflow.py new --wing WING-UX-001
python3 .agents/skills/workbench-workflow/scripts/workflow.py list
python3 .agents/skills/workbench-workflow/scripts/workflow.py use <run-id>
python3 .agents/skills/workbench-workflow/scripts/workflow.py show
python3 .agents/skills/workbench-workflow/scripts/workflow.py validate
python3 .agents/skills/workbench-workflow/scripts/workflow.py dispatch
python3 .agents/skills/workbench-workflow/scripts/workflow.py record-result result.json
python3 .agents/skills/workbench-workflow/scripts/workflow.py record-review blind.json edge.json verify.json
python3 .agents/skills/workbench-workflow/scripts/workflow.py approve human_approve_ux
```

## Review diagnosis

- `PATCH` — implementation correction inside a valid contract.
- `BAD_SPEC` — the executable Feather contract is wrong or incomplete.
- `INTENT_GAP` — a human/product decision is required.
- `CORRECT_COURSE` — an upstream Wing/design/product assumption must be reconsidered.
- `DEFER` — a real issue outside current ownership.

Precedence:

`CORRECT_COURSE > INTENT_GAP > BAD_SPEC > PATCH > DEFER/PASS`

Incorrect implementation must not become accidental authority.

## Human authority

Human-only events cannot be produced by the ordinary transition path. Approval is an explicit interactive boundary.

Technical PASS does not mean product acceptance. Human rejection overrides prior technical verification.

## Runtime state

Local state is gitignored:

```text
.workbench-workflow/runs/<run-id>/
  state.json
  events.jsonl
```

The event journal is append-only. The state snapshot is atomically replaced and can be repaired from the journal after interruption.

## Scope

This is a Codex-native deterministic workflow runtime, not a distributed agent platform. It does not currently provide remote queues, distributed locks, cloud tracing, provider-neutral worker execution or cryptographic human identity.

## License

Current repository development is under **PolyForm Strict License 1.0.0**. See `LICENSE`.

Historical releases already distributed under MIT, including v0.2.0, retain the permissions that applied when they were released. See `LEGACY-LICENSE.md`.

Copyright © 2026 Bruce Ng. All rights not expressly granted by the applicable license are reserved.
