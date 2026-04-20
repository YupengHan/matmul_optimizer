# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 20/20` with `1` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_200532`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 20 human-idea audit against measured evidence: Tiling is accepted historically, but the final-round implication is now to return to the correct 64x384 accepted base rather than keep the 256x128 half-panel branch alive, because the half-panel family remained incorrect after two repair rounds. Coalescing Access is accepted as baseline because 16-byte cp.async staging is already in place; Data Reuse is accepted as baseline because both the accepted base and the half-panel branch already depend on shared-memory reuse; Async Copy is accepted as baseline for the same reason; Bank Conflict is accepted as the primary final-round family because the user specifically asked that any renewed B-feed experiment stay warp-local and avoid CTA repack overhead; L2 Cache swizzle is deferred because neither the accepted base nor the latest failed run looks L2-bound; Register Reuse is rejected for the final round as a primary family because the half-panel branch still fails correctness despite strong occupancy; Pg2s is accepted as baseline because double-buffer global-to-shared prefetch is already present; Ps2r is deferred because A-side reuse only matters if the half-panel branch is first made correct; Stage is accepted as a secondary correct-branch family, but not the top pick, because the accepted base already reduced barrier and mio substantially. Recommended direction is dir_01 because the last round should end on the correct branch and still test one auditable feed idea that respects the user's hard constraints.`
- dir_01: Human idea 5 Bank conflict fallback: restore the accepted 64x384 base and try a warp-local B-consumer transform with zero extra CTA repack | bottleneck: Shared/L1/bank behavior on the stable 64x384 hot path rather than occupancy. The goal is to improve operand delivery without destabilizing correctness.
- dir_02: Human idea 7 last-chance sparse-error repair: keep the half-panel branch and hunt the remaining outlier path only | bottleneck: Residual sparse correctness bug in the half-panel path, likely in the remaining lane/local-half ownership contract or export path rather than feed throughput.
- dir_03: Human idea 10 Stage / human idea 4 epilogue budget: return to the accepted base and trim the steady-state barrier or c_shared export path instead of touching B layout | bottleneck: Residual steady-state barrier/export overhead on the accepted 64x384 path, not register pressure.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
