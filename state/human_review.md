# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 17/50` with `34` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_235645`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 17: accepted as primary are Stage, Async Copy, Pg2s, Ps2r, and Data Reuse because the corrected 128x128 path established that orchestration, not macro tiling, is what unlocked the new best custom runtime. Tiling 256x128 with 64x64 warp tiles is deferred because the 128x128 family has not yet been fully exploited and already beats the prior best custom result. Coalescing Access and Bank Conflict are deferred again because mio-throttle and scoreboard pressure are not the dominant signals in the corrected run. Register Reuse is also deferred because the current gain came from stage timing rather than a new register schedule. The L2 cache / block-order clue remains a valid later experiment, but only after the hot-band pipeline is stable.`
- dir_01: Re-enable the 128x128x32 hot-band steady-state with the proven consume-before-overwrite fence | bottleneck: Mainloop control and overlap efficiency in the corrected 128x128 family. The target is to raise tensor active back toward the earlier incorrect K32/K16 peaks without reopening the shared-stage race.
- dir_02: Tighten the K16 consume fence instead of fencing every iteration with a full CTA barrier | bottleneck: Barrier overhead inside the corrected K16 mainloop rather than memory bandwidth or a macro-tile limitation.
- dir_03: Try an L2-friendly CTA-order clue only after the corrected hot-band pipeline stabilizes | bottleneck: L2 reuse and block-issue locality rather than tensor-core delivery within a CTA.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
