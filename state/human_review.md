# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 12/17` with `6` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_163042`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 12/17 diagnosis for run 20260420_163016_bf16_gemm_v1_48ee4f9. Human-review mapping for this round: keep the non-PTX 128x128 control closed after its clear DRAM regression, and keep deeper export cleanup plus reopened prefetch closed. The fresh evidence is that the grouping family is the only family still moving in the right direction on top of the accepted export base: the 4-row window brought runtime down to 25.40644836 ms with correctness intact and long-scoreboard down to 6.14, materially better than the earlier 5-row and 6-row variants. No new explicit human idea family is queued in state/human_review.md, so the ranking stays narrow: accept one more grouping-window retune at 2 rows, defer the older 64x384 control as the broader fallback, and keep the hot-band / peeled seam only as a tertiary bounded option.`
- dir_01: Tighten PTX Hot-Band Grouping Further To A 2-Row Window | bottleneck: Residual CTA grouping and orchestration overhead around the PTX hot-band grouped-row mapping.
- dir_02: Reopen The Measured 64x384 Fixed-Main-Tile Control Path | bottleneck: Broader hot-band path selection and arithmetic-intensity tradeoff rather than PTX helper overhead.
- dir_03: Freeze PTX Grouping And Probe Only The Hot-Band / Peeled Seam | bottleneck: Boundary and launch split cost between the PTX hot-band kernel and the peeled 384-row row-band path.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
