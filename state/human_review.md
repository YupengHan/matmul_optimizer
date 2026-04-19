# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `awaiting_direction_selection_for_node_c`
- round loop: `round 1/5` with `5` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_130817`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `This diagnosis intentionally keeps all three directions on the same human-directed 64x384 hot-band PTX microkernel branch. The 64x96 tail remains unchanged in every direction, and the round-18 sweep still anchors 64x384 as the right hot-band macro tile. Strong negative evidence from earlier warp specialization, producer straight-lining, and consumer-side B swizzle means the branch should not revert to generic WMMA cleanup or other old feed-path experiments; later rounds should refine the explicit PTX hot-band path instead.`
- dir_01: PTX hot-band microkernel branch with unchanged 64x96 tail | bottleneck: The dominant limiter is the WMMA hot-band control surface itself: it constrains fragment lifetime and instruction ordering, which keeps tensor issue diluted by feed/orchestration overhead even though the macro tile and tail split are already well chosen.
- dir_02: PTX phase 1 compute-core swap under current staging and tail split | bottleneck: Instruction selection and fragment scheduling inside the hot compute body, not the launch split and not the fixed 64x96 tail.
- dir_03: PTX register-first export and overlap-budget follow-through | bottleneck: The hot-band export path and c_shared round-trip still consume shared-memory and LSU budget that could otherwise support more overlap once the PTX branch owns accumulator residency.

## Active direction

- selected direction: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`
