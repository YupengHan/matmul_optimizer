# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 2/30` with `29` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_215602`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 2/30 starts from a recovered and credible exploratory anchor again. Restoring the round-8 streaming-B branch recovered runtime to 30.618112 ms and restored the better feed-side profile: tensor active back up to about 38.56, barrier stall back down to about 6.56, short scoreboard about 6.72, `mio_throttle` about 0.33, and registers back to the pre-producer level. That confirms the loop should keep working from this branch rather than keep spending rounds on resets. The shared-permutation and producer-only staging variants are already known negatives, so the next best move is the next remaining high-ceiling step on top of the streaming-B consumer path: a one-fragment Ps2r lookahead. Dir_02 keeps the stronger global baseline option (`b13027c`) in reserve if this branch stalls again. Dir_03 covers the next non-feed family on the same branch by trimming the export path.`
- dir_01: Human idea Ps2r: one-fragment shared-to-register lookahead on the restored streaming-B branch | bottleneck: Residual shared-to-register feed latency inside the hot-band 64x64 micro-tile after the streaming consumer cleanup.
- dir_02: Reset to the best measured custom commit `b13027c` and port future experiments from there | bottleneck: Not an immediate micro-bottleneck attack; this is a better global baseline reset for later rounds.
- dir_03: Trim the hot-band export path on top of the restored streaming-B branch | bottleneck: Epilogue/export LSU and shared-memory round-trip overhead after the feed path has already been partially improved.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
