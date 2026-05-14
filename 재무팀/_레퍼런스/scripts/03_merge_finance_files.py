"""
03_merge_finance_files.py

02_inspect_input_files.py 가 만든 인벤토리(input_file_inventory.csv)를 보고,
status=="include" 인 파일만 읽어서 표준 컬럼으로 통합한다.

핵심 책임:
  - 다양한 컬럼명을 표준 컬럼명으로 매핑한다.
  - 날짜 컬럼을 datetime 으로 변환한다 (실패 시 별도 플래그).
  - 금액 컬럼을 숫자로 변환한다 (쉼표/원/문자열 제거, 실패 시 별도 플래그).
  - 원본 파일명을 source_file 컬럼에 남긴다.
  - 중복 invoice_no 여부를 표시한다.

출력:
  data/processed/merged_expenses.csv
  - 표준 컬럼 + date_parse_failed / amount_parse_failed / is_duplicate_invoice

원본 파일은 절대 수정하지 않는다 (읽기 전용).
"""

from pathlib import Path
import re

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
INVENTORY_PATH = PROCESSED_DIR / "input_file_inventory.csv"
OUT_PATH = PROCESSED_DIR / "merged_expenses.csv"


# 표준 컬럼명
STANDARD_COLUMNS = [
    "transaction_date",
    "department",
    "vendor",
    "category",
    "amount",
    "payment_method",
    "invoice_no",
    "memo",
    "source_file",
]


# 원본 컬럼명 → 표준 컬럼명 매핑 사전
# (소문자 변환 후 비교한다. 한글 키도 그대로 둔다.)
COLUMN_ALIASES: dict[str, str] = {
    # 거래일
    "거래일": "transaction_date",
    "거래 날짜": "transaction_date",
    "date": "transaction_date",
    # 부서
    "부서": "department",
    "dept": "department",
    # 거래처
    "거래처": "vendor",
    "vendor_name": "vendor",
    "vendor": "vendor",
    "업체명": "vendor",
    # 항목
    "항목": "category",
    "비용분류": "category",
    "category": "category",
    # 금액
    "금액": "amount",
    "amount_krw": "amount",
    "결제금액": "amount",
    "amount": "amount",
    # 결제수단
    "결제수단": "payment_method",
    "payment": "payment_method",
    "payment_method": "payment_method",
    # 인보이스 번호
    "인보이스번호": "invoice_no",
    "invoice": "invoice_no",
    "invoice_no": "invoice_no",
    "증빙번호": "invoice_no",
    # 비고
    "비고": "memo",
    "메모": "memo",
    "memo": "memo",
}


def load_inventory() -> pd.DataFrame:
    """02 단계가 만든 인벤토리를 읽어온다."""
    if not INVENTORY_PATH.exists():
        raise FileNotFoundError(
            f"인벤토리 파일이 없다: {INVENTORY_PATH}\n"
            "먼저 02_inspect_input_files.py 를 실행하세요."
        )
    return pd.read_csv(INVENTORY_PATH)


def read_raw_file(path: Path) -> pd.DataFrame:
    """파일 확장자에 맞게 읽는다. 원본은 수정하지 않는다."""
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"지원하지 않는 형식: {path.name}")


def normalize_columns(df: pd.DataFrame, source_file: str) -> pd.DataFrame:
    """원본 컬럼명을 표준 컬럼명으로 바꾸고, 빠진 컬럼은 NaN으로 채운다."""
    # 컬럼명을 좌우 공백 정도만 정리한다 (의미를 바꾸지 않는 범위).
    df = df.rename(columns=lambda c: str(c).strip())

    # 매핑 사전을 그대로 적용 (없는 키는 그대로 유지)
    df = df.rename(columns={c: COLUMN_ALIASES.get(c, c) for c in df.columns})

    # 표준 외 컬럼은 버린다. 분석에 쓰지 않기 때문.
    keep_cols = [c for c in df.columns if c in STANDARD_COLUMNS]
    df = df[keep_cols].copy()

    # 빠진 표준 컬럼은 빈 값으로 채운다.
    for col in STANDARD_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA

    df["source_file"] = source_file
    return df[STANDARD_COLUMNS]


_AMOUNT_CLEAN_RE = re.compile(r"[^\d\-]")


def clean_amount(value) -> tuple[float | None, bool]:
    """
    금액을 float 으로 정리한다.
    반환: (값, 실패여부)
      - 실패한 경우 (None, True)
    """
    if pd.isna(value):
        return None, True
    if isinstance(value, (int, float)):
        return float(value), False

    text = str(value).strip()
    if not text:
        return None, True

    # 쉼표, '원', 공백, 통화기호 등을 모두 제거
    cleaned = _AMOUNT_CLEAN_RE.sub("", text)
    if not cleaned or cleaned == "-":
        return None, True

    try:
        return float(cleaned), False
    except ValueError:
        return None, True


def clean_date(value) -> tuple[pd.Timestamp | None, bool]:
    """
    날짜 문자열을 datetime 으로 정리한다.
    pandas to_datetime 의 다양한 추론을 활용하되, 실패 플래그를 따로 기록한다.
    """
    if pd.isna(value):
        return None, True

    text = str(value).strip()
    # '2026.03.05' 같은 점 구분 표기를 슬래시로 바꿔 추론을 돕는다.
    text = text.replace(".", "-")

    parsed = pd.to_datetime(text, errors="coerce", dayfirst=False)
    if pd.isna(parsed):
        # 미국식 M/D/YYYY 가능성도 한 번 더 시도
        parsed = pd.to_datetime(text, errors="coerce", dayfirst=False, format="mixed")

    if pd.isna(parsed):
        return None, True
    return parsed, False


def merge_all(inventory: pd.DataFrame) -> pd.DataFrame:
    """include 파일만 모두 읽어 표준 형태로 합친다."""
    include_files = inventory[inventory["status"] == "include"]["file_name"].tolist()
    if not include_files:
        print("  ! 분석 대상 파일이 없다. 02 단계의 분류 결과를 확인하세요.")
        return pd.DataFrame(columns=STANDARD_COLUMNS)

    frames: list[pd.DataFrame] = []
    for file_name in include_files:
        src = PROJECT_ROOT / file_name
        if not src.exists():
            print(f"  ! 원본 파일이 사라졌다: {file_name}")
            continue

        print(f"  읽는 중: {file_name}")
        raw = read_raw_file(src)
        normalized = normalize_columns(raw, source_file=file_name)
        frames.append(normalized)

    if not frames:
        return pd.DataFrame(columns=STANDARD_COLUMNS)

    merged = pd.concat(frames, ignore_index=True)
    return merged


def add_quality_flags(df: pd.DataFrame) -> pd.DataFrame:
    """날짜/금액 변환 결과와 중복 인보이스 여부를 플래그로 붙인다."""
    # 금액 정리
    cleaned_amounts = df["amount"].apply(clean_amount)
    df["amount"] = [v for v, _ in cleaned_amounts]
    df["amount_parse_failed"] = [failed for _, failed in cleaned_amounts]

    # 날짜 정리
    cleaned_dates = df["transaction_date"].apply(clean_date)
    df["transaction_date"] = [v for v, _ in cleaned_dates]
    df["date_parse_failed"] = [failed for _, failed in cleaned_dates]

    # 중복 인보이스: 비어 있지 않은 invoice_no 중 2회 이상 등장한 것
    invoice_series = df["invoice_no"].fillna("").astype(str).str.strip()
    counts = invoice_series.value_counts()
    duplicated_set = set(counts[(counts > 1) & (counts.index != "")].index)
    df["is_duplicate_invoice"] = invoice_series.isin(duplicated_set)

    return df


def main() -> None:
    print("[03] 파일 통합 작업을 시작한다.")
    inventory = load_inventory()

    merged = merge_all(inventory)
    if merged.empty:
        print("  ! 통합 결과가 비어 있다.")
        return

    merged = add_quality_flags(merged)

    # 정렬: 날짜 → source_file 순
    merged = merged.sort_values(
        by=["transaction_date", "source_file"], na_position="last"
    ).reset_index(drop=True)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUT_PATH, index=False, encoding="utf-8-sig")

    total = len(merged)
    bad_date = int(merged["date_parse_failed"].sum())
    bad_amt = int(merged["amount_parse_failed"].sum())
    dup = int(merged["is_duplicate_invoice"].sum())

    print(f"  통합 행수: {total}")
    print(f"  날짜 변환 실패: {bad_date}건")
    print(f"  금액 변환 실패: {bad_amt}건")
    print(f"  중복 인보이스(중복으로 표시된 행 수): {dup}건")
    print(f"  저장됨: {OUT_PATH.relative_to(PROJECT_ROOT)}")
    print("[03] 완료. 이제 04_create_summary_tables.py 를 실행하세요.")


if __name__ == "__main__":
    main()
