# 2026-07-05 Daily Podcast Index

Daily target: at least 5 single-repository podcast episodes.

Status: done. All 5 episodes use one repository per episode, have script plus `.m4a` audio, are between 10 and 40 minutes, and passed `ffmpeg` decode verification.

| # | Repository | Fit role | Script | Audio | Duration | Status |
| --- | --- | --- | --- | --- | ---: | --- |
| 01 | `coderamp-labs/gitingest` | Repository-to-LLM-context digestion layer for GitHub podcast research. | `outputs/2026-07-05_gitingest_single_repo_script.md` | `outputs/2026-07-05_gitingest_single_repo.m4a` | 15.5 min | done |
| 02 | `ttlequals0/Audicle` | Private reading-list-to-podcast feed architecture for Feishu/article workflows. | `outputs/2026-07-05_audicle_single_repo_script.md` | `outputs/2026-07-05_audicle_single_repo.m4a` | 13.7 min | done |
| 03 | `sourcelabs-nl/ai-podcast-studio` | End-to-end source monitoring, scoring, script, TTS, publishing, and quota reference. | `outputs/2026-07-05_ai_podcast_studio_single_repo_script.md` | `outputs/2026-07-05_ai_podcast_studio_single_repo.m4a` | 14.9 min | done |
| 04 | `H2O-YAOZE/feishu-claude-code` | Future Feishu control plane for triggering and monitoring local podcast generation. | `outputs/2026-07-05_feishu_claude_code_single_repo_script.md` | `outputs/2026-07-05_feishu_claude_code_single_repo.m4a` | 13.1 min | done |
| 05 | `Winfred1024/feishu-pm-kit` | Governance model for daily manifests, health checks, and Feishu/Bitable sync. | `outputs/2026-07-05_feishu_pm_kit_single_repo_script.md` | `outputs/2026-07-05_feishu_pm_kit_single_repo.m4a` | 14.4 min | done |

Verification:

- `python3 -m py_compile github_podcast_pipeline.py`
- `ffprobe` duration check for all 5 single-repo `.m4a` files
- `ffmpeg -v error -i <audio> -f null -` decode check for all 5 single-repo `.m4a` files

Operating rule for future days:

- Generate at least 5 completed episodes per calendar day.
- Each episode must focus on exactly one GitHub repository.
- A repo roundup is allowed only as candidate research, never as a final episode.
- If an episode already has a script but audio synthesis fails, retry audio only.
- If an episode already has valid audio, do not regenerate it unless explicitly requested.
- Commit and push durable outputs after each daily run.
