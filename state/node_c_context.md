# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `PTX accumulator and export lifetime compaction to attack the 167-register wall`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_165923`
- round loop: `round 2/20`
- hypothesis: `Round 1 already gave the key negative evidence for this branch point: tightening full-width tile-pair fragment issue order by itself moved runtime only from 33.12844658 ms to 33.15251350 ms, with tensor, active warps, barrier, mio, and occupancy all essentially flat. That means the next sustainable move is not more issue-order massaging, but a change in compiler-visible live state. Keep the same 64x384 hot-band PTX microkernel and unchanged 64x96 tail, but compact the accumulator/export helper surface so fewer accumulator, B-fragment, and export temporaries stay live across the compute-to-store boundary. Concretely, shrink recursive/template helper lifetime, narrow temporary scope around the 12 named accumulator tiles, and make the paired export path drain smaller explicit slices instead of letting the whole tile-set and export helpers stay resident together.`
- expected bottleneck: `Register-limited occupancy and weak latency hiding are the main remaining bottlenecks; long scoreboard is now the more meaningful residual stall because barrier and mio are already low.`
- code locations: `src/kernels/bf16_gemm_v1.cu:239-402, src/kernels/bf16_gemm_v1.cu:442-495, src/kernels/bf16_gemm_v1.cu:801-818, src/kernels/bf16_gemm_v1.cu:950-956`
- risk: `Medium risk. If the refactor is only cosmetic, ptxas may still allocate about 167 registers and nothing material will move. This direction also has to stay away from the already-unhelpful tile-pair issue-order retightening, the prechecked pair-compaction path, and the regressed explicit half-panel compute split.`
- metrics to re-check: `launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, median runtime`

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

- `src/kernels/bf16_gemm_v1.cu`
