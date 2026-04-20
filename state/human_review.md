# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 1/50` with `50` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_223457`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 1/50 starts from the current best custom measurement at 29.325824 ms. The hot-band kernel still dominates and recent copy / consumer changes mostly regressed, so the next defensible move is to attack the export side. Recommended direction dir_01 keeps the same accumulator layout and shared footprint but changes the 64x64 export batching from horizontal pairs to vertical pairs, which should reduce warp-sync count in the hot-band epilogue. Dir_02 is a strict best-commit re-anchor fallback, and dir_03 records that fixed-shape peeling should only be revisited after the export behavior becomes simpler.`
- dir_01: Trim the hot-band export path by batching 64x64 stores vertically instead of horizontally | bottleneck: Hot-band epilogue / export synchronization and shared-memory round-trip overhead.
- dir_02: Re-anchor explicitly at the current best custom commit before more export work | bottleneck: Workflow / baseline drift rather than a micro-bottleneck.
- dir_03: Revisit stage peeling only after export behavior is simpler | bottleneck: Fixed-shape control and epilogue interaction after export simplification.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
