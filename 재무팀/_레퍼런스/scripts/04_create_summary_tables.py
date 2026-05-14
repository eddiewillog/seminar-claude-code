"""
04_create_summary_tables.py

03 단계에서 만든 통합 데이터(merged_expenses.csv)를 읽어,
재무팀이 자주 보는 요약 테이블을 CSV 로 떨군다.

생성 파일 (모두 data/output/ 에):
  - monthly_expense_summary.csv     : 월별 총 비용
  - department_expense_summary.csv  : 부서별 총 비용
  - category_expense_summary.csv    : 항목별 총 비용
  - vendor_top10_summary.csv        : 거래처별 Top 10
  - duplicate_invoice_list.csv      : 중복 invoice_no 목록
  - data_quality_summary.csv        : 데이터 품질 이슈 요약

모든 결과는 초보자가 Excel 로 바로 열어볼 수 있게 UTF-8 BOM 인코딩으로 저장한다.
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "data" / "output"
MERGED_PATH = PROCESSED_DIR / "merged_expenses.csv"


def load_merged() -> pd.DataFrame:
    if not MERGED_PATH.exists():
        raise FileNotFoundError(
            f"통합 파일이 없다: {MERGED_PATH}\n"
            "먼저 03_merge_finance_files.py 를 실행하세요."
        )
    df = pd.read_csv(MERGED_PATH)
    # 날짜 컬럼 복원
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    return df


def save_csv(df: pd.DataFrame, path: Path) -> None:
    """UTF-8 BOM 으로 저장해 Excel 한글 깨짐을 방지한다."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"  저장됨: {path.relative_to(PROJECT_ROOT)} ({len(df)}행)")


def summarize_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """월(YYYY-MM)별 총 비용. 날짜 변환 실패 행은 제외한다."""
    valid = df.dropna(subset=["transaction_date", "amount"]).copy()
    valid["year_month"] = valid["transaction_date"].dt.strftime("%Y-%m")
    g = (
        valid.groupby("year_month", as_index=False)
        .agg(transaction_count=("amount", "size"), total_amount=("amount", "sum"))
        .sort_values("year_month")
    )
    return g


def summarize_department(df: pd.DataFrame) -> pd.DataFrame:
    valid = df.dropna(subset=["amount"]).copy()
    g = (
        valid.groupby("department", as_index=False, dropna=False)
        .agg(transaction_count=("amount", "size"), total_amount=("amount", "sum"))
        .sort_values("total_amount", ascending=False)
    )
    return g


def summarize_category(df: pd.DataFrame) -> pd.DataFrame:
    valid = df.dropna(subset=["amount"]).copy()
    g = (
        valid.groupby("category", as_index=False, dropna=False)
        .agg(transaction_count=("amount", "size"), total_amount=("amount", "sum"))
        .sort_values("total_amount", ascending=False)
    )
    return g


def summarize_vendor_top10(df: pd.DataFrame) -> pd.DataFrame:
    valid = df.dropna(subset=["amount"]).copy()
    g = (
        valid.groupby("vendor", as_index=False, dropna=False)
        .agg(transaction_count=("amount", "size"), total_amount=("amount", "sum"))
        .sort_values("total_amount", ascending=False)
        .head(10)
    )
    return g


def list_duplicate_invoices(df: pd.DataFrame) -> pd.DataFrame:
    """is_duplicate_invoice == True 인 행을 invoice_no 기준으로 묶어 보여준다."""
    dup_rows = df[df["is_duplicate_invoice"] == True].copy()  # noqa: E712
    if dup_rows.empty:
        return pd.DataFrame(
            columns=[
                "invoice_no",
                "transaction_date",
                "department",
                "vendor",
                "amount",
                "source_file",
            ]
        )
    return dup_rows[
        [
            "invoice_no",
            "transaction_date",
            "department",
            "vendor",
            "amount",
            "source_file",
        ]
    ].sort_values(["invoice_no", "source_file"])


def summarize_data_quality(df: pd.DataFrame) -> pd.DataFrame:
    """이슈 종류별 건수를 표로 만든다."""
    total = len(df)
    bad_date = int(df["date_parse_failed"].sum())
    bad_amount = int(df["amount_parse_failed"].sum())
    dup = int(df["is_duplicate_invoice"].sum())
    missing_vendor = int(df["vendor"].isna().sum())
    missing_dept = int(df["department"].isna().sum())
    missing_invoice = int(df["invoice_no"].isna().sum() + (df["invoice_no"] == "").sum())

    rows = [
        {"issue": "총 거래 건수", "count": total},
        {"issue": "날짜 변환 실패", "count": bad_date},
        {"issue": "금액 변환 실패", "count": bad_amount},
        {"issue": "중복 invoice_no 로 표시된 건수", "count": dup},
        {"issue": "거래처(vendor) 누락", "count": missing_vendor},
        {"issue": "부서(department) 누락", "count": missing_dept},
        {"issue": "인보이스 번호 누락", "count": missing_invoice},
    ]
    return pd.DataFrame(rows)


def main() -> None:
    print("[04] 요약 테이블 생성을 시작한다.")
    df = load_merged()
    print(f"  통합 데이터 행 수: {len(df)}")

    save_csv(summarize_monthly(df), OUTPUT_DIR / "monthly_expense_summary.csv")
    save_csv(summarize_department(df), OUTPUT_DIR / "department_expense_summary.csv")
    save_csv(summarize_category(df), OUTPUT_DIR / "category_expense_summary.csv")
    save_csv(summarize_vendor_top10(df), OUTPUT_DIR / "vendor_top10_summary.csv")
    save_csv(list_duplicate_invoices(df), OUTPUT_DIR / "duplicate_invoice_list.csv")
    save_csv(summarize_data_quality(df), OUTPUT_DIR / "data_quality_summary.csv")

    print("[04] 완료. 이제 05_generate_report.py 를 실행하세요.")


if __name__ == "__main__":
    main()
