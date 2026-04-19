# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Replace the simple B-row skew with a warp-friendly shared-memory B swizzle`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260418_225935`
- round loop: `round 6/20`
- hypothesis: `The round 5 retile already pushed the kernel up to its current shared-memory occupancy ceiling: NCU reports 7 theoretical CTAs per SM from shared memory, 28 maximum warps per active cycle, and 58.03% active warps, so another occupancy-only tweak is no longer the first-order move. The remaining dominant stall is MIO throttle at 33.09%, and the detailed CSV still shows heavy LSU/L1 activity from the steady-state load path (`l1tex__data_pipe_lsu_wavefronts` 66.09%, `l1tex__data_bank_reads` 13.55%). Each warp still issues three `matrix_b` fragment loads per K-step from a row-major shared tile with only a +8-element skew, so a stronger B-side swizzle or permuted staging layout is the most direct way to reduce shared-load pressure and feed Tensor Cores more consistently.`
- expected bottleneck: `Shared-memory and MIO pressure on the B fragment load path inside the steady-state tensor loop`
- code locations: `src/kernels/bf16_gemm_v1.cu:36-44 (`kBSharedStride`, `kBSharedTileElems`, and B staging shape constants), src/kernels/bf16_gemm_v1.cu:91-102 (`stage_b_shared_tile_async`), src/kernels/bf16_gemm_v1.cu:204-211 (B shared pointer setup and `wmma::load_matrix_sync` for `b_frags`)`
- risk: `Moderate. The B layout change must preserve 16-byte `cp.async` alignment and the current WMMA row-major semantics; a swizzle that helps the warp-load pattern can still make staging math or correctness more fragile.`
- metrics to re-check: `median_runtime_ms, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, l1tex__data_pipe_lsu_wavefronts.avg.pct_of_peak_sustained_elapsed, l1tex__data_bank_reads.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, correctness_passed`

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
