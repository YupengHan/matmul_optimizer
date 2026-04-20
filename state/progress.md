# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `66273be4ab02d93dca25251ada08f52ec95cdfd9`
- plateau counter: `2`
- round loop: `round 55/100`
- rounds remaining: `46`
- notes: `Node A completed round 54/100. Run node_b to continue round 55/100.`

## Latest measured custom run

- run id: `20260420_083244_bf16_gemm_v1_66273be`
- run dir: `runs/20260420_083244_bf16_gemm_v1_66273be`
- correctness: `PASS`
- median runtime: `24.896433 ms`
- TFLOP/s: `29.201751 TFLOP/s`
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
- current best custom gap: `-1.022401 ms`, `0.960552x` slower than CUTLASS
