# Progress

## Objective

Beat cuBLAS and drive the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1` to `<= 18.000 ms`.
- target runtime: `<= 18.000 ms`
- comparison target: `cuBLAS`
- rebootstrap source: `20260420_235922_bf16_gemm_v1_489574e`, commit `489574ed5013268dbb79c634450d9a60155a294a`, historical runtime `24.164272 ms`

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `13d245423db024e85562e537ddcb71b1b9e8d722`
- plateau counter: `16`
- round loop: `round 1/1`
- rounds remaining: `1`
- notes: `Node C build succeeded for round 1/1. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_170056_bf16_gemm_v1_13d24542`
- run dir: `runs/20260421_170056_bf16_gemm_v1_13d24542`
- correctness: `PASS`
- median runtime: `31.239679 ms`
- TFLOP/s: `23.272307 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_171314`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-guidance audit for this round: keep Register Reuse as the primary family, but reject the just-measured `col_step_interleaved` subfamily because the live run contradicts its design claim. Keep Async Copy / Pg2s / Stage accepted as the secondary family on the same 128x128 PTX surface, and keep 256x128 Tiling / Data Reuse alive only as the high-ceiling reopen once the current localized regression has been unwound.`
- dir_01: Replace The Failed Interleaved PTX 64x64 Hot-Band Microkernel With The Compact Row-Pair Path | bottleneck: Register-pressure-driven occupancy collapse on the dominant hot-band PTX kernel: 241 registers/thread keeps the kernel at 2 CTAs/SM and leaves tensor utilization low despite unsaturated memory bandwidth.
- dir_02: Port The PTX Hot-Band Path To The Existing 2-K Pg2s Stage Schedule | bottleneck: Wait-group, barrier, and refill cadence on the dominant hot-band path rather than raw global-memory bandwidth.
- dir_03: Reopen 256x128 64x64-Warp Hot-Band Tiling For The Dominant Surface | bottleneck: Hot-band tiling and panel-reuse ceiling: the 128x128 hot-band surface is doing too much coordination per useful math tile and leaves too much work on the slowest profiled kernel.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` of CUTLASS runtime (faster)
- cuBLAS median runtime: `22.000000 ms`
- current best custom gap vs cuBLAS: `2.164272 ms`, `1.098376x` of cuBLAS runtime (slower)
