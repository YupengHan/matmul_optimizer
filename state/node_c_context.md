# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Human idea 5 fallback reset: restore the last correct accepted base before spending more rounds on the hot branch`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260419_210044`
- round loop: `round 4/10`
- hypothesis: `Round 2 proved the half-panel branch has real occupancy upside, but round 3 proved it is still not stable enough to justify continued blind repair: runtime regressed to 31.486 ms, correctness stayed 0/3, and local reruns of the same correctness case still moved the max-error index and value. With six more implementation rounds available after this diagnosis, the highest expected-value move is to stop paying debugging tax on an unstable branch and restore the last correct accepted base first. That gives the loop back a known-good runtime/correctness floor and frees the remaining budget to attack the correct branch with the user's warp-local B-consumer and feed-orchestration ideas instead of continuing to burn rounds on nondeterministic half-panel behavior.`
- expected bottleneck: `The immediate bottleneck is workflow risk, not another micro-metric: the current half-panel branch is still an incorrect and unstable implementation. Restoring the accepted base removes that blocker so the next rounds can optimize a correct kernel again.`
- code locations: `src/kernels/bf16_gemm_v1.cu, src/runner/main.cpp, include/runner_contract.h`
- risk: `This gives up the only live branch that pierced the 167-register wall. The tradeoff is deliberate: correctness and a clean baseline are worth more than one more speculative repair round when six rounds remain after the reset.`
- metrics to re-check: `correctness, median runtime, TFLOP/s, restored run id / commit, latest NCU summary on the restored base`

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
