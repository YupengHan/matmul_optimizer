# Human review queue

## Current workflow gate

- next node: `node_b`
- status: `ready_for_node_b`
- round loop: `round 84/100` with `17` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `None`
- diagnosis status: `pending_generation`
- recommended direction: `None`
- approved direction: `None`
- diagnosis notes: `Run node_b to produce exactly three directions from the latest measured run.`
- no diagnosis recorded yet; run node_b first

## Active direction

- selected direction: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`

## Persisted experience for the next session

- current best active reference in this environment: `20260420_115626_bf16_gemm_v1_469a12b` at `25.643007 ms`
- historical best recorded custom run still matters as the long-term target anchor: `20260420_084915_bf16_gemm_v1_4e5579e` at `24.570881 ms`
- use the active `25.643007 ms` run as the immediate comparison anchor for node_b ranking in the next session
- do not re-rank pure baseline-restore work near the top unless there is a concrete new explanation for why it would behave differently

## Families to avoid reopening casually

- broad default hot-band promotion away from the PTX microkernel
- reason: `64x384` default -> `33.594879 ms`, `256x128` default -> `31.867904 ms`
- staged `128x128x32` K32 family
- reason: `31.552928 ms`
- paired PTX export-lifetime helper
- reason: `25.837568 ms` and worse `long_scoreboard`
- PTX grouped-row narrowing from `8` to `4`
- reason: `25.944464 ms`, essentially flat-to-negative
- PTX helper flattening without a new codegen hypothesis
- reason: prior attempt was effectively a no-op

## What still looks live

- narrow PTX-adjacent ideas that reduce `long_scoreboard` without pushing DRAM back up
- very small export / feed / orchestration experiments on top of the zero-padding PTX baseline
- if node_b wants a control family, keep it bounded and compare against `25.643007 ms`, not just the latest regressed round
