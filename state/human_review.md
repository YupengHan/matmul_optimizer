# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 3/30` with `28` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_215936`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 3/30 starts from a branch that is directionally healthy but still fundamentally stuck on the register wall. The one-fragment B-side Ps2r lookahead built cleanly, preserved correctness, and improved runtime from 30.618112 ms to 30.592960 ms, but the gain is only about 0.025 ms and the headline profile barely moved: tensor active is still about 38.57%, active warps about 16.76%, `mio_throttle` is already low at about 0.33, short scoreboard remains about 6.74, and the hot-band kernel still uses about 167 registers per thread with `launch__occupancy_limit_registers = 1`. That means the loop has probably extracted most of the cheap B-feed cleanup available without changing the live working set. Recommended direction dir_01 therefore shifts to the user-provided register-reuse / phased-tiling family: keep the accepted 256x128 CTA and 64x64 warp geometry, but split the warp-local output columns into two mirrored 64x32 accumulator panels so the kernel can test whether reduced live accumulator footprint buys back occupancy and tensor activity. Dir_02 keeps the Ps2r family alive on the A side if the panelization looks too invasive, and dir_03 records the user-provided L2 traversal clue as a lower-priority structural experiment once the occupancy-side opportunities are exhausted.`
- dir_01: Human idea register reuse: phase the 64x64 hot-band warp tile into two 64x32 accumulator panels | bottleneck: Register-limited occupancy and warp-level live-fragment pressure in the hot-band PTX microkernel.
- dir_02: Human idea Ps2r: preload the next A row-pair while the current row-pair consumes the mirrored B stream | bottleneck: Residual shared-to-register latency on the A side inside the hot-band row-pair sweep after the B side has already been partially overlapped.
- dir_03: Human idea L2 cache clue: try a grouped CTA traversal for the 256x128 hot band | bottleneck: Potential L2 locality loss from the default CTA traversal over the fixed hot-band grid.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
