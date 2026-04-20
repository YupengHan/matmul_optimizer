# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `a4dc5e8104404eb15624be12dac380ba80e64ec6`
- plateau counter: `18`
- round loop: `round 77/100`
- rounds remaining: `24`
- notes: `Node C build succeeded for round 77/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_113704_bf16_gemm_v1_a4dc5e8`
- run dir: `runs/20260420_113704_bf16_gemm_v1_a4dc5e8`
- correctness: `PASS`
- median runtime: `31.867904 ms`
- TFLOP/s: `22.813531 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_113820`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Latest measured run 20260420_113704_bf16_gemm_v1_a4dc5e8 is a clear negative for the non-PTX default hot-band dispatch promotion family: runtime is 31.86790371 ms, still far slower than the prior fast PTX regime around 24.696 ms, while tensor active is 36.43, barrier is 10.69, short scoreboard is 10.20, and launch__occupancy_limit_registers is 1. That closes the non-PTX default promotion family for now. The earlier 64x384 promotion was already closed-negative, and the PTX-helper flattening family remains closed-negative as well. Ranking therefore shifts back to restoring the exact fast PTX default baseline first, then exploring a distinct staged 128x128x32 family or a low-rank PTX-adjacent export/scratch cleanup from that restored baseline.`
- dir_01: Restore The Exact Fast PTX Default Hot-Band Path | bottleneck: The failed non-PTX default promotions are exposing barrier and memory inflation rather than a compute win, so the baseline PTX path should re-center the profile on the proven lower-overhead hot-band schedule.
- dir_02: Try The Staged 128x128x32 Hot-Band Family | bottleneck: Stage synchronization, live-range pressure, and short-scoreboard stalls in a smaller-granularity hot-band kernel.
- dir_03: Trim PTX Export And Scratch Shape On The Restored Baseline | bottleneck: Residual export-side instruction overhead and scratch/register clutter around the PTX writeback path.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
