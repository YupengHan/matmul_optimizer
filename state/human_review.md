# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 3/100` with `98` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_113657`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 3/100 diagnosis re-emitted after clearing the partial node_c edit and rerunning node_b.`
- dir_01: Trim live state inside the recovered 128x128 PTX hot-band control path | bottleneck: occupancy_latency_hiding_issue with a secondary tensor_core_underutilization component on the accepted 128x128 PTX hot-band path
- dir_02: Collapse PTX wait-group and consumer barrier cadence without growing shared state | bottleneck: synchronization_barrier_issue with occupancy_latency_hiding_issue as the guardrail
- dir_03: Repair the 256x128 half-panel register-reuse branch with compact B staging | bottleneck: occupancy_latency_hiding_issue on the wide hot-band geometry, with secondary synchronization_barrier_issue and short_scoreboard sensitivity

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
