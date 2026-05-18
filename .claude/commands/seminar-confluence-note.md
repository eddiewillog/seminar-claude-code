# Seminar Confluence Note

## Scope Gate

- Use this skill only for AI Native Education / Seminar program work.
- Record only concrete education work: sessions delivered, materials created, workflows designed, curriculum decisions, team outcomes.
- Exclude Claude Code/skill/hook/local setup infrastructure unless it directly changes the seminar program deliverable.
- If there is no Seminar work to record, do not create or update a note.

## Fixed Location

- Cloud ID: `6c7e48c9-025f-4ff9-b6d1-a2a6ddf4ad25`
- Space ID: `1304985607`
- Space key: `DST`
- Cloud URL: `https://willog.atlassian.net`
- Project base page ID: `1654816773` ([DS] 사내 AI-Native, Claude Code 교육)
- Daily notes folder ID: `1654521859` ([Seminar] Daily Notes)
- Weekly notes folder ID: `1654521878` ([Seminar] Weekly Notes)
- Rule book folder ID: `1654489096` ([Seminar] Rule Book)

Daily notes must be created and maintained under folder `1654521859`.

## Title Rule

```
[AI-native Workshop] Reports YYMMDD — {핵심 작업명}
```

- Use Asia/Seoul date (YYMMDD format).
- Keep the prefix exactly `[AI-native Workshop] Reports {yymmdd}`.
- 핵심 작업명은 2~4 단어 명사형으로 작성.
- When updating an existing note, also update the page title so it reflects the day's cumulative work.
- Example: `2026-05-14` → `[AI-native Workshop] Reports 260514 — 인사팀 가이드 초안 완성`

## Workflow

1. Apply the Scope Gate.
2. Determine target date. If not specified, use today's Asia/Seoul date.
3. Search Confluence for existing pages whose title starts with `[AI-native Workshop] Reports {yymmdd}`.
4. If a matching page exists:
   - Use `updateConfluencePage` for consolidating or rewriting the main note.
   - Use `createConfluenceFooterComment` for appending a short update.
5. If no matching page exists, create a new page under folder `1654521859`.
6. If multiple same-date pages exist, merge content into one canonical page.
7. If the existing title no longer represents the day's cumulative work, rename it while preserving the `[AI-native Workshop] Reports {yymmdd}` prefix.
8. **보고 목록 업데이트**: After any create or title change, fetch the parent page `1654521859`, find the 보고 목록 table, and append a new row:
   - 날짜: `YYYY-MM-DD`
   - 제목: page title (핵심 작업명 부분)
   - 링크: Confluence page URL
   - If a row for the same date already exists, update it instead of appending.
   - Preserve all existing rows; do not overwrite other entries.
9. After the parent page update, invoke `seminar-weekly-report` to refresh the current week's report.
10. After any successful Confluence write, run the Git push hook.

## Search Guidance

CQL title search:
```
title ~ "[AI-native Workshop] Reports {yymmdd}" AND space = "DST"
```

## Content Rules

- Write in concise bullet-style Korean (`개조식`).
- Separate facts from next actions.
- Include file paths, Jira keys, page links, workflow names when relevant.
- Do not paste large logs; summarize outputs.
- Do not include "created a skill", "added a hook", or similar Claude Code infrastructure activity.

Preferred sections:
- `Summary`
- `오늘 만든 것 / 설계한 것`
- `팀별 진행 현황`
- `결정 사항`
- `다음 액션`

## Post-Confluence Git Push Hook

After any successful Confluence mutation:

```bash
git push
```

- Run only after a successful page create, page update, or comment create.
- Do not auto-commit uncommitted work.
- If push fails because remote changes must be integrated first, do not force push. Report the failure.
