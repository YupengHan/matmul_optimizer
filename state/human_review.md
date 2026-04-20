# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 47/100` with `54` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_073749`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `- Context: round 46's grouped-row traversal moved the measured median runtime from 26.892288 ms to 25.677312 ms, set a new best custom run, and already beat the local CUTLASS baseline, but the user goal is still <20 ms so winning the baseline is only a waypoint.
- Hotspot weighting: the dominant profile cost is still the grouped 128x128 PTX hot-band kernel; the peeled 64x384 and tiny tail kernel are much smaller, so diagnosis ranking stays focused on the hot band.
- Headline delta read: tensor active 48.24 -> 48.22 was basically flat, warps active 16.68 -> 16.86 ticked up, barrier 8.48 -> 7.63 fell, short scoreboard 2.03 -> 1.91 fell, and long scoreboard 1.42 -> 1.29 fell. This says the gain came from cleaner feed/locality rather than a new compute schedule.
- Coalescing Access: partially validated already. Grouped-row likely fixed the most important access-order waste, so I am not ranking generic vectorization/coalescing changes first.
- Data Reuse: strongly supported. dram throughput dropping to 12.90% while lts throughput returned to 29.45% is the clearest sign that the grouped-row remap improved cross-CTA reuse, so dir_01 keeps pushing this family.
- Async Copy: already present and functional through cp.async, so the question is not whether to add async copy but whether the cadence and recycle timing are still optimal. That makes Async Copy a lower-priority refinement, not the lead move.
- Bank Conflict: still worth watching. The hot-band kernel shows non-trivial l1tex bank read/write activity, so some of the remaining feed pain may still be hidden as shared-bank friction rather than pure DRAM latency.
- L2 Cache: the current profile most clearly endorses this family. Locality got better without raising tensor active, which is why the top recommendation stays on grouped-row/L2/feed refinement.
- Register Reuse: still a live secondary family. The 128x128 PTX microkernel keeps tight accumulator/export state, but its mirrored-column B reload pattern suggests there is still room to trade a little register reuse for fewer ps2r/shared reloads if occupancy survives.
- Pg2s: no longer the lead suspect. The global-to-shared path is already 16-byte cp.async based, and the dramatic DRAM drop says gross pg2s inefficiency is not the main thing blocking <20 ms.
- Ps2r: still attractive. The PTX hot-band path reloads B fragments per row pair instead of using the lookahead pattern that exists elsewhere, so dir_02 explicitly re-tests this family under the new locality regime.
- Stage: worth re-evaluating, but only third. Barrier improved enough that stage cadence no longer looks like the primary limiter, yet 7.63% barrier is still high enough to justify a controlled K16 vs K32 check after the higher-confidence feed and ps2r ideas.`
- dir_01: Tighten Grouped-Row L2 Feed In The 128x128 PTX Hot Band | bottleneck: Residual hot-band L2-to-shared feed inefficiency in the dominant 128x128 PTX microkernel, showing up as remaining mio_throttle plus modest shared-bank pressure even after locality improved.
- dir_02: Trim PTX Hot-Band Ps2r Live Range Without Losing Occupancy | bottleneck: Compute-side fragment feed and shared-to-register pressure inside the hot-band PTX microkernel, contributing to residual mio_throttle and leaving tensor active essentially flat even after the locality fix.
- dir_03: Re-evaluate K16 Versus K32 Stage Cadence After Locality Recovery | bottleneck: Steady-state cp.async handoff cadence and CTA sync frequency in the 128x128 hot band, with risk that a deeper per-stage payload raises shared pressure faster than it reduces barriers.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
