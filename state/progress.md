# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `af155a5bdaa475a7edba5ed1957b25a46454536e`
- plateau counter: `0`
- round loop: `round 1/5`
- rounds remaining: `5`
- notes: `Node C build succeeded for round 1/5. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260418_201228_bf16_gemm_v1_af155a5`
- run dir: `runs/20260418_201228_bf16_gemm_v1_af155a5`
- correctness: `PASS`
- median runtime: `145.344559 ms`
- TFLOP/s: `5.002041 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260418_210351`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Async double-buffered K pipeline | bottleneck: Global-memory latency plus CTA-wide synchronization between K-slices, visible as long scoreboard stalls and barrier stalls in the steady-state loop.
- dir_02: Swizzle shared-memory staging for WMMA loads | bottleneck: Shared-memory communication pressure around fragment loads, showing up as MIO throttle and lingering scoreboard stalls even though DRAM is not saturated.
- dir_03: Retile CTA and warp partitioning | bottleneck: Synchronization overhead and low tensor-issue density from the current CTA/warp shape, not raw DRAM bandwidth.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `119.426670 ms`, `5.607886x` slower than CUTLASS
