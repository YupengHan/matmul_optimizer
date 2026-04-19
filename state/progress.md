# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `da19f01bfb3793b3cca3cc67fd521b0fe4fcf2b7`
- plateau counter: `0`
- round loop: `round 10/20`
- rounds remaining: `11`
- notes: `Node C build succeeded for round 10/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260418_234153_bf16_gemm_v1_da19f01`
- run dir: `runs/20260418_234153_bf16_gemm_v1_da19f01`
- correctness: `PASS`
- median runtime: `46.771713 ms`
- TFLOP/s: `15.543998 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260418_234449`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Using docs/heuristics.md explicitly, the current 64x96 kernel is no longer a simple DRAM-bound case; it is a mixed class-1 tensor under-utilization, class-3 shared/LSU feed pressure, and class-5 synchronization problem. Tensor active is 28.78%, warps active is already 82.91%, barrier stall is 29.48%, MIO throttle is 34.18%, LSU issue is 83.94%, and DRAM is only 47.58%, so rounds 10-14 are intentionally biased toward more aggressive experiments that materially change instruction mix rather than another small steady-state cleanup tweak, because the project is still far from the long-horizon ~20 ms target.`
- dir_01: Split the fixed shape into a 64x128 main kernel plus a 64x96 tail kernel | bottleneck: Barrier and fragment-feed overhead in the steady-state K loop; the current CTA already improved residency, so the next step is to amortize `cp.async`, `__syncthreads()`, and `wmma::load_matrix_sync` across more MMA before the next handoff.
- dir_02: Turn the lockstep cp.async loop into a warp-specialized producer-consumer pipeline | bottleneck: CTA-wide serialization of staging and compute work, plus MIO saturation from making every warp execute copy/setup work on every 16-wide K step.
- dir_03: Remove the `c_shared` round-trip and emit a register-first BF16 epilogue | bottleneck: Epilogue-side MIO and LSU pressure from the `c_shared` store-reread-convert-write sequence, which adds non-tensor instructions after the main MMA loop.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `20.853825 ms`, `1.804611x` slower than CUTLASS
