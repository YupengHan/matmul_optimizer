# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `d1b835ea84e73b2922092b0bf1f54e08f04b2622`
- plateau counter: `1`
- round loop: `round 6/30`
- rounds remaining: `25`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 6/30.`

## Latest measured custom run

- run id: `20260419_221322_bf16_gemm_v1_d1b835e`
- run dir: `runs/20260419_221322_bf16_gemm_v1_d1b835e`
- correctness: `PASS`
- median runtime: `30.692336 ms`
- TFLOP/s: `23.687328 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_221410`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 6/30 starts from a negative but informative experiment. The grouped CTA traversal that was meant to hint better L2 locality preserved correctness and slightly improved the isolated hot-band kernel time, but it regressed end-to-end runtime by about 1.26 ms, so it is not a viable surface for continued optimization. Recommended direction dir_01 therefore restores the newly established best custom branch `5dd9f0d` before another family is tried. Dir_02 and dir_03 both stay aligned with the user-provided human ideas on top of that restored branch: first a warp-local bank/conflict consumer sweep that still respects the no-extra-shared rule, then a cp.async ownership retune if the consumer-side variant does not pay off.`
- dir_01: Restore the new best custom branch `5dd9f0d` and discard the grouped-CTA traversal | bottleneck: Not a new bottleneck attack; this is a branch reset after a structurally negative CTA-traversal experiment.
- dir_02: Human idea bank conflict: test a `Right Left Right Left` warp-local B consumer sweep on the restored best branch | bottleneck: Residual B-side shared-to-register delivery and bank behavior inside the 64x64 hot-band micro-tile.
- dir_03: Human idea coalescing + async copy: retune hot-band cp.async ownership after the restore | bottleneck: Global-to-shared staging instruction overhead and copy ownership regularity.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `3.514943 ms`, `1.135618x` slower than CUTLASS
