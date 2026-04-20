# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 15/17` with `3` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_163723`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 15/17 diagnosis for run 20260420_163637_bf16_gemm_v1_81bde72. Human-review mapping for this round: keep the broad 64x384 control closed, keep non-PTX 128x128 closed, and keep deeper export cleanup closed. The fresh evidence is that the seam family is the cleanest remaining direction after the broad controls failed: shifting the pivot from 6400 to 6144 recovered the runtime to 25.65470409 ms with DRAM held to 11.25 and long-scoreboard at 5.91. No new explicit human idea family is queued in state/human_review.md, so the ranking now stays narrow for the last rounds: accept one more seam shift first, keep the 4-row grouping as the secondary PTX fallback, and leave prefetch only as a tertiary scoreboard tradeoff.`
- dir_01: Shift The Hot-Band / Peeled Seam Down One More 256-Row Chunk | bottleneck: Boundary and launch split cost between the PTX hot-band kernel and the peeled 384-row row-band path.
- dir_02: Keep The 4-Row PTX Grouping As The Last PTX Retry | bottleneck: Residual CTA grouping and orchestration overhead around the PTX hot-band grouped-row mapping.
- dir_03: Retry PTX Prefetch Only As A Final Scoreboard Tradeoff | bottleneck: Copy-pipeline handoff timing and future-tile refill cadence in the PTX hot-band steady-state loop.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
