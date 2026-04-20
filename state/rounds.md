# Round loop

- active: `yes`
- status: `awaiting_measurement`
- total rounds: `50`
- completed rounds: `6`
- remaining rounds: `44`
- current round label: `round 7/50`
- auto use recommended: `yes`
- accepted base run id: `20260419_222734_bf16_gemm_v1_0d78758`
- accepted base measured commit: `0d787589a75b35984fb169106135c77436806bc6`
- accepted base runtime: `29.325824 ms`
- started at: `2026-04-19T22:34:28-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Build passed for round 7/50. Node A will measure the result next.`

## Last completed round

- round: `6/50`
- direction: `dir_01`
- direction name: `Apply peeled steady-state only to the 8-warp 256x128 hot band and leave the residual 64x128 path on the proven generic loop`
- verdict: `regressed`
- runtime delta: `+0.094096 ms`
- TFLOP/s delta: `-0.075710 TFLOP/s`
- run dir: `runs/20260419_230146_bf16_gemm_v1_b368da0`
- ncu rep path: `runs/20260419_230146_bf16_gemm_v1_b368da0/ncu_profile.ncu-rep`
