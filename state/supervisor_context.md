# Supervisor context

This file is for the main Codex supervisor. It decides whether to run the next step directly or dispatch a sub-agent.

## Current dispatch

- dispatch node: `node_c`
- dispatch mode: `sub_agent`
- graph status: `awaiting_direction_selection_for_node_c`
- round label: `single-run`
- round loop active: `no`
- rounds remaining: `0`
- auto-select frontier: `no`
- latest run id: `20260421_105134_bf16_gemm_v1_8dcab81`
- latest runtime: `24.186960 ms`
- recommended direction: `dir_01`
- active direction: `None`
- display update due at current checkpoint: `yes`
- watchdog status: `idle`
- continue required now: `no`
- stop allowed now: `yes`
- natural stop states disallowed: `no`
- interrupt policy: `none`

## Supervisor protocol

- read `docs/supervisor_protocol.md` first
- node-specific protocol: `docs/node_c_protocol.md`
- node context file: `state/node_c_context.md`
- prepare command: `python scripts/graph.py node_c`
- selection command: `python scripts/graph.py use-recommended-direction`
- finalize command: `python scripts/graph.py node_c --finalize`
- current dispatch requires direct GPU access: `no`

## Dispatch rule

- main agent stays responsible for graph state, commits, and loop control
- spawn exactly one sub-agent for the current node
- after the sub-agent returns, run the finalize command from the main agent
- then re-read `state/supervisor_task.json` before dispatching the next node

## Multi-round loop

- no multi-round loop is active
- to arm one, run `python scripts/graph.py rounds --count N --auto-use-recommended`

## Watchdog

- timeout: `10` minutes without workflow changes
- latest observed progress: `2026-04-21T11:01:26-07:00` via `state/graph_state.json`
- idle minutes: `N/A`
- watchdog status: `idle`
- continue instruction: `No watchdog action is currently required.`

## Notes

- `Ensure exactly one direction is selected, spawn an implementation sub-agent for a real code edit, and do not replace node_c with a scripted helper before finalizing from the main Codex agent.`
