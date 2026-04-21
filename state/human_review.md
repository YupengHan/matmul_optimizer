# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 29/100` with `72` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_012211`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 29 switches the ranking rule from local plateau chasing to structure-first search. On the latest measured run, the hot-band PTX kernel still dominates at about 32.69 us with 200 registers per thread, 22,016 B shared memory per block, occupancy limit registers=2, and only 16.59% active warps. DRAM is only 9.77%, so the bottleneck is not bandwidth. The search therefore treats the 24.16-24.18 ms cluster as a noise-band plateau and ranks directions by whether they can break the residency wall instead of whether they can replay another small control-path delta.`
- dir_01: Force 3-CTA Residency On The PTX 128x128 Hot Band | bottleneck: Register-limited occupancy and latency hiding in the 128x128 PTX hot-band kernel, not global bandwidth.
- dir_02: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and steady-state staging efficiency inside the 256x128 hot-band path, plus barrier overhead created by the old half-panel ownership split.
- dir_03: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Known register-limited plateau on the accepted PTX hot-band surface.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
