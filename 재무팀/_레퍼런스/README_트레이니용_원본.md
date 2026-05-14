# 재무 비용 정리 실습 프로젝트 (finance-practice)

> 재무팀 초보 실무자를 위한 Claude Code 실습 예제다.
> Excel/CSV로 흩어진 비용 파일을 자동으로 정리·통합·요약·리포트화하는 흐름을 따라가 본다.

---

## 1. 프로젝트 소개

이 프로젝트는 "정리되지 않은 폴더"에서 시작한다.
실제 재무팀이 그동안 Excel/CSV 파일을 수기로 관리해 온 상황을 그대로 가정한다.

스크립트를 순서대로 실행하면 다음 작업이 자동으로 끝난다.

1. 흩어진 파일 자동 탐색
2. 분석 대상 파일과 제외 대상 파일 자동 구분
3. 표준 컬럼/날짜/금액 형식으로 정리
4. 월별, 부서별, 항목별, 거래처별 요약 테이블 생성
5. 데이터 품질 이슈(중복 인보이스, 변환 실패) 탐지
6. 재무팀 보고용 Markdown 리포트 자동 생성

---

## 2. 이 프로젝트가 해결하는 재무팀 문제

- 매월 받는 비용 파일의 **컬럼명이 매번 다르다**.
- 어떤 파일은 날짜가 `2026-01-05`, 어떤 파일은 `2026/01/05`, 어떤 파일은 `2026.01.05`.
- 금액이 숫자로 들어오기도 하고 `"1,200,000원"` 처럼 문자열로 들어오기도 한다.
- 거래처 표기가 미묘하게 다르다.
- 같은 인보이스가 두 파일에 모두 들어 있어 **중복 결제 의심** 검증이 필요하다.
- 매월 보고서를 수기로 만들기에는 시간이 너무 많이 든다.

이 실습은 위 문제들을 한 번에 처리하는 **자동화 파이프라인** 예시를 제공한다.

---

## 3. 시작 상태

이 프로젝트는 "깔끔하게 정리된 개발 프로젝트"가 아니라,
**파일이 그냥 한 폴더에 펼쳐져 있는 상태**에서 출발한다.

`01_generate_messy_sample_files.py` 를 한 번 실행하면 아래 모습이 된다.

```
finance-practice/
├── 1월비용.xlsx
├── 2월 비용 정리.xlsx
├── 3월_비용_최종.xlsx
├── 거래처지급내역_1.csv
├── 거래처 지급 내역 2.csv
├── 임시메모.txt
├── old_backup.xlsx
├── CLAUDE.md
├── README.md
├── requirements.txt
└── scripts/
    ├── 01_generate_messy_sample_files.py
    ├── 02_inspect_input_files.py
    ├── 03_merge_finance_files.py
    ├── 04_create_summary_tables.py
    └── 05_generate_report.py
```

`data/`, `reports/` 폴더는 **처음에는 없다**. 02번 스크립트가 자동으로 만든다.

---

## 4. 전체 자동화 흐름

```
[루트의 원본 파일]
        │
        ▼
01_generate_messy_sample_files.py   ← 실습용 지저분한 샘플 데이터 생성
        │
        ▼
02_inspect_input_files.py           ← 파일 점검, 분류, 폴더 자동 생성, 원본 백업
        │
        ▼
03_merge_finance_files.py           ← 표준 컬럼/날짜/금액 정리, 통합, 품질 플래그
        │
        ▼
04_create_summary_tables.py         ← 월별/부서별/항목별/거래처 Top 10/품질 요약
        │
        ▼
05_generate_report.py               ← 재무팀 보고용 Markdown 리포트 생성
```

---

## 5. 실행 전 준비

1. Python 3.11 이상을 사용한다.
2. 터미널에서 이 프로젝트 폴더로 이동한다.

```bash
cd 재무팀/finance-practice
```

> 본 저장소는 부서별 폴더 구조를 쓰고 있어 한 단계 들어와야 한다.

---

## 6. 패키지 설치 방법

가상환경을 만든 뒤 의존성을 설치한다.

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

---

## 7. 실행 순서

아래 순서대로 한 줄씩 실행하면 된다.

```bash
python scripts/01_generate_messy_sample_files.py
python scripts/02_inspect_input_files.py
python scripts/03_merge_finance_files.py
python scripts/04_create_summary_tables.py
python scripts/05_generate_report.py
```

각 단계가 끝나면 다음 단계 안내가 콘솔에 출력된다.

---

## 8. 각 스크립트 설명

| 스크립트 | 역할 |
| --- | --- |
| `01_generate_messy_sample_files.py` | 실습용 합성 원본 데이터(Excel/CSV)를 프로젝트 루트에 생성한다. |
| `02_inspect_input_files.py` | 루트 파일을 점검해 분석 대상/제외 대상을 구분하고, 작업 폴더를 자동 생성하며 원본을 `data/raw_snapshot/` 에 복사한다. |
| `03_merge_finance_files.py` | 인벤토리의 include 파일만 읽어 표준 컬럼으로 통합하고, 날짜/금액/중복 인보이스 품질 플래그를 붙인다. |
| `04_create_summary_tables.py` | 월별, 부서별, 항목별, 거래처 Top 10, 중복 인보이스, 품질 이슈 요약 CSV를 만든다. |
| `05_generate_report.py` | 위 결과를 모아 `reports/finance_expense_report.md` 보고서를 만든다. |

---

## 9. 결과 파일 설명

| 경로 | 내용 |
| --- | --- |
| `data/raw_snapshot/` | 원본 파일의 백업 복사본 (수정 방지용) |
| `data/processed/input_file_inventory.csv` | 어떤 파일을 분석하고 무엇을 제외했는지 |
| `data/processed/merged_expenses.csv` | 표준 컬럼으로 통합된 전체 데이터 + 품질 플래그 |
| `data/output/monthly_expense_summary.csv` | 월별 총 비용 |
| `data/output/department_expense_summary.csv` | 부서별 총 비용 |
| `data/output/category_expense_summary.csv` | 비용 항목별 총 비용 |
| `data/output/vendor_top10_summary.csv` | 거래처 지출 Top 10 |
| `data/output/duplicate_invoice_list.csv` | 중복 가능성이 있는 인보이스 목록 |
| `data/output/data_quality_summary.csv` | 데이터 품질 이슈 종합 |
| `reports/finance_expense_report.md` | 재무팀 보고용 최종 Markdown 리포트 |

---

## 10. 원본 파일을 수정하지 않는 이유

재무 데이터는 감사·증빙의 근거가 되기 때문에 **원본은 절대 변경하지 않는 것**이 원칙이다.

- 원본을 직접 수정하면 변경 이력이 사라진다.
- 컬럼명을 바꾸면 다음 달 원본 양식과 어긋난다.
- 자동화는 항상 "원본 → 복사본 → 정리본" 흐름으로 동작해야 한다.

그래서 이 프로젝트는 다음을 보장한다.

- 02번 스크립트가 원본을 `data/raw_snapshot/` 에 복사해 둔다.
- 03번 이후 모든 스크립트는 **읽기 전용**으로만 원본을 사용한다.
- 정리된 결과는 모두 `data/processed/`, `data/output/`, `reports/` 에 저장된다.

---

## 11. Google Sheets 데이터를 사용할 경우

이 초보용 실습에서는 **Google Sheets API를 직접 연결하지 않는다**.
대신 다음 방법을 권장한다.

1. Google Sheets에서 메뉴: **파일 → 다운로드 → CSV 또는 Microsoft Excel(.xlsx)**
2. 다운로드한 파일을 이 프로젝트 폴더(`finance-practice/`)에 그대로 넣는다.
3. 파일명에 `backup`, `old`, `임시`, `temp` 같은 키워드가 들어가지 않도록 정리한다.
4. 다시 `02 → 03 → 04 → 05` 순서로 스크립트를 실행한다.

> 추후 확장 과제로 `gspread` 같은 라이브러리를 이용한 Google Sheets API 직접 연동을 추가해도 좋다.

---

## 12. Claude Code로 해볼 수 있는 연습 과제

이 프로젝트는 그 자체로도 의미가 있지만, Claude Code 실습을 위한 출발점으로 더 가치 있다.
아래 과제를 Claude Code에게 시켜 보자.

1. **파일 추가 실습**
   - 직접 만든 4월 비용 Excel 파일을 루트에 넣고, 같은 파이프라인이 잘 동작하는지 확인한다.

2. **컬럼 매핑 추가 실습**
   - 새 파일이 `"이체일"` 같은 새로운 컬럼명을 사용한다면, `03_merge_finance_files.py`의 `COLUMN_ALIASES`에 매핑을 추가한다.

3. **요약 테이블 추가 실습**
   - "결제수단별 비용 합계" 요약을 추가하고 리포트에도 섹션으로 넣는다.

4. **중복 감지 강화**
   - 같은 (vendor, amount, transaction_date) 조합도 중복 후보로 잡아보는 규칙을 추가한다.

5. **시각화 확장**
   - matplotlib 으로 월별 추이 그래프 PNG를 만들어 `reports/` 에 함께 저장한다.

6. **Google Sheets API 직접 연동**
   - `gspread`를 활용해 특정 Sheet ID에서 직접 데이터를 받아오도록 만든다.

7. **자동화 스크립트 통합**
   - `run_all.py`를 만들어 01~05를 한 번에 실행한다.

각 과제는 본 프로젝트의 `CLAUDE.md` 원칙을 지키며 진행한다.
특히 **원본 수정 금지**, **합성 데이터만 사용**, **단순한 코드 유지** 를 잊지 말 것.
