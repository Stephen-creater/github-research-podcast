# 单仓库播客 03：ai-podcast-studio，真正的源监控到播客流水线

[主持人]
今天这一期只讲一个仓库：ai-podcast-studio。它是一个自托管 pipeline，用来监控网站、RSS 和 X 账号，筛选值得讲的内容，写成播客脚本，合成音频，再发布成 podcast feed。

[分析员]
一句话结论：这个项目最接近你最初描述的“夜间自动生成跑步播客”的完整形态。它不是文章转音频，也不是单次 TTS 工具，而是从源发现、去重、相关性评分、脚本生成、TTS、发布、失败恢复，到 dashboard 管理的一整条链路。

[主持人]
先讲它解决的问题。普通新闻摘要的问题是噪声太大；普通播客生成器的问题是没有稳定信息源；普通 TTS 工具的问题是只负责朗读。ai-podcast-studio 把这三件事串起来：你配置源，它持续抓取；到生成时间，它挑选值得讲的内容；然后写稿、合成、发布。

[分析员]
README 的流程图很清楚。第一步，watching your sources。它会按源配置的间隔轮询 RSS、网站、X 或 Nitter mirror。不同站点并行，来自同一 host 的源会控制节奏，避免 rate limit。失败太多会自动放慢，永久失败则禁用。

[主持人]
第二步是 picking what is worth covering。它不是把所有抓来的内容都讲一遍，而是把 unprocessed posts 转成 articles。长文一篇就是一篇 article；短推文会按 thread 聚合。然后用较便宜的模型给每篇内容打 0 到 10 分相关性分数，生成短摘要，也可以按 subtopic 分类。低于阈值直接丢掉。

[分析员]
第三步是写脚本。这里用了更强的模型。它会把今天的文章按 topic 分组，并和最近几期历史节目对比。新话题正常进入；旧话题如果是 follow-up，会提示模型自然承接；已经讲烂的主题会跳过。它还能搜索过去节目，避免重复，还能用 Tavily 做外部 web research。

[主持人]
第四步是录音。脚本先经过 TTS 清洗，比如去掉 TTS 容易念错的破折号，注入发音提示。长脚本会按句子切块，再把音频块拼回一个 MP3。它支持 OpenAI、ElevenLabs、Inworld。多说话人、访谈风格则主要依赖 ElevenLabs 或 Inworld。

[分析员]
第五步是发布和恢复。MP3、recap、show notes 会进入 RSS feed。feed 可以是 live HTTP endpoint，也可以导出静态 `feed.xml`，放到静态服务器、S3 或 CDN。失败时它记住失败阶段，retry 时从失败阶段继续，不重复花前面已经花过的 LLM 调用。

[主持人]
这就是这个仓库对你最重要的地方：它把“每天至少 5 期”这种需求从手工劳动变成 pipeline 问题。你不应该每天手工说“继续”，系统应该每天自动扫源、挑 5 个高相关仓库、每个仓库生成一期，不够 5 个就继续扩展源。

[分析员]
它的技术栈也值得看。后端是 Spring Boot，负责轮询源、跑 LLM pipeline、生成音频和发布。前端是 Next.js dashboard，和后端 HTTP 通信。SQLite 保存状态。音频、feed.xml 和 episode 文件在 data 目录。外部 provider 包括 OpenRouter、OpenAI、ElevenLabs、Inworld、Tavily、FTP、SoundCloud、X。

[主持人]
和你现在桌面项目相比，ai-podcast-studio 是重型版本。你的桌面项目现在做的是：选仓库、写单仓库稿、MiMo TTS 合成、commit push。它还缺：源池管理、已讲历史去重、每天 quota 管理、失败阶段恢复、feed 发布、dashboard。ai-podcast-studio 正好提供这些长期设计参考。

[分析员]
我们要拆一下它的配置思想。每个 podcast 有 topic、language、style、ttsProvider、ttsVoices、speakerNames、targetWords、cron、timezone、customInstructions、relevanceThreshold、subtopics、requireReview、maxLlmCostCents、deepDiveEnabled 等字段。这说明一个播客不是一个脚本，而是一个带策略的实体。

[主持人]
对你来说，topic 不应该写成泛泛的 AI 新闻，而应该写成“叶耀楠的项目雷达”。subtopics 可以是：Coding Agent、Feishu 自动化、知识库与阅读管线、TTS/播客生成、AI FDE 案例产品化、浏览器/Computer Use、低噪声信息源。每个 subtopic 设权重，系统就知道什么内容优先讲。

[分析员]
它也强调 review。`requireReview` 打开后，系统生成脚本先停在 pending review，不立刻花 TTS 成本。你可以读、改、丢弃，再批准生成音频。这个设计对你很现实：每天自动生成 5 期不能变成每天自动制造 5 段垃圾音频。最少要先能控制主题和质量。

[主持人]
不过你现在说的是“每天至少更新 5 个播客”，我会把第一版自动化理解成：每天自动生成 5 个单仓库音频，并 commit push。不是每天生成一个五仓合集。ai-podcast-studio 给我们的启发是加 quota 和 history：当天已有几期、哪些仓库讲过、哪些候选还没讲。

[分析员]
这个仓库的局限也很明确。第一，它重，需要 Java、Spring Boot、Next.js、SQLite、provider key。第二，它默认 TTS provider 是 OpenAI、ElevenLabs 或 Inworld，不是你现在接的词元跳动 MiMo。第三，Twitter/X 源可能有 API 成本和可用性问题。第四，它是新闻/信息源 pipeline，不是专门为“GitHub 仓库深度解读”写的，需要你改 prompt 和 source filter。

[主持人]
如果要落地到你的项目，我建议不要直接部署它，而是把它拆成四个功能借用。第一，每日 quota 管理：每天至少 5 期。第二，历史去重：讲过的仓库短期不重复。第三，source scoring：候选仓库必须有 fit 分数。第四，失败恢复：脚本已生成但音频失败时，不要重写稿，直接重合成。

[分析员]
你目前的桌面项目可以马上吸收这些规则。比如增加 `outputs/daily/2026-07-05.md`，记录今天生成了哪 5 期；每个 episode 有 repo、commit、script、audio、duration、status；自动化每天启动时先看当天已完成几期，少于 5 就继续生成。

[主持人]
我们把这个仓库再往你自己的系统里翻译一下。ai-podcast-studio 里面最核心的抽象，是把“播客”当成一个长期运行的生产体，而不是一次性生成任务。它会有主题、有信息源、有声音、有成本上限、有审稿策略、有发布时间。你现在的 GitHub 播客也应该这样看：它不是今天临时生成几个 MP3，而是一个每天醒来都能自己生产的私人技术雷达。

[分析员]
如果照这个仓库的思路，你的系统至少需要五张表，哪怕第一版只是 Markdown 或 JSON。第一张是 source pool，记录从哪里找仓库，比如 GitHub Trending、关键词搜索、你关注的组织、你之前做过的项目相关仓库。第二张是 candidate queue，记录今天候选仓库和 fit 分数。第三张是 episode history，记录哪些仓库已经讲过。第四张是 generation state，记录脚本、音频、验证各阶段状态。第五张是 daily quota，记录今天是否已经满 5 期。

[主持人]
这五张表不用一开始就上数据库。feishu-pm-kit 那一期会讲到，Markdown manifest 也可以做事实源。关键是要从“我让 AI 继续”变成“系统知道差几期”。比如今天 5 期里，gitingest 已完成，Audicle 正在合成，ai-podcast-studio 待合成，feishu-claude-code 待合成，feishu-pm-kit 待合成。自动化下次启动时不应该重头来，而是只补没完成的部分。

[分析员]
ai-podcast-studio 的 retry 思路就很适合这个。它记录失败阶段，避免重复花费。对你来说尤其重要，因为 TTS 是真实成本，LLM 也是成本。如果脚本已经写好，音频失败，就只重跑音频；如果音频已经通过，commit push 失败，就只重跑同步；如果仓库已经讲过，不要隔天重复生成同一个仓库，除非仓库有重大更新。

[主持人]
再讲 relevance scoring。你不需要泛泛抓“AI 热门项目”，因为那会产生很多热闹但无用的内容。你的 fit 规则应该很具体：第一，能不能帮助你把 Codex 或 Claude Code 用得更像生产系统。第二，能不能接进 Feishu、知识库、文章管理或 Daily。第三，能不能帮助你做 AI FDE、案例包装、面试作品。第四，能不能降低信息噪声，转成可听、可执行、可复盘的资产。

[分析员]
这会改变选仓库的质量。比如一个 50k star 的前端 UI 库，如果和你当前项目没有关系，就不该优先讲。反过来，一个只有几百 star 的 Feishu 自动化工具，如果能让你把知识库变成执行入口，它就很值得讲。ai-podcast-studio 的分数机制提醒我们：热度只是一个信号，个人适配度才是核心。

[主持人]
这个仓库还有一个很现实的思想：成本闸门。它有 `maxLlmCostCents` 这类配置，意思是每期成本不能无限膨胀。你现在也要有成本意识。每天 5 期，如果每期都长到 40 分钟，TTS 成本和时间都会上去。更合理的是默认 12 到 20 分钟，只有特别重要的仓库才拉长到 30 分钟以上。

[分析员]
所以“10 到 40 分钟”不是让每期都堆满 40 分钟，而是给一个听觉上的有效区间。低于 10 分钟，往往只够介绍，学不到东西；高于 40 分钟，跑步时信息密度容易下降，也更容易生成废话。ai-podcast-studio 的 targetWords 思路可以迁移过来：每期有目标字数和目标结构，不是随缘写。

[主持人]
你最开始提到那个播客里说，B 站或 YouTube 很多二三十分钟讲解信息量很低。ai-podcast-studio 能解决一半：它能稳定生产和分发。但另一半要靠 prompt 和评审解决：每期必须讲清楚“这个仓库解决什么问题、怎么运行、架构怎么分层、关键设计为什么这么做、缺点是什么、怎么和我的项目结合”。少一个都不算合格。

[分析员]
这也是为什么我会把今天的任务改成每个仓库一集，而不是五六个仓库做合集。合集适合资讯浏览，不适合真正学习。单仓库节目才有空间讲代码结构、数据流、失败场景和迁移建议。ai-podcast-studio 本身也在强调 topic continuity，而不是把当天所有东西硬塞在一起。

[主持人]
如果未来你想把这个系统做成作品，ai-podcast-studio 可以作为对标对象，但你的差异点要明确。它偏新闻源监控和 podcast feed，你的版本偏个人上下文和仓库深度解读。也就是说，普通系统问“今天有什么新闻”；你的系统问“今天有哪些仓库能改变我的工作流”。这是产品定位上的差别。

[分析员]
落地路线可以这样排。第一，今天先补齐 5 个单仓库音频。第二，自动化改成每天至少 5 期。第三，增加每日 index 和历史记录。第四，把候选仓库选择从固定列表升级成搜索和评分。第五，再接 RSS 或 Feishu 回传。第六，才考虑 dashboard。不要一上来就做漂亮界面，先把生产闭环跑稳。

[主持人]
还有一个点，ai-podcast-studio 支持 `requireReview`，但你现在要求“持续运行，每天至少 5 个”。这两者有冲突：完全自动化会提高产量，但会降低质量控制。我的建议是第一阶段先自动生成并同步，同时 daily index 里标记“未人工听完”。等你发现哪类内容质量差，再把那一类切成先审稿后合成。

[分析员]
这是一种可进化的自动化，而不是一次性赌对。自动化系统最怕的不是第一版简陋，而是没有反馈入口。每天 5 期跑起来以后，你只要在 Feishu 或 daily index 里标记“好、一般、废”，下一轮候选选择和脚本提示就能改进。

[主持人]
这期总结：ai-podcast-studio 解决的是“持续监控信息源，并按主题生成可订阅播客”的问题。它的关键设计是源轮询、去重、相关性评分、脚本写作、TTS 切块、RSS 发布、失败阶段恢复和成本控制。对你来说，它是每天 5 期系统的架构参考，不是马上替换当前桌面脚本的工具。

[分析员]
下一步动作：把你的自动化从“每 6 小时看一看”改成“每天生成至少 5 个单仓库 episode”。同时引入 daily index 和历史去重。这样才符合你刚才说的持续运行。

[主持人]
今天这期只讲 ai-podcast-studio，到这里结束。
