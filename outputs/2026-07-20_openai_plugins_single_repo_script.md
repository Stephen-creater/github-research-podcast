# openai/plugins：Codex 插件到底该怎么打包

[主持人]
今天只讲一个仓库：`openai/plugins`。它不是一个普通的 SDK，也不是某个单一工具，而是当前公开的 Codex 插件目录。为什么选它？因为最近很多工作都围绕 Codex、插件、skills、Feishu/Lark、GitHub 自动化和 AI 视频工具展开，真正卡住的不是“有没有一个提示词”，而是“一个可复用能力应该怎么被打包、安装、授权、验证、下线”。这个仓库正好给了一个官方参考。

[分析员]
对。先把事实固定住：本次研究看的提交是 `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9`，提交信息是给 ClickUp 增加网站 URL。根 README 说，这个仓库包含 Codex plugin examples；每个插件在 `plugins/<name>/` 下，必须有 `.codex-plugin/plugin.json`，还可以带 `skills/`、`.app.json`、`.mcp.json`、插件级 agents、commands、hooks、assets、ui、scripts 等配套文件。也就是说，它展示的是一个插件包的目录契约，而不是单个技能文件的写法。

[主持人]
这个点很关键。之前如果只看 `SKILL.md`，很容易把所有东西都塞进一个文件：工具怎么登录、MCP 怎么接、什么时候需要用户授权、脚本放哪里、图标和命令放哪里，全靠文字约定。`openai/plugins` 的结构更像是把这些边界拆开了。

[分析员]
是的。再看 marketplace。默认 marketplace 在 `.agents/plugins/marketplace.json`，API-key 用户还有 `.agents/plugins/api_marketplace.json`。本次 pinned checkout 里，默认 marketplace 有 180 个条目，API marketplace 有 29 个条目。默认 marketplace 里 Developer Tools 和 Productivity 都是 44 个，Finance 27 个，Communication 12 个，Creativity 9 个。API marketplace 更偏开发者工具，有 18 个 Developer Tools。这个差异说明一个事实：不同登录形态下，可安装、可授权、可使用的插件集合不是完全一样的。

[主持人]
这和用户最近的操作习惯也一致。比如用户明确要求某个插件时，正确做法不是用一个相似工具替代，而是先看当前环境有没有这个插件、有没有 callable capabilities、是否需要安装或登录。如果缺授权，就停在用户接管点。

[分析员]
GitHub 插件就是一个很好的例子。它的 manifest 叫 `plugins/github/.codex-plugin/plugin.json`，里面声明 name、version、description、license、skills、apps、mcpServers、界面文案、capabilities 和默认提示。它的 `.app.json` 指向 GitHub app connector；它的 `.mcp.json` 指向 GitHub hosted MCP server，并用 `GITHUB_PAT_TOKEN` 作为 API-key Codex session 的 token 环境变量。README 还明确区分了两种情况：ChatGPT-login Codex session 用 App Connector，Codex 管理授权，不需要 PAT；API-key Codex session 则走 GitHub 官方 MCP 安装指南和环境变量。

[主持人]
所以这个仓库的复用价值，不是“拿来装一堆插件”，而是学习判断边界：什么属于 manifest，什么属于 skill，什么属于 app connector，什么属于 MCP，什么属于安装和认证 policy。

[分析员]
对。Figma 插件展示了更复杂的组合：它有 `.app.json`、`.mcp.json`、多个 Figma skills、agents、commands、hooks、assets，还有 `ui/figma-workbench.html`。OpenAI Developers 插件则把 OpenAI Platform connector、本地 MCP 确认服务、API key 设置脚本、Agents SDK skills、ChatGPT Apps skills 和测试放在一个插件包里。Remotion 插件更轻，主要打包一个 Remotion video creation skill 和图标资源。不同复杂度都在同一个目录规范下。

[主持人]
报告里还提到了 `plugin-eval`。这个插件为什么值得单独看？

[分析员]
因为它把“聊天入口”和“确定性本地工具”结合得比较清楚。`plugin-eval` 既是 Codex plugin bundle，也是本地 Node.js CLI。README 说它可以从自然语言请求开始，比如评估一个 skill、解释评分、看 token budget、做 benchmark，然后路由到本地命令。代码里 `scoring.js` 会按 manifest、skill-structure、budget、measurement、best-practice、complexity、readability、code-quality 等类别计算扣分；`analyze.js` 会解析目标路径、判断是 skill 还是 plugin，加入预算、观察用量、代码指标和改进建议。这个模式很适合当前自动化：聊天负责理解目标，本地命令负责可复验结果。

[主持人]
那它具体帮最近哪个项目问题？

[分析员]
最直接帮助的是当前 Codex 桌面和自动化操作系统。用户已经有 GitHub 研究播客、Feishu/Lark skills、ChatCut/AI 视频工作流、插件安装边界、skill 瘦身去重这些线。共同问题是：能力越来越多，但如果没有打包契约和验证规则，很快就会变成“提示词、脚本、权限、凭证、UI 入口混在一起”。`openai/plugins` 给出的答案是：用 `.codex-plugin/plugin.json` 做前门；用 `skills/` 放可复用说明；用 `.app.json` 声明 Codex connector；用 `.mcp.json` 声明 MCP server；用 marketplace policy 声明安装和认证时机；用 plugin-eval 这类工具做结构和预算检查。

[主持人]
最小试验应该怎么做？不要大迁移，只要一个有用的小动作。

[分析员]
最小试验是挑一个现有本地能力，比如一个 Feishu 辅助 skill，或者 AI 视频生产 skill，在 scratch workspace 里包成一个 skill-only plugin。只做一层最小结构：`.codex-plugin/plugin.json`，一个 `skills/<name>/SKILL.md`，如果真的需要连接器才加 `.app.json`，如果真的需要本地或远端工具才加 `.mcp.json`。然后按一个小 checklist 验证：manifest 是否存在，skill 是否能被发现，是否没有 secrets，是否没有私有路径，认证缺失时是否明确停在用户接管点。

[主持人]
哪些部分不能照抄？

[分析员]
不能把整个官方 marketplace 镜像到用户项目里；不能假设 `.app.json` 里的 connector 已经安装或授权；不能把插件 README 当成访问外部账号的许可；也不能把 license 不清楚的插件内容复制进业务交付物。这个仓库本身没有 repository-level license，很多插件自己的 manifest 才写 license，有的甚至是 proprietary。所以它适合作为目录结构、权限边界和评估方法的参考，不适合无脑搬运。

[主持人]
还有一个现实限制：这个仓库 issues 是 disabled，release list 没有给出可用 release。也就是说维护成熟度不能只靠 issue/release 判断。

[分析员]
没错。GitHub metadata 显示它最近有 push 和 update，说明在维护，但公开 issue 信号缺失。再加上插件目录、connector id、marketplace policy 都可能变化，所以要固定 commit 来研究。今天报告固定的是 `11c74d6`。未来真正采用时，应该重新看当前 main 和官方 Codex plugin docs。

[主持人]
最后结论是什么？

[分析员]
结论是：Use now，现在就用，但用的是它的 packaging reference 和决策边界，不是迁移整个系统。短期最值得做的是一个本地 plugin-wrapper 小试验，再配一个 plugin-eval 风格的验证清单。当前 GitHub 播客、Feishu 和 AI 视频管线不需要重写；只需要在新增能力时，用插件目录契约把 skill、connector、MCP、auth policy 和验证拆清楚。

[主持人]
所以今天这一期的关键词是：插件不是更长的 skill，而是一个可安装、可授权、可验证的能力包。推荐：Use now，用作当前 Codex 插件化和本地能力治理的参考。
