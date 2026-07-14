# wonju-holiday-api-dashboard

공휴일 · 문의 워밍업 Streamlit 앱입니다.  
**교육용 샘플 데이터**만 포함하며, Streamlit Community Cloud 배포용으로 정리한 독립 프로젝트입니다.

## 데이터

| 파일 | 설명 |
|------|------|
| `data/holidays_2026.json` | 교육용 샘플 — 2026 공휴일 목록 |
| `data/inquiries_sample.csv` | 교육용 샘플 — 합성 문의 집계 |

실제 업무 자료·개인정보는 포함되어 있지 않습니다.

## 로컬 실행 방법

상위 폴더 `wonju-advanced-demos`의 가상환경(`.venv`)을 재사용합니다.

```powershell
cd wonju-holiday-api-dashboard
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
..\.venv\Scripts\streamlit.exe run app.py
```

브라우저: http://localhost:8501  
(로그인·API 키 불필요. 종료는 터미널에서 `Ctrl+C`)

자동 점검:

```powershell
..\.venv\Scripts\python.exe scripts\preflight_local.py
```

## 화면 결과 설명

1. **공휴일 표** — 섹션「1. 공휴일 목록」에 교육용 JSON의 날짜·공휴일명을 표로 보여 줍니다 (샘플 기준 10행).
2. **holiday_yn / 휴일여부** — 섹션「2. 문의 + 휴일 여부」표에서 각 문의 날짜가 공휴일인지 표시합니다.  
   자료·내부 필드로는 `is_holiday`(또는 개념상 `holiday_yn`)이고, **화면 컬럼명은 `휴일여부`**입니다 (`True`/`False`).
3. **요약** — 공휴일 전날과 당일 문의 건수를 비교하고, 상단에「전날 − 당일(요약)」을 보여 줍니다.

## 배포(공유) URL

| 구분 | 주소 |
|------|------|
| GitHub (코드) | https://github.com/swani2004-byte/wonju-holiday-api-dashboard |
| Streamlit 공유 URL (제출용) | https://wonju-holiday-api-dashboard-z4mt7yavq9n99it46sl6mw.streamlit.app/ |

- Main file: `app.py`
- Branch: `main`
- Secrets: 비움 (교육용 샘플만 사용, API 키 없음)
- `.env`, API 키, `secrets.toml`은 GitHub에 올리지 않습니다.

## Community Cloud · 재배포

코드를 고친 뒤:

1. `git commit` → `git push`  
2. Streamlit Community Cloud가 새 커밋을 받아 다시 빌드  
3. **같은 공유 URL**로 결과 확인  

## 최종 제출 체크리스트

- [ ] GitHub에 `.env`, `.venv`, `secrets.toml`, `outputs/`, `__pycache__/` 가 **올라가지 않음**
- [ ] `requirements.txt`에 앱에 필요한 패키지만 있음 (`streamlit`, `pandas`, `tabulate`)
- [ ] README에 **로컬 실행 방법**이 있음
- [ ] README에 **배포(공유) URL**이 있음 (`*.streamlit.app`)
- [ ] README에 **공휴일 표**와 **holiday_yn(=휴일여부)** 설명이 있음
- [ ] 공개 URL에서 공휴일 표 · 휴일여부 · 요약이 보임
- [ ] Secrets / API 키를 README·채팅·GitHub에 적지 않음
- [ ] 제출물에는 **교육용 샘플 데이터**만 사용했음을 명시함
