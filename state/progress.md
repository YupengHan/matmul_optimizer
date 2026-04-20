# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `b50742ed0692244d8e518dccedae3d255d61b85c`
- plateau counter: `5`
- round loop: `round 6/50`
- rounds remaining: `45`
- notes: `Node C build succeeded for round 6/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_225909_bf16_gemm_v1_b50742e`
- run dir: `runs/20260419_225909_bf16_gemm_v1_b50742e`
- correctness: `FAIL`
- median runtime: `30.012527 ms`
- TFLOP/s: `24.223865 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_225949`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 6/50 still shows an incorrect but faster peeled steady-state: the main 256x128 hot-band kernel improved again to about 40.131 ms, which strengthens the case that the control-flow idea is sound but the shared peeled schedule is not safe across both tile configs. The recommended next move is therefore dir_01: split the behavior by TileConfig and keep the peeled schedule only on the dominant 8-warp main hot band while restoring the residual 64x128 path to the proven generic loop.`
- dir_01: Apply peeled steady-state only to the 8-warp 256x128 hot band and leave the residual 64x128 path on the proven generic loop | bottleneck: Main hot-band control overhead is still the target, but correctness risk is likely concentrated in the smaller residual 64x128 variant rather than the dominant 256x128 kernel.
- dir_02: Re-anchor on the accepted-correct surface and push warp-local Ps2r plus right-left register reuse | bottleneck: Per-warp operand delivery and register reuse inside the 64x64 PTX microkernel.
- dir_03: Revisit a light L2-friendly logical CTA swizzle after the correctness branch settles | bottleneck: Inter-CTA L2 locality across hot-band B tiles.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.407935 ms`, `1.131490x` slower than CUTLASS
