# Seminar Jira Update

## Scope Gate

- Use this skill only for the AI Native Education / Seminar program work.
- Do not use for Alarm, Focus, or unrelated project work.
- Include only concrete seminar work: session design, material creation, workflow setup, team outcomes, or curriculum decisions.
- Exclude Claude Code/hook/skill/local infrastructure details unless they directly change the seminar program deliverable.

## Fixed Jira Context

- Cloud ID: `6c7e48c9-025f-4ff9-b6d1-a2a6ddf4ad25`
- Project Key: `DSTEAM`
- Jira URL: `https://willog.atlassian.net`

## Card Identification Rule

- Treat Jira issues as Seminar-owned only when the issue summary starts with `[Seminar]`.
- Use `[Seminar]` as the primary identification rule for selecting, reviewing, updating, or creating cards.
- If a Jira issue is in `DSTEAM` but does not use the `[Seminar]` prefix, do not treat it as a Seminar working card unless the user explicitly says so.

## Status Gate

- For automatic same-session progress updates, only use Seminar cards still in active stages: backlog, to do, in progress, or equivalent.
- Do not update cards already at review, done, or resolved unless the user explicitly names that issue.
- If today's work belongs to a Seminar topic but no suitable pre-review card exists, create a new `[Seminar]` issue in working status.

## Supported Modes

1. Update an existing issue
2. Create a new backlog issue

Default selection rule:
- User provides a Jira key or URL and asks to reflect today's work → **update mode**
- User asks to create a next-task card or backlog item → **backlog mode**

## Issue Type Selection

| 상황 | 이슈 타입 | ID |
|------|-----------|-----|
| 교육 프로그램 전체 묶음, 기수 단위 | 에픽 | `11057` |
| 교육 자료 제작, 세션 기획, 워크플로우 설계 | 작업 | `11060` |
| 세부 실행 항목 | Subtask | `11058` |

## Mode A: Update Existing Issue

### Default Write Mode

- Default: update the issue **description**.
- Do not add a comment unless the user explicitly asks.

### Required Output Format

```
## 배경
- ...

## 진행내용
- ...

## 산출물
- 작업명
  - 산출물 / 링크 / 경로
```

### Formatting Rules

- `배경`: one bullet by default; two only when necessary.
- `진행내용`: at most 5 bullets, one short sentence each.
- `산출물`: parent bullet for work item, sub-bullets for files, pages, workflows.
- Keep wording short and factual.
- Preferred style:
  - `인사팀 회의록 자동화 가이드 제작함`
  - `운영팀 재고 리포트 스킬 초안 작성함`
  - `세션 2 커리큘럼 설계 완료함`
- Avoid: `~했습니다`, `~하였습니다`, `~가능성을 확인했습니다`

### Content Rules

- Write only today's actual Seminar work.
- `배경`: why this work item matters, one line.
- `진행내용`: what was designed, created, or delivered.
- `산출물`: concrete outputs only — files, Confluence pages, workflows, guides.
- If a related Confluence note exists, include it under `산출물`.
- Scope updates to the target card title/background — do not mix in unrelated seminar work.

## Mode B: Create Backlog Issue

### Recommendation-First Rule

- If the user asks for backlog creation without a finalized task, propose 3 to 5 candidate next tasks first.
- Each candidate: short title + one-sentence reason.
- After the user chooses, create the issue.
- If the user rejects all and gives a different task, create from the user's task.

### Backlog Write Mode

- Create a new Jira issue in `DSTEAM`.
- Naming pattern: `[Seminar] <Task Title>`
- Write only the title and `배경` section.

### Required Format for Backlog Issues

```
## 배경
- ...
```

### Backlog Rules

- One short bullet by default.
- Background explains why this work should exist, not how it was done.
- Prefer compact execution-oriented titles:
  - `[Seminar] 인사팀 회의록 자동화 가이드 v2 제작`
  - `[Seminar] 운영팀 세션 커리큘럼 개선`
  - `[Seminar] 2기 세미나 설계 및 대상 팀 선정`

## Workflow

1. Detect mode: update or backlog.
2. Check that the target issue uses `[Seminar]` prefix.
   - If not, treat as out of scope unless the user explicitly overrides.
3. Update mode:
   - Fetch target issue.
   - Read summary and existing `배경`.
   - Confirm the issue is still pre-review when selected automatically.
   - Gather today's Seminar work from the current conversation.
   - Filter to only work matching the target card title/background.
   - Write description in the fixed format.
4. Backlog mode:
   - Propose candidates if task is not finalized.
   - Wait for user's choice.
   - Create issue with `[Seminar]` title and `배경` only.
5. Confirm what was updated or created with the issue URL.
