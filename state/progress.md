# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `ef8cb27f3c48e6dc473559e4a6c3fb3da8b055b8`
- plateau counter: `17`
- round loop: `round 76/100`
- rounds remaining: `25`
- notes: `Node C build succeeded for round 76/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_113238_bf16_gemm_v1_ef8cb27`
- run dir: `runs/20260420_113238_bf16_gemm_v1_ef8cb27`
- correctness: `PASS`
- median runtime: `33.594879 ms`
- TFLOP/s: `21.640781 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_113413`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Latest measured run 20260420_113238_bf16_gemm_v1_ef8cb27 is a strong negative for the round-75 64x384 default promotion: runtime regressed to 33.59487915 ms from 24.6968317 ms, tensor active fell to 36.06, barrier jumped to 16.62, DRAM throughput rose to 54.20, and launch__occupancy_limit_registers dropped to 1. That closes the 64x384 promotion family for this round. The prior PTX-helper flattening family remains effectively closed-negative as well. Ranking therefore shifts back to restoring a fast default path through the distinct auxiliary 256x128 family first, with the exact PTX default fallback and staged 128x128x32 as lower-rank alternatives.`
- dir_01: Restore The Fast Auxiliary 256x128 Default Hot-Band Path | bottleneck: The 64x384 promotion is exposing DRAM overfetch and barrier amplification rather than compute throughput, so the fix is to return to the lower-overhead 256x128 schedule and recover tensor utilization.
- dir_02: Reinstate The Exact PTX Default Path As The Baseline Fallback | bottleneck: Residual register pressure and scheduler friction in the PTX default hot-band path, but without the wide-tile DRAM blowup seen in the 64x384 promotion.
- dir_03: Try The Staged 128x128x32 Hot-Band Family | bottleneck: Stage synchronization and live-range pressure in a smaller-granularity hot-band kernel, especially under the new barrier-heavy profile.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
