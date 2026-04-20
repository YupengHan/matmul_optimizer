# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 6/50` with `45` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_225949`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 6/50 still shows an incorrect but faster peeled steady-state: the main 256x128 hot-band kernel improved again to about 40.131 ms, which strengthens the case that the control-flow idea is sound but the shared peeled schedule is not safe across both tile configs. The recommended next move is therefore dir_01: split the behavior by TileConfig and keep the peeled schedule only on the dominant 8-warp main hot band while restoring the residual 64x128 path to the proven generic loop.`
- dir_01: Apply peeled steady-state only to the 8-warp 256x128 hot band and leave the residual 64x128 path on the proven generic loop | bottleneck: Main hot-band control overhead is still the target, but correctness risk is likely concentrated in the smaller residual 64x128 variant rather than the dominant 256x128 kernel.
- dir_02: Re-anchor on the accepted-correct surface and push warp-local Ps2r plus right-left register reuse | bottleneck: Per-warp operand delivery and register reuse inside the 64x64 PTX microkernel.
- dir_03: Revisit a light L2-friendly logical CTA swizzle after the correctness branch settles | bottleneck: Inter-CTA L2 locality across hot-band B tiles.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
