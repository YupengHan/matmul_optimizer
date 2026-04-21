# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 7/100` with `94` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_122308`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 7/100 diagnosis emitted after the round-6 helper-flattening probe improved runtime slightly without changing the core occupancy signature.`
- dir_01: Trim PTX export/store-path scalar live state on the current 128x128 anchor | bottleneck: occupancy_latency_hiding_issue with tail_overhead_or_generic_path_issue concentrated in the PTX export/store path after the MMA loop
- dir_02: Retime the PTX wait-group and CTA barrier seam on the current anchor | bottleneck: synchronization_barrier_issue layered on top of an occupancy_latency_hiding_issue in the active 128x128 PTX hot-band kernel
- dir_03: Transplant the lower-register half-panel budget into the correctness-safe 256x128 pivot | bottleneck: occupancy_latency_hiding_issue addressed by a geometry and register-budget change rather than another PTX-local retime

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
