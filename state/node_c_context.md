# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea: autotune fixed-shape main tiling across 10+ candidates`
- selection mode: `human_idea`
- source diagnosis id: `diagnosis_20260419_011317`
- round loop: `round 18/20`
- hypothesis: `The current optimization loop can jump to a new tiling family, but it lacks a fast empirical map of which fixed-shape main widths actually help on this GPU. Before another diagnosis round, compile support for a broad set of candidate main tile widths, run at least 10 concrete tiling sizes on the fixed 7680-column hot band, and use the measured timing curve to identify where the widened-main trend stops helping.`
- expected bottleneck: `Search-space blindness rather than a single micro-bottleneck: we need real timing data for multiple tile widths to understand the trade between CTA count, DRAM pressure, MIO throttle, and register pressure.`
- code locations: `src/kernels/bf16_gemm_v1.cu: add host-side fixed-shape dispatch support for multiple main tile widths, src/runner/main.cpp or scripts/*: add a sweep path that can run the benchmark repeatedly under different fixed-shape tile selections, state/*: persist the tile sweep results and distilled insights for later node_b consumption`
- risk: `Medium. The sweep infrastructure widens code surface and compile time, and very large tile widths may compile but launch poorly or fail resource checks.`
- metrics to re-check: `median runtime for each tested tile width, best-performing tile width and delta versus the current 41.53497696 ms baseline, trend between tile width and runtime, any build or launch failures encountered during the sweep`

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

- `scripts/graph.py`
- `src/kernels/bf16_gemm_v1.cu`
