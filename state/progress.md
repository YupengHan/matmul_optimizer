# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `1b918573ad23909f16117d559ff52de3af7f1f05`
- plateau counter: `21`
- round loop: `round 80/100`
- rounds remaining: `21`
- notes: `Node C build succeeded for round 80/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_114650_bf16_gemm_v1_1b91857`
- run dir: `runs/20260420_114650_bf16_gemm_v1_1b91857`
- correctness: `PASS`
- median runtime: `27.076655 ms`
- TFLOP/s: `26.850415 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_114802`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 80/100 diagnosis for run 20260420_114650_bf16_gemm_v1_1b91857. The broad default-dispatch promotion family remains closed-negative, and the K32 staged family is also closed-negative after the round-79 regression. The existing 128x128 two-stage sibling improved strongly from 31.55292797 ms to 27.07665539 ms, with tensor activity back near baseline at 48.18 and long scoreboard down at 1.51, but it still trails the restored PTX baseline in the current environment while dram (31.39) and LTS (27.25) remain elevated. Treat the remaining gap as export/orchestration work, not another baseline-restore loop.`
- dir_01: Trim PTX Export Scratch On The Restored Baseline | bottleneck: PTX epilogue export bandwidth, shared scratch lifetime, and L2 traffic in the hot-band store path.
- dir_02: One More Bounded 128x128 Two-Stage Sibling Iteration | bottleneck: Synchronization and feed latency inside the 128x128 two-stage kernel, not tensor throughput.
- dir_03: Tighten PTX Hot-Band Grouping And Peel Orchestration | bottleneck: Hot-band orchestration overhead and peel coordination, especially around grouped-row partitioning.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
