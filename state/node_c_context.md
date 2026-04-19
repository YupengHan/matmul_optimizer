# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Two-level B staging for the 64x384 hot band`
- selection mode: `human_idea`
- source diagnosis id: `diagnosis_20260419_092350`
- round loop: `round 1/5`
- hypothesis: `The promoted 64x384 path already wins on CTA count, but the B feed still uses one row-major shared layout plus a single 16-byte warp-group skew. On the measured 64x384 kernel, mio_throttle is 31.60%, l1tex LSU wavefront pressure is high, and tensor active is only 32.61%, which points to the current B producer and consumer layout serving neither cp.async/coalescing nor warp consumption especially well. Keep the 64x384 outer tile, but split global->shared and shared->fragment into separate layouts via a CTA-local reorder or an interleaved swizzle so producer traffic and consumer bank behavior are optimized independently.`
- expected bottleneck: `Shared/L1 B-feed pressure and LSU issue bandwidth in the hot 64x384 kernel.`
- code locations: `src/kernels/bf16_gemm_v1.cu:47-52 (current single-skew B shared layout in TensorCoreTileConfig), src/kernels/bf16_gemm_v1.cu:208-239 (logical-to-shared B mapping and async staging path), src/kernels/bf16_gemm_v1.cu:437-445 (warp B base pointer selection and per-fragment shared loads)`
- risk: `A two-level B layout can add address math, extra shared traffic, or enough staging footprint to offset the gain if the reorder is not kept local and cheap.`
- metrics to re-check: `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, l1tex__data_bank_reads.avg.pct_of_peak_sustained_elapsed, l1tex__data_bank_writes.avg.pct_of_peak_sustained_elapsed, l1tex__lsuin_requests.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
