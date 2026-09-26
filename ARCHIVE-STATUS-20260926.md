# Archive status — 2026-09-26

This is a snapshot of the research archive, not a live product status page. The production branches remain in their own repositories.

## Repositories

- Plugin activity implementation: `wislap/neko_rimworld`, commit `4990e9e`, opt-in only.
- Bench activity replay/harness: `wislap/rimworld-bench`, commit `ddda994`.
- Native Mod baseline: `wislap/NekoRimWorld`, commit `43bb92f`, unchanged for v2.4.

## Validation recorded for v2.4

- Plugin: 587 tests passed.
- Bench: 614 tests passed.
- Mod build: 0 errors; existing analyzer/nullable warnings remain.
- BridgeSmoke net8.0: passed.
- No paid model calls and no installed DLL deployment.

## What this does not establish

The archive records deterministic activity compilation, relation binding, replay preservation and existing native smoke coverage. It does not establish that an Agent selects sound high-level strategies, that a rescue or transfer Job succeeds, or that autonomous play is production-ready.

`research/decisions/CURRENT-STATE-20260918.md` is deliberately retained as a historical document with its original date and wording; it is not the current status page.
