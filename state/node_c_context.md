# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Rebalance the warp tile split to recover active warps`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260418_213538`
- round loop: `round 5/5`
- hypothesis: `The new 2-warp CTA improved runtime by cutting barrier stalls from 21.86% to 8.89% and raising tensor activity from 13.64% to 15.07%, but it also doubled the register occupancy limit from 12 to 24 and dropped active warps to 45.70%. Retuning the CTA and warp tile split so each warp holds less output state while keeping some of the new per-warp reuse should recover latency hiding without fully giving back the reuse win.`
- expected bottleneck: `Occupancy and latency hiding from register-limited resident warps, now exposed as low sm__warps_active together with elevated long_scoreboard and mio_throttle stalls.`
- code locations: `src/kernels/bf16_gemm_v1.cu:kWarpTilesM, src/kernels/bf16_gemm_v1.cu:kWarpTilesN, src/kernels/bf16_gemm_v1.cu:kWarpMmaTilesN, src/kernels/bf16_gemm_v1.cu:kWarpsPerBlock, src/kernels/bf16_gemm_v1.cu:bf16_gemm_v1_tensor_core_kernel`
- risk: `Changing the warp-to-output mapping can easily reintroduce the barrier overhead that the current best run just removed, so a full rollback to the older 4-warp shape is not automatically a win.`
- metrics to re-check: `median runtime, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, launch__occupancy_limit_registers, launch__block_size`

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
