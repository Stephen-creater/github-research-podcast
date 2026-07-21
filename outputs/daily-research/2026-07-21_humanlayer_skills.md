# humanlayer/skills：把周期性 Agent 任务设计成可测量、可迭代的控制回路

- Repository: [humanlayer/skills](https://github.com/humanlayer/skills)
- Revision: [`39fb327`](https://github.com/humanlayer/skills/commit/39fb32786ae7a7cd864cf2c237148c38b1e4db07)
- Date: 2026-07-21
- License: MIT
- Verification: read-only inspection of pinned GitHub metadata, README, MIT license, marketplace manifest, `build-iterated-agentic-loop` skill, `design-control-loop` skill, workflow/memory templates, open issues, pull requests, and releases. Git clone was slow, so the pinned GitHub archive was unpacked under ignored `work/repos/`.

## One-sentence explanation

`humanlayer/skills` is a small public collection of Claude Code skills whose strongest idea is to turn recurring coding-agent work into an observable loop: define a target state, measure it with a sensor, select one bounded increment with a controller, apply it with an agent skill, then feed reviewer memory back into the next run.

## Problem and users

The active problem is how to keep agent automations useful after the first successful run. A scheduled agent can drift, pile up unreviewed work, forget reviewer feedback, or run without a repeatable measurement. This repository addresses that by packaging skills that design or build repo-local agent loops rather than one-off prompts.

The repository targets users already operating Claude Code-style skills and GitHub Actions. Its README exposes four skills: `improve-claude-md`, `narrow-react-prop-types`, `build-iterated-agentic-loop`, and `design-control-loop`. The first two are focused task skills; the latter two are meta-skills for building scheduled, reviewable coding-agent workflows.

## Setup and minimal use

The README shows installation through `npx skills add humanlayer/skills --skill SKILLNAME`, followed by slash-command use inside a project. For this project, the minimal useful use is not to install it blindly. The better trial is read-only: inspect the `design-control-loop` skill and adapt its operating model to one existing automation.

The pinned repository is small and structured as a plugin catalog. `.claude-plugin/marketplace.json` lists the four plugins and points each entry to `./plugins/<name>`. Each plugin has its own `.claude-plugin/plugin.json`, and the main skill content lives under `plugins/<name>/skills/<skill-name>/SKILL.md`. The control-loop skill then keeps longer templates in sibling `references/` files.

## Architecture and entrypoints

The repo is a skill/template bundle, not a runtime framework. The two relevant entrypoints are:

- `plugins/build-iterated-agentic-loop/skills/build-iterated-agentic-loop/SKILL.md`: builds a repo-local skill, GitHub Actions workflow, prompt, memory file, and optional references for a recurring coding-agent task.
- `plugins/design-control-loop/skills/design-control-loop/SKILL.md`: interviews the user to design a loop using control-theory vocabulary, then builds sensor, controller, actuator, workflow, memory, and optional dampener.

The `design-control-loop` skill decomposes a recurring task into a set point, sensor, controller, actuator, disturbances, optional dampener, and human feedback. Its workflow phases require reading the target repo before asking questions, designing the loop with the user, writing a repo-local actuator skill, making each component runnable locally, then wiring CI only after the parts work by hand.

The templates reinforce the same architecture. `workflow-template.yml` has scheduled/manual runs for one sense -> control -> actuate iteration, a `/iterate` path for maintainer comments, PR-body markers for routing comments to the correct workflow, permissions for contents/pull-requests/issues, and a gate that no-ops scheduled runs when an open PR already exists for that loop. `memory-template.md` defines a concise standing-feedback file loaded into future runs.

## Reusable design ideas

First, name the measurement before naming the agent. The control-loop taxonomy forces a set point and sensor before automation. That is a useful correction for recurring tasks that currently depend on "run the agent and judge afterward."

Second, keep sensor, controller, and actuator runnable locally before CI. The workflow should orchestrate commands the maintainer can run by hand, which makes failures easier to debug and avoids hiding all judgment inside one opaque scheduled job.

Third, bound work in progress. The workflow template checks for existing open PRs with the loop label and skips scheduled runs when the review queue is already full. That is directly reusable for automations that should not create more work than a person can inspect.

Fourth, treat memory as steering, not logging. The memory template is meant for durable scope constraints, known false positives, and reviewer preferences. It explicitly avoids raw transcripts and one-off run details.

Fifth, use `/iterate` as a feedback channel for the same PR. The helper script can append a workflow marker to PR bodies and build an iteration prompt from the PR, comments, and memory. That gives a practical pattern for tuning an agent loop without spawning unrelated follow-up tasks.

## Help for recent projects

This helps the current GitHub research podcast automation and the broader Codex/Feishu/AI-video operating workflows. The active project problem is that several recurring tasks already run on schedules, depend on private context, must publish only when complete, and need clear blocker/no-op behavior. The decision is how to make those loops more explicit without overbuilding a full orchestration platform.

Reusable pieces are the control-loop vocabulary and gates: define the set point as "one complete verified repository bundle per local calendar day"; use sensors that check report, script, audio decode, both indexes, sync state, and secret scan; use a controller that selects missing stage versus no-op versus one new repo; use the existing Codex automation as the actuator; keep a small memory file for durable reviewer preferences; and add a flow-control rule that refuses extra completed episodes on the same day.

The smallest useful trial is to write a short internal design note for this exact podcast automation using set point, sensor, controller, actuator, disturbances, and dampener. Do not change the production workflow first. Then convert one repeated audit, such as "today's bundle exists and validates," into a local script that emits a structured measurement. If that measurement is stable, wire it into future automation prompts or CI.

What does not fit and should not be copied: do not copy the Claude-only runner blocks, HumanLayer-specific CodeLayer commands, or the full GitHub Actions workflow into this repo. This project currently runs inside Codex desktop with a local TTS key path and manual Git publishing constraints. Also do not treat the `npx skills add` install path as guaranteed; the repository has an open issue saying the README install direction can install a different skill with the same name in some cases.

## Limitations and risks

This is a young and small repository: GitHub metadata at inspection time showed 94 stars, 4 forks, 1 open issue, no open pull requests, and no releases. Community momentum is real but limited; it is better as a design reference than as a dependency to vendor.

The only open issue reports an installation ambiguity where the README command can install a different skill with the same name. That is a concrete reason to avoid recommending blind installation until the user's current skill toolchain is verified.

The workflow templates are examples, not drop-in production code. They assume GitHub Actions, Bun/Node setup, Claude/HumanLayer runner examples, and PR-based code review. Those assumptions do not match every Codex desktop automation.

The repo packages instructions and templates; it does not provide a scheduler, observability backend, queue, or secret manager. Those pieces still need to come from the target environment.

## Recommendation

结论选择：**Study only / 先研究，不直接安装**。

Study `humanlayer/skills` now as a practical reference for designing bounded, measurable, reviewable agent loops. Reuse the sensor-controller-actuator model, local-first component verification, durable memory, `/iterate` feedback, and PR flow-control ideas. Do not install or copy the workflow wholesale until the current skill installer path and target runtime are verified.

## Primary sources

- [Repository README](https://github.com/humanlayer/skills/blob/39fb32786ae7a7cd864cf2c237148c38b1e4db07/README.md)
- [MIT license](https://github.com/humanlayer/skills/blob/39fb32786ae7a7cd864cf2c237148c38b1e4db07/LICENSE)
- [Marketplace manifest](https://github.com/humanlayer/skills/blob/39fb32786ae7a7cd864cf2c237148c38b1e4db07/.claude-plugin/marketplace.json)
- [Build Iterated Agentic Loop skill](https://github.com/humanlayer/skills/blob/39fb32786ae7a7cd864cf2c237148c38b1e4db07/plugins/build-iterated-agentic-loop/skills/build-iterated-agentic-loop/SKILL.md)
- [Design Control Loop skill](https://github.com/humanlayer/skills/blob/39fb32786ae7a7cd864cf2c237148c38b1e4db07/plugins/design-control-loop/skills/design-control-loop/SKILL.md)
- [Control loop taxonomy](https://github.com/humanlayer/skills/blob/39fb32786ae7a7cd864cf2c237148c38b1e4db07/plugins/design-control-loop/skills/design-control-loop/references/control-loop-taxonomy.md)
- [Workflow template](https://github.com/humanlayer/skills/blob/39fb32786ae7a7cd864cf2c237148c38b1e4db07/plugins/design-control-loop/skills/design-control-loop/references/workflow-template.yml)
- [Memory template](https://github.com/humanlayer/skills/blob/39fb32786ae7a7cd864cf2c237148c38b1e4db07/plugins/design-control-loop/skills/design-control-loop/references/memory-template.md)
- [Open installation issue #1](https://github.com/humanlayer/skills/issues/1)
