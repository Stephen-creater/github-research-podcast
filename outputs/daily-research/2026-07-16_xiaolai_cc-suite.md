# xiaolai/cc-suite：让 Claude、Codex 和 Antigravity 共用一套项目说明

- 仓库：[xiaolai/cc-suite](https://github.com/xiaolai/cc-suite)
- 本次检查版本：[`fbcf751`](https://github.com/xiaolai/cc-suite/commit/fbcf751edac4001c49678253d6be7a109d473254)
- 检查日期：2026-07-16
- 许可证：ISC
- 验证方式：只读检查 README、插件清单、桥接脚本、Runner、Hooks 和测试目录；没有安装或执行第三方代码

## 一句话说明

`cc-suite` 是一套多编程 Agent 的“翻译层和接线板”：它让 Claude Code、Codex CLI 和 Antigravity 在同一个项目中尽量共用 `AGENTS.md`、Skills、Hooks 与 MCP 配置，并允许这些工具把审核、规划、实现或调试任务相互委派。

## 解决什么问题

同一个项目同时使用 Claude Code 和 Codex 后，最容易出现的不是代码冲突，而是规则冲突：Claude 读取 `CLAUDE.md`，Codex 读取 `AGENTS.md`；Claude 的项目 Skills 默认放在 `.claude/skills/`，Codex 和 Antigravity 使用 `.agents/skills/`；Claude 的 MCP 配置和 Codex 的 TOML 配置又是两套格式。人工维护几份近似文件，短期能工作，长期一定会漂移。

`cc-suite` 面向已经同时使用多种命令行 Agent 的开发者。它把 `AGENTS.md` 定为共享说明的源头，让 `CLAUDE.md` 只保留 `@AGENTS.md` 导入；用符号链接共享 Skills；把 Claude 侧可兼容的 Hooks 和 MCP Server 转换给 Codex 与 Antigravity；再通过 MCP Server 让 Claude 调 Codex、Codex 调 Claude。它不是新的模型，也不是独立 IDE，而是现有工具之间的项目级协调层。

## 安装和使用

作者推荐通过 Claude Code 插件市场安装：

```bash
claude plugin marketplace add xiaolai/claude-plugin-marketplace
claude plugin install cc-suite@xiaolai --scope project
```

安装后运行：

```text
/cc-suite:init
```

初始化会建立说明文件桥接、Skills 共享、MCP 注册和项目配置。完整双向委派还要求本机已有 Codex CLI；Codex 调 Claude 使用运行时下载的 `claude-octopus`；使用 Google 路径时还需要 `agy`。Codex 项目必须被标记为 trusted，插件 Hooks 还需要启用 `plugin_hooks` 功能。

对我们更稳妥的最小试验不是一次开启所有功能，而是在一个低风险测试仓库中先执行三步：把共享规则收敛到 `AGENTS.md`；验证 `CLAUDE.md` 导入；验证 `.agents/skills` 和 `.claude/skills` 是否指向同一组 Skills。MCP 双向委派和会话读取应放到第二阶段。

## 架构和重要入口

它的核心不是一个常驻服务，而是一组命令、转换脚本和两个委派 Runner。

- `commands/`：初始化、状态检查、修复、桥接 Skills/Hooks/MCP，以及审核、实现、调试和验证等命令入口。
- `scripts/bridge_skills.sh`：把插件 Skills 暴露到 `.claude/skills/cc-suite/`，再建立 `.agents/skills -> ../.claude/skills/` 符号链接。
- `scripts/bridge_hooks.py`：把两边语义兼容的 Hook 事件转换到 Codex 配置，而不是假设所有 Hook 都能照搬。
- `scripts/bridge_mcp.sh`：把 `.mcp.json` 的项目服务器转换到 `.codex/config.toml` 与 `.agents/mcp_config.json`，并通过标记区块避免覆盖用户手写配置。
- `scripts/codex-runner.mjs`：Claude 调用 Codex 时负责进程、JSONL 事件、超时、后台任务和结果追踪。
- `scripts/agy-runner.mjs`：为输出能力更弱的 `agy` 补上超时、后台任务与会话恢复；无法可靠识别并发会话时宁可不记录 ID。
- `scripts/mcp_claude.sh`：把 `claude-octopus` 注册为 Codex MCP Server，并固定依赖版本，减少每次运行拿到不同版本的风险。
- `hooks/hooks.json`：管理会话生命周期和可选的停止前复核门槛。
- `tests/`：覆盖命令、进程、状态、工作区与任务控制等关键逻辑。

双向委派的逻辑可以简化为：Claude 通过 `codex mcp-server` 把任务交给 Codex；Codex 通过 `claude-octopus` 把任务交给 Claude。二者复用各自 CLI 已有的登录，不额外保存模型密钥。

## 值得借鉴的设计

### 1. 共享意图，保留平台差异

它没有强行把所有文件做成完全相同。共享意图放进 `AGENTS.md`，但 Claude Rules、Codex Rules 和 Subagents 因语义或安全字段不同而明确不桥接。这个判断很重要：真正可持续的跨平台方案不是把一切复制，而是只共享语义稳定的部分。

### 2. 生成配置必须带来源标记

桥接脚本只修改自己带标记的区块，遇到用户手动维护的同名配置会拒绝覆盖。我们以后生成飞书、视频或 Agent 配置，也应该给机器生成部分加 provenance 标记，更新时只重写自己拥有的范围。

### 3. 重复运行要安全

初始化和桥接脚本强调幂等：已有 `AGENTS.md` 不覆盖，真实目录不替换成符号链接，手写 MCP 配置不抢占。自动化最怕第二次运行比第一次更危险，这种“可重复运行”应成为我们所有长期任务的默认验收项。

### 4. 委派结果必须可追踪

Runner 不只是调用另一条 CLI，还记录任务 ID、日志、超时、后台状态和继续执行入口。多 Agent 真正困难的不是“能不能叫另一个模型”，而是出了问题后能否知道谁做了什么、做到哪一步、结果是否回来。

### 5. 不确定时宁可缺失，不要错误绑定

`agy` 没有机器可读输出，也不直接返回会话 ID。并发结束时若无法唯一判断新会话，Runner 选择不写 ID，而不是猜一个。这种保守策略适合我们的业务自动化：缺数据可以重试，错误关联可能污染后续全部决策。

## 对近期项目的直接帮助

它最直接帮助的是我们正在增长的 Codex Skills、长期自动化、GitHub 研究播客和 AI 视频工作流。现在不同工具都可能读取项目说明，如果规则分散，最容易发生“Codex 知道但 Claude 不知道”或“旧 Hook 仍在执行”的情况。

可复用的不是整套插件，而是三块架构：以 `AGENTS.md` 作为共享意图源；Skills 只维护一份并通过明确桥接暴露给不同工具；所有生成配置使用带来源标记的受控区块。对 GitHub 研究播客，这能让“选题、报告、脚本、音频、验证”的完成定义在 Claude 和 Codex 中保持一致。对视频生产，它能统一素材路径、角色职责和验证门槛。对飞书自动化，它能减少多个 Agent 对同一业务字段的不同解释。

最小试验是在 `github-research-podcast` 这样的低风险项目副本中，只验证说明文件和 Skills 两层桥接：运行前保存状态，运行后检查 `AGENTS.md`、`CLAUDE.md` 与 Skills 链接，并让 Claude、Codex 分别复述同一个完成标准。暂时不要开启会话历史读取、停止前自动复核或跨模型自动实现。

不适合照搬的部分是“所有任务都相互委派”。我们的日常工作很多涉及飞书内容、私有路径和客户资料，增加一个模型就增加一次信息暴露和成本。只有当第二个模型提供明确互补价值，例如独立代码审核或故障定位，才值得委派。

## 局限和风险

1. 项目很新，创建于 2026-05-18，本次检查时只有 15 Stars、3 Forks，没有正式 GitHub Release；插件清单版本为 `0.9.0`，仍应视为快速演进阶段。
2. 主要由 Shell、JavaScript 和 Python 脚本组合，符号链接与命令行工具依赖使它更适合 macOS/Linux；跨平台行为需要额外验证。
3. 双向委派会放大成本、延迟和责任边界问题。Agent A 调 Agent B，再由 B 调回 A，若没有任务深度限制，容易形成复杂循环。
4. Codex 读取 Claude 会话记录是强能力也是隐私风险。仓库默认按当前项目限制，但 `all_projects: true` 会扩大到机器上的全部项目；不应在含敏感会话的环境随意启用。
5. MCP 配置可能包含凭据或本机路径。项目选择把 Antigravity 生成配置默认忽略是合理的，但每次同步仍需秘密扫描。
6. `claude-octopus` 通过 `npx -y` 在运行时获取，虽有版本固定措施，首次运行仍涉及供应链下载和网络可用性。
7. `AGENTS.md` 作为唯一来源并不适合所有内容。Claude 与 Codex 的专属规则仍应留在各自边界，不能为了统一而丢掉平台能力。

## 最终建议

结论选择：**现在就小范围使用（Use now）**，但只试“共享说明 + 共享 Skills”，暂不启用完整双向委派。

它对我们最有价值的不是让三个 Agent 互相调用，而是建立一套不漂移的项目控制面。先在一个无敏感数据的测试副本中验证幂等性、路径和规则一致性；通过后再决定是否把 MCP 同步引入 GitHub 研究播客或视频生产项目。会话历史读取和自动实现保留为显式开启功能。

## 主要来源

- [README 与能力边界](https://github.com/xiaolai/cc-suite/blob/fbcf751edac4001c49678253d6be7a109d473254/README.md)
- [插件清单](https://github.com/xiaolai/cc-suite/blob/fbcf751edac4001c49678253d6be7a109d473254/.claude-plugin/plugin.json)
- [Skills 桥接脚本](https://github.com/xiaolai/cc-suite/blob/fbcf751edac4001c49678253d6be7a109d473254/scripts/bridge_skills.sh)
- [MCP 桥接脚本](https://github.com/xiaolai/cc-suite/blob/fbcf751edac4001c49678253d6be7a109d473254/scripts/bridge_mcp.sh)
- [Codex Runner](https://github.com/xiaolai/cc-suite/blob/fbcf751edac4001c49678253d6be7a109d473254/scripts/codex-runner.mjs)
- [Antigravity Runner](https://github.com/xiaolai/cc-suite/blob/fbcf751edac4001c49678253d6be7a109d473254/scripts/agy-runner.mjs)
- [Claude MCP 注册脚本](https://github.com/xiaolai/cc-suite/blob/fbcf751edac4001c49678253d6be7a109d473254/scripts/mcp_claude.sh)
- [测试目录](https://github.com/xiaolai/cc-suite/tree/fbcf751edac4001c49678253d6be7a109d473254/tests)
