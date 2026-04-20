# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `de7e8be6e77487fbeecd095db66faa31c991de1e`
- plateau counter: `0`
- round loop: `round 56/100`
- rounds remaining: `45`
- notes: `Node A completed round 55/100. Run node_b to continue round 56/100.`

## Latest measured custom run

- run id: `20260420_083902_bf16_gemm_v1_de7e8be`
- run dir: `runs/20260420_083902_bf16_gemm_v1_de7e8be`
- correctness: `PASS`
- median runtime: `24.849423 ms`
- TFLOP/s: `29.256994 TFLOP/s`
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
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.068465 ms`, `0.958775x` slower than CUTLASS
