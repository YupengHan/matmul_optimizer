# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `52a3af636bfe7050aaf0eeab255ff6c111eb0e01`
- plateau counter: `8`
- round loop: `round 7/20`
- rounds remaining: `14`
- notes: `Node C build succeeded for round 7/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_174642_bf16_gemm_v1_52a3af6`
- run dir: `runs/20260419_174642_bf16_gemm_v1_52a3af6`
- correctness: `PASS`
- median runtime: `33.716736 ms`
- TFLOP/s: `21.562568 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_174713`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Audit of the 10 human idea families for round 7 on the restored accepted base 9bdc160, the round-5 Ps2r signal run eff433a, and the round-6 Ps2r refinement regression 52a3af6. Recommendation type: pivot. The diagnosis explicitly pivots from Idea 9 micro-tuning to the higher-ceiling Idea 10 stage family, while keeping Idea 9 alive as a bounded secondary family rather than declaring it dead after one bad step. Per-idea status: (1) Tiling 256x128 block / 64x64 warp = reject-for-this-round, because the current fixed-shape evidence still strongly favors the 64x384 PTX hot band and reopening macro tiling would create a separate branch with weak support from existing measurements. (2) Coalescing Access = accept-now as already present via wide 16-byte accesses; not the next differentiator. (3) Data Reuse through shared memory = accept-now as already core to the kernel. (4) Async Copy = accept-now as already core; near-neighbor handoff retimes remain rejected even though async copy itself is foundational. (5) Bank Conflict = defer, with only the warp-local PTX consumer-side permutation still viable; bank metrics are too flat to rank it in the top 2. (6) L2 Cache swizzle = reject-for-this-round, because current L2/DRAM behavior does not identify cache-locality as the dominant blocker. (7) Register Reuse RLRL = accept-now as a complementary family and kept in the ranked set, but not primary. (8) Pg2s = accept-now as already present and also the foundation for any stage-depth pivot. (9) Ps2r = accept-now and kept alive, but not recommended this round; one positive round plus one failed refinement is enough to justify a bounded continuation, not enough to justify tunneling forever. (10) Stage multi-buffer = accept-now and selected as the primary family this round because the target gap to 20 ms remains huge and the branch needs a higher-ceiling move than another small warp-local feed tweak. Additional negative evidence still in force: no explicit half-panel mma.sync compute rewrite, no pair-compaction retry, no panelized B-load reorder, no helper/lifetime compaction as the main lever, and no near-neighbor handoff-retime retry.`
- dir_01: Human idea 10 Stage: structural pivot to a true deeper hot-band pipeline, budgeted around the export path | bottleneck: One-block occupancy with persistent tensor-underfeed means the kernel still lacks enough overlap depth; stage depth, not another small warp-local reorder, is the highest-ceiling remaining lever.
- dir_02: Human idea 9 Ps2r: one bounded continuation that restores the simpler lookahead signal without slice nesting | bottleneck: Warp-local shared-to-register latency remains a demonstrated limiter, but the current nested Ps2r refinement likely traded away too much simplicity for too little additional latency hiding.
- dir_03: Human idea 7 Register Reuse: RLRL warp-internal accumulator traversal as a complement to the PTX feed path | bottleneck: Warp-internal compute ordering and register reuse inefficiency may now be limiting tensor issue after the obvious feed-side symptoms have been partially addressed.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `6.083199 ms`, `1.234710x` slower than CUTLASS
