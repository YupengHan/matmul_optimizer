# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `6eaca8ea3a675237521dd743b9e744b57167933f`
- plateau counter: `4`
- round loop: `round 15/20`
- rounds remaining: `6`
- notes: `Node C build succeeded for round 15/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_003937_bf16_gemm_v1_6eaca8e`
- run dir: `runs/20260419_003937_bf16_gemm_v1_6eaca8e`
- correctness: `PASS`
- median runtime: `43.769424 ms`
- TFLOP/s: `16.610212 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_004022`
- recommended direction: `dir_01`
- approved direction: `dir_02`
- diagnosis notes: `This diagnosis incorporates the round-14 human-in-loop signal and avoids barrier/shared-B retry.`
- dir_01: Main-path explicit ldmatrix/mma.sync feed rewrite | bottleneck: Main-path operand delivery and instruction mix before tensor issue, especially the WMMA fragment-load path feeding the 64x128 CTA kernel and showing persistent smsp__warp_issue_stalled_mio_throttle_per_warp_active pressure.
- dir_02: Retile CTA and warp partition to trim per-warp N baggage | bottleneck: Per-warp fragment baggage and B-side staging pressure caused by the current CTA/warp partition, reflected in MIO throttle and possibly excess register footprint from carrying multiple N-side fragments per warp.
- dir_03: Direct-writeback epilogue that removes c_shared entirely | bottleneck: Epilogue shared-memory staging and synchronization overhead after accumulation, specifically the c_shared scratch path and warp-level syncs around accumulator writeback.

## Active implementation direction

- direction id: `dir_02`
- selection mode: `approved`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `17.779776 ms`, `1.686004x` slower than CUTLASS
