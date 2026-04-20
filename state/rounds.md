# Round loop

- active: `yes`
- status: `running`
- total rounds: `20`
- completed rounds: `9`
- remaining rounds: `11`
- current round label: `round 10/20`
- auto use recommended: `yes`
- accepted base run id: `20260419_142213_bf16_gemm_v1_9bdc160`
- accepted base measured commit: `9bdc160ee2a6ef0f1171c09f4cf72f7dd081cab1`
- accepted base runtime: `33.128447 ms`
- started at: `2026-04-19T14:22:54-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Completed round 9/20. Continue with node_b for round 10/20. Accepted base: 20260419_142213_bf16_gemm_v1_9bdc160 at 33.128447 ms.`

## Last completed round

- round: `9/20`
- direction: `dir_01`
- direction name: `Human idea 10 Stage: keep the corrected 3-stage hot band, but squeeze it under the 128-reg cliff`
- verdict: `regressed`
- runtime delta: `+452.851747 ms`
- TFLOP/s delta: `-18.879646 TFLOP/s`
- run dir: `runs/20260419_181807_bf16_gemm_v1_3dd4394`
- ncu rep path: `runs/20260419_181807_bf16_gemm_v1_3dd4394/ncu_profile.ncu-rep`
