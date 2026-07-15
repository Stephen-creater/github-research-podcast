# NLPM：把写给 AI 的说明书当成代码来检查

- 仓库：[xiaolai/nlpm](https://github.com/xiaolai/nlpm)
- 本次检查版本：[`62e63da`](https://github.com/xiaolai/nlpm/commit/62e63da2562dd8b99940903379a39fed202ba118)
- 检查日期：2026-07-15
- 许可证：ISC
- 本地验证：`python3 bin/nlpm-check .` 通过；`python3 -m unittest discover -s tests -v` 的 81 项测试全部通过

## 一句话说明

NLPM 可以理解成“AI 工作说明书的质检员”。普通代码有 ESLint、Ruff 和测试套件，NLPM 检查的则是 `AGENTS.md`、`CLAUDE.md`、Skills、Agents、Commands、Hooks 和插件清单等自然语言文件。它要解决的问题不是代码能不能运行，而是 AI 会不会因为说明含糊、文件漏登记、规则互相冲突或引用失效而悄悄做错事。

## 它解决什么问题

AI 项目越做越大，真正控制行为的往往不只是 Python 或 TypeScript，还包括大量 Markdown、YAML、JSON 和 TOML 配置。这些文件常见四类问题：

1. 文件存在，但没有登记进插件清单，安装后实际不可见。
2. 指令写得很像人话，却没有明确输入、输出、成功标准和失败处理。
3. 多个 Skill、Agent 和 Hook 使用不同名称描述同一件事，时间久了互相冲突。
4. 本机能用，但发布或换一台机器后失效，而且安装过程不一定报错。

NLPM 最有辨识度的能力是“清单和磁盘一致性检查”：把插件清单里声明的组件与仓库里真实存在的文件做对照，找出漏登记、路径错误和孤立组件。这个检查很机械，却正好覆盖了很多单文件检查器看不到的边界。

## 怎么安装和使用

对我们来说，最稳妥的起点不是先启用整套自动对外审计，而是使用它不依赖 Claude Code 的检查器：

```bash
curl -fsSL -o /usr/local/bin/nlpm-check \
  https://raw.githubusercontent.com/xiaolai/nlpm/main/bin/nlpm-check
chmod +x /usr/local/bin/nlpm-check
nlpm-check /path/to/project
```

它要求 Python 3.11 以上，没有第三方依赖，适合放在提交前检查或 GitHub Actions 中。完整的 `/nlpm:score`、`/nlpm:fix`、`/nlpm:test` 等交互命令主要作为 Claude Code 插件运行；Codex 侧目前更适合使用它的规则知识和独立检查器，而不是假设全部 Claude 编排命令都能原样运行。

官方入口：

- [README 与安装方式](https://github.com/xiaolai/nlpm#installation)
- [独立检查器](https://github.com/xiaolai/nlpm/blob/main/bin/nlpm-check)
- [插件作者指南](https://github.com/xiaolai/nlpm/blob/main/docs/for-authors.md)
- [GitHub Actions 模板](https://github.com/xiaolai/nlpm/blob/main/templates/workflows/nlpm-check.yml)

## 架构和重要入口

NLPM 实际上有两层。

第一层是面向单个项目的质量检查：

- `commands/`：8 个用户命令，负责发现、评分、检查、修复、趋势、测试、初始化和安全扫描。
- `agents/`：扫描、评分、一致性检查、模糊词检查、测试和安全扫描六类 Agent。
- `skills/nlpm/`：评分表、50 条规则、平台约定、安全模式和写作指南。
- `bin/nlpm-check`：不依赖 Claude Code 的确定性检查器，是最适合我们先接入的入口。
- `.nlpm-test/` 与 `tests/`：一边测试自然语言产物，一边测试 Python 检查器本身。

第二层是 `auditor/` 和 `.github/workflows/auditor-*.yml` 组成的外部审计流水线：发现仓库、审计、生成修复、跟踪 PR、收集维护者反馈、沉淀案例，再反过来更新自己的规则。它的 PR 跟踪任务当前每 4 小时运行一次，因此李笑来的贡献图会出现大量自动生成和合并的活动。

## 最值得借鉴的五个设计

### 1. 先做机械检查，再让模型判断

路径、清单、字段和引用可以由 Python 稳定判断；“描述是否含糊”“例子是否足够”才交给模型。这样便宜、容易测试，也减少模型一本正经乱判。

### 2. 用分层规则支持不同工具

它先定义通用底线，再分别覆盖 Claude Code、Codex 和 Antigravity 的目录与配置差异。我们以后管理跨 Codex、Claude、ChatCut 和飞书的 Skill，也应该采用“共同规则 + 平台差异”，而不是复制四套互相漂移的说明。

### 3. 自然语言工作流也要有测试

NLPM 提倡先写 `.nlpm-test` 规格，再写 Agent 或 Skill。这对我们的自动化很有价值：可以明确“什么输入应该触发”“必须输出哪些字段”“什么情况必须停止”，避免只凭肉眼觉得提示词不错。

### 4. 把外部反馈变成规则数据

它不只统计 PR 是否合并，还区分已合并、维护者另行修复、拒绝、CLA 阻塞等结果。好的规则不是作者自己宣布有效，而是要看真实使用者是否接受。这种反馈闭环可直接借鉴到我们的 GitHub 研究、视频生产和飞书自动化中。

### 5. 给自动化设置硬边界

项目里已经有安全阻断、CLA 检查、单仓库 PR 数量限制和人工门槛。虽然仍需谨慎，但这个思路是对的：Agent 的能力越强，越需要明确“哪些能自动做、哪些只能提出候选、哪些必须由人批准”。

## 对我们有什么直接帮助

### GitHub 每日研究

今天刚启用的每日研究任务本身就是自然语言程序。可以用 NLPM 的思路检查它是否写清楚了选题范围、输出目录、重复判断、来源要求、秘密扫描、提交归属和失败时不制造空提交。最重要的不是给提示词打一个漂亮分数，而是让任务长期运行后仍然不跑偏。

### Codex Skills 和长期自动化

我们已经有多套 Skills、`AGENTS.md`、定时任务和记忆规则。最先值得检查的是：Skill 名称和目录是否一致、说明是否准确触发、不同 Skill 是否重复、自动任务是否写清楚成功标准，以及换一个新任务后是否还能恢复上下文。

### 飞书和 AI 视频工作流

ChatCut、Seedance、批量视频和飞书多维表格之间有很多角色、输入输出与禁止事项。可借鉴 NLPM 的跨组件检查方式，验证“脚本 -> 视频帧 -> 视频”的字段和文件引用是否一致，并把创意生成与 FFmpeg 确定性后期的边界写成可检查规则。

### AI FDE 项目

给客户做自动化 Demo 时，业务 SOP 本身就是自然语言程序。若能展示“需求规则有版本、有测试、有审计记录”，会比只展示一个能聊天的 Agent 更接近可交付系统。

## 局限和风险

1. 完整评分仍有模型参与。仓库把评分描述成确定性的，但只要使用 LLM 做语义判断，结果就会受到模型版本和上下文影响；真正稳定的是 `bin/nlpm-check` 覆盖的机械部分。
2. Claude Code 支持最完整。Codex 目前能复用规则和独立检查器，但不能把所有斜杠命令与多 Agent 编排直接照搬。
3. 仓库变化很快。它在 2026-03-25 才创建，本次检查时没有正式 GitHub Release；README、规则数量和实际目录可能继续快速变化，接入时应该固定提交版本。
4. 自动对外贡献有社区风险。即使修复真实，短时间向多个仓库提交大量 PR 也可能被维护者视为噪声。我们不应该复制“批量对外提交”这一层。
5. 审计陌生仓库会接触不可信内容。提示注入、恶意脚本和依赖风险仍然存在，必须坚持只读检查、沙箱、最小权限和人工审批。

## 最终建议

结论是“现在就小范围使用，但不要整套照搬”。

第一阶段只做两件事：把 `nlpm-check` 或同类机械规则接到我们自己的 Skill/Agent 仓库；再用它的 50 条规则为三个核心工作流做一次人工体检。暂时不要自动给外部仓库提 PR，也不要为了分数大改所有提示词。等我们验证它确实能抓到真实问题，再考虑做适合 Codex 的轻量版本。

优先检查顺序：每日 GitHub 研究自动化、视频生产 Skills、飞书业务自动化。它们都是会长期运行、最容易因规则漂移造成实际损失的地方。

## 主要来源

- [NLPM README](https://github.com/xiaolai/nlpm/blob/62e63da2562dd8b99940903379a39fed202ba118/README.md)
- [生态检查缺口分析](https://github.com/xiaolai/nlpm/blob/62e63da2562dd8b99940903379a39fed202ba118/analysis/ecosystem-gap.md)
- [独立检查器源码](https://github.com/xiaolai/nlpm/blob/62e63da2562dd8b99940903379a39fed202ba118/bin/nlpm-check)
- [PR 状态追踪工作流](https://github.com/xiaolai/nlpm/blob/62e63da2562dd8b99940903379a39fed202ba118/.github/workflows/auditor-track.yml)
- [对外贡献工作流](https://github.com/xiaolai/nlpm/blob/62e63da2562dd8b99940903379a39fed202ba118/.github/workflows/auditor-contribute.yml)
- [测试目录](https://github.com/xiaolai/nlpm/tree/62e63da2562dd8b99940903379a39fed202ba118/tests)
