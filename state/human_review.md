# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 4/100` with `97` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_114106`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 4/100 diagnosis emitted after a large measured regression on the PTX live-state trim.`
- dir_01: Restore the accepted PTX hot-band anchor after the failed live-state trim | bottleneck: Known register-limited plateau on the accepted 128x128 PTX surface; this direction is a recovery step, not a new bottleneck attack.
- dir_02: After recovery, retime the PTX barrier handoff without changing the shared footprint | bottleneck: synchronization_barrier_issue on the accepted PTX hot-band path
- dir_03: Keep the 256x128 half-panel repair alive, but only after the PTX base is recovered | bottleneck: occupancy_latency_hiding_issue on the wide geometry, with secondary barrier and short-scoreboard sensitivity

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
