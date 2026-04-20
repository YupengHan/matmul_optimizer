# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 2/50` with `49` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_223724`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 2/50 starts from a neutral export rewrite. The hot-band kernel remained essentially unchanged at about 41.10 ms while end-to-end runtime regressed, so the best next move is not more export work. Recommended direction dir_01 returns to the user-provided bank-conflict family with the smallest viable layout change: increase the hot-band B shared-memory skew from +8 elements to +16 elements while leaving tile shape, stage depth, and consumer order untouched. Dir_02 is the restore fallback if that padding is neutral or negative, and dir_03 explicitly defers more export work until the bank-layout side has been re-tested.`
- dir_01: Human idea bank conflict: increase the hot-band B shared-memory padding from +8 to +16 elements | bottleneck: Residual B-side shared-memory bank behavior in the hot-band WMMA/PTX consumer path.
- dir_02: Restore-only fallback if the larger B padding regresses | bottleneck: Not a direct bottleneck attack; this is the restore path after a footprint-only experiment.
- dir_03: Later: revisit export path only if bank padding gives a measurable signal | bottleneck: Secondary export-side overhead after the operand-delivery path is re-tuned.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
