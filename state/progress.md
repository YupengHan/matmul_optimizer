# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `dfd7960585906ecd34e523003e3631dcd1bfd37b`
- plateau counter: `16`
- round loop: `single-run`
- rounds remaining: `0`
- notes: `Node A completed the final planned round. Review the results before starting another loop.`

## Latest measured custom run

- run id: `20260419_214535_bf16_gemm_v1_dfd7960`
- run dir: `runs/20260419_214535_bf16_gemm_v1_dfd7960`
- correctness: `PASS`
- median runtime: `32.758783 ms`
- TFLOP/s: `22.193114 TFLOP/s`
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
- current best custom gap: `4.134879 ms`, `1.159538x` slower than CUTLASS
