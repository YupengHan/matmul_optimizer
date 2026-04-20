# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 83/100` with `18` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_120428`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 83/100 diagnosis for run 20260420_120349_bf16_gemm_v1_af42390. The bounded 128x128 two-stage cadence experiment is now effectively closed as a distinct next step: it was flat-to-slightly-negative versus the best PTX baseline, with runtime 25.90412712 ms, barrier 5.24, mio 3.00, but dram 30.18 and long scoreboard 7.22. The paired-export-lifetime variant remains closed-negative, and the best current baseline stays the PTX microkernel default with zero export padding. The next work should target long-scoreboard reduction at the PTX hot-band grouping / orchestration boundary or use another narrow PTX-adjacent control path, not reopen the closed broad families.`
- dir_01: Tighten PTX Hot-Band Grouping For Long-Scoreboard | bottleneck: Long-scoreboard stalls caused by hot-band orchestration, grouped-row mapping, and tail handoff in the PTX microkernel path.
- dir_02: Low-Risk PTX Export-Side Cleanup | bottleneck: Residual address-generation and scratch-lifetime overhead in the PTX store helpers.
- dir_03: Use The Non-PTX 128x128 Sibling As A Control | bottleneck: PTX export/store complexity versus a simpler non-PTX 128x128 feed path.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
