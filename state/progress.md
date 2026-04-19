# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `6eaca8ea3a675237521dd743b9e744b57167933f`
- plateau counter: `4`
- round loop: `round 15/20`
- rounds remaining: `6`
- notes: `Node A completed round 14/20. Run node_b to continue round 15/20.`

## Latest measured custom run

- run id: `20260419_003937_bf16_gemm_v1_6eaca8e`
- run dir: `runs/20260419_003937_bf16_gemm_v1_6eaca8e`
- correctness: `PASS`
- median runtime: `43.769424 ms`
- TFLOP/s: `16.610212 TFLOP/s`
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
- current best custom gap: `17.779776 ms`, `1.686004x` slower than CUTLASS
