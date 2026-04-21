# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 6/100` with `95` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_114852`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-review reflection for round 6: accept the live barrier-trim family and the PTX export cleanup family against the latest rich NCU evidence; defer the 256x128 register-budget transplant as the orthogonal structural branch; reject another accepted-surface restore this round because the current workload no longer reproduces the stale 24 ms anchor.`
- dir_01: Retime the PTX wait-group and CTA barrier seam on the current 128x128 anchor | bottleneck: synchronization_barrier_issue layered on top of an occupancy_latency_hiding_issue in the active 128x128 PTX hot-band kernel
- dir_02: Trim PTX export-address and store-path scalar live state after the MMA loop | bottleneck: occupancy_latency_hiding_issue with tail_overhead_or_generic_path_issue concentrated in the PTX export/store path
- dir_03: Transplant the lower-register half-panel budget into the correctness-safe 256x128 pivot | bottleneck: occupancy_latency_hiding_issue addressed by a geometry and register-budget change rather than another PTX-local retime

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
