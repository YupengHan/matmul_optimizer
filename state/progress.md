# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `edb374118aaec47be2390e0a334526b8d5359596`
- plateau counter: `1`
- round loop: `round 5/5`
- rounds remaining: `1`
- notes: `Node C build succeeded for round 5/5. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_105226_bf16_gemm_v1_edb3741`
- run dir: `runs/20260419_105226_bf16_gemm_v1_edb3741`
- correctness: `PASS`
- median runtime: `34.966097 ms`
- TFLOP/s: `20.792124 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_105254`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Diagnosed regressed run 20260419_105226_bf16_gemm_v1_edb3741 against the restored accepted best 8346b48. The latest single-level B skew retune is negative evidence: end-to-end runtime regressed from 34.655231 ms to 34.966097 ms, tensor active slipped from 35.06 to 34.56, mio_throttle stayed effectively unchanged at 35.83, and hot-kernel LSU wavefront pressure rose sharply. The ranking therefore excludes any further B-skew or mapping tweaks, and it also keeps the earlier named-barrier/subgroup handoff family excluded because that path already regressed much harder by inflating register pressure and collapsing active warps.`
- dir_01: Specialize Tile384 cp.async producer assignment in the peeled hot path | bottleneck: Producer-side cp.async issue overhead and LSU address-generation pressure in the 64x384 peeled hot kernel, not occupancy or synchronization.
- dir_02: Pair the Tile384 epilogue export across the existing two C-scratch stages | bottleneck: Hot-kernel epilogue LSU traffic and shared-memory export overhead after MMA completion, which can still contribute to the elevated mio_throttle.
- dir_03: Add a fixed-K peeled 64x96 tail kernel | bottleneck: Residual generic-loop, barrier, and scoreboard overhead in the 64x96 tail kernel; the upside is capped because the tail is a small fraction of total time.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `8.737343 ms`, `1.337116x` slower than CUTLASS
