# Human review queue

## Current workflow gate

- next node: `node_b`
- status: `node_b_context_ready`
- round loop: `round 7/20` with `14` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction
- active user goal: push this hardware and workflow toward `20 ms`, not merely a local win over the current accepted base
- exploration policy from the user: a promising direction family may run for multiple rounds; do not assume one round per family and do not force an immediate revert after a single bad step if the family still shows signal or ceiling

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_174713`
- diagnosis status: `awaiting_codex`
- recommended direction: `None`
- approved direction: `None`
- diagnosis notes: `Run node_b to produce exactly three ranked directions.`
- dir_01: PENDING | bottleneck: PENDING
- dir_02: PENDING | bottleneck: PENDING
- dir_03: PENDING | bottleneck: PENDING

## Active direction

- selected direction: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`
