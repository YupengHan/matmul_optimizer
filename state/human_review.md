# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 4/5` with `2` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260418_212651`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Increase per-warp output tile reuse | bottleneck: Tensor Core under-utilization driven by too little MMA work per staged tile, currently surfacing as low `sm__pipe_tensor_cycles_active` with persistent `smsp__warp_issue_stalled_mio_throttle`.
- dir_02: Pad or swizzle shared A/B tiles for WMMA loads | bottleneck: Shared-memory / MIO pressure around `wmma::load_matrix_sync`, likely caused by conflict-prone staging layout rather than global-memory bandwidth saturation.
- dir_03: Specialize a 2x K macro-stage pipeline | bottleneck: Synchronization overhead from the current one-barrier-per-`kWmmaK` steady-state loop.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
