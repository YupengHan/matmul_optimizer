# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `b368da06a9ba04f8051906d194e80b09bdad9760`
- plateau counter: `6`
- round loop: `round 7/50`
- rounds remaining: `44`
- notes: `Node C build succeeded for round 7/50. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_230146_bf16_gemm_v1_b368da0`
- run dir: `runs/20260419_230146_bf16_gemm_v1_b368da0`
- correctness: `FAIL`
- median runtime: `30.106624 ms`
- TFLOP/s: `24.148155 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_230227`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 7/50 pivots away from peeled control-flow experiments because the main hot-band speedup is real but correctness has not recovered after multiple repair attempts. The recommended next move is therefore dir_01: restore the accepted-correct hot-band loop and test the user's warp-local right-left-right-left register-reuse idea as an isolated experiment.`
- dir_01: Restore the accepted-correct control flow and switch the 64x64 column sweep to explicit right-left-right-left order | bottleneck: Per-warp operand delivery and register reuse inside the 64x64 PTX hot-band microkernel rather than CTA-level pipeline control.
- dir_02: Keep the accepted-correct loop and deepen warp-local Ps2r with next-A-row-pair lookahead | bottleneck: Warp-local shared-to-register latency on the A-side of the 64x64 PTX microkernel.
- dir_03: Return to a light L2-friendly logical CTA swizzle once correctness is back on the accepted surface | bottleneck: Inter-CTA L2 reuse across neighboring hot-band B tiles.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.407935 ms`, `1.131490x` slower than CUTLASS
