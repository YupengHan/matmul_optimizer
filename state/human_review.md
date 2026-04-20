# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 9/17` with `9` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_160829`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 9/17 diagnosis for run 20260420_160736_bf16_gemm_v1_d8e9048. Human-review mapping for this round: keep the deeper export cleanup from round 8 closed, and continue to keep the expanded B-shared-skew and grouped-row-window families closed after their measured losses. The key new evidence is that round 7 established a new accepted base at 24.84582424 ms with the minimal export-address cleanup, while round 8 showed that pushing the row-pair export cleanup further regressed sharply to 25.95990372. That means the export family is no longer the best immediate lever beyond the accepted base. No new explicit human idea family is queued in state/human_review.md, so the ranking now shifts to: accept a narrower PTX prefetch-handoff retime on top of the new accepted export base, defer the older-but-measured 64x384 control as the main broader fallback, and keep the non-PTX 128x128 sibling as a tertiary control path.`
- dir_01: Reopen PTX Prefetch Handoff On Top Of The New Export Base | bottleneck: Copy-pipeline handoff timing and future-tile refill cadence in the PTX hot-band steady-state loop.
- dir_02: Reopen The Measured 64x384 Fixed-Main-Tile Control Path | bottleneck: Broader hot-band path selection and arithmetic-intensity tradeoff rather than PTX helper overhead.
- dir_03: Use The Non-PTX 128x128 Sibling As A Control | bottleneck: PTX-specific export/store and prefetch orchestration versus the simpler non-PTX 128x128 sibling.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
