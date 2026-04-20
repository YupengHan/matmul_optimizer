# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 1/17` with `17` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_154129`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 1/17 diagnosis for run 20260420_153144_bf16_gemm_v1_c550d79. Human-review mapping: accept narrow PTX-adjacent follow-ups on top of the restored zero-padding PTX baseline; defer pure baseline-restore work because the loop already anchored a new accepted base at 25.76332855 ms; reject reopening broad default-promotion, staged K32, paired export-lifetime, and helper-flattening families. The latest run recovered the PTX path and pulled DRAM back down to 11.52%, but it still trails the earlier PTX baseline because long-scoreboard rose to 7.79 while tensor activity stayed flat near 48%. That makes grouped traversal the best next move, with export-helper cleanup and PTX-specific prefetch retiming as the two secondary families.`
- dir_01: Retune PTX Hot-Band Group Traversal Around The 6-Row Window | bottleneck: Hot-band orchestration locality and CTA traversal order inside the PTX microkernel, visible as long-scoreboard pressure with DRAM and L2 acting as guardrails.
- dir_02: Trim PTX Export Syncs Without Reopening The Paired-Scratch Family | bottleneck: PTX export-side synchronization and shared-to-global store orchestration in the hot-band epilogue.
- dir_03: Retune PTX Prefetch Handoff In The K Loop | bottleneck: Copy-pipeline depth and handoff timing in the PTX hot-band steady-state loop.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
