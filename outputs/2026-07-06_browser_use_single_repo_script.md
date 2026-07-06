# 单仓库播客 03：browser-use，给 Coding Agent 一个可靠浏览器

[主持人]
今天这一期只讲一个仓库：`browser-use/browser-use`。它的定位很直接：Make websites accessible for AI agents。更具体一点，它在 README 里已经把方向喊出来了：Browser Use CLI 3.0 是给 Claude Code、Codex 这类 coding agent 的浏览器能力。对你来说，这个仓库的价值不是“自动填表”这种演示，而是它把浏览器操作变成 agent 可以稳定调用的工具面，适合接到信息雷达、GitHub 研究、Feishu 页面处理和产品案例采集里。

[分析员]
先讲它解决的问题。大模型要操作网页，最原始的做法是看截图、点坐标、等页面变化。这种方式很脆弱，也很吃上下文。browser-use 的思路是把网页变成 agent 可理解的对象和动作：打开页面、读页面信息、点击、输入、提取内容、保留会话。它既提供 Python 库，也提供 CLI，还提供 skill 和 MCP 相关目录。它关注的不只是“能打开浏览器”，而是让 agent 在真实网页任务中有更高成功率。

[主持人]
怎么跑？README 里人类快速开始是 `uv add browser-use` 或 `pip install browser-use`。然后写一个 Python 脚本：导入 `Agent`、`BrowserProfile`、`ChatBrowserUse`，给 agent 一个任务，比如找到 browser-use 仓库星数，指定 allowed domains，然后 `await agent.run()`。如果走 CLI，可以用 `browser-use` 命令直接执行一段 Python 风格操作，例如 `new_tab("https://example.com")` 和 `page_info()`。它也提供 `uvx browser-use init --template default` 生成模板。

[分析员]
看仓库结构。核心包在 `browser_use/`。`agent/` 里有 agent service、prompts、judge、views，负责高层任务循环。`browser/` 里有 session、profile、events、chrome、video_recorder，负责浏览器会话和配置。`actor/` 里有 page、mouse、element，偏动作执行。`dom/` 里有 enhanced snapshot、markdown extractor、service，把页面转成模型更容易处理的结构。`controller/` 和 `tools/` 提供工具层。`mcp/`、`skills/`、`cli.py` 则说明它在努力覆盖不同 agent 接入方式。

[主持人]
一个关键设计是 allowed domains。README 示例里 `BrowserProfile` 设置了 `allowed_domains=["*.github.com"]`。这不是装饰项，而是 agent 浏览器自动化的安全边界。你的 GitHub 播客系统如果让 agent 去找仓库、读 README、看 issues 或 releases，也应该限制域名和任务范围。尤其当它接触 Feishu、GitHub、TokenDance 这类登录态时，边界越清楚，越不容易出现误操作。

[分析员]
第二个设计是“给 agent CLI，而不是只给 MCP”。README 里提到 Browser Use CLI 3.0，让 coding agent 通过命令使用浏览器；仓库里也有 `browser_use/skills`。这和 Microsoft Playwright MCP 的说明形成对照：有些任务适合 MCP 的持续会话，有些 coding agent 更适合短命令和 skill。对 Codex 自动化来说，CLI 往往更省上下文，也更容易写入脚本、日志和重试。

[主持人]
它和你的当前工作流有什么关系？第一，GitHub 候选仓库发现可以不只靠 API 搜索，也可以让 browser-use 打开 GitHub Trending、项目主页、docs、release 页面，提取“是否值得做一期”的证据。第二，你的 Feishu/Daily 系统里有很多页面和剪存，browser-use 可以承担“打开页面、读取结构、找链接、回填摘要”的自动化。第三，AI FDE 或面试案例需要收集产品材料时，它可以作为浏览器执行层，而不是让你手动复制页面。

[分析员]
但不要过度神化它。browser-use 是浏览器 agent 工具，不是信息质量判断器。网页结构变动、登录态、验证码、反爬、动态加载，都会影响成功率。它的 cloud 版本可能更强，但你的本地自动化要先明确是否允许外部服务、是否能处理隐私页面。对 GitHub 播客这类定时任务，浏览器自动化最好只用于 API 不够用的补充环节，而不要把所有候选发现都压在浏览器 UI 上。

[主持人]
如果把它接进你的项目，我建议先做一个很小的用例：给一个 GitHub repo URL，browser-use 打开 README、docs、release 或 examples 页面，提取三类证据：项目一句话、最小运行方式、核心入口路径。然后把这些证据写进 `work/repo_notes`，脚本生成时必须引用。这样它不是替代 Codex 思考，而是替代你机械地打开网页和摘信息。

[分析员]
它的限制也可以转化成设计原则。第一，所有自动浏览都要有 domain allowlist。第二，所有写操作默认禁止，除非任务明确要求。第三，浏览器观察结果要落日志，避免“看过但没记录”。第四，和 Feishu 相关时要区分公开文档、个人知识库和需要权限的页面，不能把登录态内容写进公开输出。你的播客系统最终应该把 browser-use 当作一个受控采集器，而不是自由行动的代理。

[主持人]
这一期结论：browser-use 对你的价值在“连接真实网页世界”。它不能直接让今天的 5 期播客变得更长，但它能让明天的候选发现更真实，让 Feishu 和 GitHub 页面材料进入自动化，让 AI 产品案例收集从手工浏览变成可重复流程。对一个以 Codex、Feishu、GitHub 和播客生产为核心的个人系统来说，这类浏览器能力是很关键的一块执行肌肉。

[分析员]
再具体一点，browser-use 可以承担三种小任务。第一种是 GitHub 页面证据采集：打开仓库主页、docs、examples、releases，抽取安装命令、核心功能、最近更新和 demo 链接。第二种是产品案例采集：打开一个 AI 工具网站，记录它的导航、定价、核心 workflow 和用户承诺。第三种是个人知识系统回填：打开 Feishu 或其他页面，把生成的播客索引写回指定位置。不过第三种涉及登录态和写操作，必须单独加确认和审计。

[主持人]
它对 agent 设计的启发也很明显。一个好的浏览器 agent 不应该只是“能点击”，而应该能把页面转成稳定表示，再让模型在稳定表示上行动。仓库里的 `dom`、`agent`、`browser`、`actor` 分层正是这个思路：DOM 负责观察，browser 负责会话，actor 负责动作，agent 负责策略。你的播客系统也可以学这种分层：source 负责候选，ingestion 负责读仓库，script 负责写稿，audio 负责合成，verification 负责验收，index 负责状态。

[分析员]
还有一点很适合你的 AI FDE / 产品化方向：browser-use 不只是开发工具，也是演示工具。你做面试案例或产品故事时，最有说服力的不是“我能写脚本”，而是“我让 agent 在真实网页上完成了一个端到端任务，并且有日志、有回放、有边界”。如果未来你要展示 ExpenseFlow 或 GitHub 播客系统，浏览器自动化可以承担可视化 demo，让别人看到工作流而不是只听概念。

[主持人]
不过使用时要克制。比如今天的播客生产没有必要用 browser-use 来打开五个 GitHub 页面，因为本地 clone 和 README 已经足够。真正该用它的时候，是网页本身就是信息源，或者网页交互是任务的一部分。这个判断能帮你避免自动化过度复杂：能用 git 和 API 解决的，不必上浏览器；必须看页面结构或登录态时，再让浏览器工具出场。

[分析员]
最后给一个具体下一步：为播客项目写一个 `browser_research.md` 模板。每次浏览器采集只填四项：页面 URL、观察到的事实、截图或页面片段路径、对本期选题的影响。这样 browser-use 的输出不会飘散在终端里，而会进入可复查材料。工具的价值不只是执行动作，还在于把动作变成证据链。

[主持人]
再从安全角度补一层。浏览器自动化最容易被低估的风险，是它天然继承用户登录态。如果 agent 打开的是 GitHub、Feishu、Gmail、支付后台，它看到的不是公开网页，而是你的个人工作面。所以 browser-use 这类工具接入个人系统时，必须有三条默认规则：只读优先，域名白名单，输出最小化。尤其是播客脚本这种会提交到远程的文件，不能把登录页面里的私有内容原样写进去。

[分析员]
它和 Feishu 的结合也要分阶段。第一阶段，只让它读公开网页和 GitHub，提升候选发现。第二阶段，让它读你明确指定的 Feishu 页面，只提取标题、链接和你允许的摘要。第三阶段，才考虑自动回填索引，而且每次写入前都要有 dry run 或可回滚记录。这个顺序很重要，因为工具能力增长得很快，但个人知识库的权限边界不能跟着模糊。

[主持人]
从产品化角度看，browser-use 还代表一种趋势：AI agent 不再只在 IDE 里写代码，它会跨网页、文档、表格和后台系统执行任务。你做 AI FDE 或 AI 产品经理案例时，可以把它当作“agent 执行层”的现实样本来讲。一个好案例不是“我用了大模型”，而是“我把任务拆成工具可执行的步骤，并且每一步都有边界、日志和验收”。

[分析员]
放回今天的播客系统，它最适合接的位置不是音频合成，而是上游调研和下游分发。上游，它帮你发现网页证据；下游，它可以把完成的 daily index 回填到 Feishu 或发布页面。中间的写稿和 TTS 仍然交给现有 pipeline。这样分工清楚，系统复杂度也不会失控。
