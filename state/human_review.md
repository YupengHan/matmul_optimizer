# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `single-run` with `0` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260418_194629`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `dir_01`
- dir_01: Rewrite the steady-state tile around BF16 Tensor Cores | bottleneck: Tensor Core under-utilization
- dir_02: Keep tiles in BF16 and add a staged vectorized copy pipeline | bottleneck: Global-memory and shared-memory staging pressure
- dir_03: Split the fixed-shape steady state from edge cleanup | bottleneck: Tail-handling overhead from generic code and excess synchronization

## Active direction

- selected direction: `dir_01`
- selection mode: `approved`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
