# GitHub Research Podcast

研究一个 GitHub 仓库，并把结论做成可听的中文播客。

## 它做什么

```text
发现仓库 → 核验 README / Docs / Code / Issues → 中文研究报告 → 双人脚本 → 音频
```

- 一次只讲一个仓库。
- 结论固定到具体 commit，不复述宣传文案。
- 研究报告是事实底稿，播客脚本和音频必须与报告一致。
- 第三方源码只放在 `work/repos/`，不提交。

## 怎么选仓库

每次先读取近期项目上下文，再给候选仓库评分：

| 维度 | 权重 |
| --- | ---: |
| 对近期项目的直接帮助 | 40% |
| 可复用的实现或设计 | 25% |
| 证据与维护成熟度 | 15% |
| 相比历史报告的新信息 | 10% |
| 社区热度与近期活跃 | 10% |

因此它不是 GitHub Trending 搬运：Star 高但帮不到当前项目的仓库会降级。
报告和播客都必须说明“帮助哪个项目问题、复用什么、最小怎么试、哪里不适合”。

## 安装 Skill

```bash
git clone https://github.com/Stephen-creater/github-research-podcast.git
cd github-research-podcast
python3 scripts/install_skill.py
```

默认安装到 `~/.codex/skills/github-research-podcast`。安装后可直接说：

> 研究这个 GitHub 仓库，并把研究结果做成中文双人播客。

Skill 源码在 [`skills/github-research-podcast`](skills/github-research-podcast)。

## 产物

```text
outputs/daily-research/YYYY-MM-DD_owner_repo.md   # 研究报告
outputs/YYYY-MM-DD_repo_single_repo_script.md     # 双人脚本
outputs/YYYY-MM-DD_repo_single_repo.m4a           # 播客音频
```

历史播客、脚本、日报和索引都保留在 [`outputs/`](outputs/)。

## 生成音频

生产音频使用 MiMo TTS，需要 `ffmpeg`、`ffprobe` 和 `TOKENDANCE_API_KEY`：

```bash
export TOKENDANCE_API_KEY=your_key
python3 github_podcast_pipeline.py audio-mimo \
  --script outputs/2026-07-05_gitingest_single_repo_script.md \
  --output work/gitingest.m4a
```

macOS 本地测试可使用系统语音，不应当作最终成片：

```bash
python3 github_podcast_pipeline.py audio \
  --script outputs/2026-07-05_gitingest_single_repo_script.md \
  --output work/gitingest-test.m4a
```

验证脚本格式、音频时长和完整解码：

```bash
python3 github_podcast_pipeline.py verify \
  --script outputs/2026-07-05_gitingest_single_repo_script.md \
  --audio outputs/2026-07-05_gitingest_single_repo.m4a
```

原有候选仓库摘要命令继续可用：

```bash
python3 github_podcast_pipeline.py brief
```

## 验证与打包

```bash
python3 -m unittest discover -s tests -v
python3 skills/github-research-podcast/scripts/validate_report.py \
  outputs/daily-research/2026-07-15_xiaolai_nlpm.md \
  --index outputs/daily-research/index.md
```

可分发 Skill 包：[`dist/github-research-podcast.skill`](dist/github-research-podcast.skill)。

## License

[MIT](LICENSE)。第三方仓库和引用内容遵循各自许可证。
