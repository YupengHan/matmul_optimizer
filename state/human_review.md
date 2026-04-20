# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 14/50` with `37` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_232652`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 14/50 incorporates the recorded CUTLASS NCU baseline directly. CUTLASS runs a 128-thread 128x128x32 multistage kernel with much higher tensor and DRAM utilization and almost no barrier pressure, while the current custom hot-band path remains stuck near 38% tensor active with 256 threads and k16 stages. The recommended next move is therefore a structural hot-band branch, not another local swizzle.`
- dir_01: Start a CUTLASS-shaped hot-band branch: 128x128 CTA, 64x64 warp tiles, 128-thread launch, and K32 staged mainloop | bottleneck: Feed/orchestration inefficiency from the current 256-thread hot-band structure rather than a single bank-conflict or epilogue detail.
- dir_02: Escalate directly to an explicit ldmatrix/mma.sync hot-band microkernel if the CUTLASS-shaped WMMA branch still underfeeds Tensor Cores | bottleneck: Tensor Core under-utilization caused by the current WMMA fragment delivery path.
- dir_03: Restore the accepted-correct implementation surface before continuing the search | bottleneck: Not a bottleneck attack; this is the reset path.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
