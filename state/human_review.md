# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 15/20` with `6` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_190621`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 15 is a continue-family move on the new Human idea 1 / Tiling branch, not a pivot away from it. The evidence is decisive: the 256x128 CTA / 64x64 warp structural pivot created the new accepted base, and the round-14 paired-export follow-up improved it again to 30.06254387 ms. The key interpretation is that paired export worked even though the headline barrier metric barely moved: the hot kernel stayed at barrier 20.89 vs 20.76 before, registers stayed at 166, tensor active stayed essentially flat at 37.58 vs 37.63, and active warps stayed around 16.55. The real signal was elsewhere: long scoreboard dropped from 0.55 to 0.22, short scoreboard dropped slightly from 6.78 to 6.64, and the hot-kernel time still improved. That means the paired-export win came from shortening warp-local export and dependency chains, not from removing the main-loop CTA barrier. So the next move should not blindly chase the barrier percentage. It should exploit the new export structure to attack the next unchanged wall: live-state and register pressure inside the 64x64 PTX microkernel.

Human idea audit for round 15:
1. Tiling: accept-now as the active top-level family. The 256x128/64x64 branch is clearly the current mainline and should keep the implementation surface.
2. Coalescing Access: defer. DRAM throughput is only 17.81 and the branch already uses wide async copies, so global coalescing is not the next limiter.
3. Data Reuse: accept-now as a concrete secondary direction. Reusing dead B-shared storage for export scratch is now technically relevant because paired export already proved that export-side scratch matters.
4. Async Copy: accept-now only as an established baseline. The current branch is not losing to obvious global-to-shared latency anymore.
5. Bank Conflict: accept-now as a lower-ranked local follow-up. With long scoreboard nearly gone, the residual short-scoreboard may now be local shared-load behavior in the 64x64 branch.
6. L2 Cache: reject-for-this-round. The hot kernel is not L2- or DRAM-limited.
7. Register Reuse: accept-now and rank first. Registers per thread are still 166, occupancy remains register-limited, and paired export created a concrete way to flush partial work earlier and reuse accumulator state.
8. Pg2s: defer. The global-to-shared pipeline is already doing its job on this family.
9. Ps2r: defer. Long scoreboard is already tiny, so another Ps2r-first move is not the highest-value next step here.
10. Stage: reject-for-this-round. A deeper stage family is both budget-constrained by the new shared-memory footprint and less evidence-backed than the current tiling branch.

Primary choice for this round: continue the Human idea 1 family, but shift the immediate lever to Human idea 7 register reuse inside that family. The round-14 result says export structure is now an enabling mechanism, not the main unfinished objective.`
- dir_01: Human idea 7 Register reuse: stream the 64x64 PTX micro-tile by row-pairs and export each completed pair through the new paired scratch | bottleneck: Register and warp-local dependency pressure inside the 64x64 PTX microkernel, which now appears more important than headline CTA barrier rate.
- dir_02: Human idea 3 Data reuse: keep paired export, but remap its scratch onto dead B-shared storage so the win survives without the extra 8 KB c_shared budget | bottleneck: Dedicated export scratch budget and residual export-side dependency overhead at the end of the 256x128 kernel.
- dir_03: Human idea 5 Bank conflict: retime only the 64x64 branch's B-fragment load and consume order to target the remaining short-scoreboard tax | bottleneck: Warp-local shared-memory load and bank behavior in the 64x64 PTX branch, showing up primarily as residual short-scoreboard rather than global-memory latency.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
