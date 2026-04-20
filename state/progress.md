# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `f35aea8b55dcd6d7d085a93469f414d6471ccd07`
- plateau counter: `3`
- round loop: `round 20/50`
- rounds remaining: `31`
- notes: `Node C build succeeded for round 20/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_000504_bf16_gemm_v1_f35aea8`
- run dir: `runs/20260420_000504_bf16_gemm_v1_f35aea8`
- correctness: `PASS`
- median runtime: `60.609537 ms`
- TFLOP/s: `11.995132 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_000825`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 20: Stage remains the primary family, but in a deliberately conservative form because the last two aggressive experiments failed for different reasons. Register Reuse is temporarily deferred after round 19 showed that forcing higher occupancy through launch-bounds was far too expensive. Tiling 256x128 is now rejected for the current branch because it raised shared footprint and reduced active warps without any upside. Async Copy, Data Reuse, Pg2s, and Ps2r remain accepted background mechanisms already present in the accepted 128x128 K16 kernel. Coalescing Access and Bank Conflict remain deferred because the regressions were driven much more by occupancy / stage effects than by those signals. The L2 clue stays as the next orthogonal backup plan.`
- dir_01: Restore the accepted 128x128 K16 base and scope the consume fence only to real stage overwrites | bottleneck: Barrier / orchestration overhead in the accepted 128x128 K16 hot-band loop, with no increase in shared footprint or register pressure.
- dir_02: Restore the accepted base and try a milder register hint that does not target extra resident blocks | bottleneck: Compiler register allocation quality on the accepted 128x128 K16 kernel.
- dir_03: Hold the accepted base fixed and use the deferred L2-friendly block-order clue as the next orthogonal axis | bottleneck: Inter-CTA cache reuse rather than within-CTA feed or occupancy.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.287104 ms`, `1.126828x` slower than CUTLASS
