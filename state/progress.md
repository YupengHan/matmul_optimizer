# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `9bdc160ee2a6ef0f1171c09f4cf72f7dd081cab1`
- plateau counter: `2`
- round loop: `round 1/20`
- rounds remaining: `20`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 1/20.`

## Latest measured custom run

- run id: `20260419_142213_bf16_gemm_v1_9bdc160`
- run dir: `runs/20260419_142213_bf16_gemm_v1_9bdc160`
- correctness: `PASS`
- median runtime: `33.128447 ms`
- TFLOP/s: `21.945473 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_142321`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `All three directions remain strictly inside the current 64x384 hot-band PTX microkernel mainline and keep the 64x96 tail untouched. Ranking is anchored on the fresh restored baseline run 20260419_142213_bf16_gemm_v1_9bdc160 of the accepted c9d030a code: barrier and mio are already low, while occupancy is still one block/SM and long-scoreboard is the more obvious residual stall. Known negative evidence is carried forward: explicit mma.sync half-panel compute regressed, and pair-compaction plus panelized B-load reorder prechecks did not beat the base. Because this is the start of a 20-round run, the recommendation favors a medium-risk, sustainable full-width PTX dataflow improvement rather than a larger rewrite.`
- dir_01: Full-width PTX fragment-issue scheduling with tighter live ranges | bottleneck: Residual long-scoreboard latency and register-limited live state inside the current full-width PTX helper surface are now more limiting than synchronization overhead.
- dir_02: PTX state and helper lifetime compaction without pair-compaction | bottleneck: Helper-induced live-range inflation around the named 12-tile PTX accumulator surface is still contributing to occupancy_limit_registers=1 even after the productive orchestration/export work.
- dir_03: More direct register-packed pair export beyond shared float scratch | bottleneck: Export-side shared traffic and short-scoreboard pressure remain a secondary but still meaningful residual after paired export batching.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `6.083199 ms`, `1.234710x` slower than CUTLASS
