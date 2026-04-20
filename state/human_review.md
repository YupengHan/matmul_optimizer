# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 6/30` with `25` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_221410`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 6/30 starts from a negative but informative experiment. The grouped CTA traversal that was meant to hint better L2 locality preserved correctness and slightly improved the isolated hot-band kernel time, but it regressed end-to-end runtime by about 1.26 ms, so it is not a viable surface for continued optimization. Recommended direction dir_01 therefore restores the newly established best custom branch `5dd9f0d` before another family is tried. Dir_02 and dir_03 both stay aligned with the user-provided human ideas on top of that restored branch: first a warp-local bank/conflict consumer sweep that still respects the no-extra-shared rule, then a cp.async ownership retune if the consumer-side variant does not pay off.`
- dir_01: Restore the new best custom branch `5dd9f0d` and discard the grouped-CTA traversal | bottleneck: Not a new bottleneck attack; this is a branch reset after a structurally negative CTA-traversal experiment.
- dir_02: Human idea bank conflict: test a `Right Left Right Left` warp-local B consumer sweep on the restored best branch | bottleneck: Residual B-side shared-to-register delivery and bank behavior inside the 64x64 hot-band micro-tile.
- dir_03: Human idea coalescing + async copy: retune hot-band cp.async ownership after the restore | bottleneck: Global-to-shared staging instruction overhead and copy ownership regularity.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
