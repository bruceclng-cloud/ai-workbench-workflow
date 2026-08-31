# AI Workbench Workflow

A Codex-native software-development workflow for projects that want **durable product authority + deterministic execution + bounded specialist agents** without adopting a full distributed orchestration framework.

Product hierarchy:

**North → Bird → Wing → Feather → Tasks**

The hierarchy defines what the product means. The runtime decides where execution is, which agent is eligible to run next, what human gate blocks progress, and how review failures route upstream.

## v0.2

v0.1 was mostly a strong prompt protocol with a state validator. v0.2 adds the missing engine layer:

- declarative workflow definition + project overlays;
- durable per-run execution state and resume;
- append-only event journal with crash-repairable atomic snapshots;
- deterministic `dispatch`, `record-result`, and `record-review`;
- actual Codex custom agents and JIT step files;
- structured agent/reviewer result contracts;
- interactive human-only approval gates;
- frozen approved-intent hashes for Wing/Feather contracts;
- `PATCH / BAD_SPEC / INTENT_GAP / CORRECT_COURSE / DEFER` review routing;
- rollback-before-reroute for upstream review failures;
- bounded remediation loops;
- baseline/commit boundaries for deterministic rollback;
- installer + `doctor` checks;
- multiple durable runs with `new / list / use`.

## Architecture

```text
Human product authority
        │
        ▼
North → Bird → Wing → Feather → Tasks
                    │
                    ▼
        durable specs / UX / architecture
                    │
                    ▼
         declarative workflow definition
            + optional overlays
                    │
                    ▼
       deterministic local runtime
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
    dispatch      state       human gate
        │         /events          │
        ▼           │              ▼
 Codex custom       │           HUMAN
    agents           │
        │            │
        └──── result ┘
              │
              ▼
       deterministic routing
```

The parent Codex thread is the **Control Tower**. It does not invent orchestration. It asks the runtime what stage is active, loads one JIT step, invokes only the configured worker(s), and hands structured results back to the runtime.

## Install immediately

Requires Python 3.11+ and a current Codex release with project custom-agent/skill support.

```bash
git clone https://github.com/bruceclng-cloud/ai-workbench-workflow.git
cd ai-workbench-workflow
python3 install.py /path/to/your/project
```

The public repository ships the complete tested v0.2 source tree as seven compact text package parts (`workbench-workflow-v0.2.0.part*`). The bootstrap installer reassembles them, verifies SHA-256, safely extracts the source, and runs the canonical installer. Nothing else has to be downloaded.

To inspect the complete source before installing:

```bash
python3 install.py --extract-source ./source
```

The canonical installer merges the marked workflow block into an existing `AGENTS.md`, copies the Codex agents/skill/runtime definition, preserves existing project instructions, adds runtime paths to `.gitignore`, and runs `doctor`. It refuses conflicting workflow files unless `--force` is explicitly supplied.

Then, from the adopting project:

```bash
python3 .agents/skills/workbench-workflow/scripts/workflow.py new
python3 .agents/skills/workbench-workflow/scripts/workflow.py dispatch
```

Or tell the parent Codex session to use `$workbench-workflow`.

## Core commands

```bash
# health
python3 .agents/skills/workbench-workflow/scripts/workflow.py doctor

# durable runs
python3 .agents/skills/workbench-workflow/scripts/workflow.py new --wing WING-UX-001
python3 .agents/skills/workbench-workflow/scripts/workflow.py list
python3 .agents/skills/workbench-workflow/scripts/workflow.py use <run-id>

# state + next dispatch
python3 .agents/skills/workbench-workflow/scripts/workflow.py show
python3 .agents/skills/workbench-workflow/scripts/workflow.py validate
python3 .agents/skills/workbench-workflow/scripts/workflow.py dispatch

# worker result ingestion
python3 .agents/skills/workbench-workflow/scripts/workflow.py record-result result.json
python3 .agents/skills/workbench-workflow/scripts/workflow.py record-review blind.json edge.json verify.json

# human-only gate
python3 .agents/skills/workbench-workflow/scripts/workflow.py approve human_approve_ux
```

## Review diagnosis

Every verified finding is one of:

- `PATCH` — contract is correct; direct implementation correction.
- `BAD_SPEC` — intent exists, executable Feather contract was wrong/incomplete.
- `INTENT_GAP` — a visible decision genuinely needs the human.
- `CORRECT_COURSE` — upstream Wing/design/product assumption needs reconsideration.
- `DEFER` — real but not caused/owned by the active Feather.

The runtime uses precedence:

`CORRECT_COURSE > INTENT_GAP > BAD_SPEC > PATCH > DEFER/PASS`

For upstream categories, implementation must be rolled back to the recorded baseline before the runtime routes upstream. Bad implementation therefore does not become accidental authority.

## Human authority

Human-only events are rejected by the ordinary transition path. Approval requires an interactive terminal and exact confirmation phrase. This is an anti-accident workflow boundary, not an OS security sandbox against a process that already controls the workstation.

Technical PASS never equals product acceptance. Human rejection overrides prior technical verification.

## Runtime state

Local runtime data is gitignored:

```text
.workbench-workflow/runs/<run-id>/
  state.json
  events.jsonl
```

`events.jsonl` is append-only and stores post-transition state. `state.json` is an atomically replaced snapshot and can repair from the journal after an interrupted write.

## Influences

The design adapts proven ideas rather than vendoring another framework:

- **BMAD** — JIT step files, bounded Build units, frozen human intent, upstream review diagnosis, UX-before-build, Correct Course.
- **GitHub Spec Kit** — declarative workflow definition, validation, durable run/resume model, overlays and control-flow mindset.
- **OpenSpec** — keep the human-facing process understandable and artifact-driven.
- **CrewAI / LangGraph / agent runtimes** — separate workflow definition, execution runtime and replaceable workers; use checkpoint/interrupt thinking.

No upstream framework source code is vendored here.

## Scope

v0.2 is intentionally a **Codex-native deterministic workflow runtime**, not a distributed agent platform. It does not yet provide remote queues, distributed locks, cloud tracing, provider-neutral worker execution, or cryptographic human identity. Its boundaries are designed so those can be added later without changing North/Bird/Wing/Feather semantics.

## License

MIT. See `LICENSE` and `NOTICE.md`.
