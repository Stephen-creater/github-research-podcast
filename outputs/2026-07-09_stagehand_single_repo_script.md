# Stagehand 单仓播客脚本

[主持人]
今天这一期只讲 `browserbase/stagehand`。它的定位是 AI Browser Automation Framework，用自然语言和代码共同控制浏览器。这个仓库对你很有现实价值，因为你的工作流里有大量“浏览器里的事实”：GitHub 页面、Feishu 文档、招聘网站、课程平台、公众号外链、AI 工具官网。纯 Playwright 代码很稳定但写起来细；纯 agent 浏览器很灵活但不够可控。Stagehand 想解决的就是这两者之间的断层。

[分析员]
README 的核心观点是：开发者应该能选择什么时候写代码，什么时候用自然语言。熟悉、稳定、重复的动作用代码；陌生、变化大、选择器不稳定的页面，用 AI。它提供 `act()` 执行动作，`agent()` 做多步任务，`extract()` 做结构化提取，并且可以 preview AI actions、cache repeatable actions、自愈页面变化。这个设计很适合生产自动化，因为它没有把所有事情都交给不确定的 agent。

[主持人]
快速开始是 `npx create-browser-app`。源码构建则是 `git clone` 后 `pnpm install`、`pnpm run build`、`pnpm run example`。示例代码里先拿 `stagehand.context.pages()[0]`，再 `page.goto("https://github.com/browserbase")`，然后 `stagehand.act("click on the stagehand repo")`，或者 `const agent = stagehand.agent(); await agent.execute("Get to the latest PR")`，最后用 `stagehand.extract("extract the author and title", z.object(...))` 拿结构化结果。它把浏览器控制、AI 行为和 zod schema 组合在一起。

[分析员]
看目录结构，`packages/core` 是核心 SDK，里面有 `examples`、`lib/inference.ts`、`lib/logger.ts`、`lib/prompt.ts`、`lib/modelUtils.ts`、`lib/v3Evaluator.ts` 等；`packages/cli` 提供命令行、daemon、skills、doctor、remote options、driver commands 等测试；`packages/evals` 提供浏览器任务评测和 CLI；`packages/docs` 是文档站。这个结构说明 Stagehand 很重视工程化评估和 CLI 入口，不只是一个 demo wrapper。

[主持人]
对你的第一个用法，是补足 Feishu 和网页操作。很多页面不能只靠抓 HTML，必须点击、筛选、滚动、登录后读取。Stagehand 可以让你把确定步骤写成代码，比如打开 URL、等待某个区域、保存截图；把不确定步骤交给自然语言，比如“找到今天最新的项目记录”“点击导出按钮”“提取这个岗位的职责和薪资”。最后用 `extract()` 输出结构化 JSON，再交给 Codex 写入 Daily。

[分析员]
第二个用法，是 GitHub 播客候选发现。你可以让 Stagehand 打开 GitHub trending、搜索 coding agents、MCP、Lark automation、TTS podcast generation 等关键词；用代码控制分页和过滤，用自然语言处理页面里不固定的卡片和描述；再用 `extract()` 抽出 repo 名、描述、stars、最近更新、文档链接。相比只用 GitHub API，它能读取页面上额外展示的信息；相比纯 browser agent，它更容易缓存和复跑。

[主持人]
第三个用法，是面试和求职流程。招聘网站、公司官网、投递系统经常结构不稳定，纯 API 不存在，手动操作又容易漏。Stagehand 的思路可以做一个半自动助手：人负责登录和确认敏感动作，脚本负责读取页面、提取岗位信息、生成 Feishu 记录、提醒下一步。这里一定要把“提交申请、发送邮件、改资料”这类动作设成人工确认，不要让 agent 自动越权。

[分析员]
设计上最值得学的是“AI 与代码分工”。很多浏览器自动化项目走两个极端：要么全靠选择器，页面一变就坏；要么全靠 agent，结果不可预测。Stagehand 的强项是让你把稳定部分锁进代码，把不稳定感知部分交给模型，再通过 caching 和 self-healing 降低重复成本。对你的自动化来说，这种分工比“让 AI 自己在浏览器里随便操作”更可维护。

[主持人]
它还有一个和你很相关的关键词：evaluation。`packages/evals` 下有评测框架、任务配置、agent model modes、rubric、cleanup 等。浏览器自动化不是跑通一次就算成功，因为页面会变、模型会变、网络会变、登录态会变。Stagehand 把 evals 放进仓库，说明它把可靠性当成产品核心。你以后做 AI FDE demo，也应该把浏览器任务的成功率、失败原因、截图证据和重试策略记录下来。

[分析员]
局限要明确。第一，Stagehand 仍然需要 LLM provider 和可能的 Browserbase credentials，生产成本要算。第二，AI action 不是确定程序，必须有日志、preview、缓存和人工确认。第三，涉及账号、支付、投递、发送消息、删除内容时，必须做人类确认。第四，页面自动化很容易被网站条款、验证码和反自动化策略限制。第五，它是 TypeScript 生态，对 Python 或本地 shell 流水线来说，需要额外桥接。

[主持人]
读源码建议按三条线走。第一，读 `packages/core/README.md` 和 examples，尤其是 `v3-agent.ts`、`targeted-extract.ts`、`mcp.ts`、`persist-logs-example.ts`、`record-video.ts`，看典型能力如何组合。第二，读 `packages/core/lib/inference.ts`、`prompt.ts`、`modelUtils.ts`，理解自然语言动作如何进入模型。第三，读 `packages/evals/README.md` 和 `framework`，看它如何定义任务、评估结果和清理浏览器状态。第四，读 CLI 测试，理解它希望用户通过命令行获得哪些稳定体验。

[分析员]
如果今天做最小实验，我建议选一个低风险页面，比如 GitHub repo 搜索结果。流程是：代码打开搜索 URL；自然语言让 Stagehand 找出前十个 repo；`extract()` 用 zod schema 输出 repo、description、stars、updated time；保存为 `work/radar/github_search_YYYY-MM-DD.json`；再由 podcast pipeline 从中选仓库。这个实验不碰账号、不提交动作，但能验证 Stagehand 的结构化浏览能力。

[主持人]
它和 browser-use、playwright-mcp 的关系也要区分。browser-use 更像通用 AI 浏览器 agent；playwright-mcp 是把 Playwright 暴露为 MCP 工具；Stagehand 更像在 Playwright 精确控制和 AI 自然语言操作之间加一层开发者友好的抽象。你如果要做可重复、可测试、可缓存的网页流程，Stagehand 值得优先研究；如果只是临时让 agent 看页面，MCP 或 browser-use 可能更快。

[分析员]
这一期结论：Stagehand 对你的意义不是“又一个浏览器自动化库”，而是一个分工模型：代码负责可预测路径，AI 负责页面理解和柔性操作，schema 负责结构化输出，evals 负责长期可靠性。它非常适合 GitHub 雷达、网页证据采集、求职页面整理和 Feishu 入库前的半自动浏览流程。

[主持人]
最后给一个落地边界：Stagehand 可以帮助你读网页、点开信息、提取结构化字段，但不应该默认代替你做高后果动作。凡是发送、购买、删除、投递、授权、改隐私设置，都应该停下来让人确认。这样它会成为可靠助手，而不是不可控的浏览器代理。对你的工作流来说，Stagehand 最适合作为“可审计的网页操作层”。

[分析员]
再补一个实际架构。你可以把 Stagehand 放在 ingestion 和 action 之间：上游由 RSSHub、GitHub 搜索、Firecrawl、Crawl4AI 提供候选 URL；Stagehand 只处理那些需要登录、点击、展开、截图、确认页面状态的来源；下游再把结构化结果送给 Feishu、播客脚本或求职项目页。这样它不会承担所有网页摄取任务，而是专门处理“静态抓取不够、纯人工太慢”的中间地带。

[主持人]
日志也要作为一等产物。每次 Stagehand 执行时，最好保存输入任务、最终 URL、关键截图、抽取 JSON、模型使用量、是否命中缓存、是否触发自愈、失败原因。这样当页面变了，你不是只知道“自动化坏了”，而是能回看它在哪里误判。对你这种日更自动化和求职跟进并行的工作流，可追溯日志会直接决定系统能不能长期维护。

[分析员]
最后再说一个学习重点：不要只看 `act()` 的神奇效果，要看它怎样把自然语言动作压回工程约束。真正的生产价值来自 schema、缓存、eval、日志、preview 和人工确认的组合。Stagehand 的名字听起来像一个会帮你点网页的助手，但它更值得学的地方，是如何让这个助手在可测试的框架里工作。
