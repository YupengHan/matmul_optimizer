# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `1181247a12bfd0978dd155838558142b6386710e`
- plateau counter: `0`
- round loop: `round 9/50`
- rounds remaining: `42`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 9/50.`

## Latest measured custom run

- run id: `20260420_185423_bf16_gemm_v1_1181247`
- run dir: `runs/20260420_185423_bf16_gemm_v1_1181247`
- correctness: `PASS`
- median runtime: `24.422464 ms`
- TFLOP/s: `29.768471 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_185444`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 9/50 diagnosis for new best run 20260420_185423_bf16_gemm_v1_1181247. Human-review reflection is explicit here: state/human_review.md currently contains queue state only and no new user-supplied idea bullets, so this round does not invent a new human family and instead maps the latest measured evidence into auditable accept/defer/reject calls. Accepted primary family: stay on the new best grouped-rows-4 128x128 sibling base and clean up the remaining residual outlier first, which is why dir_01 targets the 64-row peeled 64x384 handoff. Accepted but lower-ranked family: tail-only cleanup on the isolated 64x96 path, reflected in dir_02. Deferred alternate family: reopen the PTX 128x128 control branch only if the bounded sibling-base cleanups stall, reflected in dir_03. Rejected for this round: broad fixed-main tile retuning from autotune_round18_main_tiles, because that sweep predates the current hot-band plus grouped-row sibling surface and does not outrank the bounded residual-kernel work now that 1181247 is the accepted best run. Also rejected this round: reopening the 256x128 auxiliary branch, because newer measurements already replaced that family with the stronger 128x128 sibling path.`
- dir_01: Specialize The Peeled 64x384 Residual Band On The New Best Sibling Base | bottleneck: Peeled 64x384 residual-kernel epilogue shared-export traffic and barrier serialization after the hot-band handoff.
- dir_02: Trim The Fixed 64x96 Tail Kernel Without Touching The Hot-Band Path | bottleneck: Generic 64x96 tail-kernel staging and epilogue overhead, especially barrier and scoreboard pressure in the tail-only path.
- dir_03: Reopen The PTX 128x128 Hot-Band Control Branch As The Alternate Family | bottleneck: Dominant 128x128 hot-band kernel control flow, especially PTX-specific export and staging behavior rather than the current residual kernels.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.495424 ms`, `0.942301x` slower than CUTLASS
