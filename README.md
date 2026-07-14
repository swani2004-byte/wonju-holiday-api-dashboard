# wonju-holiday-api-dashboard

공휴일 · 문의 워밍업 Streamlit 앱입니다.  
**교육용 샘플 데이터**만 포함하며, Streamlit Community Cloud 배포용으로 정리한 독립 프로젝트입니다.

## 데이터

| 파일 | 설명 |
|------|------|
| `data/holidays_2026.json` | 교육용 샘플 — 2026 공휴일 목록 |
| `data/inquiries_sample.csv` | 교육용 샘플 — 합성 문의 집계 |

실제 업무 자료·개인정보는 포함되어 있지 않습니다.

## 로컬 실행 방법 (배포 전 테스트 완료)

상위 폴더 `wonju-advanced-demos`의 가상환경(`.venv`)을 재사용합니다.

```powershell
cd wonju-holiday-api-dashboard
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
..\.venv\Scripts\streamlit.exe run app.py
```

브라우저: http://localhost:8501  
(로그인·API 키 불필요. 종료는 터미널에서 `Ctrl+C`)

### 로컬 확인 결과 (성공)

| 항목 | 결과 |
|------|------|
| 가상환경 | 상위 `.venv` 재사용 |
| 패키지 | `streamlit`, `pandas`, `tabulate` 설치·동작 |
| HTTP | http://localhost:8501 → **200 OK** |
| AppTest | 제목「공휴일 · 문의 워밍업 대시보드」렌더 OK |
| 숫자 | 공휴일 10 · 문의 18 · 전날 126 · 당일 28 |

### 브라우저에서 확인할 것

1. **공휴일 표** — 섹션「1. 공휴일 목록」에 날짜·공휴일명 (10행)
2. **문의 + 휴일 여부** — 섹션「2」표의 **`휴일여부`** 컬럼  
   (내부 필드명은 `is_holiday`이며, 화면에는 `휴일여부`로 표시됩니다. 자료의 `holiday_yn`과 같은 역할입니다.)
3. **요약** — 상단 지표「전날 − 당일(요약)」과 파란 안내문(전날 합계가 당일보다 많음), 섹션「3」비교 표의 **`요약포함`** 열

자동 점검만 다시 돌리려면:

```powershell
..\.venv\Scripts\python.exe scripts\preflight_local.py
```

## Community Cloud

- GitHub: https://github.com/swani2004-byte/wonju-holiday-api-dashboard
- Main file: `app.py`
- 이 폴더만 GitHub 저장소로 올리면 됩니다.
- `.env`, API 키, `secrets.toml`은 올리지 마세요.
