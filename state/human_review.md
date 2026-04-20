# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 3/20` with `18` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_170743`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `All three directions remain strictly inside the 64x384 hot-band PTX microkernel mainline and keep the 64x96 tail unchanged. Ranking is anchored on the latest regressed run 20260419_170714_bf16_gemm_v1_1930e3f while reasoning from the restored accepted base 20260419_142213_bf16_gemm_v1_9bdc160. The new hard evidence is that helper/lifetime compaction is not an effective next move on this branch: it only lowered launch__registers_per_thread from 167 to 166 and slightly improved barrier/long-scoreboard/mio, yet runtime still regressed by about 1.58 ms. That rules out retrying helper compaction as a family. Earlier negative evidence also remains in force: no explicit mma.sync half-panel compute, no pair-compaction retry, and no panelized B-load reorder. The recommendation therefore shifts toward bounded schedule/dataflow changes that can still matter at occupancy_limit_registers=1 without reopening the already-failed structural cleanups.`
- dir_01: Asymmetric PTX two-stage handoff retime without new barriers | bottleneck: With occupancy still capped at 1 block/SM and barrier plus mio already low, the more actionable residual is long-scoreboard latency that is not being hidden well enough by the current steady-state handoff.
- dir_02: Register-first PTX pair export beyond float shared scratch | bottleneck: Export-side shared traffic and epilogue-side live state are still secondary pressure points that can feed both runtime and the remaining register wall even when barrier and mio are already low.
- dir_03: Full-width PTX B-fragment lookahead pipeline inside the 12-tile sweep | bottleneck: Residual long-scoreboard latency on shared-backed B fragment loads may still be limiting tensor issue efficiency more than the current headline metrics suggest.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
