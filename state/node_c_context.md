# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Trim PTX Accumulator And Export Live Range On The Restored Grouped-Rows-4 Base`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_181421`
- round loop: `round 4/50`
- hypothesis: `Run `20260420_181354_bf16_gemm_v1_e1c12b7` is the first negative result after the grouped-rows-4 restore became the accepted best custom surface. It tested the recommended steady-state handoff retime and regressed end-to-end runtime from 24.44441605 ms to 25.51500797 ms, yet the dominant hot-band kernel barely changed versus the accepted `2e4dd24` base: kernel time only moved from 32.80 ms to 32.95 ms, registers stayed at 200, shared memory stayed at 22.016 KiB, barrier stayed flat at 5.61% -> 5.62%, and long scoreboard only worsened slightly from 7.43% to 7.58%. That is strong negative evidence against continuing the handoff-retime family on this surface. The remaining obvious open wall on the restored base is still occupancy and live-state pressure: `launch__occupancy_limit_registers = 2`, only 16.6% active warps, and a full `PtxWmmaAccTileSet64x64` plus repeated single-scratch export sequence kept alive through the PTX hot-band epilogue. The best next direction is therefore to leave the restored grouped-rows-4 launch and handoff semantics alone and instead shorten accumulator/export lifetimes to see whether the hot-band kernel can recover issue headroom without reopening the closed handoff family.`
- expected bottleneck: `Register pressure and export-side live-state lifetime in the PTX hot-band microkernel, which is still capping occupancy and latency hiding on the restored best surface.`
- code locations: `src/kernels/bf16_gemm_v1.cu:405-408, src/kernels/bf16_gemm_v1.cu:1010-1067, src/kernels/bf16_gemm_v1.cu:1952-2047`
- risk: `Medium to high. This attacks a persistent measured wall, but the export path is correctness-sensitive and a bad lifetime trim can add instructions or synchronization without reducing the 200-register footprint.`
- metrics to re-check: `correctness, median runtime, launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`

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
