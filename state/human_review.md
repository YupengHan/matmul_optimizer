# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 2/20` with `19` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_220312`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 2/20 human-review audit: the queue still contributes only the approval gate and the exactly-one-direction rule, with no extra user-authored family to prioritize. The just-finished round reopened the PTX one-k 128x128 control branch and turned it into the new accepted base at 24.419329 ms, which now beats the recorded CUTLASS baseline. Because that family already validated strongly, the best next use of the round budget is an orthogonal family test rather than another immediate local nibble on the same branch. Accepted as the primary family for this diagnosis is the existing 256x128 pivot hot-band kernel, because the hot-band wall is still 32.687232 ms with 200 registers per thread and only 16.62% active warps. Deferred fallback families are a bounded PTX-local exploit pass and a light traversal/locality retune on the current 128x128 PTX grid. Rejected again for this round are the standard one-k copy-cadence family, the two-K stage-deepening path, and the stale full-band 64x384 route.`
- dir_01: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: Hot-band CTA geometry and block-count overhead on the current 128x128 PTX base, rather than a remaining local control-path bubble inside the winning branch.
- dir_02: Retune The Active PTX One-K 128x128 Hot-Band Control Path | bottleneck: Residual control-path overhead and live-range pressure inside the winning PTX one-k 128x128 hot-band branch.
- dir_03: Retune Hot-Band CTA Traversal On The 128x128 PTX Grid | bottleneck: Inter-CTA locality and traversal efficiency on the current 128x128 PTX hot-band grid.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
