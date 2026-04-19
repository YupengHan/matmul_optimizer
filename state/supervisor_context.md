# Supervisor context

This file is for the main Codex supervisor. It decides whether to run the next step directly or dispatch a sub-agent.

## Current dispatch

- dispatch node: `node_b`
- dispatch mode: `sub_agent`
- graph status: `ready_for_node_b`
- round label: `single-run`
- round loop active: `no`
- rounds remaining: `0`
- latest run id: `20260418_201228_bf16_gemm_v1_af155a5`
- latest runtime: `145.344559 ms`
- recommended direction: `None`
- active direction: `None`

## Supervisor protocol

- read `docs/supervisor_protocol.md` first
- node-specific protocol: `docs/node_b_protocol.md`
- node context file: `state/node_b_context.md`
- prepare command: `python scripts/graph.py node_b`
- finalize command: `python scripts/graph.py node_b --finalize`
- node_a requires direct GPU access: `no`

## Dispatch rule

- main agent stays responsible for graph state, commits, and loop control
- spawn exactly one sub-agent for the current node
- after the sub-agent returns, run the finalize command from the main agent
- then re-read `state/supervisor_task.json` before dispatching the next node

## Multi-round loop

- no multi-round loop is active
- to arm one, run `python scripts/graph.py rounds --count N --auto-use-recommended`

## Notes

- `Prepare node_b context if needed, spawn a diagnosis sub-agent, then finalize node_b from the main Codex agent.`
