# AI Workbench Workflow — Canonical Authority

## Hierarchy

**North → Bird → Wing → Feather**

There is no planning or execution layer below Feather.

- **North** — full product direction and durable product principles.
- **Bird** — a major product domain.
- **Wing** — one coherent integrated product outcome inside a Bird.
- **Feather** — one bounded executable capability required by a Wing.

A Feather is the terminal executable unit. It contains the complete execution contract and is acted on directly by the Builder. Small implementation details may appear inside the Feather as ordinary steps, code notes, or checklists. They do not become another workflow object, identifier, lifecycle, review gate, or document type.

## Planning authority

Parents reference children without embedding their specifications:

- North lists Birds.
- Bird lists Wings.
- Wing lists Feathers.
- Feather contains its complete bounded execution contract.

Navigator decomposes authority downward. Planning decomposition is independently reviewed before implementation.

## Wing execution

The default executable product boundary is one explicitly activated Wing.

For each dependency-ready Feather:

**implement → targeted verification → commit → independent adversarial review → blocker-only remediation when required → smallest affected recheck → delta re-review → verified**

After a Feather is verified, the Builder may continue automatically only to another dependency-ready Feather inside the same active Wing.

When all required Feathers are verified:

**Wing Integration Review → Wing verified if PASS → STOP**

The system must never infer permission to activate another Wing. Entry into another Wing requires explicit human authorization or an explicit batch authorization that names the Wings and scope in advance.

## Review ownership

Feathers prove local correctness with the cheapest sufficient deterministic evidence.

Wing Integration Review proves the assembled outcome, including completeness, cross-Feather behaviour, relevant cross-Wing compatibility, direction coverage, and integrated product quality. Expensive browser/native/visual evidence belongs at Wing level unless a Feather cannot otherwise be technically verified.

Technical verification never means human acceptance. Only the human product owner can grant acceptance.

## Control Tower

The parent Codex session is Control Tower. It must recover exact state from durable repository/runtime records, not infer state from conversation history. It must stop product implementation when workflow authority, current state, or review status is ambiguous.

A verified stop boundary is a real gate. The absence of a runtime enforcement mechanism does not convert prose permission into authority.

## Continuity

Every active project using this workflow must maintain a concise handover/Compass that records:

- current branch and head;
- active Bird/Wing/Feather, if any;
- exact lifecycle and review state;
- last independently verified boundary;
- blockers and unresolved human decisions;
- next legally executable workflow transition.

If the installed runtime or project instructions disagree with this file on hierarchy or Wing-stop semantics, this file is the current workflow authority until a later explicitly reviewed version supersedes it.
