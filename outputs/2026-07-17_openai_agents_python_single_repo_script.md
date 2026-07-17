# openai/openai-agents-python：把长期 Agent 工作流拆成可控的编排、护栏和运行状态

[主持人]
今天只讲一个仓库：`openai/openai-agents-python`。它不是一个普通聊天示例库，而是 OpenAI 的 Python Agent 编排 SDK。本次检查固定在 `965335aba6f6c71500e0b8cdb4e9e495f5801d4d` 这个提交，许可证是 MIT，包元数据里的版本是 `0.18.3`。它值得听，是因为我们的 GitHub 研究播客、Codex Skills、Feishu 自动化和 AI 视频流程都在遇到同一个问题：长流程任务怎么拆分、怎么限制副作用、怎么验证、怎么在失败后恢复。

[分析员]
这个仓库的核心抽象是 `Agent` 和 `Runner`。Agent 配置 instructions、tools、handoffs、guardrails、MCP server、模型和结构化输出；Runner 负责运行循环。文档里描述得很明确：Runner 会调用当前 Agent 的模型，如果产生 final output 就结束；如果发生 handoff，就切换到下一个 Agent；如果产生 tool calls，就执行工具、追加结果，再继续下一轮；超过 `max_turns` 会抛出异常。

它的架构入口也比较清楚。`src/agents/run.py` 是 Runner 主入口，`src/agents/tool.py` 处理 function tools、hosted tools、computer、apply patch、local shell、审批、超时和错误格式；`src/agents/guardrail.py` 定义输入和输出 guardrail；`src/agents/mcp/server.py` 处理 stdio、SSE、streamable HTTP 的 MCP 连接，还包括 approval policy、tool filter 和 HTTP client 配置。文档还把多 Agent 编排分成两种常见模式：manager 模式，也就是 `Agent.as_tool()`，由一个主控 Agent 调专家；handoff 模式，则让专业 Agent 接管下一段对话。

[主持人]
那它对近期项目具体能帮哪个问题？不要泛泛讲“能做 Agent”，我更关心 GitHub 研究播客和自动化工作流怎么受益。

[分析员]
最直接帮助的是多阶段自动化的控制面。现在每日 GitHub 研究播客要做选题、取证、报告、脚本、MiMo TTS、验证、索引、扫描、提交和推送。这个流程如果全靠一个长 prompt 记住所有规则，很容易在 TTS 失败、索引缺失、私有路径泄露或重复选题时出错。

从这个仓库可以复用四个设计。第一，用 manager 模式让一个主控流程拥有最终产物，只把“报告验证”“音频生成”“发布前扫描”这类边界清晰的动作暴露成工具。第二，只有在专家应该接管时才用 handoff，避免 Agent 之间互相转交导致责任不清。第三，用 blocking input guardrail 或 tool guardrail 在工具执行前挡住秘密、私有路径和外部发布动作；报告里特别提醒，Agent 级 input guardrail 只覆盖链路第一个 Agent，output guardrail 只覆盖最终输出，中间工具需要 tool guardrail。第四，用 session 和 tracing 记录每次自动化运行的状态和失败原因，但对含私密内容的任务要关闭敏感 trace 或先脱敏。

最小试验不是迁移整个播客项目，而是在一个不含私密数据的本地副本里写一个小 runner：manager agent 只能调用三个本地 function tools，分别是检查今天 bundle、验证报告、生成待办摘要；工具输入加 secret 和 path guardrail；`max_turns` 设小；只记录不含敏感内容的 tracing metadata。这个试验能回答一个实际问题：Agent SDK 是否能让长期自动化比长 prompt 更稳定。

[主持人]
它有什么不适合直接搬的地方？

[分析员]
第一，不要把现有 MiMo TTS 管线重写成 realtime 或 voice agent。仓库确实有 voice 和 realtime 能力，但今天的项目已经有明确的音频生成与验证命令，重写会增加风险。第二，不要默认启用远程沙箱。我们的 Codex 环境已经有文件、权限和验证约束，先学它的 `SandboxAgent` 思路，不急着替换运行时。第三，tracing 很适合调试，但可能记录模型输入和工具输出；Feishu、客户资料和本地私有路径必须做脱敏或关闭敏感数据。第四，这个仓库还在快速迭代，`v0.18.3` 就是本次运行当天发布的版本，公开 issue 仍然涉及 session history、sandbox provider、eager tool dispatch、FunctionTool 底层访问和 tracing 行为。

所以结论是：**Use now / 现在就小范围使用**。用它做一个低风险的本地编排试验，学习 manager vs handoff、blocking guardrails、tool-level checks、session/tracing 和 MCP approval；但不要把整个播客、Feishu 或视频生产管线一次性迁移过去。
