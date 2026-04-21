# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Single-Source Warp Ownership End To End On The Half-Panel Branch`
- candidate id: `diagnosis_20260421_005735:dir_01`
- base run id: `20260421_005653_bf16_gemm_v1_0c534cb`
- primary family id: `historical::repair_the_256x128_half_panel_register_reuse_branch`
- planned action fingerprint: `restore_half_panel_single_sourced_ownership_snapshot_from_76622e3953ae33585df08f275e54bdd27fad9860`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260421_005735`
- round loop: `round 23/100`
- hypothesis: `Round 22 confirmed that the half-panel branch still attacks the right wall on the current machine. The result was bad overall, but the machine state moved exactly where the plateaued 24.16-24.18 ms surfaces do not: active warps rose to 32.92%, register occupancy stayed at limit=2, and long scoreboard dropped to 0.62%. The remaining blockers are now very explicit: correctness failed 0/3 and barrier climbed to 21.27%. That makes the next best move a precise continuation inside the same family, not a fresh family jump. The historical 76622e3 snapshot is that continuation: it single-sources warp ownership and panel identity end to end so the branch can keep the occupancy breakthrough while attacking the remaining overlapping-writer / ownership mismatch.`
- expected bottleneck: `Half-panel ownership and export correctness on top of a branch that already solved the live-state wall but still pays excessive synchronization.`
- code locations: `src/kernels/bf16_gemm_v1.cu:345-1066, src/kernels/bf16_gemm_v1.cu:1580-1676, src/kernels/bf16_gemm_v1.cu:1676-1813`
- risk: `High. This branch still fails correctness and the next step is another broad historical surface restore, but now the key occupancy signal has been reproduced locally.`
- metrics to re-check: `correctness pass rate across all 3 cases, launch__registers_per_thread, launch__occupancy_limit_registers, sm__warps_active.avg.pct_of_peak_sustained_active, smsp__warp_issue_stalled_barrier_per_warp_active.pct, end-to-end median runtime`

## Allowed edit surface

- `src/kernels/*`
- `src/runner/main.cpp` when the direction requires runner glue
- `include/*` when a stable interface change is required
- `CMakeLists.txt` only if the build path genuinely needs it
- `scripts/graph.py` or `scripts/sweep_fixed_main_tiles.py` only when the direction requires minimal workflow glue

## Implementation notes

- implement exactly one selected direction
- stay within the primary family by default
- if the implementation clearly crosses into another family, update `state/active_direction.json` and record `secondary_family_ids` before finalize
- if the implementation semantically drifts from the planned action, update `implemented_action_fingerprint`, `semantic_delta_tags`, or `actual_code_regions` in `state/active_direction.json` before finalize
- build failure is still recorded as a structured `state/latest_attempt.json` entry with `build_status=FAIL`

## Required commands

- edit code for one direction only
- then run `python scripts/graph.py node_c --finalize`
- default behavior after a successful node_c finalize is to auto-run node_a

## Dirty working tree snapshot before node_c finalize

- no tracked dirty paths at prepare time
