# Round loop

- active: `yes`
- status: `round_in_progress`
- total rounds: `5`
- completed rounds: `2`
- remaining rounds: `3`
- current round label: `round 3/5`
- auto use recommended: `yes`
- accepted base run id: `20260419_102608_bf16_gemm_v1_2872f92`
- accepted base measured commit: `2872f92585773d6f6a38c911cb76d010d4209366`
- accepted base runtime: `35.677088 ms`
- started at: `2026-04-19T10:16:39-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Executing round 3/5.`

## Last completed round

- round: `2/5`
- direction: `dir_01`
- direction name: `Reduce stage-recycle barriers in the peeled 64x384 hot loop`
- verdict: `regressed`
- runtime delta: `+6.068319 ms`
- TFLOP/s delta: `-2.962213 TFLOP/s`
- run dir: `runs/20260419_103438_bf16_gemm_v1_3eeb098`
- ncu rep path: `runs/20260419_103438_bf16_gemm_v1_3eeb098/ncu_profile.ncu-rep`
