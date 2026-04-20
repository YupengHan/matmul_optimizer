# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore the exact round-69 base, then change PTX issue grouping inside the 64x64 compute helpers without changing accepted traversal semantics`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_105723`
- round loop: `round 71/100`
- hypothesis: `The current reproducible exact base is the round-69 restore at 25.49913597 ms, not the old historical 24.57088089 ms snapshot. Round 70 tested a very narrow one-sync handoff closure by splitting only the final tile out of the hot loop, and it regressed badly to 25.90719986 ms while barrier fell from 6.41 to 4.49 but long_scoreboard jumped from 3.98 to 12.11. That is strong evidence that the handoff-closure family is closed-negative in this exact-base regime: it mainly trades barrier for scoreboard and loses runtime. With grouped_rows sweeps, snake locality, fixed-K peeling, export traversal changes, A-first refill, consumer-order sweeps, and broad stage overexpansions all already closed, the best remaining bounded family is a PTX issue-order move that preserves the accepted semantics: grouped_rows=8, right-left 64x64 PTX consume order, reversed PTX compute row-pair traversal, linear export traversal, one-sync steady-state handoff, B-first refill, active-loop unroll 2, accepted 256x128 unroll 1, and accepted helper shapes. Concretely, restore the exact round-69 base first, then change only how the PTX 64x64 compute helpers group and issue the already-accepted work, for example by batching the accepted right-left column issues or otherwise reshaping helper structure inside the current row-pair recursion without changing the logical consume order or the higher-row-first compute traversal.`
- expected bottleneck: `PTX compute-helper issue grouping and scheduler behavior inside the accepted 64x64 hot-band microkernel, now exposed as long scoreboard after the handoff family was falsified.`
- code locations: `src/kernels/bf16_gemm_v1.cu:730-781, src/kernels/bf16_gemm_v1.cu:1934-2025`
- risk: `Moderate. This is a bounded one-node_c change in the active PTX hot-band compute helpers, but it is easy to accidentally drift into a disguised reopen of consumer-order sweeps or handoff timing if the semantics are not held fixed.`
- metrics to re-check: `median_runtime_ms against the exact round-69 base at 25.49913597 ms, runs/*/ncu_metrics.csv hot-band gpu__time_duration.sum, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, correctness on all three fixed BF16 cases`

## Allowed edit surface

- `src/kernels/*`
- `src/runner/main.cpp` when the direction requires runner glue
- `include/*` when a stable interface change is required
- `CMakeLists.txt` only if the build path genuinely needs it
- `scripts/graph.py` or `scripts/sweep_fixed_main_tiles.py` only when the direction requires minimal workflow glue

## Required commands

- edit code for one direction only
- then run `python scripts/graph.py node_c --finalize`
- default behavior after a successful node_c finalize is to auto-run node_a

## Dirty working tree snapshot before node_c finalize

- no tracked dirty paths at prepare time
