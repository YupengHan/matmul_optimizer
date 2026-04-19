# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 18/20` with `3` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_011317`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `dir_01`
- diagnosis notes: `Human-in-loop round: skip node_b diagnosis and run a fixed-shape tiling autotune sweep over 10+ candidate main widths, then preserve the results for later node_b use.`
- dir_01: Human idea: autotune fixed-shape main tiling across 10+ candidates | bottleneck: Search-space blindness rather than a single micro-bottleneck: we need real timing data for multiple tile widths to understand the trade between CTA count, DRAM pressure, MIO throttle, and register pressure.
- dir_02: Fallback: keep the current 64x192 main + 64x128 middle + 64x96 tail | bottleneck: No new hypothesis; this is a stability fallback while preserving the current best measured result.
- dir_03: Follow-up after sweep: promote a super-main width if the timing curve keeps improving | bottleneck: Potential remaining CTA-count overhead in the hot band if the timing curve continues improving as width grows.

## Active direction

- selected direction: `dir_01`
- selection mode: `human_idea`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
