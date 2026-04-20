# Round loop

- active: `yes`
- status: `round_in_progress`
- total rounds: `100`
- completed rounds: `63`
- remaining rounds: `37`
- current round label: `round 64/100`
- auto use recommended: `yes`
- accepted base run id: `20260420_084915_bf16_gemm_v1_4e5579e`
- accepted base measured commit: `4e5579ec72e9b1f05820c895c0315235d66f30cd`
- accepted base runtime: `24.570881 ms`
- started at: `2026-04-19T22:34:28-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Executing round 64/100.`

## Last completed round

- round: `63/100`
- direction: `dir_01`
- direction name: `Restore accepted base, then retest finer issue granularity on the hot band`
- verdict: `regressed`
- runtime delta: `+0.652352 ms`
- TFLOP/s delta: `-0.723339 TFLOP/s`
- run dir: `runs/20260420_091330_bf16_gemm_v1_863f60f`
- ncu rep path: `runs/20260420_091330_bf16_gemm_v1_863f60f/ncu_profile.ncu-rep`
