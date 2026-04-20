# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `d777e9e7089a038cf09cb966e7ee5ea458717dd4`
- plateau counter: `8`
- round loop: `round 3/10`
- rounds remaining: `8`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 3/10.`

## Latest measured custom run

- run id: `20260419_204427_bf16_gemm_v1_d777e9e`
- run dir: `runs/20260419_204427_bf16_gemm_v1_d777e9e`
- correctness: `FAIL`
- median runtime: `30.644224 ms`
- TFLOP/s: `23.724517 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_205559`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 3 human-idea audit against the latest measured evidence: `Tiling` stays accepted as the outer family because the 256x128 hot-band branch is the only path that materially broke the register wall; `Coalescing Access`, `Data Reuse`, and `Async Copy` remain accepted as baseline infrastructure because the kernel is already on 16-byte cp.async staging and the profile is still not DRAM-limited; `Bank Conflict` is deferred to the fallback family only, because the current blocker is correctness, not shared-feed throughput on a correct branch; `L2 Cache` stays deferred because neither the latest run nor the accepted base is L2-bound; `Register Reuse` remains the primary accepted family because the half-panel branch is still the only path that reached 93 regs/thread and 2-block occupancy; `Pg2s`, `Ps2r`, and `Stage` are accepted as the next family after correctness because replaying the A producer path across two full half-panel passes is now the clearest remaining tax once the branch is stable. The key new diagnosis signal is local rerun instability: after round 2, rerunning the same correctness case changed the max-error index and value while mean_abs_err stayed near 0.033. That points to a sparse nondeterministic ownership or overlapping-writer bug, not just one fixed deterministic column formula. Recommended direction `dir_01` therefore keeps the high-ceiling half-panel family alive for one more round, but narrows the task to end-to-end ownership stabilization. If that still fails, the next round should pivot to the correct 64x384 fallback.`
- dir_01: Human idea 7 sparse-error repair: keep the half-panel branch, but fix the remaining nondeterministic ownership/overlap bug end to end | bottleneck: Correctness-blocking nondeterministic ownership/coverage bug in the half-panel control/export path, not DRAM bandwidth or the macro tile choice. Success means the same correctness case stops drifting across reruns while preserving the 93-reg / 2-block occupancy signal.
- dir_02: Human idea 8/9 Pg2s + Ps2r: once correctness is stable, fuse the two 32-column passes into one K-loop so each staged A tile is consumed twice | bottleneck: Replay of the A-side producer path and repeated barrier tax across two serial half-panel sweeps. Successful fusion should cut barrier pressure and compute-memory throughput without giving back the current 93-reg occupancy win.
- dir_03: Human idea 5 Bank conflict fallback: restore the accepted 64x384 base and spend the next round on a warp-local B-consumer transform | bottleneck: Shared/L1/B-operand delivery behavior on the accepted 64x384 path rather than occupancy. This is lower ceiling than the half-panel branch, but also much lower correctness risk.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `4.134879 ms`, `1.159538x` slower than CUTLASS
