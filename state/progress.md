# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `ded79334aec4e4dda1a27d395a6b03406bc3c377`
- plateau counter: `30`
- round loop: `round 43/100`
- rounds remaining: `58`
- notes: `Node C is ready to implement auto_diagnosis_round_043:dir_01 via recommended selection for round 43/100.`

## Latest measured custom run

- run id: `20260421_083834_bf16_gemm_v1_ded7933`
- run dir: `runs/20260421_083834_bf16_gemm_v1_ded7933`
- correctness: `PASS`
- median runtime: `24.265152 ms`
- TFLOP/s: `29.961462 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `auto_diagnosis_round_043`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Auto-generated round 43 diagnosis. Recommended family: aggressive::transplant_half_panel_register_budget_into_the_correct_256x128_pivot.`
- dir_01: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Search drift away from the accepted PTX steady state rather than a missing structural opportunity.
- dir_03: Port Grouped-Row Traversal Into The Non-PTX 128x128 Sibling | bottleneck: A branch-local hot-band scheduling or geometry bottleneck on the dominant kernel path, rather than a pure restore-only action.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
