# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Half-Panel Correctness Repair With Single-Sourced Panel Identity`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_195407`
- round loop: `round 19/20`
- hypothesis: `Idea 7 / Register Reuse remains the primary family for round 19. Run 778a0b4 is still wrong, but it preserved the core half-panel breakthrough: 92 registers per thread, occupancy_limit_registers = 2, active warps about 32.9, tensor active about 43.7, and runtime already back to 30.236 ms. That is too much real signal to abandon with two rounds left. The next move is to make HalfPanelIdentity64x32 the only source of compact/shared/global column identity across staging, MMA tile selection, and export so the two 64x32 passes stop disagreeing about where a panel lives.`
- expected bottleneck: `Correctness is the immediate blocker; the likely failing surface is pass-local panel identity and output-column mapping inside the half-panel path, not raw throughput.`
- code locations: `src/kernels/bf16_gemm_v1.cu:270-321, src/kernels/bf16_gemm_v1.cu:700-771, src/kernels/bf16_gemm_v1.cu:946-1008, src/kernels/bf16_gemm_v1.cu:1045-1143, src/kernels/bf16_gemm_v1.cu:1635-1660`
- risk: `Medium. If the wrong-result source is a deeper cross-pass hazard instead of duplicated panel arithmetic, one more repair round may be needed. Any fix that regrows the live state above roughly 96 registers per thread risks collapsing occupancy back to 1 block per SM.`
- metrics to re-check: `correctness, median runtime, max_abs_err, launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
