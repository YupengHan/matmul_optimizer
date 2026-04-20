# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 14/17` with `4` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_163459`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 14/17 diagnosis for run 20260420_163357_bf16_gemm_v1_a64854a. Human-review mapping for this round: keep the 64x384 control closed after its catastrophic regression, and keep non-PTX 128x128 plus deeper export cleanup closed as well. The new evidence is decisive: the broad 64x384 path drove runtime to 33.9645443 ms, DRAM to 55.24, and barrier to 17.01, so the remaining search needs to stay inside the accepted default PTX launch rather than reopen broad alternate paths. No new explicit human idea family is queued in state/human_review.md, so the ranking narrows to the seam and residual PTX families: accept a one-block downward seam shift first, keep the 4-row grouping as the last PTX retry, and leave prefetch only as a tertiary scoreboard tradeoff if the cleaner options fail.`
- dir_01: Shift The Hot-Band / Peeled Seam Down By One PTX Block | bottleneck: Boundary and launch split cost between the PTX hot-band kernel and the peeled 384-row row-band path.
- dir_02: Keep The 4-Row PTX Grouping As The Last PTX Retry | bottleneck: Residual CTA grouping and orchestration overhead around the PTX hot-band grouped-row mapping.
- dir_03: Retry PTX Prefetch Only As A Last Scoreboard Tradeoff | bottleneck: Copy-pipeline handoff timing and future-tile refill cadence in the PTX hot-band steady-state loop.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
