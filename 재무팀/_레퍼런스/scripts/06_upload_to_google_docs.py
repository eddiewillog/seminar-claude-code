"""
06_upload_to_google_docs.py

5단계에서 만든 Word 리포트(.docx)를 회사 Google Drive 에 업로드해서
Google Docs 로 변환한다. 업로드가 끝나면 공유 가능한 webViewLink 를 출력한다.

인증 흐름:
  - 진행자가 사전 발급한 OAuth client 파일을 ../_준비/credentials.json 에 둔다.
  - 첫 실행 시: 브라우저가 열려 회사 Google 계정으로 로그인 + 권한 허용.
  - 인증 토큰은 ../_준비/token.json 에 저장되어 다음 실행부터 자동 사용된다.
  - 토큰이 만료되면 자동 갱신 시도, 실패하면 다시 브라우저 인증.

의존성:
  pip install google-api-python-client google-auth-oauthlib

OAuth client 발급 방법은 ../_준비/README.md 참고.
"""

from datetime import datetime
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# 이 스크립트의 위치: _레퍼런스/scripts/06_..py
# 실제 사용 시에는 finance-practice/scripts/ 에서 동작한다고 가정한다.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORT_PATH = REPORTS_DIR / "finance_expense_report.docx"

# OAuth 자격 파일은 finance-practice/ 와 같은 레벨에 있는 _준비/ 폴더에 둔다.
# finance-practice/../_준비/  →  PROJECT_ROOT.parent / "_준비"
PREP_DIR = PROJECT_ROOT.parent / "_준비"
CREDENTIALS_PATH = PREP_DIR / "credentials.json"
TOKEN_PATH = PREP_DIR / "token.json"

# Drive 의 files.create 만 필요하면 drive.file 권한이면 충분하다.
# (이 앱이 만든 파일에 대해서만 접근 가능 — 최소 권한 원칙)
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

# Word 문서 mimeType
DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
# Google Docs 변환 대상 mimeType
GOOGLE_DOC_MIME = "application/vnd.google-apps.document"


def load_or_create_credentials() -> Credentials:
    """token.json 이 있으면 재사용, 없거나 만료되면 새로 인증한다."""
    creds: Credentials | None = None

    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
            return creds
        except Exception as e:
            print(f"  토큰 갱신 실패, 다시 인증한다: {e}")

    if not CREDENTIALS_PATH.exists():
        raise FileNotFoundError(
            f"OAuth 클라이언트 파일이 없다: {CREDENTIALS_PATH}\n"
            "진행자에게 _준비/credentials.json 발급을 요청하세요. "
            "발급 방법은 _준비/README.md 참고."
        )

    print("  브라우저가 열려 회사 Google 계정으로 로그인을 요청한다...")
    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
    creds = flow.run_local_server(port=0)
    TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    print(f"  인증 토큰 저장: {TOKEN_PATH.relative_to(PROJECT_ROOT.parent)}")
    return creds


def upload_as_google_doc(creds: Credentials, file_path: Path) -> dict:
    """주어진 docx 파일을 Google Docs 로 변환 업로드한다."""
    service = build("drive", "v3", credentials=creds)

    file_name = f"재무 비용 리포트 - {datetime.now().strftime('%Y-%m-%d')}"

    metadata = {
        "name": file_name,
        # 업로드 후 Google Docs 로 변환되도록 mimeType 지정
        "mimeType": GOOGLE_DOC_MIME,
    }

    media = MediaFileUpload(str(file_path), mimetype=DOCX_MIME, resumable=True)

    print(f"  업로드 중: {file_path.name} → \"{file_name}\"")
    uploaded = (
        service.files()
        .create(body=metadata, media_body=media, fields="id, name, webViewLink")
        .execute()
    )
    return uploaded


def main() -> None:
    print("[06] Google Docs 업로드를 시작한다.")

    if not REPORT_PATH.exists():
        raise FileNotFoundError(
            f"업로드할 Word 리포트가 없다: {REPORT_PATH}\n"
            "먼저 05_generate_report.py 를 실행하세요."
        )

    creds = load_or_create_credentials()
    result = upload_as_google_doc(creds, REPORT_PATH)

    print("  업로드 완료.")
    print(f"  Google Docs 파일명: {result.get('name')}")
    print(f"  공유 링크: {result.get('webViewLink')}")
    print("[06] 완료.")


if __name__ == "__main__":
    main()
