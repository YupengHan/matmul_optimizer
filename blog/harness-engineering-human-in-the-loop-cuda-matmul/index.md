# Harness Engineering + Human-in-the-Loop: a weekend CUDA matmul project that beat CUTLASS

This was a weekend project, but it was really a question I wanted to test for myself:

**How far can I push a shape-specialized CUDA kernel in two days, on my own machine, with modern LLMs inside a tight harness?**

I am a GPU performance engineer, not part of NVIDIA, and I did **not** start by reading CUTLASS internals. I wanted to try something narrower and more practical: pick **one fixed BF16 GEMM**, on **one RTX 3070 Laptop GPU**, build a reproducible human-in-the-loop optimization loop, and see how close I could get to a strong reference implementation with limited weekend time.

So far, the result is already interesting enough to share: the custom kernel moved from roughly **800 ms** at the beginning to **under 25 ms** on the official benchmark snapshot, with the current best custom run at **24.18 ms**, while the local CUTLASS baseline on the same benchmark is **25.92 ms**. That now puts the official snapshot ahead by about **1.74 ms**, or about **6.71%** in runtime.

That is still not a broad “we beat CUTLASS” story. It is a **fixed-shape local result** and a **proof-of-concept about harness engineering**: with a strong evaluation loop, good profiling, short-context iteration, and human steering at the right moments, a single engineer can move surprisingly far, surprisingly fast.

## Why I built it

I care a lot about **harness engineering**: once models get strong enough, a big part of the problem becomes **how to use them well**.

For kernel optimization, that means:

- fixed benchmark
- reproducible correctness checks
- repeatable runtime measurement
- profiling capture
- structured diagnosis
- controlled implementation attempts
- explicit state tracking across many rounds

That is what this repo is really about. The kernel matters, but the harness matters just as much.

I also think this mirrors a broader engineering trend. Many real workflows are not “solve the general problem.” They are closer to:

> fixed hardware + fixed workload + fixed objective + limited time + repeated local decisions

That is exactly where a good harness can make LLMs much more useful.

## What I learned so far


This project started as a weekend practice, but the part I really care about is not only the final number. It is **what this workflow taught me**.

I had written down a lot of small observations while doing the project, and looking back, they actually fit together into one bigger picture:

### 1. Harness engineering is about taking something already powerful and making it much more useful

My first insight is still the most important one.

Modern LLMs are already very powerful. But a powerful model by itself is not the same thing as a productive engineering system.

**Harness engineering is the work of finding the best way to use a powerful model.**

For this kind of kernel optimization, that means building the surrounding loop:
- fixed benchmark
- correctness checks
- stable measurement
- profiling capture
- branch tracking
- rollback
- comparison across rounds

So the harness is not some accessory around the model. In many cases, it is the thing that turns raw capability into actual engineering progress.

### 2. Harness engineering is also memory management

The more rounds I ran, the more I felt that harness engineering is also a **memory-management problem**.

That is true on both sides.

On the productivity side, the harness reduces how much state I, as the engineer, need to keep in my head:
- which branch tried what
- what regressed
- what plateaued
- what is worth restoring
- what is worth abandoning

On the LLM side, the harness architecture decides how much useful context the model needs to carry, and how much irrelevant history it can safely forget.

So for me, harness engineering is not just automation. It is also **memory management for the engineer and for the model**. When the harness architecture fits the task, the engineer becomes much more productive, and the model becomes much more productive too.

### 3. Current LLMs are genuinely good at incremental optimization

I do not think the right conclusion is “LLMs cannot do performance engineering.” That is too shallow.

My actual experience here is that current models are already very helpful for:
- incremental improvements
- implementation work
- local diagnosis
- turning profiler observations into code changes
- iterating quickly inside a narrow branch

That part is real.

### 4. But current LLMs can still get trapped in local minima and non-pivot directions

At the same time, I also saw a very clear limitation.

A model can keep improving the wrong area.

It can spend many rounds fine-tuning a non-pivot issue, get a few smaller wins, and still end up in a plateau that is not strategically helpful. In other words, the model may still be “improving,” but not in a way that changes the overall outcome very much.

That is why in this project I kept using **human idea changes** and broader **out-of-box thinking chats** to keep the search moving forward.

So one of my strongest takeaways is:
**today’s models are already good at local optimization, but they are not automatically good at choosing the right optimization direction.**

### 5. Profiling tools feel like pre-harness LLMs to me

This is one of the analogies I like most from this project.

Before people figured out how to really use modern LLMs well, the models were already powerful. But without the right harness, that power was not being used effectively.

I think profiling tools are in a very similar stage.

Profiling tools are already very powerful. A year ago they were already powerful. But:
- the user was mostly human
- the learning curve was high
- the workflow around them was still underdeveloped
- a lot of the available signal was not being fully used

So to me, profiling tools today feel a bit like LLMs before better harness engineering:
**already strong, still waiting for better frameworks to make them even more powerful.**

And I think now we are starting to get those frameworks.

### 6. In the future, one “user” of the profiling tool may be the model

This follows naturally from the previous point.

If the profiler already exposes rich signals, and if we now know much more about how to build loops around powerful models, then one obvious next step is:

**the model becomes the profiling-tool user.**

Not in some abstract sci-fi sense. I mean very concretely:
- read the profiler output
- connect it to hardware utilization
- estimate likely bottlenecks
- prioritize branches
- reject low-upside directions
- propose the next implementation move

That is one of the reasons I think this area is so interesting right now.

### 7. Short context often helps powerful agents more than long context

Another very practical lesson: longer context is not automatically better.

For this kind of project, long context often does **not** give more useful information. Sometimes it actively hurts:
- too many stale ideas
- too many mixed branches
- diluted priorities
- harder handoff
- weaker decisions

Short context with the right summary is often much better.

So I do not think “give the model everything” is the right default. For many optimization loops, the better strategy is:
**compress hard, keep the signal, drop the rest.**

### 8. Critical thinking matters even more in the future, not less

As models get stronger, I do not think the engineer becomes less important. I think the engineer’s role becomes more centered on **critical thinking**.

Especially:
- building the evaluation matrix
- deciding what to measure
- deciding what to trust
- deciding what is a real bottleneck versus a side signal
- deciding when to continue, branch, revert, or stop

The model can generate options. The engineer still needs to judge which options are worth spending time on.

### 9. Tool setup matters, and I intentionally kept this one narrow

Part of the point of this project is that I wanted the setup to be constrained and honest.

So for transparency:
- I did **not** start by reading CUTLASS code
- I mainly used **GPT-5.4** and **Codex CLI**
- I also used **GPT-5.4 Pro in chat** for discussion and idea exploration
- but the main optimization workflow was not “just ask GPT-5.4 Pro to solve everything”

I wanted to see what happens when a strong model is placed inside a good harness, on a very specific problem, with a human still steering the direction.

### 10. Engineers may actually get more opportunities, not fewer

One thing I keep coming back to is this:

the current level of CUDA optimization is already the result of very strong engineers pushing close to the limit of human working memory.

A lot of this work is hard not because the machine is mysterious, but because the optimization stack is deep and people cannot keep every layer active in their head at once.

That is why abstraction matters so much. We need different levels of abstraction to preserve the key principles while making the problem tractable.

In that sense, I do not see better models as reducing the need for engineers. I can easily imagine the opposite:
**engineers get more opportunities, because the system now makes it possible to work at more layers and search more paths.**

### 11. CUDA is only one layer; future human-in-the-loop optimization may move closer to PTX

Related to the previous point, I find it very plausible that future optimization workflows go lower.

CUDA is already an abstraction layer. Under it there is PTX, and below that there is even more hardware reality.

If stronger harnesses and stronger model-tool loops make lower-level work more tractable, then I think one very interesting direction is:
**human-in-the-loop PTX optimization.**

Not because abstraction is bad, but because better abstractions may finally let more people operate closer to the machine without losing the global reasoning.

### 12. The optimization history itself became part of the learning

Another thing I did not expect at first: once the project accumulated 30+ rounds, the history itself became useful.

The rounds are not just a log. They reveal structure.

You can already group many attempts into a few families:
- tiling / CTA-shape ideas
- staging / async-copy / pipeline ideas
- shared-memory layout ideas
- epilogue / writeback ideas
- fixed-shape specialization ideas
- and then a separate category for **human idea changes**

That is why I wanted the optimization tree in the post. It is not just a decoration. It is a way to make the search process visible.

### 13. The next bottleneck may be search policy

This is the part I am most excited about for the next version.

In human-in-the-loop kernel optimization, the search space is huge, and the real cost is not only kernel coding speed. It is the time spent deciding which path to explore next.

Looking at the optimization tree, I realized that my current workflow is still basically a single-path search with a rollback mechanism: push one direction forward until it plateaus, step back, then try another branch. That works, but it is not a very efficient way to use the information accumulated across the whole search.

So if I want to improve the workflow itself, the next step is probably not only “write better kernels faster.” It is to make better choices about **which path to explore next**, while keeping multiple candidate states alive instead of collapsing too early onto one branch.

That is why I want to add things like:
- maintaining multiple kernel variants in a queue
- using profiler signals and hardware-efficiency clues to estimate upper and lower bounds for each direction
- applying something closer to **heuristic planning**, **A*-like search**, or even an **RL-style structure** to keep multiple states active and allocate search effort more efficiently

In other words, the next layer is not only kernel optimization.

It is **optimization of the optimization process itself**.


## Current snapshot
![Optimization tree](./matmul_optimization_tree_pretty.svg)

This repo is intentionally narrow:
- one fixed BF16 GEMM shape
- one machine
- one custom kernel path
- one local CUTLASS baseline
- one evolving optimization tree

That narrowness is the point.

I am not trying to claim a general matmul breakthrough. I am trying to test how far **harness engineering + profiling + human steering + LLM assistance** can go in a realistic constrained setup.

The tree below is regenerated from the latest tracked round history in the repo, which now spans **205 recorded measurement rounds**, so it shows the latest exploratory commits while keeping the official best snapshot anchored to the current recorded-best commit **`68c21ac`**.

Because the search has already moved below the local CUTLASS baseline, the chart now places the CUTLASS marker at the point where that threshold was first crossed instead of pinning it to the bottom as a future target. In the current history, that first sub-CUTLASS run is round **46**, version **`22b4466`**, at **25.68 ms**.

At the moment, the official benchmark snapshot in the repo is:
- custom kernel: **24.18 ms**
- local CUTLASS baseline: **25.92 ms**
- result: about **1.74 ms** faster than the local CUTLASS baseline, or about **6.71%** lower runtime, enough to show the harness can cross a strong local baseline on one fixed problem while still leaving room to validate and extend the win

## What I want to add next

The next bottleneck may not be kernel coding speed. It may be **search policy**.

The search space in human-in-the-loop kernel optimization is very large, and the real cost is the time spent choosing which path to explore next.

My next version will likely push in that direction:
- keep multiple kernel variants alive in a queue
- estimate upper and lower bounds for each direction using profiling signals and hardware-efficiency clues
- use something closer to **heuristic planning**, **A*-like search**, or even an **RL-style structure** to choose the next branch

In other words, not just optimize the kernel.

**Optimize the optimizer.**

## Repo

Project repo: `YupengHan/matmul_optimizer`

I am still actively iterating on it, so this post is not a final result write-up. It is a progress note from a weekend experiment that already taught me a lot about where LLM-assisted performance engineering is actually useful today.
