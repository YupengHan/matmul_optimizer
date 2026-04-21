# Supervisor context

This file is for the main Codex supervisor. It decides whether to run the next step directly or dispatch a sub-agent.

## Current dispatch

- dispatch node: `node_b`
- dispatch mode: `sub_agent`
- graph status: `paused_on_explicit_user_redirect`
- round label: `single-run`
- round loop active: `no`
- rounds remaining: `90`
- loop selection strategy: `frontier_every_5_rounds_else_recommended_v1`
- loop selection strategy source: `explicit_user_redirect`
- effective selection mode this round: `frontier`
- auto-select frontier: `no`
- latest run id: `20260421_124420_bf16_gemm_v1_fc400df`
- latest runtime: `45.920258 ms`
- recommended direction: `None`
- active direction: `None`
- display update due at current checkpoint: `yes`
- watchdog status: `idle`
- continue required now: `no`
- stop allowed now: `yes`
- natural stop states disallowed: `no`
- interrupt policy: `none`

## Supervisor protocol

- read `docs/supervisor_protocol.md` first
- node-specific protocol: `docs/node_b_protocol.md`
- node context file: `state/node_b_context.md`
- prepare command: `python scripts/graph.py node_b`
- finalize command: `python scripts/graph.py node_b --finalize`
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
- latest observed progress: `2026-04-21T12:56:12-07:00` via `state/latest_diagnosis.json`
- idle minutes: `N/A`
- watchdog status: `idle`
- continue instruction: `No watchdog action is currently required.`

## Notes

- `Prepare node_b context if needed, spawn a diagnosis sub-agent for live reasoning, and do not replace node_b with a scripted helper before finalizing from the main Codex agent.`
