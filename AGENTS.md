# AGENTS

This repository is a local, Codex-oriented workflow for one fixed benchmark:

- target: beat the local CUTLASS baseline on `fixed_bf16_gemm_v1`
- shape: `m=6464, n=7776, k=7232`
- dtype: BF16 inputs, FP32 accumulation, BF16 output reference
- execution-critical path: script-first
- agent use: diagnosis and implementation only

No OpenAI API key, cloud service, or LangGraph runtime is required. The repo only borrows the node / edge / state framing.

## Standard commands

Dataset init:

```bash
python scripts/generate_fixed_bf16_dataset.py
```

Main-loop build:

```bash
cmake -S . -B build -DENABLE_CUTLASS_RUNNER=OFF
cmake --build build -j 4 --target custom_runner
```

Node workflow entrypoints:

```bash
python scripts/graph.py status
python scripts/graph.py supervisor
python scripts/graph.py cycle
python scripts/graph.py rounds --status
python scripts/graph.py rounds --count 5 --auto-use-recommended
python scripts/graph.py node_a
python scripts/graph.py node_b
python scripts/graph.py node_b --finalize
python scripts/graph.py approve --direction dir_02
python scripts/graph.py use-recommended-direction
python scripts/graph.py node_c
python scripts/graph.py node_c --finalize
python scripts/graph.py cycle
```

CUTLASS side-path build and baseline run:

```bash
cmake -S . -B build -DENABLE_CUTLASS_RUNNER=ON -DCUTLASS_ROOT=/path/to/cutlass
cmake --build build -j 4 --target cutlass_runner
python scripts/run_cutlass_baseline.py --runner ./build/cutlass_runner --kernel-tag cutlass_ref_v1
```

`python scripts/graph.py cycle` reads `state/graph_state.json` and either runs the script-first node or prepares the next Codex handoff context.

`python scripts/graph.py supervisor` refreshes and prints the current main-agent dispatch task from `state/supervisor_task.json`.

## Supervisor layer

The execution model has one extra orchestration layer:

- the main Codex agent is the supervisor
- `node_a` is executed directly by the main agent
- `node_b` and `node_c` are executed through one dedicated `sub-agent` each
- repo-local scripts prepare context, validate state, and finalize commits
- repo-local scripts do **not** try to spawn Codex agents by themselves

The supervisor contract lives in:

- `docs/supervisor_protocol.md`
- `state/supervisor_task.json`
- `state/supervisor_context.md`

Supervisor rule:

1. read `state/supervisor_task.json`
2. if `dispatch_mode = direct_script`, run the node directly
3. if `dispatch_mode = sub_agent`, prepare the node context, spawn exactly one sub-agent for that node, then run the finalize command from the main agent
4. after every node completion, re-read `state/supervisor_task.json` before dispatching the next node

## Natural-language command mapping

When the user says `开始运行 node_a`:

1. run `python scripts/graph.py node_a` outside the Codex sandbox, with direct CUDA access
2. read `state/latest_run.json`, `state/latest_ncu_summary.json`, and `state/graph_state.json`
3. report the real measured outcome only after the script finishes

When the user says `开始运行 node_b`:

1. run `python scripts/graph.py node_b`
2. read `docs/supervisor_protocol.md`, `docs/node_b_protocol.md`, and `state/node_b_context.md`
3. main Codex supervisor spawns one diagnosis `sub-agent` for node_b
4. the sub-agent reads the files listed there and edits `state/latest_diagnosis.json` so it contains exactly 3 directions
5. after the sub-agent returns, the main agent runs `python scripts/graph.py node_b --finalize`

When the user says `开始运行 node_c`:

1. ensure a direction is selected in `state/active_direction.json`
2. if none is selected, use either:
   - `python scripts/graph.py approve --direction dir_0X`
   - `python scripts/graph.py use-recommended-direction`
3. run `python scripts/graph.py node_c`
4. read `docs/supervisor_protocol.md`, `docs/node_c_protocol.md`, and `state/node_c_context.md`
5. main Codex supervisor spawns one implementation `sub-agent` for node_c
6. the sub-agent implements exactly one direction
7. after the sub-agent returns, the main agent runs `python scripts/graph.py node_c --finalize`

When the user says `批准使用推荐方向`:

1. run `python scripts/graph.py use-recommended-direction`
2. confirm the selected direction in `state/active_direction.json`
3. proceed to node_c

When the user says `开始运行5圈`:

1. run `python scripts/graph.py rounds --count 5 --auto-use-recommended`
2. read `state/supervisor_task.json`
3. keep looping through `node_b -> node_c -> node_a`
4. for `node_b` and `node_c`, use one `sub-agent` per node and let the main agent finalize after each sub-agent returns
5. treat one completed round as:
   - diagnose one measured run
   - implement one selected direction
   - re-measure it with node_a
6. continue until `state/round_loop_state.json` shows `remaining_rounds = 0` or a failure pauses the loop
7. use the node_a commit for each completed round as the round-level record of:
   - modification idea
   - performance delta
   - profile paths

When the user says `连续工作5圈`:

- treat it as the same instruction as `开始运行5圈`
- the main agent owns the loop budget and the stop condition
- the current dispatch step is always visible in `state/supervisor_task.json`

## Strict node definitions

### node_a

Role:

- script-first measurement node
- must run outside the Codex sandbox because the benchmark and NCU profiling require direct CUDA device access

Must:

- build `custom_runner` if needed
- call `scripts/eval_kernel.py`
- record correctness / performance / NCU outputs
- update machine-readable state:
  - `state/graph_state.json`
  - `state/latest_run.json`
  - `state/latest_ncu_summary.json`
  - `state/run_registry.jsonl`
- update human-readable state:
  - `state/latest_run.md`
  - `state/latest_ncu_summary.md`
  - `state/progress.md`
  - `state/current_focus.md`
  - `state/benchmark_baselines.md`
  - `state/human_review.md`
- commit lightweight state only after a real measurement finishes
- include previous-runtime delta and profile paths in the node_a commit body
- end with `current_node = node_b`

Must not:

- claim performance without a real measured run
- commit raw `runs/` artifacts
- depend on CUTLASS being configured

### node_b

Role:

- Codex-friendly diagnosis node
- normally executed through one diagnosis `sub-agent` under the main Codex supervisor

Must read:

- `state/latest_run.md`
- `state/latest_ncu_summary.md`
- `docs/heuristics.md`
- `state/progress.md`
- `state/current_focus.md`
- `state/human_review.md`
- current kernel source
- raw run summary / raw NCU CSV referenced from `state/node_b_context.md`

Must output:

- exactly 3 directions in `state/latest_diagnosis.json`
- one `recommended_direction_id`

Each direction must contain:

- `hypothesis`
- `expected_bottleneck`
- `code_locations`
- `risk`
- `metrics_to_recheck`

Must also:

- update the human-review state via `python scripts/graph.py node_b --finalize`
- commit only lightweight state
- include the active round label when a multi-round loop is running
- end with `current_node = node_c`

### node_c

Role:

- Codex-friendly implementation node
- normally executed through one implementation `sub-agent` under the main Codex supervisor

Must:

- read `state/latest_diagnosis.json`, `state/active_direction.json`, and `state/node_c_context.md`
- implement exactly one direction
- keep edits inside the allowed surface unless the protocol explicitly requires a minimal glue change
- build before claiming success
- stop on build failure, update failure state, and avoid a success commit
- commit code plus lightweight state only after the build passes
- include the active round label when a multi-round loop is running
- auto-trigger node_a by default after a successful finalize

Must not:

- implement multiple directions in one loop
- auto-merge anything
- claim a performance win before node_a measures it

## Allowed vs disallowed edits

Safe to modify during node_c:

- `src/kernels/*`
- `src/runner/main.cpp`
- `include/*`
- `CMakeLists.txt` when strictly necessary
- `state/*.json`
- `state/*.md`
- `docs/node_b_protocol.md`
- `docs/node_c_protocol.md`
- `docs/supervisor_protocol.md`
- `README.md`
- `docs/pipeline_graph.md`
- `docs/commit_convention.md`
- `AGENTS.md`
- `scripts/graph.py`
- `scripts/state_lib.py`
- `scripts/eval_kernel.py`

Do not casually modify:

- dataset definitions in `configs/fixed_bf16_gemm_v1.json`
- generated dataset binaries under `artifacts/datasets/`
- raw run artifacts under `runs/`
- the benchmark shape itself

## Git conventions

Commit types are node-specific:

- `node_a: ...` for measured state commits
- `node_b: ...` for diagnosis commits
- `node_c: ...` for implementation commits after build success
- `infra: ...` for repo-level workflow / protocol changes

Rules:

- node_a commits state only
- node_b commits state only
- node_c commits code plus lightweight state
- do not create a node_c success commit if the build failed
- do not commit unrelated staged files

Template reference:

- `.gitmessage`
- `docs/commit_convention.md`

## Large-file and artifact policy

Never commit:

- `runs/`
- `artifacts/` dataset binaries
- `build/`
- `*.ncu-rep`
- raw CSV/log artifacts from Nsight Compute
- scratch logs such as `state/*.log`

The commit-friendly layer is the lightweight state in `state/`.
