# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 5/20` with `16` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_222244`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 5/20 audit: round 4's grouped-CTA traversal probe regressed from 24.177664 ms to 24.519168 ms, while the active PTX hot-band kernel still shows the same basic signature: 200 registers/thread, register-limited occupancy at 2 CTAs per SM, only 16.60% active warps, 48.36% tensor-pipe activity, and very low DRAM pressure. That rejects CTA traversal/locality as the primary family for the next round and puts the focus back on the PTX microkernel's control-path and live-range pressure. Because the recent search-policy update thinned the live queue, the ranking also pulls in two historically strong families from round_history: a register-pressure/helper-flattening branch and a restore of the best measured PTX grouping window. The 256x128 pivot family stays deferred after its earlier loss.`
- dir_01: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual PTX hot-band control-path overhead and live-range pressure inside the current 128x128 microkernel, not global bandwidth or another CTA-ordering miss.
- dir_02: Flatten PTX Hot-Band Compute Helpers To Reduce Register Pressure | bottleneck: Register-limited occupancy and weak latency hiding driven by helper structure and live-range expansion in the PTX hot-band compute path.
- dir_03: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Inter-CTA locality and launch-order mapping on the accepted PTX surface, but only as a historical restore fallback rather than the primary bottleneck attack.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
