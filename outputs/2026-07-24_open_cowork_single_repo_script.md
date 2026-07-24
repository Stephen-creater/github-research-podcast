# OpenCoworkAI/open-cowork：桌面 agent 产品壳的安全边界

[主持人]
今天只聊一个仓库：`OpenCoworkAI/open-cowork`。它是一个开源的 Windows 和 macOS 桌面 agent 应用，用 Electron 把 Claude Code 风格的编码代理、MCP 工具、Skills、沙箱隔离、实时 trace、多模型配置，以及 Feishu 和 Slack 远程控制放进一个产品壳里。

这期和最近项目的关系很直接。我们现在面对的不是“能不能让模型写代码”，而是“怎么把本地 agent 变成一个可用、可控、可恢复的桌面产品”：它能不能只碰允许的工作区？MCP 子进程会不会拿到不该拿的环境变量？远程 Feishu 消息怎么验证？Skills 怎么发现、热加载和删除？用户怎么知道工具到底执行了什么？

先给结论：**Study only / 仅研究并做一个安全边界试验**。不要马上把生产 Feishu、AI 视频或私人桌面流程迁进去。最小动作是拿它做一份 desktop agent shell checklist，再用一个 disposable public workspace 做本地试验。

[分析员]
我们检查的 pinned commit 是 `6f0c04741386b8600aa977f14ac0679d2203bd1b`。GitHub API 显示仓库是 TypeScript 为主，license 是 MIT，描述是面向 Windows 和 macOS 的开源 AI agent desktop app，特点包括 one-click install Claude Code、MCP tools、Skills、sandbox isolation、多模型支持和 Feishu/Slack integration。

README 里的定位也很明确：Open Cowork 是 Claude Cowork 的开源实现，支持 Windows 和 macOS 安装器；可以在沙箱 workspace 里管理文件、生成 PPTX、DOCX、XLSX、PDF 等专业输出；可以通过 MCP 连接 browser、Notion 和其他桌面 app；可以做 GUI automation；也可以通过 Feishu/Lark 和 Slack 做远程控制。

这不是一个普通 SDK，而是一个桌面产品壳。代码结构也印证了这一点：`src/main` 是 Electron main process，里面有 agent、sandbox、mcp、skills、remote、memory、session、tools；`src/renderer` 是 React UI，里面有 ChatView、ConfigModal、ContextPanel、PermissionDialog、TracePanel、RemoteControlPanel、SandboxSetupDialog、SubagentProgress 等组件。

[主持人]
最值得看的第一块是 sandbox 和 path boundary。它不只是说“我们安全”，而是在代码里把路径解析、禁止目录、symlink escape、危险命令模式都做成模块。

比如 `src/main/sandbox/path-guard.ts` 会根据 Linux/WSL 和 macOS/Lima 选择不同的 forbidden path patterns，还会拦截 `rm -rf /`、`curl | bash`、`sudo rm`、`dd of=/dev` 这类危险命令。`src/main/sandbox/path-resolver.ts` 则把 virtual path 映射到真实路径，检查 mount root containment，拒绝 `..` 和 `~`，并检查 symlink 是否逃出授权目录。

[分析员]
这对当前自动化非常可复用。GitHub 日研播客、Feishu 操作、AI 视频生产、甚至 AdventureX 的桌面 agent 原型，都应该先定义 workspace root、source inputs、maintained code、outputs、scratch 和 third-party repo 的边界。远程消息和模型输出不能默认拥有整台 Mac。

第二块是 MCP。`src/main/mcp/mcp-manager.ts` 管理 MCP server config、stdio/SSE/streamable HTTP transport、OAuth retry、server lifecycle、tool/resource/prompt discovery，还会把 MCP tool name 规范化到模型/provider 能接受的长度和字符范围。它还把 list tools 和 call tool timeout 设成五分钟，说明真实 MCP server 发现和调用可能很慢，不能只按 demo 的十秒超时设计。

更重要的是风险。2026 年 7 月 17 日的 open issue #305 明确指出，MCP server child processes 可能继承完整 `process.env`，包括 API keys；随后 PR #306 的标题就是用默认环境替换这种泄漏。这个点对 Codex plugin、Feishu connector、browser automation 都很关键：子进程应该拿最小 env、明确 cwd、明确 credential 注入、明确日志脱敏。

[主持人]
第三块是 Skills。`src/main/skills/skills-manager.ts` 负责 built-in、global、project-level skills 的发现，解析 `SKILL.md` metadata，做 hot reload，还处理 plugin install/uninstall。它会校验 skill name 不能包含路径分隔符或父目录引用，也会跳过 dangling symlink。

这和我们最近的 Skills/plugin 清理很贴近。一个 Skill 不能只是散落在硬盘上的提示词文件。它需要生命周期：发现、校验、启用、禁用或卸载、热加载、所有权边界、以及和 MCP server 的关系。

[分析员]
第四块是 Feishu 远程控制。`src/main/remote/channels/feishu/feishu-channel.ts` 会刷新 access token，读取 bot info，支持 WebSocket 或 webhook 模式，发送消息时有 retry；webhook 侧会检查 `X-Lark-Signature`，timestamp，nonce 和 verification token，用 HMAC 做签名验证，而且没有 verification token 就拒绝 webhook。

这个比普通 webhook 示例更接近真实工作流。因为一旦 Feishu 消息可以远程驱动本地 agent，就必须知道消息来源是谁、签名是否可信、允许哪些用户、哪些命令需要用户批准、失败重试会不会重复执行。

[主持人]
那它具体帮哪个近期项目决策？第一，是 AdventureX 和桌面 agent 产品化：MVP 不一定要做完整“个人 AI 身份”，更可能先做一个低摩擦 continuation/control layer，让用户把任务交给桌面 agent，但边界、trace、权限和恢复都清楚。

第二，是当前 Codex、Skills、Feishu、AI 视频和自动化工作：如果我们要把这些流程做成可复用产品，不能只写 prompt，需要把 permission、workspace contract、MCP env、remote auth、trace、memory 和 schedule 都纳入产品设计。

[分析员]
最小试验应该非常小。不要安装到主工作环境，不要接私人 Feishu、Slack、browser 或 TTS 凭证。先做一个 public-only checklist，再开一个 disposable workspace。

这个试验只验证六件事：一个 workspace folder；一个 Skill；一个 MCP server，而且 env 是最小化的；一个需要 permission 的命令；一条 trace；一个 Feishu-style remote message，可以先模拟，如果真的要连 Feishu，也只连测试 bot。验收标准不是“agent 多聪明”，而是它能不能清楚解释 allowed paths、denied paths、tool approvals、env exposure 和 stop/resume state。

[主持人]
局限也要讲。Open Cowork 是 2026 年创建的年轻项目，表面积很大：Electron、sandbox、MCP、Skills、remote control、memory、installer、CI bot 都在一起。作为参考很有价值，但作为依赖直接接入风险不小。

[分析员]
沙箱也不是绝对安全。README 说 WSL2 和 Lima 是 enhanced isolation，但 fallback 可以是 native execution plus path restrictions。近期 issue 里有 Windows sandbox detection，release 里也提到修了 Lima/WSL path traversal bypass。也就是说，真要采用，必须在目标平台上测试 sandbox，而不是只信文档。

另外，README 的 macOS 安装建议里包含 `--no-quarantine`。这能降低用户摩擦，但不应该无脑复制到安全敏感的内部流程。是否绕过 Gatekeeper，是单独的信任和签名决策。

[主持人]
所以今天的建议很明确：把 `OpenCoworkAI/open-cowork` 当成桌面 agent 产品壳的参考，而不是马上迁移目标。

[分析员]
结论和报告一致：**Study only / 仅研究并做一个安全边界试验**。复用它的架构清单：Electron main/renderer 分层、WSL/Lima/native sandbox adapters、path containment、PermissionDialog、MCP lifecycle、最小子进程环境、Feishu channel verification、Skills lifecycle、memory/context strategy、trace UI，以及 CI bot 的 stale review context reset。暂时不要复制整套 app，也不要把生产 Feishu、AI 视频或私人桌面工作流接进去。
