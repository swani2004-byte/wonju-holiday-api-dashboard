# 4단계 — 로컬 실행과 배포 전 테스트

## 목표

GitHub / Streamlit Community Cloud에 올리기 전에,  
Cursor가 **로컬에서 앱이 도는지** 자동으로 확인합니다.

## 하는 일

1. `streamlit` / `pandas` / `tabulate` import
2. 교육용 샘플로 분석 숫자(10 / 18 / 126·28) 확인
3. Streamlit **AppTest**로 `app.py` 기동 (브라우저 로그인 없음)

## 실행

```powershell
cd C:\Users\ADMIN\Desktop\wonju-advanced-demos\wonju-holiday-api-dashboard
..\.venv\Scripts\python.exe scripts\preflight_local.py
```

결과: `outputs/preflight_local.md`

## 선택 — 브라우저에서 직접 보기

```powershell
..\.venv\Scripts\streamlit.exe run app.py
```

http://localhost:8501 — API 키·로그인 불필요. 확인 후 터미널에서 Ctrl+C.

## 주의

- `data/` 원본은 삭제·덮어쓰지 않음
- 자동 테스트가 `outputs/report.md`를 **새로 생성**할 수 있음 (실행 결과물)
