# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `6821ef5bfd8f089ea59938238f7d8375903a005e`
- plateau counter: `38`
- round loop: `round 13/17`
- rounds remaining: `5`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 13/17.`

## Latest measured custom run

- run id: `20260420_163143_bf16_gemm_v1_6821ef5`
- run dir: `runs/20260420_163143_bf16_gemm_v1_6821ef5`
- correctness: `PASS`
- median runtime: `26.066944 ms`
- TFLOP/s: `27.890474 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_163231`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 13/17 diagnosis for run 20260420_163143_bf16_gemm_v1_6821ef5. Human-review mapping for this round: keep non-PTX 128x128, reopened prefetch-handoff, and deeper export cleanup closed, and now mostly close the grouping family too. The fresh evidence is that 4 rows was the best member of the grouping family on top of the accepted export base, while 2 rows regressed back to 26.06694412 ms and raised DRAM to 21.47. That means the grouping family has likely plateaued below the accepted base. No new explicit human idea family is queued in state/human_review.md, so the ranking shifts to the remaining measured control paths: accept the older 64x384 fixed-main-tile control first, keep the hot-band / peeled seam as the next bounded launch-path fallback, and retain the 4-row grouping only as a last PTX retry if the broader controls are worse.`
- dir_01: Reopen The Measured 64x384 Fixed-Main-Tile Control Path | bottleneck: Broader hot-band path selection and arithmetic-intensity tradeoff rather than PTX helper overhead.
- dir_02: Probe Only The Hot-Band / Peeled Seam | bottleneck: Boundary and launch split cost between the PTX hot-band kernel and the peeled 384-row row-band path.
- dir_03: Keep The 4-Row PTX Grouping As The Last PTX Retry | bottleneck: Residual CTA grouping and orchestration overhead around the PTX hot-band grouped-row mapping.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
