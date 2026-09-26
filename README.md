# RimWorld Bench Archive

This public repository preserves high-value research records and design decisions from the N.E.K.O RimWorld Agent work. Start with [INDEX.md](INDEX.md).

It is an archive, not the production plugin, Mod, or active benchmark source tree. It contains selected plans, result reports, correction records, replay/evidence indexes, and research-only scripts. Large raw traces, game saves, model streams, credentials, generated caches, and `.bench-results` are not copied here; their local retention roots and interpretation boundaries are recorded in the evidence indexes.

The 2026-09-26 archive covers v1.10 corrections, v2.2/v2.3 observation work, rescue failure audits, review replay records, and the v2.4 generic activity-evaluation design.

A passing deterministic test proves the recorded software contract, replay binding or native smoke path. It does not prove that an Agent chooses a correct strategy, that a RimWorld Job succeeds, or that complex rescue has reached production reliability.

Source revisions:

- Plugin: `wislap/neko_rimworld`, activity implementation `4990e9e`.
- Bench: `wislap/rimworld-bench`, activity replay/harness baseline `ddda994`.
- Mod: `wislap/NekoRimWorld`, unchanged native baseline `43bb92f`.
