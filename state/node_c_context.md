# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Restore Sweep-Backed 64x384 Full Hot Band`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_192106`
- round loop: `round 12/50`
- hypothesis: `Because `state/human_review.md` offers no competing round-12 idea family beyond the approval gate, accept the measured fixed-shape routing family for this loop: restore the sweep-backed `64x384` kernel over the full `7680`-column hot band and keep the `64x96` tail. The current default instead launches the reopened `128x128` PTX hot-band microkernel over the first `6400 x 7680`, and that branch is register-limited (`200` regs/thread, `16.64%` active warps, `48.09%` tensor activity), which lines up with the `+0.214911 ms` regression after reopening it.`
- expected bottleneck: `Main hot-band occupancy and tensor-core under-utilization caused by the default dispatch choosing the PTX `128x128` branch instead of the measured `64x384` full-band tile path.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1181-1233, src/kernels/bf16_gemm_v1.cu:1473-1567, src/kernels/bf16_gemm_v1.cu:2091-2137`
- risk: `The round-18 tile sweep was measured on an earlier accepted base, so removing the PTX branch could give back a real first-6400-row win if the restored `1181247` surface changed the tile-width ranking.`
- metrics to re-check: `median runtime / TFLOP/s, whether NCU still shows `bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel` in the default path, main-kernel `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`, main-kernel `sm__warps_active.avg.pct_of_peak_sustained_active`, main-kernel `launch__registers_per_thread``

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
