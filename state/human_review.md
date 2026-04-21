# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 4/20` with `17` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_221111`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 4/20 human-review audit: the queue still contributes only the approval gate and exactly-one-direction rule. The current PTX exploit family just produced the new best custom run at 24.177664 ms, but the NCU signature stayed almost unchanged, which argues against immediately spending another round on the same class of PTX control tweak. Accepted as the primary family for this diagnosis is therefore the cheap grouped-CTA traversal/locality probe on the 128x128 PTX grid. Deferred fallback families are another bounded PTX exploit pass and a reopen of the prior PTX baseline as an A/B guardrail. The failed 256x128 pivot family remains rejected for this round.`
- dir_01: Retune Hot-Band CTA Traversal On The 128x128 PTX Grid | bottleneck: Inter-CTA locality and traversal efficiency on the current 128x128 PTX hot-band grid under low occupancy.
- dir_02: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual PTX control-path overhead in the current one-k 128x128 hot-band branch.
- dir_03: Reopen The Prior PTX One-K 128x128 Control Branch For A/B Guardrail | bottleneck: Not a new bottleneck attack; this is the PTX-family A/B restore guardrail.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
