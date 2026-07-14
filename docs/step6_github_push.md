# 6단계 — Cursor로 GitHub에 첫 저장과 push 하기

## 목표

로컬 `wonju-holiday-api-dashboard` 코드를 GitHub에 올려  
Streamlit Community Cloud가 읽을 수 있게 합니다.

## 이미 완료된 것 (5~6단계 연속 작업)

| 항목 | 결과 |
|------|------|
| 원격 저장소 | https://github.com/swani2004-byte/wonju-holiday-api-dashboard |
| 로컬 Git | `main` 브랜치 |
| 원격 이름 | `origin` |
| 동기화 | `main` = `origin/main` (up to date) |
| 첫 커밋 | 앱·교육용 data·requirements·README·.gitignore 등 |

## 올라간 파일 (요지)

- `app.py`, `analysis.py`, `requirements.txt`, `README.md`, `.gitignore`
- `data/holidays_2026.json`, `data/inquiries_sample.csv`
- `docs/`, `scripts/` (점검·안내)

## 올리지 않은 것 (`.gitignore`)

- `.venv/`, `.env`, `.env.*`, `.streamlit/secrets.toml`
- `__pycache__/`, `outputs/` (로컬 실행 결과)

## 다시 확인할 때

```powershell
cd wonju-holiday-api-dashboard
& "C:\Program Files\Git\cmd\git.exe" status
& "C:\Program Files\Git\cmd\git.exe" log --oneline -3
```

브라우저에서 저장소 → `app.py`, `data/` 가 보이면 성공입니다.

## 다음에 할 일 (7단계)

1. https://share.streamlit.io 접속  
2. GitHub 계정 연결 (브라우에서만 로그인)  
3. 저장소 `wonju-holiday-api-dashboard` 선택  
4. Main file path: **`app.py`**  
5. Deploy → 공개 URL 확인
