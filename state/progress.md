# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `6dd39ad50b8e36dd035ae435800103257053f6a2`
- plateau counter: `4`
- round loop: `round 5/5`
- rounds remaining: `1`
- notes: `Node A completed round 4/5. Run node_b to continue round 5/5.`

## Latest measured custom run

- run id: `20260419_100457_bf16_gemm_v1_6dd39ad`
- run dir: `runs/20260419_100457_bf16_gemm_v1_6dd39ad`
- correctness: `PASS`
- median runtime: `37.373951 ms`
- TFLOP/s: `19.452571 TFLOP/s`
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
- current best custom gap: `11.367918 ms`, `1.438613x` slower than CUTLASS
