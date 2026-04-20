# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `80ceab789912da1c2cad1e92a16a158dfc2d6448`
- plateau counter: `3`
- round loop: `round 42/100`
- rounds remaining: `59`
- notes: `Node C build succeeded for round 42/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_015358_bf16_gemm_v1_80ceab7`
- run dir: `runs/20260420_015358_bf16_gemm_v1_80ceab7`
- correctness: `PASS`
- median runtime: `27.261951 ms`
- TFLOP/s: `26.667916 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_015436`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Ranking is explicitly centered on restoring the accepted round-38 PTX branch first: commit e26d834 at 25.974272 ms remains the best known active-path base, and round 41's producer-partition Pg2s/Async Copy variant is a clean reject because it added about 1.287679 ms while pushing barrier to 14.61% even though mio stayed at 0.48%. Human-idea audit for this round: Tiling is rejected as the primary family because both the real active 256x128/64x64 path and the 128x128x32 path already regressed far beyond the accepted 128x128 K16 PTX base; Coalescing Access is deferred because global->shared already uses 16-byte cp.async and the latest run is not DRAM or mio limited; Data Reuse is accepted only in the already-proven full consumer-side B-reuse form on the accepted PTX branch; Async Copy is accepted only after restoring that branch, while explicit producer partitioning is rejected for this round; Bank Conflict is accepted as the primary family because export-path shared traffic and short-scoreboard remain live; L2 Cache is deferred because grouped-order experiments were already explored and the current regression is not L2-led; Register Reuse is accepted only as a bounded warp-local tweak that preserves full B reuse; Pg2s is rejected for producer partitioning and deferred for non-partitioned sequencing cleanup; Ps2r is deferred to the bounded consumer-side direction; Stage is accepted only as a narrow steady-state sequencing cleanup at the current depth, while deeper staging or extra CTA coordination is rejected. The goal remains <20 ms, not merely matching the 25.917889 ms CUTLASS baseline, so the ranking favors the highest-ceiling families still consistent with the accepted PTX branch rather than another tiling reset.`
- dir_01: Restore Accepted PTX Branch And Tighten Export Path | bottleneck: Shared-memory export overhead and warp-local synchronization in the PTX c_shared round-trip, now showing up mainly as barrier and short-scoreboard stalls rather than mio or DRAM starvation.
- dir_02: Restore Accepted PTX Branch And Rewrite Steady-State Sequencing | bottleneck: CTA-level synchronization and cp.async orchestration overhead in the active PTX steady-state loop, expressed as barrier inflation even when memory-issue pressure is already low.
- dir_03: Restore Accepted PTX Branch And Apply A Narrow Consumer-Side Tweak | bottleneck: Warp-local fragment residency, consumer-side bank behavior, and short-scoreboard pressure inside the PTX 64x64 accumulate path.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `0.056383 ms`, `1.002175x` slower than CUTLASS
