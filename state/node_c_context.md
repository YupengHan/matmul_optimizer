# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Explicit ldmatrix PTX microkernel with smaller hot-band live set`
- selection mode: `approved`
- source diagnosis id: `diagnosis_20260419_131829`
- round loop: `round 2/5`
- hypothesis: `The first PTX cut proved the branch is real, but the hot 64x384 kernel is still conservative: it uses inline PTX WMMA wrappers at src/kernels/bf16_gemm_v1.cu:231-299 and keeps the existing staging/export structure, while the hot kernel now sits at 172 registers/thread and only 16.69 active warps. The best next move is to push the PTX branch to explicit ldmatrix plus mma.sync control in the hot band and, at the same time, shrink live fragment residency by serializing narrower N micro-panels inside the same 64x384 CTA. That gives direct control over load order and lane mapping while attacking the occupancy=1 guardrail that is now more important than mio.`
- expected bottleneck: `Register footprint and live-fragment residency inside the current PTX hot-band compute body are limiting occupancy and latency hiding; explicit fragment control is needed to lower that footprint without abandoning the PTX branch.`
- code locations: `src/kernels/bf16_gemm_v1.cu:231-299, src/kernels/bf16_gemm_v1.cu:605-627, src/kernels/bf16_gemm_v1.cu:629-739, src/kernels/bf16_gemm_v1.cu:798-832`
- risk: `Switching to explicit ldmatrix/mma.sync requires correct lane mapping and accumulator layout. If the new microkernel is not carefully staged, it can either keep the same register footprint under a harder-to-debug implementation or break correctness before any occupancy gains materialize.`
- metrics to re-check: `launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, median runtime`

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
