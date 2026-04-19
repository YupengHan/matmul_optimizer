# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Micro-retune the single-level B skew in the peeled 64x384 hot kernel`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_104652`
- round loop: `round 4/5`
- hypothesis: `8346b48 is the new best base because the pairwise peeled hot loop raised tensor active to 35.06 without increasing register pressure beyond 128/thread or breaking the 2-block register occupancy limit. The next visible limiter is no longer synchronization but shared-memory / LSU feed pressure: hot-kernel mio_throttle climbed to 35.58, l1tex data-bank reads rose to 12.15, and lsuin_requests reached 83.68 while active warps stayed flat at 33.07. The coherent next move is a tiny single-level mapping retune inside the existing B shared layout, such as adjusting the warp-group skew or logical-to-shared column mapping, while explicitly avoiding the previously regressive two-level repack and named-barrier handoff families.`
- expected bottleneck: `Shared-memory B-fragment load pressure and bank behavior in the 64x384 hot kernel, expressed as high mio_throttle and LSU issue pressure rather than low occupancy.`
- code locations: `src/kernels/bf16_gemm_v1.cu:48-53, src/kernels/bf16_gemm_v1.cu:231-263, src/kernels/bf16_gemm_v1.cu:535-556, src/kernels/bf16_gemm_v1.cu:619-620`
- risk: `Feed-path rewrites have a bad track record in this search. This must stay at the level of one skew or mapping tweak inside the current single-stage layout; if it turns into a broader B repack or new handoff scheme, it is repeating disproven ground.`
- metrics to re-check: `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, l1tex__data_bank_reads.avg.pct_of_peak_sustained_elapsed, l1tex__data_pipe_lsu_wavefronts.avg.pct_of_peak_sustained_elapsed, l1tex__lsuin_requests.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, median runtime`

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

- `src/kernels/bf16_gemm_v1.cu`
