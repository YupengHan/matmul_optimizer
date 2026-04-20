# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `5e1cfd4820c9703956000c4048b5a8054a8df2d5`
- plateau counter: `13`
- round loop: `round 14/50`
- rounds remaining: `37`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 14/50.`

## Latest measured custom run

- run id: `20260419_232419_bf16_gemm_v1_5e1cfd4`
- run dir: `runs/20260419_232419_bf16_gemm_v1_5e1cfd4`
- correctness: `PASS`
- median runtime: `30.695424 ms`
- TFLOP/s: `23.684945 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_232652`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 14/50 incorporates the recorded CUTLASS NCU baseline directly. CUTLASS runs a 128-thread 128x128x32 multistage kernel with much higher tensor and DRAM utilization and almost no barrier pressure, while the current custom hot-band path remains stuck near 38% tensor active with 256 threads and k16 stages. The recommended next move is therefore a structural hot-band branch, not another local swizzle.`
- dir_01: Start a CUTLASS-shaped hot-band branch: 128x128 CTA, 64x64 warp tiles, 128-thread launch, and K32 staged mainloop | bottleneck: Feed/orchestration inefficiency from the current 256-thread hot-band structure rather than a single bank-conflict or epilogue detail.
- dir_02: Escalate directly to an explicit ldmatrix/mma.sync hot-band microkernel if the CUTLASS-shaped WMMA branch still underfeeds Tensor Cores | bottleneck: Tensor Core under-utilization caused by the current WMMA fragment delivery path.
- dir_03: Restore the accepted-correct implementation surface before continuing the search | bottleneck: Not a bottleneck attack; this is the reset path.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.407935 ms`, `1.131490x` slower than CUTLASS
