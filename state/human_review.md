# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 32/50` with `19` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_002827`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 32, reviewed family by family against the measured best run at 26.924 ms with tensor active 48.56, barrier stall 8.13, mio_throttle 4.44, long_scoreboard 1.31, and registers still limiting occupancy to 2 blocks/SM. Tiling: reject reopening the 256x128 / 64x64 main retile this round because the measured winner is still the 128x128 hot-band branch and prior 256x128/K32 attempts regressed. Coalescing Access: accept as already satisfied in the base via 16-byte aligned wide global-to-shared movement, so hold fixed. Data Reuse: accept the current shared-memory A/B reuse structure as base and do not perturb it first. Async Copy: accept as base via cp.async and non-blocking staging, but do not make it the primary knob yet. Bank Conflict: defer new padding/permuted-layout changes because the current run is not dominated by shared-feed failure; the existing layout is good enough for this round. L2 Cache: accept as the primary family because grouped CTA order is still producing real gains, so `grouped_rows=2` is the next best bounded move. Register Reuse: accept as fixed in the base through `__launch_bounds__(128, 2)` plus unroll-2; no further reuse rewrite is first. Pg2s: accept the current double-buffered global-to-shared pipeline as the base. Ps2r: defer deeper warp-local consumer pipelining because the simpler L2 locality knob is still moving the curve. Stage: accept the current multi-buffer pipeline as sufficient for now and only revisit small barrier cleanup after the grouped-order sweep stalls.`
- dir_01: Keep the current best branch and reduce grouped_rows one more step to 2 | bottleneck: Cross-CTA cache locality under the current best compiler-guided hot-band branch.
- dir_02: Freeze grouped_rows=4 as the new best hot-band setting and start trimming the smaller remainder only if grouped_rows=2 fails | bottleneck: Secondary-region overhead after hot-band tuning converges.
- dir_03: Hold the current best branch fixed and revisit tiny barrier-side cleanup only after the grouped_rows=2 result is known | bottleneck: Residual barrier overhead in the current best hot-band kernel.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
