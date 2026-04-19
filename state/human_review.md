# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 3/5` with `3` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_094909`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 3/5 diagnosis prepared after the round-2 phased-64x384 experiment regressed to 42.673632 ms. Both recent human-guided families are treated as negative evidence on top of the restored accepted base 16a98f7 (37.285807 ms): round-1 two-level B staging regressed to 42.341888 ms and round-2 phased micro-panels regressed to 42.673632 ms. Ranking therefore pivots to other levers on the restored accepted base.`
- dir_01: Warp-specialize the 64x384 copy/compute pipeline on the restored base | bottleneck: CTA-wide synchronization and hot-loop feed orchestration in the 64x384 K-loop.
- dir_02: Peel a fixed-shape steady-state hot kernel for 6464x7776x7232 | bottleneck: Generic control-flow and stage-transition overhead diluting tensor issue in the fixed-shape hot loop.
- dir_03: Trim the c_shared epilogue/export path on the restored base | bottleneck: LSU/shared writeback pressure in the hot epilogue rather than another B-feed or live-set bottleneck family.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
