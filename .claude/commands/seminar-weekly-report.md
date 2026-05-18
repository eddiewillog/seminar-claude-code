# Seminar Weekly Report

## Scope Gate

- Use this skill only for AI Native Education / Seminar program work.
- Source content from `[Seminar] Notes` daily notes only.
- Exclude Claude Code/skill/hook/local setup unless it directly changed the seminar program deliverable.
- If no Seminar notes exist for the target week, do not create a report unless the user explicitly asks for a skeleton.

## Fixed Location

- Cloud ID: `6c7e48c9-025f-4ff9-b6d1-a2a6ddf4ad25`
- Space ID: `1304985607`
- Space key: `DST`
- Cloud URL: `https://willog.atlassian.net`
- Project base page ID: `1654816773` ([DS] 사내 AI-Native, Claude Code 교육)
- Daily notes folder ID: `1654521859` ([Seminar] Daily Notes)
- Weekly notes folder ID: `1654521878` ([Seminar] Weekly Notes)

Weekly notes must be created and maintained under folder `1654521878`.

## Week Rule

- Use Asia/Seoul date.
- One reporting week starts on Wednesday and ends on the next Tuesday.
- Page title uses the week start date:

```
[Seminar] Weekly {yymmdd}
```

Example:
```
Week: 2026-05-13 Wed ~ 2026-05-19 Tue
Title: [Seminar] Weekly 260513
```

## Source Notes

Collect daily notes for every date in the reporting week from folder `1654521859`:

CQL search:
```
title ~ "[Seminar] Notes" AND space = "DST" AND ancestor = 1654521859
```

If a daily note does not exist for a date, skip that date.

## Output Format

```
## 프로젝트

사내 AI Native 교육 프로그램

## 금주수행업무

- ...

## 주요산출물

- ...

## 차주예정업무

- ...
```

Keep concise. Merge duplicate work across daily notes instead of listing day-by-day logs.

## Upsert Workflow

1. Apply the Scope Gate.
2. Determine the target reporting week. If no date given, use today's Asia/Seoul date.
3. Compute week start (Wednesday) and week end (Tuesday).
4. Search for `[Seminar] Weekly {yymmdd}` under folder `1654521878`.
5. Collect all `[Seminar] Notes` for dates in the week from folder `1654521859`.
6. Summarize into `금주수행업무`, `주요산출물`, `차주예정업무`.
7. If the weekly page exists, fetch and update it — preserve still-valid content, merge new bullets, remove obsolete contradictions.
8. If not, create under `1654521878`.
9. After successful write, run the Git push hook.

## Content Rules

- Write in concise bullet-style Korean (`개조식`).
- `주요산출물`: only concrete education deliverables — guides created, workflows designed, sessions delivered, skills built.
  - Good: `인사팀 회의록 자동화 가이드 제작 완료`, `운영팀 재고 리포트 스킬 2종 배포`
  - Bad: `SKILL.md 파일 생성`, `.claude/commands/ 경로에 배포`
- `차주예정업무`: next actions and open follow-ups from daily notes.
- Do not include raw file paths, Jira keys, or Claude Code infrastructure as the primary content.

## Post-Confluence Git Push Hook

After any successful Confluence mutation:

```bash
git push
```

- Never force push.
- If nothing to push, report that clearly.
