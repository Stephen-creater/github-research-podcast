# 单仓库播客 05：RSSHub，把全网内容变成可订阅的信息源

[主持人]
今天这一期只讲一个仓库：`DIYgod/RSSHub`。它的口号是 Everything is RSSible。对你的个人 GitHub 播客系统来说，RSSHub 的价值不是“再多一个 RSS 工具”，而是它展示了一个超大规模信息路由网络怎么组织：路由、缓存、渲染、部署、社区贡献、Playwright 抓取、Redis、Docker、Worker，多种内容源被统一输出成 feed。这正好对应你想做的“GitHub Trending、公众号、Bilibili、课程、Feishu 前哨站，最后变成个人可听内容”的方向。

[分析员]
先讲它解决的问题。很多网站没有 RSS，或者 RSS 不完整；RSSHub 用开源路由把各种网页、平台、API 重新包装成 RSS/Atom/JSON 等 feed。README 说它由超过 5000 个全球实例组成，每月服务大量请求，并且和 Folo 这种现代 RSS 阅读器配合。它不是一个小脚本，而是一个社区维护的信息基础设施。你的信息雷达如果只靠手工打开网页，就永远不稳定；如果能把来源变成 feed，后面的筛选、脚本、TTS 才能自动化。

[主持人]
怎么部署？README 指向 docs，但仓库里已经能看到 `docker-compose.yml`。标准服务包含 `rsshub`、`redis`，以及可选的 `browserless`。`rsshub` 暴露 1200 端口，`CACHE_TYPE=redis`，`REDIS_URL=redis://redis:6379/`。如果启用需要浏览器的路由，可以通过 `PLAYWRIGHT_WS_ENDPOINT` 接到 browserless。最小体验可以用公共实例或 Docker；正式自用则建议自托管，避免公共实例限制和稳定性问题。

[分析员]
看代码结构。核心在 `lib/`。`lib/index.ts`、`server.ts`、`app.ts` 是服务入口；`lib/routes/` 是路由体系；`lib/registry.ts` 管路由注册；`lib/middleware/` 里有 cache、debug、header、parameter、template、trace、sentry、honeybadger 等中间件；`lib/utils/` 里有 got、ofetch、playwright、wechat-mp、parse-date、rss-parser 等工具；`lib/views/` 负责 rss、atom、json 等输出。它不是单纯爬虫集合，而是一套路由框架。

[主持人]
一个关键设计是“路由即插件”。每个内容源通过路由接入，统一走参数、缓存、抓取、解析、渲染。对你来说，这启发很大：你的 GitHub 播客候选也可以路由化。比如 `/github/trending/ai-agents`、`/github/search/feishu`、`/feishu/daily/links`、`/wechat/saved/articles`，每个 route 输出候选条目，后面统一打分、去重、写脚本。这样系统不会变成一个越来越长的 if else。

[分析员]
第二个设计是缓存。RSSHub 的 docker-compose 直接把 Redis 放进标准服务，说明内容抓取不能每次都打源站。你的播客自动化也是一样：每天至少 5 期不代表每 6 小时都重新抓全网。候选仓库、README、stars、commit、release、脚本和音频都应该有缓存和复用规则。今天已经完成的集数要保留，只补缺口，这就是同一种思想在播客生产里的体现。

[主持人]
第三个设计是浏览器抓取作为补充。RSSHub 依赖里有 Playwright 或 Patchright 相关内容，docker-compose 里有 browserless。这说明它承认有些网页不能只靠 HTTP 请求解析，需要真实浏览器。但它没有把所有抓取都浏览器化，而是按路由需要启用。你的系统也应该这样：GitHub API 能解决就不用浏览器；动态网页必须浏览器时再调用 browser-use 或 Playwright MCP。

[分析员]
RSSHub 和你的 Feishu/Daily 系统也很贴。你现在有很多信息入口：GitHub Trending、AI 产品训练营、公众号、Bilibili、YouTube、课程录播、飞书剪存。RSSHub 的方法论是：先把来源统一成 feed，再用阅读器或下游系统消费。你可以把“每日播客候选”也定义成 feed：每条 item 是一个仓库或文章，带来源、时间、fit role、摘要、去重 key 和状态。这样 Feishu 只是一个展示和沉淀层，不是所有自动化的唯一源头。

[主持人]
局限也必须讲。RSSHub 是 AGPL-3.0，产品化时要注意许可证义务。它的路由数量多，维护成本也高；源站页面一改，路由就可能坏。公共实例的稳定性、速率、隐私都不能完全依赖。自托管虽然可控，但要处理 Redis、浏览器、部署、日志和更新。对个人系统来说，应该先用它的思路和部分路线，而不是一上来维护一整套大型实例。

[分析员]
如果要把它接到你的 GitHub 播客，建议先做一个很小的“信息源层”。第一，定义候选 item JSON：`source`、`url`、`repo`、`title`、`reason`、`seen_at`、`status`。第二，从 GitHub API、RSSHub feed、Feishu 手动剪存三类来源收集候选。第三，统一去重和打分。第四，只有进入 top candidates 的仓库才 clone 和写脚本。RSSHub 的路由思想能让这个输入层持续扩展，而不是每加一个来源就重写主流程。

[主持人]
这一期结论：RSSHub 是你的“信息雷达基础设施参考”。它不负责写播客，也不负责理解仓库，但它告诉你怎样把杂乱来源变成稳定、可订阅、可缓存、可扩展的输入网络。对一个每天要生产 5 期高贴合 GitHub 仓库播客的系统来说，输入层质量决定后面所有内容质量。RSSHub 值得被认真研究，不是为了复制它的 5000 个路由，而是为了学习它如何把互联网变成结构化信息流。

[分析员]
再把它映射到你的个人系统。你现在的 Feishu/Daily 更像知识沉淀层，适合写判断、计划、复盘和链接；RSSHub 代表的是信息采集层，适合把外部变化标准化成 feed；GitHub 播客 pipeline 则是内容生产层，负责把高价值候选变成脚本和音频。这三层如果混在一起，就会出现一个问题：Feishu 页面既当 inbox、又当数据库、又当任务队列，最后自动化很难判断状态。

[主持人]
所以更清楚的做法是：RSSHub 或类似 feed 工具负责“有什么新东西”；本地 JSON 或 selected repos 文件负责“今天选什么”；daily index 负责“哪些已经做完”；Feishu 负责“我听完后沉淀什么”。这个职责划分能让系统更耐用。RSSHub 的路由体系之所以能扩展，就是因为输入、处理、输出有边界。

[分析员]
RSSHub 还有一个对内容质量很重要的点：它天然鼓励订阅，而不是刷流。订阅意味着你可以长期跟踪固定源，比较变化，建立历史；刷流则更容易被热点牵着走。你的 GitHub 播客如果想长期有个人价值，也应该形成一组稳定主题源：coding agents、Feishu/Lark、知识管理、repo ingestion、TTS/podcast、browser automation、AI FDE。每天从这些源里挑，而不是随机追热榜。

[主持人]
它也适合和 RSSHub Radar 一起看。README 里相关项目提到 RSSHub Radar，可以在浏览器里发现当前网站的 RSS 或 RSSHub 路由。对你来说，这很像“候选发现助手”：当你看到一个有价值网站、课程页、公众号镜像、项目博客时，不要只复制链接到 Feishu，还要问能不能订阅。能订阅，就能进入自动化；不能订阅，才考虑浏览器抓取或手工剪存。

[分析员]
最后给一个保守落地建议：先不要自托管完整 RSSHub。你可以先用它作为研究对象和路线库，挑少数和你强相关的来源做小规模 feed 输入。等你确认这些 feed 确实能提高每日播客选题质量，再考虑 Docker + Redis + browserless 的完整部署。这样成本和收益匹配，也不会因为维护基础设施拖慢内容生产。

[主持人]
再补一个和“每日 5 期”直接相关的设计。RSSHub 的 feed 思维可以帮你避免选题枯竭。每天 5 个仓库不是每天临时搜索 5 个，而是维护一个持续流入的候选池。每个候选池条目有生命周期：new、shortlisted、scripted、audio_done、verified、published、skipped。RSSHub 负责让 new 源源不断，daily index 负责记录 published，selected repos 负责保留 shortlisted 和 fit 判断。

[分析员]
这个生命周期还能避免重复劳动。比如昨天已经做过 gitingest、Audicle、ai-podcast-studio、feishu-claude-code、feishu-pm-kit，今天就不应该再把它们当新集，除非有重大更新。RSSHub 式输入层加上本地状态，可以让系统知道“见过”和“做过”的区别。见过但没做，可以继续候选；做过且验证通过，就进入历史库。

[主持人]
它也能提升个性化。普通 RSS 是按来源订阅，你的系统可以按主题订阅：coding agents、browser automation、Feishu/Lark、TTS、knowledge management、repo ingestion。每个主题都有自己的候选路线和权重。这样每日播客不是泛技术新闻，而是和你的 Codex、Feishu、Daily、AI FDE 项目持续对齐的学习材料。

[分析员]
最后要注意，RSSHub 强的是输入标准化，不是价值判断。真正的价值判断仍然要来自你的当前项目：这个仓库能不能接进工作流？能不能成为面试案例？能不能改善知识管理？能不能节省重复劳动？所以 RSSHub 在你的系统里应该负责“把更多可能性送到门口”，而不是替你决定今天讲什么。
