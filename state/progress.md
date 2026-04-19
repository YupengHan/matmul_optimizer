# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `eecbb72cf2ce923b80d7eab679b5355a3873fc88`
- plateau counter: `0`
- round loop: `round 2/20`
- rounds remaining: `19`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 2/20.`

## Latest measured custom run

- run id: `20260418_221951_bf16_gemm_v1_eecbb72`
- run dir: `runs/20260418_221951_bf16_gemm_v1_eecbb72`
- correctness: `PASS`
- median runtime: `82.266624 ms`
- TFLOP/s: `8.837356 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260418_222017`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Retune the tensor tile so each warp does more MMA work per shared-memory feed | bottleneck: Shared-memory / fragment-load issue pressure with too little MMA work per warp and too few ready warps to hide it.
- dir_02: Rewrite the A/B shared-memory layout for lower-friction WMMA fragment loads | bottleneck: Shared-memory layout inefficiency on the WMMA load path, especially the B-fragment feed, causing excessive MIO throttling before Tensor Cores can be kept busy.
- dir_03: Retune the async pipeline handoff to reduce per-K synchronization bubbles | bottleneck: Stage-transition overhead from the double-buffered `cp.async` pipeline, where full-CTA waits and barriers are now a secondary limiter after global-load widening.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `56.348736 ms`, `3.174125x` slower than CUTLASS
