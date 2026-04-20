# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `5775c085b600b2078e7adc4489329d3d1dfa5c92`
- plateau counter: `14`
- round loop: `round 9/10`
- rounds remaining: `2`
- notes: `Node C build succeeded for round 9/10. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_213613_bf16_gemm_v1_5775c08`
- run dir: `runs/20260419_213613_bf16_gemm_v1_5775c08`
- correctness: `PASS`
- median runtime: `30.662016 ms`
- TFLOP/s: `23.710751 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_213703`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 9 human-idea audit after the round-8 B-feed experiment: Tiling stays accepted because the 64x384 hot band is still the measured macro-shape sweet spot; Coalescing Access, Data Reuse, Async Copy, and Pg2s remain baseline infrastructure; L2 Cache stays rejected because the grouped CTA remap already regressed runtime and hot-band time; Stage stays rejected because the fixed-shape control refactor also regressed; the round-8 warp-local B consumer transform did not beat the accepted base, but it did produce the first meaningful same-family positive signal after those failures: runtime improved by about 0.65 ms over the negative L2 run, hot-band time dropped to about 41.17 us, tensor active rose to about 38.47, short scoreboard improved, `mio_throttle` collapsed to about 0.33, registers stayed at 167, and shared footprint did not grow. That is enough evidence to keep the last two rounds on the B-feed family rather than switching again. Recommended direction dir_01 therefore advances from consumer issue order alone to the user's deeper producer/consumer-layout split inside the same shared-memory budget: keep the new single-fragment streaming consumer path, but physically permute the B shared layout inside each warp group so producer layout and consumer layout are no longer identical.`
- dir_01: Human idea two-level B staging follow-through: footprint-neutral B shared permutation on top of the current streaming consumer path | bottleneck: Warp-local shared/L1 operand delivery and bank behavior on the hot-band B fragment path rather than CTA-level control flow.
- dir_02: Warp-specialized producer/consumer on top of the current B-feed branch | bottleneck: All-warps staging and handoff overhead after the most obvious B-fragment issue pressure has already been reduced.
- dir_03: Human idea Ps2r on the current streaming branch: one-fragment shared-to-register lookahead | bottleneck: Residual shared-to-register feed latency inside the hot-band 64x64 micro-tile after the first consumer-order cleanup.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `4.134879 ms`, `1.159538x` slower than CUTLASS
