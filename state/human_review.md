# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 1/30` with `30` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_215124`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 1/30 starts from a bad exploratory endpoint rather than a trustworthy optimization anchor. The latest measured branch (`dfd7960`) is correctness-stable but clearly negative: runtime regressed to 32.758783 ms, the hot-band kernel slowed to about 47.99 us, tensor active collapsed to about 33.2%, barrier stall jumped to about 27.97%, and registers exploded to about 222/thread. That means the minimal producer-only staging variant is not a viable baseline for another 29 rounds. The first move should therefore be a reset to a stronger implementation surface before spending more rounds on new ideas. Among recent branches, the restored round-8 streaming-B path is the best exploratory anchor because it was the last family with a clean positive feed-side signal while keeping registers and shared memory flat. Recommended direction dir_01 therefore restores the round-8 streaming-B implementation surface, re-establishes that branch as the working baseline, and only then resumes B-feed exploration. Dir_02 keeps the stronger global objective in view by offering a reset to the best measured custom commit, while dir_03 is the highest-ceiling direct follow-up once the streaming-B branch is restored.`
- dir_01: Restore the round-8 streaming-B branch before continuing exploration | bottleneck: Not a micro-bottleneck change; this is a branch reset to remove a clearly negative orchestration experiment and recover the last good B-feed baseline.
- dir_02: Reset to the best measured custom commit `b13027c` and re-anchor the loop there | bottleneck: Not a direct bottleneck attack; this is a global baseline reset to the best measured implementation surface.
- dir_03: After restoring round 8, add one-fragment Ps2r lookahead on the streaming-B path | bottleneck: Residual shared-to-register feed latency inside the hot-band 64x64 micro-tile after the round-8 consumer cleanup.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
