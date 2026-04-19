# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Widen the async staging path to 16-byte fixed-tile copies`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260418_220408`
- round loop: `round 1/20`
- hypothesis: `The restored round-4 kernel keeps the good 2-warp, 2-output-fragment shape, but it still stages every A/B tile with 8-byte `cp.async` operations plus generic row and column address math. For this fixed shape, both source strides and tile origins are 16-byte aligned, so specializing the copy path to 16-byte moves should roughly halve the staging instruction count, reduce the dominant 39.12% `smsp__warp_issue_stalled_mio_throttle`, and leave more issue bandwidth for `wmma::load_matrix_sync` and MMA.`
- expected bottleneck: `Global-to-shared staging instruction pressure and MIO throttling from the current 8-byte async copy path, not a pure DRAM bandwidth ceiling.`
- code locations: `src/kernels/bf16_gemm_v1.cu:30-39 (`kAsyncCopyElems` / `cp_async_copy_8_bytes`), src/kernels/bf16_gemm_v1.cu:58-69 (`stage_shared_tile_async` generic copy loop), src/kernels/bf16_gemm_v1.cu:150-169 (A/B warm-up and steady-state staging sites)`
- risk: `Low to moderate. The shape and strides are favorable for 16-byte copies, but the implementation must preserve alignment for both A and B tiles and avoid reintroducing scalar fallback code that erases the instruction-count win.`
- metrics to re-check: `median runtime_ms, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed, dram__throughput.avg.pct_of_peak_sustained_elapsed, correctness cases`

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
