# Round loop

- active: `yes`
- status: `round_in_progress`
- total rounds: `50`
- completed rounds: `7`
- remaining rounds: `43`
- current round label: `round 8/50`
- auto use recommended: `yes`
- accepted base run id: `20260419_222734_bf16_gemm_v1_0d78758`
- accepted base measured commit: `0d787589a75b35984fb169106135c77436806bc6`
- accepted base runtime: `29.325824 ms`
- started at: `2026-04-19T22:34:28-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Executing round 8/50.`

## Last completed round

- round: `7/50`
- direction: `dir_01`
- direction name: `Restore the accepted-correct control flow and switch the 64x64 column sweep to explicit right-left-right-left order`
- verdict: `regressed`
- runtime delta: `+0.443904 ms`
- TFLOP/s delta: `-0.350876 TFLOP/s`
- run dir: `runs/20260419_230410_bf16_gemm_v1_abefa1e`
- ncu rep path: `runs/20260419_230410_bf16_gemm_v1_abefa1e/ncu_profile.ncu-rep`
