# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 20/20` with `1` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_014602`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 20 diagnosis is intentionally framed for implementation on the accepted round-18 base commit ea27d5a906ceb46b0a4ec429d6d53f4a457620d6 at 38.47372818 ms, not on the regressed round-19 code. Round 19 is treated as negative evidence: the localized 64x384 B-fragment shared-layout rewrite regressed to 39.30060768 ms while MIO throttle rose from 31.42 to 36.14, LSU wavefront activity rose from 48.590499 to 68.567113, and tensor active fell from 32.130750 to 29.184802.`
- dir_01: Reduce hot-kernel epilogue and writeback work on the accepted 64x384 base | bottleneck: Non-tensor epilogue work and shared-scratch writeback are diluting Tensor Core issue inside the proven 64x384 hot kernel.
- dir_02: Pivot away from B-layout rewrites and peel the fixed 452-step steady state | bottleneck: Steady-state control, address-generation, and wait/sync bookkeeping on the accepted round-18 path are wasting issue bandwidth that should go to Tensor Core work.
- dir_03: Keep the 64x384 macro split, but cut per-warp fragment footprint | bottleneck: Register-limited occupancy and low ready-warp count are capping Tensor Core utilization on the accepted 64x384 base.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
