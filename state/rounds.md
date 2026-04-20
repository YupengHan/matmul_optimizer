# Round loop

- active: `yes`
- status: `running`
- total rounds: `50`
- completed rounds: `18`
- remaining rounds: `32`
- current round label: `round 19/50`
- auto use recommended: `yes`
- accepted base run id: `20260419_235558_bf16_gemm_v1_be44358`
- accepted base measured commit: `be44358062dd87db8692cf1a8ce8017bab55a65d`
- accepted base runtime: `29.204992 ms`
- started at: `2026-04-19T22:34:28-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Completed round 18/50. Continue with node_b for round 19/50. Accepted base: 20260419_235558_bf16_gemm_v1_be44358 at 29.204992 ms.`

## Last completed round

- round: `18/50`
- direction: `dir_01`
- direction name: `Try the 256x128 hot-band CTA with 64x64 warp tiles on top of the proven K16 stage contract`
- verdict: `regressed`
- runtime delta: `+0.785407 ms`
- TFLOP/s delta: `-0.583638 TFLOP/s`
- run dir: `runs/20260420_000122_bf16_gemm_v1_a4646fc`
- ncu rep path: `runs/20260420_000122_bf16_gemm_v1_a4646fc/ncu_profile.ncu-rep`
