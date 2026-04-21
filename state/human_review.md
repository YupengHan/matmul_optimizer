# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `awaiting_direction_selection_for_node_c`
- round loop: `single-run` with `0` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_093739`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `The current kernel already matches the best historical PTX grouping surface at the source level, so this diagnosis avoids another replay cycle and focuses on real low-risk control-path tightening in the active 128x128 hot-band kernels.`
- dir_01: Hoist 128x128 Hot-Band Shared Offsets Out Of The Steady-State Loop | bottleneck: Warp-local shared-pointer arithmetic and loop-carried control overhead in the 128x128 hot-band steady state are stealing issue slots from tensor work.
- dir_02: Trim PTX 64x64 Export Address Math In The Hot-Band Epilogue | bottleneck: PTX export-side address generation in the 64x64 writer is adding integer/control overhead after the MMA loop.
- dir_03: Retime The 128x128 PTX Wait-Group And Consumer Barrier Handoff | bottleneck: The PTX 128x128 steady state may be overserializing cp.async wait-group completion and CTA-wide consumer handoff.

## Active direction

- selected direction: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve, use-recommended-direction, or select-next after node_b.`
