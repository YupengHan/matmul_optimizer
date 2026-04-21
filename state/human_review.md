# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 7/100` with `94` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_223553`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 7/100 audit: restoring the historical PTX grouping window and accepted-surface prologue delivered a real win, dropping runtime from 24.535040 ms to 24.180656 ms. That says the search should bank the restored surface and spend the next budget unit on a new family rather than immediately iterate the same restore knob again. The restored run still shows the familiar signature: 16.62% active warps, register-limited occupancy, barrier 5.48%, and long-scoreboard 7.17% with low DRAM pressure. That makes the PTX export-address/control surface the best next bounded family, with a second PTX control-path exploit and one off-branch export-scratch family kept alive behind it.`
- dir_01: Apply Only A Minimal PTX Export Address Cleanup | bottleneck: PTX export-side address/control overhead and scratch bookkeeping on the restored accepted hot-band surface.
- dir_02: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual PTX hot-band control-path overhead on the restored grouping surface, not another locality or macro-tiling miss.
- dir_03: Trim The Grouped-Row 128x128 Sibling Export Scratch To The PTX-Style Single Stage | bottleneck: Export scratch lifetime and writeback overhead on the grouped-row 128x128 sibling path, used as an off-branch fallback family.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
