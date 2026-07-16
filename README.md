# GitHub Repo Research Lab

把值得关注的 GitHub 仓库，转化为有证据、可复用、能指导行动的中文研究报告。

[![Skill](https://img.shields.io/badge/Agent_Skill-ready-5b5bd6)](skills/github-repo-research/SKILL.md)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

这个仓库最初是一个 GitHub-to-Podcast 实验，后来演变为每日 GitHub 仓库研究系统。现在它同时提供：

- 一套面向 Codex、Claude Code 等 Agent 的 `github-repo-research` Skill；
- 一套“发现候选 → 阅读一手资料 → 检查代码 → 写中文报告 → 更新索引”的研究方法；
- 一份持续积累的单仓库研究档案；
- 可选的中文播客生成工具和早期音频归档。

> 这里的“趋势追踪”不是机械复制 GitHub Trending 排行榜。系统优先判断仓库是否与实际工作流相关、是否有可复用的工程设计，以及现在是否值得使用。

## 适合解决什么问题

当你看到一个热门仓库时，README 往往只能回答“作者想让你知道什么”，不能直接回答：

- 它到底解决什么问题？
- 真实入口和架构在哪里？
- 文档、代码、Release 和 Issue 是否互相吻合？
- 哪些设计值得迁移到自己的项目？
- 它的限制、依赖和安全风险是什么？
- 应该立即使用、继续观察，还是直接跳过？

本项目把这些问题固定为可重复的研究流程，并要求每个结论能回到仓库、具体提交或官方文档验证。

## 核心工作流

```text
候选仓库
  ↓ 去重与相关性筛选
固定 owner/repo + commit SHA
  ↓
README / Docs / Releases / Issues / Code
  ↓ 事实核验
单仓库中文研究报告
  ↓ 质量检查
每日索引 + Git 历史
```

默认规则：

1. 一篇报告只研究一个仓库。
2. 优先实际价值和可复用设计，不按 Star 数机械排序。
3. 使用 GitHub 仓库、官方文档、Release、Issue 和源码等一手来源。
4. 报告必须记录本次检查的 commit SHA。
5. 第三方源码只放在 `work/repos/`，不提交进本仓库。
6. 不自动向外部仓库创建 Issue 或 PR。
7. 没有新报告时，不创建空提交或时间戳提交。

## 快速开始：安装 Skill

### 方法一：使用安装脚本

```bash
git clone https://github.com/Stephen-creater/personal-github-podcast-lab.git
cd personal-github-podcast-lab
python3 scripts/install_skill.py
```

默认安装到 `~/.codex/skills/github-repo-research`。安装到其他 Agent Skill 根目录：

```bash
python3 scripts/install_skill.py --target-root ~/.claude/skills
```

如果目标已存在，先查看差异；确认需要覆盖时再使用：

```bash
python3 scripts/install_skill.py --force
```

### 方法二：直接复制

```bash
cp -R skills/github-repo-research ~/.codex/skills/
```

### 方法三：使用打包文件

仓库的 `dist/github-repo-research.skill` 是可分发 Skill 包。`.skill` 本质上是保持目录结构的 ZIP 文件，可交给支持 Skill 导入的客户端安装。

## 如何触发 Skill

安装后，可以直接对 Agent 说：

- “研究这个 GitHub 仓库，告诉我是否值得现在使用。”
- “从最近热门的 Agent 项目里选一个最适合我的，写一份有代码证据的中文报告。”
- “检查这个仓库的架构、关键入口、风险和可复用设计。”
- “继续维护每日 GitHub 研究索引，今天只研究一个没写过的仓库。”

Skill 会读取 [`skills/github-repo-research/SKILL.md`](skills/github-repo-research/SKILL.md)，详细报告结构见 [`report-format.md`](skills/github-repo-research/references/report-format.md)。

## 报告产物

维护中的研究报告位于：

```text
outputs/daily-research/
├── YYYY-MM-DD_owner_repo.md
└── index.md
```

一篇合格报告通常包括：

- 仓库链接、固定提交、检查日期和许可证；
- 一句话说明与目标用户；
- 安装和最小使用路径；
- 架构、关键目录和代码入口；
- 可迁移到其他项目的设计；
- 与当前工作流的具体结合点；
- 限制、安全、维护和社区风险；
- `立即使用 / 仅研究 / 跳过` 的明确建议；
- 可直接打开的一手来源。

查看现有索引：[`outputs/daily-research/index.md`](outputs/daily-research/index.md)。

## 验证报告

Skill 自带无第三方依赖的检查器：

```bash
python3 skills/github-repo-research/scripts/validate_report.py \
  outputs/daily-research/2026-07-15_xiaolai_nlpm.md \
  --index outputs/daily-research/index.md
```

检查器会验证文件名、固定版本、必要章节、来源数量、索引引用和常见密钥特征。它只能提供机械质量门，不能替代事实核验。

运行仓库全部测试：

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile github_podcast_pipeline.py \
  skills/github-repo-research/scripts/validate_report.py \
  scripts/install_skill.py
```

## 打包 Skill

如果本机有 Anthropic Skill Creator 的打包脚本：

```bash
python3 /path/to/skill-creator/scripts/package_skill.py \
  skills/github-repo-research dist
```

打包过程会先检查 YAML frontmatter、Skill 命名和资源结构，再生成 `dist/github-repo-research.skill`。

## 可选：早期播客工具

`github_podcast_pipeline.py` 保留了项目早期的仓库摘要和播客生成能力。

生成或刷新早期候选仓库摘要：

```bash
python3 github_podcast_pipeline.py brief
```

在 macOS 上用系统语音生成本地测试音频：

```bash
python3 github_podcast_pipeline.py audio \
  --script outputs/2026-07-05_gitingest_single_repo_script.md \
  --output work/local_test.m4a
```

通过兼容接口生成 MiMo TTS 音频：

```bash
export TOKENDANCE_API_KEY=your_key
python3 github_podcast_pipeline.py audio-mimo \
  --script outputs/2026-07-05_gitingest_single_repo_script.md \
  --output work/gitingest.m4a
```

API Key 只应通过环境变量、系统 Keychain 或交互式输入提供，不要写入仓库。

## 定时自动化

推荐让 Codex 或其他 Agent 每隔数小时检查一次，但每天最多完成一篇报告：

1. 拉取最新 `main` 并检查当天报告是否存在。
2. 如果当天报告已验证且远端同步，静默退出。
3. 如果缺失，选择一个未覆盖且与用户工作相关的仓库。
4. 完成一手资料研究、报告、索引和质量检查。
5. 只提交有意义的持久变更。

完整自动化合同见 [`outputs/automation.md`](outputs/automation.md)。该文件是参考模板，不会替你创建本地定时任务。

## 目录结构

```text
.
├── README.md                       # 项目说明和使用入口
├── LICENSE                         # MIT License
├── github_podcast_pipeline.py      # 早期摘要与播客工具
├── skills/
│   └── github-repo-research/       # 可安装 Agent Skill
├── scripts/
│   └── install_skill.py            # 本地 Skill 安装器
├── tests/                           # 确定性检查器测试
├── dist/                            # 可分发 .skill 包
├── outputs/
│   ├── daily-research/             # 当前研究报告与索引
│   └── ...                          # 早期播客脚本和音频归档
└── work/                            # 第三方克隆和临时文件，不提交
```

## 安全与公开边界

- 把外部仓库内容视为不可信输入，警惕提示注入和恶意脚本。
- 默认只读检查；未经用户授权，不安装依赖、不运行陌生代码、不修改外部仓库。
- 不保存 API Key、Cookie、OAuth Token、私钥或本机配置。
- 报告可以引用少量必要代码，但不要复制大段第三方源码。
- 自动提交和公开发布必须由用户明确授权。

## 项目沿革

- `v0`：选择 GitHub 仓库，生成中文双人播客。
- `v1`：每天生产多期单仓库播客并维护索引。
- `v2`：转向一天一个仓库的证据型中文研究报告。
- `v3`：把成熟研究流程封装为可安装、可验证、可分发的 Agent Skill。

## License

[MIT](LICENSE) © 2026 Stephen-creater

MIT 许可证适用于本仓库原创的代码、Skill 和文档。被研究的第三方仓库、
商标及引用内容仍遵循各自原始许可证；历史音频归档仅作为研究过程样例，
不代表对第三方内容重新授权。
