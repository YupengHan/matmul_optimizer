# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 6/20` with `15` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_174046`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Audit of the 10 human idea families for round 6 on the restored accepted base 9bdc160 and the round-5 Ps2r run eff433a: (1) Tiling 256x128 block / 64x64 warp = reject-for-this-round, because the accepted 64x384 PTX hot band is still the only measured winner and reopening tile hierarchy leaves the validated mainline. (2) Coalescing Access wide global-memory instructions = accept-now as already present in the base through 16-byte async copies and wide stores, but not the next differentiator. (3) Data Reuse using shared memory for A and B = accept-now as already core to the current kernel, not the missing lever. (4) Async Copy = accept-now as already core; near-neighbor handoff-retime retries remain rejected even though async copy itself is foundational. (5) Bank Conflict = accept-now only in the narrow warp-local PTX consumer-permutation form; CTA-wide reorder stays rejected. (6) L2 Cache swizzle = reject-for-this-round, because L2/DRAM behavior does not point to cache locality as the primary blocker on the restored base. (7) Register Reuse RLRL internal warp schedule = accept-now as a complementary family, but not primary because it is adjacent to the earlier low-value issue-order result and must be justified through reuse, not mere reorder. (8) Pg2s double-buffer global-to-shared = accept-now as already present in the base and not the new lever. (9) Ps2r double-buffer shared-to-register = accept-now and selected as the primary family again for round 6, because round 5 provided positive measured evidence by lowering the targeted long-scoreboard stall even though it did not yet beat the accepted base. (10) Stage multi-buffer global-to-shared = defer, because it remains high-upside but still blocked by shared/register budget and is not yet the most practical next move. Additional negative evidence still in force: no explicit half-panel mma.sync compute rewrite, no pair-compaction retry, no panelized B-load reorder, no helper/lifetime compaction as the main lever, and no near-neighbor handoff-retime retry.`
- dir_01: Human idea 9 Ps2r: slice-local two-fragment ping-pong on the full-width PTX sweep | bottleneck: Warp-local shared-to-register latency is now a proven residual limiter, but the current Ps2r form is not organized tightly enough to convert that stall reduction into better tensor issue.
- dir_02: Human idea 7 Register Reuse: RLRL serpentine tile traversal on top of Ps2r-compatible PTX compute | bottleneck: Residual tensor under-issue now looks more like warp-internal compute ordering and register reuse inefficiency than raw memory feed failure.
- dir_03: Human idea 5 Bank Conflict: warp-local PTX B-consumer permutation layered under Ps2r | bottleneck: Residual bank/LSU serialization on B-fragment loads may still be limiting how much of the round-5 Ps2r gain reaches tensor issue.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
