# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 56/100` with `45` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_084003`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 56/100 diagnosis anchored to run 20260420_083902_bf16_gemm_v1_de7e8be at 24.849423 ms. Rejected this round: reopening warmup-order branch, K32 cadence, extra-live B lookahead, unroll-1 base, CTA-level B repack, or wider shared-memory rewrites.`
- dir_01: Steady-state barrier / handoff retime | bottleneck: Barrier latency at the active hot-band handoff, not stage count, macro tiling, grouped-row count, or warmup-order mechanics.
- dir_02: PTX hot-band consumer-order refinement | bottleneck: Consumer-side ordering detail in the PTX hot-band path, especially row-pair traversal or lane-local reuse, with the current run still showing barrier as the primary exposed issue.
- dir_03: Hot-band L2 / grouped-row launch-order locality | bottleneck: L2 cache locality and grouped-row launch order rather than the steady-state barrier limiter.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
