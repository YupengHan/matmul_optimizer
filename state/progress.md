# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `68c21acd26439775c646252dbb0e52d247ea9f47`
- plateau counter: `0`
- round loop: `round 4/20`
- rounds remaining: `17`
- notes: `Node C build succeeded for round 4/20. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_221009_bf16_gemm_v1_68c21ac`
- run dir: `runs/20260420_221009_bf16_gemm_v1_68c21ac`
- correctness: `PASS`
- median runtime: `24.177664 ms`
- TFLOP/s: `30.069879 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_221111`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 4/20 human-review audit: the queue still contributes only the approval gate and exactly-one-direction rule. The current PTX exploit family just produced the new best custom run at 24.177664 ms, but the NCU signature stayed almost unchanged, which argues against immediately spending another round on the same class of PTX control tweak. Accepted as the primary family for this diagnosis is therefore the cheap grouped-CTA traversal/locality probe on the 128x128 PTX grid. Deferred fallback families are another bounded PTX exploit pass and a reopen of the prior PTX baseline as an A/B guardrail. The failed 256x128 pivot family remains rejected for this round.`
- dir_01: Retune Hot-Band CTA Traversal On The 128x128 PTX Grid | bottleneck: Inter-CTA locality and traversal efficiency on the current 128x128 PTX hot-band grid under low occupancy.
- dir_02: Continue The Active PTX One-K 128x128 Control-Path Exploit | bottleneck: Residual PTX control-path overhead in the current one-k 128x128 hot-band branch.
- dir_03: Reopen The Prior PTX One-K 128x128 Control Branch For A/B Guardrail | bottleneck: Not a new bottleneck attack; this is the PTX-family A/B restore guardrail.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.740225 ms`, `0.932856x` slower than CUTLASS
