# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 31/100` with `70` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_013500`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 31 is a recovery diagnosis after two informative but clearly negative aggressive probes. The round-29 launch-bounds probe reduced the hot-band register budget from 200 to 168, raised occupancy_limit_registers from 2 to 3, and increased active warps to 24.77%, but barrier stall jumped to 10.97%. The round-30 128x128x32 follow-on kept 168 registers but raised shared memory per block to 43,008 B, which collapsed active warps back to 16.58% and regressed the hot-band kernel to 38.09 us. The search should therefore restore the exact PTX anchor now, then reuse the lessons from these two rounds to choose the next aggressive branch from a clean base.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Known register-limited plateau on the accepted 128x128 PTX surface, used here as a recovery anchor rather than a discovery move.
- dir_02: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and synchronization strategy in the 256x128 hot-band path, plus correctness-sensitive output ownership.
- dir_03: Trim Microkernel Barriers Without Reintroducing Shared-Memory Blowup | bottleneck: Barrier cadence inside the single-K 128x128 PTX microkernel while preserving the lower shared-memory footprint.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
