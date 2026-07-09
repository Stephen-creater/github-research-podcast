# Supermemory 单仓播客脚本

[主持人]
今天这一期只讲 `supermemoryai/supermemory`。它把自己定义为 AI 的 memory and context layer，也可以作为公司或个人大脑使用。对你的当前工作方式来说，这个 repo 很贴近：你一边用 Codex 做自动化，一边用 Feishu Daily 记录求职、课程、项目和信息前哨站，还希望把 GitHub 仓库变成个性化音频。问题不只是“存资料”，而是如何让 AI 在不同会话、不同工具、不同项目之间拿到正确上下文。

[分析员]
README 里最重要的能力有五类：Memory，从对话中抽取事实，处理时间变化、矛盾和自动遗忘；User Profiles，自动维护稳定事实和近期活动，并在一次调用里返回；Hybrid Search，把 RAG 和个人记忆合在一个查询里；Connectors，连接 Google Drive、Gmail、Notion、OneDrive、GitHub，并用 webhook 同步；Multi-modal Extractors，处理 PDF、图片 OCR、视频转写、代码 AST-aware chunking。这个组合说明它不是单纯向量数据库，而是完整上下文栈。

[主持人]
使用路径分三种。普通用户可以用 Supermemory App、浏览器扩展、插件和 MCP server，让 Claude Desktop、Cursor、Windsurf、VS Code、Claude Code、OpenCode 等客户端拥有持久记忆。开发者可以 `npm install supermemory` 或 `pip install supermemory`，然后 `client.add({ content, containerTag })` 保存内容，用 `client.profile({ containerTag, q })` 获取 profile 和 search results。自托管则可以通过安装脚本运行本地版本，README 强调 one binary、zero config，也支持 Ollama 这类本地模型。

[分析员]
看目录结构，它是一个 monorepo。`apps/web` 是网页应用，`apps/browser-extension` 是浏览器扩展，`apps/mcp` 是 MCP 相关入口，`apps/docs` 是文档站，`packages/memory-graph` 暗示核心记忆图谱能力，`packages/ai-sdk`、`packages/openai-sdk-python`、`packages/agent-framework-python`、`packages/cartesia-sdk-python` 等提供不同 SDK 和 agent framework 接入，`packages/lib` 放共享 API、auth、queries、types、similarity 等基础能力。它的工程形态更像一个产品平台，而不是小库。

[主持人]
对你的第一个启发，是“个人大脑”不应该只是一堆 Markdown。Feishu Daily 很适合做人类可读的工作台，但 agent 检索时需要更结构化的入口。Supermemory 的 container tag、profile、memory、recall、context 这些概念可以映射到你的系统：每个项目一个 container，比如 `github-podcast`、`internship-search`、`business-intelligence-course`；稳定偏好进入 profile；每天发生的变化进入 memory；agent 开始任务时先拉 context。

[分析员]
第二个启发，是 connectors。你的输入分布在 Gmail、GitHub、Feishu、浏览器、WPS、本地文件和课程资料里。Supermemory 内置 Google Drive、Gmail、Notion、OneDrive、GitHub 等连接器，虽然没有直接等同 Feishu，但它给了架构样板：不要让用户手动搬运所有资料，而是让连接器持续同步，然后统一抽取和检索。对你来说，Feishu/Lark connector 或本地 Feishu 导出桥接，就是可以借鉴的方向。

[主持人]
第三个启发，是 MCP。README 给了 `npx -y install-mcp@latest https://mcp.supermemory.ai/mcp --client claude --oauth=yes` 的安装方式，并列出 `memory`、`recall`、`context` 三类工具。这个设计很适合你的 Codex/Claude 双工具环境：不是每个 agent 都自己实现记忆，而是通过 MCP 调同一个记忆服务。这样换客户端时，上下文不丢；也更容易审计谁写入了什么记忆。

[分析员]
如果把它接到 GitHub 播客，最自然的方式是做“已听和已做仓库记忆”。每个 episode 完成后，保存 repo、commit、主题、音频时长、和你的个人 fit 判断。下一次选仓库时，先 recall “已经讲过哪些 browser automation repo”“哪些 memory repo 适合后续二刷”“哪些工具可以进入 Feishu Daily demo”。这会让播客从每日生产变成长期学习路径，而不是孤立音频列表。

[主持人]
如果把它接到求职和 AI FDE，价值也很明显。你可以把公司画像、岗位职责、面试重点、待遇推进状态、个人判断都作为记忆，但要按 container 隔离。比如 `internship-hangzhou-youzan`、`puhui-future-ai-media`、`ai-fde-general`。agent 问“这个岗位适合我吗”时，不应该从全局随机召回，而应该先在对应 container 里找，再结合全局偏好。Supermemory 的 project/container 思路能减少上下文串线。

[分析员]
局限同样重要。第一，它是平台型项目，接入成本高于一个小库，你需要先决定是用 API、MCP、还是自托管。第二，连接器越多，隐私和权限风险越大，尤其是 Gmail、GitHub、Drive 这类高权限入口。第三，自动记忆如果没有 review，会把误解、临时想法和过期事实写成长期上下文。第四，自托管虽然可控，但需要处理升级、备份、模型配置、索引和鉴权。第五，个人大脑不是越全越好，关键是可解释、可删除、可隔离。

[主持人]
读源码建议按产品路径走。第一，读 README 和 `apps/docs` 下的 quickstart、memory operations、search、user profiles，理解外部 API。第二，读 `apps/mcp`，看 MCP server 如何暴露 memory、recall、context。第三，读 `packages/lib/api.ts`、`auth.ts`、`queries.ts`、`types.ts`，理解共享客户端和数据类型。第四，读 `packages/memory-graph`，看记忆图谱如何建模。第五，读 `apps/browser-extension` 和 `apps/web`，理解它如何从用户行为到后台记忆服务。

[分析员]
如果今天做最小实验，我建议不用全量接管 Feishu，而是只做一个“GitHub 播客上下文容器”。把每天的 five episodes 存成 memories，把 repo fit role 存成 tags，把脚本里提到的可落地项目存成 action hints。然后在下一次选题时问：过去四天已经覆盖了哪些主题？浏览器自动化、网页摄取、记忆系统、工作流自动化还缺哪类？这样 Supermemory 的价值会很快显现。

[主持人]
Supermemory 和 Mem0 的区别，可以用产品重心来理解。Mem0 更像可嵌入应用的 memory layer，强调多后端、多 SDK 和 agent skills；Supermemory 更像跨工具的上下文平台，强调用户 profile、connectors、MCP、浏览器扩展和个人大脑。你的使用场景里，如果是给一个具体 agent 应用加 memory，Mem0 更轻；如果是希望多个 AI 工具共享同一套个人上下文，Supermemory 的思路更完整。

[分析员]
这一期结论：Supermemory 值得学，因为它把“AI 记住我”拆成了产品化系统：资料连接器、事实抽取、用户画像、混合检索、MCP 工具、浏览器扩展、自托管和 SDK。它对你的 Feishu/Daily 项目非常有启发，但落地时一定要小步试验，先从低风险容器开始，逐步验证检索质量、隔离策略和删除能力。

[主持人]
最后给一个判断标准：如果某条信息会影响未来决策，比如“我不想做纯运营岗位”“某门课的报告格式要求”“某自动化禁止使用本地 fallback”，它适合进入记忆；如果只是一次性草稿、敏感凭据、未确认传闻或临时情绪，就不应该自动进入长期上下文。Supermemory 的强大之处是让 AI 有长期记忆，但真正的工程难点，是决定什么值得被记住。

[分析员]
再放到你的 Feishu 体系里看，Supermemory 不应该替代 Feishu。Feishu 仍然是你的人类可读工作台，Daily 仍然承载日期、项目、判断和行动。Supermemory 更适合作为 agent 的快速上下文索引：当 Codex 开始一个任务时，先用 recall 找到相关偏好和项目事实，再决定要不要读取完整 Feishu 页面。这样可以减少每次从零翻文档的成本，也避免把人类笔记和机器检索混成一个不可控黑箱。

[主持人]
还有一个值得学的点是“profile 和 search results 分离”。Profile 是稳定偏好和近期活动，适合在任务开始时注入；search results 是针对具体问题召回的证据，适合回答时引用。你的个人系统也可以这样设计：不要每次都把所有记忆塞进 prompt，而是先注入少量稳定 profile，再按问题检索项目证据。这样上下文更短，答案也更不容易漂。

[分析员]
所以这期的行动建议是：把 Supermemory 当成“跨客户端上下文层”的样板，而不是马上全量迁移。先用一个容器记录 GitHub 播客学习路径，再用一个容器记录 AI FDE 方向判断，最后再评估是否接入求职和课程材料。每一步都要检查召回是否准确、是否能删除、是否能导出、是否能解释来源。能解释的记忆，才配进入长期系统。
