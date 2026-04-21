# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 5/50` with `46` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_182334`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 5/50 diagnosis anchored to run `20260420_182305_bf16_gemm_v1_e003c0e`, with the implementation surface already restored to the accepted best measured commit `2e4dd246f55b505bd095c42b62c56dc497c8fde1`. Human-review audit for this round: `state/human_review.md` currently lists no explicit user-provided idea-family bullets beyond the workflow gate, so there are no active queued human ideas to accept, defer, or reject one by one; the ranking is therefore driven directly by the latest measured evidence and the required raw-file history. That evidence is now decisive on the two most recent hot-band-local families: round 3/50 handoff retime regressed by 1.070592 ms, and round 4/50 export/live-range trimming regressed again to 25.52985573 ms while keeping the hot-band kernel pinned at 200 registers/thread and worsening long-scoreboard to 8.18%. Those two misses close narrow handoff and export trimming as primary follow-ups on the grouped-rows-4 winner. The next ranked families are therefore: accept fixed-shape 452-tile loop specialization as the primary move because it still attacks the dominant hot-band kernel without repeating the two closed micro-families; defer the 6144 seam as the best bounded measured launch-split fallback; reject broad fixed-main control as anything more than a tertiary audit branch because the old autotune ancestry is outweighed by much slower modern evidence on this PTX regime.`
- dir_01: Specialize The 452-Tile PTX Hot-Band Loop On The Restored Grouped-Rows-4 Base | bottleneck: Generic loop-control and stage-transition overhead inside the dominant 128x128 PTX hot-band kernel, which is still limiting tensor issue after the recent handoff and export micro-tunes failed.
- dir_02: Restore The 6144 Hot-Band/Peeled Seam As The Best Launch-Split Fallback | bottleneck: Boundary cost between the 128x128 PTX hot-band kernel and the peeled 64x384 follow-on path, especially whether the fixed 6400-row split leaves avoidable barrier-heavy work in the secondary kernels.
- dir_03: Keep The Broad Fixed-Main 64x384 Control Only As An Audit Branch | bottleneck: Broader dispatch-path and arithmetic-intensity tradeoff across the fixed-shape hot band, not the inner PTX hot-band microkernel itself.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
