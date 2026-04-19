# Round loop

- active: `yes`
- status: `running`
- total rounds: `20`
- completed rounds: `8`
- remaining rounds: `12`
- current round label: `round 9/20`
- auto use recommended: `yes`
- accepted base run id: `20260418_225901_bf16_gemm_v1_91e446e`
- accepted base measured commit: `91e446eea2cf2de912e81e21c45653dcd227d591`
- accepted base runtime: `54.136911 ms`
- started at: `2026-04-18T22:03:53-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Completed round 8/20. Continue with node_b for round 9/20. Accepted base: 20260418_225901_bf16_gemm_v1_91e446e at 54.136911 ms.`

## Last completed round

- round: `8/20`
- direction: `dir_01`
- direction name: `Specialize the fixed-shape K loop so the 4-warp CTA spends less time in barrier and control overhead`
- verdict: `regressed`
- runtime delta: `+2.676958 ms`
- TFLOP/s delta: `-0.631481 TFLOP/s`
- run dir: `runs/20260418_233053_bf16_gemm_v1_6bee469`
- ncu rep path: `runs/20260418_233053_bf16_gemm_v1_6bee469/ncu_profile.ncu-rep`
