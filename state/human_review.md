# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 75/100` with `26` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_113007`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Latest measured run 20260420_112828_bf16_gemm_v1_f1ae7fa is effectively unchanged from round 74: 24.6968317 ms vs 24.69619179 ms, TFLOP/s 29.4377607, tensor active 48.23, warps active 16.57, barrier 6.39, long scoreboard 3.74, mio throttle 3.34, and launch__occupancy_limit_registers = 2. That makes the PTX helper flattening family effectively closed-negative for this round unless a clearly different variant is proposed. Ranking now shifts to distinct schedule families: the wide 64x384 dispatch path as the best grounded non-PTX alternative, the auxiliary 256x128 schedule as the next distinct schedule family, and the 128x128x32 staged kernel as a lower-rank but materially different PTX-adjacent option.`
- dir_01: Promote The 64x384 Hot-Band Dispatch And Retune Around The Wide-Tile Path | bottleneck: Register pressure and launch/schedule overhead in the current PTX hot-band path, which is consistent with the low 16.57 warps-active number and the register occupancy limit.
- dir_02: Revisit The Auxiliary 256x128 Hot-Band Schedule As A Separate Family | bottleneck: Compute scheduling and latency hiding on the auxiliary 256x128 hot-band path, not DRAM bandwidth.
- dir_03: Activate Or Retune The 128x128x32 Staged Hot-Band Kernel To Cut Live Ranges | bottleneck: Register pressure plus stage-synchronization overhead in the 128x128x32 hot-band variant.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
