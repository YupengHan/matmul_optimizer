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
python scripts/graph.py search-status
python scripts/graph.py frontier --top N
python scripts/graph.py select-next
python scripts/graph.py restore-base --run-id <run_id>
python scripts/graph.py cycle
python scripts/graph.py rounds --status
python scripts/graph.py rounds --count N --auto-use-recommended
python scripts/graph.py rounds --count N --auto-select-frontier
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

Supervisor no-stop rule:

1. if `state/round_loop_state.json` reports `active = true` and `remaining_rounds > 0`, the main agent must treat the workflow as still running
2. `ready_for_node_b`, `ready_for_node_c`, and `ready_for_node_a` are continue states during an active loop, not natural summary or stop points
3. during an active loop, the main agent may emit only progress updates and must keep dispatching the next node
4. the main agent must not stop merely because one round finished, a new node became ready, or there is a useful intermediate summary to report
5. the main agent may stop only when:
   - `remaining_rounds = 0`, or
   - the graph enters a failure / paused state, or
   - a required permission or environment dependency blocks further execution, or
   - the user explicitly redirects the conversation away from the active loop

Supervisor machine-readable continue contract:

1. when `state/round_loop_state.json` reports `active = true` and `remaining_rounds > 0`, `state/supervisor_task.json` must encode the continue requirement directly, not only in prose
2. during that active-loop window, the task file must expose:
   - `continue_required = true`
   - `stop_allowed = false`
   - `continue_until = "remaining_rounds == 0 or explicit_user_redirect"`
   - `continue_instruction = ...` for the current dispatch node
   - `interrupt_policy = "only_explicit_user_redirect"`
3. `ready_for_node_b`, `ready_for_node_c`, `ready_for_node_a`, and checkpoint states are continue states while `continue_required = true`
4. an intermediate summary, a completed round, or a newly ready node is not a legal stop reason while `continue_required = true`
5. the only legal stop reasons during an active loop are:
   - `round_loop_complete`
   - `graph_failure_or_pause`
   - `permission_or_environment_block`
   - `explicit_user_redirect`

Supervisor checkpoint rule:

1. during an active multi-round loop, the main agent must run a context-compression checkpoint after every 5 completed rounds
2. that same 5-round checkpoint must also refresh the public display snapshot:
   - update `README.md`
   - update `blog/harness-engineering-human-in-the-loop-cuda-matmul/index.md`
   - refresh the rendered optimization tree image
   - commit only the doc/image files touched by that display refresh
   - run `git push origin master` after the checkpoint doc/image commit so the current loop state is published remotely
3. the checkpoint must refresh `state/supervisor_context.md` with the latest dispatch state, active round, accepted base, current selected direction or candidate, display-refresh checkpoint state, and watchdog state
4. the checkpoint is a continue point, not a stop point
5. after the checkpoint, the main agent must immediately re-read `state/supervisor_task.json` and keep dispatching unless one of the no-stop-rule stop conditions is met

Supervisor watchdog rule:

1. during an active multi-round loop, if 10 minutes pass with no repo-visible workflow progress and `remaining_rounds > 0`, the main agent must treat the workflow as stalled rather than completed
2. on that stall condition, the main agent must re-read `state/supervisor_task.json` and issue the current continue instruction for the active dispatch node
3. for `node_b` and `node_c`, the continue instruction must still preserve the supervisor contract:
   - prepare or refresh the node context if needed
   - spawn exactly one sub-agent
   - run the finalize command from the main agent
4. the watchdog is a continue mechanism, not a stop condition by itself

## Natural-language command mapping

When the user says `开始运行 node_a`:

1. run `python scripts/graph.py node_a` outside the Codex sandbox, with direct CUDA access
2. read `state/latest_run.json`, `state/latest_ncu_summary.json`, and `state/graph_state.json`
3. report the real measured outcome only after the script finishes

When the user says `开始运行 node_b`:

1. run `python scripts/graph.py node_b`
2. read `docs/supervisor_protocol.md`, `docs/node_b_protocol.md`, and `state/node_b_context.md`
3. main Codex supervisor spawns one diagnosis `sub-agent` for node_b
4. the sub-agent reads the files listed there and edits `state/latest_diagnosis.json` so it contains exactly 3 directions, plus live-reasoning provenance fields
5. the diagnosis must come from real best-model reasoning, not a repo-external scripted helper or template emitter
6. the diagnosis must include concrete evidence refs for the live run context and distinct direction names / action fingerprints
7. after the sub-agent returns, the main agent runs `python scripts/graph.py node_b --finalize`

When the user says `开始运行 node_c`:

1. ensure a direction is selected in `state/active_direction.json`
2. if none is selected, use either:
   - `python scripts/graph.py select-next`
   - `python scripts/graph.py approve --direction dir_0X`
   - `python scripts/graph.py use-recommended-direction`
3. run `python scripts/graph.py node_c`
4. read `docs/supervisor_protocol.md`, `docs/node_c_protocol.md`, and `state/node_c_context.md`
5. main Codex supervisor spawns one implementation `sub-agent` for node_c
6. the sub-agent implements exactly one direction with a real compiled-code edit in the allowed build surface
7. the implementation must not be a repo-external scripted history replay or a no-op state-only change
8. after the sub-agent returns, the main agent runs `python scripts/graph.py node_c --finalize`

When the user says `批准使用推荐方向`:

1. run `python scripts/graph.py use-recommended-direction`
2. confirm the selected direction in `state/active_direction.json`
3. proceed to node_c

When the user says `开始运行N圈`:

1. parse the requested positive integer round count `N` from the user message
2. run `python scripts/graph.py rounds --count N --auto-use-recommended`
3. read `state/supervisor_task.json`
4. keep looping through `node_b -> node_c -> node_a`
5. for `node_b` and `node_c`, use one `sub-agent` per node and let the main agent finalize after each sub-agent returns
6. treat one completed round as:
   - diagnose one measured run
   - implement one selected direction
   - re-measure it with node_a
7. continue until `state/round_loop_state.json` shows `remaining_rounds = 0` or a failure pauses the loop
8. use the node_a commit for each completed round as the round-level record of:
   - modification idea
   - performance delta
   - profile paths
9. do not stop after a completed round just to summarize; if the loop is still active, proceed directly into the next `node_b`
10. after every 5 completed rounds, refresh `state/supervisor_context.md`, refresh the public display snapshot, commit only the doc/image refresh, run `git push origin master`, and then continue the loop without treating that checkpoint as a completion point
11. if the loop is still active, and `state/supervisor_task.json` later reports a 10-minute watchdog stall without reaching the target round count, issue the continue instruction and keep dispatching
12. once the loop is armed, treat every `ready_for_node_*` state as a continue point until the round budget is exhausted or the user explicitly redirects the conversation
13. any resident supervisor or external helper may keep dispatch alive, but it must not replace the actual `node_b` reasoning work or the actual `node_c` implementation work

If the user explicitly asks to prefer frontier-based selection for the loop, use:

```bash
python scripts/graph.py rounds --count N --auto-select-frontier
```

In that mode, when node_c is entered with no selected direction, the main agent should try `python scripts/graph.py select-next` first and only fall back to the current recommended direction if the frontier has no selectable open candidate.

When the user says `连续工作N圈`:

- treat it as the same instruction as `开始运行N圈`
- the main agent owns the loop budget and the stop condition
- the current dispatch step is always visible in `state/supervisor_task.json`

When the user says `再运行N圈`:

- treat it as the same instruction as `开始运行N圈`
- arm a fresh `N`-round loop from the current accepted base / current graph state
- the main agent owns the loop budget and the stop condition
- the current dispatch step is always visible in `state/supervisor_task.json`

When the user asks to restore an exact measured base by run id:

1. run `python scripts/graph.py restore-base --run-id <run_id>`
2. let the script resolve the measured/source commit from repo state
3. treat the action as a first-class search restore with `family_id=restore_base`
4. do not claim performance; a later `node_a` run is still required for any new measurement

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
- `reasoning_source` set to `main_codex_agent` or `codex_sub_agent`
- `reasoning_mode` set to `manual_reasoned_best_model`
- a non-trivial `reasoning_summary`
- `evidence_refs` that include the live run context files

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
- use distinct direction names and distinct `action_fingerprint` values across the 3 directions
- reject repo-external scripted helpers, template emitters, and auto-generated diagnoses as invalid node_b output
- end with `current_node = node_c`

### node_c

Role:

- Codex-friendly implementation node
- normally executed through one implementation `sub-agent` under the main Codex supervisor

Must:

- read `state/latest_diagnosis.json`, `state/active_direction.json`, and `state/node_c_context.md`
- implement exactly one direction
- keep edits inside the allowed surface unless the protocol explicitly requires a minimal glue change
- make at least one real compiled-code edit in `src/kernels/*`, `include/*`, `src/runner/main.cpp`, or `CMakeLists.txt`
- force a rebuild before claiming success
- stop on build failure, update failure state, and avoid a success commit
- commit code plus lightweight state only after the build passes
- include the active round label when a multi-round loop is running
- auto-trigger node_a by default after a successful finalize

Must not:

- implement multiple directions in one loop
- auto-merge anything
- claim a performance win before node_a measures it
- treat a repo-external scripted replay, historical `git restore`, or state-only edit as valid node_c work

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
