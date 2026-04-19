# Supervisor context

This file is for the main Codex supervisor. It decides whether to run the next step directly or dispatch a sub-agent.

## Current dispatch

- dispatch node: `node_c`
- dispatch mode: `sub_agent`
- graph status: `awaiting_direction_selection_for_node_c`
- round label: `round 3/5`
- round loop active: `yes`
- rounds remaining: `3`
- latest run id: `20260419_094829_bf16_gemm_v1_fe097e9`
- latest runtime: `42.673632 ms`
- recommended direction: `dir_01`
- active direction: `None`

## Supervisor protocol

- read `docs/supervisor_protocol.md` first
- node-specific protocol: `docs/node_c_protocol.md`
- node context file: `state/node_c_context.md`
- prepare command: `python scripts/graph.py node_c`
- selection command: `python scripts/graph.py approve --direction dir_0X`
- finalize command: `python scripts/graph.py node_c --finalize`
- current dispatch requires direct GPU access: `no`

## Dispatch rule

- main agent stays responsible for graph state, commits, and loop control
- spawn exactly one sub-agent for the current node
- after the sub-agent returns, run the finalize command from the main agent
- then re-read `state/supervisor_task.json` before dispatching the next node

## Multi-round loop

- active loop: `round 3/5` with `3` rounds remaining
- auto-use recommended: `no`
- keep looping until `state/round_loop_state.json` reports `remaining_rounds = 0` or a failure pauses the loop

## Notes

- `Ensure exactly one direction is selected, spawn an implementation sub-agent, then finalize node_c from the main Codex agent.`
