# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 5/20` with `16` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_173445`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Audit of the 10 human idea families for this round on the restored accepted base 9bdc160 and the failed round-4 export-shrink run d2a8c31: (1) Tiling 256x128 block / 64x64 warp = reject-for-this-round, because the accepted 64x384 hot-band tile is still the only measured winner and reopening tile hierarchy exits the current PTX mainline. (2) Coalescing Access wide global-memory instructions = accept-now as already present via 16-byte cp.async-style wide accesses, but not the main limiter this round. (3) Data Reuse through shared memory for A and B = accept-now as already core to the current kernel, not the next differentiator. (4) Async Copy non-blocking = accept-now as already core to the current kernel; near-neighbor handoff-retime retries are rejected as a primary lever. (5) Bank Conflict padding/permuted access = defer, with only the warp-local PTX consumer-side permutation still viable; CTA-wide reorder remains rejected. (6) L2 Cache swizzle access mode = reject-for-this-round, because current L2/DRAM behavior does not point to cache locality as the dominant blocker. (7) Register Reuse Right-Left-Right-Left warp-internal schedule = defer, because it sits too close to the earlier low-value issue-order family to be the round-5 primary bet. (8) Pg2s double-buffer global-to-shared = accept-now as already present in the accepted base; it is a foundation, not the recommended new family. (9) Ps2r double-buffer shared-to-register = accept-now and selected as the primary idea family for round 5, because current residual long-scoreboard under one-block occupancy points most directly here. (10) Stage multi-buffer global-to-shared = defer, because it remains high-upside but budget-blocked for this round even after export-side scratch shrink. Additional negative evidence still in force: no explicit half-panel mma.sync compute rewrite, no pair-compaction retry, no panelized B-load reorder, no helper/lifetime compaction as the main lever, and no near-neighbor handoff-retime retry.`
- dir_01: Human idea 9 Ps2r: full-width PTX shared-to-register lookahead inside the 12-tile sweep | bottleneck: Warp-local shared-to-register latency on B-fragment consumption is the most actionable remaining underfeed source once export shrink and handoff retime have both failed to beat the accepted base.
- dir_02: Human idea 5 Bank Conflict: warp-local PTX B-fragment permute without CTA reorder | bottleneck: Residual shared-bank serialization on the B-fragment consumer path may still be contributing to long-scoreboard and LSU pressure even though the current skew avoids catastrophic conflicts.
- dir_03: Human idea 10 Stage: real third G2S stage only after the budget math closes | bottleneck: If the branch can eventually add a genuine third global-to-shared stage, the main payoff would be deeper latency hiding under one-block occupancy rather than a marginal retime of the existing two-stage pipeline.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
