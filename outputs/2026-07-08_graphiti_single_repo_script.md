# Graphiti 单仓播客脚本

[主持人]
今天这一期只讲 getzep/graphiti。它的定位是为 AI agents 构建 temporal context graphs，也就是会随时间变化的上下文图谱。你可以把它理解为：普通 RAG 把文档切成块，问的时候找相似片段；Graphiti 更关心实体、关系、事实、来源和时间。谁和谁有什么关系，这个事实什么时候成立，什么时候被新信息替代，来自哪条原始 episode。对你现在的 Feishu Daily、招聘线索、项目复盘、播客选题和个人知识库来说，它回答的是“长期记忆怎样不变成一堆过期摘要”。

[分析员]
README 里先强调 context graph 的组成：Entities 是人、产品、政策、概念等节点；Facts 或 Relationships 是边，带有 temporal validity windows；Episodes 是原始数据流，是所有派生事实的来源；Custom Types 用 Pydantic 模型定义实体和边类型。这个模型非常适合你的真实场景。比如“杭州有赞岗位需要 AI FDE 能力”是一条事实，“AttendancePilot 适合作为面试 demo”也是一条事实，它们都应该有来源、时间和可能被替代的版本，而不是被塞进一个永久不变的总结里。

[主持人]
怎么跑？README 写了基本要求：Python 3.10 以上，图数据库可以是 Neo4j、FalkorDB、Amazon Neptune 等，默认需要 OpenAI API key 做 LLM 推理和 embedding，也支持 Gemini、Anthropic、Groq 等替代服务。仓库里有 `docker-compose.yml`、`.env.example`、`pyproject.toml`、`Makefile`，还有 `examples/quickstart`、`examples/langgraph-agent`、`examples/ecommerce`、`examples/podcast`。如果只是学习，优先看 quickstart 和 examples；如果要给 agent 接入，重点看 `mcp_server/README.md` 和 `mcp_server/src`。

[分析员]
目录结构很清晰。核心在 `graphiti_core/`，里面有 `graphiti.py`、`nodes.py`、`edges.py`、`graph_queries.py`、`search/`、`driver/`、`embedder/`、`llm_client/`、`models/`、`prompts/`、`utils/`。这说明它把图谱核心、存储驱动、embedding、LLM 客户端、搜索和 prompt 都拆开。`server/` 是服务化封装，`mcp_server/` 是给 Claude、Cursor 等 MCP 客户端使用的工具服务器，`tests/` 和 `tests/evals/` 则说明它不只是 demo，而是在验证检索、驱动、LLM 客户端和图操作行为。

[主持人]
Graphiti 和传统 GraphRAG 的差异，是这一期最重要的知识点。README 对比说，GraphRAG 更偏静态文档总结，通常是 batch processing；Graphiti 是动态、增量、实时更新。GraphRAG 往往用实体群落和社区摘要来回答；Graphiti 用带时间窗口的实体、事实、episode 和图遍历。GraphRAG 的矛盾处理常依赖 LLM 总结判断；Graphiti 则保留旧事实，让新事实使旧事实失效，但不删除历史。这对个人系统很关键，因为你的学习、求职和项目决策都在变，旧判断不应该被粗暴覆盖。

[分析员]
给一个具体例子。假设你每天把 Feishu Daily、BOSS 面试记录、GitHub 播客候选 repo、课程作业状态都作为 episode 写入 Graphiti。今天你记录“某岗位偏产品经理”，明天电话沟通后发现“实际偏 AI 自动化交付”。普通笔记系统可能只留下最新总结，或者两个矛盾条目并存。Graphiti 的思路是：把这两条都当成有时间和来源的事实，查询“现在我对这个岗位的判断是什么”时返回新事实；查询“我为什么改变判断”时还能追溯旧 episode。这个能力比单纯向量检索更像真正的项目记忆。

[主持人]
它的 MCP server 对你尤其重要。README 里提示新的 MCP server 可以给 Claude、Cursor 和其他 MCP clients 提供带 temporal awareness 的 context graph memory。也就是说，你可以把它接到 agent 工作流里，让 agent 不只是读某个 Markdown 文件，而是查询“这个人、这个项目、这个仓库、这个任务过去发生了什么，现在什么事实有效”。如果未来你要做一个 Codex 桌面长期助手，Graphiti 可以承担记忆层的一部分。

[分析员]
不过落地成本不低。第一，它需要图数据库和 LLM/embedding 服务，不是一个零依赖脚本。第二，README 也强调 structured output 很重要，小模型或不支持结构化输出的服务可能导致 schema 错误和 ingestion failure。第三，Graphiti 是开源核心，Zep 是托管平台；如果你自托管 Graphiti，用户管理、治理、可视化、性能和运维要自己做。第四，图谱建模很容易过度设计，个人系统不要一上来就给所有东西建复杂 ontology。

[主持人]
对你的当前项目，最合理的切入点不是全量替换 Feishu，而是做一个小型“事实记忆层”。比如先选择三个实体类型：Repository、Project、Opportunity。Repository 记录仓库用途、运行方式、限制、是否已做成播客；Project 记录 AttendancePilot、GitHub 播客、商务智能作业等项目状态；Opportunity 记录实习岗位、面试时间、JD 判断和下一步动作。每次 Daily 或播客自动化运行后，把关键事件作为 episode 写入。这样一来，agent 下次帮你做决策时可以问图谱，而不是从零翻笔记。

[分析员]
读源码的路线建议是：先读 README 理解 temporal context graph；再看 `examples/quickstart` 学最小写入和查询；然后看 `graphiti_core/graphiti.py` 把 API 入口串起来；再看 `nodes.py`、`edges.py`、`graph_queries.py` 理解数据模型；最后看 `mcp_server`，评估如何让 Codex 或 Claude 调它。不要一开始沉到所有 backend driver 里，那会迷路。先搞清楚 episode 到 fact 到 search 的主链路。

[主持人]
这一期的结论是：Graphiti 值得你重点收藏，因为它解决的是“长期上下文会变化”这个真实痛点。你的知识库不是百科，而是每天被新项目、新岗位、新课程、新 repo 改写的行动系统。Graphiti 教你的关键设计，是保留来源、保留时间、让事实可失效、让 agent 查询当前有效关系。它不一定今天就进生产，但它应该进入你的 Personal Knowledge Agent 架构备选。

[分析员]
再强调一个容易忽略的点：Graphiti 的 episode 概念非常适合自动化日志。你每天的 GitHub 播客运行，天然会产生 episode：候选仓库、选择理由、脚本路径、音频路径、时长、失败重试、commit hash。现在这些信息在 daily index 和 git history 里，已经可追溯；如果写入 Graphiti，就能问更高层的问题，比如“过去三天哪些仓库都和 Feishu 自动化有关”“哪些 repo 反复出现但还没做成项目”“哪个选题最接近 AI FDE 面试展示”。这就是从文件索引升级到可查询事实网络。

[主持人]
还有一个和 Feishu 很贴的方向：Daily 不是静态笔记，而是每天变化的控制面。Graphiti 可以把 Daily 里的人、项目、任务、机会抽成实体，把“今天判断”“下一步动作”“来源链接”抽成带时间的边。这样 agent 不需要每次全文读完所有 Daily 才知道你在做什么，而是可以先查询当前有效事实，再按需打开原文。注意，这不是替代 Feishu。Feishu 仍然是你看的地方、写的地方、协作的地方；Graphiti 更像背后的语义索引和时间机器。

[分析员]
最后给一个风险提醒。记忆系统最怕把错误结构化以后变得更难纠正。所以一开始不要让 Graphiti 自动吞掉所有内容。先从低风险、可验证的事件开始，比如“某仓库已生成播客”“某岗位已投递”“某课程报告已完成截图”“某项目下一步是补 demo”。每条事实都带 source。等你确认查询有用，再逐步增加实体类型。Graphiti 的能力很强，但个人系统的第一目标不是宏大，而是可信。

[主持人]
所以你可以把 Graphiti 作为“第二阶段基础设施”。第一阶段，继续用 Feishu、Markdown index 和 git commit 保证产物可追溯；第二阶段，把已经稳定的 index 事件写成 graph episode；第三阶段，让 agent 在做选题、求职判断或项目复盘前先查图谱。这样迁移风险最小。Graphiti 很适合长期，但它不应该打断你现在已经跑通的每日生产闭环。

[分析员]
如果用一句工程话概括 Graphiti 的位置：它不是资料仓库，而是上下文判断层。资料仓库回答“原文在哪里”，向量库回答“哪段文本相似”，Graphiti 更适合回答“现在有哪些关系成立，它们从什么时候开始成立，证据来自哪里”。这个差异对 agent 很关键，因为 agent 做行动决策时，最需要的往往不是最长的原文，而是当前有效事实和变化原因。你的系统已经有 Feishu 和 GitHub 存原文，下一步真正缺的，正是这种随时间演化的判断层。

[主持人]
所以今天听完不用急着部署。先把 Graphiti 当成设计语言：episode、entity、fact、validity window、provenance、hybrid retrieval。下次你整理岗位、项目或仓库时，试着用这些词重新描述一遍信息结构。只要你开始区分“事实本身”“事实来源”“事实有效时间”“事实被什么新信息替代”，你的个人知识系统就已经比普通笔记更接近 agent memory 了。
