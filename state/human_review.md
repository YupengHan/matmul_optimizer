# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 5/100` with `96` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_114422`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 5/100 diagnosis emitted after recognizing that the historical accepted base is stale under the latest workload.`
- dir_01: Re-anchor on the best measured PTX surface under the current workload | bottleneck: Current-workload re-anchoring step; establishes the local PTX baseline before the next bounded barrier exploit.
- dir_02: After re-anchoring, retime the PTX barrier handoff on the 198-register surface | bottleneck: synchronization_barrier_issue on the current-workload 198-register PTX surface
- dir_03: Keep the 256x128 half-panel repair alive behind the new local anchor | bottleneck: occupancy_latency_hiding_issue on the wide geometry, with secondary barrier sensitivity

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
