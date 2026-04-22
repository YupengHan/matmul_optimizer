# Progress

## Objective

Beat cuBLAS and drive the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1` to `<= 18.000 ms`.
- target runtime: `<= 18.000 ms`
- comparison target: `cuBLAS`
- rebootstrap source: `20260420_235922_bf16_gemm_v1_489574e`, commit `489574ed5013268dbb79c634450d9a60155a294a`, historical runtime `24.164272 ms`

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `9652b83550cd0d483328509f8a3f908c72a1e03a`
- plateau counter: `28`
- round loop: `round 12/20`
- rounds remaining: `9`
- notes: `Node C build succeeded for round 12/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_191613_bf16_gemm_v1_9652b835`
- run dir: `runs/20260421_191613_bf16_gemm_v1_9652b835`
- correctness: `PASS`
- median runtime: `30.174224 ms`
- TFLOP/s: `24.094055 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_191808`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 12/20 diagnosis emitted from the measured 256x128 loss; frontier should restore the compact 128x128 PTX anchor before spending another round on a new structural probe.`
- dir_01: Restore The Compact 128x128 PTX Grouped-Rows-4 Anchor After The Failed 256x128 Reopen | bottleneck: The immediate problem is the bad 256x128 hot-band geometry itself, which inflated shared-memory footprint and collapsed tensor throughput.
- dir_02: Reopen Pairwise Wait-Sync Collapse Once The Compact PTX Anchor Is Restored | bottleneck: On the restored compact PTX surface, the remaining bottleneck is still hot-loop wait/sync cadence and latency hiding rather than tile geometry.
- dir_03: Retry The 2-K-Stage Pg2s Port Only After The Compact Anchor Is Back | bottleneck: If revisited later, the target bottleneck is compact-surface latency hiding and per-tile copy cadence, not wide-tile geometry.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `frontier`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` of CUTLASS runtime (faster)
- cuBLAS median runtime: `22.000000 ms`
- current best custom gap vs cuBLAS: `2.164272 ms`, `1.098376x` of cuBLAS runtime (slower)
