# Report format

Use this as a strong default. Adapt headings when the repository requires it, but
preserve the evidence, architecture, risk, recommendation, and source contracts.

```markdown
# [Repository]: [plain-language value proposition]

- Repository: [owner/repo](https://github.com/owner/repo)
- Revision inspected: [`short-sha`](https://github.com/owner/repo/commit/full-sha)
- Inspection date: YYYY-MM-DD
- License: [SPDX identifier or clearly stated status]
- Local verification: [checks run, or "read-only inspection only"]

## One-sentence explanation

[Explain the project without repeating its tagline.]

## Problem and users

[State the job, target user, and why existing approaches are insufficient.]

## Setup and minimal use

[Give the smallest truthful path. Separate required and optional dependencies.]

## Architecture and entrypoints

[Name important directories, executable entrypoints, data flow, and boundaries.]

## Reusable design ideas

[Explain concrete patterns worth transferring, with evidence.]

## Fit with the user's workflow

[Describe practical integration points, costs, and what not to adopt.]

## Limitations and risks

[Cover maintenance, security, privacy, licensing, cost, maturity, and unknowns.]

## Recommendation

[Choose Use now, Study only, or Skip. Give reasons and one smallest next action.]

## Primary sources

- [Pinned README or documentation]
- [Relevant code entrypoint]
- [Release or issue evidence]
```

## Quality checks

- Study one repository only.
- Pin the inspected revision instead of describing a moving `main` branch.
- Include at least three direct primary-source links when the repository provides
  enough evidence.
- Make architecture claims traceable to files or official documentation.
- Separate facts, inferences, and recommendations.
- Avoid generic praise such as "powerful" or "easy to use" without evidence.
- Never hide a failed installation, missing license, stale release, security risk,
  or unsupported platform.
