# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 1/20` with `20` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_215833`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 1/20 human-review audit: `state/human_review.md` still contributes only the approval gate and the exactly-one-direction rule, with no extra user-authored family to prioritize. The just-measured round spent its budget on an in-family retune of the active one-K 128x128 copy cadence, and node_a measured that branch slightly slower at 25.381776 ms than the 25.325055 ms accepted base. That is enough evidence to step away from the same immediate family for the next round. Accepted as the primary family for this diagnosis is the PTX one-K 128x128 control branch, because it preserves the current hot-band geometry and split while testing a different control/export path that already produced a nearby 25.379312 ms run. Deferred fallback families are the existing 256x128 pivot hot-band kernel and a light grouped-CTA traversal retune on the current 128x128 grid. Rejected for this round are reopening the two-K 128x128x32 stage-deepening path and the stale full-band 64x384 sweep-backed route.`
- dir_01: Reopen The PTX One-K 128x128 Hot-Band Control Branch | bottleneck: Hot-band inner-loop control and export overhead in the standard one-K 128x128 path, rather than the peeled 64x384 residual rows or the 64x96 tail.
- dir_02: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: CTA geometry and block-count overhead on the hot-band region, rather than a pure one-K copy-cadence problem.
- dir_03: Retune Hot-Band CTA Traversal On The 128x128 Grid | bottleneck: Inter-CTA locality and block traversal efficiency on the hot-band grid under register-limited low occupancy.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
