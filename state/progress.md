# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `9f8afe4d5bc56643bbd110d2285046ea298e310b`
- plateau counter: `19`
- round loop: `round 78/100`
- rounds remaining: `23`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 78/100.`

## Latest measured custom run

- run id: `20260420_114003_bf16_gemm_v1_9f8afe4`
- run dir: `runs/20260420_114003_bf16_gemm_v1_9f8afe4`
- correctness: `PASS`
- median runtime: `25.973760 ms`
- TFLOP/s: `27.990535 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_114200`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Latest measured run 20260420_114003_bf16_gemm_v1_9f8afe4 is back in the restored PTX baseline shape, but the environment is slower than the earlier round-74 measurement: 25.97375965 ms versus about 24.696 ms. The profile shape is still the same class of problem, with tensor active 47.88, barrier 6.53, long scoreboard 3.71, mio 3.31, and launch__occupancy_limit_registers 2. The source file is identical to the earlier round-74 f1ae7fa surface, so this should be treated as the current baseline environment rather than a launch-path discrepancy. The non-PTX default promotion family is already closed-negative, so the next search should stay on genuinely different PTX-adjacent families from this restored baseline.`
- dir_01: Try The 128x128x32 Staged Hot-Band Family | bottleneck: Barrier cost, short-scoreboard pressure, and register/occupancy pressure in the current 128x128 PTX hot-band cadence.
- dir_02: Activate The Existing 128x128 Two-Stage Hot-Band Kernel | bottleneck: Occupancy and synchronization overhead in a smaller 128x128 kernel, rather than DRAM bandwidth.
- dir_03: Trim PTX Export And Scratch Shape On The Restored Baseline | bottleneck: Residual export-side instruction overhead and scratch/register clutter around the writeback path.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
