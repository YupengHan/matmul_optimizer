# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `0ac7611b334ecc5aed0106a24dfae3c2125360d8`
- plateau counter: `3`
- round loop: `round 14/20`
- rounds remaining: `7`
- notes: `Node C build succeeded for round 14/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_002954_bf16_gemm_v1_0ac7611`
- run dir: `runs/20260419_002954_bf16_gemm_v1_0ac7611`
- correctness: `PASS`
- median runtime: `65.610237 ms`
- TFLOP/s: `11.080884 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_003032`
- recommended direction: `dir_01`
- approved direction: `dir_01`
- diagnosis notes: `Human-in-loop round: skip automatic node_b direction selection and prioritize the user-requested vectorization + thread-coarsening path for high MIO throttle.`
- dir_01: Human idea: vectorize transfers and thread-coarsen the load/store path | bottleneck: MIO throttle and LSU pressure from too many narrow load/store instructions in the hot path and epilogue.
- dir_02: Replace WMMA fragment loads with an explicit tensor feed pipeline | bottleneck: Tensor-core underfeed from the fragment delivery path, expressed as high MIO throttle and oversized LSU wavefront pressure before each MMA issue window.
- dir_03: Retile the CTA and cut per-warp output ownership | bottleneck: Per-warp fragment/accumulator footprint and issue inefficiency from the current 4x2 warp layout plus wide N-side ownership.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `human_idea`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `17.779776 ms`, `1.686004x` slower than CUTLASS
