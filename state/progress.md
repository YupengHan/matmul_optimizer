# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `17032e6cabd475782c1528c2900f3c4239f3b45d`
- plateau counter: `18`
- round loop: `round 31/100`
- rounds remaining: `70`
- notes: `Node C build succeeded for round 31/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_013416_bf16_gemm_v1_17032e6`
- run dir: `runs/20260421_013416_bf16_gemm_v1_17032e6`
- correctness: `PASS`
- median runtime: `28.200448 ms`
- TFLOP/s: `25.780421 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_013500`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 31 is a recovery diagnosis after two informative but clearly negative aggressive probes. The round-29 launch-bounds probe reduced the hot-band register budget from 200 to 168, raised occupancy_limit_registers from 2 to 3, and increased active warps to 24.77%, but barrier stall jumped to 10.97%. The round-30 128x128x32 follow-on kept 168 registers but raised shared memory per block to 43,008 B, which collapsed active warps back to 16.58% and regressed the hot-band kernel to 38.09 us. The search should therefore restore the exact PTX anchor now, then reuse the lessons from these two rounds to choose the next aggressive branch from a clean base.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Known register-limited plateau on the accepted 128x128 PTX surface, used here as a recovery anchor rather than a discovery move.
- dir_02: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and synchronization strategy in the 256x128 hot-band path, plus correctness-sensitive output ownership.
- dir_03: Trim Microkernel Barriers Without Reintroducing Shared-Memory Blowup | bottleneck: Barrier cadence inside the single-K 128x128 PTX microkernel while preserving the lower shared-memory footprint.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
