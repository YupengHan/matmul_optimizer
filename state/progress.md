# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `de7e8be6e77487fbeecd095db66faa31c991de1e`
- plateau counter: `0`
- round loop: `round 56/100`
- rounds remaining: `45`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 56/100.`

## Latest measured custom run

- run id: `20260420_083902_bf16_gemm_v1_de7e8be`
- run dir: `runs/20260420_083902_bf16_gemm_v1_de7e8be`
- correctness: `PASS`
- median runtime: `24.849423 ms`
- TFLOP/s: `29.256994 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_084003`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 56/100 diagnosis anchored to run 20260420_083902_bf16_gemm_v1_de7e8be at 24.849423 ms. Rejected this round: reopening warmup-order branch, K32 cadence, extra-live B lookahead, unroll-1 base, CTA-level B repack, or wider shared-memory rewrites.`
- dir_01: Steady-state barrier / handoff retime | bottleneck: Barrier latency at the active hot-band handoff, not stage count, macro tiling, grouped-row count, or warmup-order mechanics.
- dir_02: PTX hot-band consumer-order refinement | bottleneck: Consumer-side ordering detail in the PTX hot-band path, especially row-pair traversal or lane-local reuse, with the current run still showing barrier as the primary exposed issue.
- dir_03: Hot-band L2 / grouped-row launch-order locality | bottleneck: L2 cache locality and grouped-row launch order rather than the steady-state barrier limiter.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.068465 ms`, `0.958775x` slower than CUTLASS
