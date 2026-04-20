# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore Linear PTX Export Order, Then Peel The Fixed-K Steady State`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_093003`
- round loop: `round 66/100`
- hypothesis: `Round 65 should be treated as a closed negative on export traversal order, not as a new base: restoring grouped_rows=8 while reversing the PTX hot-band export traversal regressed to 25.69215965 ms even though dram, barrier, and long_scoreboard improved slightly versus round 64. That points to the export-order reversal itself being harmful, while grouped_rows=8 remains the accepted locality base. The next best move is therefore to restore the accepted active base exactly: grouped_rows=8, PTX hot-band right-left 64x64 consume order, reversed PTX compute row-pair traversal, original linear export traversal, one-sync steady-state handoff, B-first refill, and unroll 2. Once that accepted base is back, the highest-upside still-open family is fixed-shape steady-state peeling for the PTX hot-band K loop: split the fixed 452 K-tiles into prologue, steady-state, and epilogue so the active loop stops paying generic next_tile and future_tile control every iteration while keeping the current K16 double buffer unchanged.`
- expected bottleneck: `Hot-loop orchestration in the active PTX 128x128 K16 kernel, especially barrier plus long_scoreboard overhead from the generic fixed-K loop handoff rather than raw DRAM bandwidth or a new tiling problem. The metrics still show low dram throughput and acceptable tensor activity, so the most plausible remaining headroom is fixed-shape control-path cleanup inside the existing two-stage pipeline.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1912 bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel, src/kernels/bf16_gemm_v1.cu:1964 stage_b_shared_tile_async B-first prologue in the active PTX kernel, src/kernels/bf16_gemm_v1.cu:1980 active PTX hot-band K loop with one-sync steady-state handoff, src/kernels/bf16_gemm_v1.cu:2005 B-first refill path inside the accepted PTX steady state`
- risk: `Medium. This direction touches the fixed-shape pipeline schedule in the active kernel, so it can easily reintroduce the already-closed K32 cadence or extra-live staging mistakes if the peeling is not kept strictly within the accepted K16 double-buffer structure. It must not reopen A-first refill, unroll-1, or any consumer-order sweep variants.`
- metrics to re-check: `median runtime, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__throughput.avg.pct_of_peak_sustained_elapsed`

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
