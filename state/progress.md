# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `deeb9765cb3ed49aa93e1d9cefc6b3beacd950f5`
- plateau counter: `1`
- round loop: `round 3/5`
- rounds remaining: `3`
- notes: `Node C build succeeded for round 3/5. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260418_212022_bf16_gemm_v1_deeb976`
- run dir: `runs/20260418_212022_bf16_gemm_v1_deeb976`
- correctness: `FAIL`
- median runtime: `101.616016 ms`
- TFLOP/s: `7.154575 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260418_212050`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Restore explicit cp.async warm-up and consume ordering | bottleneck: Correctness-breaking cp.async producer/consumer hazard in the ping-pong pipeline; after recovery, the remaining limit is still CTA synchronization and MIO throttle rather than DRAM saturation.
- dir_02: Fall back to a correctness-first single-stage staging path | bottleneck: Synchronization and MIO throttle overhead from an over-complicated copy pipeline, not raw memory bandwidth. The current profile already shows barrier stalls rising to 23.82% and MIO throttle to 39.04% while performance regresses.
- dir_03: Amortize sync with a two-slice K macro-stage | bottleneck: Barrier and MIO throttle from too-frequent 16-wide stage turnover, which leaves tensor utilization low at 13.46% even though active warps stay high.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `75.457073 ms`, `3.911390x` slower than CUTLASS
