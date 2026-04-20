# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `786b3e4e1c7f3af5172b6e3b88e32251bd72c972`
- plateau counter: `7`
- round loop: `round 2/10`
- rounds remaining: `9`
- notes: `Node C build succeeded for round 2/10. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_203259_bf16_gemm_v1_786b3e4`
- run dir: `runs/20260419_203259_bf16_gemm_v1_786b3e4`
- correctness: `PASS`
- median runtime: `30.415296 ms`
- TFLOP/s: `23.903086 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_203505`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 2/10 diagnosis pivots on one hard correction: round 1 optimized the residual `bf16_gemm_v1_tensor_core_fixed_peeled_kernel`, but the dominant runtime is still the separate `bf16_gemm_v1_tensor_core_fixed_hot_band_256x128_kernel<(int)452>` at about 41.03 us, 167 registers/thread, shared 42.496 KiB, and occupancy limited by registers. That means the round-1 regression was mostly a target-selection miss, not evidence against live-set reduction itself. Human-idea audit for this round: `Tiling` is deferred because the current bottleneck is not a lack of CTA coverage but a live-set wall inside the chosen hot tile; `Coalescing Access`, `Data Reuse`, and `Async Copy` are accepted as background constraints but not as the primary change, since the current kernel already uses wide 16-byte cp.async staging and DRAM throughput remains modest; `Bank Conflict` is accepted only in the warp-local consumer-scope form and explicitly rejected in CTA repack form; `L2 Cache` is deferred because the profile is not L2-saturated; `Register Reuse` is the primary accepted family because the hot kernel is still at 167 regs/thread and one-block occupancy; `Pg2s` and `Stage` are accepted as secondary structure choices that must support, not replace, the live-set cut; `Ps2r` is accepted in the sense that the chosen direction serializes the consumer working set so shared-to-register feed can stay ahead of mma. Recommended direction `dir_01` is therefore the highest-upside, highest-relevance move for round 2: port the 64x32 local-half branch onto the true 256x128 hot kernel and only then judge whether the family is valid.`
- dir_01: Human idea 7/9 Register reuse + Ps2r: move the 64x32 local-half live-set cut onto the true 256x128 hot-band kernel | bottleneck: Register-limited occupancy and underfed tensor issue inside the 256x128 hot-band kernel. Success should lower `launch__registers_per_thread`, move `launch__occupancy_limit_registers` away from the current one-block limit, and raise `sm__warps_active` / tensor active on the dominant kernel instead of only on the peeled remainder path.
- dir_02: Human idea 5 Bank conflict: keep the 64x64 hot-band math shape but retune the B-consumer load order at warp scope only | bottleneck: Warp-local shared-memory operand delivery on the true hot-band kernel rather than occupancy. A positive result would show up as higher tensor active and lower consumer-side delivery stalls without increasing shared memory footprint or reducing stage depth.
- dir_03: Human idea 10 Stage: specialize the 256x128 hot-band loop into fixed steady-state control with less per-iteration orchestration | bottleneck: Steady-state orchestration overhead in the hot-band loop rather than raw operand layout. Success would mostly appear as lower hot-band runtime at similar register/shared counts, with modest tensor-active improvement from cleaner issue scheduling.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `4.134879 ms`, `1.159538x` slower than CUTLASS
