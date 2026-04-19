# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `awaiting_direction_selection_for_node_c`
- round loop: `round 2/5` with `4` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_093742`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 2/5 diagnosis prepared from regressed run 20260419_093633_bf16_gemm_v1_d90a873. Round-1 two-level B staging is treated as negative evidence; recommendation pivots to the human phased-64x384 idea on the restored accepted base surface.`
- dir_01: Phased 64x384 micro-panels to shrink the live set | bottleneck: Register-limited occupancy and weak latency hiding from the 12-fragment live set in the hot 64x384 loop.
- dir_02: Simplify the 64x384 K-loop pipeline instead of repacking B | bottleneck: CTA-wide synchronization and copy-pipeline issue pressure in the hot loop.
- dir_03: Trim the 64x384 epilogue export path on the restored single-skew base | bottleneck: LSU/shared writeback pressure and epilogue-side shared-memory traffic after the main MMA loop.

## Active direction

- selected direction: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`
