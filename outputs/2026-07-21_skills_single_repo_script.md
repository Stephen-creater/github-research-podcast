# humanlayer/skills：把周期性 Agent 任务变成可测量的控制回路

[主持人]
今天只聊一个仓库，`humanlayer/skills`。它不是一个大而全的 Agent 运行时，也不是要替代 Codex、Claude Code 或 GitHub Actions。它更像一组可以学习的技能模板，尤其是里面的 `build-iterated-agentic-loop` 和 `design-control-loop`，在回答一个很现实的问题：当一个 Agent 任务不是跑一次，而是每天、每周、每几个小时重复执行时，怎样让它可测量、可复盘、可被人类稳定调参？

我先把结论放前面：这期推荐是“先研究，不直接安装”。原因很简单，仓库本身很有启发，但它偏 Claude Code 和 HumanLayer 的生态，安装路径还有一个公开 issue 提到可能装到同名的别处技能。所以今天更适合把它当作设计参考，而不是马上复制它的工作流。我们真正要拿走的是一个模型：设定目标，测量当前状态，选择一个小步改动，让 Agent 执行，然后把人的反馈写回下一轮。

[分析员]
对，这个仓库在 pinned commit `39fb32786ae7a7cd864cf2c237148c38b1e4db07` 下非常小，但结构清楚。根目录 README 说它提供 HumanLayer 的 Claude Code skills，安装形式是 `npx skills add humanlayer/skills --skill SKILLNAME`，然后在项目里用对应的 slash command。公开列出的技能有四个：`improve-claude-md`、`narrow-react-prop-types`、`build-iterated-agentic-loop` 和 `design-control-loop`。

前两个是具体任务技能，后两个才是今天的重点。`build-iterated-agentic-loop` 的目标是帮一个项目生成 repo-local skill、GitHub Actions workflow、prompt、memory file，以及可选的参考模板。换句话说，它关心的不是“让 Agent 写一次代码”，而是“把一个反复发生的 Agent 任务变成一个有边界的自动化”。`design-control-loop` 又往前走了一步，它要求先和用户一起设计控制回路：set point、sensor、controller、actuator、disturbance、dampener，这些词听上去偏工程控制论，但放进 Agent 工作流里很实用。

所谓 set point，就是你希望仓库达到的状态。sensor 是测量当前状态的方法，可能是 lint、类型检查、结构搜索、测试、遥测查询，或者自定义脚本。controller 是根据测量结果决定这一轮做什么，以及做多大。actuator 才是具体改代码的 Agent，加上 repo-local skill 和验证命令。disturbance 是外部干扰，比如团队其他人合代码、依赖升级、生成代码变化、测试偶发失败。dampener 则是可选的防退化门禁，防止问题在循环修复期间继续变糟。

[主持人]
这和我们当前的最近项目很贴。比如这个 GitHub research podcast 自动化，本身就是一个周期性 Agent loop。它每六小时跑一次，但每天最多只能产出一个完整仓库节目。一个完整 bundle 不是只有报告，还要有报告、两人脚本、可解码的 m4a 音频、daily research index、daily episode index，而且 GitHub main 要同步，链接和 secret scan 也要过。

如果用 `humanlayer/skills` 的语言来描述，set point 就是“本地自然日内恰好有一个完整、验证通过、已发布的单仓研究播客 bundle”。sensor 不是一句“看起来完成了”，而是一组确定检查：今天有没有 report，有没有 `[主持人]` 和 `[分析员]` 格式的 script，音频能不能 `ffmpeg` 解码，两个 index 有没有对应条目，`validate_report.py` 和 `github_podcast_pipeline.py verify` 有没有通过，`HEAD` 和 `origin/main` 是否一致，工作区有没有非预期改动。

[分析员]
controller 就是决定下一步状态：如果完整 bundle 已经存在且验证通过，就 no-op；如果 report 有了但 script 或 audio 缺失，就从缺失阶段恢复；如果今天完全没有 bundle，就选择一个新仓库、研究、写报告、写脚本、合成音频、验证、更新索引、提交、推送。这里最关键的是 controller 不应该被星标数牵着走，它要按项目契合度、可复用设计、证据成熟度、新颖性和近期活跃度打分。这个逻辑其实已经写在当前自动化要求里，而 `design-control-loop` 给了它一个更清晰的系统名字。

actuator 则是 Codex 当前这条自动化本身：读取上下文、研究 public GitHub primary sources、写文件、跑验证、提交推送。它不是一定要换成 Claude Code 或 CodeLayer。相反，报告里明确说不该复制 HumanLayer 的 Claude-only runner 或 GitHub Actions 模板，因为当前项目运行在 Codex desktop，有本地 TTS keychain 路径和特定的发布约束。可复用的是设计，不是运行时。

[主持人]
那它对近期项目的具体帮助，最小试验应该怎么做？

我觉得最小试验不是“现在安装 humanlayer/skills”，而是先给当前 podcast automation 写一份内部控制回路设计笔记。用六个标题就够：set point、sensor、controller、actuator、disturbance、dampener。然后把最重复、最容易出错的那块，也就是“今天 bundle 是否完整并可验证”，提成一个本地脚本，让它输出结构化 measurement。比如输出 today、report_path、script_path、audio_path、report_valid、episode_valid、indexes_updated、git_synced、status。这样下一轮 Agent 不需要重新用自然语言猜状态，而是先读 measurement。

[分析员]
对，而且这个仓库还提醒了两个很实际的防失控点。第一，组件要先能本地单独运行，再接进 CI 或调度器。sensor 能单独跑，controller 能对 sensor 输出做选择，actuator 能对一个选择目标完成验证。这样出错时知道是哪一层坏了，而不是所有逻辑混在一个长 prompt 里。

第二，flow control 要明确。`workflow-template.yml` 的一个强设计是：计划任务如果发现这个 loop 已经有一个打开的 PR，就直接 no-op。对于当前项目，等价规则是“同一个本地日期不要产出第二个 completed repository episode”。这比单纯依赖调度频率安全，因为调度频率只是触发次数，flow control 才是业务边界。

第三，memory 不是日志。`memory-template.md` 的意思是，把长期有效的偏好和已知 false positive 写进去，比如“如果 TTS 失败，保留 report 和 script，下次只重试 audio；不要声称完成”；或者“候选仓库必须服务最近项目问题，raw stars 不能压过项目契合度”。但不要把每次运行的完整日志、临时错误、或者原始私密路径塞进去。这个边界对现在的自动化很重要，因为它同时处理公开报告和私有项目背景。

[主持人]
仓库本身的成熟度怎么样？能不能放心作为依赖？

[分析员]
按这次 inspection，它更适合当设计参考。GitHub API 显示这个仓库创建于 2026 年 3 月，pushed at 是 2026 年 6 月 30 日，检查时有 94 stars、4 forks、1 个 open issue、没有 open pull requests，也没有 releases。License 是 MIT。这个信号说明它不是无人维护，但也不是成熟基础设施。更重要的是，唯一 open issue 正好说 README 的安装指令在某些情况下会装到另一个同名 skill。这不影响我们读源码和模板，但会影响“直接安装”的建议。

所以不该复制的部分包括：不要照搬 `npx skills add`，不要照搬 HumanLayer 的 CodeLayer runner，不要照搬默认 GitHub Actions 里的 Bun/Node/Claude secret 假设，也不要把这个仓库当成调度、队列、密钥管理或观测系统。它没有提供这些。它提供的是一种把 Agent 工作流拆成可观察组件的写法。

[主持人]
我总结一下：`humanlayer/skills` 对我们最有价值的不是一个新工具，而是一套问法。这个循环到底要把什么指标推向什么目标？现在如何测量？本轮选哪个最小动作？谁来执行？怎么验证？人的反馈如何影响下一轮？什么情况下要 no-op？

如果把这套问法套回最近项目，GitHub 播客自动化可以先把“完整 bundle gate”脚本化；Feishu 或 AI-video 相关自动化也可以用同样结构，把“素材齐不齐”“输出有没有通过视觉/节奏检查”“是否需要用户接管登录授权”变成 sensor，而不是藏在长对话里。

[分析员]
最后给出和报告一致的建议：**Study only / 先研究，不直接安装**。现在值得复用的是 sensor-controller-actuator 模型、本地先验证每个组件、把 reviewer feedback 写成 durable memory、用 `/iterate` 或类似机制调整同一个工作单元、以及用 flow control 防止计划任务超过人的审核能力。等当前项目有一个稳定的 measurement 脚本后，再考虑是否把它升级成 repo-local skill 或 CI workflow。
