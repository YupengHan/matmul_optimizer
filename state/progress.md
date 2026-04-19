# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `8138da55448e546af314940addc89fd3cadc56ff`
- plateau counter: `0`
- round loop: `round 4/5`
- rounds remaining: `2`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 4/5.`

## Latest measured custom run

- run id: `20260418_212627_bf16_gemm_v1_8138da5`
- run dir: `runs/20260418_212627_bf16_gemm_v1_8138da5`
- correctness: `PASS`
- median runtime: `97.885185 ms`
- TFLOP/s: `7.427267 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260418_212651`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Increase per-warp output tile reuse | bottleneck: Tensor Core under-utilization driven by too little MMA work per staged tile, currently surfacing as low `sm__pipe_tensor_cycles_active` with persistent `smsp__warp_issue_stalled_mio_throttle`.
- dir_02: Pad or swizzle shared A/B tiles for WMMA loads | bottleneck: Shared-memory / MIO pressure around `wmma::load_matrix_sync`, likely caused by conflict-prone staging layout rather than global-memory bandwidth saturation.
- dir_03: Specialize a 2x K macro-stage pipeline | bottleneck: Synchronization overhead from the current one-barrier-per-`kWmmaK` steady-state loop.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `71.967297 ms`, `3.776742x` slower than CUTLASS
