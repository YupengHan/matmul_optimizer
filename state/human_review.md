# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 3/20` with `18` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_220747`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 3/20 human-review audit: the queue still contributes only the approval gate and the exactly-one-direction rule. The last round cleanly falsified the 256x128 pivot family as the current primary bet: it regressed to 30.286848 ms and slowed the hot-band kernel to 43.291456 ms. The search should therefore return to the accepted PTX base rather than compounding that loss with another broad family swing. Accepted as the primary family for this diagnosis is a bounded exploit pass on the active PTX one-k 128x128 control path. Deferred fallback families are the light traversal/locality retune on the PTX grid and the explicit restore to the accepted PTX branch. Rejected for this round are reusing the failed 256x128 pivot as primary, reopening the earlier standard one-k copy-cadence family, and reopening the K32 stage-deepening branch.`
- dir_01: Retune The Active PTX One-K 128x128 Hot-Band Control Path | bottleneck: Residual control-path overhead and live-range pressure inside the accepted PTX one-k 128x128 hot-band branch.
- dir_02: Retune Hot-Band CTA Traversal On The 128x128 PTX Grid | bottleneck: Inter-CTA locality and traversal efficiency on the current 128x128 PTX hot-band grid.
- dir_03: Restore The Accepted PTX One-K 128x128 Base | bottleneck: Not a new bottleneck attack; this is the recovery path back to the accepted PTX base after the failed 256x128 excursion.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
