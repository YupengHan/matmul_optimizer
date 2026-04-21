# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `fc400df814258c9927aa72a78b213b2e9325787f`
- plateau counter: `102`
- round loop: `round 11/100`
- rounds remaining: `90`
- notes: `Node A completed round 10/100. Run node_b to continue round 11/100.`

## Latest measured custom run

- run id: `20260421_124420_bf16_gemm_v1_fc400df`
- run dir: `runs/20260421_124420_bf16_gemm_v1_fc400df`
- correctness: `PASS`
- median runtime: `45.920258 ms`
- TFLOP/s: `15.832216 TFLOP/s`
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
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
