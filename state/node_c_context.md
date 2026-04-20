# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 7 Register reuse: replace the full 64x64 accumulator set with two serial 64x32 half-panel passes`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_191757`
- round loop: `round 16/20`
- hypothesis: `Round 15 proved that the current 256x128/64x64 tiling branch still has real headroom, but it also clarified what the true wall is. The hot kernel's barrier stall fell from 20.89 to 6.49 and mio throttle fell from 2.23 to 0.33, while tensor active rose to 38.55, yet wall-clock moved by only 0.009776 ms and registers per thread actually rose from 166 to 167. That means barrier was not the final wall; the row-pair helper mainly converted synchronization delay into more immediate shared-memory work. The remaining hard wall is still the full 16-fragment 64x64 accumulator footprint plus one-block-per-SM register residency. The concrete next step is to stop carrying a full 64x64 accumulator set through the whole K sweep. Instead, split each warp's 64x64 output into two serial 64x32 half-panels, accumulate one half-panel across all K tiles with an 8-fragment accumulator set, export it through the existing paired scratch, then reuse those registers for the second half-panel. This is the first follow-up that can actually cut live accumulator state rather than only changing issue order.`
- expected bottleneck: `Register-limited occupancy and warp-local live-state pressure inside the 64x64 PTX microkernel, not headline CTA barrier frequency.`
- code locations: `src/kernels/bf16_gemm_v1.cu:318-320, src/kernels/bf16_gemm_v1.cu:512-595, src/kernels/bf16_gemm_v1.cu:716-768, src/kernels/bf16_gemm_v1.cu:1261-1329`
- risk: `A real half-panel accumulator cut will increase some A/B shared loads and may raise LSU or bank pressure further if the implementation is sloppy. If the register drop is not large enough to change scheduling or occupancy behavior, the extra shared traffic can erase the benefit.`
- metrics to re-check: `median runtime, launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, l1tex__data_pipe_lsu_wavefronts.avg.pct_of_peak_sustained_elapsed, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct`

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
