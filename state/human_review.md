# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `awaiting_direction_selection_for_node_c`
- round loop: `single-run` with `0` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260418_194629`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Rewrite the steady-state tile around BF16 Tensor Cores | bottleneck: Tensor Core under-utilization
- dir_02: Keep tiles in BF16 and add a staged vectorized copy pipeline | bottleneck: Global-memory and shared-memory staging pressure
- dir_03: Split the fixed-shape steady state from edge cleanup | bottleneck: Tail-handling overhead from generic code and excess synchronization

## Active direction

- selected direction: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`
