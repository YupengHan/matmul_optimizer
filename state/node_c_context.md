# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Keep The Initial Prime Retime But Restore The Future Refill To B-Then-A`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_164308`
- round loop: `round 17/17`
- hypothesis: `Round 16/17 showed that the full prefetch retime improved the narrower refill-only variant from 25.67678452 ms down to 25.62406445 ms, but it still missed the accepted export base at 24.84582424 ms. That points to a mixed result inside the family: the initial A-then-B prime likely helps, while carrying A-then-B all the way into the future refill likely over-rotates and reintroduces barrier cost. The only remaining untested permutation in this family is the hybrid ordering where the initial two prime stages stay A-then-B but the steady-state future refill goes back to B-then-A, which also matches the nearby 128x128 PTX sibling path.`
- expected bottleneck: `Copy-pipeline handoff balance between long-scoreboard relief from the retimed initial primes and barrier pressure from the future-tile refill ordering in the PTX hot-band microkernel.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1882-1922, src/kernels/bf16_gemm_v1.cu:1995-2006, src/kernels/bf16_gemm_v1.cu:2031-2039`
- risk: `Medium. The prefetch family already had mixed results, but this is the last untested ordering permutation and it is a smaller step than reopening a broad launch-path control.`
- metrics to re-check: `correctness, median runtime, smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct, smsp__warp_issue_stalled_barrier_per_warp_active.pct, dram__throughput.avg.pct_of_peak_sustained_elapsed, sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`

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
