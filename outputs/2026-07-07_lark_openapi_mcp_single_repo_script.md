# 2026-07-07 单仓库播客脚本：larksuite/lark-openapi-mcp

[主持人]
这一集只讲 `larksuite/lark-openapi-mcp`。它是官方 Feishu/Lark OpenAPI MCP 工具，把 Feishu/Lark Open Platform API 包成 MCP tools，让 Claude、Cursor、Trae 或其他支持 MCP 的 AI assistant 直接调用文档、消息、日历、任务、表格、知识库等能力。对你来说，它是“让 agent 进入 Feishu”的另一条官方路线，和 `lark-cli` 互补。

[分析员]
先讲怎么用。README 的最小配置是在 MCP client 里加一个 server：命令是 `npx`，参数是 `-y @larksuiteoapi/lark-mcp mcp -a <your_app_id> -s <your_app_secret>`。如果要用用户身份访问私人资源，需要先运行 `npx -y @larksuiteoapi/lark-mcp login -a cli_xxxx -s yyyyy`，并在应用后台配置 OAuth redirect URL，默认是 `http://localhost:3000/callback`。

[主持人]
它支持 Feishu 中国域和 Lark 国际域。默认是 `https://open.feishu.cn`，如果用国际版 Lark，可以加 `--domain https://open.larksuite.com`。它还支持 `--oauth`、`--token-mode user_access_token`、`--tools`、`--tool-name-case`、`--language zh/en`、`--mode stdio/sse/streamable`、`--config`。这说明它不是只给一个 IDE 用，而是能作为不同 agent runtime 的 MCP 后端。

[分析员]
源码入口在 `src/cli.ts`。它用 commander 定义四类命令：`whoami` 看用户 session，`login` 做 OAuth，`logout` 清除 token，`mcp` 启动 OpenAPI MCP 服务，`recall-developer-documents` 启动开发者文档检索 MCP。启动 mcp 时，它会合并默认参数、环境变量参数、配置文件参数和 CLI 参数，然后调用 `initMcpServerWithTransport('oapi', ...)`。

[主持人]
核心工具封装在 `src/mcp-tool/mcp-tool.ts` 的 `LarkMcpTool`。构造函数里，如果有 appId 和 appSecret，就创建 `@larksuiteoapi/node-sdk` 的 Client；然后根据语言、默认工具名、token mode 和工具选项过滤工具集合。`registerMcpServer` 会把每个 Lark 工具注册到 MCP server，并在调用时决定是否使用 user access token。

[分析员]
这一段的设计很关键。`TokenMode` 可以是 auto、user_access_token、tenant_access_token。需要用户 token 时，`ensureGetUserAccessToken()` 会检查 token 是否有效，过期时尝试 refresh token；如果不能刷新，就生成重新授权信息。对于 user access token 权限不足或失效的错误，它会返回带授权 URL 和说明的 MCP 错误内容。也就是说，它把“让 agent 请求用户重新授权”做成了工具协议的一部分。

[主持人]
对你的 Feishu/Daily 系统，`lark-openapi-mcp` 和 `lark-cli` 的取舍是这样的：如果你要在 shell 自动化里稳定执行，CLI 更直观；如果你要让 Claude、Codex、Cursor 在对话中直接调用 Feishu 工具，MCP 更自然。比如你说“把今天五个播客条目写到 Daily，并把音频路径挂到对应项目”，MCP 工具可以直接暴露给 assistant，而不是让 assistant 拼 shell 命令。

[分析员]
限制必须注意。README 明确提示它还在 beta，API 和功能可能变化。文件上传下载操作还不支持，直接编辑 Feishu 云文档也不支持，只支持导入和读取等能力。非 preset API 没有充分兼容测试，AI 理解和使用效果可能不稳定。所以在生产流程里，建议先启用小工具集合，比如文档读取、创建、日历、任务，不要一口气打开全部 OpenAPI。

[主持人]
如果你要用它做一个小闭环，我建议从三件事开始。第一，配置一个只读或低风险 app，先让 agent 读 Daily、读 Wiki、读 Calendar。第二，按 preset 限定工具，避免工具面过大。第三，把写入动作前置确认，比如写 Daily 或发 IM 前，要求 agent 展示将写入的 Markdown。这样既能接入 Feishu，又不会把个人知识库变成无人监管的写入目标。

[分析员]
总结：`larksuite/lark-openapi-mcp` 是 Feishu/Lark 官方 MCP 桥。它的核心价值是把 OpenAPI 变成 agent 可调用的工具，并处理 app 凭据、OAuth、token mode、工具过滤和传输模式。对你的个人系统，它适合成为“对话式 Feishu 自动化入口”，而 `lark-cli` 更适合成为“脚本式 Feishu 自动化入口”。两者组合，正好覆盖你的 Daily、知识库、任务、会议和 GitHub 播客雷达。

[主持人]
我们再比较一下 MCP 和 CLI 的使用心智。CLI 像命令行工具，适合写在 pipeline 里，输入输出明确，失败码明确。MCP 像给 agent 装工具箱，适合在对话中临时组合任务，比如先查 Daily，再查任务，再创建一条文档记录。你不一定要二选一。更好的方式是：稳定重复的每日生产用 CLI；探索式、对话式、跨页面的 Feishu 操作用 MCP。

[分析员]
`lark-openapi-mcp` 还有一个很适合你的点：工具过滤。README 里可以用 `-t` 指定工具或 preset。对个人知识库来说，不建议一开始开放所有工具。比如先开 `docx`、`wiki`、`calendar`、`task` 的低风险读写，再根据需要加 `im` 或 `base`。这就像给 agent 配一个小权限房间，而不是把整栋楼钥匙都交出去。

[主持人]
从源码看，`LarkMcpTool` 在注册工具时会统一包一层 handler。这层 handler 做 client 检查、token mode 判断、用户 token 获取、错误处理和重新授权提示。这个模式对你写自定义 MCP server 也有启发：不要让每个工具自己处理鉴权和错误；应该有统一外壳，业务工具只关心“我要调用哪个 API，参数是什么”。

[分析员]
最后给一个落地建议：先把它接到一个低风险 MCP client 里，只启用读取 Daily 和查询任务的工具。然后让 agent 回答一个非常具体的问题：“今天 Daily 里和 GitHub 播客相关的未完成项是什么？”如果这个小问题能稳定回答，再逐步开放写入。这样你可以用真实 Feishu 数据验证 MCP 的价值，而不是一次性搭一个过大的自动化系统。

[主持人]
再补一个技术细节：它的 CLI 支持 stdio、sse、streamable 三种 transport。stdio 最适合本地 Claude 或 Cursor 这类工具直接启动；SSE 和 streamable 更像服务化部署。对你现阶段来说，优先 stdio，因为简单、权限范围小、出问题容易关掉。等你真的需要多个 agent 共享同一个 Feishu 工具服务，再考虑服务化模式。

[分析员]
另外，`recall-developer-documents` 命令也值得注意。它不是操作你的 Feishu 内容，而是启动开发者文档检索 MCP。对 agent 来说，这能降低“不会用 OpenAPI”带来的幻觉。你以后如果做自己的工具，也可以分两类 MCP：一类是业务操作工具，真的读写 Daily；另一类是文档检索工具，只帮助 agent 查 API 和规则。两类权限应该分开。

[主持人]
所以它给你的长期启发是：Feishu 自动化不要只追求“能调用”，还要追求“可控地调用”。工具列表要筛选，token mode 要明确，读写权限要分层，授权失败要能让用户重新授权，beta 限制要写进系统提示。做到这些，MCP 才会从一个新鲜玩具变成可靠入口。

[分析员]
和 `lark-cli` 放在一起看，今天的结论更清楚：CLI 适合固定流程，MCP 适合对话协作。你的每日播客生产、音频验证、索引提交，应该继续走固定流程；而“根据 Daily 里的上下文帮我选择今天该关注什么 repo”“把这集摘要写到哪个知识库分类”，更适合 MCP。把这两个边界分清，Feishu 自动化就不会变成一团混乱的万能工具调用。

[主持人]
最后再强调一个边界：MCP 工具越接近个人知识库，越需要最小权限。先读 Wiki、Docs、Tasks，再做有限写入；先限定工具 preset，再逐步扩大；先在一个测试文档里验证，再碰 Daily 主页面。这样做不是保守，而是让 agent 的能力增长和你的信任增长保持同步。

[分析员]
如果这个仓库未来稳定下来，它会非常适合你的“Feishu 作为操作系统”方向。Codex 负责计划和执行，MCP 负责把 Feishu 能力暴露成工具，Daily 负责承载结果和下一步。今天先理解这条链路，就已经足够有价值。
