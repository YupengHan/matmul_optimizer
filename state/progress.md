# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `11e5daeb5a66a62b66c1d61a4bf59d47622a76ec`
- plateau counter: `13`
- round loop: `round 72/100`
- rounds remaining: `29`
- notes: `Node C is ready to implement dir_01 via recommended selection for round 72/100.`

## Latest measured custom run

- run id: `20260420_110307_bf16_gemm_v1_11e5dae`
- run dir: `runs/20260420_110307_bf16_gemm_v1_11e5dae`
- correctness: `PASS`
- median runtime: `25.746432 ms`
- TFLOP/s: `28.237676 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_110400`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Goal remains below 20 ms. The current reproducible exact base remains round 69 at 25.49913597 ms. Round 71 changed PTX issue grouping inside the 64x64 compute helpers by flattening the recursive column issue into an explicit Step 0/1/2/3 sequence while restoring the round-69 base. That improved relative to round 70 but still measured 25.7464323 ms, with tensor 47.67, dram 10.31, lts 30.78, barrier 6.47, long_scoreboard 4.18, and mio 3.24. That is sufficient evidence that this explicit PTX helper issue-grouping variant is not a win on the exact base and should now be treated as closed negative. Closed-negative families for this round therefore include: grouped_rows sweeps, snake launch-order locality, fixed-K peeling, export traversal changes, A-first refill, consumer-order sweeps, broad stage overexpansions, the narrow handoff-closure family, and the explicit helper issue-grouping variant just tested. Export-side second-sync removal remains non-primary, but export-lifetime from the exact base is still available as a bounded low-rank family. The accepted active exact-base surface remains: grouped_rows=8, right-left 64x64 PTX consume order, reversed PTX compute row-pair traversal, linear export traversal, one-sync steady-state handoff, B-first refill, active-loop unroll 2, and accepted helper shapes. Human-idea audit for this round: tiling is rejected as a main search family because grouped_rows retunes and broader tile changes are already closed negative, but an isolated 256x128 auxiliary-path schedule retune remains acceptable as a bounded side-path experiment rather than a reopened tile search; coalescing and wide global access are accepted as already implemented through the existing 16-byte async staging path; shared-memory reuse is accepted as the current base; async copy is accepted only in the exact K16 two-stage B-first form, while broad stage or handoff expansions remain closed negative; bank-conflict handling remains available only through a low-rank export-lifetime recheck on the exact base; L2 locality is rejected for ranking because snake launch-order locality is already closed negative; register reuse Right-Left-Right-Left is accepted as fixed exact-base behavior, while the explicit helper issue-grouping variant is now closed negative; Pg2s double buffer is accepted as already in place; Ps2r double buffer is accepted in the current helper stack and any remaining PTX helper-shape work must preserve exact accepted traversal semantics; stage and multi-buffer remain closed beyond the present exact baseline.`
- dir_01: Restore Exact Round-69 Base And Recheck Export Lifetime From There | bottleneck: Residual shared export lifetime and barrier cost on the active PTX hot-band path. This is no longer a high-ceiling family, but it is still the cleanest bounded move that touches the exact default path without reopening any already-closed PTX compute-order experiments.
- dir_02: Isolate The 256x128 Auxiliary Path And Retune Its Local Schedule | bottleneck: Auxiliary-path local scheduling and latency hiding inside the non-PTX 256x128 kernel, especially the exact K-loop unroll choice and its local sync cadence. This is not a claim that tiling itself should be reopened; it is a narrow schedule retune on an already-existing auxiliary kernel surface.
- dir_03: Preserve Exact Accepted Order And Try A Smaller PTX Helper-Shape Move | bottleneck: Warp-level helper overhead and instruction locality inside the PTX 64x64 compute stack, not a new consume-order search. The target would be helper shape, call layering, or inlining boundaries while preserving the exact accepted order semantics.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
