# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 74/100` with `27` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_112500`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Latest measured run: 24.69619179 ms with tensor active 48.21, barrier 6.38, long scoreboard 3.74, mio 3.33, and launch__occupancy_limit_registers = 2. That reads as compute/schedule limited with a register ceiling, not DRAM bound. Human-idea audit for this round: register-pressure reduction is accepted as the primary family because the profile is occupancy-limited; auxiliary 256x128 scheduling is accepted as a separate bounded family because the previous round already improved that path; export helper cleanup is deferred to low rank because barrier is present but not dominant; coalescing / global-memory widening is deferred because DRAM is only 9.73%; shared-memory / bank-conflict work is deferred because the profile does not show a strong shared-memory stall signature; launch-order locality is rejected for now because the evidence does not point to it and prior snake-style locality work regressed.`
- dir_01: Flatten PTX Hot-Band Compute Helpers To Reduce Register Pressure | bottleneck: Register pressure and compiler scheduling friction inside the active PTX hot-band compute path, which is consistent with launch__occupancy_limit_registers = 2 and the low achieved warps-active number.
- dir_02: Revisit The 256x128 Auxiliary Hot-Band Path As A Separate Schedule Family | bottleneck: Compute scheduling and latency hiding on the auxiliary 256x128 hot-band path, not DRAM bandwidth.
- dir_03: Trim PTX Export Helper Shape Without Changing Store Semantics | bottleneck: Residual export-side instruction overhead and register clutter around the PTX writeback path, not global memory bandwidth.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
