# 2026-07-07 单仓库播客脚本：larksuite/cli

[主持人]
这一集只讲 `larksuite/cli`，也就是官方 Lark/Feishu CLI。这个仓库和你高度相关，因为你的知识库、Daily、习惯账户、项目交接、面试材料、文章归档都在 Feishu 里。它的 README 直接说：这是给人类和 AI Agents 用的官方 CLI，覆盖 Messenger、Docs、Base、Sheets、Calendar、Mail、Tasks、Meetings、Wiki、Markdown 等核心域，有 200 多个命令和 26 个 AI Agent Skills。

[分析员]
先讲怎么运行。推荐安装是 `npx @larksuite/cli@latest install`。配置应用凭据用 `lark-cli config init`，登录用 `lark-cli auth login --recommend`，验证用 `lark-cli auth status`，然后可以跑 `lark-cli calendar +agenda`。README 还专门给 AI Agent 写了 quick start：运行 `config init --new`，拿授权 URL 给用户；再运行 `auth login --recommend`，同样把 URL 给用户；最后检查状态。

[主持人]
这个 CLI 的关键设计是“三层命令系统”。第一层是 `+shortcut`，比如 `lark-cli calendar +agenda`、`lark-cli docs +create`，适合人和 agent 直接完成任务。第二层是 API commands，自动从 OpenAPI 元数据生成，比如 `lark-cli calendar calendars list`。第三层是 raw API，像 `lark-cli api GET /open-apis/calendar/v4/calendars`，作为逃生口。对 agent 来说，优先 shortcut，缺口再用 typed API，最后才 raw API。

[分析员]
源码入口很简单：`main.go` 只调用 `cmd.Execute()`，并导入 env credential provider。真正的根命令在 `cmd/root.go`。它的 root help 对 agent 非常友好：浏览命令用 `lark-cli <domain> --help`，检查调用用 `lark-cli schema <service.resource.method>`，优先用 `+shortcut`，每个命令标注 read、write 或 high-risk-write，高风险写入需要 `--yes` 且用户确认。这是典型的 agent-native CLI 设计。

[主持人]
内部架构可以从 `AGENTS.md` 和 `internal/cmdutil/factory.go` 看。`Factory` 注入配置、HTTP client、Lark SDK client、IO streams、Keychain、Credential、FileIOProvider。身份解析支持 user、bot 和 auto，还能根据 strict mode 强制身份。也就是说它不是把 token 塞进全局变量，而是把“当前身份、凭据、客户端、输出格式”作为命令运行上下文传进去。

[分析员]
`shortcuts/common/runner.go` 是 shortcut 执行管线。`RuntimeContext` 提供 `As()`、`AccessToken()`、`LarkSDK()`、`EnsureScopes()`、flag 读取、输出过滤等工具。它还区分 stdout 是数据、stderr 是提示，JSON 成功和错误 envelope 分开。对你来说，这一点特别重要：Feishu 自动化如果要让 agent 稳定调用，输出必须机器可读，错误必须带原因、参数和修复建议。

[主持人]
这个仓库对你的直接用法非常明确。第一，把 Daily 摘要、会议纪要、待办、文章归档，都可以变成 `lark-cli` 命令或技能调用。第二，你的 GitHub 播客每日 index 可以写回 Feishu Daily：仓库名、脚本、音频路径、时长、状态。第三，你的“时间负债”“付费汇总”“实习简历描述”这些表格和文档，可以通过 Base、Sheets、Docs、Tasks 串成一个个人操作系统。

[分析员]
但限制也要讲。第一，真正使用需要 Feishu/Lark 应用、权限范围、OAuth 登录，agent 不能替用户绕过授权。第二，写操作要谨慎，尤其是 Base、Docs、Mail、IM、Tasks，最好先 `--dry-run` 或读状态再写。第三，CLI 和 skills 版本会漂移，仓库里还有 `_notice.skills` 和 `lark-cli update` 机制，说明长期使用要维护版本一致性。

[主持人]
如果今天要落地一个小实验，我建议不是一下子接管整个 Feishu，而是做一个窄动作：每天播客生产完成后，用 `lark-cli docs +create` 或 Markdown 能力，在 `LifeOps / Daily` 下追加一个“GitHub Podcast Radar”小节，列出五集、路径、时长、fit role、下一步。这样播客系统就进入你的真实控制面板，而不是只留在本地 repo。

[分析员]
总结：`larksuite/cli` 是你 Feishu 工作流最值得长期关注的基础设施。它的价值在于官方、覆盖面广、agent-native、命令分层清晰、错误结构化、身份和权限边界明确。对你的个人系统，它可以成为 Codex 和 Feishu 之间最稳定的桥。

[主持人]
我们把一个真实场景跑通一下。假设今天播客五集完成后，你想写入 Daily。第一步不是直接写，而是先确认目标位置，比如用 wiki 或 docs 命令找到当天 Daily 页面。第二步生成一段 Markdown：每一集有 repo、fit role、script path、audio path、duration、status。第三步再用 docs 或 markdown 写入能力追加。第四步读回页面确认内容存在。这个流程看似繁琐，但它把“写入个人知识库”变成可审计操作。

[分析员]
`lark-cli` 的 `--format json`、`--jq`、`--dry-run` 对这个场景特别重要。`--dry-run` 可以在真正写入前预览请求；JSON 输出可以让脚本稳定解析；`--jq` 可以只取需要字段。你现在很多任务会在 Feishu 页面、WPS、浏览器和本地 repo 之间切换，如果每一步输出都适合 agent 解析，系统就会越来越稳。

[主持人]
再说身份。很多 Feishu 动作既可以 bot 身份做，也可以 user 身份做。创建公开项目通知可能适合 bot；读取个人 Daily、私人简历材料、会议纪要，通常需要 user。`lark-cli` 在 Factory 和 RuntimeContext 里把身份解析做成一等概念，这一点很关键。你的自动化也应该在每个动作前标明“这一步需要 user 还是 bot”，不要让 agent 自己猜。

[分析员]
如果你要扩展自己的 Feishu 能力，优先顺序可以是：先读 Daily 和任务，形成每日上下文；再写播客生产结果；再接会议纪要和项目交接；最后才做高风险写入，比如发消息、改 Base 大量记录、发送邮件。用这个顺序，你能尽快得到价值，同时把误操作成本控制住。

[主持人]
这个仓库还提醒我们，给 agent 用的 CLI 必须重视错误信息。`AGENTS.md` 里说，错误要结构化、可行动、具体，因为 AI 会解析错误来决定下一步。比如缺权限时，不应该只说 failed，而应该说缺哪个 scope、应该去哪里授权、是否可以用 `--as user` 或 `--as bot`。这对你自己的 pipeline 也一样。TTS 失败要说是 key 缺失、HTTP 错误、decode 失败，还是时长不合格。

[分析员]
如果未来你把播客结果写入 Feishu，失败恢复尤其重要。写脚本成功但 TTS 失败，不应该创建“完成”记录；音频成功但 daily index 没写，不应该重新合成音频；Feishu 写入失败，应该保留本地 index 并报告 Feishu 阻塞。这种分步状态，正是 `lark-cli` 这种 agent-native 工具一直在强调的：让机器知道现在处在哪一步，以及下一步应该怎么修。

[主持人]
所以这集不是单纯推荐一个 Feishu 命令行工具，而是在讲个人系统的底层连接器。你已经有 Feishu 作为知识库，有 Codex 作为执行层，有 GitHub 作为代码和音频产物仓库。`lark-cli` 可以把这三者连起来，让本地生产结果进入你的日常工作台。

[分析员]
最后的判断是：如果你今天只能选一个 Feishu 自动化基础设施先深入，优先读 `larksuite/cli`。因为它的命令、错误、身份、权限和输出都适合脚本化，也适合 agent 学习。等 CLI 路线跑稳，再把 MCP 路线接进对话式操作。这样你的 Feishu 系统会从“人工打开页面复制粘贴”，逐步变成“Codex 执行、Feishu 沉淀、GitHub 留痕”的闭环。

[主持人]
最后给一个很具体的每日流程：早上先让 `lark-cli calendar +agenda` 和 task 查询形成当天上下文；白天把 GitHub 播客生产结果写入 Daily；晚上再读回 Daily 和任务，生成一个小结。这个流程不需要一次性自动化所有 Feishu 功能，但能把信息流、行动流和复盘流串起来。`lark-cli` 的价值就在这里：它把 Feishu 从浏览器页面变成了可被 agent 稳定操作的工作台。

[分析员]
只要记住一个原则：先读后写，先低风险后高风险，先固定流程后开放探索。这个顺序比任何单个命令都重要。
