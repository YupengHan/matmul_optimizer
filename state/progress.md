# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `48ee4f9bb82099f9dee321757edcdb92828cd707`
- plateau counter: `37`
- round loop: `round 12/17`
- rounds remaining: `6`
- notes: `Node C build succeeded for round 12/17. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_163016_bf16_gemm_v1_48ee4f9`
- run dir: `runs/20260420_163016_bf16_gemm_v1_48ee4f9`
- correctness: `PASS`
- median runtime: `25.406448 ms`
- TFLOP/s: `28.615547 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_163042`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 12/17 diagnosis for run 20260420_163016_bf16_gemm_v1_48ee4f9. Human-review mapping for this round: keep the non-PTX 128x128 control closed after its clear DRAM regression, and keep deeper export cleanup plus reopened prefetch closed. The fresh evidence is that the grouping family is the only family still moving in the right direction on top of the accepted export base: the 4-row window brought runtime down to 25.40644836 ms with correctness intact and long-scoreboard down to 6.14, materially better than the earlier 5-row and 6-row variants. No new explicit human idea family is queued in state/human_review.md, so the ranking stays narrow: accept one more grouping-window retune at 2 rows, defer the older 64x384 control as the broader fallback, and keep the hot-band / peeled seam only as a tertiary bounded option.`
- dir_01: Tighten PTX Hot-Band Grouping Further To A 2-Row Window | bottleneck: Residual CTA grouping and orchestration overhead around the PTX hot-band grouped-row mapping.
- dir_02: Reopen The Measured 64x384 Fixed-Main-Tile Control Path | bottleneck: Broader hot-band path selection and arithmetic-intensity tradeoff rather than PTX helper overhead.
- dir_03: Freeze PTX Grouping And Probe Only The Hot-Band / Peeled Seam | bottleneck: Boundary and launch split cost between the PTX hot-band kernel and the peeled 384-row row-band path.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
