# 单仓库播客 01：Morning-news-podcast，把每日新闻做成可听的 Android 简报

[主持人]
今天这一期只讲一个仓库：`niuz3199-collab/Morning-news-podcast`。它不是泛泛的新闻聚合，也不是一个只有 README 的概念项目，而是一个 Android 原生应用：抓取多源新闻，用大模型写播报稿，再用 TTS 合成音频，最后在手机里播放。对你的“GitHub 播客雷达”来说，它的价值在于提供了一个端侧新闻音频产品的完整样板：新闻源、文稿生成、TTS、播放器、定时任务、日志排查，全都在一个可运行应用里。

[分析员]
先讲它解决的问题。很多新闻工具只解决“看见更多信息”，但这个仓库想解决的是“每天早上能听完一份简报”。README 里明确写了多源新闻聚合、AI 文稿生成、MiMo TTS、来源审计、WorkManager 定时生成、ExoPlayer 播放，以及失败日志。换句话说，它不是 RSSHub 这种通用 feed 基础设施，而是把信息采集到收听体验这条链路收拢成移动端产品。你现在做的 GitHub 仓库播客，本质也是类似链路：候选源、筛选、脚本、TTS、音频、索引和验收。

[主持人]
怎么运行？它是 Kotlin + Jetpack Compose 项目。环境要求是 Android Studio、JDK 11 以上、Android SDK 35，最低支持 Android 8。最小路径是克隆仓库后运行 `./gradlew assembleDebug`，或者直接用 Android Studio 打开并 Run。启动后去设置页配置 LLM 和 TTS：LLM 支持 DeepSeek、阶跃星辰 Step Plan，以及 OpenAI 兼容协议；TTS 支持小米 MiMo 或兼容的 chat-completions TTS。World News API 是可选项，用来补国际新闻。

[分析员]
代码结构很清楚。入口在 `app/src/main/java/com/morningnewspodcast/MainActivity.kt` 和 `MorningNewsApplication.kt`。数据模型在 `data/model`，比如 `NewsItem`、`NewsSource`、`BroadcastScript`、`BroadcastAudio`、`BroadcastConfig`。本地持久化在 `data/local`，用 Room DAO 管新闻、脚本、音频和配置。远程服务在 `data/remote`，包括 `NewsRssService`、`DeepSeekApiService`、`MiMoTtsService`、`WorldNewsApiClient`。业务编排在 `domain/usecase`，主要是 `FetchDailyNewsUseCase`、`GenerateBroadcastUseCase` 和 `GetBroadcastsUseCase`。

[主持人]
从架构角度看，它的分层是典型 Android Clean-ish 架构：UI 不直接抓新闻，也不直接调 TTS；UI 找 ViewModel，ViewModel 找 use case，use case 再走 repository 和 remote/local。比如生成一条播报，不应该是按钮点击后直接拼 HTTP 请求，而是经过 `GenerateBroadcastUseCase`：拿配置，拿新闻，调用 LLM 生成脚本，调用 TTS 生成音频，写数据库，最后让播放器读本地音频。这个分层对你以后做桌面版或 Feishu 控制版也有启发：不要把“发现仓库、写稿、合成、校验、入索引”揉在一个巨大函数里。

[分析员]
它一个关键设计是“失败可排查”。README 提到生成失败时可以看 `/sdcard/Android/data/com.morningnewspodcast/files/broadcast.log`，并且日志会记录 LLM/TTS 调用过程、HTTP 状态码、响应体和异常堆栈。对自动化播客来说，这一点非常重要。你现在的流水线也应该保留每集的失败原因：是没有 TTS key，是 API 超时，是脚本太短，还是 ffmpeg 解码失败。只有能排查，日更系统才不会变成黑盒。

[主持人]
再讲它和你当前项目的贴合点。第一，它直接用了 MiMo TTS 思路，和你现在的 TokenDance MiMo 音频路径同类。第二，它把新闻抓取和音频播放放在 Android 端，这给你一个后续方向：如果 GitHub 播客要从“文件夹里的 m4a”变成真正随身听，可以做一个极简移动端或 podcast feed，而不是每次手动找文件。第三，它强调“每天早上”，这和你自动化里“每天至少 5 个单仓库 episode”的 quota 思维一致。

[分析员]
局限也要讲清楚。它是 Android 应用，不是服务端 pipeline；如果你要在 Mac 上每天自动生产 GitHub 仓库播客，不能直接复用它的 UI 层。它的新闻源面向一般新闻，不是 GitHub repo discovery；如果要迁移，需要把 `NewsItem` 换成 `RepositoryCandidate`，把 RSS/World News 换成 GitHub 搜索、Trending、你的 Feishu 前哨站和 Daily。还有一点，API key 在移动端配置时要更小心，正式产品要考虑本地加密、同步、备份和泄露风险。

[主持人]
如果今天听完只做一个动作，我建议把这个仓库当作“端侧收听体验参考”，不要当作你的主 pipeline。你的主 pipeline 仍然应该在 Mac/Codex 里跑：发现仓库、克隆到 `work/repos`、写脚本、MiMo 合成、ffprobe/ffmpeg 验收、写 daily index、commit push。Morning-news-podcast 给你的，是播放端、日志端、定时端和移动端用户体验的实现参考。它提醒我们：播客自动化的最后一公里不是生成音频，而是让用户每天能稳定、可追溯、低摩擦地听完。

[分析员]
我们再把它拆成一个可以迁移的产品流程。第一步是信息源管理。这个项目里新闻源不是临时 URL，而是有 `NewsSource` 模型和来源筛选，这意味着用户可以追踪一条新闻从哪里来。你的 GitHub 播客也应该这样：每个候选仓库都要保留来源，比如 GitHub 搜索、Trending、Feishu 剪存、朋友推荐、某篇文章提到。没有来源字段，后面就很难复盘为什么选了这个仓库。

[主持人]
第二步是脚本生成和音频生成分开。Morning-news-podcast 里有 `BroadcastScript` 和 `BroadcastAudio` 两类模型，这个分离很重要。脚本成功但 TTS 失败时，不应该重新抓新闻、重新写稿；只需要重试音频。你当前自动化 prompt 也写了同样的要求：如果脚本存在但 audio failed，就 retry audio only。这个仓库从移动端产品角度证明了这个拆分是合理的。

[分析员]
第三步是播放和文稿并存。很多音频产品只给一个播放按钮，但这个项目有文稿查看。对你的仓库播客来说，文稿不是副产品，而是知识库资产。你可以把 `.m4a` 当作运动时消费，把 `.md` 脚本当作 Feishu/Daily 可检索材料。未来回看某个仓库，不一定重听 15 分钟，而是直接搜脚本里的入口文件、限制和适配建议。

[主持人]
第四步是后台定时。Android 端用 WorkManager，是因为移动系统会杀后台，任务要遵守电量和系统调度。Mac/Codex 这边虽然不是 WorkManager，但思想一样：定时不是简单 cron 一下，而是要有“今天是否已完成、完成几期、哪些已验证、哪些失败待重试”的状态。日索引就是你的 WorkManager 状态表。

[分析员]
最后再提醒一个现实限制：它的配置集中在 App 设置页，适合个人手机使用；但如果你把这个思路迁移到自己的生产系统，配置应该进入安全的本机环境或 Keychain，而不是写进仓库。尤其是 TTS key、LLM key、World News API key。这个仓库给了功能路线，真正上线时还要补更严格的 secret 管理和提交前扫描。

[主持人]
还有一个值得借鉴的细节是“来源审计”。新闻简报很容易变成模型编出来的一段顺口稿，但这个项目强调新闻列表按来源筛选、查看每个源的出稿数量。对 GitHub 仓库播客也一样：一期节目里所有判断都应该能回到仓库证据，比如 README、package、入口文件、测试、Dockerfile、release 或 issue。以后脚本可以固定加一段“本期证据来自哪里”，这样听起来不是空泛评价，而是有出处的技术讲解。

[分析员]
如果把 Morning-news-podcast 改造成 GitHub 版本，大致会有四个模型替换。`NewsItem` 替换成 `RepoItem`，字段包括 owner、repo、url、stars、updated_at、topics、fit_reason。`BroadcastScript` 继续保留，但 prompt 从新闻播报变成仓库讲解。`BroadcastAudio` 继续保留，用来记录 `.m4a` 路径、duration、decode status。`BroadcastConfig` 则增加每日目标、主题白名单和 TTS provider。这个迁移不难，关键是别把 Android UI 和后台生产逻辑绑死。

[主持人]
它也提醒你，播客不是只有生产端，还有消费端。现在你的输出都在 `outputs/`，这对自动化验证没问题，但长期听的时候会需要排序、播放进度、文稿搜索、收藏和回听。Morning-news-podcast 用 ExoPlayer 和本地数据库解决了这些问题。你未必马上写 Android App，但可以先生成一个简单 RSS feed 或网页索引，让手机播客客户端能订阅这些 m4a。那时这个仓库的播放层设计就会更有参考价值。
