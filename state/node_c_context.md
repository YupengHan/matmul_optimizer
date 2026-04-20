# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Keep the accepted 128x128 K16 kernel and apply an L2-friendly grouped CTA order on the hot band`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_001011`
- round loop: `round 21/50`
- hypothesis: `The hot-band kernel is now stable enough that the next credible upside is orthogonal to CTA-local staging. The user's L2-cache idea fits the current evidence: tensor active is reasonable, shared footprint is already minimized, and the remaining gap to CUTLASS may come from cross-CTA B reuse. A grouped traversal of the fixed 60x50 hot-band tile grid, similar in spirit to Triton-style grouped ordering, can keep neighboring launched CTAs on the same small set of B tiles for longer without changing the kernel's inner pipeline.`
- expected bottleneck: `L2 / B-tile reuse across CTAs rather than within-CTA shared-memory orchestration.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1635, src/kernels/bf16_gemm_v1.cu:1757`
- risk: `CUDA does not guarantee issue order, so the gain may be small or noisy. The mapping must also preserve full coverage of the fixed hot-band grid with no duplicate or skipped tiles.`
- metrics to re-check: `median runtime, lts__throughput.avg.pct_of_peak_sustained_elapsed, dram__throughput.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, correctness pass rate`

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
