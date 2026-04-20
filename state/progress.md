# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `212255834e8215f9f39a12cd699bfa87eb8fb458`
- plateau counter: `8`
- round loop: `round 9/50`
- rounds remaining: `42`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 9/50.`

## Latest measured custom run

- run id: `20260419_230631_bf16_gemm_v1_2122558`
- run dir: `runs/20260419_230631_bf16_gemm_v1_2122558`
- correctness: `PASS`
- median runtime: `30.363136 ms`
- TFLOP/s: `23.944148 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_230713`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 9/50 resumes forward optimization from a restored correct surface. The recommended next move is dir_01, which follows the human Ps2r idea on the A side while keeping control flow and CTA staging unchanged so the result stays easy to interpret.`
- dir_01: Keep the restored control flow and add A-side row-pair lookahead inside the 64x64 PTX microkernel | bottleneck: Warp-local shared-to-register latency on the A-fragment path inside the 64x64 PTX microkernel.
- dir_02: Keep the restored surface and test a light L2-friendly logical CTA swizzle | bottleneck: Inter-CTA L2 reuse across neighboring hot-band B tiles.
- dir_03: Try warp-specialized Pg2s staging on the restored surface without changing the tile shape | bottleneck: CTA-level staging orchestration and barrier dilution inside the hot-band loop.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.407935 ms`, `1.131490x` slower than CUTLASS
