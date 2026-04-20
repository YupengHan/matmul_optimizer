# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 73/100` with `28` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_111736`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Goal remains <20 ms. The current reproducible exact-base neighborhood is round 69 at 25.49913597 ms; round 72 measured 25.59897614 ms after removing the second export-side syncwarp again, so export-lifetime recheck is also closed-negative as a primary direction in this regime. Current profile still looks compute/schedule limited rather than bandwidth limited: tensor 47.95%, SM throughput 47.47%, warps_active 16.60%, DRAM 10.38%, L2 30.98%, barrier 6.54%, long_scoreboard 4.19%. That makes more barrier/lifetime surgery a weak bet and shifts ranking toward the remaining schedule-shape families. Human-idea audit: tiling 256x128/64x64 remains open only through the auxiliary 256x128 family; coalescing and wide global access are already substantially covered and do not read as primary at 10.38% DRAM; shared-memory reuse is already built into the accepted layouts; async copy and Pg2s double buffer are already present on the 256x128 auxiliary kernel; bank-conflict handling lacks a strong profile signal and stays deferred. L2 cache swizzle and launch-order locality are rejected for this round because snake mapping regressed; register reuse keeps the accepted right-left consume order plus reversed row-pair traversal and rejects further consumer-order sweeps; Ps2r double buffer as extra-live lookahead is closed-negative, so only semantics-preserving helper-shape fallbacks stay open; broad stage or multi-buffer expansion and narrow handoff closure remain rejected.`
- dir_01: Retune The Auxiliary 256x128 Hot-Band K-Loop Schedule | bottleneck: Compute scheduling and latency hiding on the auxiliary 256x128 hot-band path, not DRAM bandwidth.
- dir_02: Flatten PTX Hot-Band Accumulate Helpers Without Changing Consume Semantics | bottleneck: Register allocation and compiler scheduling friction inside the active PTX hot-band consume path.
- dir_03: Flatten PTX Export Helper Shape While Preserving Exact Sync And Linear Order | bottleneck: Minor export-side instruction overhead and register pressure, not barrier lifetime.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
