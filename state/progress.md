# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `948fc5c0301c8859a9885095e934be38c5a23240`
- plateau counter: `36`
- round loop: `round 11/17`
- rounds remaining: `7`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 11/17.`

## Latest measured custom run

- run id: `20260420_162632_bf16_gemm_v1_948fc5c`
- run dir: `runs/20260420_162632_bf16_gemm_v1_948fc5c`
- correctness: `PASS`
- median runtime: `26.704384 ms`
- TFLOP/s: `27.224722 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_162714`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 11/17 diagnosis for run 20260420_162632_bf16_gemm_v1_948fc5c. Human-review mapping for this round: keep the deeper export cleanup, reopened prefetch-handoff, and non-PTX 128x128 control all closed after their measured losses. The new evidence is especially clear for the non-PTX control: correctness stayed intact, but DRAM jumped to 34.17 and runtime regressed to 26.70438385 ms, so moving off the PTX microkernel is not the next win. No new explicit human idea family is queued in state/human_review.md, so the ranking now returns to the remaining bounded PTX-adjacent and launch-seam families: accept a grouping retry with a 4-row window on top of the accepted export base, defer the older 64x384 control as the broader fallback, and keep the hot-band / peeled seam only as a tertiary option.`
- dir_01: Retry PTX Hot-Band Grouping With A 4-Row Window | bottleneck: CTA grouping and orchestration overhead around the PTX hot-band grouped-row mapping.
- dir_02: Reopen The Measured 64x384 Fixed-Main-Tile Control Path | bottleneck: Broader hot-band path selection and arithmetic-intensity tradeoff rather than PTX helper overhead.
- dir_03: Freeze PTX Launch And Recheck Only The Peeled 384 Tail Split | bottleneck: Boundary and launch split cost between the PTX hot-band kernel and the peeled 384-row row-band path.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
