# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 10/100` with `91` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_124005`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 10/100 diagnosis emitted after the compact writer sweep stayed correctness-safe but failed to move the 198-register anchor.`
- dir_01: Retime the PTX barrier seam on the current correctness-safe 128x128 anchor | bottleneck: synchronization_barrier_issue layered on top of occupancy_latency_hiding_issue in the current correctness-safe 128x128 PTX anchor
- dir_02: Apply only a minimal PTX export-address cleanup on the correct anchor | bottleneck: occupancy_latency_hiding_issue with a small tail_overhead_or_generic_path_issue in the PTX export address math
- dir_03: Transplant the lower-register half-panel budget into the correctness-safe 256x128 pivot | bottleneck: occupancy_latency_hiding_issue attacked through geometry and register-budget change rather than another PTX-local cleanup

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
