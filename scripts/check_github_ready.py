"""5단계: GitHub에 올리기 직전 로컬 준비 점검.

실행:
  ..\\.venv\\Scripts\\python.exe scripts\\check_github_ready.py
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(parents=True, exist_ok=True)
RESULT_MD = OUTPUTS / "github_ready_check.md"

MUST_FILES = [
    "app.py",
    "analysis.py",
    "requirements.txt",
    "README.md",
    ".gitignore",
    "data/holidays_2026.json",
    "data/inquiries_sample.csv",
]

FORBIDDEN = [".env", ".venv", ".streamlit/secrets.toml"]


def check(name: str, ok: bool, detail: str) -> dict:
    status = "OK" if ok else "FAIL"
    line = f"[{status}] {name}: {detail}"
    print(line)
    return {"ok": ok, "line": line}


def main() -> int:
    results: list[dict] = []

    for rel in MUST_FILES:
        p = ROOT / rel
        results.append(check(f"파일 {rel}", p.is_file(), str(p)))

    gi = (ROOT / ".gitignore").read_text(encoding="utf-8") if (ROOT / ".gitignore").is_file() else ""
    for token in (".venv", ".env", ".env.*", "secrets.toml", "__pycache__", "outputs"):
        results.append(
            check(f".gitignore 에 {token}", token in gi, "있음" if token in gi else "없음")
        )

    for rel in FORBIDDEN:
        p = ROOT / rel
        results.append(check(f"없는 것이 좋음: {rel}", not p.exists(), "없음" if not p.exists() else "있음!"))

    results.append(check("git 초기화", (ROOT / ".git").is_dir(), "됨" if (ROOT / ".git").is_dir() else "아직 안 됨(다음 단계)"))

    failed = [r for r in results if not r["ok"] and "git 초기화" not in r["line"]]
    # git not init yet is OK for browser-first step
    overall = len(failed) == 0

    lines = [
        "# GitHub 올리기 직전 점검",
        "",
        f"시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"폴더: `{ROOT}`",
        f"전체: {'통과 — 브라우저에서 저장소 만들면 됩니다' if overall else '미통과'}",
        "",
        "## 검사 결과",
        "",
    ]
    for r in results:
        lines.append(f"- {r['line']}")
    lines.extend(
        [
            "",
            "## 브라우저 할 일",
            "",
            "1. https://github.com → 로그인",
            "2. New repository → Public → README 없이 생성",
            "3. 저장소 URL을 채팅에 알려 주기",
            "",
        ]
    )
    RESULT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"결과 저장: {RESULT_MD}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
