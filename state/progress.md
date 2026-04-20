# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `2c6441d8d428ccc1a769600d6c12add7a5c35d61`
- plateau counter: `6`
- round loop: `round 45/100`
- rounds remaining: `56`
- notes: `Node C build succeeded for round 45/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_022041_bf16_gemm_v1_2c6441d`
- run dir: `runs/20260420_022041_bf16_gemm_v1_2c6441d`
- correctness: `PASS`
- median runtime: `26.955776 ms`
- TFLOP/s: `26.970821 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_022105`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 44 mattered because it was restorative but informative: removing K32 and switching to single-scratch sequential export pulled runtime from 30.126080 ms back to 26.955776 ms. Relative to round 42 at 27.003904 ms, the active PTX hot-band only nudged upward on tensor active (47.86 -> 48.05) while barrier (11.18 -> 11.21) and long scoreboard (1.29 -> 1.33) stayed basically flat; mio throttle improved (0.56 -> 0.34) but was already small. That means export lifetime trimming has positive signal, but the ceiling remains limited and the next round must push the active PTX path below the current 26 ms band rather than reintroduce restorative pipeline experiments. The user goal is still sub-20 ms, not merely catching CUTLASS. Family review: Coalescing Access -> deprioritized for now because the active path already uses aligned 16-byte async copies and the profile does not show a classic global-load packing failure. Data Reuse -> still live, but the highest-value reuse idea is CTA traversal / L2 residency, not another generic tile-size sweep. Async Copy -> deprioritized as a primary move because rolling back to the K16 double buffer is what restored performance and long scoreboard is already low. Bank Conflict -> monitor but not top-ranked; the shared path has measurable bank traffic, yet the profile does not show a decisive bank-conflict stall signature on its own. L2 Cache -> promoted and captured by dir_02 because the active 60x50 hot-band grid dominates runtime and the PTX branch no longer uses the grouped-row remap present in the older 128x128x32 path. Register Reuse -> promoted hardest and captured by dir_01 because 188 regs/thread plus occupancy capped at 2 blocks/SM is the clearest remaining ceiling on tensor issue. Pg2s -> deprioritized because mio throttle and long scoreboard are both low after the rollback, so the global-to-shared path is no longer the obvious limiter. Ps2r -> kept as a secondary direction in dir_03 because short scoreboard and shared wavefront pressure still leave room for a better fragment load path. Stage -> deprioritized because round 44 already showed that extra stage depth / K32 buffering was not the way through the plateau.`
- dir_01: Trim PTX Hot-Band Accumulator And Fragment Live Ranges | bottleneck: Occupancy and tensor-core under-utilization in the active PTX hot-band path, driven by register pressure rather than global-memory latency.
- dir_02: Port Grouped-Row CTA Traversal To The PTX Hot Band For Better L2 Reuse | bottleneck: L2 reuse and block traversal efficiency for the hot-band CTA schedule, especially B-side reuse across adjacent row groups.
- dir_03: Retune Shared-To-Register Fragment Access In The PTX Hot Band | bottleneck: Shared-memory to register movement and fragment load replay in the PTX hot-band steady state.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `0.056383 ms`, `1.002175x` slower than CUTLASS
