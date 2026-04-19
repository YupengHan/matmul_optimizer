# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 4/5` with `2` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_104652`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Diagnosed accepted-best run 20260419_104631_bf16_gemm_v1_8346b48 at 34.655231 ms. Pairwise peeled hot-loop unrolling was a real win: hot-kernel duration dropped from the 2872f92 base while registers/thread stayed at 128 and occupancy_limit_registers stayed at 2. The remaining dominant symptom is hot-kernel shared/LSU feed pressure, especially mio_throttle at 35.58. The previous named-barrier/subgroup handoff path remains strong negative evidence because it regressed badly to 41.745407 ms by inflating the hot kernel to 167 registers/thread and cutting active warps in half, so none of the ranked directions continue that family.`
- dir_01: Micro-retune the single-level B skew in the peeled 64x384 hot kernel | bottleneck: Shared-memory B-fragment load pressure and bank behavior in the 64x384 hot kernel, expressed as high mio_throttle and LSU issue pressure rather than low occupancy.
- dir_02: Specialize Tile384 cp.async producer assignment in the peeled hot path | bottleneck: Producer-side cp.async issue overhead and LSU address-generation work in the 64x384 hot loop, not a synchronization problem.
- dir_03: Add a fixed-K peeled 64x96 tail kernel | bottleneck: Residual generic-loop and scoreboard overhead in the 64x96 tail kernel; total upside is capped by the tail's small share of wall time.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
