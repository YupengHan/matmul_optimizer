# Round loop

- active: `yes`
- status: `round_in_progress`
- total rounds: `50`
- completed rounds: `11`
- remaining rounds: `39`
- current round label: `round 12/50`
- auto use recommended: `yes`
- accepted base run id: `20260419_222734_bf16_gemm_v1_0d78758`
- accepted base measured commit: `0d787589a75b35984fb169106135c77436806bc6`
- accepted base runtime: `29.325824 ms`
- started at: `2026-04-19T22:34:28-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Executing round 12/50.`

## Last completed round

- round: `11/50`
- direction: `dir_01`
- direction name: `Keep the restored correct surface and let only half the CTA issue hot-band Pg2s async copies`
- verdict: `regressed`
- runtime delta: `+1.403392 ms`
- TFLOP/s delta: `-1.058336 TFLOP/s`
- run dir: `runs/20260419_231544_bf16_gemm_v1_1cc244f`
- ncu rep path: `runs/20260419_231544_bf16_gemm_v1_1cc244f/ncu_profile.ncu-rep`
