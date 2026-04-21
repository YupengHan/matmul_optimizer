# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `df5bac281a2efef7f02478947a334a51b6510138`
- plateau counter: `0`
- round loop: `round 8/100`
- rounds remaining: `93`
- notes: `Node A completed round 7/100. Run node_b to continue round 8/100.`

## Latest measured custom run

- run id: `20260420_224147_bf16_gemm_v1_df5bac2`
- run dir: `runs/20260420_224147_bf16_gemm_v1_df5bac2`
- correctness: `PASS`
- median runtime: `24.164352 ms`
- TFLOP/s: `30.086443 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

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
- notes: `No direction selected yet. Use approve, use-recommended-direction, or select-next after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753536 ms`, `0.932343x` slower than CUTLASS
