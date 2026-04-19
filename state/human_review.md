# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 16/20` with `5` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_005301`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Aggressive widened-main follow-up informed by the round-14 human-in-loop signal and the round-15 retile failure.`
- dir_01: 64x160 main + 64x96 tail widened fixed split | bottleneck: Main-path operand movement and memory traffic from the too-narrow round-15 split; a 64x160 steady-state should improve reuse and reduce launch pressure without reopening generic tail overhead.
- dir_02: 64x192 main + 64x128 middle + 64x96 tail hierarchy | bottleneck: Hot-band CTA overpopulation and DRAM pressure on the first 7680 columns, with the middle 384-column strip isolated so the super-wide main kernel does not pay for remainder handling in its steady-state loop.
- dir_03: 64x256 super-main with small cleanup launches | bottleneck: The current hot path is probably paying too much per-CTA overhead and rereading too much B data for the fixed width; a 64x256 super-main is a deliberate attempt to trade much fewer CTAs for much higher per-CTA reuse, at the risk of turning register/shared pressure into the new limiter.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
