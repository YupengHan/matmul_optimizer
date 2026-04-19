# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 13/20` with `8` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_002159`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `This diagnosis incorporates aggressive exploration and human-in-loop guidance.`
- dir_01: Rewrite shared fragment delivery to cut MIO pressure | bottleneck: Shared-memory fragment delivery and MIO saturation from the current CTA-wide staging plus warp-group B skew, not CTA barrier cadence.
- dir_02: Collapse the epilogue scratch and scalar writeback path | bottleneck: Epilogue/writeback overhead from shared scratch plus scalar output stores diluting tensor-core work.
- dir_03: Retile warp ownership to raise tensor density and active warps | bottleneck: Poor CUDA-core vs tensor-core work partitioning from the present CTA/warp tile shape, not synchronization frequency.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
