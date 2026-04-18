# Task 02: Implement `cutlass_runner`

## Goal

Add a CUTLASS-based runner binary that matches the existing runner contract so it can be driven by `scripts/run_cutlass_baseline.py` and `scripts/eval_kernel.py`.

## Why this task exists

The repo already has the wrapper script:

- `scripts/run_cutlass_baseline.py`

But it does not yet have:

- `build/cutlass_runner`

That binary is the missing piece for generating the first CUTLASS baseline.

## Read first

- `scripts/run_cutlass_baseline.py`
- `scripts/eval_kernel.py`
- `src/runner/main.cpp`
- `include/kernel_api.h`
- `include/runner_contract.h`
- `CMakeLists.txt`

## Design constraints

- keep the same CLI contract as `custom_runner`
- keep the same JSON output shape as `custom_runner`
- keep the same dataset loading and correctness/perf flow where possible
- do not rewrite the Python harness unless required
- prefer copying the current runner flow and swapping the kernel launch path

## Required CLI contract

The new binary must support:

- `--dataset-dir`
- `--case-id`
- `--mode correctness|perf`
- `--warmup`
- `--iters`
- `--flush-cache-mb`
- `--json-out`

## Required outputs

The JSON written by `cutlass_runner` must stay compatible with `eval_kernel.py`.

Correctness mode output:

- `mode`
- `passed`
- `correctness.max_abs_err`
- `correctness.max_rel_err`
- `correctness.mean_abs_err`
- `correctness.bf16_exact_match`
- `correctness.atol`
- `correctness.rtol`

Perf mode output:

- `mode`
- `passed`
- `runtime_ms.median`
- `runtime_ms.p10`
- `runtime_ms.p90`
- `tflops`

## Recommended implementation approach

1. Duplicate the logic in `src/runner/main.cpp` into a new file, likely `src/runner/cutlass_main.cpp`.
2. Keep:
   - argument parsing
   - dataset loading
   - correctness checks
   - perf timing
   - cache flush
   - JSON writing
3. Replace only the actual GEMM execution path with CUTLASS GEMM.
4. Add a new CMake target named `cutlass_runner`.
5. Document any external dependency steps needed to build CUTLASS.

## Deliverables

- a compilable `cutlass_runner` target
- CMake wiring for that target
- any required include paths or dependency notes
- no behavior regressions to `custom_runner`

## Definition of done

- `cmake --build build -j` produces `build/cutlass_runner`
- `build/cutlass_runner --help` is not required, but the required flags must work
- `scripts/run_cutlass_baseline.py --runner build/cutlass_runner ...` can call it without interface mismatch

## Suggested prompt for VSCode chat

```text
Please complete todo/02_cutlass_runner.md. Reuse the existing runner contract from src/runner/main.cpp and implement a CUTLASS-based build/cutlass_runner that can be consumed unchanged by scripts/run_cutlass_baseline.py and scripts/eval_kernel.py.
```
