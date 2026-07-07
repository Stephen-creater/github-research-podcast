# 2026-07-07 Daily Podcast Index

Daily target: at least 5 single-repository podcast episodes.

Status: done. All 5 episodes use one repository per episode, have script plus `.m4a` audio, are between 10 and 40 minutes, and passed `ffmpeg` decode verification.

| # | Repository | Fit role | Script | Audio | Duration | Status |
| --- | --- | --- | --- | --- | ---: | --- |
| 01 | `openai/codex` | OpenAI coding-agent architecture reference for CLI, desktop app, threads, tools, sandboxing, skills, plugins, and MCP. | `outputs/2026-07-07_codex_single_repo_script.md` | `outputs/2026-07-07_codex_single_repo.m4a` | 10.5 min | done |
| 02 | `anthropics/claude-code` | Claude Code plugin/workflow reference for commands, agents, skills, hooks, and repeatable AI work systems. | `outputs/2026-07-07_claude_code_single_repo_script.md` | `outputs/2026-07-07_claude_code_single_repo.m4a` | 10.2 min | done |
| 03 | `anthropics/claude-code-action` | GitHub Actions bridge for Claude Code automation, PR/issue triggers, permissions, structured outputs, and runner safety. | `outputs/2026-07-07_claude_code_action_single_repo_script.md` | `outputs/2026-07-07_claude_code_action_single_repo.m4a` | 10.5 min | done |
| 04 | `larksuite/cli` | Official Feishu/Lark CLI for agent-native Docs, Daily, Base, Calendar, Tasks, Mail, and workflow automation. | `outputs/2026-07-07_lark_cli_single_repo_script.md` | `outputs/2026-07-07_lark_cli_single_repo.m4a` | 10.5 min | done |
| 05 | `larksuite/lark-openapi-mcp` | Official Feishu/Lark MCP bridge for exposing OpenAPI tools to Claude, Codex, Cursor, and other agents. | `outputs/2026-07-07_lark_openapi_mcp_single_repo_script.md` | `outputs/2026-07-07_lark_openapi_mcp_single_repo.m4a` | 10.7 min | done |

Verification:

- `python3 -m py_compile github_podcast_pipeline.py`
- `ffprobe` duration check for all 5 single-repo `.m4a` files:
  - `2026-07-07_codex_single_repo.m4a`: 632.64s
  - `2026-07-07_claude_code_single_repo.m4a`: 614.88s
  - `2026-07-07_claude_code_action_single_repo.m4a`: 627.36s
  - `2026-07-07_lark_cli_single_repo.m4a`: 631.84s
  - `2026-07-07_lark_openapi_mcp_single_repo.m4a`: 640.96s
- `ffmpeg -v error -i <audio> -f null -` decode check for all 5 single-repo `.m4a` files

Operating note:

- Today's completed episodes intentionally avoid a final multi-repository roundup.
- Third-party repositories were cloned or updated only under `work/repos/`, which is ignored by git.
