"""
05_generate_report.py

요약 테이블(data/output/) 과 파일 점검 결과(data/processed/input_file_inventory.csv)
를 읽어, 재무팀 보고용 Markdown 리포트를 생성한다.

산출:
  reports/finance_expense_report.md

원칙:
  - 데이터에서 직접 읽은 사실만 기록한다.
  - 모르는 값은 "확인 필요" 라고 적는다.
  - 중복 인보이스는 단정하지 않고 "중복 가능성 있음" 으로 표현한다.
  - 과장 표현을 쓰지 않는다.
"""

from datetime import datetime
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "data" / "output"
REPORTS_DIR = PROJECT_ROOT / "reports"

INVENTORY_PATH = PROCESSED_DIR / "input_file_inventory.csv"
MERGED_PATH = PROCESSED_DIR / "merged_expenses.csv"
REPORT_PATH = REPORTS_DIR / "finance_expense_report.md"


def fmt_amount(value) -> str:
    """금액을 사람이 보기 좋게 표시 (예: 1,234,567)."""
    if pd.isna(value):
        return "확인 필요"
    try:
        return f"{int(round(float(value))):,}"
    except (TypeError, ValueError):
        return "확인 필요"


def safe_read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def df_to_markdown_table(df: pd.DataFrame, amount_cols: list[str] | None = None) -> str:
    """간단한 Markdown 표 변환. 외부 의존성(tabulate) 없이 만든다."""
    if df.empty:
        return "_데이터 없음_\n"

    amount_cols = amount_cols or []
    cols = list(df.columns)
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join(["---"] * len(cols)) + " |"
    lines = [header, sep]

    for _, row in df.iterrows():
        cells = []
        for c in cols:
            v = row[c]
            if c in amount_cols:
                cells.append(fmt_amount(v))
            elif pd.isna(v):
                cells.append("")
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def build_report() -> str:
    today = datetime.now().strftime("%Y-%m-%d")

    inventory = safe_read_csv(INVENTORY_PATH)
    merged = safe_read_csv(MERGED_PATH)
    monthly = safe_read_csv(OUTPUT_DIR / "monthly_expense_summary.csv")
    dept = safe_read_csv(OUTPUT_DIR / "department_expense_summary.csv")
    category = safe_read_csv(OUTPUT_DIR / "category_expense_summary.csv")
    vendor_top10 = safe_read_csv(OUTPUT_DIR / "vendor_top10_summary.csv")
    duplicates = safe_read_csv(OUTPUT_DIR / "duplicate_invoice_list.csv")
    quality = safe_read_csv(OUTPUT_DIR / "data_quality_summary.csv")

    included = inventory[inventory["status"] == "include"] if not inventory.empty else inventory
    excluded = inventory[inventory["status"] == "exclude"] if not inventory.empty else inventory

    total_amount = merged["amount"].sum() if "amount" in merged.columns else 0
    total_rows = len(merged)

    lines: list[str] = []
    lines.append("# 재무 비용 분석 리포트")
    lines.append("")
    lines.append(f"_작성일: {today}_  ")
    lines.append("_본 리포트는 합성 데이터를 기반으로 한 실습용 산출물이다._")
    lines.append("")

    # 1. 분석 개요
    lines.append("## 1. 분석 개요")
    lines.append("")
    lines.append("- 프로젝트 루트의 Excel/CSV 파일을 자동으로 점검·통합한 결과를 정리한다.")
    lines.append(f"- 분석 대상 파일 수: **{len(included)}개**")
    lines.append(f"- 제외 파일 수: **{len(excluded)}개**")
    lines.append(f"- 통합 거래 건수: **{total_rows}건**")
    lines.append(f"- 통합 거래 총액(원): **{fmt_amount(total_amount)}**")
    lines.append("")

    # 2. 분석 대상 파일
    lines.append("## 2. 분석 대상 파일 목록")
    lines.append("")
    if included.empty:
        lines.append("_분석 대상 파일이 없다._")
    else:
        view = included[["file_name", "file_type", "row_count", "note"]].copy()
        lines.append(df_to_markdown_table(view))
    lines.append("")

    # 3. 제외 파일
    lines.append("## 3. 제외 파일 목록")
    lines.append("")
    if excluded.empty:
        lines.append("_제외된 파일이 없다._")
    else:
        view = excluded[["file_name", "file_type", "note"]].copy()
        lines.append(df_to_markdown_table(view))
    lines.append("")

    # 4. 전체 비용 합계
    lines.append("## 4. 전체 비용 합계")
    lines.append("")
    lines.append(f"- 총 거래 건수: {total_rows}건")
    lines.append(f"- 총 결제 금액(원): {fmt_amount(total_amount)}")
    lines.append("")

    # 5. 월별 비용 요약
    lines.append("## 5. 월별 비용 요약")
    lines.append("")
    lines.append(df_to_markdown_table(monthly, amount_cols=["total_amount"]))
    lines.append("")

    # 6. 부서별 비용 요약
    lines.append("## 6. 부서별 비용 요약")
    lines.append("")
    lines.append(df_to_markdown_table(dept, amount_cols=["total_amount"]))
    lines.append("")

    # 7. 비용 항목별 요약
    lines.append("## 7. 비용 항목별 요약")
    lines.append("")
    lines.append(df_to_markdown_table(category, amount_cols=["total_amount"]))
    lines.append("")

    # 8. 거래처 Top 10
    lines.append("## 8. 거래처 Top 10")
    lines.append("")
    lines.append(df_to_markdown_table(vendor_top10, amount_cols=["total_amount"]))
    lines.append("")

    # 9. 데이터 품질 점검 결과
    lines.append("## 9. 데이터 품질 점검 결과")
    lines.append("")
    lines.append(df_to_markdown_table(quality))
    lines.append("")

    # 10. 중복 인보이스
    lines.append("## 10. 중복 invoice_no 목록 (중복 가능성 있음)")
    lines.append("")
    if duplicates.empty:
        lines.append("_중복으로 추정되는 인보이스가 없다._")
    else:
        lines.append(df_to_markdown_table(duplicates, amount_cols=["amount"]))
    lines.append("")

    # 11. 확인 필요 사항
    lines.append("## 11. 재무팀 확인 필요 사항")
    lines.append("")
    if not quality.empty:
        # 품질 이슈가 있는 항목만 모아 안내한다.
        issues = quality[quality["count"].astype(int) > 0]
        # "총 거래 건수" 행은 이슈가 아니므로 제외
        issues = issues[issues["issue"] != "총 거래 건수"]
        if issues.empty:
            lines.append("- 별도의 데이터 품질 이슈가 발견되지 않았다.")
        else:
            for _, r in issues.iterrows():
                lines.append(f"- {r['issue']}: {int(r['count'])}건 → 원본 파일 재확인 필요")
    else:
        lines.append("- 품질 요약이 비어 있다. 확인 필요.")
    lines.append("")

    # 12. 다음 액션
    lines.append("## 12. 다음 액션")
    lines.append("")
    lines.append("- 제외 파일 목록을 재무팀 담당자와 함께 검토한다.")
    lines.append("- 날짜/금액 변환 실패 행은 원본 파일에서 표기를 확인한다.")
    lines.append("- 중복 invoice_no 목록은 동일 거래 중복 입력 여부를 확인한다.")
    lines.append("- 확정된 결과는 별도 보고용 양식에 정리해 공유한다.")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    print("[05] 리포트 생성을 시작한다.")
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    text = build_report()
    REPORT_PATH.write_text(text, encoding="utf-8")
    print(f"  저장됨: {REPORT_PATH.relative_to(PROJECT_ROOT)}")
    print("[05] 완료. 모든 단계가 끝났습니다.")


if __name__ == "__main__":
    main()
