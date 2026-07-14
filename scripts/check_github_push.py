"""6단계: GitHub 원격과 로컬이 맞는지 확인합니다.

실행:
  ..\\.venv\\Scripts\\python.exe scripts\\check_github_push.py
"""

from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(parents=True, exist_ok=True)
RESULT_MD = OUTPUTS / "github_push_check.md"
GIT = Path(r"C:\Program Files\Git\cmd\git.exe")
EXPECTED_REMOTE = "https://github.com/swani2004-byte/wonju-holiday-api-dashboard.git"


def run_git(*args: str) -> tuple[int, str]:
    proc = subprocess.run(
        [str(GIT), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out.strip()


def check(name: str, ok: bool, detail: str) -> dict:
    status = "OK" if ok else "FAIL"
    line = f"[{status}] {name}: {detail}"
    print(line)
    return {"ok": ok, "line": line}


def main() -> int:
    results: list[dict] = []

    results.append(check("git.exe", GIT.is_file(), str(GIT)))
    results.append(check(".git 폴더", (ROOT / ".git").is_dir(), str(ROOT / ".git")))

    code, remote = run_git("remote", "get-url", "origin")
    remote_ok = code == 0 and EXPECTED_REMOTE.rstrip("/") in remote.replace(".git", "") + ".git" or remote.rstrip("/") == EXPECTED_REMOTE.rstrip("/")
    # simpler compare
    remote_norm = remote.strip().rstrip("/").removesuffix(".git")
    expect_norm = EXPECTED_REMOTE.rstrip("/").removesuffix(".git")
    remote_ok = code == 0 and remote_norm == expect_norm
    results.append(check("origin URL", remote_ok, remote or "없음"))

    code, sb = run_git("status", "-sb")
    synced = "ahead" not in sb and "behind" not in sb and "origin/main" in sb
    results.append(check("origin/main 동기화", synced or ("## main" in sb and "origin/main" in sb and "ahead" not in sb and "behind" not in sb), sb))

    must = [
        "app.py",
        "analysis.py",
        "requirements.txt",
        "README.md",
        ".gitignore",
        "data/holidays_2026.json",
        "data/inquiries_sample.csv",
    ]
    code, tracked = run_git("ls-files")
    for rel in must:
        results.append(check(f"추적 중 {rel}", rel.replace("\\", "/") in tracked.replace("\\", "/"), rel))

    # secrets not tracked
    for bad in (".env", "outputs/report.md"):
        results.append(
            check(
                f"미추적(비밀·결과) {bad}",
                bad not in tracked.splitlines(),
                "추적 안 함" if bad not in tracked.splitlines() else "추적 중!",
            )
        )

    code, log = run_git("log", "--oneline", "-3")
    results.append(check("최근 커밋", code == 0 and bool(log), log.replace("\n", " | ")))

    failed = [r for r in results if not r["ok"]]
    overall = len(failed) == 0

    lines = [
        "# GitHub push 확인",
        "",
        f"시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"폴더: `{ROOT}`",
        f"전체: {'통과 — Cloud Deploy로 진행 가능' if overall else '미통과 — FAIL 확인'}",
        "",
        f"저장소: {EXPECTED_REMOTE}",
        "",
        "## 검사 결과",
        "",
    ]
    for r in results:
        lines.append(f"- {r['line']}")
    lines.extend(
        [
            "",
            "## 다음에 할 일",
            "",
            "1. https://share.streamlit.io 에서 GitHub 연결",
            "2. 저장소 선택, Main file: app.py",
            "3. Deploy",
            "",
        ]
    )
    RESULT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"결과 저장: {RESULT_MD}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
