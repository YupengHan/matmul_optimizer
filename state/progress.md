# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `778a0b475a3fbcfd5a0f3fecc8381784fa832256`
- plateau counter: `3`
- round loop: `round 19/20`
- rounds remaining: `2`
- notes: `Node C build succeeded for round 19/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_195339_bf16_gemm_v1_778a0b4`
- run dir: `runs/20260419_195339_bf16_gemm_v1_778a0b4`
- correctness: `FAIL`
- median runtime: `30.236128 ms`
- TFLOP/s: `24.044726 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `ready_for_finalize`
- diagnosis id: `diagnosis_20260419_195407`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 19 decision: continue-family on the half-panel 64x32+64x32 branch, with Idea 7 / Register Reuse as the primary family. Run 778a0b4 is FAIL, but it still holds 92 regs/thread, occupancy_limit_registers = 2, active warps about 32.9, tensor active about 43.7, and 30.236 ms runtime, so the branch looks incomplete rather than invalid. With only rounds 19 and 20 left, the honest path is to repair correctness first while preserving that machine state, then convert the surviving signal into lower feed tax.
Human idea audit for this round:
1. Tiling - accept-now as the outer 256x128 CTA and 64x64 warp shell; round 18 main-tile sweep and rounds 13-15 already proved this structural shell, so do not reopen macro tiling now.
2. Coalescing Access - defer; DRAM throughput is only about 21 percent and cp.async already uses 16-byte accesses, so coalescing is not the current main wall.
3. Data Reuse - accept-now as dir_02; both half-panel passes still replay the same A sweep, so reuse across the two passes is the cleanest next feed-side ceiling after correctness.
4. Async Copy - defer; async copy is already present and the current issue is duplicated use of it, not absence of it.
5. Bank Conflict - accept-now only as the bounded dir_03 backup; compact panel bank/layout cleanup is plausible, but it should not outrank correctness repair or shared-A reuse.
6. L2 Cache - reject-for-this-round; nothing in the latest profile says L2 is the limiting factor.
7. Register Reuse - accept-now and primary; the half-panel split is exactly what opened the 92-register, 2-block-per-SM, 32.9-active-warp regime.
8. Pg2s - accept-now as part of dir_02; the next producer-side improvement should be one staged A tile feeding both half-panels instead of two independent passes.
9. Ps2r - reject-for-this-round; the old ps2r family gave mixed signal and the current branch is not dominated by the same long-scoreboard signature anymore.
10. Stage - reject-for-this-round; the stage family changed the machine state before, but its corrected versions stayed around 35.7 ms and no longer justify primary ranking.
Ranking rationale: dir_01 preserves the strongest surviving path toward the 20 ms goal while fixing the only blocker that still invalidates the result. dir_02 is the highest-ceiling next step once correctness is restored because it removes the duplicated A producer tax beneath the new occupancy regime. dir_03 stays inside the same family as a lower-risk cleanup if the branch becomes correct but still carries shared-bank and short-scoreboard residue.`
- dir_01: Half-Panel Correctness Repair With Single-Sourced Panel Identity | bottleneck: Correctness is the immediate blocker; the likely failing surface is pass-local panel identity and output-column mapping inside the half-panel path, not raw throughput.
- dir_02: Twin-Panel Shared-A Reuse Inside One K Sweep | bottleneck: Duplicated A-side staging and shared/LSU traffic from running two full half-panel passes over K, rather than reusing one staged A tile across both panels.
- dir_03: Compact Panel Shared and Export Bank Cleanup | bottleneck: Residual short scoreboard and shared-bank pressure inside the compact 64x32 B-load and export path, which is now more visible because long scoreboard and mio are already low.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `4.134879 ms`, `1.159538x` slower than CUTLASS
