# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `d327deeed06ccae5ee77ceb137c32207ef43487c`
- plateau counter: `26`
- round loop: `round 39/100`
- rounds remaining: `62`
- notes: `Node C is ready to implement diagnosis_20260421_082126:dir_01 via recommended selection for round 39/100.`

## Latest measured custom run

- run id: `20260421_081904_bf16_gemm_v1_d327dee`
- run dir: `runs/20260421_081904_bf16_gemm_v1_d327dee`
- correctness: `PASS`
- median runtime: `24.171520 ms`
- TFLOP/s: `30.077522 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_082126`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 39 ranks the bounded PTX wait/commit-window reopen first, with exact restore as the fallback and the 256x128 pivot kept live as the structural branch.`
- dir_01: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual cp.async wait-group timing and control-path latency in the PTX 128x128 hot-band microkernel after the exact restore surface has been re-established.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Search drift away from the accepted PTX anchor, not a missing structural branch.
- dir_03: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Structural latency hiding and control amortization on the hot band, not another micro-retime within the same PTX steady state.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
