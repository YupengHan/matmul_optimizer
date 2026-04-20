# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 17/20` with `4` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_192859`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 17 should be treated as a continue-family move, not a pivot away from the half-panel line. The raw kernel signal is too strong to ignore: in the hot bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel, launch__registers_per_thread fell from 167 to 93, launch__occupancy_limit_registers increased from 1 to 2, sm__warps_active rose from 16.68 to 32.98, and sm__pipe_tensor_cycles_active rose to 42.01. That is the first result in many rounds that clearly punctures the register wall instead of just moving stalls around. The reason wall-clock and correctness both failed is that the current implementation only solved half the problem. It cut the accumulator set to 64x32 + 64x32, but it still replays full-width A/B staging for both passes, especially a full 128-column B tile through stage_b_shared_tile_async<FixedHotBandTile256x128>(), which drives compute-memory throughput up to 61.03 and dram throughput up to 35.19. On top of that, the pass-local export/orchestration is fragile enough that correctness failed with max_abs_err around 10.14. So the correct conclusion is not 'family failed'; it is 'family is real, but the current implementation is incomplete and wrong.' With only four rounds left, the best strategy is to continue the family only if the next round repairs correctness and removes the obvious full-width feed tax together, rather than spending two more rounds on isolated micro-fixes.

Human idea audit for round 17:
1. Tiling: accept-now as the proven top-level family. Do not reopen unrelated macro-tile retunes.
2. Coalescing Access: defer. The current problem is not generic vector width; it is pass-local dataflow and replayed movement.
3. Data Reuse: accept-now as a supporting lever. Compact pass-local B staging is now directly relevant.
4. Async Copy: accept-now as a supporting lever. The recommended direction still uses async copy, but makes it half-panel-local.
5. Bank Conflict: defer as a secondary alternative. Shared-load pressure is real, but only after the half-panel family is made correct and less wasteful.
6. L2 Cache: reject-for-this-round. The current profile is dominated by replayed feed, not an isolated cache-hint problem.
7. Register Reuse: accept-now and rank first. This family is the first one that clearly broke the register wall.
8. Pg2s: accept-now as a supporting lever. The next step should compact the producer path around the active half-panel slices.
9. Ps2r: reject-for-this-round. The new issue is not shared-to-register lookahead; it is duplicated producer traffic and incorrect panel orchestration.
10. Stage: reject-for-this-round. There is no time budget to reopen a previously weaker family when the current one just showed a real occupancy breakthrough.

Primary decision: continue Human idea 7 inside the Human idea 1 tiling mainline, but upgrade it from an accumulator-only half-panel cut to an end-to-end half-panel pass. That is the only route that both respects the strong signal and has a plausible path to convert it into a measured win within the remaining rounds.`
- dir_01: Human idea 7 Register reuse: continue the half-panel family, but make it an end-to-end 64x32 pass with explicit half-panel export mapping and compact B staging | bottleneck: Broken half-panel orchestration: correctness risk in the pass-local export mapping plus excessive shared/global feed from replaying full-width B staging for both half-panel passes.
- dir_02: Human idea 7 Register reuse: do a correctness-first repair of half-panel export/orchestration only, leaving feed structure unchanged for one validation round | bottleneck: Correctness bug in the half-panel export/pass plumbing, with the full-width B replay cost intentionally left unchanged for one bounded verification step.
- dir_03: Human idea 5 Bank conflict: abandon the broken half-panel branch and return to the accepted base for a bounded local shared-load retune | bottleneck: Residual shared-memory bank / short-scoreboard behavior on the accepted-base 256x128/64x64 path, after abandoning the broken half-panel branch.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
