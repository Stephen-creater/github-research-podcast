# openai/openai-agents-python：把长期 Agent 工作流拆成可控的编排、护栏和运行状态

- Repository: [openai/openai-agents-python](https://github.com/openai/openai-agents-python)
- Revision: [`965335a`](https://github.com/openai/openai-agents-python/commit/965335aba6f6c71500e0b8cdb4e9e495f5801d4d)
- Date: 2026-07-17
- License: MIT
- Verification: 只读检查 README、许可证、`pyproject.toml`、Agent/Handoff/Guardrail/Runner/MCP 文档与源码、最新 release 和公开 issue；没有安装或执行第三方代码。浅克隆 checkout 失败，但 `git show HEAD:<file>` 可读取固定提交内容。

## One-sentence explanation

`openai-agents-python` 是 OpenAI 的 Python Agent 编排 SDK：它把 Agent 定义、工具调用、MCP、handoff、guardrail、session、tracing、sandbox agent 和 realtime/voice 能力放进同一套运行循环，适合把“长流程自动化”做成可观测、可恢复、可限制的工程系统。

## Problem and users

近期项目里最常见的问题不是“能不能调用一个模型”，而是多步任务如何不失控：GitHub 研究播客要在选题、取证、报告、脚本、TTS、验证、提交之间保持状态；Codex Skills 和本地自动化要知道何时需要人批准、何时可以继续；AI 视频和 Feishu 工作流又经常涉及私有上下文、外部工具和重复运行。

这个仓库面向的用户是需要构建生产型 Agent 工作流的开发者，而不是只想写一次聊天脚本的人。它的核心抽象是 `Agent` 与 `Runner`：Agent 配置 instructions、tools、guardrails、handoffs、MCP server 和 output type；Runner 负责多轮循环、工具调用、handoff、session、streaming、tracing 与错误边界。

## Setup and minimal use

README 要求 Python 3.10 或更新版本，包名是 `openai-agents`，`pyproject.toml` 中当前版本为 `0.18.3`。基础安装是：

```bash
pip install openai-agents
```

可选能力按依赖组拆开，例如 `voice`、`redis`、`sqlalchemy`、`encrypt`、`litellm`、`any-llm`、`docker`、`e2b`、`modal`、`runloop` 和 `temporal`。这说明仓库没有把所有运行环境硬塞进默认安装，而是把会话存储、模型提供商、沙箱和语音能力作为明确选项。

最小使用可以只创建一个文本 Agent 并用 `Runner.run()`、`Runner.run_sync()` 或 `Runner.run_streamed()` 执行。README 还给出 `SandboxAgent` 示例：当任务需要读文件、跑命令、打补丁或保留工作区状态时，可以用 manifest 定义仓库输入，再通过 sandbox run config 执行。

## Architecture and entrypoints

架构上，它不是一个黑盒平台，而是一组可组合的 SDK 模块：

- `src/agents/agent.py`：定义 Agent 的 instructions、tools、handoffs、guardrails、model、output type、MCP servers 等配置面。
- `src/agents/run.py`：`Runner` 的主入口。文档说明运行循环会调用模型，处理 final output、handoff 或 tool calls，并在超过 `max_turns` 时抛出异常。
- `src/agents/tool.py`：定义 function tools、hosted tools、computer/apply-patch/local shell 等工具相关类型，并支持工具输出、审批、超时和错误格式。
- `src/agents/guardrail.py`：输入、输出 guardrail 的数据结构与执行接口；guardrail 返回 tripwire 后可以中止运行。
- `src/agents/mcp/server.py`：支持 stdio、SSE、streamable HTTP 等 MCP server 连接，并包含 approval、tool filter 和 HTTP client 配置。
- `src/agents/memory/` 与 `src/agents/extensions/memory/`：处理 session、SQLite、Redis、SQLAlchemy、MongoDB、Dapr、加密等会话存储。
- `src/agents/tracing/`：为 Agent、task、turn、tool 等运行过程提供 tracing。
- `src/agents/sandbox/` 与 `src/agents/extensions/experimental/codex/`：把长时程文件/命令工作流和 Codex 风格任务接入 SDK。

最新 release `v0.18.3` 发布于 2026-07-17，变更包括 task/turn tracing span 可配置、realtime usage tracking、conversation session 初始化串行化、handoff history wrapper 保留、concurrent run provider 隔离、E2B workspace root 修复和 streamed session input retry 保留。这些都说明近期维护重点集中在可观测性、并发、session 和 handoff 可靠性。

## Reusable design ideas

第一，编排策略分成两类：`Agent.as_tool()` 的 manager 模式，和 handoff 的交接模式。前者适合一个主控 Agent 收集多个专家结果并统一输出；后者适合让专业 Agent 接管下一段对话。这个区分可以直接迁移到我们的自动化：选题、验证、音频、发布不必都由同一个角色完成，但最终责任必须明确。

第二，guardrail 明确说明了边界：输入 guardrail 默认可与 Agent 并行以降低延迟，也可设为 blocking 以避免成本和副作用；输出 guardrail 只在最终输出后运行；工具 guardrail 才能覆盖每次 function-tool 调用。这个细节对含私密上下文的 Feishu、视频和 GitHub 自动化很关键，因为只在入口检查一次不能防止工具输出泄露。

第三，Runner 把 `max_turns`、session、previous response、streaming、handoff input filter、tracing metadata、tool execution concurrency 和 tool error formatter 做成运行级配置。相比把规则写死在 prompt 里，这些开关更适合作为长期自动化的工程护栏。

第四，MCP 支持不是“把所有工具暴露给模型”这么简单。源码里有 approval policy、tool filter、transport 超时、streamable HTTP client 与错误处理，这些都是把真实工具接进 Agent 时必须有的控制面。

第五，仓库提供大量 `examples/agent_patterns`，包括 parallelization、routing、human-in-the-loop、input/output guardrails、LLM-as-judge 和 deterministic flow。它适合作为架构参考，而不只是依赖包。

## Help for recent projects

它最直接帮助的是当前的 GitHub 研究播客自动化、Codex Skills 体系和 Feishu/AI 视频工作流的“多阶段任务控制”问题：这些任务都需要在多个步骤之间传递状态、限制工具副作用、保留验证证据，并在缺少授权或 TTS 失败时可靠恢复。

可复用的不是整套 SDK 迁移，而是四个方法：用 manager 模式让一个主控流程拥有最终产物；用 handoff 或 agent-as-tool 只委派边界清晰的子任务；用 blocking input/tool guardrails 把秘密、私有路径和外部发布动作挡在执行前；用 session/tracing 给每次自动化运行留下可追踪的状态和失败原因。对 GitHub 研究播客，最适合复用的是“报告验证、脚本生成、音频生成、发布前扫描”各自作为有输入输出契约的工具或专家，而不是继续让一个长 prompt 背完整流程。

最小有用试验是在一个不含私密数据的本地副本里做一个小 runner：定义一个 manager agent，只允许调用三个本地 function tools：检查今天 bundle、验证报告、生成待办摘要；给工具输入加 secret/path guardrail；把 `max_turns` 设小；打开 tracing metadata，但不上传敏感内容。通过后再考虑把脚本生成或报告评审拆成 agent-as-tool。

不适合照搬的是 realtime/voice、完整沙箱托管和多模型 provider 抽象。当前播客项目已经有明确的 MiMo TTS 管线，音频生成不应重写成 realtime agent；涉及 Feishu 和客户资料的工作也不应默认启用远程沙箱或扩大 trace 内容。SDK 的 `SandboxAgent` 很有启发，但在本机 Codex 已经提供沙箱、权限和文件上下文时，先复用模式，不急于替换运行时。

## Limitations and risks

1. 仓库仍在快速迭代。当前版本是 `0.18.3`，latest release 就在本次运行当天，公开 issue 仍包括 session history retrieval、sandbox provider、eager tool dispatch、FunctionTool 底层函数访问和 tracing 行为等问题。
2. 默认把复杂工作交给模型决策会带来成本、延迟和可重复性问题。文档也建议代码编排和 LLM 编排可以混用；对我们的自动化，关键路径应更多由代码控制。
3. Guardrail 的执行点容易被误解。Agent 级 input guardrail 只覆盖链路第一个 Agent，output guardrail 只覆盖最终输出；如果中间工具可能泄露内容，必须使用 tool guardrail 或工具内部检查。
4. Tracing 对调试非常有价值，但 trace 可能包含模型输入、工具参数和输出。含私密资料的任务必须关闭敏感数据或做脱敏。
5. MCP、local shell、apply patch、computer 和 sandbox 能力会显著扩大副作用边界。引入时必须配合 approval、tool filter、最小权限和发布前扫描。
6. 依赖面很广。虽然可选依赖拆得清楚，但一旦启用 Redis、SQLAlchemy、Docker、E2B、Runloop、Temporal 或 realtime，就会引入额外服务和运维复杂度。

## Recommendation

结论选择：**Use now / 现在就小范围使用**，但只用于一个本地最小试验：把“每日 bundle 检查、报告验证、发布前扫描”抽象成工具和 guardrail，验证 Agent 编排能不能减少长流程 prompt 的脆弱性。

短期不要把现有播客管线整体迁移到 SDK，也不要启用远程沙箱或把 Feishu 私密内容放进 tracing。正确路线是先学习它的工程边界：manager vs handoff、blocking guardrails、tool-level checks、session/tracing 和 MCP approval；稳定后再把某个低风险自动化步骤替换成 SDK runner。

## Primary sources

- [README](https://github.com/openai/openai-agents-python/blob/965335aba6f6c71500e0b8cdb4e9e495f5801d4d/README.md)
- [License](https://github.com/openai/openai-agents-python/blob/965335aba6f6c71500e0b8cdb4e9e495f5801d4d/LICENSE)
- [Package metadata](https://github.com/openai/openai-agents-python/blob/965335aba6f6c71500e0b8cdb4e9e495f5801d4d/pyproject.toml)
- [Agent docs](https://github.com/openai/openai-agents-python/blob/965335aba6f6c71500e0b8cdb4e9e495f5801d4d/docs/agents.md)
- [Agent orchestration docs](https://github.com/openai/openai-agents-python/blob/965335aba6f6c71500e0b8cdb4e9e495f5801d4d/docs/multi_agent.md)
- [Handoff docs](https://github.com/openai/openai-agents-python/blob/965335aba6f6c71500e0b8cdb4e9e495f5801d4d/docs/handoffs.md)
- [Guardrail docs](https://github.com/openai/openai-agents-python/blob/965335aba6f6c71500e0b8cdb4e9e495f5801d4d/docs/guardrails.md)
- [Runner implementation](https://github.com/openai/openai-agents-python/blob/965335aba6f6c71500e0b8cdb4e9e495f5801d4d/src/agents/run.py)
- [Tool implementation](https://github.com/openai/openai-agents-python/blob/965335aba6f6c71500e0b8cdb4e9e495f5801d4d/src/agents/tool.py)
- [MCP server implementation](https://github.com/openai/openai-agents-python/blob/965335aba6f6c71500e0b8cdb4e9e495f5801d4d/src/agents/mcp/server.py)
- [Latest release v0.18.3](https://github.com/openai/openai-agents-python/releases/tag/v0.18.3)
- [Open issue: session history retrieval](https://github.com/openai/openai-agents-python/issues/3738)
