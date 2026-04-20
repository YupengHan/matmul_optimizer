# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `c3f11c31cb51d8199d308580575f3aff7ac381c1`
- plateau counter: `33`
- round loop: `round 8/17`
- rounds remaining: `10`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 8/17.`

## Latest measured custom run

- run id: `20260420_160517_bf16_gemm_v1_c3f11c3`
- run dir: `runs/20260420_160517_bf16_gemm_v1_c3f11c3`
- correctness: `PASS`
- median runtime: `24.845824 ms`
- TFLOP/s: `29.261232 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_160556`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 8/17 diagnosis for run 20260420_160517_bf16_gemm_v1_c3f11c3. Human-review mapping for this round: keep the immediate prefetch-handoff, expanded B-shared-skew, grouped-row-window, and broader default-promotion reopenings closed. Round 7 established a new accepted base at 24.84582424 ms with correctness intact, DRAM down to 11.33, and long-scoreboard down to 7.26 after a minimal PTX export-address cleanup, so the export family is still the only live family with fresh positive measured evidence. No new explicit human idea family is queued in state/human_review.md, so the ranking is: accept one more narrow export-helper cleanup first, keep the older-but-measured 64x384 control as the secondary fallback, and leave the non-PTX 128x128 sibling as a tertiary control only if the export family stalls.`
- dir_01: Continue The Narrow PTX Export Cleanup In The Row-Pair Helper | bottleneck: Residual row-pair export helper setup and sync cadence inside the PTX store path.
- dir_02: Reopen The Measured 64x384 Fixed-Main-Tile Control Path | bottleneck: Broader hot-band path selection and arithmetic-intensity tradeoff rather than PTX helper overhead.
- dir_03: Use The Non-PTX 128x128 Sibling As A Control | bottleneck: PTX-specific export/store complexity versus the simpler non-PTX 128x128 sibling.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
