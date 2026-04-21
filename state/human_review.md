# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 12/50` with `39` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_192106`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 12/50: `state/human_review.md` currently contributes only the approval/selection gate and no extra user-authored idea families, so the ranking is tied directly to measured evidence. Accepted for this round: the fixed-shape tile-routing family backed by `state/autotune_round18_main_tiles.md`, where `64x384` was the best measured hot-band width. Deferred: deeper PTX hot-band tuning until the active `128x128` branch is no longer stuck at `200` regs/thread and `16.64%` active warps. Rejected as the primary explanation: a DRAM-bound diagnosis for the main path, because the active hot-band kernel reaches only `13.05%` DRAM throughput while tensor cycles are `48.09%`. Tail-memory cleanup remains tertiary because the `64x96` branch covers only the last `96` columns.`
- dir_01: Restore Sweep-Backed 64x384 Full Hot Band | bottleneck: Main hot-band occupancy and tensor-core under-utilization caused by the default dispatch choosing the PTX `128x128` branch instead of the measured `64x384` full-band tile path.
- dir_02: Trim 128x128 PTX Hot-Band Register Pressure | bottleneck: Register-limited occupancy inside the PTX hot-band microkernel, amplified by heavy LSU/shared export work in the current accumulate/store path.
- dir_03: Specialize The 64x96 Tail Memory Path | bottleneck: Memory and LSU pressure in the fixed `64x96` tail region, not the primary hot-band compute path.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
