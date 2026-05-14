# _레퍼런스 — 진행자용 답안지

> ⚠️ **트레이니에게 미리 보여주지 말 것.**
> 이 폴더는 워크숍 진행자가 트레이니의 결과물과 비교하기 위한 참고 자료다.

## 내용

| 파일 | 가이드 단계 | 비교 대상 |
| --- | --- | --- |
| `scripts/02_inspect_input_files.py` | 1~3단계 | 파일 탐색·분류·인벤토리 생성 |
| `scripts/03_merge_finance_files.py` | 4단계 | 표준 컬럼 통합 + 품질 플래그 |
| `scripts/04_create_summary_tables.py` | 5단계 | 요약 CSV 6종 생성 |
| `scripts/05_generate_report.py` | 6단계 | Word(.docx) 리포트 생성 |
| `scripts/06_upload_to_google_docs.py` | 7단계 | Google Drive 업로드 + Docs 변환 |
| `requirements.txt` | — | 7단계까지 필요한 모든 의존성 |

> 이 답안 코드는 원래 `finance-practice/scripts/` 안에 있다고 가정해 경로가 계산된다.
> 그대로 실행하고 싶다면 `재무팀/finance-practice/scripts/` 로 임시 복사 후 실행한다.
> 보통은 **코드 비교 용도로만** 읽는다.

## 주의

- 트레이니의 답이 이 레퍼런스와 **완전히 같을 필요는 없다**.
  표준 컬럼이 잡혔고 원본을 손대지 않았고 Word 리포트가 만들어졌고 Google Docs 링크가 나왔다면 정답이다.
- 클로드코드의 코드 생성 방식은 매번 조금씩 다르다. 결과물의 **품질**을 보고, 코드 자체를 비교하지 말 것.
- 7단계(Google Docs 업로드)의 인증은 `_준비/credentials.json` 이 있어야 동작한다.
  발급/배포 방법은 `재무팀/_준비/README.md` 의 B 섹션 참고.
