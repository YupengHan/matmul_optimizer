# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 14/20` with `7` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_003032`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `dir_01`
- diagnosis notes: `Human-in-loop round: skip automatic node_b direction selection and prioritize the user-requested vectorization + thread-coarsening path for high MIO throttle.`
- dir_01: Human idea: vectorize transfers and thread-coarsen the load/store path | bottleneck: MIO throttle and LSU pressure from too many narrow load/store instructions in the hot path and epilogue.
- dir_02: Replace WMMA fragment loads with an explicit tensor feed pipeline | bottleneck: Tensor-core underfeed from the fragment delivery path, expressed as high MIO throttle and oversized LSU wavefront pressure before each MMA issue window.
- dir_03: Retile the CTA and cut per-warp output ownership | bottleneck: Per-warp fragment/accumulator footprint and issue inefficiency from the current 4x2 warp layout plus wide N-side ownership.

## Active direction

- selected direction: `dir_01`
- selection mode: `human_idea`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
