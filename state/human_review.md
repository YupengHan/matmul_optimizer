# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 7/30` with `24` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_221629`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 7/30 starts from the same implementation surface as the previously measured best custom, although the latest remeasurement landed closer to 30.30 ms than 29.43 ms. The code surface is therefore stable enough to continue experimentation without another restore-only round. Recommended direction dir_01 now follows the user-provided bank-conflict / register-reuse guidance directly: keep everything footprint-neutral and warp-local, but reverse the 64x64 B-consumer sweep into a `Right Left Right Left` order so the hot-band PTX path tests a different operand-delivery pattern. Dir_02 keeps the fixed-shape stage-peeling idea in reserve for the hot-band loop, and dir_03 captures the remaining coalescing / async-copy ownership experiment.`
- dir_01: Human idea bank conflict: reverse the mirrored 64x64 B sweep into a `Right Left Right Left` order | bottleneck: Residual warp-local B delivery / bank behavior inside the 64x64 hot-band consumer path.
- dir_02: Human idea stage: peel the hot-band K loop into fixed-shape prologue / steady-state / epilogue | bottleneck: Fixed-shape control-flow and stage-transition overhead inside the hot-band pipeline.
- dir_03: Human idea coalescing + async copy: retune hot-band cp.async ownership into contiguous warp stripes | bottleneck: Global-to-shared staging issue regularity and instruction ownership rather than raw bandwidth.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
