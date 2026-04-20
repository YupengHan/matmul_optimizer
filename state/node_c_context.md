# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `PTX hot-band consume retime`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_083324`
- round loop: `round 55/100`
- hypothesis: `Warmup cp.async ordering is no longer the primary lever. With tensor active at 48.28, warps active at 16.57, barrier at 6.42, mio at 4.22, short scoreboard at 3.02, dram at 9.78, and lts at 30.67 on run 20260420_083244_bf16_gemm_v1_66273be (24.896433 ms), the next gain is a consumer-side retime at the PTX microkernel boundary: sweep the PTX-hot-band-local column order and lane consume order to improve register reuse and reduce bank conflict pressure instead of changing macro tiling or adding CTA repack.`
- expected bottleneck: `PTX hot-band consumer ordering is leaving register reuse and shared-memory bank behavior suboptimal after the producer side has already been tuned.`
- code locations: `src/kernels/bf16_gemm_v1.cu::PtxWmmaMirroredTileIndex64x64, src/kernels/bf16_gemm_v1.cu::PTX hot-band accumulate helper, src/kernels/bf16_gemm_v1.cu::PTX hot-band load helper`
- risk: `Moderate. The retime may only reshuffle latency exposure without changing steady-state throughput if the hot band is already consumer-bound.`
- metrics to re-check: `tensor_active, warps_active, barrier, mio, short_scoreboard, dram, lts`

## Allowed edit surface

- `src/kernels/*`
- `src/runner/main.cpp` when the direction requires runner glue
- `include/*` when a stable interface change is required
- `CMakeLists.txt` only if the build path genuinely needs it
- `scripts/graph.py` or `scripts/sweep_fixed_main_tiles.py` only when the direction requires minimal workflow glue

## Required commands

- edit code for one direction only
- then run `python scripts/graph.py node_c --finalize`
- default behavior after a successful node_c finalize is to auto-run node_a

## Dirty working tree snapshot before node_c finalize

- no tracked dirty paths at prepare time
