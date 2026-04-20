# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 16/17` with `2` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_163934`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 16/17 diagnosis for run 20260420_163839_bf16_gemm_v1_fcc145b. Human-review mapping for this round: keep the broad 64x384 control and non-PTX 128x128 control closed, and now also stop line-searching deeper into the seam family because 5888 regressed relative to the 6144 pivot. The fresh evidence is that the seam family has a local best already, while the accepted export base still has one meaningful untested prefetch variant left: the full A-before-B retime across both prime and refill. No new explicit human idea family is queued in state/human_review.md, so the ranking for the penultimate round is: accept the full prefetch retime first, keep the 4-row grouping as the best measured PTX fallback, and retain the 6144 seam only as the best measured launch-split fallback.`
- dir_01: Apply The Full PTX Prefetch Retime On The Accepted Export Base | bottleneck: Copy-pipeline handoff timing across both the initial stage prime and the future-tile refill in the PTX hot-band steady-state loop.
- dir_02: Keep The 4-Row PTX Grouping As The Best Measured PTX Fallback | bottleneck: Residual CTA grouping and orchestration overhead around the PTX hot-band grouped-row mapping.
- dir_03: Hold The 6144 Seam Variant As The Best Launch-Split Fallback | bottleneck: Boundary and launch split cost between the PTX hot-band kernel and the peeled 384-row row-band path.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
