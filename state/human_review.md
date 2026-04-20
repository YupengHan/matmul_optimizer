# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 16/50` with `35` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_235321`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 16: accepted as primary for this round are Async Copy, Pg2s, Ps2r, Data Reuse, and Stage because the new 128x128 family already proved the macro shape and exposed a stage-reuse race. Deferred are Coalescing Access and Bank Conflict because the failing 28.36 ms run showed low mio-throttle and low scoreboard pressure, so feed width and bank fixes are not the immediate limiter. Register Reuse is also deferred because the 128x128 family already lifted tensor active materially without a new register scheme. The L2 cache / block-order clue stays alive as a later experiment, but only after the hot-band branch is correct.`
- dir_01: Make the 128x128 hot-band stage reuse safe before the next cp.async overwrite | bottleneck: Barrier / stage orchestration inside the hot-band mainloop. The goal is to trade a controlled barrier increase for removing the hidden producer-consumer race while preserving the much higher tensor utilization of the 128x128 branch.
- dir_02: Reintroduce the 128x128x32 steady-state once the 128x128 family is correct | bottleneck: Pipeline depth and control overhead in the hot-band kernel. This targets stage efficiency rather than a new macro tile.
- dir_03: Add an L2-friendly block-order clue only after the hot-band kernel is correct and stable | bottleneck: L2 reuse / CTA launch order rather than shared-memory feed. This is a compiler-scheduling clue experiment, not a first-order correctness or tensor-pipeline fix.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
