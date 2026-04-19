# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 17/20` with `4` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_010436`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `This diagnosis builds directly on the successful round-16 widened-main 64x160 + 64x96 result at 42.56455994 ms.`
- dir_01: 64x192 main + 64x128 middle + 64x96 tail fixed split | bottleneck: The main bottleneck should remain tensor-core under-utilization in the dominant hot band, with barrier and MIO throttle caused by too many medium-width CTAs rather than raw DRAM bandwidth.
- dir_02: 64x256 super-main over 7680 columns with minimal cleanup launches | bottleneck: The likely limiter shifts from launch granularity to occupancy and register/shared pressure: the super-main tile may improve tensor utilization only if its larger block does not push the kernel into a lower-latency-hiding regime.
- dir_03: Keep 64x160 main and collapse the fixed-shape cleanup path | bottleneck: The hot band remains limited by the same tensor/barrier/MIO behavior as round 16, but the target here is residual fixed-shape cleanup overhead from the separate 64x96 tail path rather than a new tile-level compute schedule.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
