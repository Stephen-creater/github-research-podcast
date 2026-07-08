# n8n 单仓播客脚本

[主持人]
今天这一期只讲 n8n-io/n8n。它的 README 把自己定义为 AI agents and workflow automation platform：用可视化画布、自定义代码、自托管或云部署，把 1500 多个集成和 AI 工作流连接起来。对你来说，n8n 的意义不是“又一个自动化平台”，而是一个成熟案例：如何把很多零散工具、人工确认、模型调用、业务系统、日志和权限组织成可运维的流程。

[分析员]
先看怎么跑。README 给了两个最直接的方式：如果本机有 Node.js，可以 `npx n8n`，然后访问 `http://localhost:5678`；如果用 Docker，可以创建 `n8n_data` volume，再运行 `docker.n8n.io/n8nio/n8n`，把容器的 5678 端口暴露出来。这个入门门槛很低，所以它适合做快速试验。但你要注意它是 fair-code/source-available，并不是传统宽松开源许可，商业和再分发边界需要看 LICENSE.md 和 LICENSE_EE.md。

[主持人]
看目录结构，n8n 是典型大型 monorepo。根目录有 `packages/cli`、`packages/core`、`packages/workflow`、`packages/nodes-base`、`packages/frontend`、`packages/testing`、`packages/node-dev`。`packages/cli` 多半承担服务启动、命令行和后端入口；`packages/workflow` 是工作流数据结构和执行逻辑核心；`packages/nodes-base` 是大量内置节点；`packages/frontend` 是可视化编辑器；`packages/core` 放通用运行能力。根目录还有 `pnpm-workspace.yaml`、`package.json`、`docker/`、`docs/`、`scripts/`、`security/`，说明它以 pnpm workspace 管理多包工程。

[分析员]
n8n 的核心设计，是把自动化拆成 node 和 workflow。node 可以是触发器、HTTP 请求、数据库操作、AI 模型、代码片段、Slack、Notion、Google Sheet、Webhook 等；workflow 把 node 连接成有条件、有分支、有人工步骤的流程。README 强调可以结合 JavaScript、Python、npm 包，这说明它不只服务无代码用户，也允许工程师在关键节点写代码。这一点对你的 AI FDE 很重要，因为企业自动化通常不能纯靠拖拽，也不能全靠代码，必须能在两者之间切换。

[主持人]
它对你当前工作最有参考价值的地方，是“从 prototype 到 production”。README 里明确提到逻辑、工具使用、human approvals、observability、RBAC、audit trails、敏感数据部署。你做 Feishu 自动化或 AttendancePilot 时，如果只展示一个 LLM 聊天框，会显得很薄；如果能展示流程编排、审批节点、失败重试、执行日志、权限控制和数据回写，就更像真实交付。n8n 给你的不是具体面试答案，而是产品化检查清单。

[分析员]
如果映射到你的 Feishu/Daily 系统，可以设计这样的 n8n 工作流：定时触发读取 GitHub Trending 或 selected repos，调用抓取和转换工具生成 Markdown，调用 LLM 评分和写中文脚本，调用 TokenDance TTS 生成音频，ffprobe 验证时长，最后把 daily index 写回 GitHub，并把摘要发送到 Feishu Daily。另一个工作流可以是招聘跟进：BOSS 或官网投递信息进入 webhook，n8n 调模型抽取岗位要求，再创建 Feishu 任务、更新 Daily、生成面试准备清单。

[主持人]
读源码路线建议很明确。先读根 README 和 docs，理解使用模型。然后看 `packages/workflow`，因为这是理解 n8n 的核心抽象；再看 `packages/nodes-base`，观察一个内置节点如何声明输入输出、参数和执行逻辑；接着看 `packages/cli`，理解服务怎么启动、配置怎么加载、执行器怎么接上数据库；最后看 `packages/frontend`，理解画布如何表示 workflow。不要从 1500 个集成里随机挑，那会被体量拖住。

[分析员]
n8n 的局限同样重要。第一，平台很大，作为个人项目直接二次开发成本高。第二，节点生态强，但复杂流程一多，调试、版本管理、凭据管理和权限会变成真正工程问题。第三，source-available 许可需要认真看，不能把它当成随便嵌入商业产品的基础库。第四，对高度定制的 agent 行为，n8n 适合编排和集成，不一定适合承担所有智能决策。最佳位置是 workflow control plane，而不是唯一大脑。

[主持人]
和 OpenHands 对比，OpenHands 更像 coding agent 控制台，聚焦开发任务、多后端 agent 和自动化；n8n 更像通用业务流程编排平台，聚焦节点、触发器、集成、审批和生产运维。你不需要二选一。一个合理架构是：OpenHands 或 Codex 负责深度代码执行，n8n 负责把业务事件和工具串起来，Feishu/Daily 负责承接结果和人工决策，Graphiti 负责长期事实记忆，MarkItDown 和 Firecrawl 负责输入层。这五个仓库正好拼出一套个人 AI 工作流地图。

[分析员]
今天的落地动作可以很小：本机用 Docker 跑 n8n，建一个 webhook trigger，加一个 HTTP request 节点打到你自己的本地脚本或 GitHub API，再加一个 Feishu 或文件输出节点。先把“收到事件 -> 调工具 -> 产生日志 -> 写回结果”这条链跑通。之后再考虑模型节点、人工审批、错误重试和凭据管理。n8n 最适合通过小流程逐步长大，不适合一上来画一个巨型自动化宇宙。

[主持人]
这一期结论：n8n-io/n8n 是你理解 AI FDE 和业务自动化交付的必读仓库。它告诉你，真正的自动化不是一个 prompt，而是触发器、节点、数据、权限、审批、日志、部署和可维护性。对你的 GitHub 播客和 Feishu 项目，它最有价值的启发是把每日生产、信息雷达、招聘跟进和课程任务都抽象成可追踪 workflow。先学它的工作流思想，再决定是否把它作为实际编排平台。

[分析员]
再补一个架构观察。n8n 的 `packages/nodes-base` 很重要，因为它体现了“连接器经济”。一个平台的威力不只来自核心执行器，还来自大量可复用节点。你自己的系统也会遇到同样问题：Feishu 文档、飞书任务、GitHub、TokenDance、ffmpeg、浏览器、文件转换、知识图谱，每一个都可以是节点。如果每次都在脚本里临时写调用，短期快，长期会乱。n8n 的启发是给每个外部能力一个稳定节点接口，让 workflow 负责组合。

[主持人]
它也提醒你关注凭据和人审。AI 自动化最危险的地方，不是模型写错一句话，而是它拿着凭据执行了错误动作。n8n 的生产叙事里反复出现 self-host、RBAC、audit trails、human approvals。这些词在面试和真实交付里很有分量。比如 Feishu 自动化可以默认只生成草稿，敏感任务必须人工确认；GitHub 自动化可以先开 PR，不直接 push main；播客流水线可以先验证时长和 decode，再 commit。你现在的任务其实已经在实践这些原则。

[分析员]
如果把 n8n 放进你的个人项目包装里，可以这样讲：我不是要替代所有系统，而是用 workflow engine 把事件、工具和人连接起来。Codex 适合深度代码和文件操作，Feishu 适合承接知识和协作，Graphiti 适合长期事实记忆，MarkItDown 和 Firecrawl 适合素材摄取，n8n 适合编排可重复流程。这个表述既不夸大 n8n，也能展示你理解系统边界。对 AI FDE 来说，边界感比堆功能更重要。

[主持人]
再给一个面试表达版本。你可以说：我看 n8n 不是为了复制一个自动化平台，而是为了学习企业流程系统必须具备的元素。一个真实 AI FDE 项目至少要有触发器、数据输入、模型节点、业务系统节点、错误处理、人工审批、执行日志、凭据管理和部署方式。我的 AttendancePilot 或 GitHub 播客 demo 可以先小，但结构上要覆盖这些点。这样讲，别人会听出你不是只会做玩具 demo，而是在按交付系统思考。

[分析员]
另外，n8n 的可视化画布对沟通很有价值。很多业务方不想看代码，但能看懂“从表单触发，到读取表格，到调用模型，到发飞书消息，到等待审批”的流程图。AI FDE 经常要在技术和业务之间翻译，n8n 这类工具提供了一个共同语言。即使最终不用 n8n，你也可以借鉴它的表达方式，把自己的自动化画成节点和边，让客户、面试官、同学都能理解。

[主持人]
最后提醒一点：越是强大的编排平台，越要克制。不要把所有个人任务都塞成复杂 workflow。适合 n8n 的，是重复、有外部系统、有明确输入输出、需要日志或审批的流程。一次性的深度思考、代码重构、长文写作，仍然交给 Codex 或 Claude 更合适。懂得什么时候不用某个工具，也是工程能力的一部分。
