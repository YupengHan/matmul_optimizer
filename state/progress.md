# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `bbcc928d6298d5a0483248e079094b06db6afc4c`
- plateau counter: `35`
- round loop: `round 10/17`
- rounds remaining: `8`
- notes: `Node C build succeeded for round 10/17. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_162425_bf16_gemm_v1_bbcc928`
- run dir: `runs/20260420_162425_bf16_gemm_v1_bbcc928`
- correctness: `PASS`
- median runtime: `25.676785 ms`
- TFLOP/s: `28.314270 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_162446`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 10/17 diagnosis for run 20260420_162425_bf16_gemm_v1_bbcc928. Human-review mapping for this round: keep the deeper export cleanup from round 8 closed, and now also close the reopened PTX prefetch-handoff family after round 9/17. The new evidence is that the narrower future-refill retime reduced long-scoreboard to 6.58 and DRAM to 11.44, but it still lost to the accepted base because barrier rose to 6.68 and total runtime stayed at 25.67678452 ms. No new explicit human idea family is queued in state/human_review.md, so the ranking now shifts away from more PTX micro-adjustments: accept the non-PTX 128x128 sibling as the next control path, defer the older-but-measured 64x384 control as the broader fallback, and keep grouping/orchestration only as a tertiary PTX-adjacent retry if the cleaner controls also stall.`
- dir_01: Use The Non-PTX 128x128 Sibling As The Next Control Path | bottleneck: PTX-specific export/store and refill interaction versus the simpler non-PTX 128x128 sibling path.
- dir_02: Reopen The Measured 64x384 Fixed-Main-Tile Control Path | bottleneck: Broader hot-band path selection and arithmetic-intensity tradeoff rather than PTX helper overhead.
- dir_03: Retry Grouping / Orchestration Only If Control Paths Stall | bottleneck: CTA grouping and orchestration overhead around the PTX hot-band grouped-row mapping.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
