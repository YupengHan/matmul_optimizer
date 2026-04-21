# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `00b6a0a4ce0ebbeb1b31342c943a6930b2f8af6e`
- plateau counter: `3`
- round loop: `round 12/50`
- rounds remaining: `39`
- notes: `Node C build succeeded for round 12/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_191909_bf16_gemm_v1_00b6a0a`
- run dir: `runs/20260420_191909_bf16_gemm_v1_00b6a0a`
- correctness: `PASS`
- median runtime: `25.379312 ms`
- TFLOP/s: `28.646144 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_192106`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 12/50: `state/human_review.md` currently contributes only the approval/selection gate and no extra user-authored idea families, so the ranking is tied directly to measured evidence. Accepted for this round: the fixed-shape tile-routing family backed by `state/autotune_round18_main_tiles.md`, where `64x384` was the best measured hot-band width. Deferred: deeper PTX hot-band tuning until the active `128x128` branch is no longer stuck at `200` regs/thread and `16.64%` active warps. Rejected as the primary explanation: a DRAM-bound diagnosis for the main path, because the active hot-band kernel reaches only `13.05%` DRAM throughput while tensor cycles are `48.09%`. Tail-memory cleanup remains tertiary because the `64x96` branch covers only the last `96` columns.`
- dir_01: Restore Sweep-Backed 64x384 Full Hot Band | bottleneck: Main hot-band occupancy and tensor-core under-utilization caused by the default dispatch choosing the PTX `128x128` branch instead of the measured `64x384` full-band tile path.
- dir_02: Trim 128x128 PTX Hot-Band Register Pressure | bottleneck: Register-limited occupancy inside the PTX hot-band microkernel, amplified by heavy LSU/shared export work in the current accumulate/store path.
- dir_03: Specialize The 64x96 Tail Memory Path | bottleneck: Memory and LSU pressure in the fixed `64x96` tail region, not the primary hot-band compute path.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.495424 ms`, `0.942301x` slower than CUTLASS
