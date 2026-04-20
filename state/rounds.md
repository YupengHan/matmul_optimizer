# Round loop

- active: `yes`
- status: `running`
- total rounds: `50`
- completed rounds: `5`
- remaining rounds: `45`
- current round label: `round 6/50`
- auto use recommended: `yes`
- accepted base run id: `20260419_222734_bf16_gemm_v1_0d78758`
- accepted base measured commit: `0d787589a75b35984fb169106135c77436806bc6`
- accepted base runtime: `29.325824 ms`
- started at: `2026-04-19T22:34:28-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Completed round 5/50. Continue with node_b for round 6/50. Accepted base: 20260419_222734_bf16_gemm_v1_0d78758 at 29.325824 ms.`

## Last completed round

- round: `5/50`
- direction: `dir_01`
- direction name: `Keep the peeled steady state, but restore the proven final-two-tile handoff to recover correctness`
- verdict: `regressed`
- runtime delta: `+0.004320 ms`
- TFLOP/s delta: `-0.003487 TFLOP/s`
- run dir: `runs/20260419_225909_bf16_gemm_v1_b50742e`
- ncu rep path: `runs/20260419_225909_bf16_gemm_v1_b50742e/ncu_profile.ncu-rep`
