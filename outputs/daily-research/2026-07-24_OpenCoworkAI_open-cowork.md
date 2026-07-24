# OpenCoworkAI/open-cowork：把 Claude Code、MCP、Skills 和 Feishu 远程控制做成桌面 agent 产品壳

- Repository: [OpenCoworkAI/open-cowork](https://github.com/OpenCoworkAI/open-cowork)
- Revision: [`6f0c047`](https://github.com/OpenCoworkAI/open-cowork/commit/6f0c04741386b8600aa977f14ac0679d2203bd1b)
- Date: 2026-07-24
- License: MIT
- Verification: read-only inspection of GitHub API metadata, pinned main commit, `readme.md`, `LICENSE`, latest release metadata, open issues and pull requests, repository tree, `package.json`, and selected TypeScript entrypoints for sandboxing, MCP, Skills, memory, Feishu remote control, and PR review automation. `git pull` / `git fetch` to this project remote failed through GitHub HTTPS in this environment, so third-party code was not cloned or executed.

## One-sentence explanation

`OpenCoworkAI/open-cowork` is an Electron desktop application that packages coding agents, Claude Code-style workflows, MCP connectors, Skills, workspace sandboxing, trace UI, memory, schedules, and Feishu/Slack remote control into a one-click Windows/macOS agent product.

## Problem and users

The active problem is no longer only "which coding agent is best." Current work repeatedly needs a practical product shell around agents: safe local file access, explicit permission prompts, desktop/browser/Feishu integration, reusable Skills, long-running sessions, current-state memory, observable tool execution, and a clear boundary between private user workspaces and publishable outputs.

This repository targets users who want desktop automation without manually assembling a terminal, Node runtime, Claude Code, MCP servers, document-generation skills, remote-control channels, and sandbox isolation. The README positions it as an open-source implementation of Claude Cowork with installers for Windows and macOS, one-click setup, multi-model support, VM-level sandbox isolation with WSL2 or Lima, MCP integration, GUI operation, built-in document Skills, and Feishu/Lark plus Slack remote control.

This candidate scored highest among uncovered options checked today: direct help to recent projects 37/40, reusable implementation/design 22/25, evidence and maintenance maturity 12/15, novelty versus previous reports 9/10, and community/recent activity 8/10, for approximately 88/100. Raw stars did not decide the choice. The fit is that Open Cowork is close to current Codex desktop, Skills/plugin, Feishu/Lark, browser/computer-use, recurring automation, and AdventureX agent-productization questions.

Other plausible candidates were weaker for today. A pure "personal AI identity" project would connect to the Second Me direction, but would not help as much with operational sandboxing and Feishu control. Another browser automation or video-rendering repo would duplicate earlier Stagehand and Remotion coverage. A generic agent framework would overlap with the Mastra episode from 2026-07-23.

## Setup and minimal use

The README offers three paths:

- macOS Homebrew cask: `brew tap OpenCoworkAI/tap` then `brew install --cask --no-quarantine open-cowork`.
- Download platform installers from the release page: `.exe` for Windows and `.dmg` for Apple Silicon macOS.
- Build from source with `git clone`, `npm install`, `npm run rebuild`, and `npm run dev`; local installer build uses `npm run build`.

The pinned `package.json` describes version `3.3.1`, Node `>=22`, Electron/Vite/React/TypeScript tooling, and build steps for bundled Node, Python, GUI tools, WSL agent, Lima agent, MCP bundle, TypeScript, Vite, pre-build checks, and Electron Builder. Runtime dependencies include Anthropic, OpenAI, Google GenAI, Lark SDK, Slack SDK, MCP TypeScript SDK, better-sqlite3, Electron Store, ngrok, and the `pi` agent packages.

For the current workspace, the smallest useful trial should be read-only and local. Install nothing first. Study the architecture and extract a short checklist for an agent desktop shell: workspace path contract, command execution boundary, MCP child-process environment filtering, permission dialog, Feishu webhook/WebSocket verification, Skills discovery rules, memory context policy, and trace UI. Only after that, test the app in a disposable public workspace with no private credentials.

## Architecture and entrypoints

The repository is mainly TypeScript with Python, JavaScript, CSS, shell, PowerShell, NSIS, and HTML support. It is organized like a desktop app rather than a library:

- `src/main/index.ts`: Electron main process entrypoint.
- `src/main/agent/agent-runner.ts`: agent execution layer, with nearby modules for loop guard, message end handling, compaction extension, model resolution, session runtime, shared auth, subagents, and tool result utilities.
- `src/main/sandbox/`: sandbox adapters and bridges for native execution, WSL, Lima, sync, bootstrap, path guard, path resolver, and platform-specific agents.
- `src/main/tools/`: sandbox tool execution and path-containment helpers.
- `src/main/mcp/mcp-manager.ts`: MCP server config CRUD, stdio/SSE/streamable HTTP transports, OAuth retry, server lifecycle, tool/resource/prompt discovery, timeouts, and provider-compatible tool-name normalization.
- `src/main/skills/skills-manager.ts`: built-in/global/project skill discovery, `SKILL.md` metadata parsing, hot reload, plugin install/uninstall, and path validation for skill names.
- `src/main/remote/`: remote gateway, message router, tunnel manager, remote config, Feishu and Slack channels, and stdio channel.
- `src/main/remote/channels/feishu/feishu-channel.ts`: Feishu token refresh, bot info, WebSocket or webhook mode, HMAC signature verification, retrying sends, and message handling.
- `src/main/memory/`: message history, context management, memory extraction, retrieval, prompt optimization, eval harness, state store, and tools.
- `src/renderer/components/`: chat, settings, context, trace, permissions, remote-control setup, sandbox setup, subagent progress, and message/tool rendering components.
- `.github/workflows/codex-pr-review.yml`, `.github/prompts/codex-pr-review.md`, and `.github/scripts/deepseek-*.mjs`: CI-side agent review automation, including follow-up context reset after rebase/force-push and advisory review policy.

Several implementation details are directly relevant. `PathGuard` blocks dangerous paths and command patterns, checks sandbox membership, resolves symlinks, and treats platform-specific forbidden directories differently for Linux/WSL and macOS/Lima. `PathResolver` maps virtual paths to real paths, validates mount-root containment, rejects `..` and `~`, and checks symlink escapes through existing parents. `McpManager` normalizes MCP tool names to fit model/provider limits, supports multiple transports, and uses five-minute timeouts for tool discovery and calls. `SkillsManager` validates skill names against separators and parent references, skips dangling symlinks, and distinguishes built-in, global, and project-level skills. The Feishu channel rejects webhook requests without a verification token/signature path and uses retry logic for sends.

The latest GitHub release was `v3.3.1`, published on 2026-05-23. Its release notes emphasize security hardening and provider/installer reliability: permission dialog gating for local-agent tool calls, tool-call loop detection, Lima/WSL path traversal fix, thinking-block preservation, MCP tool-name sanitation, longer MCP timeouts, bundled npm package handling on Windows, renderer tab-switch fix, and release CI fixes. Open issues and PRs on 2026-07-24 show continued work around MCP child-process environment leakage, scheduled-task reactive polling, sandbox detection on Windows, quit cleanup, CI, dependency upgrades, i18n, and Feishu/Slack-adjacent platform integration.

## Reusable design ideas

First, productize the permission boundary as UI, not only as backend checks. Open Cowork has both sandbox/path guard code and a renderer `PermissionDialog`. Current Codex/Feishu automations should copy the pattern, not the code: a tool call that can modify files, run commands, or touch connected apps needs a visible approval model, a storage rule, and an audit trail.

Second, separate "workspace root" from "host machine." The path resolver and guard make workspace containment a first-class concern. That is useful for recurring automations and Feishu-controlled actions because remote prompts should never imply broad access to the whole Mac. A daily research or AI-video workflow should define which source folders, maintained code, outputs, scratch areas, and third-party repos are allowed before execution starts.

Third, treat MCP servers as untrusted child processes. The open issue about MCP child processes inheriting `process.env`, plus the PR replacing env leakage with a default environment, is a concrete reminder for Codex/plugin work: connector subprocesses should receive minimal env, explicit credentials, bounded cwd, timeout, and log redaction.

Fourth, keep Skills as lifecycle-managed artifacts. `SkillsManager` checks directory names, reads `SKILL.md`, watches storage, skips dangling symlinks, and handles plugin runtime services. That maps directly to current local skill/plugin cleanup and AnySpecs-style context-packaging work: Skills need discovery, validation, ownership, hot reload, and uninstall semantics instead of being loose prompt files.

Fifth, remote control needs channel-specific verification. The Feishu channel requires token refresh, bot identity, WebSocket or webhook mode, HMAC signature verification, retries, and message routing. That is a better reference for Feishu automation than a plain webhook demo because it shows the operational pieces required before letting remote chat drive local work.

Sixth, trace and memory should be visible product surfaces. The README highlights real-time trace, while the code includes memory manager and prompt/context optimization modules. For agent products, the user needs to see what tools ran, why a task paused, what context was used, and what state is being reused.

## Help for recent projects

Which active project problem or decision does this help? It helps decide how far a desktop-agent product should go for AdventureX and related AI-productization work: should the MVP be a generic "agent desktop," a low-friction continuation surface, or a smaller control layer around Codex/Feishu/video workflows? It also helps ongoing Codex/Skills/plugin cleanup, Feishu remote operation, and recurring automation hardening.

What code, architecture, workflow, or evaluation method can be reused? Reuse the architecture checklist: Electron main/renderer separation for agent control, sandbox adapters for WSL/Lima/native execution, path containment and symlink checks, explicit permission dialogs, MCP lifecycle and tool-name normalization, minimal child-process env, Feishu channel verification, Skills discovery and validation, memory/context strategy, trace UI, and CI bots that discard stale review context after non-linear PR history.

What is the smallest useful trial? Create a public-only "desktop agent shell checklist" for one current workflow, then run a disposable local test with no private credentials: one workspace folder, one skill, one MCP server with a deliberately minimal env, one command that requires permission, one trace entry, and one Feishu-style remote message simulated or sent through a test bot only if credentials are intentionally provided. The acceptance check is whether the workflow can explain allowed paths, denied paths, tool approvals, env exposure, and stop/resume state.

What does not fit and should not be copied? Do not copy the whole Electron app into current projects. Do not bypass macOS quarantine or install unsigned desktop apps in the main work environment just to inspect a repo. Do not connect personal Feishu, Slack, browser, or TTS credentials during the first trial. Do not assume path guards alone make destructive operations safe. Do not adopt their exact model/provider list or Chinese-model presets without current pricing, compliance, and quality checks. Do not publish private workspace paths or chat contents as examples.

## Limitations and risks

The repo is broad and young: created in 2026, with major surface area across Electron, sandboxing, MCP, Skills, remote control, memory, installers, and CI bots. That breadth is useful for product reference but increases integration and security risk.

The sandbox is layered, not absolute. The README says WSL2 and Lima provide enhanced isolation, but fallback execution can run natively with path-based restrictions. Current issues mention sandbox detection and cleanup problems, and the release notes include a path traversal fix. Any adoption should treat sandbox behavior as something to test on the exact platform.

MCP and remote control expand the blast radius. Open issue #305 explicitly flags MCP child-process environment inheritance including API keys. This makes the repo more valuable as a hardening reference, but also shows why connected tools should start from least privilege.

The release cadence and dependency surface are active. Open PRs include dependency updates for Anthropic SDK, Lark SDK, MCP SDK, OpenAI SDK, actions, and `pi` packages. A trial should pin the inspected commit and avoid using floating model/provider behavior as a stable contract.

The README's installation path includes `--no-quarantine` for Homebrew cask. That may reduce user friction, but it is not a pattern to copy into internal security-sensitive workflows without a separate trust and signing decision.

## Recommendation

结论选择：**Study only / 仅研究并做一个安全边界试验**。

Study `OpenCoworkAI/open-cowork` now as a desktop-agent product-shell reference for Codex/Skills/MCP/Feishu workflows and AdventureX agent-productization decisions. The smallest useful next step is a public-only checklist plus a disposable sandbox trial focused on path boundaries, permission prompts, MCP env minimization, Feishu-style remote routing, trace, and stop/resume state. Do not migrate active Feishu, AI-video, or private desktop workflows into this app yet.

## Primary sources

- [Repository](https://github.com/OpenCoworkAI/open-cowork)
- [Pinned commit](https://github.com/OpenCoworkAI/open-cowork/commit/6f0c04741386b8600aa977f14ac0679d2203bd1b)
- [Repository metadata API](https://api.github.com/repos/OpenCoworkAI/open-cowork)
- [`readme.md`](https://github.com/OpenCoworkAI/open-cowork/blob/6f0c04741386b8600aa977f14ac0679d2203bd1b/readme.md)
- [`LICENSE`](https://github.com/OpenCoworkAI/open-cowork/blob/6f0c04741386b8600aa977f14ac0679d2203bd1b/LICENSE)
- [Latest release `v3.3.1`](https://github.com/OpenCoworkAI/open-cowork/releases/tag/v3.3.1)
- [`package.json`](https://github.com/OpenCoworkAI/open-cowork/blob/6f0c04741386b8600aa977f14ac0679d2203bd1b/package.json)
- [`src/main/agent/agent-runner.ts`](https://github.com/OpenCoworkAI/open-cowork/blob/6f0c04741386b8600aa977f14ac0679d2203bd1b/src/main/agent/agent-runner.ts)
- [`src/main/sandbox/path-guard.ts`](https://github.com/OpenCoworkAI/open-cowork/blob/6f0c04741386b8600aa977f14ac0679d2203bd1b/src/main/sandbox/path-guard.ts)
- [`src/main/sandbox/path-resolver.ts`](https://github.com/OpenCoworkAI/open-cowork/blob/6f0c04741386b8600aa977f14ac0679d2203bd1b/src/main/sandbox/path-resolver.ts)
- [`src/main/mcp/mcp-manager.ts`](https://github.com/OpenCoworkAI/open-cowork/blob/6f0c04741386b8600aa977f14ac0679d2203bd1b/src/main/mcp/mcp-manager.ts)
- [`src/main/skills/skills-manager.ts`](https://github.com/OpenCoworkAI/open-cowork/blob/6f0c04741386b8600aa977f14ac0679d2203bd1b/src/main/skills/skills-manager.ts)
- [`src/main/remote/channels/feishu/feishu-channel.ts`](https://github.com/OpenCoworkAI/open-cowork/blob/6f0c04741386b8600aa977f14ac0679d2203bd1b/src/main/remote/channels/feishu/feishu-channel.ts)
- [`src/main/memory/memory-manager.ts`](https://github.com/OpenCoworkAI/open-cowork/blob/6f0c04741386b8600aa977f14ac0679d2203bd1b/src/main/memory/memory-manager.ts)
- [`src/renderer/components/PermissionDialog.tsx`](https://github.com/OpenCoworkAI/open-cowork/blob/6f0c04741386b8600aa977f14ac0679d2203bd1b/src/renderer/components/PermissionDialog.tsx)
- [Open issue #305](https://github.com/OpenCoworkAI/open-cowork/issues/305)
- [Open issue #302](https://github.com/OpenCoworkAI/open-cowork/issues/302)
- [Open PR #306](https://github.com/OpenCoworkAI/open-cowork/pull/306)
- [Open PR #307](https://github.com/OpenCoworkAI/open-cowork/pull/307)
