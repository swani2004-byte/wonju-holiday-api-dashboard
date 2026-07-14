# 5단계 — GitHub 저장소를 브라우저에서 만들기

## 목표

`wonju-holiday-api-dashboard`를 **공개(Public) GitHub 저장소**로 만들어  
나중에 Streamlit Community Cloud가 이 코드를 읽을 수 있게 합니다.

이 단계에서 Cursor는 **비밀번호·토큰을 받지 않습니다.**  
GitHub 로그인은 **본인 브라우저에서만** 하세요.

## 준비된 로컬 폴더

```
wonju-holiday-api-dashboard/
  app.py
  analysis.py
  requirements.txt
  README.md
  .gitignore
  data/          ← 교육용 샘플만
  docs/
  scripts/
```

올리면 안 되는 것(이미 `.gitignore`): `.venv`, `.env`, `.env.*`, `secrets.toml`, `__pycache__`, `outputs/`

---

## 당신이 브라우저에서 할 일

### 1) GitHub 로그인
1. https://github.com 접속  
2. 본인 계정으로 로그인 (비밀번호는 채팅에 입력하지 마세요)

### 2) 새 저장소 만들기
1. 오른쪽 위 **+** → **New repository**  
2. 설정 예:

| 항목 | 값 |
|------|-----|
| Repository name | `wonju-holiday-api-dashboard` (추천) |
| Description | Educational holiday inquiry Streamlit app (sample data) |
| Visibility | **Public** (Community Cloud 무료 배포용) |
| Add a README | **체크하지 않음** (로컬에 이미 README 있음) |
| Add .gitignore | **None** (로컬에 이미 있음) |
| License | 없음(또는 수업 안내에 따름) |

3. **Create repository** 클릭

### 3) 저장소 주소 확인
생성 후 주소가 비슷하게 보입니다.

```text
https://github.com/본인아이디/wonju-holiday-api-dashboard
```

이 URL을 채팅에 알려 주세요.  
(토큰·비밀번호는 보내지 마세요.)

---

## Cursor가 이어서 할 일 (URL을 받은 뒤)

1. 로컬에 `git init` · 첫 커밋 (아직 안 했다면)  
2. `git remote add origin …`  
3. `git push` — 인증 창이 뜨면 **브라우저/GitHub에서만** 로그인

## 주의

- `wonju-advanced-demos` 전체(유튜브 실습 포함)를 올리지 않습니다.  
- **이 폴더만** 올립니다.  
- 실제 업무 데이터·API 키는 넣지 않습니다.
