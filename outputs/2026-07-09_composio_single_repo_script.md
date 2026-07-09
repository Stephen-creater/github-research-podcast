# Composio 单仓播客脚本

[主持人]
今天这一期只讲 `ComposioHQ/composio`。它的定位是给 agent 提供可进化的 skills 和外部工具集成，让 OpenAI Agents、Anthropic、LangChain、LangGraph、LlamaIndex、CrewAI、AutoGen、Google Gemini 等框架能连接真实应用。对你的 AI FDE、Feishu Daily、GitHub 播客和求职自动化来说，Composio 代表的是“agent 如何安全地调用外部世界”，不是只在聊天窗口里生成文本。

[分析员]
README 里最基础的用法很直接。TypeScript 安装 `npm install @composio/core`，Python 安装 `pip install composio`。然后初始化 `Composio`，为某个 `userId` 获取工具，比如 `composio.tools.get(userId, { toolkits: ['HACKERNEWS'] })`，再把 tools 交给 OpenAI Agents 的 `Agent`。Python 版本类似，用 `Composio(provider=OpenAIAgentsProvider())`，再把 tools 放进 `Agent` 和 `Runner.run()`。它强调的是工具获取、用户身份和 agent framework 适配。

[主持人]
Provider 支持很广。TypeScript 侧有 OpenAI、OpenAI Agents、Anthropic、LangChain、LangGraph、LlamaIndex、Vercel AI SDK、Gemini、Mastra、Cloudflare Workers AI；Python 侧有 OpenAI、OpenAI Agents、Anthropic、LangChain、LangGraph、LlamaIndex、Gemini、Google ADK、CrewAI、AutoGen 等。这个广度说明 Composio 不想绑定单一模型公司，而是做 agent 工具层。对你来说，这和 Feishu/Lark MCP、Codex tools、Claude Code plugins 属于同一个大方向。

[分析员]
看目录结构，`ts` 是 TypeScript SDK，包含 docs、providers、tool-router、mcp、triggers 等；`python` 是 Python SDK，包含 `composio/sdk.py`、`client`、`core`、`utils`、provider packages、examples 和大量 tests；`docs` 是文档站；`.gitleaks.toml`、`.gitleaksignore`、`sensitive_file_upload_paths.py`、`upload_dir_allowlist.py` 这类文件说明它很关注工具调用时的敏感文件风险。仓库也有 `.codex`、`AGENTS.md`、`CLAUDE.md`，说明它本身也面向 coding agent 协作。

[主持人]
它还有一个重要概念叫 Rube。README 说 Rube 是基于 Composio 的 MCP server，可以把 AI 工具连接到 Gmail、Slack、GitHub、Notion 等五百多个应用。安装一次、认证一次，不同 MCP 客户端就可以执行真实动作，比如发邮件或创建任务。这个和你的场景非常贴近：你不只是让 agent 总结信息，还想让它在合适边界内写 Feishu、查 Gmail、整理 GitHub、生成任务。

[分析员]
对你的第一个具体用法，是把它作为“agent 工具网关”的参考。你现在的工具面很分散：Feishu/Lark CLI、Gmail、GitHub、浏览器、文件系统、TTS、Keychain。Composio 的结构提醒我们，一个成熟 agent 系统要解决三件事：用户身份如何映射到外部账号，工具 schema 如何交给不同 agent framework，敏感操作如何授权、限制和审计。没有这些，只是把 API key 塞进脚本，很快会失控。

[主持人]
第二个用法，是 AI FDE demo。企业客户不会只关心模型能不能回答问题，他们会问：能不能连接工单、CRM、文档、代码仓库、邮件和日历？能不能只允许某些动作？能不能记录谁让 agent 做了什么？Composio 的 SDK、provider、tool router、triggers 和 MCP 方向都可以作为 demo 参考。你可以用它讲“AI FDE 不是做一个聊天机器人，而是把业务工具变成可控 action surface”。

[分析员]
第三个用法，是 GitHub 播客和个人雷达。Composio 本身未必直接替代现有 pipeline，但它能启发你如何把候选源变成 toolkits。比如 GitHub 搜索、RSSHub、Firecrawl、Feishu Daily、Gmail 招聘邮件、Notion 或 Drive 文件，都可以抽象成工具。agent 先用工具找候选，再用 repo ingestion 读材料，最后用 TTS 生成音频。工具层和内容层分开后，系统更容易扩展。

[主持人]
设计上最值得学的是 provider abstraction。README 里同一个 Composio 工具可以接 OpenAI Agents、Anthropic、LangChain、LlamaIndex 等。对你来说，这个抽象很重要，因为你经常在 Codex、Claude、浏览器、Feishu CLI 之间切换。如果每个工具只为一个 agent 写死，维护成本会爆炸。更好的设计是把工具 schema、认证、执行、权限和审计集中起来，agent 只是不同前端。

[分析员]
安全边界也要认真看。Composio 连接的是 Gmail、Slack、GitHub、Notion 这类真实账号，风险比普通 RAG 高得多。仓库里的 sensitive file upload guard、allowlist、gitleaks 配置、webhook verification、auth configs、connected accounts tests，都是你应该关注的地方。对你的个人系统来说，最危险的不是模型答错一句话，而是 agent 带着权限执行了错误动作，或者把私密文件上传到了不该去的地方。

[主持人]
局限也要说。第一，Composio 偏平台和 SDK，接入前要确认它支持你真正需要的应用，尤其是 Feishu/Lark 生态。第二，很多外部集成依赖账号授权和云服务，隐私和成本要评估。第三，多 provider 支持会带来版本兼容和行为差异。第四，工具越多，agent 越需要规划和权限约束，否则会出现“能做很多事，但不知道该做哪件”的问题。第五，真实动作必须有 dry run、确认和日志。

[分析员]
读源码建议从 Python 和 TypeScript 两条线各挑重点。Python 先读 `python/composio/sdk.py`、`python/composio/client/types.py`、`python/composio/utils/openapi.py`、`python/composio/utils/sensitive_file_upload_paths.py`，再看 `python/examples/tool_router` 和 `python/providers/openai_agents`。TypeScript 先读 `ts/README.md`、`ts/docs/core-concepts.md`、`ts/docs/api/tools.md`、`ts/docs/api/tool-router.md`、`ts/docs/api/mcp.md`。最后看测试，尤其是 tool execution、webhook、auth configs、sensitive file upload。

[主持人]
如果今天做最小实验，我会选低风险工具，不碰邮箱发送和账号写操作。比如用 HackerNews 或 GitHub 只读工具，让 agent 查询某类项目，再输出候选 repo JSON。然后把结果交给现有播客流水线。这个实验能验证 Composio 的工具获取、provider 接入和结果结构，但不会引入高风险动作。等只读流程稳定后，再考虑 Feishu 写入或任务创建这种需要确认的动作。

[分析员]
它和 MCP 的关系也值得理解。Composio SDK 可以直接给某个 agent framework 提供 tools；Rube 则把这些能力包装成 MCP server，让不同客户端共享。你现有工作流已经大量接触 MCP 和 CLI，未来更可能需要“一个工具层，多种 agent 前端”。Composio 的 MCP 方向说明这个趋势很明确：工具不应该只属于一个聊天产品，而应该成为可授权、可审计、可复用的能力层。

[主持人]
这一期结论：Composio 是 agent productization 的工具集成参考。它让我们看到，真正可用的 agent 不只是会读上下文，还要会以正确身份、正确权限、正确 schema 调用外部应用，并留下审计痕迹。对你的 AI FDE 路线，它可以作为“业务工具连接层”的学习样板；对个人自动化，它提醒你先做只读、再做人类确认、最后才做写操作。

[分析员]
最后给一个实践原则：任何 agent 工具平台，都要先把动作分级。读取公开信息是低风险；读取私人账号是中风险；发送、删除、购买、授权、投递是高风险。Composio 这类平台的价值，是让高风险动作有身份、权限和日志，而不是让 agent 随便执行。你如果把这个原则带进 Feishu/Daily、Gmail、GitHub 和求职流程，系统会更可靠，也更适合作为 AI FDE 的展示案例。

[主持人]
再补一层产品判断。Composio 这类工具集成平台，本质上是在回答“agent 如何从建议者变成操作者”。建议者只需要读上下文和生成文本；操作者必须面对账号授权、动作确认、失败回滚、幂等性、审计日志和权限最小化。你如果做 AI FDE 方向，这个区别非常关键。客户不缺一个会说话的模型，缺的是能安全接入业务系统、并且知道什么时候必须停下来的执行层。

[分析员]
它对个人系统的启发也是一样。你可以先定义一个工具目录：只读 GitHub、只读网页、只读 Gmail、写入 Feishu 草稿、创建本地任务、生成播客音频。每个工具标清风险等级、需要的凭据、是否允许自动执行、是否必须人工确认。Composio 的 provider 和 toolkit 思路可以作为目录结构参考。这样后续接入新工具时，不是临时把 API 拼进去，而是纳入统一治理。

[主持人]
所以这一期最后的行动建议是：先用 Composio 学工具抽象和权限设计，不急着把所有账号都接进去。最值得复用的是它的 provider 层、tool router、MCP 方向、敏感文件保护和测试覆盖。等你要做对外 demo 时，再挑一个只读工具和一个低风险写入工具展示完整闭环。这样既能体现 agent 的执行力，也能体现你对风险边界的判断。
