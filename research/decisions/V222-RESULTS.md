# V2.2.2 — bounded display ordering, quality improvement not accepted

2026-09-24. Completed the three predeclared candidate stages and final paired
regression. Retain only the low-impact order-only display change; S1 routing
and S3 completion text are reverted. This is not an overall accuracy release
and does not resolve the complex rescue bad case.

## What ships

`agent/world_order.py` creates a detached view for the three V2.2 world tools.
Pawn state exposes injuries/capacities before the native overall-health summary;
object facets prioritize Pawn/state/stats/work/contextual state over generic
condition metadata. No field, value, path, row, array order, scope, unknown,
coverage flag, parameter or tool is removed/added. Raw observations remain in
native order. Legacy look/count and production prompt/tool descriptions are
unchanged. No hidden routing, critic call, new semantic guard, action or native
Mod change is introduced. The formatter does not shorten JSON or native reads.

Code invariants and local injury-recognition evidence support retaining this as
a display adjustment. Model-quality acceptance remains open: the independent
holdout has a candidate coverage error and does not demonstrate an overall win.
The test results below are retained, not reclassified to justify release.

## Separate experiments

| Stage | Baseline core | Candidate core | Model requests | Outcome |
| --- | ---: | ---: | --- | --- |
| S1 tool routing, 4 tasks twice | 5/8 | 6/8 | 40 → 40 | Reverted |
| S2 fixed evidence, 4 cases twice | 6/8 | 7/8 | 8 → 8 one-turn calls | Native validation, then display-only retention |
| S3 decision-changing gaps, 4 tasks twice | 3/8 | 6/8 | 38 → 40 | Reverted |
| Final paired holdout, 4 tasks once | 4/4 | 3/4 | 16 → 14 | No overall quality acceptance |

Core correctness is separate from extra prose errors and protocol delivery.
Do not pool the differing stages into a global success rate or claim significance.
S1/S3 use the same paused native host and counterbalanced/interleaved dispatch;
S1 differs only in the appended guide. S3 uses the order-only view in both arms
and differs only by one research-only completion instruction. S2 keeps system,
tools and evidence values equal and changes dictionary order only. The holdout
compares plugin42a6697 with the order-only final candidate, using questions held
out from S1/S3, not unseen throughout the entire project's history.

### S1

Native business reads71→53, but candidate rescue-0 had five overlength submission
repairs and degraded delivery (baseline8/8 normal, candidate7/8). Production and
one pickup case show actual routing benefits; both rescue repeats still missed
actual candidate stats, bed recipient/carrier predicates and the carry leg.
Simple counts still over-read. Reported tokens1,094,445 vs at least1,135,960;
candidate rescue-0 usage is incomplete. No demonstrated cost improvement.

### S2

Only stats/nearby cases contain Pawn facets and test injury ordering (4 slots
per arm). Overview changes other facets but returns no Pawn rows; it is not
injury-salience evidence. Bed control is an identical unavailable-target receipt,
not a successful bed-state test; all four input hashes match. Its variation is
sampling noise. Original preflight copies remain under s2-preflight and had no
paid attempts; actual runner/formatter hashes were checked before running s2.

Stats core2/2 in both arms. Nearby core0/2→1/2, and the candidate retains Near's
injuries in both repeats whereas baseline health-summary wording obscures them.
One candidate still overstates medical necessity to move; extra factual errors
remain. Sixteen one-turn outputs did not run production submit/repair validation;
one baseline short answer exceeds180 tokens. These are interpretation results,
not proof of valid deliveries or autonomous tool selection. Tokens144,581 vs
145,385, all reported. Same JSON length is intentional, not an optimization miss.

### S3

Some pickup and production conclusions preserve uncertainty better, contributing
to higher core score. They do not demonstrate the intended missing-evidence
repair: both rescue runs still lack candidate stats, bed context and carry-leg
checks. Candidate count over-reads, length rejections6→11, native reads62→61;
rescue-1 takes11 model requests vs5. All eight deliver in each arm, but candidate
rescue-1 usage is incomplete. Reported tokens1,024,795 vs at least1,524,751. Revert
the extra instruction; this does not mean it had no positive answers or prove
it caused every regression.

### Final regression

Both sides correctly answer explicit bed and actual-stat tasks. Candidate three
world returns actually reorder; seven returned world observations checked
against raw native data preserve all values and arrays. Skill uses only legacy
look on both sides (no ordering exposure). Area has no Pawn rows: candidate
incorrectly applies objects17/62 pagination to fully returned roof supports53/53
and omits the real object-list limitation. Baseline also has an additional
unsupported all-walls durability claim. Core4/4→3/4; all normal deliveries.

Requests16→14 but business reads13→19, tokens322,883→245,691. These single samples
and differing query choices do not establish efficiency improvement. The area
error is retained; absence of data loss is not proof that ordering cannot affect
model behavior. No claim that the rescue problem is fixed.

## Verification, accounting and limits

- 67 actual native receipts: equal facts/paths/arrays, unchanged raw JSON,
  idempotent transformation and equal JSON length;58 serializations reordered.
- Plugin473 passed; bench497 passed. Integration test covers all three world-tool
  handlers, partial/unavailable facts and mutation isolation. Bench mirror is
  byte-checked against the production formatter; production is authoritative.
- Standards: initial S2 execution-hash check gap fixed before paid calls; final
  no blocking findings. Spec: production contains only S2; S1/S3 do not remain.
- Native Mod unchanged at dff95bc; capture build succeeded. No normal-game DLL
  overwritten. Own paused host stopped normally; private credential config
  removed after exact-secret artifact scan.
- 40 native episodes +16 fixed-evidence calls;204 model requests/attempts.
  Reported token lower bound5,638,491;two episodes lack complete provider usage.
  Never interpret missing usage as zero or report an exact total cost.
- No failed slot rerun to pass; no additional candidate wording trial. API
  credentials and evaluator labels were not sent as model task context.

Full artifacts: `.bench-results/v222/` (sealed source/inputs/native receipts,
outputs, independent reviews, decisions, metrics). Lightweight copies and rejected
patches: `experiments/v222/`. Existing untracked Wiki scripts were untouched.

Production plugin commit: `3a99913`; native Mod remains `dff95bc`. Experimental source/results are committed separately in this bench repository.
