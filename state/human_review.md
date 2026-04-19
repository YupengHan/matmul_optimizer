# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `awaiting_direction_selection_for_node_c`
- round loop: `round 1/5` with `5` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_092350`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 1/5 diagnosis prepared from run 20260419_015554_bf16_gemm_v1_16a98f7. Recommended dir_01 per human-priority override; dir_01 and dir_02 are human ideas.`
- dir_01: Two-level B staging for the 64x384 hot band | bottleneck: Shared/L1 B-feed pressure and LSU issue bandwidth in the hot 64x384 kernel.
- dir_02: Phased 64x384 micro-panels to shrink the live set | bottleneck: Register-limited occupancy and weak latency hiding from keeping the full 384-wide working set live per warp.
- dir_03: Warp-specialized producer-consumer pipeline for the 64x384 loop | bottleneck: Synchronization and stage-orchestration overhead in the hot K-loop rather than raw DRAM bandwidth.

## Active direction

- selected direction: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`
