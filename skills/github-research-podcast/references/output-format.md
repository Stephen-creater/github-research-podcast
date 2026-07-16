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
## Fit with the user's workflow
## Limitations and risks
## Recommendation
## Primary sources
```

Choose one recommendation: **Use now**, **Study only**, or **Skip**.

## Podcast script

Use only these speaker markers:

```markdown
# owner/repo：播客标题

[主持人]
开场：仓库是什么，为什么值得听。

[分析员]
用报告中的事实解释问题、架构和关键入口。

[主持人]
追问使用方式、限制和与用户工作流的关系。

[分析员]
给出结论和最小下一步。
```

Requirements:

- Discuss one repository only.
- Ground every factual claim in the report.
- Explain architecture and limitations, not only features.
- Write natural dialogue rather than alternating sentence fragments.
- Let evidence density determine duration; do not pad the script.
- End with the same recommendation as the report.
