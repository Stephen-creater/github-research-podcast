# Output format

## Research report

Use this minimum structure:

```markdown
# owner/repo: plain-language value

- Repository: [owner/repo](https://github.com/owner/repo)
- Revision: [`short-sha`](https://github.com/owner/repo/commit/full-sha)
- Date: YYYY-MM-DD
- License: SPDX identifier or status
- Verification: checks run, or read-only inspection

## One-sentence explanation
## Problem and users
## Setup and minimal use
## Architecture and entrypoints
## Reusable design ideas
## Help for recent projects
## Limitations and risks
## Recommendation
## Primary sources
```

Choose one recommendation: **Use now**, **Study only**, or **Skip**.

Under `Help for recent projects`, answer four concrete questions:

1. Which active project problem or decision does this help?
2. What code, architecture, workflow, or evaluation method can be reused?
3. What is the smallest useful trial?
4. Which part does not fit and should not be copied?

Use only the minimum project context needed for the explanation. Do not publish
private paths, credentials, confidential names, or unrelated personal details.

## Podcast script

Use only these speaker markers:

```markdown
# owner/repo：播客标题

[主持人]
开场：仓库是什么，为什么值得听。

[分析员]
用报告中的事实解释问题、架构和关键入口。

[主持人]
追问：具体能帮助最近哪个项目问题？复用什么？最小怎么试？

[分析员]
回答直接帮助与不适用部分，再给出结论和最小下一步。
```

Requirements:

- Discuss one repository only.
- Ground every factual claim in the report.
- Explain architecture and limitations, not only features.
- Include one concrete recent-project-help segment from the report.
- Write natural dialogue rather than alternating sentence fragments.
- Let evidence density determine duration; do not pad the script.
- End with the same recommendation as the report.
