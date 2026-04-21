# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `bb3fc522e8e54b6da3644845bce77f2182f5f41c`
- plateau counter: `8`
- round loop: `single-run`
- rounds remaining: `0`
- notes: `Node A completed the final planned round. Review the results before starting another loop.`

## Latest measured custom run

- run id: `20260420_205720_bf16_gemm_v1_bb3fc52`
- run dir: `runs/20260420_205720_bf16_gemm_v1_bb3fc52`
- correctness: `PASS`
- median runtime: `25.381776 ms`
- TFLOP/s: `28.643363 TFLOP/s`
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
- current best custom gap: `-1.495424 ms`, `0.942301x` slower than CUTLASS
