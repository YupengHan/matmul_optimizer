# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 2/20` with `19` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_165923`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `All three directions stay strictly inside the 64x384 hot-band PTX microkernel mainline and keep the 64x96 tail unchanged. Ranking is anchored on the latest measured run 20260419_142929_bf16_gemm_v1_a34f072 and the restored accepted base 20260419_142213_bf16_gemm_v1_9bdc160: the round-1 full-width tile-pair fragment issue-order tightening was basically negative evidence, regressing by about 0.024 ms while leaving tensor active, active warps, barrier, mio, and occupancy effectively unchanged. Because barrier and mio are already low, the recommendation shifts toward actual live-state/register relief and export-lifetime cleanup, with orchestration retime kept only as a bounded third option. Previously bad lines remain excluded: no explicit mma.sync half-panel compute, no pair-compaction retry, and no panelized B-load reorder.`
- dir_01: PTX accumulator and export lifetime compaction to attack the 167-register wall | bottleneck: Register-limited occupancy and weak latency hiding are the main remaining bottlenecks; long scoreboard is now the more meaningful residual stall because barrier and mio are already low.
- dir_02: Register-first PTX pair export that trims float c_shared dependence | bottleneck: Export-side shared traffic and shared-backed epilogue temporaries are now a secondary limiter that can still feed into register pressure, LSU pressure, and short/long scoreboard exposure.
- dir_03: PTX two-stage handoff retime for long-scoreboard hiding without new barriers | bottleneck: Residual long-scoreboard latency from the current wait/commit/consume placement may still be leaving tensor issue underfed even after barrier and mio were pushed down.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
