# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `3eeb098209be61266f0448e163821fbc4f819003`
- plateau counter: `1`
- round loop: `round 3/5`
- rounds remaining: `3`
- notes: `Node C build succeeded for round 3/5. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_103438_bf16_gemm_v1_3eeb098`
- run dir: `runs/20260419_103438_bf16_gemm_v1_3eeb098`
- correctness: `PASS`
- median runtime: `41.745407 ms`
- TFLOP/s: `17.415555 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_103511`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Diagnosed run 20260419_103438_bf16_gemm_v1_3eeb098 against the restored accepted base 2872f92. The named-barrier/subgroup stage-handoff retune is strong negative evidence: it cut barrier and mio stalls but ballooned the hot kernel to 167 registers/thread, dropped register-limited occupancy to one block per SM, and regressed to 41.745407 ms. The ranking therefore stays on bounded changes around the winning peeled 64x384 plus 64x96 split and does not continue the named-barrier path.`
- dir_01: Pairwise unroll the peeled 64x384 hot loop without changing the handoff model | bottleneck: Tensor issue underfill and loop/control overhead inside the fixed 64x384 hot kernel, with register growth as the main guardrail.
- dir_02: Add a fixed-K peeled 64x96 tail kernel | bottleneck: Residual barrier and scoreboard overhead in the generic 64x96 tail kernel; total upside is capped because the tail is only about 0.9 ms of GPU time today.
- dir_03: Micro-retune the single-level B skew inside the existing 64x384 pipeline | bottleneck: Shared-memory bank behavior and LSU pressure on B-fragment loads, with limited headroom before a mapping tweak starts hurting cp.async coalescing or reopens earlier feed-path regressions.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `9.759199 ms`, `1.376543x` slower than CUTLASS
