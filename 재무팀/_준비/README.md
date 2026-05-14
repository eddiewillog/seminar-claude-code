# _준비 — 진행자용 워크숍 셋업

이 폴더는 **워크숍 진행자가 트레이니 입장하기 전에** 사용하는 자료를 모아둔 곳이다.
트레이니는 이 폴더 안의 파일을 직접 만들지 않는다. 진행자가 미리 준비해 둔다.

| 파일 | 누가 만드나 | 언제 사용하나 |
| --- | --- | --- |
| `01_generate_messy_sample_files.py` | 이미 제공됨 | 매 트레이니 시작 전 폴더 초기화 |
| `02_convert_guide_to_docx.py` | 이미 제공됨 | `실습_가이드.md` 수정 후 `.docx` 재생성 |
| `credentials.json` | **진행자가 직접 발급** | 7단계 Google Docs 업로드용 |
| `token.json` | 트레이니 첫 인증 시 자동 생성 | 다음 실행부터 자동 인증 |

---

## A. 폴더 초기화 (매 트레이니 시작 전)

```bash
cd 재무팀/_준비
python 01_generate_messy_sample_files.py
```

이 명령으로 `재무팀/finance-practice/` 가 "지저분한 시작 상태"로 돌아간다.

---

## A-2. 가이드 워드 파일 재생성 (가이드 수정 후)

`재무팀/실습_가이드.md` 를 편집한 뒤, 트레이니에게 배포할 워드 파일을 갱신하려면:

```bash
cd 재무팀/_준비
python 02_convert_guide_to_docx.py
```

이 명령은 `재무팀/실습_가이드.docx` 를 새로 만들거나 덮어쓴다.
트레이니에게는 `.md` 와 `.docx` 둘 중 편한 형태로 배포하면 된다.

---

## B. Google OAuth 자격(credentials.json) 발급 (워크숍 첫 셋업 시 한 번)

7단계에서 트레이니가 Word 리포트를 회사 Google Drive 에 업로드하려면
**OAuth client 자격 파일**이 필요하다. 진행자가 한 번만 발급해서 이 폴더에 두면, 모든 트레이니가 같은 파일을 공유한다.

### B-1. Google Cloud 프로젝트 만들기

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 상단 프로젝트 드롭다운에서 **새 프로젝트** 생성
   (예: `claude-code-finance-seminar`)
3. 결제 계정 연결은 필요 없다 (Drive API 사용량 무료 한도 내).

### B-2. Drive API 사용 설정

1. 좌측 메뉴 → **API 및 서비스 > 라이브러리**
2. "Google Drive API" 검색 → **사용 설정**

### B-3. OAuth 동의 화면 구성

1. 좌측 메뉴 → **API 및 서비스 > OAuth 동의 화면**
2. **User Type**:
   - 회사가 Google Workspace 를 쓰면 **Internal** (사내 사용자만, 가장 깔끔)
   - 일반 Gmail 도 섞여 있으면 **External** (이 경우 테스트 사용자 등록 필요)
3. 앱 정보 입력:
   - 앱 이름: `Finance Seminar Uploader`
   - 사용자 지원 이메일, 개발자 연락처: 진행자 이메일
4. 범위(Scopes): 기본 그대로 (스크립트에서 `drive.file` 만 요청)
5. **External** 인 경우 **테스트 사용자** 탭에서 트레이니들의 Google 계정 이메일을 미리 추가한다.

### B-4. OAuth client ID 만들기

1. 좌측 메뉴 → **API 및 서비스 > 사용자 인증 정보**
2. **+ 사용자 인증 정보 만들기** → **OAuth 클라이언트 ID**
3. **애플리케이션 유형**: **데스크톱 앱**
4. 이름: `Finance Seminar Desktop Client`
5. 생성 후 **JSON 다운로드** 버튼 클릭
6. 다운로드한 파일을 이 폴더에 **`credentials.json`** 이라는 이름으로 저장한다.

```
재무팀/_준비/credentials.json
```

### B-5. 동작 확인 (진행자 본인 계정으로 미리 테스트)

진행자가 워크숍 전에 한 번 시험 실행해서, 인증 흐름이 정상인지 확인한다.

```bash
# 실습 폴더에서 (트레이니와 동일한 위치)
cd ../finance-practice

# 가이드 1~6단계까지 실행해서 Word 리포트 만든 뒤
# 7단계와 동일한 스크립트 실행 (또는 클로드코드에 7단계 프롬프트 입력)
python ../_레퍼런스/scripts/06_upload_to_google_docs.py
```

- 브라우저가 열리고 Google 로그인 → 권한 허용
- 콘솔에 `webViewLink` 출력 → 클릭해서 Google Docs 가 잘 열리는지 확인
- `_준비/token.json` 이 생성됐는지 확인

> ⚠️ 트레이니 워크숍 시작 전에는 **`_준비/token.json` 을 삭제**해 둔다.
> 그래야 트레이니가 본인 계정으로 처음부터 인증 흐름을 경험할 수 있다.

---

## C. 트러블슈팅 (자주 보고되는 문제)

### "Access blocked: This app's request is invalid"

→ External 모드인데 테스트 사용자에 트레이니 이메일이 등록 안 됨.
   OAuth 동의 화면 > 테스트 사용자 탭에서 추가한다.

### "이 앱은 인증되지 않았습니다" 경고

→ External + 미게시 상태에서 정상이다. **고급 > 안전하지 않은 페이지로 이동** 클릭하면 계속 진행된다.
   사내 워크숍 용도라면 게시하지 않아도 무방.

### Workspace 관리자가 외부 OAuth 앱을 막아둠

→ Workspace 관리자에게 "Finance Seminar Uploader (client ID: xxxxx)" 를 허용 목록에 추가 요청하거나, Internal 모드로 재발급한다.

### `token.json` 이 다른 사람 계정으로 묶여 있을 때

→ 단순히 `_준비/token.json` 을 지우고 다시 실행하면 새로 인증한다.

---

## D. 워크숍 후 정리

다음 회차 시작 전 한 번에 정리하려면:

```bash
cd 재무팀
# 트레이니 작업물 초기화
rm -rf finance-practice/data finance-practice/reports
# OAuth 토큰 초기화 (credentials.json 은 유지)
rm -f _준비/token.json
# 샘플 데이터 새로 생성
python _준비/01_generate_messy_sample_files.py
```

---

## E. 보안 메모

- `credentials.json` 은 **OAuth client ID/secret** 이 들어있다. 외부로 유출되면 안 된다.
  - GitHub 등 공개 저장소에 커밋하지 말 것 (`.gitignore` 에 추가 권장).
- `token.json` 은 **사용자 액세스 토큰** 이라 더 민감하다.
  - 트레이니별로 매번 새로 발급되는 게 원칙. 진행자 본인 토큰을 트레이니에게 넘기지 말 것.
- 본 워크숍은 **`drive.file` 범위** 만 요청한다.
  이 앱이 만든 파일에 대해서만 접근 가능하며, 사용자의 기존 Drive 파일에는 접근할 수 없다.
