# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `69f60e616da5be56d1786504c06088f10b6eaa46`
- plateau counter: `2`
- round loop: `round 11/50`
- rounds remaining: `40`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 11/50.`

## Latest measured custom run

- run id: `20260420_191351_bf16_gemm_v1_69f60e6`
- run dir: `runs/20260420_191351_bf16_gemm_v1_69f60e6`
- correctness: `PASS`
- median runtime: `25.164400 ms`
- TFLOP/s: `28.890791 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_191417`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 11/50 diagnosis for regressed run 20260420_191351_bf16_gemm_v1_69f60e6, with the implementation surface already restored to the accepted 1181247 base. Human-review reflection is explicit here: state/human_review.md still contains queue state only and no new user-provided idea bullets, so this round maps the measured families directly. Accepted primary family: reopen hot-band alternatives, because the latest NCU comparison shows the dominant 128x128 hot-band kernel is the only kernel that clearly trails the accepted best while both the peeled and tail kernels are slightly faster in isolation. That is why dir_01 recommends the PTX 128x128 control branch and dir_02 keeps the dormant 128x128x32 pipeline as the secondary hot-band alternative. Deferred family: tail-only cleanup. Round 11 explicitly rejects it as the next default path because 69f60e6 is the second straight end-to-end regression from a bounded cleanup attempt, even though the tail kernel itself improved in NCU. Also deferred for this round: reopening the peeled single-stage residual family as a default, because the earlier cc89c17 run already showed that a local peeled-kernel win can still lose end to end. Rejected again for ranking: the stale broad fixed-main tile sweep in state/autotune_round18_main_tiles, because it predates the current hot-band split regime and does not outrank the now-evidence-backed hot-band recovery family.`
- dir_01: Reopen The PTX 128x128 Hot-Band Control Branch On The Restored 1181247 Base | bottleneck: Dominant 128x128 hot-band control flow, especially cp.async wait cadence and export-scratch behavior inside the steady-state hot path.
- dir_02: Activate The Dormant 128x128x32 Hot-Band Pipeline On The Restored Base | bottleneck: Hot-band stage cadence and synchronization frequency in the 128x128 steady-state loop.
- dir_03: Keep Tail-Only Cleanup Behind An Explicit Gate Instead Of The Default Path | bottleneck: Generic 64x96 tail staging and epilogue behavior, especially the still-high compute-memory throughput and barrier-heavy tail cleanup path.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.495424 ms`, `0.942301x` slower than CUTLASS
