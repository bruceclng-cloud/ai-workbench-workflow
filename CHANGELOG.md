# Changelog

## Unreleased

- Restored the canonical hierarchy to **North → Bird → Wing → Feather**. Feather is the terminal executable unit; implementation detail inside a Feather is not a separate workflow level or artifact type.
- Added `WORKFLOW.md` as the current human-readable workflow authority and explicit Wing-stop rule.
- Marked historical `Task`/`Tasks` wording in the retained v0.2.0 package as superseded rather than rewriting the released artifact.
- Changed current repository development from MIT to PolyForm Strict License 1.0.0 for stronger control over redistribution and derivative works.
- Added explicit legacy-license notice preserving historical MIT grants for already-published releases.
- Added patent/disclosure guidance without making any false `patent pending` claim.
- Added unregistered project-mark policy, commercial licensing policy, and protected contribution policy.
- Strengthened copyright and IP notices.

## 0.2.0

- Added declarative workflow definition and overlay layer.
- Added per-run runtime state, active-run switching, append-only events, atomic snapshot writes, and process locking.
- Added deterministic dispatch and structured result ingestion.
- Added reviewer result validation and deterministic review precedence.
- Added rollback-before-upstream-routing for BAD_SPEC / INTENT_GAP / CORRECT_COURSE.
- Fixed blocked-review resume semantics by restoring the exact pre-block snapshot.
- Fixed review-loop boundary: five remediation loops allowed by default, sixth blocks.
- Added frozen approved-intent hashes for Wing/Feather contracts.
- Added interactive human-only approval path and explicit push authorization event.
- Added immediate installer, doctor checks, schemas, overlays, and multi-run commands.
- Strengthened UX, specification, review, baseline/commit, and Wing-close procedures using lessons from major spec-driven and agent workflow systems.

## 0.1.0

- Initial Codex-native workflow package with North → Bird → Wing → Feather hierarchy, custom agents, JIT steps, state validator, review taxonomy, UX gates and Correct Course.
