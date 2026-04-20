# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `1930e3ff6a7fb22016af4b6c81929000cdd784fc`
- plateau counter: `4`
- round loop: `round 3/20`
- rounds remaining: `18`
- notes: `Node A completed round 2/20. Run node_b to continue round 3/20.`

## Latest measured custom run

- run id: `20260419_170714_bf16_gemm_v1_1930e3f`
- run dir: `runs/20260419_170714_bf16_gemm_v1_1930e3f`
- correctness: `PASS`
- median runtime: `34.709423 ms`
- TFLOP/s: `20.945880 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `pending_generation`
- diagnosis id: `None`
- recommended direction: `None`
- approved direction: `None`
- diagnosis notes: `Run node_b to produce exactly three directions from the latest measured run.`
- no directions recorded yet

## Active implementation direction

- direction id: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `6.083199 ms`, `1.234710x` slower than CUTLASS
