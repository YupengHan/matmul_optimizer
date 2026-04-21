# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `bb69e9bb681f6dfb5b01e35965b180d20506fd3d`
- plateau counter: `17`
- round loop: `round 30/100`
- rounds remaining: `71`
- notes: `Node C build succeeded for round 30/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_013042_bf16_gemm_v1_bb69e9b`
- run dir: `runs/20260421_013042_bf16_gemm_v1_bb69e9b`
- correctness: `PASS`
- median runtime: `25.911183 ms`
- TFLOP/s: `28.058133 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_013125`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 30 treats round 29 as a structurally useful failure. The launch-bounds probe did exactly what the occupancy diagnosis wanted: registers fell from 200 to 168, occupancy_limit_registers rose from 2 to 3, active warps rose from 16.59% to 24.77%, and long-scoreboard stall collapsed from 7.34% to 1.69%. The runtime regression therefore points to the next missing piece, not a fully wrong premise: barrier stall doubled to 10.97% and the hot-band kernel slowed from about 32.69 us to about 33.76 us. The ranking therefore continues the aggressive path, but narrows it to barrier amortization on top of the newly proven occupancy gain.`
- dir_01: Keep 3-CTA Residency And Amortize Barriers With Two-K Stages | bottleneck: Synchronization and stage handoff overhead after the residency wall has been partially relaxed.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Known register-limited plateau on the accepted 128x128 PTX surface.
- dir_03: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and handoff strategy in the 256x128 hot-band path, plus correctness-sensitive writer ownership.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
