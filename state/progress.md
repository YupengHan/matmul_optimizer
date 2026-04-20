# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `9a4bb85409600456179030fc1eb1e59eb5ea3722`
- plateau counter: `15`
- round loop: `round 74/100`
- rounds remaining: `27`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 74/100.`

## Latest measured custom run

- run id: `20260420_112149_bf16_gemm_v1_9a4bb85`
- run dir: `runs/20260420_112149_bf16_gemm_v1_9a4bb85`
- correctness: `PASS`
- median runtime: `24.696192 ms`
- TFLOP/s: `29.438523 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_112500`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Latest measured run: 24.69619179 ms with tensor active 48.21, barrier 6.38, long scoreboard 3.74, mio 3.33, and launch__occupancy_limit_registers = 2. That reads as compute/schedule limited with a register ceiling, not DRAM bound. Human-idea audit for this round: register-pressure reduction is accepted as the primary family because the profile is occupancy-limited; auxiliary 256x128 scheduling is accepted as a separate bounded family because the previous round already improved that path; export helper cleanup is deferred to low rank because barrier is present but not dominant; coalescing / global-memory widening is deferred because DRAM is only 9.73%; shared-memory / bank-conflict work is deferred because the profile does not show a strong shared-memory stall signature; launch-order locality is rejected for now because the evidence does not point to it and prior snake-style locality work regressed.`
- dir_01: Flatten PTX Hot-Band Compute Helpers To Reduce Register Pressure | bottleneck: Register pressure and compiler scheduling friction inside the active PTX hot-band compute path, which is consistent with launch__occupancy_limit_registers = 2 and the low achieved warps-active number.
- dir_02: Revisit The 256x128 Auxiliary Hot-Band Path As A Separate Schedule Family | bottleneck: Compute scheduling and latency hiding on the auxiliary 256x128 hot-band path, not DRAM bandwidth.
- dir_03: Trim PTX Export Helper Shape Without Changing Store Semantics | bottleneck: Residual export-side instruction overhead and register clutter around the PTX writeback path, not global memory bandwidth.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
