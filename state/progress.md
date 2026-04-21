# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `5b106fe2b635fb7711559e798e1c5da4968126a4`
- plateau counter: `38`
- round loop: `round 51/100`
- rounds remaining: `50`
- notes: `Node C build succeeded for round 51/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_083949_bf16_gemm_v1_5b106fe`
- run dir: `runs/20260421_083949_bf16_gemm_v1_5b106fe`
- correctness: `PASS`
- median runtime: `24.448512 ms`
- TFLOP/s: `29.736755 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `auto_diagnosis_round_051`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Auto-generated round 51 diagnosis. Recommended family: aggressive::transplant_half_panel_register_budget_into_the_correct_256x128_pivot.`
- dir_01: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Search drift away from the accepted PTX steady state rather than a missing structural opportunity.
- dir_03: Port Grouped-Row Traversal Into The Non-PTX 128x128 Sibling | bottleneck: A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
