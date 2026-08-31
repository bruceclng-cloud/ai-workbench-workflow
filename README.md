# AI Workbench Workflow

A Codex-native software-development workflow for projects that want **durable product authority + deterministic execution + bounded specialist agents** without adopting a full orchestration framework.

> **Public distribution note:** this repository's one-command download ships the complete v0.2 source tree in `workbench-workflow.bundle.json`. `install.py` verifies every bundled file, extracts it to a temporary directory, and runs the canonical installer. Use `python3 install.py --extract-source ./source` if you want the full source tree expanded for inspection.

Product hierarchy:

**North → Bird → Wing → Feather → Tasks**

The hierarchy defines what the product means. The workflow runtime decides where execution is, which agent is eligible to run next, what human gate blocks progress, and how review failures route upstream.

## What changed in v0.2

v0.1 was mostly a strong prompt protocol with a state validator. v0.2 adds the missing engine layer:

- declarative `workflow/definition.json` rather than stage routing hard-coded only in prose;
- project overlays under `workflow/overlays/`;
- one durable runtime record per execution under `.workbench-workflow/runs/<run-id>/`;
- append-only event journal + crash-repairable snapshots;
- atomic writes and per-run process locks;
- deterministic `dispatch`, `record-result`, and `record-review` commands;
- structured agent/reviewer result contracts;
- interactive human-only approval commands;
- frozen approved-intent hashes for Wing/Feather contracts;
- BAD_SPEC / INTENT_GAP / CORRECT_COURSE rollback-before-reroute semantics;
- five allowed remediation loops, blocking on the sixth;
- local baseline/Feather commit boundaries for reliable rollback;
- installer + `doctor` command so a fresh download can be adopted immediately;
- multi-run `new / list / use` support.

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
         workflow/definition.json
            + optional overlays
                    │
                    ▼
      Workbench zero-dependency runtime
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

The parent Codex thread is the **Control Tower**. It does not invent orchestration. It asks the runtime what stage is active, loads one JIT step, invokes the configured custom agent(s), and hands structured results back to the runtime.

## Install into any repository

Requires Python 3.11+ and a current Codex release with project custom-agent/skill support.

```bash
git clone https://github.com/bruceclng-cloud/ai-workbench-workflow.git
cd ai-workbench-workflow
python3 install.py /path/to/your/project

# optional: expand the complete source package for inspection
python3 install.py --extract-source ./source
```

The installer merges the workflow block into an existing `AGENTS.md`, copies the Codex agents/skill/runtime definition, adds runtime paths to `.gitignore`, and runs `doctor`. It refuses to overwrite conflicting workflow files unless `--force` is supplied.

Then, from the adopting project:

```bash
python3 .agents/skills/workbench-workflow/scripts/workflow.py new
python3 .agents/skills/workbench-workflow/scripts/workflow.py dispatch
```

Or tell the parent Codex session to use `$workbench-workflow`.

## Core commands

```bash
# installation/runtime health
python3 .agents/skills/workbench-workflow/scripts/workflow.py doctor

# start/switch durable runs
python3 .agents/skills/workbench-workflow/scripts/workflow.py new --wing WING-UX-001
python3 .agents/skills/workbench-workflow/scripts/workflow.py list
python3 .agents/skills/workbench-workflow/scripts/workflow.py use <run-id>

# state + deterministic next dispatch
python3 .agents/skills/workbench-workflow/scripts/workflow.py show
python3 .agents/skills/workbench-workflow/scripts/workflow.py validate
python3 .agents/skills/workbench-workflow/scripts/workflow.py dispatch

# Control-Tower transition
python3 .agents/skills/workbench-workflow/scripts/workflow.py transition route_wing

# agent result ingestion
python3 .agents/skills/workbench-workflow/scripts/workflow.py record-result result.json
python3 .agents/skills/workbench-workflow/scripts/workflow.py record-review blind.json edge.json verify.json

# human-only gate (must be run interactively by the human)
python3 .agents/skills/workbench-workflow/scripts/workflow.py approve human_approve_ux
```

## Review diagnosis

Every verified finding is one of:

- `PATCH` — contract is correct; direct implementation correction.
- `BAD_SPEC` — intent exists, executable Feather contract was wrong/incomplete.
- `INTENT_GAP` — a visible decision genuinely needs the human.
- `CORRECT_COURSE` — upstream Wing/design/product assumption needs reconsideration.
- `DEFER` — real but not caused/owned by the active Feather.

The runtime uses precedence `CORRECT_COURSE > INTENT_GAP > BAD_SPEC > PATCH > DEFER/PASS`.

For the three upstream categories, implementation must be rolled back to the recorded baseline before the runtime routes upstream. This prevents a bad implementation from becoming accidental authority.

## Human authority

Human-only events are rejected by the normal transition command. The approval command requires an interactive terminal and an exact confirmation phrase.

This prevents ordinary autonomous Codex runs from silently clicking through product gates. It is **not a security sandbox** against an agent/process with full OS control; use OS/account permissions for security-sensitive boundaries.

Technical PASS never equals product acceptance.

## Runtime state

`.workbench-workflow/` is local runtime data and should remain gitignored.

Each run contains:

```text
.workbench-workflow/runs/<run-id>/
  state.json
  events.jsonl
```

`events.jsonl` is append-only and stores the post-event state. `state.json` is an atomically replaced snapshot. If an interruption lands between those writes, the next load repairs the snapshot from the event journal.

`workflow/status.json` is only a materialized active-run view and is gitignored.

## Influences

The design borrows proven ideas rather than vendoring another framework:

- BMAD: JIT step files, bounded Build units, frozen human intent, upstream review diagnosis, UX-before-build, Correct Course.
- GitHub Spec Kit: declarative workflow definition, validation, durable run/resume model, control-flow mindset, overlays.
- OpenSpec: keep human-facing process understandable and artifact-driven.
- CrewAI/LangGraph/agent runtimes: separate workflow definition from execution and workers; checkpoint/interrupt mental model.

No upstream implementation code is vendored here.

## Status

v0.2 is still intentionally small: it is a **Codex-native deterministic workflow runtime**, not a distributed agent platform. It does not provide queues, remote workers, distributed locking, cloud tracing, or model-provider abstraction yet. The file/agent/state boundaries are designed so those can be added later without changing North/Bird/Wing/Feather semantics.

## License

MIT. See [`LICENSE`](LICENSE) and [`NOTICE.md`](NOTICE.md).
