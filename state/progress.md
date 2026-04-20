# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `469a12bfb9bb7579ea3238342f598a34e84a5e1a`
- plateau counter: `22`
- round loop: `round 81/100`
- rounds remaining: `20`
- notes: `Node A completed round 80/100. Run node_b to continue round 81/100.`

## Latest measured custom run

- run id: `20260420_115626_bf16_gemm_v1_469a12b`
- run dir: `runs/20260420_115626_bf16_gemm_v1_469a12b`
- correctness: `PASS`
- median runtime: `25.643007 ms`
- TFLOP/s: `28.351566 TFLOP/s`
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
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
