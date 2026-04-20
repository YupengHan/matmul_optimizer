# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 60/100` with `41` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_085737`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Anchored to latest measured run 20260420_085640_bf16_gemm_v1_f71a41f at 25.995744 ms. Use the accepted grouped_rows=8 + reversed row-pair traversal + one-sync handoff base as the starting point and keep rejected branches closed.`
- dir_01: Restore accepted base, then test mirrored hot-band column sweep | bottleneck: Bad instruction-flow and locality interaction from the failed row-pair-dependent column split, rather than the accepted base traversal itself.
- dir_02: Recover overlap behind the one-sync handoff | bottleneck: Residual latency in the handoff window between row-pair traversal and the next shared-memory/compute phase.
- dir_03: Small locality closure only | bottleneck: Minor cache/shared-memory locality losses rather than a structural scheduling problem.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
