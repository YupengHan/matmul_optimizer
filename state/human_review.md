# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 16/100` with `85` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_001509`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 16 treats the latest PTX control-path result as a flat-positive continuation rather than a decisive closeout: the branch improved the accepted-base runtime slightly but not enough to replace the best-known 24.164272 ms run or to promote the accepted base in search state. The absorbed restore/export-cleanup families stay filtered out on the current source, while grouped_rows=8 and the 256x128 pivot branch remain explicitly live because the user asked to repopulate the frontier from promising round_history states after the search-policy update.`
- dir_01: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual cp.async handoff and inner-loop control overhead in the active 128x128 PTX hot-band microkernel, not DRAM bandwidth saturation and not another restore-only action.
- dir_02: Restore accepted grouped_rows=8 hot-band consumer ordering | bottleneck: Grouped-row traversal and consumer-order locality in the PTX hot-band path, not the same steady-state wait/commit seam targeted by dir_01.
- dir_03: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: Geometry-level latency hiding and control amortization on the 256x128 hot-band path, not the current 128x128 PTX wait/commit seam.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
