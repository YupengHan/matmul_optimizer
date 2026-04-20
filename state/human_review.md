# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 81/100` with `20` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_115714`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 81/100 diagnosis for run 20260420_115626_bf16_gemm_v1_469a12b. The zero-padding PTX export trim improved runtime to 25.64300728 ms, with tensor activity back at 48.00 and barrier down at 5.50, so the restored PTX baseline is now the current reference. The new concern is long-scoreboard pressure at 7.61, not DRAM or barrier inflation; the broad default-promotion family and the K32 staged family remain closed-negative, so the next work should stay in the PTX-adjacent export/feed/orchestration space rather than reopening those paths.`
- dir_01: Trim The Remaining PTX Export Scoreboard | bottleneck: PTX export-lifetime latency, shared scratch residency, and address-generation overhead in the hot-band store path.
- dir_02: One More Bounded 128x128 Two-Stage Feed Iteration | bottleneck: Copy-feed latency and stage handoff inside the 128x128 two-stage kernel, with long-scoreboard pressure rather than raw tensor under-utilization.
- dir_03: Tighten PTX Hot-Band Grouping And Peel Handoff | bottleneck: Hot-band orchestration and peel coordination, especially around grouped-row mapping and the fixed tail handoff.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
