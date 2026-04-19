# Human review queue

## Current workflow gate

- next node: `node_b`
- status: `node_b_context_ready`
- round loop: `single-run` with `0` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260418_174143`
- diagnosis status: `awaiting_codex`
- recommended direction: `None`
- approved direction: `None`
- dir_01: PENDING | bottleneck: PENDING
- dir_02: PENDING | bottleneck: PENDING
- dir_03: PENDING | bottleneck: PENDING

## Active direction

- selected direction: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`
