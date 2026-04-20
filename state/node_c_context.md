# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Retune The Accepted Grouped-Row=8 PTX Hot Band Around Stage Cadence`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_074934`
- round loop: `round 49/100`
- hypothesis: `Round 47's grouped-row=8 PTX hot-band path remains the accepted best base at 25.529328 ms, and round 48 showed that keeping one more mirrored-column B fragment live is not the right next lever: mio_throttle only moved 4.77 -> 4.72 and lts throughput only moved 30.02 -> 30.11 while runtime regressed to 25.759745 ms. With DRAM still low at 10.35%, tensor activity only 48.21%, warps active only 16.64%, and barrier still 7.52%, the next highest-upside move is to keep the accepted grouped-row=8 traversal and shift to a structural stage/cadence experiment in the dominant 128x128 PTX hot-band kernel. The existing two-K staged 128x128 path is the most relevant template: borrow its stage turnover or wait/commit cadence, but do not reintroduce B-fragment lookahead as the main mechanism.`
- expected bottleneck: `Synchronization and steady-state K16 stage turnover in the dominant grouped-row=8 PTX hot-band kernel, which is still underfeeding Tensor Cores after the locality win.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1669-1806, src/kernels/bf16_gemm_v1.cu:1954-2028, src/kernels/bf16_gemm_v1.cu:151`
- risk: `This is the highest-upside but also the most structural option. A cadence change can raise shared-memory footprint, lengthen live ranges, perturb occupancy, or undo the current grouped-row=8 stability. The implementation must stay anchored to the accepted grouped-row=8 PTX path rather than reopening the failed B-fragment-live branch.`
- metrics to re-check: `median runtime and TFLOP/s against the 25.529328 ms accepted base and the <20 ms user target, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct, launch__shared_mem_per_block_allocated, launch__registers_per_thread`

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
