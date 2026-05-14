# 재무팀 — Claude Code 실습 패키지

비코딩 인력(재무팀 실무자)이 클로드코드(Claude Code)와 자연어로 일하는 감각을 익히는 워크숍 자료다.
"흩어진 Excel/CSV 파일을 자동으로 정리·통합·요약·리포트화" 한 뒤
**Word 보고서로 출력하고 회사 Google Docs 로 공유** 하는 흐름을 클로드코드에게 한 단계씩 시키면서 따라간다.

---

## 폴더 구성

```
재무팀/
├── 실습_가이드.md          ← 트레이니가 보고 따라하는 메인 문서 (프롬프트 모음)
├── finance-practice/       ← 트레이니가 실제로 작업하는 폴더 (Excel/CSV만 있음)
├── _준비/                  ← 진행자 사전 셋업 (샘플 데이터 + Google OAuth credentials)
└── _레퍼런스/              ← 진행자용 참고 답안 (scripts 등 — 트레이니에게 미리 보여주지 말 것)
```

| 폴더/파일 | 누가 보나? | 역할 |
| --- | --- | --- |
| `실습_가이드.md` | 트레이니 | 클로드코드에 넣을 프롬프트를 단계별로 모아둔 가이드 |
| `finance-practice/` | 트레이니 | 클로드코드를 켜고 작업하는 실제 폴더. Excel/CSV/txt 원본만. |
| `_준비/01_generate_messy_sample_files.py` | 진행자 | `finance-practice/` 를 "시작 상태"로 초기화 |
| `_준비/credentials.json` | 진행자가 발급, 트레이니가 사용 | 7단계 Google Docs 업로드용 OAuth 자격 |
| `_준비/README.md` | 진행자 | OAuth 발급/배포 절차 안내 |
| `_레퍼런스/` | 진행자 | 정답 코드 (트레이니 답안 비교용) |

---

## 워크숍 진행 순서

### A. 진행자 사전 준비 (워크숍 첫 회차 시 한 번)

1. Python 3.11+ 설치 확인
2. 패키지 설치:
   ```bash
   pip install pandas openpyxl python-docx google-api-python-client google-auth-oauthlib
   ```
3. **Google OAuth 자격 발급**: `재무팀/_준비/README.md` 의 B 섹션을 따라
   `_준비/credentials.json` 을 생성·배치한다.
4. 본인 계정으로 전체 흐름(1~7단계) 한 번 시험 실행해서 문제 없는지 확인.
5. 트레이니 입장 직전 `_준비/token.json` 은 삭제한다 (트레이니가 본인 계정으로 인증해야 함).

### B. 매 트레이니 시작 전 폴더 초기화

```bash
cd 재무팀/_준비
python 01_generate_messy_sample_files.py
```

이 명령으로 `재무팀/finance-practice/` 안에 지저분한 샘플 Excel/CSV 7개가 생성된다.

### C. 트레이니가 따라하기

1. `재무팀/실습_가이드.md` 를 열어둔다 (옆 모니터/PDF/노션 등).
2. 터미널에서 실습 폴더로 이동:
   ```bash
   cd 재무팀/finance-practice
   ```
3. 클로드코드 실행:
   ```bash
   claude
   ```
4. 가이드의 **1단계부터 7단계**까지 프롬프트를 순서대로 입력.

### D. 다음 트레이니를 위한 리셋

```bash
cd 재무팀
rm -rf finance-practice/data finance-practice/reports
rm -f _준비/token.json
python _준비/01_generate_messy_sample_files.py
```

`credentials.json` 은 유지한다.

---

## 실습 흐름 한눈에 보기

| 단계 | 트레이니가 할 일 | 폴더에 생기는 것 |
| ---: | --- | --- |
| 0 | `cd finance-practice && claude` | 클로드코드 켜짐 |
| 1 | "이 폴더에 뭐가 있는지 봐줘" | (대화로 확인) 분석 5 / 제외 2 |
| 2 | "원본 백업하고 작업 폴더 만들어줘" | `data/raw_snapshot/`, `data/processed/`, `data/output/`, `reports/` |
| 3 | "파일 점검 표 만들어줘" | `data/processed/input_file_inventory.csv` |
| 4 | "표준 형식으로 합쳐줘" | `data/processed/merged_expenses.csv` |
| 5 | "요약 테이블 만들어줘" | `data/output/*.csv` (6개) |
| 6 | "Word 리포트 만들어줘" | `reports/finance_expense_report.docx` |
| 7 | "Google Docs로 업로드해줘" | 공유 가능한 Google Docs 링크 |

각 단계의 자세한 프롬프트는 `실습_가이드.md` 에 있다.

---

## 교육 포인트 (진행자용)

- **"정리되지 않은 폴더"에서 시작하는 게 의도된 설정이다.**
  실제 재무팀의 평소 작업 환경을 재현한다.
- **마지막 두 단계(Word + Google Docs)가 핵심이다.**
  "내가 한 일이 진짜 회사에서 쓸 수 있는 결과물(.docx + Drive 링크)로 끝난다"는 경험을 만든다.
- **OAuth 인증은 가장 막히기 쉬운 구간이다.**
  진행자가 사전 테스트로 인증 흐름을 한 번 거쳐두고,
  Workspace 정책 차단 등 환경 이슈를 미리 점검해두자.
- **`_레퍼런스/` 는 절대 트레이니에게 미리 열어주지 말 것.**
  답안을 보면 직접 만드는 경험이 사라진다. 트레이니가 막혔을 때 진행자가 비교용으로만 참고한다.

---

## 트러블슈팅

| 증상 | 해결 |
| --- | --- |
| `claude` 명령이 없다 | Claude Code CLI 설치 안내 (별도 문서) |
| 한글이 깨진 CSV가 나온다 | 가이드 5단계 프롬프트에 `utf-8-sig` 강조됨 |
| `pandas`/`openpyxl`/`python-docx` 없다고 함 | 위 A-2 명령으로 일괄 설치 |
| 6단계 Word 파일이 안 열린다 | `python-docx` 버전 확인 / 파일 권한 확인 |
| 7단계 브라우저 인증이 막힌다 | `_준비/README.md` 의 C 섹션(트러블슈팅) 참고 |
| 폴더가 꼬였다 | 위 D 섹션(리셋) 실행 |

---

## 라이선스/주의

- 모든 데이터는 **합성 데이터**다. 실존 기업/거래처/개인 정보를 사용하지 않는다.
- `credentials.json`, `token.json` 은 OAuth 비밀 정보다. **공개 저장소에 절대 커밋하지 말 것** (.gitignore 에 등록됨).
- 실제 회사 데이터로 같은 흐름을 시도할 때는 별도 폴더에서 보안 정책에 맞춰 진행한다.
