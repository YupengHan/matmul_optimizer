# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `a7d381754d2b7e09d1ea99275532f036dfd5fc81`
- plateau counter: `20`
- round loop: `round 79/100`
- rounds remaining: `22`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 79/100.`

## Latest measured custom run

- run id: `20260420_114346_bf16_gemm_v1_a7d3817`
- run dir: `runs/20260420_114346_bf16_gemm_v1_a7d3817`
- correctness: `PASS`
- median runtime: `31.552928 ms`
- TFLOP/s: `23.041266 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_114507`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 79/100 diagnosis for run 20260420_114346_bf16_gemm_v1_a7d3817. The staged K32 family is now explicitly closed-negative: the round-79 measurement regressed to 31.55292797 ms with tensor active 39.90, barrier 10.02, long scoreboard 5.76, mio 4.98, and dram 23.54. The restored PTX baseline from round 78 remains the current reference shape in this environment, but the source surface alone does not explain the slowdown back to 25.97375965 ms and should not be treated as an unresolved launch-path difference. Do not reopen the broad default-dispatch promotion family unless a concrete new hypothesis appears.`
- dir_01: Activate The Existing 128x128 Two-Stage Hot-Band Kernel | bottleneck: Residual synchronization and latency-hiding overhead in the hot-band steady state, with lower occupancy pressure than the failed K32 staging variant.
- dir_02: Trim PTX Export And Scratch Shape On The Restored Baseline | bottleneck: PTX epilogue overhead, register pressure around the export path, and secondary synchronization cost rather than raw tensor throughput.
- dir_03: Bound The 128x128 PTX Hot-Band Grouping Window | bottleneck: Group coordination and tail-peeled row-band overhead inside the PTX hot-band path, not the staged K32 pipeline itself.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
