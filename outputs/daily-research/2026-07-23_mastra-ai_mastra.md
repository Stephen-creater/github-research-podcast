# mastra-ai/mastra：用 TypeScript 把 agent、workflow、memory、evals 组合成 AI 产品工程层

- Repository: [mastra-ai/mastra](https://github.com/mastra-ai/mastra)
- Revision: [`c1a66a2`](https://github.com/mastra-ai/mastra/commit/c1a66a27b8679abaa01ea57a9260c01d1c6f93de)
- Date: 2026-07-23
- License: mixed repository license. The README and `LICENSE.md` describe Apache-2.0 for most code, with directories named `ee/` under Mastra Enterprise License.
- Verification: read-only inspection of GitHub API metadata, pinned main commit, README, `LICENSE.md`, latest release metadata, open issues and pull requests, docs under `docs/src/content/en/docs`, selected package manifests, and selected TypeScript entrypoints. `git pull` and `git ls-remote` to GitHub HTTPS timed out in this environment, so no third-party code was executed or cloned.

## One-sentence explanation

`mastra-ai/mastra` is a modern TypeScript framework for building AI applications and agents, with first-class primitives for agents, explicit graph workflows, human approval, memory, RAG, MCP, evals, observability, deployment surfaces, and Studio debugging.

## Problem and users

The recent project problem is not "how to call one LLM" anymore. Current work has several repeating needs: Codex-centered automations need resumable control loops, Feishu/Lark and browser tasks need permission-aware tool wiring, AI-video production needs a reliable planning and QA layer around generation, and AI productization work needs a way to evaluate and observe agents instead of judging them by anecdotes.

Mastra targets developers building AI-powered applications in TypeScript. Its README says it can run with React, Next.js, Node, or as a standalone server, and positions the stack as a path from early prototypes to production-ready AI products. The repository topics and docs focus on agents, workflows, model routing, memory, RAG, MCP, evals, observability, TTS, and server integrations.

This candidate scored highest among uncovered options checked for today. `larksuite/cli` and `larksuite/lark-openapi-mcp` remain important but were already covered in the earlier single-repo production set; `browserbase/stagehand` was already covered for browser automation; another video-rendering candidate would duplicate yesterday's Remotion episode. `mastra-ai/mastra` scored approximately 87/100: direct help to active projects 34/40, reusable implementation and design 22/25, evidence and maintenance maturity 13/15, novelty 9/10, and community momentum 9/10. Raw stars were not the deciding factor; the decisive fit is that it turns agent behavior, workflow state, memory, evaluation, and observability into reusable product architecture.

## Setup and minimal use

The README recommends starting with:

```bash
npm create mastra@latest
```

The manual-install docs show the smaller dependency path: install `typescript`, `@types/node`, `mastra`, `@mastra/core`, and `zod`, add `dev` and `build` scripts using `mastra dev` and `mastra build`, and use modern ES module TypeScript settings. The agents docs show a minimal `Agent` from `@mastra/core/agent` with `id`, `name`, `instructions`, and `model`, then registering it in a `Mastra` instance. The workflows docs show `createStep()` plus `createWorkflow()` with input/output schemas and `.then(...).commit()`.

For this project, the smallest useful trial should not be a platform migration. Create one local Mastra sandbox that models an existing automation as a typed workflow: gather public source evidence, draft a report, run a validator, request human input only if a required credential or publication decision is missing, and record observability/eval data for one run. Do not connect private Feishu, mail, or production credentials in the first trial.

## Architecture and entrypoints

The repository is a large TypeScript monorepo. The main conceptual entrypoints are:

- `@mastra/core`: common runtime exports for agents, workflows, storage, schedules, logger, memory interfaces, eval scorers, MCP server base classes, background tasks, observability hooks, and the `Mastra` instance.
- `@mastra/core/agent`: exports the `Agent` API, message conversion, signals, schedule types, subagent compatibility, network/delegation options, and goal-related utilities.
- `@mastra/core/workflows`: exports `createWorkflow`, `createStep`, execution engines, scheduler/state-reader utilities, workflow types, and control-flow building blocks.
- `@mastra/memory` plus core memory interfaces: message history, working memory, semantic recall, observational memory, memory processors, and storage-backed thread state.
- `@mastra/mcp`: both `MCPClient` for consuming external MCP tools and `MCPServer`/server base classes for exposing Mastra tools, agents, workflows, prompts, and resources through MCP-compatible clients.
- `@mastra/evals`: scorer APIs for rule-based, statistical, and model-graded checks, including live evaluations and CI-oriented scoring.
- `@mastra/observability`: trace, log, metric, feedback, exporter, and sensitive-data filtering surfaces for inspecting agent runs, workflow steps, tool calls, and model interactions.
- CLI and docs: `npm create mastra@latest`, `mastra dev`, `mastra build`, docs for agent builder, agent controller, deployment, long-running agents, Studio, workflows, memory, evals, observability, and MCP.

The `Mastra` class itself imports and wires a broad set of runtime services: agents, workflows, memory, vector stores, TTS, model gateways, MCP servers, schedules, background tasks, pub/sub, storage domains, observability exporters, hooks, workers, datasets, workspaces, and license handling. That is useful evidence that this is an application runtime, not just a thin prompt wrapper.

The latest release returned by the GitHub API was `@mastra/core@1.51.0`, published on 2026-07-15. Its highlights are especially relevant: durable-agent crash recovery, scoped `AgentController` sessions for parallel sessions per resource, Mastra Platform workspace/sandbox providers, public Mastra Code SDK, richer MCP server streaming/notifications, structured scorer and dataset identity work, provider-tool-call observability spans, workflow topic cleanup, and multiple durable-agent fixes. Current open issues and PRs on 2026-07-23 show active work on channels, Slack tenant resolution, factory workflow, dataset scorer selection, structured judge results, and Studio compare panels.

## Reusable design ideas

First, separate open-ended agent reasoning from explicit workflows. Mastra docs tell users to use agents when the steps are unknown, and workflows when the process is predetermined and needs control over data movement and execution order. That distinction is directly reusable in automation design: do not let an LLM decide every step when the daily podcast loop has known gates such as pull, duplicate check, report validation, audio verification, secret scan, commit, and push.

Second, treat workflow state and suspend/resume as product features. The suspend-and-resume docs describe storing workflow snapshots in configured storage, then resuming from a specific step with typed `resumeData`. This maps well to real automation blockers: TTS credentials missing, a login required, a human approval needed before publishing, or a long-running task recovering after process restart.

Third, make memory layered instead of dumping all history into prompts. The memory docs distinguish message history, observational memory, working memory, semantic recall, multi-user threads, and memory processors. That is a useful evaluation frame for current context-management and AnySpecs-style work: decide which facts are working memory, which belong to semantic recall, which should be compressed observations, and which should stay out of the prompt.

Fourth, use evals and observability from the start. The eval docs describe scorers as automated tests for non-deterministic agent outputs, and the observability docs describe traces across agent runs, workflow steps, tool calls, model interactions, logs, metrics, cost, and feedback. This can be reused as a quality contract for AI-video planning agents, Feishu automations, and recurring research scripts.

Fifth, MCP is a useful boundary rather than only an integration list. Mastra can consume tools through `MCPClient` and expose Mastra tools, agents, workflows, prompts, and resources through `MCPServer`. That fits the existing Codex/plugin/Lark direction: keep connectors permissioned and typed, avoid embedding credentials in prompts, and make tool approval explicit where needed.

## Help for recent projects

Which active project problem or decision does this help? It helps the decision of whether current agentic work should stay as ad hoc scripts plus prompts, or be modeled as a product-grade runtime with explicit workflow state, memory, tool boundaries, evals, and observability. The most immediate beneficiaries are the recurring GitHub research podcast automation, Feishu/Lark operating workflows, AI-video production QA, and AI productization planning.

What code, architecture, workflow, or evaluation method can be reused? Reuse the architecture pattern: agents for open-ended reasoning, workflows for deterministic gates, storage-backed suspend/resume for missing credentials or human approval, MCP as the tool boundary, memory layers for durable context, scorers for output checks, and traces/logs/metrics for debugging. The specific code to study is the workflow API, the `Mastra` runtime composition, memory docs, MCP docs, and eval/observability docs.

What is the smallest useful trial? Build one local proof of concept around the existing daily research loop: a workflow with steps for candidate scoring, primary-source collection, report drafting, validation, script derivation, audio verification, and publish gating. Use a tiny fake or public-only dataset first. Add one scorer that checks whether the recent-project-help section answers the four mandatory questions, and one trace or log surface that shows where a run stopped.

What does not fit and should not be copied? Do not migrate all current Codex, Feishu, or video workflows into Mastra immediately. Do not copy enterprise `ee/` code or assume it is Apache-2.0. Do not add production Feishu, email, browser, or TTS credentials to a trial. Do not replace simple shell scripts that already work with a framework just for architectural neatness. Do not let Studio or cloud deployment distract from the first local workflow-state/eval experiment.

## Limitations and risks

The framework is broad. That is useful for productization, but it also means a real adoption will bring Node/TypeScript project structure, package management, storage choices, model-provider configuration, observability storage, and deployment decisions. For a narrow automation, that can be too heavy.

The license is mixed. Most code is Apache-2.0, but directories named `ee/` are under Mastra Enterprise License. The GitHub API reports `NOASSERTION` for SPDX. Any commercial or redistributed use needs path-level license awareness.

The project is moving quickly. The latest release contains many durable-agent and workflow fixes, and open issues include memory-scope concerns and product-surface work. Active maintenance is a positive sign, but it also means APIs and recommended patterns may change. A trial should pin versions and avoid deep coupling until the exact primitives prove useful.

The repository could not be cloned through `git` in this run because GitHub HTTPS timed out for git operations. GitHub API and raw file access worked, so primary-source read-only inspection was still possible. The local workflow should retry git synchronization before publishing this repository's own outputs.

## Recommendation

结论选择：**Study only / 仅研究并做一个小型本地试验**。

Study `mastra-ai/mastra` now as an architecture reference for turning ad hoc agent loops into product-grade TypeScript workflows with memory, MCP, evals, and observability. Run one local proof of concept around an existing public-only automation. Do not migrate production Feishu, AI-video, or podcast workflows until the trial proves that workflow state, suspend/resume, scoring, and traceability materially reduce operational risk.

## Primary sources

- [Repository README](https://github.com/mastra-ai/mastra/blob/c1a66a27b8679abaa01ea57a9260c01d1c6f93de/README.md)
- [Pinned commit](https://github.com/mastra-ai/mastra/commit/c1a66a27b8679abaa01ea57a9260c01d1c6f93de)
- [Repository metadata API](https://api.github.com/repos/mastra-ai/mastra)
- [Latest release `@mastra/core@1.51.0`](https://github.com/mastra-ai/mastra/releases/tag/%40mastra/core%401.51.0)
- [`LICENSE.md`](https://github.com/mastra-ai/mastra/blob/c1a66a27b8679abaa01ea57a9260c01d1c6f93de/LICENSE.md)
- [`@mastra/core` package manifest](https://github.com/mastra-ai/mastra/blob/c1a66a27b8679abaa01ea57a9260c01d1c6f93de/packages/core/package.json)
- [`Mastra` runtime entrypoint](https://github.com/mastra-ai/mastra/blob/c1a66a27b8679abaa01ea57a9260c01d1c6f93de/packages/core/src/mastra/index.ts)
- [`@mastra/core/agent` exports](https://github.com/mastra-ai/mastra/blob/c1a66a27b8679abaa01ea57a9260c01d1c6f93de/packages/core/src/agent/index.ts)
- [`@mastra/core/workflows` exports](https://github.com/mastra-ai/mastra/blob/c1a66a27b8679abaa01ea57a9260c01d1c6f93de/packages/core/src/workflows/index.ts)
- [`@mastra/core/memory` exports](https://github.com/mastra-ai/mastra/blob/c1a66a27b8679abaa01ea57a9260c01d1c6f93de/packages/core/src/memory/index.ts)
- [`@mastra/core/mcp` server base](https://github.com/mastra-ai/mastra/blob/c1a66a27b8679abaa01ea57a9260c01d1c6f93de/packages/core/src/mcp/index.ts)
- [Agents overview docs](https://github.com/mastra-ai/mastra/blob/c1a66a27b8679abaa01ea57a9260c01d1c6f93de/docs/src/content/en/docs/agents/overview.mdx)
- [Workflows overview docs](https://github.com/mastra-ai/mastra/blob/c1a66a27b8679abaa01ea57a9260c01d1c6f93de/docs/src/content/en/docs/workflows/overview.mdx)
- [Suspend and resume docs](https://github.com/mastra-ai/mastra/blob/c1a66a27b8679abaa01ea57a9260c01d1c6f93de/docs/src/content/en/docs/workflows/suspend-and-resume.mdx)
- [Memory overview docs](https://github.com/mastra-ai/mastra/blob/c1a66a27b8679abaa01ea57a9260c01d1c6f93de/docs/src/content/en/docs/memory/overview.mdx)
- [Evals overview docs](https://github.com/mastra-ai/mastra/blob/c1a66a27b8679abaa01ea57a9260c01d1c6f93de/docs/src/content/en/docs/evals/overview.mdx)
- [Observability overview docs](https://github.com/mastra-ai/mastra/blob/c1a66a27b8679abaa01ea57a9260c01d1c6f93de/docs/src/content/en/docs/observability/overview.mdx)
- [MCP overview docs](https://github.com/mastra-ai/mastra/blob/c1a66a27b8679abaa01ea57a9260c01d1c6f93de/docs/src/content/en/docs/mcp/overview.mdx)
- [Manual install docs](https://github.com/mastra-ai/mastra/blob/c1a66a27b8679abaa01ea57a9260c01d1c6f93de/docs/src/content/en/docs/getting-started/manual-install.mdx)
- [Open issue #20076](https://github.com/mastra-ai/mastra/issues/20076)
- [Open PR #20022](https://github.com/mastra-ai/mastra/pull/20022)
