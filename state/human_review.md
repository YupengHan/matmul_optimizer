# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 6/100` with `95` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_222929`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `dir_03`
- diagnosis notes: `Round 6/20 audit: the round-5 B-first prologue staging tweak measured 24.535040 ms, only 0.015872 ms slower than the previous run, but it moved the wrong counters: active warps slipped from 16.60% to 16.49%, barrier rose from 5.18% to 5.33%, and long-scoreboard rose from 7.28% to 7.50% while registers stayed pinned at the same occupancy ceiling. That is strong evidence that another copy-order micro-tune is not the best immediate use of budget. The diagnosis therefore promotes the rehydrated register-pressure family to rank 1, keeps a narrower PTX export cleanup as the active-branch fallback, and preserves one historical PTX grouping-window restore as the restore-style fallback family. This uses the live queue expansion from round_history instead of letting the loop collapse back to only one or two families.`
- dir_01: Flatten PTX Hot-Band Compute Helpers To Reduce Register Pressure | bottleneck: Register-limited occupancy and weak latency hiding caused by helper-induced live ranges in the PTX hot-band compute path.
- dir_02: Apply Only A Minimal PTX Export Address Cleanup | bottleneck: PTX export-side address/control overhead and scratch management after MMA, rather than another feed-order or traversal issue.
- dir_03: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Inter-CTA locality and launch-order mapping on the accepted PTX surface, but explicitly as a restore fallback rather than the primary next attack.

## Active direction

- selected direction: `dir_03`
- selection mode: `approved`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
