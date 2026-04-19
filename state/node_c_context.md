# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `64x160 main + 64x96 tail widened fixed split`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_005301`
- round loop: `round 16/20`
- hypothesis: `Round 15 proved that trimming per-warp N baggage can reduce MIO throttle, but the 32x128 retile cratered because it doubled down on CTA count and drove DRAM to 78.82% with a register occupancy cap of 6. Keep the round-14 vectorized epilogue and widen the fixed-shape main kernel to 64x160 across the first 7680 columns so the hot region drops from 60 CTAs to 48 CTAs per row while preserving the proven 64x96 tail.`
- expected bottleneck: `Main-path operand movement and memory traffic from the too-narrow round-15 split; a 64x160 steady-state should improve reuse and reduce launch pressure without reopening generic tail overhead.`
- code locations: `src/kernels/bf16_gemm_v1.cu:28-79 add a 64x160 TileConfig alias and retune the fixed-shape main/tail constants for a 7680-column main region plus a 96-column tail, src/kernels/bf16_gemm_v1.cu:132-145 and 190-257 update B-stage copy counts, shared-stride math, and the tensor-core K-loop for the wider main-path specialization, src/kernels/bf16_gemm_v1.cu:265-287 and 320-339 keep the round-14 vectorized epilogue behavior, but launch a 48x101 64x160 main grid ahead of the existing 64x96 tail`
- risk: `Moderate. The wider B tile raises shared footprint and live fragment count, but it is the cleanest widened-main follow-up because it reduces CTA count without introducing an extra middle cleanup stage.`
- metrics to re-check: `median runtime, TFLOP/s, dram__throughput.avg.pct_of_peak_sustained_elapsed, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, launch__occupancy_limit_registers`

## Allowed edit surface

- `src/kernels/*`
- `src/runner/main.cpp` when the direction requires runner glue
- `include/*` when a stable interface change is required
- `CMakeLists.txt` only if the build path genuinely needs it

## Required commands

- edit code for one direction only
- then run `python scripts/graph.py node_c --finalize`
- default behavior after a successful node_c finalize is to auto-run node_a

## Dirty working tree snapshot before node_c finalize

- no tracked dirty paths at prepare time
