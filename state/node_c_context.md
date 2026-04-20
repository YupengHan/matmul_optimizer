# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 7 Register reuse: demote Stage, restore the accepted hot-band control surface, then reorder the 12-fragment PTX sweep`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_182858`
- round loop: `round 11/20`
- hypothesis: `Stage no longer has enough measured evidence to remain primary. After four rounds, the family has one incorrect run, one catastrophic codegen miss, and two correct runs that both sit in the same ~35.7 ms neighborhood. Those correct runs slash barrier, long-scoreboard, and mio, yet still lose badly to the accepted base at 33.12844658 ms. That means feed/orchestration is not the limiting factor anymore. The better next family is warp-internal register reuse and issue order: restore the accepted 9bdc160-style hot-band control surface first, then change only the 12 named PTX accumulator traversal from the current monotone sweep to a right-left-right-left style order that tries to raise tensor issue efficiency without paying the Stage-family tax.`
- expected bottleneck: `Warp-local tensor issue efficiency and short-latency scheduling waste inside the 64x384 PTX hot sweep, not CTA-level pipeline overlap.`
- code locations: `src/kernels/bf16_gemm_v1.cu:323-408, src/kernels/bf16_gemm_v1.cu:592-646, src/kernels/bf16_gemm_v1.cu:898-1015`
- risk: `This direction requires demoting the current Stage control surface before the reuse-order change is even measurable. If the restore step is sloppy, the comparison becomes muddy. There is also a real chance that traversal order alone only buys a small gain if the accepted base is already near the local optimum for the current tile hierarchy.`
- metrics to re-check: `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_short_scoreboard_per_warp_active.pct, launch__registers_per_thread, sm__warps_active.avg.pct_of_peak_sustained_active, median runtime, correctness`

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
