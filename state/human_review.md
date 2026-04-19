# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 5/5` with `1` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260418_213538`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Rebalance the warp tile split to recover active warps | bottleneck: Occupancy and latency hiding from register-limited resident warps, now exposed as low sm__warps_active together with elevated long_scoreboard and mio_throttle stalls.
- dir_02: Swizzle or pad shared tiles to reduce WMMA load MIO pressure | bottleneck: Shared-memory and fragment-load efficiency, expressed as high smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct despite only moderate DRAM and L2 throughput.
- dir_03: Deepen the async copy pipeline for the 2-warp CTA | bottleneck: Copy-to-compute overlap and long scoreboard stalls from a pipeline that is now too shallow for only two resident warps per CTA.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
