# CLAUDE.md — Working Guide for Claude Code

> This file is the **always-on instruction manual** for Claude Code when
> working inside this project. Read it fully before doing anything.
> It reflects the company-wide Claude Code education program: the goal is not just
> to "make code run" but to teach **safe, transparent, and beginner-friendly automation**
> for non-developers (특히 재무팀 실무자).

---

## 1. Project Overview

This is a **beginner-friendly practice project** for the finance team
(재무팀 초보 실습 프로젝트).
It demonstrates how to take a messy folder full of Excel/CSV expense files
and turn it into a clean, auditable reporting pipeline using Python + pandas,
guided by Claude Code.

The deliverables, in order, are:

1. Discovery — figure out which files in the folder are actually analyzable.
2. Standardization — normalize columns, dates, amounts.
3. Aggregation — produce monthly / department / category / vendor summaries.
4. Quality control — detect duplicate invoices and parsing failures.
5. Reporting — generate a Markdown report finance staff can hand to management.

The audience is **non-engineers** (재무팀 담당자) who are following along.
Optimize every decision for **clarity over cleverness**.

---

## 2. Starting Assumption

The project does **not** start from a clean directory tree.
It starts from the realistic state of a finance team's working folder:

```
finance-practice/
├── 1월비용.xlsx
├── 2월 비용 정리.xlsx
├── 3월_비용_최종.xlsx
├── 거래처지급내역_1.csv
├── 거래처 지급 내역 2.csv
├── 임시메모.txt
└── old_backup.xlsx
```

There is no `data/`, no `scripts/`-relative imports, no virtualenv layout to assume.
The scripts themselves create the working folders (`data/raw_snapshot/`,
`data/processed/`, `data/output/`, `reports/`) the first time they run.

**Never assume folders exist. Always `mkdir(parents=True, exist_ok=True)`.**

---

## 3. Beginner-Friendly Principles

- Write for someone who learned Python last week.
  명확함이 최고의 미덕이다 (clarity beats cleverness).
- Prefer many small named functions over one clever pipeline.
- Use `print()` to narrate progress at every meaningful step
  (e.g., `"  생성: 1월비용.xlsx (18행)"`).
- Use Korean in user-facing print messages and comments where it helps the
  finance team understand. Code identifiers stay in English.
- Every script must have a top-level docstring explaining what it does,
  what it reads, what it writes, and what comes next.
- Error messages should tell the user **what to do next**, not just what failed.

---

## 4. Folder and File Rules

| Path | Purpose | Created by |
| --- | --- | --- |
| project root | The user's original Excel/CSV files live here | user / step 01 |
| `scripts/` | All Python automation scripts | hand-authored |
| `data/raw_snapshot/` | Read-only safety copies of originals | step 02 |
| `data/processed/` | Cleaned intermediate data (inventory, merged) | steps 02–03 |
| `data/output/` | Summary tables for finance team | step 04 |
| `reports/` | Final Markdown reports | step 05 |

Rules:

- Originals stay in the project root. Do not move them.
- Generated artifacts never overwrite originals.
- Every script that writes output must `mkdir(parents=True, exist_ok=True)` its
  target folder first.
- Use `pathlib.Path` everywhere. No raw string paths. No `os.path.join`.
- Resolve the project root as `Path(__file__).resolve().parent.parent`
  (scripts/ → project root).

---

## 5. Data Handling Rules

- All sample data must be **synthetic** (합성 데이터).
- Never use real company names, real vendor names, real people, or real KRW values
  that could be mistaken for real data.
- Never connect to external APIs, databases, or cloud services in this
  beginner project. CSV/Excel files only.
- Treat the originals as read-only at all times. Read with pandas; never call
  `to_excel()` / `to_csv()` against a path inside the project root that
  matches an original file name.
- When the user wants to use Google Sheets, instruct them to export to
  CSV/XLSX and drop the file into the project root — do **not** wire up the
  Google Sheets API in the beginner pipeline.
- The standard column schema is fixed:

  ```
  transaction_date, department, vendor, category, amount,
  payment_method, invoice_no, memo, source_file
  ```

  Plus quality flags added by step 03:

  ```
  date_parse_failed, amount_parse_failed, is_duplicate_invoice
  ```

- New incoming column names must be added to `COLUMN_ALIASES` in
  `03_merge_finance_files.py`. Do not invent a parallel mapping elsewhere.

---

## 6. Script Writing Rules

- Target Python 3.11.
- Use `pandas` and `openpyxl`. No additional heavyweight dependencies without
  asking the user.
- Every script must:
  - Have a top-level docstring.
  - Define a `main()` function.
  - End with `if __name__ == "__main__": main()`.
  - Print a clear "starting" line and a clear "completed, next step is X" line.
- Functions should be short and named for what they produce
  (`summarize_monthly`, `clean_amount`, `read_raw_file`).
- Avoid classes unless they pull real weight. This project has none and should stay that way.
- No global mutable state beyond constants at the top of the file.
- No silent `except Exception: pass`. If you must catch, print a useful message
  and continue with a documented fallback.
- No hardcoded absolute paths. Always derive from `PROJECT_ROOT`.

---

## 7. Report Writing Rules

The Markdown report is for finance staff, not engineers.

- State only what the data shows. No marketing tone, no superlatives.
- For uncertain or missing values, write `확인 필요` (literally "needs review").
- For duplicate invoices, use the phrasing `중복 가능성 있음`
  ("possible duplicate") — never declare them as confirmed fraud or errors.
- Always list excluded files **with the reason** they were excluded.
- Always include a "재무팀 확인 필요 사항" section that surfaces every
  quality-issue category that has a non-zero count.
- Tables should be built with the simple `df_to_markdown_table` helper.
  Do not add new template engines (no Jinja, no tabulate dependency).

---

## 8. File Modification Rules

- **Never** edit anything in the project root that wasn't created by a script
  (i.e., don't rewrite the user's original Excel/CSV).
- **Never** edit anything inside `data/raw_snapshot/` — that's the audit copy.
- Re-running any script must be safe (idempotent). It should overwrite its own
  outputs in `data/processed/`, `data/output/`, `reports/`, but never touch originals.
- If you need to change file naming or output paths, update **both** the producing
  script and any downstream script that reads it, in the same change.

---

## 9. Validation Checklist

Before declaring any change "done," confirm:

- [ ] All five scripts still run cleanly in order `01 → 02 → 03 → 04 → 05`.
- [ ] `data/raw_snapshot/` contains an exact copy of every analyzed original.
- [ ] `data/processed/input_file_inventory.csv` correctly marks `include` / `exclude`.
- [ ] `data/processed/merged_expenses.csv` has all 9 standard columns + 3 quality flags.
- [ ] `data/output/` contains all six expected summary CSVs.
- [ ] `reports/finance_expense_report.md` opens and renders without broken tables.
- [ ] No script wrote to or modified any file in the project root that it did not create itself.
- [ ] No new third-party dependency was added without updating `requirements.txt`.
- [ ] README.md still matches actual script names and outputs.

---

## 10. Prohibited Actions

Do **not**:

- Use real personal data, real company names, or real vendor/account info.
- Hit external APIs, databases, or cloud storage from any script in this project.
- Introduce web frameworks (Flask, FastAPI), ORMs, or database engines.
- Add machine-learning libraries.
- Add async / multiprocessing — this pipeline is small and must stay readable.
- Use `--no-verify`, `--force`, or destructive Git operations on the user's behalf.
- Move, rename, or delete the user's original files in the project root.
- Commit secrets, credentials, or `.env` files.
- Translate Korean comments/print strings into English just for style —
  preserve them where they help the finance reader.

---

## 11. Future Extension Ideas

These are explicitly **out of scope** for the beginner pipeline but are good
follow-up exercises the user can request:

- Google Sheets API integration via `gspread`.
- Excel-formatted (`.xlsx`) summary output alongside CSV.
- Monthly trend chart (matplotlib) embedded as a PNG in the report.
- Multi-currency support (currently KRW only).
- Stricter duplicate detection on `(vendor, amount, transaction_date)` tuples.
- A unified `run_all.py` entry point that chains all five steps.
- Year-over-year comparison once multiple years of data exist.

When the user asks for any of these, scope the change carefully, keep the
beginner ergonomics, and update both `README.md` and this `CLAUDE.md`.

---

## 12. House Rules for Claude Code in This Repo

- Before editing, read the relevant script end-to-end. Don't patch blind.
- Keep diffs small. One concern per change.
- After any script change, re-run the full `01 → 05` chain and confirm
  the report still renders.
- If you discover the user's environment is missing dependencies, suggest
  `pip install -r requirements.txt` — never silently install packages.
- When unsure, prefer asking the user once over guessing.
- This is a teaching artifact. Code that is "correct but unreadable" is wrong here.
