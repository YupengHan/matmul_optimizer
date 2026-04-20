# Round loop

- active: `yes`
- status: `round_in_progress`
- total rounds: `10`
- completed rounds: `6`
- remaining rounds: `4`
- current round label: `round 7/10`
- auto use recommended: `yes`
- accepted base run id: `20260419_202711_bf16_gemm_v1_5135c1d`
- accepted base measured commit: `5135c1d6edb580191a96d8c6d9b47cb3ec8b96be`
- accepted base runtime: `30.310320 ms`
- started at: `2026-04-19T20:27:38-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Executing round 7/10.`

## Last completed round

- round: `6/10`
- direction: `dir_01`
- direction name: `Human idea 10 Stage: keep the correct hot kernel, but specialize the fixed 452-tile loop into explicit prologue / steady-state / epilogue control`
- verdict: `regressed`
- runtime delta: `+0.195072 ms`
- TFLOP/s delta: `-0.150790 TFLOP/s`
- run dir: `runs/20260419_212123_bf16_gemm_v1_b276585`
- ncu rep path: `runs/20260419_212123_bf16_gemm_v1_b276585/ncu_profile.ncu-rep`
