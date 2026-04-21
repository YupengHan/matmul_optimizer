# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `676f10de876324a904cbb7d13cb85c6ade2a276b`
- plateau counter: `1`
- round loop: `round 3/20`
- rounds remaining: `18`
- notes: `Node A completed round 2/20. Run node_b to continue round 3/20.`

## Latest measured custom run

- run id: `20260420_220628_bf16_gemm_v1_676f10d`
- run dir: `runs/20260420_220628_bf16_gemm_v1_676f10d`
- correctness: `PASS`
- median runtime: `30.286848 ms`
- TFLOP/s: `24.004460 TFLOP/s`
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
- notes: `No direction selected yet. Use approve, use-recommended-direction, or select-next after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.498560 ms`, `0.942180x` slower than CUTLASS
