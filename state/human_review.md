# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 13/17` with `5` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_163231`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 13/17 diagnosis for run 20260420_163143_bf16_gemm_v1_6821ef5. Human-review mapping for this round: keep non-PTX 128x128, reopened prefetch-handoff, and deeper export cleanup closed, and now mostly close the grouping family too. The fresh evidence is that 4 rows was the best member of the grouping family on top of the accepted export base, while 2 rows regressed back to 26.06694412 ms and raised DRAM to 21.47. That means the grouping family has likely plateaued below the accepted base. No new explicit human idea family is queued in state/human_review.md, so the ranking shifts to the remaining measured control paths: accept the older 64x384 fixed-main-tile control first, keep the hot-band / peeled seam as the next bounded launch-path fallback, and retain the 4-row grouping only as a last PTX retry if the broader controls are worse.`
- dir_01: Reopen The Measured 64x384 Fixed-Main-Tile Control Path | bottleneck: Broader hot-band path selection and arithmetic-intensity tradeoff rather than PTX helper overhead.
- dir_02: Probe Only The Hot-Band / Peeled Seam | bottleneck: Boundary and launch split cost between the PTX hot-band kernel and the peeled 384-row row-band path.
- dir_03: Keep The 4-Row PTX Grouping As The Last PTX Retry | bottleneck: Residual CTA grouping and orchestration overhead around the PTX hot-band grouped-row mapping.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
