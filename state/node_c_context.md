# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Add CTA-level shared-memory staging for WMMA tiles`
- selection mode: `approved`
- source diagnosis id: `diagnosis_20260418_200741`
- round loop: `single-run`
- hypothesis: `The new WMMA kernel moved math onto Tensor Cores, but each warp still loads its A and B fragments directly from global memory with no cross-warp reuse. The profile now looks memory-led: tensor pipe active is only 4.78%, DRAM/L2 throughput is much higher than SM throughput, and long scoreboard plus MIO throttle stalls dominate. A shared-memory staging path with CTA-level reuse, ideally double-buffered, is the highest-upside next step because it should turn repeated global fragment fetches into reused BF16 tiles that feed multiple warps.`
- expected bottleneck: `Global-memory bound`
- code locations: `src/kernels/bf16_gemm_v1.cu::bf16_gemm_v1_tensor_core_kernel, src/kernels/bf16_gemm_v1.cu::launch_bf16_gemm_v1`
- risk: `Moderate to high: shared-memory layout, load choreography, and WMMA-compatible tile packing all become more complex, and a bad layout can trade one memory bottleneck for another.`
- metrics to re-check: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, dram__throughput.avg.pct_of_peak_sustained_elapsed, median_runtime_ms`

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

- `src/kernels/bf16_gemm_v1.cu`
