# Current focus

- next node: `node_b`
- status: `ready_for_node_b`
- latest run id: `20260420_120552_bf16_gemm_v1_84de30b`
- latest kernel tag: `bf16_gemm_v1_84de30b`
- median runtime: `25.944464 ms`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- round loop: `round 84/100`
- rounds remaining: `17`
- recommended direction: `None`
- selected direction: `None`
- immediate next action: `Node A completed round 83/100. Run node_b to continue round 84/100.`

## Persisted loop memory

- best active family in the current environment: `128x128 PTX microkernel default hot-band + zero PTX export padding`
- best active run in the current environment: `20260420_115626_bf16_gemm_v1_469a12b` at `25.643007 ms`
- best active measured commit for the current environment: `469a12bfb9bb7579ea3238342f598a34e84a5e1a`
- best recorded historical custom run remains `20260420_084915_bf16_gemm_v1_4e5579e` at `24.570881 ms`
- do not spend rounds on pure baseline-restore work alone: the same source surface previously measured differently across sessions, so new rounds should focus on fresh bottleneck hypotheses, not just recreating an old commit
- most useful current read on the active baseline: tensor is back near `48%`, barrier is down near `5.5%`, DRAM is low near `10%`, but `long_scoreboard` remains elevated and is the main residual signal to attack
- next diagnosis should compare new ideas against the `25.643007 ms` active baseline, not only against the latest `25.944464 ms` grouping regression

## Closed Or Weak Families

- broad default hot-band promotion away from the PTX microkernel is closed-negative for now
- evidence: `64x384` default promotion regressed to `33.594879 ms`
- evidence: `256x128` default promotion regressed to `31.867904 ms`
- `128x128x32` staged K32 family is closed-negative for now
- evidence: staged K32 regressed to `31.552928 ms`
- PTX helper-flattening was effectively a no-op and should not be revisited without a materially different codegen hypothesis
- evidence: helper flattening moved from `24.696192 ms` to `24.696832 ms`
- paired PTX export-lifetime variant is closed-negative for now
- evidence: paired export regressed from `25.643007 ms` to `25.837568 ms`
- tightening `kFixedHotBandPtxGroupedRows` from `8` to `4` was flat-to-negative
- evidence: grouping tweak regressed from `25.904127 ms` to `25.944464 ms`
- one bounded `128x128` two-stage feed-cadence experiment was only weak/flat
- evidence: cadence retime landed at `25.904127 ms` and traded lower barrier / mio for higher DRAM
