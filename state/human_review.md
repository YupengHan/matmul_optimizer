# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `awaiting_direction_selection_for_node_c`
- round loop: `round 5/5` with `1` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_125849`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Ranking is against the restored 19f846e baseline at 36.371967 ms. Round 1 warp specialization, round 3 producer straight-lining, and round 4 consumer-side B swizzle remain strong negative evidence and rule out further B-feed or occupancy-collapsing follow-ons. The round-18 autotune sweep still anchors 64x384 as the correct macro tile, so dir_01 is framed explicitly as epilogue budget for overlap: reduce c_shared/export cost only insofar as the saved bytes can buy more useful A/B overlap on the hot peeled kernel.`
- dir_01: Tile384 epilogue budget for overlap | bottleneck: The limiting factor is overlap budget inside the 64x384 peeled kernel: shared-memory allocation and epilogue round-trip pressure leave the hot loop underfed, which shows up as persistent mio throttle and only middling tensor activity despite low DRAM pressure.
- dir_02: Retimed two-stage recycle in the peeled hot loop | bottleneck: Barrier and issue-slot dilution inside the fixed peeled steady-state loop, not global memory bandwidth and not the macro tile width.
- dir_03: Fixed-shape peel and export cleanup for the 64x96 tail | bottleneck: Residual fixed-shape overhead in the generic tail kernel, especially generic control flow and narrower export/store handling rather than hot-band feed mechanics.

## Active direction

- selected direction: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`
