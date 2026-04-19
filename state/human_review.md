# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 3/5` with `3` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_123925`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Diagnosed round-2 run 20260419_123851_bf16_gemm_v1_98fdc11 while ranking against the restored accepted base 15d63b2 at 35.725824 ms. Round 1 warp specialization remains strong negative evidence because it pushed the hot kernel to 219 registers/thread, occupancy_limit_registers to 1, and active warps to 16.60. Round 2 phase splitting is mixed evidence: it improved over round 1 and lowered barrier and mio versus the accepted base, but it still regressed to 36.462511 ms and raised hot-kernel short-scoreboard stall from 0.54 to 4.50. The ranking therefore avoids the warp-specialized family entirely and stays conservative about phase-split follow-ons.`
- dir_01: Straight-line the Tile384 cp.async producer schedule on the restored base | bottleneck: Producer-side cp.async issue and LSU address-generation overhead in the 64x384 hot kernel, while preserving the accepted 128-register, 2-block occupancy behavior.
- dir_02: Pair Tile384 epilogue export across the existing two C-scratch stages | bottleneck: Hot-kernel shared export and LSU traffic after MMA completion, which can still dilute tensor issue even when occupancy is healthy.
- dir_03: Peel only the fixed final-drain path instead of the whole hot-loop schedule | bottleneck: Terminal stage-drain control overhead in the hot kernel, with risk that a fixed-shape rewrite simply trades barrier/mio improvements for more scoreboard stalls again.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
