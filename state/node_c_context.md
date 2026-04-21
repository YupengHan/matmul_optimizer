# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Trim The Grouped-Row 128x128 Sibling Export Scratch To The PTX-Style Single Stage`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_184841`
- round loop: `round 8/50`
- hypothesis: `The latest measured run 20260420_184822_bf16_gemm_v1_2ab9365 is effectively at parity with the accepted 2e4dd24 best: 24.44902420 ms versus 24.44441605 ms, with the hot-band kernel also nearly identical at 32.831584 ms versus 32.801760 ms. The new sibling path is already correct and preserves grouped-row traversal, but it still carries the generic two-stage `c_shared` export path: 26,112 B shared per block versus 22,016 B on the accepted PTX microkernel. The cleanest next move is to keep this sibling base and port the PTX-style single-stage per-warp export scratch lifetime into its store path, so the remaining gap can be chased through a bounded shared/export trim instead of another family pivot.`
- expected bottleneck: `The likely residual bottleneck is shared export/writeback overhead rather than math scheduling. If the single-stage export trim works, it should lower the sibling's shared footprint and reduce the tiny hot-band gap without harming the already-matched barrier and long-scoreboard profile.`
- code locations: `src/kernels/bf16_gemm_v1.cu:110-137, src/kernels/bf16_gemm_v1.cu:936-1068, src/kernels/bf16_gemm_v1.cu:1836-1948`
- risk: `Low-medium. This is a narrow refinement on a correct near-best base, but it touches the export path, so the main risk is reintroducing subtle writeback or lifetime bugs while chasing a single-digit-microsecond gain.`
- metrics to re-check: `correctness pass rate across all 3 cases, median_runtime_ms, hot-band kernel gpu__time_duration.sum, launch__shared_mem_per_block_allocated, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`

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
