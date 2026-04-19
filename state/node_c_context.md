# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Rewrite the steady-state tile around BF16 Tensor Cores`
- selection mode: `approved`
- source diagnosis id: `diagnosis_20260418_194629`
- round loop: `single-run`
- hypothesis: `The current kernel is a 16x16 scalar FP32-FMA tiled GEMM that converts BF16 inputs to float on load and never issues Tensor Core MMA instructions. With tensor pipe activity at 0 and the kernel still over 30x slower than the CUTLASS baseline, the dominant bottleneck is instruction mix and compute-path selection rather than small launch tuning. Replacing the hot loop with a warp-level BF16 Tensor Core microkernel should deliver the largest single-step upside.`
- expected bottleneck: `Tensor Core under-utilization`
- code locations: `src/kernels/bf16_gemm_v1.cu::bf16_gemm_v1_kernel, src/kernels/bf16_gemm_v1.cu::launch_bf16_gemm_v1`
- risk: `Moderate: this is a structural rewrite of the inner kernel, so fragment layout, accumulator mapping, and the BF16 epilogue all need fresh correctness validation.`
- metrics to re-check: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__throughput.avg.pct_of_peak_sustained_elapsed, median_runtime_ms, tflops`

## Allowed edit surface

- `src/kernels/*`
- `src/runner/main.cpp` when the direction requires runner glue
- `include/*` when a stable interface change is required
- `CMakeLists.txt` only if the build path genuinely needs it

## Required commands

- edit code for one direction only
- then run `python scripts/graph.py node_c --finalize`
- default behavior after a successful node_c finalize is to auto-run node_a

## Dirty working tree snapshot before node_c finalize

- no tracked dirty paths at prepare time
