# v2.4 activity evaluation evidence index

Archive date: 2026-09-26.

## Source revisions

| Repository | Revision | Role |
|---|---|---|
| `N.E.K.O/plugin/plugins/neko_rimworld` | `4990e9e` | opt-in activity evaluator and Agent surfaces |
| `rimworld-bench` | `ddda994` | activity replay/harness wiring on the archived branch base |
| `RimWorldMod/NekoRimWorld` | `43bb92f` | unchanged native Mod baseline |

## Deterministic validation

- Plugin full test suite: 587 passed.
- Bench full test suite: 614 passed.
- Mod source build: succeeded, 0 errors; existing nullable/GraphQL analyzer warnings remain.
- BridgeSmoke net8.0: all existing spatial, world-observation, query, resource and evidence checks passed.
- Activity surface smoke: conservative and hybrid retain the existing semantic tools; simplified exposes `evaluate_activity` and `submit_response`.
- No paid model request was made for this feature.
- No Mod wire operation or installed game DLL was changed.

## Runtime artifact locations

Large evidence is intentionally external to Git. The relevant workspace roots are:

- `/mnt/k_disk/python_programe/N.E.K.O_rimworld/.bench-results/`
- `/mnt/k_disk/python_programe/N.E.K.O_rimworld/.bench-data/`
- `/home/yun_wan/.codex/experiments/rimworld-v110-deepseek-repair2-20260919/`
- `/mnt/k_disk/python_programe/N.E.K.O_rimworld/.bench-results/causal-validation-20260925/`
- `/mnt/k_disk/python_programe/N.E.K.O_rimworld/.bench-results/review-replay-20260926/`
- `/mnt/k_disk/python_programe/N.E.K.O_rimworld/.bench-results/v24-activity-full-live-final/` (if present in the local capture workspace)

Raw streams, game saves, credentials and generated caches must remain outside the Git archive. When moving machines, copy the corresponding directory and preserve its manifest/hash files.

## Interpretation boundary

This archive proves deterministic activity compilation, stage binding, replay preservation and existing native smoke coverage. It does not prove that an Agent selects correct high-level strategies or that a transfer/rescue Job succeeds in game.
