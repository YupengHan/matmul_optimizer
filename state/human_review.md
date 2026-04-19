# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 5/5` with `1` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_140716`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `dir_02`
- diagnosis notes: `All three directions remain strictly inside the 64x384 hot-band PTX microkernel branch and keep the 64x96 tail unchanged. Ranking is anchored on the new accepted base c9d030a: the PTX branch has now produced four consecutive real runtime improvements, and round 3 plus round 4 already knocked barrier and mio down to secondary concerns. The remaining guardrail is still one-block occupancy at 167 registers/thread with active warps stuck near 16.6. Because this is the final round, the recommendation favors a safer PTX-local state/lifetime compaction that builds directly on the successful paired export path, while still keeping one higher-upside full-width load-order direction and one more aggressive direct-export follow-through in reserve. Explicit mma.sync half-panel compute is intentionally excluded because that subpath has already shown negative evidence.`
- dir_01: Tile-pair PTX state compaction around the paired export path | bottleneck: Register pressure and live-range inflation around the 12-tile PTX helper surface are keeping occupancy at one block/SM even after control and export overhead were reduced.
- dir_02: Full-width explicit PTX load-order follow-through without half-panel compute | bottleneck: Residual load-to-use latency and fragment feed ordering inside the PTX compute body, now that barrier and mio overhead are largely under control.
- dir_03: Direct register-packed pair export beyond shared float scratch | bottleneck: Export-side shared/LSU work and short-scoreboard pressure, which remain visible even after the paired export cut a layer of the old path.

## Active direction

- selected direction: `dir_02`
- selection mode: `approved`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
