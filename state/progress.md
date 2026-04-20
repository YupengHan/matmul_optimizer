# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `5135c1d6edb580191a96d8c6d9b47cb3ec8b96be`
- plateau counter: `6`
- round loop: `round 1/10`
- rounds remaining: `10`
- notes: `Node C build succeeded for round 1/10. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_202711_bf16_gemm_v1_5135c1d`
- run dir: `runs/20260419_202711_bf16_gemm_v1_5135c1d`
- correctness: `PASS`
- median runtime: `30.310320 ms`
- TFLOP/s: `23.985871 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_202755`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 1/10 human-idea audit against the fresh correct baseline: Tiling is accepted historically, but not as a fresh pivot this round because the repo already proved 64x384 is the best correct macro width for this GPU/shape; Coalescing Access is accepted as baseline because cp.async staging is already 16-byte aligned and the run is not DRAM-bound; Data Reuse is accepted as baseline because the fixed peeled kernel already depends on shared reuse; Async Copy is accepted as baseline because the current pipeline is already cp.async-based; Bank Conflict is deferred to rank-3 because the more immediate limiter on the correct branch is register-driven occupancy rather than feed stalls; L2 Cache swizzle is deferred because lts and dram throughput are both modest; Register Reuse is accepted as the primary family because the stable base is still sitting at only 16.59 active warps with launch__occupancy_limit_registers = 1; Pg2s is accepted as baseline because double-buffer G2S is already present; Ps2r is accepted in spirit via serial micro-panels that reduce simultaneously live B/acc tiles; Stage is accepted as baseline because barrier and mio are already low enough that stage churn is not the first lever. Recommended direction is dir_01 because it keeps the proven 64x384 outer shape while directly attacking the remaining register wall on the correct branch.`
- dir_01: Human idea 7 Register reuse: keep the outer 64x384 hot path, but serialise the inner live set into 2x192 micro-panels | bottleneck: Register pressure and resulting latency-hiding loss on the stable 64x384 PTX hot path.
- dir_02: Human idea 7 Register reuse: if 2x192 still keeps too much live state, split the 64x384 hot path into 3x128 micro-panels | bottleneck: Register pressure first, then possible serialisation overhead if the panel size gets too small.
- dir_03: Human idea 5 Bank conflict: stay on the correct 64x384 path and do a warp-local B-consumer load-order retune with no extra shared or CTA barriers | bottleneck: Operand-delivery efficiency and shared-bank behavior inside the warp-local B consumer path, not DRAM throughput.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `4.134879 ms`, `1.159538x` slower than CUTLASS
