# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 7 Register reuse: continue the half-panel family, but make it an end-to-end 64x32 pass with explicit half-panel export mapping and compact B staging`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_192859`
- round loop: `round 17/20`
- hypothesis: `Round 16 is not a normal negative sample. The hot 256x128 kernel punched through the old register wall: registers per thread dropped from 167 to 93, occupancy_limit_registers rose to 2, active warps nearly doubled to 32.98, and tensor active rose to 42.01. That signal is too strong to discard with only four rounds left. But the current implementation only made the accumulator half-width; it did not make the whole pass half-width. The code still stages a full 128-column B tile for each pass via stage_b_shared_tile_async<FixedHotBandTile256x128>(), doubling feed cost, and the half-panel export path is still expressed through a shifted base pointer rather than an explicit HalfPanelColBase-aware mapping. The next move should therefore continue the family, but repair it as an end-to-end half-panel path: make the export/store helpers explicit about HalfPanelColBase so correctness is auditable, and add a pass-local compact B staging helper that copies only the two active 32-column warp-group slices for each half-panel pass. That directly addresses both observed failures: correctness and the new feed tax.`
- expected bottleneck: `Broken half-panel orchestration: correctness risk in the pass-local export mapping plus excessive shared/global feed from replaying full-width B staging for both half-panel passes.`
- code locations: `src/kernels/bf16_gemm_v1.cu:622-699, src/kernels/bf16_gemm_v1.cu:874-934, src/kernels/bf16_gemm_v1.cu:970-1048, src/kernels/bf16_gemm_v1.cu:1507-1565`
- risk: `This is the highest-ceiling path, but it is also the most delicate. The compact B staging must preserve the two warp-group column slices correctly, and the export fix must not introduce another off-by-panel mapping error. If either piece is wrong, correctness will still fail.`
- metrics to re-check: `correctness cases, median runtime, launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed, dram__throughput.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
