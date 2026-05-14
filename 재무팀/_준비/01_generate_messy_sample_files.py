"""
01_generate_messy_sample_files.py  (워크숍 셋업 전용)

이 스크립트는 워크숍 진행자가 **실습 시작 전에 한 번** 실행한다.
재무팀이 평소 사용하던 "정리되지 않은 폴더" 상태를 재현하기 위해,
형제 폴더 ../finance-practice/ 안에 지저분한 합성 Excel/CSV 파일을 생성한다.

생성 위치: ../finance-practice/
  - 1월비용.xlsx
  - 2월 비용 정리.xlsx
  - 3월_비용_최종.xlsx
  - 거래처지급내역_1.csv
  - 거래처 지급 내역 2.csv
  - 임시메모.txt
  - old_backup.xlsx

주의:
  - 모든 데이터는 합성 데이터다.
  - 실존 기업/거래처/개인 정보를 사용하지 않는다.
  - 이 스크립트는 워크숍 시작 전 폴더 초기화 용도다.
  - 실습 단계(클로드코드와의 대화)에서는 finance-practice/ 안의 원본을
    절대 수정하지 않는다.

사용법:
  cd 재무팀/_준비
  python 01_generate_messy_sample_files.py
"""

from pathlib import Path
import random

import pandas as pd


# 재현 가능성을 위해 시드를 고정한다.
random.seed(42)


# 이 스크립트는 _준비/ 안에 있고, 생성 대상은 형제 폴더 finance-practice/ 다.
# _준비/01_...py -> ../finance-practice/
PROJECT_ROOT = Path(__file__).resolve().parent.parent / "finance-practice"


# 합성 데이터에 사용할 가짜 거래처/부서/항목 풀
FAKE_VENDORS = [
    "가나다물산",
    "라마바상사",
    "사아자유통",
    "차카타엔지니어링",
    "파하공업사",
    "푸른하늘카페",
    "북극별인쇄소",
    "맑은샘오피스",
]

DEPARTMENTS = ["경영지원", "영업1팀", "영업2팀", "개발팀", "디자인팀", "마케팅팀"]

CATEGORIES = [
    "사무용품",
    "식대",
    "교통비",
    "출장비",
    "광고선전비",
    "소모품비",
    "통신비",
    "교육훈련비",
]

PAYMENT_METHODS = ["법인카드", "계좌이체", "현금", "법인카드(개인)"]


def _make_row(year: int, month: int, day_max: int) -> dict:
    """공통 거래 데이터 한 줄을 만든다 (표준 형태)."""
    day = random.randint(1, day_max)
    return {
        "date": f"{year}-{month:02d}-{day:02d}",
        "department": random.choice(DEPARTMENTS),
        "vendor": random.choice(FAKE_VENDORS),
        "category": random.choice(CATEGORIES),
        "amount": random.randint(15_000, 1_500_000),
        "payment_method": random.choice(PAYMENT_METHODS),
        "invoice_no": f"INV-{year}{month:02d}-{random.randint(1000, 9999)}",
        "memo": random.choice(["", "정기지출", "긴급", "회식", "출장정산", ""]),
    }


def _build_base_rows(year: int, month: int, day_max: int, n: int) -> list[dict]:
    return [_make_row(year, month, day_max) for _ in range(n)]


def generate_january_xlsx(root: Path) -> None:
    """1월비용.xlsx - 한글 컬럼명, 날짜는 'YYYY-MM-DD' 문자열."""
    rows = _build_base_rows(2026, 1, 31, 18)

    # 일부러 중복 인보이스를 한 건 만든다.
    rows[5]["invoice_no"] = rows[2]["invoice_no"]

    df = pd.DataFrame(rows).rename(
        columns={
            "date": "거래일",
            "department": "부서",
            "vendor": "거래처",
            "category": "항목",
            "amount": "금액",
            "payment_method": "결제수단",
            "invoice_no": "인보이스번호",
            "memo": "비고",
        }
    )

    out_path = root / "1월비용.xlsx"
    df.to_excel(out_path, index=False)
    print(f"  생성: {out_path.name} ({len(df)}행)")


def generate_february_xlsx(root: Path) -> None:
    """2월 비용 정리.xlsx - 컬럼명 영/한 혼용, 날짜 'YYYY/MM/DD' 형식."""
    rows = _build_base_rows(2026, 2, 28, 16)

    # 날짜 형식을 슬래시로 바꾸어 형식 불일치를 만든다.
    for r in rows:
        y, m, d = r["date"].split("-")
        r["date"] = f"{y}/{m}/{d}"

    # 금액을 일부 쉼표 포함 문자열로 변환한다.
    for i, r in enumerate(rows):
        if i % 3 == 0:
            r["amount"] = f"{r['amount']:,}"

    df = pd.DataFrame(rows).rename(
        columns={
            "date": "date",
            "department": "dept",
            "vendor": "vendor_name",
            "category": "비용분류",
            "amount": "amount_krw",
            "payment_method": "payment",
            "invoice_no": "invoice",
            "memo": "메모",
        }
    )

    out_path = root / "2월 비용 정리.xlsx"
    df.to_excel(out_path, index=False)
    print(f"  생성: {out_path.name} ({len(df)}행)")


def generate_march_xlsx(root: Path) -> None:
    """3월_비용_최종.xlsx - 또 다른 컬럼명, 날짜 '2026.03.05' 형식, 금액 문자열."""
    rows = _build_base_rows(2026, 3, 31, 20)

    for r in rows:
        y, m, d = r["date"].split("-")
        r["date"] = f"{y}.{m}.{d}"
        # 금액을 모두 문자열로 (일부는 ' 원' 표기까지 붙여서 더러움 강화)
        if random.random() < 0.4:
            r["amount"] = f"{r['amount']:,}원"
        else:
            r["amount"] = str(r["amount"])

    # 중복 invoice_no 한 건 더
    rows[10]["invoice_no"] = rows[1]["invoice_no"]

    df = pd.DataFrame(rows).rename(
        columns={
            "date": "거래 날짜",
            "department": "부서",
            "vendor": "업체명",
            "category": "항목",
            "amount": "결제금액",
            "payment_method": "결제수단",
            "invoice_no": "증빙번호",
            "memo": "비고",
        }
    )

    out_path = root / "3월_비용_최종.xlsx"
    df.to_excel(out_path, index=False)
    print(f"  생성: {out_path.name} ({len(df)}행)")


def generate_vendor_csv_1(root: Path) -> None:
    """거래처지급내역_1.csv - 영어 컬럼명, 날짜 'YYYY-MM-DD'."""
    rows = _build_base_rows(2026, 1, 31, 12) + _build_base_rows(2026, 2, 28, 10)

    df = pd.DataFrame(rows).rename(
        columns={
            "date": "date",
            "department": "dept",
            "vendor": "vendor_name",
            "category": "category",
            "amount": "amount_krw",
            "payment_method": "payment",
            "invoice_no": "invoice",
            "memo": "memo",
        }
    )

    out_path = root / "거래처지급내역_1.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"  생성: {out_path.name} ({len(df)}행)")


def generate_vendor_csv_2(root: Path) -> None:
    """거래처 지급 내역 2.csv - 한글 컬럼명, 날짜 '5/3/2026' 형식, 금액 쉼표 포함."""
    rows = _build_base_rows(2026, 3, 31, 14)

    for r in rows:
        y, m, d = r["date"].split("-")
        # 미국식 M/D/YYYY 비슷한 어색한 표기를 일부러 섞는다.
        r["date"] = f"{int(m)}/{int(d)}/{y}"
        r["amount"] = f"{r['amount']:,}"

    df = pd.DataFrame(rows).rename(
        columns={
            "date": "거래일",
            "department": "부서",
            "vendor": "거래처",
            "category": "비용분류",
            "amount": "금액",
            "payment_method": "결제수단",
            "invoice_no": "인보이스번호",
            "memo": "비고",
        }
    )

    out_path = root / "거래처 지급 내역 2.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"  생성: {out_path.name} ({len(df)}행)")


def generate_memo_txt(root: Path) -> None:
    """임시메모.txt - 분석 대상이 아닌 일반 텍스트 파일."""
    out_path = root / "임시메모.txt"
    out_path.write_text(
        "재무팀 인수인계 메모\n"
        "----------------------\n"
        "- 1월~3월 비용 정리 파일은 각 월별 Excel로 관리 중\n"
        "- 거래처 지급 내역은 두 개 CSV로 나뉘어 있음\n"
        "- old_backup.xlsx는 작년 백업이라 분석에서 빼야 함\n",
        encoding="utf-8",
    )
    print(f"  생성: {out_path.name} (텍스트 메모)")


def generate_old_backup_xlsx(root: Path) -> None:
    """old_backup.xlsx - 분석 대상에서 제외해야 하는 백업 파일."""
    rows = _build_base_rows(2025, 12, 31, 10)

    df = pd.DataFrame(rows).rename(
        columns={
            "date": "date",
            "department": "dept",
            "vendor": "vendor",
            "category": "category",
            "amount": "amount",
            "payment_method": "payment",
            "invoice_no": "invoice",
            "memo": "memo",
        }
    )

    out_path = root / "old_backup.xlsx"
    df.to_excel(out_path, index=False)
    print(f"  생성: {out_path.name} (백업 파일, 분석 대상 아님)")


def main() -> None:
    print("[01] 지저분한 샘플 파일 생성을 시작한다.")
    print(f"     대상 폴더: {PROJECT_ROOT}")

    # 프로젝트 루트가 없으면 만들어 둔다 (보통은 이미 존재).
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)

    generate_january_xlsx(PROJECT_ROOT)
    generate_february_xlsx(PROJECT_ROOT)
    generate_march_xlsx(PROJECT_ROOT)
    generate_vendor_csv_1(PROJECT_ROOT)
    generate_vendor_csv_2(PROJECT_ROOT)
    generate_memo_txt(PROJECT_ROOT)
    generate_old_backup_xlsx(PROJECT_ROOT)

    print("[01] 완료. 이제 02_inspect_input_files.py 를 실행하세요.")


if __name__ == "__main__":
    main()
