# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 12/20` with `9` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_000749`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Aggressive exploration round 12/20 with human-in-loop guidance: do not recycle the round-11 producer/consumer cp.async path unchanged; prefer the recommended structural pivot from restored base 01d0040 unless a human explicitly approves a higher-risk alternative.`
- dir_01: Stage 32-wide K macro-tiles so each sync feeds two MMA slices | bottleneck: Tensor-core underfeed from too little MMA per staging/synchronization episode in the fixed-shape main loop.
- dir_02: Replace the WMMA row-major feed path with ldmatrix/mma.sync plus a tensor-core swizzle | bottleneck: Hot-path instruction mix and shared-fragment feed overhead that underfeeds tensor issue even when data is resident.
- dir_03: Split or eliminate the c_shared epilogue round-trip | bottleneck: Epilogue-side scalar, shared-memory, and MIO work polluting the tensor kernel's instruction mix.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
