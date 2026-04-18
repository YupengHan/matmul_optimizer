# Current focus

- branch: `master`
- phase: `first_gpu_measurement_pending`
- active execution node: `custom_runner` + `eval_kernel`
- current bottleneck belief: no performance bottleneck is measured yet; the immediate blocker is that the repo does not yet contain a successful host-side GPU run artifact
- latest Codex-sandbox run: `runs/20260418_021152_bf16_gemm_v1` failed at `cudaMalloc` because the sandbox could not see the GPU
- host execution note: the operator reports that the external terminal can access the GPU
- immediate next action: run the existing pipeline from the host terminal, capture the first valid correctness/perf result under `runs/`, then add the CUTLASS baseline
