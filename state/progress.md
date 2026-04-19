# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `4473555b78b0a2cfa211c4e9ca7c96dbd42353a8`
- plateau counter: `0`
- round loop: `round 5/5`
- rounds remaining: `1`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 5/5.`

## Latest measured custom run

- run id: `20260418_213511_bf16_gemm_v1_4473555`
- run dir: `runs/20260418_213511_bf16_gemm_v1_4473555`
- correctness: `PASS`
- median runtime: `88.543102 ms`
- TFLOP/s: `8.210910 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260418_213538`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Rebalance the warp tile split to recover active warps | bottleneck: Occupancy and latency hiding from register-limited resident warps, now exposed as low sm__warps_active together with elevated long_scoreboard and mio_throttle stalls.
- dir_02: Swizzle or pad shared tiles to reduce WMMA load MIO pressure | bottleneck: Shared-memory and fragment-load efficiency, expressed as high smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct despite only moderate DRAM and L2 throughput.
- dir_03: Deepen the async copy pipeline for the 2-warp CTA | bottleneck: Copy-to-compute overlap and long scoreboard stalls from a pipeline that is now too shallow for only two resident warps per CTA.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `62.625214 ms`, `3.416293x` slower than CUTLASS
