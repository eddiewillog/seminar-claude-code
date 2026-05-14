"""
02_inspect_input_files.py

프로젝트 루트에 흩어져 있는 파일을 점검한다.
- Excel/CSV 파일만 분석 후보로 분류한다.
- 백업/임시 파일은 자동으로 제외 처리한다.
- 필요한 폴더(data/raw_snapshot, data/processed, data/output, reports)를 만든다.
- 원본 파일은 절대 수정하지 않으며, 안전을 위해 data/raw_snapshot/ 에 복사본을 둔다.
- 점검 결과는 data/processed/input_file_inventory.csv 로 저장한다.

이 스크립트는 "어떤 파일을 분석할지"를 결정하는 게이트 역할이므로,
이후 03_merge_finance_files.py 는 여기서 만든 inventory를 기준으로 동작한다.
"""

from pathlib import Path
import shutil

import pandas as pd


# 프로젝트 루트 = scripts/ 의 부모
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 작업 폴더 경로 (없으면 만든다)
DATA_DIR = PROJECT_ROOT / "data"
RAW_SNAPSHOT_DIR = DATA_DIR / "raw_snapshot"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = DATA_DIR / "output"
REPORTS_DIR = PROJECT_ROOT / "reports"

# 분석 후보로 받아주는 확장자
SUPPORTED_EXTS = {".xlsx", ".xls", ".csv"}

# 파일명에 이 키워드가 들어가면 분석에서 제외한다.
EXCLUDE_KEYWORDS = ["backup", "백업", "old", "임시", "temp", "tmp", "archive"]


def ensure_working_folders() -> None:
    """data/, reports/ 하위 작업 폴더를 자동 생성한다."""
    for folder in [RAW_SNAPSHOT_DIR, PROCESSED_DIR, OUTPUT_DIR, REPORTS_DIR]:
        folder.mkdir(parents=True, exist_ok=True)
        print(f"  준비됨: {folder.relative_to(PROJECT_ROOT)}")


def list_root_files() -> list[Path]:
    """프로젝트 루트의 파일만 반환한다 (하위 폴더는 보지 않는다)."""
    files = []
    for p in sorted(PROJECT_ROOT.iterdir()):
        # 디렉토리, 숨김 파일, 스크립트성 산출물은 무시
        if p.is_dir():
            continue
        if p.name.startswith("."):
            continue
        if p.name in {"README.md", "CLAUDE.md", "requirements.txt"}:
            continue
        files.append(p)
    return files


def classify_file(path: Path) -> tuple[str, str]:
    """
    파일 하나를 보고 (status, note) 를 돌려준다.
    - status: "include" 또는 "exclude"
    - note: 사람이 읽을 수 있는 판단 사유
    """
    name_lower = path.name.lower()

    # 1) 확장자가 지원 형식이 아니면 제외
    if path.suffix.lower() not in SUPPORTED_EXTS:
        return "exclude", "지원하지 않는 파일 형식"

    # 2) 파일명에 백업/임시 키워드가 있으면 제외
    for kw in EXCLUDE_KEYWORDS:
        if kw.lower() in name_lower:
            return "exclude", f"파일명에 '{kw}' 키워드 포함 → 백업/임시 파일로 추정"

    return "include", "분석 대상"


def read_columns_safely(path: Path) -> tuple[int | None, list[str]]:
    """
    Excel/CSV 파일에서 행 수와 컬럼명을 읽어온다. 실패하면 (None, [])를 돌려준다.
    여기서는 절대 원본을 수정하지 않는다 (read-only).
    """
    try:
        if path.suffix.lower() in {".xlsx", ".xls"}:
            df = pd.read_excel(path)
        elif path.suffix.lower() == ".csv":
            df = pd.read_csv(path)
        else:
            return None, []
        return len(df), list(df.columns)
    except Exception as e:
        print(f"    ! {path.name} 읽기 실패: {e}")
        return None, []


def snapshot_originals(files: list[Path]) -> None:
    """원본을 절대 수정하지 않기 위해 data/raw_snapshot/ 에 복사본을 둔다."""
    for f in files:
        dst = RAW_SNAPSHOT_DIR / f.name
        # 이미 동일 이름의 스냅샷이 있으면 덮어쓴다 (재실행 안정성).
        shutil.copy2(f, dst)


def main() -> None:
    print("[02] 입력 파일 점검을 시작한다.")
    print(f"     스캔 대상 폴더: {PROJECT_ROOT}")

    # 1) 작업 폴더부터 만들어 둔다.
    ensure_working_folders()

    # 2) 루트 파일을 모은다.
    files = list_root_files()
    if not files:
        print("  ! 루트에 분석할 파일이 없다. 먼저 01_generate_messy_sample_files.py 를 실행하세요.")
        return

    # 3) 원본 백업 (수정 방지용 안전망)
    snapshot_originals(files)
    print(f"  원본 백업 완료: {RAW_SNAPSHOT_DIR.relative_to(PROJECT_ROOT)}")

    # 4) 파일별 점검 결과를 모은다.
    inventory_rows: list[dict] = []
    for f in files:
        status, note = classify_file(f)

        if status == "include":
            row_count, columns = read_columns_safely(f)
        else:
            row_count, columns = None, []

        inventory_rows.append(
            {
                "file_name": f.name,
                "file_type": f.suffix.lower().lstrip("."),
                "row_count": row_count if row_count is not None else "",
                "columns": ", ".join(columns) if columns else "",
                "status": status,
                "note": note,
            }
        )

    inventory = pd.DataFrame(inventory_rows)

    # 5) 결과 저장 (Excel로 쉽게 열어볼 수 있게 CSV)
    out_path = PROCESSED_DIR / "input_file_inventory.csv"
    inventory.to_csv(out_path, index=False, encoding="utf-8-sig")

    # 6) 사람이 보기 좋게 요약 출력
    include_cnt = (inventory["status"] == "include").sum()
    exclude_cnt = (inventory["status"] == "exclude").sum()
    print(f"  점검 완료: 총 {len(inventory)}개 파일 (분석 {include_cnt} / 제외 {exclude_cnt})")
    print(f"  저장됨: {out_path.relative_to(PROJECT_ROOT)}")
    print("[02] 완료. 이제 03_merge_finance_files.py 를 실행하세요.")


if __name__ == "__main__":
    main()
