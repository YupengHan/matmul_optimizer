# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 10/100` with `91` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_232331`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `dir_02`
- diagnosis notes: `Round 10/100 audit: round 9 converted the grouped-row non-PTX 128x128 sibling from a queued family into a directly measured live branch. The dispatch switch measured 24.18073654 ms with correctness intact, which is only 0.00008011 ms slower than the accepted-base run at 24.18065643 ms and therefore effectively PASS_FLAT on the active search anchor, even though it still trails the 24.16435242 ms best-known PTX run by 0.01638412 ms. The right next move is no longer to recommend the sibling pivot itself, because that validation step is now complete. Instead, the diagnosis promotes the sibling export-scratch trim to rank 1 as the bounded follow-on on top of the newly validated sibling surface, while keeping two active-PTX fallback families alive behind it. The live queue rehydration remains in effect; these rankings intentionally follow the strongest currently open family representatives rather than only the newest diagnosis lineage.`
- dir_01: Trim The Grouped-Row 128x128 Sibling Export Scratch To The PTX-Style Single Stage | bottleneck: Shared export and writeback overhead inside the grouped-row non-PTX 128x128 sibling, especially the sibling branch's heavier export scratch lifetime after the hot-band dispatch has already moved onto that family.
- dir_02: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual PTX hot-band control-path overhead on the best-known 128x128 PTX surface, especially helper lifetime and consume-order friction that the export-address cleanup did not remove.
- dir_03: Steady-state Barrier / Handoff Retime | bottleneck: Residual wait-group and barrier cadence in the hot-band steady-state loop, either on the active PTX branch or as a scheduler lens for comparing the sibling follow-on.

## Active direction

- selected direction: `dir_02`
- selection mode: `approved`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
