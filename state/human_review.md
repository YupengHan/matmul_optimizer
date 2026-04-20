# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 4/30` with `27` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_220618`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 4/30 starts from a run that is faster but invalid. The approved A-side Ps2r lookahead improved measured runtime from 30.592960 ms to 30.270464 ms and shortened the hot-band kernel from about 41.19 us to about 40.99 us, which means the underlying overlap idea may have real upside. At the same time, correctness failed on all three cases, registers ticked up again to about 168/thread, `launch__occupancy_limit_registers` stayed pinned at 1, barrier stall jumped to about 19.84%, and `mio_throttle` rose back to about 2.50. That profile does not justify continuing to layer new optimization ideas on top of the broken branch. Recommended direction dir_01 therefore focuses on repairing or falsifying the A-lookahead family itself: keep the same concept, but flatten the row-pair preload into an explicit fixed-shape implementation that avoids the current recursive fragment handoff. Dir_02 is the safe fallback restore to the last correct round-2 surface, and dir_03 preserves the user-provided L2 traversal clue for later once the branch is valid again.`
- dir_01: Repair the A-side lookahead as an explicit fixed-shape row-pair preload, then revalidate correctness | bottleneck: Implementation / codegen risk in the current A-side lookahead path, plus residual shared-to-register A-feed latency if the idea survives repair.
- dir_02: Restore the last correct round-2 branch `06eedc6` and continue from the validated streaming-B + B-lookahead surface | bottleneck: Not a direct micro-bottleneck attack; this is a branch repair to recover a correctness-valid baseline before the next experiment.
- dir_03: Human idea L2 cache clue: try a grouped CTA traversal only after the correctness path is stable again | bottleneck: Potential CTA traversal inefficiency and weak L2 locality across the hot-band grid once a correctness-valid branch is restored.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
