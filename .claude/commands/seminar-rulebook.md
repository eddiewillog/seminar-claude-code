# Seminar Rule Book

## Scope Gate

- Use this skill only for durable AI Native Education / Seminar program rules.
- Do not use rulebook pages as daily logs or session notes.
- Exclude Claude Code/skill/hook/local setup infrastructure unless it directly defines an operating policy for the seminar program.

## Fixed Location

- Cloud ID: `6c7e48c9-025f-4ff9-b6d1-a2a6ddf4ad25`
- Space ID: `1304985607`
- Space key: `DST`
- Cloud URL: `https://willog.atlassian.net`
- Project base page ID: `1654816773` ([DS] 사내 AI-Native, Claude Code 교육)
- Rule book folder ID: `1654489096` ([Seminar] Rule Book)

Rulebook pages must be created and maintained under folder `1654489096` ([Seminar] Rule Book).

## Use For

- 팀별 커리큘럼 설계 원칙 및 실습 구성 기준
- 교육 자료 제작 규격 (파일 형식, 폴더 구조, 네이밍 규칙)
- 반복 업무 워크플로우 설계 정책 (회의록 자동화, 재고 리포트 등)
- 스킬(slash command) 작성 기준 및 명명 규칙
- 교육 대상 팀별 운영 정책 (인사팀, 운영팀 등)

## Title Rule

```
[Seminar] {Rule Title}
```

Examples:
```
[Seminar] 팀별 커리큘럼 설계 원칙
[Seminar] 교육 자료 제작 규격
[Seminar] 반복 업무 워크플로우 설계 정책
[Seminar] 스킬 작성 기준
```

## Workflow

1. Apply the Scope Gate.
2. Convert the requested rule/spec topic into a stable rule title.
3. Use the exact title pattern `[Seminar] {Rule Title}`.
4. Search Confluence for an existing page with that title or an obviously matching rule.
5. If an existing rule changes, update the existing page.
6. If no matching rule exists, create a new page under folder `1654489096`.
7. Do not include `Rule Book` in the title — the folder already identifies the page type.
8. Keep rules explicit enough to be immediately actionable.
9. If a rule changes because of a session outcome, mention the related daily note.
10. After any successful Confluence write, run the Git push hook.

## Search Guidance

Exact title lookup first:
```
title = "[Seminar] {Rule Title}" AND space = "DST"
```

Fallback keyword search:
```
title ~ "[Seminar]" AND text ~ "{main keywords}" AND space = "DST"
```

## Content Rules

- Make pages durable and actionable — not session logs.
- Include criteria, examples, and known exceptions.
- Use tables for decision rules.
- Avoid daily progress details except brief change notes.
- If the user asks for a simpler explanation, add a plain-language section rather than weakening the spec.

## Post-Confluence Git Push Hook

After any successful Confluence mutation:

```bash
git push
```

- Run only after a successful page create or page update.
- Do not auto-commit uncommitted work.
- If push fails, report the reason without force pushing.
