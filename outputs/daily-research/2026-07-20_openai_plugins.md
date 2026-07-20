# openai/plugins：把 Codex 插件、技能和连接器做成可分发的工作目录

- Repository: [openai/plugins](https://github.com/openai/plugins)
- Revision: [`11c74d6`](https://github.com/openai/plugins/commit/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9)
- Date: 2026-07-20
- License: repository-level license not declared; individual plugins declare their own license in each plugin manifest or plugin directory.
- Verification: read-only inspection of pinned commit, root README, marketplace manifests, GitHub metadata, plugin manifests, app/MCP connector declarations, selected plugin READMEs, and `plugin-eval` code. Issues are disabled on the repository; no releases were listed by `gh release list`. Third-party checkout stayed under ignored `work/repos/`.

## One-sentence explanation

`openai/plugins` is the current public Codex plugin catalog: it shows how a plugin directory combines `.codex-plugin/plugin.json`, optional `skills/`, connector `.app.json`, `.mcp.json`, commands, hooks, assets, and marketplace entries so Codex can discover, install, authenticate, and route plugin-backed workflows.

## Problem and users

The active problem is no longer "how do I write one skill file"; it is "how do I package repeatable Codex capabilities without confusing skills, plugins, MCP servers, app connectors, authentication policy, and installation surfaces." Recent work has touched plugin install boundaries, Feishu/Lark skills, ChatCut and video tools, GitHub automation, and local skill cleanup. The user needs a practical reference for deciding when a capability should be a small skill, when it should be a plugin bundle, and when it must stop for connector login or user takeover.

This repository targets Codex users and plugin authors. The root README says each plugin lives under `plugins/<name>/` with a required `.codex-plugin/plugin.json` and optional companion surfaces. The default marketplace is `.agents/plugins/marketplace.json`, while API-key login users get `.agents/plugins/api_marketplace.json`. The pinned snapshot contains 180 ChatGPT-login marketplace entries and 29 API-key marketplace entries; both are organized by category, not by raw repository popularity.

## Setup and minimal use

For research, the minimal useful action is not installing every plugin. It is inspecting one plugin directory and mapping its surfaces:

1. Read `.codex-plugin/plugin.json` for name, version, description, license, skills path, app path, MCP path, display text, capabilities, and default prompts.
2. Read `.app.json` when the plugin needs a Codex app connector, such as GitHub, Figma, Google Drive, Slack, or OpenAI Platform.
3. Read `.mcp.json` when API-key sessions or local tools need MCP wiring.
4. Read `skills/` only after selecting a specific plugin workflow.
5. Check marketplace policy for installation and authentication timing.

The GitHub plugin is a compact example: `plugins/github/.codex-plugin/plugin.json` declares skills, apps, MCP servers, capabilities, and MIT license; `.app.json` points to the GitHub app connector for ChatGPT-login Codex sessions; `.mcp.json` declares GitHub's hosted MCP server using `GITHUB_PAT_TOKEN` for API-key Codex sessions; the README explicitly says ChatGPT-login sessions do not require a PAT because Codex manages connector auth.

## Architecture and entrypoints

The repository is a marketplace plus many plugin packages, not a runtime framework. The root README defines the directory contract:

- `.codex-plugin/plugin.json`: required manifest and Codex-facing metadata.
- `skills/`: bundled skills, each with the usual `SKILL.md` shape.
- `.app.json`: connector dependency declaration for app-backed workflows.
- `.mcp.json`: MCP server declaration for hosted, OAuth, local, or API-key flows.
- `agents/`, `commands/`, `hooks.json`, `assets/`, `ui/`, `scripts/`: optional plugin-level companion surfaces.
- `.agents/plugins/marketplace.json`: ChatGPT-login marketplace.
- `.agents/plugins/api_marketplace.json`: API-key marketplace.

The richer examples show different plugin classes. `plugins/figma` combines an app connector, an OAuth MCP endpoint, multiple Figma skills, agents, commands, hooks, and UI assets for design-to-code workflows. `plugins/openai-developers` combines an OpenAI Platform connector, a local MCP confirmation server, scripts for API-key setup, Agents SDK skills, ChatGPT Apps skills, and local tests. `plugins/remotion` is a smaller creativity plugin that mostly packages one Remotion skill and assets. `plugins/plugin-eval` is especially useful because it is both a Codex plugin and a local Node CLI for evaluating skills/plugins.

## Reusable design ideas

First, plugin packaging should make dependency boundaries visible. A plugin manifest can point to skills, app connectors, and MCP servers separately. That is cleaner than hiding authentication or external tool needs inside a long `SKILL.md`.

Second, installation and authentication are policy fields, not just prose. The marketplace entries include `installation` and `authentication`, and the API marketplace can differ from the ChatGPT-login marketplace. This matches the user's standing boundary: if login, authorization, or plugin installation is missing, stop at the takeover point rather than substituting another tool.

Third, a plugin can be local-first while still being chat-friendly. `plugin-eval` routes natural prompts to deterministic local commands, static budget checks, measurement plans, and optional live benchmarks. That pattern fits existing automation work because the chat layer explains intent while the CLI layer performs repeatable verification.

Fourth, current official guidance has moved away from the deprecated `openai/skills` catalog. The `openai/skills` README now points users to this repository and the Codex build-plugin docs for current skill and plugin examples. For future skill work, this means new durable capabilities should usually be considered as skill-only plugins or plugin bundles rather than copied from the old catalog without migration checks.

## Help for recent projects

This directly helps the current Codex desktop and automation operating system, especially plugin-specific tasks, skill cleanup, GitHub research automation, AI-video tooling, and Feishu/Lark integration planning. The active decision is how to keep many tools usable without turning every workflow into a fragile pile of ad hoc prompts.

Reusable pieces are the packaging contract and evaluation method: use `.codex-plugin/plugin.json` as the front door, keep `skills/` for reusable instructions, declare app connectors in `.app.json`, declare MCP servers in `.mcp.json`, expose commands/hooks only when the workflow needs them, and put install/auth policy in marketplace metadata. For the local skill/plugin cleanup line, `plugin-eval` offers a concrete static-analysis and measurement pattern: inspect manifest structure, budget pressure, observed usage, code quality, and recommended next action before installing or promoting a plugin.

The smallest useful trial is to pick one existing local capability, such as a Feishu helper or AI-video production skill, and write a minimal skill-only plugin wrapper around it in a scratch workspace. The trial should include only one `plugin.json`, one `skills/<name>/SKILL.md`, optional `.app.json` only if a real connector is needed, and a tiny validation checklist modeled after `plugin-eval`: manifest present, skill discoverable, no secrets, no private paths, and clear authentication stop point.

What should not be copied: do not mirror the whole official marketplace into the user's repo, do not assume every `.app.json` connector is installed or authorized, do not use plugin README claims as permission to access external accounts, and do not copy proprietary plugin contents into unrelated deliverables. The repository is a reference catalog, not a license to bundle every plugin or bypass connector auth.

## Limitations and risks

The repository has no repository-level license, and plugins differ: some manifests say MIT, some proprietary, and some depend on third-party developer terms. Reuse must be per-plugin and per-file, not blanket copying.

Issues are disabled on `openai/plugins`, so normal open-issue maintenance signals are weaker than in repos with public bug triage. `gh repo view` shows recent update and push activity, but it does not replace release notes or issue evidence.

The catalog is fast-moving. At pinned commit `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9`, GitHub metadata showed a push on 2026-07-14 and repo update on 2026-07-20; plugin names, connector ids, marketplace policy, and bundled skills may drift.

Many examples require connectors, OAuth, API keys, or app-specific terms. The safe operational rule is to inspect manifests first, then explicitly install/connect only the named plugin requested by the user.

## Recommendation

结论选择：**Use now / 现在就用**。

Use `openai/plugins` immediately as the current reference for Codex plugin packaging and plugin-install decision boundaries. The best near-term reuse is a small local plugin-wrapper trial plus a plugin-eval-style validation checklist. Do not migrate private workflows wholesale, do not copy the marketplace, and do not treat app-backed plugins as available until the current Codex session exposes or authorizes their tools.

## Primary sources

- [Root README](https://github.com/openai/plugins/blob/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9/README.md)
- [Default marketplace](https://github.com/openai/plugins/blob/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9/.agents/plugins/marketplace.json)
- [API-key marketplace](https://github.com/openai/plugins/blob/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9/.agents/plugins/api_marketplace.json)
- [GitHub plugin manifest](https://github.com/openai/plugins/blob/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9/plugins/github/.codex-plugin/plugin.json)
- [GitHub plugin README](https://github.com/openai/plugins/blob/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9/plugins/github/README.md)
- [OpenAI Developers plugin README](https://github.com/openai/plugins/blob/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9/plugins/openai-developers/README.md)
- [Figma plugin README](https://github.com/openai/plugins/blob/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9/plugins/figma/README.md)
- [Plugin Eval README](https://github.com/openai/plugins/blob/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9/plugins/plugin-eval/README.md)
- [Plugin Eval scoring code](https://github.com/openai/plugins/blob/11c74d6ba24d3a6d48f54a194cd00ef3beea18f9/plugins/plugin-eval/src/core/scoring.js)
