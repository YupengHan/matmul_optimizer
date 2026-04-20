# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `469a12bfb9bb7579ea3238342f598a34e84a5e1a`
- plateau counter: `22`
- round loop: `round 81/100`
- rounds remaining: `20`
- notes: `Node C build succeeded for round 81/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_115626_bf16_gemm_v1_469a12b`
- run dir: `runs/20260420_115626_bf16_gemm_v1_469a12b`
- correctness: `PASS`
- median runtime: `25.643007 ms`
- TFLOP/s: `28.351566 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_115714`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 81/100 diagnosis for run 20260420_115626_bf16_gemm_v1_469a12b. The zero-padding PTX export trim improved runtime to 25.64300728 ms, with tensor activity back at 48.00 and barrier down at 5.50, so the restored PTX baseline is now the current reference. The new concern is long-scoreboard pressure at 7.61, not DRAM or barrier inflation; the broad default-promotion family and the K32 staged family remain closed-negative, so the next work should stay in the PTX-adjacent export/feed/orchestration space rather than reopening those paths.`
- dir_01: Trim The Remaining PTX Export Scoreboard | bottleneck: PTX export-lifetime latency, shared scratch residency, and address-generation overhead in the hot-band store path.
- dir_02: One More Bounded 128x128 Two-Stage Feed Iteration | bottleneck: Copy-feed latency and stage handoff inside the 128x128 two-stage kernel, with long-scoreboard pressure rather than raw tensor under-utilization.
- dir_03: Tighten PTX Hot-Band Grouping And Peel Handoff | bottleneck: Hot-band orchestration and peel coordination, especially around grouped-row mapping and the fixed tail handoff.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
