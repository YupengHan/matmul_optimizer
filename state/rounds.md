# Round loop

- active: `yes`
- status: `running`
- total rounds: `17`
- completed rounds: `10`
- remaining rounds: `7`
- current round label: `round 11/17`
- auto use recommended: `yes`
- accepted base run id: `20260420_160517_bf16_gemm_v1_c3f11c3`
- accepted base measured commit: `c3f11c31cb51d8199d308580575f3aff7ac381c1`
- accepted base runtime: `24.845824 ms`
- started at: `2026-04-20T15:41:15-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Completed round 10/17. Continue with node_b for round 11/17. Accepted base: 20260420_160517_bf16_gemm_v1_c3f11c3 at 24.845824 ms.`

## Last completed round

- round: `10/17`
- direction: `dir_01`
- direction name: `Use The Non-PTX 128x128 Sibling As The Next Control Path`
- verdict: `regressed`
- runtime delta: `+1.027599 ms`
- TFLOP/s delta: `-1.089549 TFLOP/s`
- run dir: `runs/20260420_162632_bf16_gemm_v1_948fc5c`
- ncu rep path: `runs/20260420_162632_bf16_gemm_v1_948fc5c/ncu_profile.ncu-rep`
