# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 82/100` with `19` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_120042`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 82/100 diagnosis for run 20260420_115942_bf16_gemm_v1_6353423. The paired PTX export-helper experiment is now explicitly closed-negative: runtime regressed from 25.64300728 ms to 25.83756828 ms and long-scoreboard worsened to 8.09 even though DRAM and barrier stayed low. Keep the broad default-promotion family, the K32 staged family, and the paired-export-lifetime variant closed. The best current baseline remains the PTX microkernel default with zero export padding, so the next work should stay in bounded PTX-adjacent feed / grouping / control paths rather than re-opening any closed broad family.`
- dir_01: Bound The 128x128 Two-Stage Feed Cadence | bottleneck: Feed latency and stage handoff inside the 128x128 two-stage kernel, with the long-scoreboard rise indicating that the current baseline is still waiting too long on data readiness.
- dir_02: Tighten PTX Hot-Band Grouping And Peel Handoff | bottleneck: Hot-band orchestration overhead and peel coordination, especially around grouped-row mapping and the fixed tail handoff.
- dir_03: Use The Non-PTX 128x128 Sibling As A Control | bottleneck: PTX export-side indirection versus a simpler two-stage feed path in the non-PTX 128x128 sibling.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
