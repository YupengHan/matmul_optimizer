# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 46/100` with `55` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_073212`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `- Round 45 moved the needle only slightly, from 26.955776 ms to 26.892288 ms, but it was a real compute-side improvement: tensor active 48.05 -> 48.24, warps active 16.58 -> 16.68, barrier 11.21 -> 8.48, short scoreboard 5.94 -> 2.03.
- The same run also exposed the new limiting side: mio_throttle 0.34 -> 4.26 and lts throughput 30.30 -> 25.45. That is why the priority call for round 46 is to switch first to grouped-row/L2 traversal, not to keep blindly squeezing live range with more B rereads.
- The user target remains sub-20 ms, not merely matching CUTLASS, so the ranking favors directions with larger structural upside over another tiny local register win.
- Coalescing Access: not the primary next family; the B path is already 16-byte aligned, and the sharper regression is in traversal/locality rather than obvious transaction packing.
- Data Reuse: this becomes the top family because grouped-row traversal can improve reuse of nearby B/L2 footprint across hot-band CTAs without undoing the round-45 compute gains.
- Async Copy: worth watching but not top-ranked by itself; cp.async is already present, so the next question is cadence and wait placement, not basic adoption.
- Bank Conflict: not the headline signal right now; barrier and short scoreboard improved, so there is no new evidence that bank conflicts overtook L2/feed locality.
- L2 Cache: explicitly promoted in priority. The lts throughput drop after the live-range win is the clearest reason to test grouped-row or traversal changes next.
- Register Reuse: still a valid family with positive signal, but it is now rank 2 because the latest gain already came with a feed-side penalty.
- Pg2s: global-to-shared movement is no longer missing, but its spatial ordering may still be suboptimal in the active PTX hot-band launch.
- Ps2r: the active PTX microkernel still pays for B-fragment/shared consumption patterns; any further live-range work must avoid making this path heavier.
- Stage: kept as rank 3. The stage family is still relevant, but after round 45 the evidence says feed cadence is a follow-up investigation, not the first move.`
- dir_01: Port Grouped-Row Traversal Into The Active PTX 128x128 Hot Band | bottleneck: L2 traversal and hot-band feed locality are now the limiting factor, expressed as elevated mio_throttle and weaker lts throughput after compute-side pressure was reduced.
- dir_02: Continue Live-Range Compression Only On The Compute Side | bottleneck: Residual register pressure and accumulator/export live range still cap warp readiness, but the route is only worthwhile if it preserves the current shared/B feed behavior.
- dir_03: Revisit Hot-Band Stage Cadence And Shared Feed Granularity | bottleneck: Shared-memory feed cadence, cp.async turnover, and Ps2r/ldmatrix-side issue pressure after the compute-side live-range trim.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
