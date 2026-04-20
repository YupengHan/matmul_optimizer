# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 80/100` with `21` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_114802`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 80/100 diagnosis for run 20260420_114650_bf16_gemm_v1_1b91857. The broad default-dispatch promotion family remains closed-negative, and the K32 staged family is also closed-negative after the round-79 regression. The existing 128x128 two-stage sibling improved strongly from 31.55292797 ms to 27.07665539 ms, with tensor activity back near baseline at 48.18 and long scoreboard down at 1.51, but it still trails the restored PTX baseline in the current environment while dram (31.39) and LTS (27.25) remain elevated. Treat the remaining gap as export/orchestration work, not another baseline-restore loop.`
- dir_01: Trim PTX Export Scratch On The Restored Baseline | bottleneck: PTX epilogue export bandwidth, shared scratch lifetime, and L2 traffic in the hot-band store path.
- dir_02: One More Bounded 128x128 Two-Stage Sibling Iteration | bottleneck: Synchronization and feed latency inside the 128x128 two-stage kernel, not tensor throughput.
- dir_03: Tighten PTX Hot-Band Grouping And Peel Orchestration | bottleneck: Hot-band orchestration overhead and peel coordination, especially around grouped-row partitioning.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
