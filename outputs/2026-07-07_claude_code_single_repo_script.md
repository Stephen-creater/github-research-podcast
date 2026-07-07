# 2026-07-07 单仓库播客脚本：anthropics/claude-code

[主持人]
这一集只讲 `anthropics/claude-code`。从 README 看，它是 Anthropic 的终端 agentic coding tool：进入项目目录运行 `claude`，它能理解代码库，解释代码，执行常规任务，处理 git 工作流，也能通过 GitHub 的 `@claude` 进入协作流程。对你最有价值的部分，是仓库里的官方插件示例，因为它把“一个 coding agent 怎样被工作流扩展”讲得很具体。

[分析员]
先讲使用路径。README 已经提醒，npm 安装已被标记为 deprecated，推荐 Mac 和 Linux 用 `curl -fsSL https://claude.ai/install.sh | bash`，也可以 `brew install --cask claude-code`。Windows 用 PowerShell 安装脚本或 Winget。安装后进入项目目录运行 `claude`。这和 Codex 的定位接近，但 Claude Code 仓库更像一个产品外壳加插件市场样板，而不是完整核心源码展开。

[主持人]
仓库里最值得读的是 `plugins/README.md`。它定义了 Claude Code 插件的概念：插件可以包含 slash commands、specialized agents、hooks、MCP servers、skills。标准结构是 `.claude-plugin/plugin.json` 放元数据，`commands/` 放命令，`agents/` 放专用 agent，`skills/` 放技能，`hooks/` 放事件处理，`.mcp.json` 放外部工具配置，README 放文档。这个结构对你做个人自动化非常实用。

[分析员]
举几个插件。`feature-dev` 是七阶段功能开发：发现需求、探索代码、澄清问题、架构设计、实现、质量审查、交付。`plugin-dev` 是八阶段插件开发：发现、组件规划、详细设计、结构创建、组件实现、验证、测试、文档。`code-review` 用多个专门 agent 做 PR 审查。`security-guidance` 用 hook 在编辑文件时提醒安全风险。这些不是抽象概念，而是把“好工程流程”打包成可复用命令。

[主持人]
对你当前的 Feishu 和 Daily 系统，Claude Code 插件体系的启发很直接。你现在经常有一类重复任务：把 Feishu 剪存页面归档，把课程材料压缩成复习包，把 GitHub 仓库做成播客，把面试项目包装成案例。每个任务都可以有三种组件：一个 slash command 触发流程，一个 skill 记录领域规则，一个 hook 或检查器防止越界，比如不要泄露 key，不要把第三方源码 commit 进你的私仓。

[分析员]
如果要运行或学习这个仓库，建议按三条线读。第一条是 `README.md`，确认安装和数据使用边界。第二条是 `plugins/README.md`，理解插件总结构。第三条是挑一个插件深读，比如 `plugins/feature-dev/README.md`，看它如何把“先理解代码再动手”变成流程。不要一开始就追所有脚本，仓库里还有 issue 管理脚本、MDM 示例、gateway 示例，容易分散。

[主持人]
它的关键设计决策是：把 agent 能力拆成可组合的工作流单元。命令负责把用户意图变成流程入口；agent 负责专门视角，比如探索代码、设计架构、审查质量；skill 负责长期规则和知识；hook 负责在关键事件上插入约束。这个模型比单个巨型 prompt 更稳，因为每个组件都有触发条件、文件位置和职责边界。

[分析员]
局限也明显。第一，这个仓库不是 Claude Code 完整内部实现，很多核心能力仍在产品本身。第二，插件示例是官方风格，不等于你应该把所有任务都插件化；短任务用普通脚本更快。第三，自动化越接近文件编辑、命令执行、GitHub 权限，安全边界越重要。尤其是处理外部仓库时，不能让陌生 README 里的命令自动执行。

[主持人]
对你的个人播客雷达，我会把它定位成“工作流产品化参考”。今天这个自动化其实也可以被插件化：`/github-podcast:daily` 负责跑每日生产，`repo-selector` agent 负责选仓库，`script-writer` skill 规定中文脚本结构，`audio-verifier` hook 在完成前强制 ffprobe 和 ffmpeg decode。这样每天不是凭记忆执行，而是靠固定组件执行。

[分析员]
最后用一句话收束：`anthropics/claude-code` 这一集最值得你学的，不是安装 Claude Code，而是它的插件观。把重复工作拆成命令、agent、skill、hook 和 MCP，这正好对应你的 Feishu 知识库、Daily 控制面板、GitHub 仓库雷达和播客生产线。

[主持人]
我们把插件结构再落到一个具体例子。假设你要做“每日 GitHub 播客”插件，`commands/daily.md` 可以写触发说明和参数，比如日期、最低集数、主题偏好。`skills/repo-selection/SKILL.md` 写选择规则：Codex、Claude Code、Feishu、知识管理、RSS、TTS、浏览器自动化优先，星数不是第一指标。`agents/script-reviewer.md` 负责检查脚本是不是单仓库、是不是讲了运行方式、架构、限制和个人 fit。`hooks/pre-commit` 或等价检查负责阻止 token 和第三方源码进入提交。

[分析员]
这个拆法比把所有规则写进一个长 prompt 更可维护。因为你的需求会变化：今天偏 Codex 和 Feishu，明天可能偏 AI FDE 和产品化，后天可能偏面试案例。变化的应该是选择 skill 和审查 agent，而不是整条 pipeline。Claude Code 插件体系给你的启发就是，把会变的知识放在 skill，把会重复的动作放在 command，把需要专门判断的事交给 agent，把绝不能破的底线交给 hook。

[主持人]
再说一个容易忽略的点：插件不是越多越好。`feature-dev` 这种七阶段流程适合大改动；如果只是修一个 typo，流程反而太重。你的个人系统也一样。Feishu 归档、每日播客、考试材料压缩、简历故事线打磨，它们的复杂度不同。应该给高频高风险任务插件化，低频简单任务保留普通脚本或人工处理。

[分析员]
所以这集真正的行动建议是：先挑一个任务做插件化样板。我会选 GitHub 播客，因为它有明确输入、明确输出、明确验证和明确安全边界。做成之后，再把同样模式迁移到 Feishu Daily 汇总和面试案例压缩。这样 Claude Code 的插件观就不会停留在“看起来很先进”，而是变成你自己的生产系统结构。

[主持人]
再补一个阅读建议。`plugins/README.md` 是总览，适合建立地图；`plugins/feature-dev/README.md` 适合理解复杂开发流程；`plugins/plugin-dev/README.md` 适合理解如何创造新插件；`plugins/security-guidance` 适合理解 hook 怎样守住底线。你不需要读完所有插件，先选这四类就够了：流程型、创建型、安全型、审查型。

[分析员]
对你来说，最重要的是把“我希望 Codex 以后总是这么做”变成文件，而不是每次口头提醒。比如“每集只讲一个 repo”“没有 TokenDance key 就不要生成最终音频”“Feishu 写入前要读回确认”“第三方源码只能在 work/repos”。这些都可以成为 skill 或 hook 的内容。Claude Code 仓库里的插件系统，本质上就是把个人偏好和团队规范文件化、可触发化。

[主持人]
所以我们把结论再说得更狠一点：插件不是装饰，而是记忆和流程的产品形态。你的个人知识系统已经有很多规则，只是散在对话、Daily 和记忆里。下一步应该把高频规则沉淀为可执行组件，让 agent 每次自动加载，而不是等你提醒。

[分析员]
最后留一个小检查表：一个任务值得插件化，至少满足三个条件。第一，它重复出现，比如每日播客、Feishu 归档、面试案例整理。第二，它有明确质量标准，比如必须验证音频、必须引用真实代码、必须写回 Daily。第三，它有明确风险边界，比如不能泄露 key、不能乱写 Feishu、不能提交第三方源码。满足这三点，就适合从普通 prompt 升级成 Claude Code 风格的插件或技能。
