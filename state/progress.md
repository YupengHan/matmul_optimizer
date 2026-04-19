# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `6600aebb6478a2fafe0e75f1780e596a9706e1d1`
- plateau counter: `2`
- round loop: `round 1/20`
- rounds remaining: `20`
- notes: `Node C build succeeded for round 1/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260418_220017_bf16_gemm_v1_2e79574`
- run dir: `runs/20260418_220017_bf16_gemm_v1_2e79574`
- correctness: `PASS`
- median runtime: `91.601360 ms`
- TFLOP/s: `7.936775 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260418_220408`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Widen the async staging path to 16-byte fixed-tile copies | bottleneck: Global-to-shared staging instruction pressure and MIO throttling from the current 8-byte async copy path, not a pure DRAM bandwidth ceiling.
- dir_02: Skew the shared tiles for bank-friendlier WMMA fragment loads | bottleneck: Shared-memory and fragment-load pressure around `wmma::load_matrix_sync`, currently surfacing as high `smsp__warp_issue_stalled_mio_throttle` with only moderate DRAM and L2 throughput.
- dir_03: Peel the fixed 7232-K loop into a branch-light steady-state pipeline | bottleneck: Synchronization and control overhead inside the generic per-slice K loop, showing up as persistent barrier and long-scoreboard stalls even after the round-4 reuse win.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `62.625214 ms`, `3.416293x` slower than CUTLASS
