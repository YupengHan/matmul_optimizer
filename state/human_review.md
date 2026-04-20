# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 19/20` with `2` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_195407`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 19 human-idea audit against measured evidence: Tiling is accepted and already embodied by the active 256x128 CTA / 64x64 warp branch; Coalescing Access is accepted as baseline because the kernel is already on 16-byte cp.async loads and the latest run is not transaction-bound; Data Reuse is accepted as baseline because the branch already depends on shared-memory reuse for both operands; Async Copy is accepted as baseline because cp.async is already central to the pipeline; Bank Conflict is deferred this round except as the fallback family because the current blocker is correctness rather than shared-feed throughput; L2 Cache swizzle is deferred because lts throughput is only 36.08% and DRAM is 21.33%, so cache is not the dominant limiter; Register Reuse is accepted as the primary family because the half-panel branch is still the only path that broke below 100 regs and lifted active warps into the low-30s; Pg2s is accepted as baseline because double-buffer global-to-shared prefetch is already present; Ps2r is accepted as the next family after correctness because replaying A across two serial half panels is now the clearest avoidable tax; Stage is accepted as baseline because the two-stage pipeline is already doing its job and the current evidence does not justify stage-count churn. Recommended direction is dir_01 because with only two rounds left, the penultimate round should either make the high-ceiling half-panel family correct or decisively prove it is not salvageable.`
- dir_01: Human idea 7 Register reuse: keep the half-panel family and close the remaining correctness gap by single-sourcing warp ownership end to end | bottleneck: Residual half-panel address-contract mismatch in the shared-to-fragment or fragment-to-export path, not DRAM bandwidth. The runtime and occupancy signal say the family is viable; correctness is the blocking bottleneck.
- dir_02: Human idea 9 Ps2r: fuse the two 32-column passes inside one K-loop so each staged A tile is consumed twice before advancing | bottleneck: Barrier and shared/A-feed replay overhead caused by running the left and right half panels as two full passes. Successful fusion should cut barrier pressure and short-scoreboard pressure without giving back the occupancy gain.
- dir_03: Human idea 5 Bank conflict fallback: return to the accepted 64x384 path and try a warp-local B-consumer transform with no extra CTA repack | bottleneck: Shared/L1/bank behavior on the stable 64x384 hot path rather than occupancy. This is a lower-ceiling but lower-correctness-risk fallback.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
