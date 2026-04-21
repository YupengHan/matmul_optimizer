# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 8/100` with `93` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_123024`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 8/100 diagnosis emitted after a correctness-failing but highly promising 104-register PTX writer surface appeared.`
- dir_01: Repair the PTX writer row sweep while preserving the 104-register surface | bottleneck: correctness recovery on the PTX export/store path first; if preserved, the new steady-state signature becomes barrier-heavy and more memory-active rather than occupancy-limited
- dir_02: After the writer repair, retime the barrier seam on the 104-register anchor | bottleneck: synchronization_barrier_issue with secondary global_memory_bound behavior on the corrected 104-register PTX surface
- dir_03: Fallback: restore the last correct PTX writer semantics if the low-register repair collapses | bottleneck: fallback recovery to the last correctness-safe current-workload PTX writer surface

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
