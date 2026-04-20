# Round loop

- active: `yes`
- status: `awaiting_measurement`
- total rounds: `100`
- completed rounds: `37`
- remaining rounds: `63`
- current round label: `round 38/100`
- auto use recommended: `yes`
- accepted base run id: `20260420_010120_bf16_gemm_v1_d52137a`
- accepted base measured commit: `d52137aeec77eeeeffce6d3af05468487e1ea98c`
- accepted base runtime: `26.093568 ms`
- started at: `2026-04-19T22:34:28-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Build passed for round 38/100. Node A will measure the result next.`

## Last completed round

- round: `37/100`
- direction: `dir_01`
- direction name: `Keep the active PTX B-fragment reuse, but rewrite warp-local sequencing to shrink the new short-scoreboard and barrier cost`
- verdict: `regressed`
- runtime delta: `+0.022576 ms`
- TFLOP/s delta: `-0.024022 TFLOP/s`
- run dir: `runs/20260420_011851_bf16_gemm_v1_f8e7058`
- ncu rep path: `runs/20260420_011851_bf16_gemm_v1_f8e7058/ncu_profile.ncu-rep`
