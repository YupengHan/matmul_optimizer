# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 11/20` with `10` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260418_235617`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Rounds 10-14 are intentionally biased toward more aggressive experiments. This round is chasing the new bottleneck from a first-principles instruction-mix perspective: the 43.70 ms round-10 win increased math per barrier and dropped barrier stalls, but the hot 64x128 main kernel is now the clear frontier with MIO throttle at 41.76%, register-limited occupancy at 4 blocks/SM, and L1TEX/LSU request pressure near 82.8%. The three directions therefore favor structural feed and epilogue changes over small parameter nudges.`
- dir_01: Main-kernel producer/consumer cp.async pipeline | bottleneck: Main-path MIO/LSU issue saturation in the 64x128 feed pipeline, with residual CTA-wide handoff cost as a secondary limiter.
- dir_02: Scratch-free or vectorized BF16 epilogue for the 64x128 main path | bottleneck: Epilogue-side MIO and shared-memory round-trip pressure layered on top of an already LSU-saturated main kernel.
- dir_03: Retile the hot main kernel to cut live B-fragment and accumulator pressure | bottleneck: Register-limited occupancy and per-K-step B-feed MIO pressure caused by the four-fragment 64x128 warp organization.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
