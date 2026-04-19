# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 6/20` with `15` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260418_225935`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Replace the simple B-row skew with a warp-friendly shared-memory B swizzle | bottleneck: Shared-memory and MIO pressure on the B fragment load path inside the steady-state tensor loop
- dir_02: Retune the cp.async pipeline so the 4-warp CTA pays fewer full-block wait/sync penalties | bottleneck: Synchronization-limited overlap between async staging and MMA consumption in the steady-state mainloop
- dir_03: Bypass the shared epilogue scratch with a register-first BF16/vector store path | bottleneck: Epilogue LSU/MIO pressure and shared-footprint overhead from the `c_shared` round-trip

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
