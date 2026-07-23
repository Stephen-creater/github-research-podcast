# mastra-ai/mastra：把 agent 项目从脚本堆推进到可观察的工作流

[主持人]
今天只聊一个仓库，`mastra-ai/mastra`。它不是一个单点工具，而是一个 TypeScript AI 应用框架：把 agents、graph workflows、human-in-the-loop、memory、RAG、MCP、evals、observability 和 Studio 调试放在同一套工程层里。

这期和最近项目的关系很直接。现在很多工作已经不是“怎么调用一次 LLM”，而是怎么把 Codex 自动化、Feishu/Lark 操作、AI 视频 QA、GitHub 日研播客、以及 AI 产品化探索做成可恢复、可验证、可观察的系统。Mastra 的价值就在于，它提供了一套可以研究的产品化结构。

先给结论：**Study only / 仅研究并做一个小型本地试验**。不要立刻迁移所有工作流，也不要把生产 Feishu、邮件、浏览器或 TTS 凭证接进去。最合适的动作，是拿一个 public-only 的现有自动化，做一个本地 proof of concept，验证 workflow state、suspend/resume、scorer 和 trace 到底能不能减少运维风险。

[分析员]
我们检查的 pinned commit 是 `c1a66a27b8679abaa01ea57a9260c01d1c6f93de`。GitHub API 显示主分支在 2026 年 7 月 23 日仍有 push，仓库主题包括 agents、AI、evals、MCP、Next.js、Node、React、TTS、TypeScript 和 workflows。README 说 Mastra 是一个用现代 TypeScript stack 构建 AI-powered applications and agents 的框架，可以和 React、Next.js、Node 集成，也可以作为 standalone server 部署。

报告里还做了去重。`larksuite/cli` 和 `larksuite/lark-openapi-mcp` 已经在早期单仓 episode 覆盖过，`browserbase/stagehand` 已经覆盖过浏览器自动化，昨天刚研究了 Remotion，不应该今天再重复视频渲染。Mastra 的新意在于，它横跨 agent runtime、明确 workflow、memory、MCP、evals 和 observability，更适合回答“怎样把 agent 工作变成可产品化系统”这个问题。

架构上，它是一个大型 TypeScript monorepo。`@mastra/core` 是核心运行时；`@mastra/core/agent` 暴露 Agent、消息转换、signals、schedules、subagent 和 delegation 相关类型；`@mastra/core/workflows` 暴露 `createWorkflow`、`createStep`、execution engine、scheduler 和 state reader；memory 相关模块处理 message history、working memory、semantic recall、observational memory 和 processors；`@mastra/mcp` 支持 MCPClient 和 MCPServer；`@mastra/evals` 做 scorers；`@mastra/observability` 做 traces、logs、metrics、feedback 和敏感信息过滤。

[主持人]
这里最值得复用的设计，是把 open-ended agent 和 explicit workflow 分开。Mastra 文档里说，步骤未知、需要模型自己决定怎么调用工具时，用 agent；步骤已知、需要明确数据流和执行顺序时，用 workflow。

这对我们的 GitHub 日研播客特别有用。这个自动化并不是每一步都需要 LLM 决策。它有固定 gate：pull、检查今日 quota、候选去重、主源研究、写报告、生成脚本、TTS、验证音频、更新索引、扫密钥、commit、push。真正适合 agent 的部分是候选判断、主源理解和报告写作；适合 workflow 的部分是状态机和验收门槛。

[分析员]
第二个可复用点是 suspend/resume。Mastra 的 workflow 文档说明，工作流可以在任一步暂停，把当前状态保存成 snapshot，之后用 typed resumeData 从指定 step 继续。这对真实自动化很实用。比如 TTS key 不存在、Feishu 登录需要用户接管、发布前需要人工确认、或者长任务中途进程重启，这些都不应该让整条链路从头开始，也不应该伪装成成功。

第三个可复用点是 memory 分层。Mastra 的 memory docs 把 message history、observational memory、working memory、semantic recall、multi-user threads、memory processors 分开。这个框架对 AnySpecs 和上下文管理工作很有启发：有些事实应该是长期偏好，有些是项目状态，有些是可检索历史，有些应该压缩成观察，有些根本不该进 prompt。

第四个是 evals 和 observability。Mastra 把 scorers 描述成给非确定性 AI 输出做自动化评估的方法，可以进入 CI，也可以 live scoring。Observability 则覆盖 agent run、workflow step、tool call、model interaction、trace、log、metric、cost 和 feedback。对 AI 视频生产来说，这可以变成“脚本是否覆盖卖点、字幕是否对齐、QA 是否通过”的 scorer；对 Feishu 自动化来说，可以变成“权限边界是否正确、失败停在哪一步”的 trace。

[主持人]
那最小试验应该怎么做？不要先谈平台迁移。就拿一个已经存在的 public-only 自动化，比如 GitHub 研究播客，抽象成一个 Mastra workflow。步骤包括候选评分、主源采集、报告草稿、报告 validator、脚本生成、音频 verify、发布 gate。先用公开数据和本地文件，不连接生产 Feishu、不连接邮件、不连接私密浏览器状态。

再加一个很小的 scorer：检查报告里的 `Help for recent projects` 是否回答了四个问题，分别是帮助哪个近期项目问题、能复用什么、最小试验是什么、哪些不适合照搬。再加一个 trace 或 structured log，让我们知道每次 run 是停在候选、报告、TTS、验证还是发布。

[分析员]
限制也要说清楚。第一，Mastra 很宽，采用它意味着引入 Node 和 TypeScript 项目结构、包管理、storage、model provider、observability storage 和部署选择。对一个简单 shell 脚本来说，这可能过重。

第二，license 是混合的。README 和 `LICENSE.md` 说，大部分代码是 Apache-2.0，但任何名为 `ee/` 的目录走 Mastra Enterprise License。GitHub API 对仓库 license 给的是 `NOASSERTION`。所以不能把整个仓库当成纯 Apache-2.0 来复制。

第三，它变化很快。最新 release `@mastra/core@1.51.0` 提到了 durable-agent crash recovery、scoped AgentController sessions、workspace/sandbox providers、Mastra Code SDK、MCP server streaming 和 notifications、scorer、dataset identity、provider-tool-call observability spans，以及很多 durable-agent 修复。维护活跃是好事，但也说明 trial 要 pin version，先验证核心模式，不要一下深度绑定。

[主持人]
所以今天的建议不是“马上全面采用”，而是“把它当成 agent 产品工程参考”。最有价值的不是复制代码，而是复用结构：agent 负责开放推理，workflow 负责确定性 gate，storage 负责暂停和恢复，MCP 负责工具边界，memory 负责上下文层次，scorer 负责质量门槛，observability 负责知道系统为什么失败。

[分析员]
结论和报告一致：**Study only / 仅研究并做一个小型本地试验**。用 Mastra 做一个围绕现有公开自动化的本地 proof of concept，验证 workflow state、suspend/resume、scoring 和 traceability 是否真的降低风险。在这个结果成立之前，不迁移生产 Feishu、AI 视频或播客工作流，不接入真实私密凭证，也不为了架构好看替换已经稳定工作的简单脚本。
