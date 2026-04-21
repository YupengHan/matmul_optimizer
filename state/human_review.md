# Human review queue

## Current workflow gate

- next node: `node_b`
- status: `paused_on_explicit_user_redirect`
- round loop: `single-run` with `90` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_125336`
- diagnosis status: `awaiting_codex`
- recommended direction: `None`
- approved direction: `None`
- diagnosis notes: `Paused on explicit user redirect after node_b context prep. Resume by filling exactly three directions for run 20260421_124420_bf16_gemm_v1_fc400df, then run node_b --finalize. Frontier was led by diagnosis_20260421_013125:dir_02 (restore exact 489574e surface), while the low-register writer family remains strategically important.`
- dir_01: PENDING | bottleneck: PENDING
- dir_02: PENDING | bottleneck: PENDING
- dir_03: PENDING | bottleneck: PENDING

## Active direction

- selected direction: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve, use-recommended-direction, or select-next after node_b.`
