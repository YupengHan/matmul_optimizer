# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 9/100` with `92` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_123602`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 9/100 diagnosis emitted after the direct writer correctness fix erased the round-7 low-register gain, suggesting the next search unit should target a more compact full-row sweep rather than abandoning the signal immediately.`
- dir_01: Recover a compact correctness-safe 4-row PTX writer sweep | bottleneck: occupancy_latency_hiding_issue in the PTX export/store path if a compact full-row sweep can retain some of the low-register behavior while staying correct
- dir_02: Retime the barrier seam on the current correct 128x128 PTX anchor | bottleneck: synchronization_barrier_issue layered on top of occupancy_latency_hiding_issue in the current correctness-safe PTX anchor
- dir_03: Fallback to the current correctness-safe PTX writer anchor if compact sweeping stalls out | bottleneck: fallback recovery to the current correctness-safe PTX writer anchor

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
