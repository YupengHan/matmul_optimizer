# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 4/5` with `2` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_140002`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `dir_01`
- diagnosis notes: `All three directions stay strictly inside the 64x384 hot-band PTX microkernel branch and keep the 64x96 tail unchanged. Ranking uses the new fact that round 3 pushed runtime down again to 33.366 ms while barrier and mio both dropped materially, so the branch should not change lines now. The remaining guardrail is still occupancy_limit_registers=1 with active warps stuck near 16.6, but the profile also shows compute-memory and DRAM throughput already much higher than before. That shifts ranking toward end-to-end PTX follow-through on export and full-width dataflow control, while explicitly avoiding the previously rejected explicit mma.sync half-panel subpath.`
- dir_01: Register-first PTX export follow-through on the hot band | bottleneck: The remaining cost has shifted away from barrier and mio tax toward export-side shared/LSU work and residual register lifetime in the hot-band epilogue.
- dir_02: Full-width explicit PTX load-order control without the regressed half-panel path | bottleneck: With barrier and mio now low, residual long-scoreboard and feed latency inside the PTX compute body are a more plausible limiter than orchestration tax.
- dir_03: PTX helper and lifetime compaction for the 12-tile accumulator set | bottleneck: Compiler-visible live-range inflation around the named 12-tile PTX helper surface is still contributing to the occupancy guardrail even after orchestration improvements.

## Active direction

- selected direction: `dir_01`
- selection mode: `approved`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
