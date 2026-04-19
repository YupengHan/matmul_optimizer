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

- diagnosis id: `diagnosis_20260418_200741`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Add CTA-level shared-memory staging for WMMA tiles | bottleneck: Global-memory bound
- dir_02: Retune the WMMA tile hierarchy for more per-warp accumulation | bottleneck: Tensor Core under-utilization
- dir_03: Specialize the hot path to the fixed aligned benchmark shape | bottleneck: Tail-handling overhead from generic code

## Active direction

- selected direction: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`
