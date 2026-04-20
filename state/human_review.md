# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 49/100` with `52` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_074934`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `- Accepted base: round 47's grouped-row=8 PTX hot-band path is still the accepted best base at 25.529328 ms (`20260420_074331_bf16_gemm_v1_17a33b2`).
- Negative result to carry forward: round 48's PTX B-fragment lookahead / rolling-window idea only moved `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct` from 4.77 to 4.72 and `lts__throughput.avg.pct_of_peak_sustained_elapsed` from 30.02 to 30.11, but runtime regressed from 25.529328 ms to 25.759745 ms. Treat this B-fragment-live Ps2r path as a negative result for now and stop digging it next round.
- Hotspot weighting: the dominant cost is still `bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_ptx_microkernel<(int)452>` at `gpu__time_duration.avg = 32.892736 ms`; the peeled 64x384 path is `0.872288 ms` and the tiny tail kernel is `0.918144 ms`, so ranking stays centered on the grouped-row=8 PTX hot band.
- Coalescing Access: not the lead family now. The grouped-row=8 accepted base already harvested the obvious access-order win, so another generic coalescing pass is lower value than a structural hot-band change.
- Data Reuse: still positive. Round 47 proved that grouped-row traversal improved reuse enough to lower DRAM and raise L2, which is why dir_02 remains in the set.
- Async Copy: already present and functional through `cp.async`; the next question is cadence and wait/commit turnover, not whether to add async copy. That is why dir_01 is framed around stage cadence rather than a generic pg2s rewrite.
- Bank Conflict: not the first move. The detailed CSV shows notable `l1tex` traffic, but not a dominant bank-conflict spike large enough to outrank stage or accepted-base traversal work.
- L2 Cache: still relevant, but now secondary. The accepted base already captured the biggest locality gain, so L2 work should be a narrow grouped-row=8 refinement rather than another broad rewrite.
- Register Reuse: still a live family only if it avoids the failed extra-B-live variant. If revisited, it should target A-side or export lifetime, which is why it is ranked third.
- Pg2s: no longer the main blocker. DRAM is only 10.35% on the regressed round-48 run, so the next round should not spend itself on a new global-to-shared mechanism.
- Ps2r: explicit conclusion for this round is to pause the B-fragment lookahead family. The measured benefit was below noise while runtime regressed.
- Stage: this is now the most worthwhile next family because tensor activity is still only 48.21%, warps active are still only 16.64%, barrier is still 7.52%, and the repository already contains a two-K staged 128x128 reference path to borrow from.
- Next-round priority statement: 1) grouped-row=8 remains the accepted base, 2) B-fragment lookahead should stop here, 3) the next most worthwhile direction is dir_01, a stage/cadence retune on top of the grouped-row=8 PTX hot band.
- Target framing: the user target remains <20 ms, not merely staying ahead of CUTLASS.`
- dir_01: Retune The Accepted Grouped-Row=8 PTX Hot Band Around Stage Cadence | bottleneck: Synchronization and steady-state K16 stage turnover in the dominant grouped-row=8 PTX hot-band kernel, which is still underfeeding Tensor Cores after the locality win.
- dir_02: Keep Grouped-Row=8 And Probe Only Incremental Traversal Or L2 Reuse Refinements | bottleneck: Residual cross-CTA locality and L2 reuse efficiency in the grouped-row=8 PTX hot band after the main DRAM/coalescing gain has already been harvested.
- dir_03: Trim A-Side Or Export Live Range Without Keeping Extra B Fragments Live | bottleneck: Residual operand and export live-range pressure inside the PTX 128x128 hot-band microkernel, which may still suppress warp readiness even after the locality improvement.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
