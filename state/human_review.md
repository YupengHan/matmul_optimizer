# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 79/100` with `22` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_114507`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 79/100 diagnosis for run 20260420_114346_bf16_gemm_v1_a7d3817. The staged K32 family is now explicitly closed-negative: the round-79 measurement regressed to 31.55292797 ms with tensor active 39.90, barrier 10.02, long scoreboard 5.76, mio 4.98, and dram 23.54. The restored PTX baseline from round 78 remains the current reference shape in this environment, but the source surface alone does not explain the slowdown back to 25.97375965 ms and should not be treated as an unresolved launch-path difference. Do not reopen the broad default-dispatch promotion family unless a concrete new hypothesis appears.`
- dir_01: Activate The Existing 128x128 Two-Stage Hot-Band Kernel | bottleneck: Residual synchronization and latency-hiding overhead in the hot-band steady state, with lower occupancy pressure than the failed K32 staging variant.
- dir_02: Trim PTX Export And Scratch Shape On The Restored Baseline | bottleneck: PTX epilogue overhead, register pressure around the export path, and secondary synchronization cost rather than raw tensor throughput.
- dir_03: Bound The 128x128 PTX Hot-Band Grouping Window | bottleneck: Group coordination and tail-peeled row-band overhead inside the PTX hot-band path, not the staged K32 pipeline itself.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
