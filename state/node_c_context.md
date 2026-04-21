# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore The Best Measured PTX Grouping Window On The Accepted Surface`
- candidate id: `diagnosis_20260421_000409:dir_01`
- base run id: `20260421_000316_bf16_gemm_v1_c643816`
- primary family id: `legacy::restore_the_best_measured_ptx_grouping_window_on_the_accepted_surface`
- planned action fingerprint: `26b22d7f05ca7ff6`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_000409`
- round loop: `round 14/100`
- hypothesis: `Round 13 gave a strong negative result on the repaired PTX surface: swapping the future-tile refill from `B->A` to `A->B` regressed runtime from the round-12 best 24.16427231 ms to 24.48483181 ms, even though the dominant hot-band kernel stayed the same PTX microkernel. A direct source diff versus the current best commit `489574e` shows the semantic delta is only that one refill-order hunk at `src/kernels/bf16_gemm_v1.cu:2042-2053`. The counters also moved in the wrong direction for this family: long-scoreboard dropped sharply, but barrier jumped from 5.43% to 6.29% and total runtime got much worse. The immediate next move is therefore not another exploit on top of the bad state; it is to restore the current best PTX surface first so the loop can continue exploring from the real winner instead of compounding a known negative handoff order.`
- expected bottleneck: `Known-negative handoff ordering on the active PTX hot-band loop, where the A-then-B future refill increases effective barrier cost enough to overwhelm any scoreboard reduction.`
- code locations: `src/kernels/bf16_gemm_v1.cu:2042-2053, src/kernels/bf16_gemm_v1.cu:2110-2117`
- risk: `Low. The restore is narrowly bounded and the current source differs from the best-known PTX surface by essentially one scheduler hunk, so this is the cleanest way to recover a valid search anchor after the round-13 regression.`
- metrics to re-check: `end-to-end median runtime versus the 24.164272 ms best-known PTX run, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, sm__warps_active.avg.pct_of_peak_sustained_active, Kernel Name in ncu_details.csv for the dominant hot-band launch, hot-band gpu__time_duration.sum`

## Allowed edit surface

- `src/kernels/*`
- `src/runner/main.cpp` when the direction requires runner glue
- `include/*` when a stable interface change is required
- `CMakeLists.txt` only if the build path genuinely needs it
- `scripts/graph.py` or `scripts/sweep_fixed_main_tiles.py` only when the direction requires minimal workflow glue

## Implementation notes

- implement exactly one selected direction
- stay within the primary family by default
- if the implementation clearly crosses into another family, update `state/active_direction.json` and record `secondary_family_ids` before finalize
- if the implementation semantically drifts from the planned action, update `implemented_action_fingerprint`, `semantic_delta_tags`, or `actual_code_regions` in `state/active_direction.json` before finalize
- build failure is still recorded as a structured `state/latest_attempt.json` entry with `build_status=FAIL`

## Required commands

- edit code for one direction only
- then run `python scripts/graph.py node_c --finalize`
- default behavior after a successful node_c finalize is to auto-run node_a

## Dirty working tree snapshot before node_c finalize

- `src/kernels/bf16_gemm_v1.cu`
