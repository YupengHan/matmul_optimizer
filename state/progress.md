# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `74f163a73e572099933f7558d0e3413019613a7b`
- plateau counter: `5`
- round loop: `round 4/20`
- rounds remaining: `17`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 4/20.`

## Latest measured custom run

- run id: `20260419_171842_bf16_gemm_v1_74f163a`
- run dir: `runs/20260419_171842_bf16_gemm_v1_74f163a`
- correctness: `PASS`
- median runtime: `33.592319 ms`
- TFLOP/s: `21.642430 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_171921`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `All three directions stay inside the 64x384 hot-band PTX mainline and keep the 64x96 tail unchanged. Ranking is anchored on the restored accepted base 20260419_142213_bf16_gemm_v1_9bdc160 and the latest diagnosed run 20260419_171842_bf16_gemm_v1_74f163a. The explicit lesson from round 3 is that asymmetric two-stage handoff retime is not the right family to keep pushing: it recovered most of the round-2 loss by driving mio down, but it still trailed the accepted base because barrier and long-scoreboard rose. Negative evidence carried forward remains strict: no explicit half-panel mma.sync compute rewrite, no pair-compaction retry, no panelized B-load reorder, no helper/lifetime compaction retry as the main lever, and no near-neighbor handoff-retime retry. The recommended direction therefore shifts to removing real hot-path work and shared-footprint from the export side, which is both materially different and more likely to unlock the next layer of overlap.`
- dir_01: Register-first PTX pair export that shrinks hot-band c_shared scratch | bottleneck: Export-side shared traffic and scratch allocation are still taxing the hot-band kernel; they show up indirectly through LSU pressure, scoreboard exposure, and lack of real overlap headroom rather than through mio alone.
- dir_02: True third A/B stage on the hot band, funded by export-budget recovery | bottleneck: The hot-band kernel is still limited by insufficient overlap depth under one-block occupancy, not just by the precise ordering of the current two-stage handoff.
- dir_03: Full-width PTX B-fragment lookahead inside the 12-tile sweep | bottleneck: Residual long-scoreboard latency may now be dominated by the warp-local B-fragment load/use sequence inside each K-slice rather than by global stage timing.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `6.083199 ms`, `1.234710x` slower than CUTLASS
