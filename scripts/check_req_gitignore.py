"""3단계: requirements.txt · .gitignore 점검 (배포 폴더용).

실행:
  ..\\.venv\\Scripts\\python.exe scripts\\check_req_gitignore.py
"""

from __future__ import annotations

import ast
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(parents=True, exist_ok=True)
RESULT_MD = OUTPUTS / "req_gitignore_check.md"

REQUIRED_PACKAGES = ("streamlit", "pandas", "tabulate")
MUST_IGNORE = (".venv", ".env", "secrets.toml", "__pycache__", "outputs")


def check(name: str, ok: bool, detail: str) -> dict:
    status = "OK" if ok else "FAIL"
    line = f"[{status}] {name}: {detail}"
    print(line)
    return {"name": name, "ok": ok, "detail": detail, "line": line}


def parse_requirements(text: str) -> list[str]:
    names: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        name = re.split(r"[<>=!~;\[]", line, maxsplit=1)[0].strip().lower()
        if name:
            names.append(name)
    return names


def third_party_imports(py_path: Path) -> set[str]:
    """프로젝트 모듈(analysis)과 stdlib 비슷 항목을 제외한 import 이름."""
    tree = ast.parse(py_path.read_text(encoding="utf-8"), filename=str(py_path))
    local_mods = {"analysis"}
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                top = alias.name.split(".")[0]
                if top not in local_mods:
                    found.add(top)
        elif isinstance(node, ast.ImportFrom):
            if node.module is None or node.level and node.level > 0:
                continue
            top = node.module.split(".")[0]
            if top not in local_mods:
                found.add(top)
    # 표준 라이브러리·내장 제외
    stdish = {
        "annotations",
        "pathlib",
        "datetime",
        "sys",
        "os",
        "re",
        "json",
        "typing",
        "__future__",
    }
    return {n for n in found if n not in stdish}


def main() -> int:
    results: list[dict] = []

    req_path = ROOT / "requirements.txt"
    gi_path = ROOT / ".gitignore"

    results.append(check("requirements.txt 존재", req_path.is_file(), str(req_path)))
    results.append(check(".gitignore 존재", gi_path.is_file(), str(gi_path)))

    req_text = req_path.read_text(encoding="utf-8") if req_path.is_file() else ""
    gi_text = gi_path.read_text(encoding="utf-8") if gi_path.is_file() else ""
    pkgs = parse_requirements(req_text)

    for pkg in REQUIRED_PACKAGES:
        results.append(
            check(
                f"requirements 에 {pkg}",
                pkg in pkgs,
                "포함" if pkg in pkgs else "누락",
            )
        )

    # import ↔ requirements 대응
    imported: set[str] = set()
    for py in (ROOT / "app.py", ROOT / "analysis.py"):
        if py.is_file():
            imported |= third_party_imports(py)

    # pandas는 import 이름이 pandas, streamlit은 streamlit
    # tabulate는 analysis에서 직접 import하지 않고 to_markdown이 런타임에 사용
    map_import_to_req = {"streamlit": "streamlit", "pandas": "pandas", "pd": "pandas"}
    needed_from_import = set()
    for name in imported:
        if name in map_import_to_req:
            needed_from_import.add(map_import_to_req[name])
        elif name not in ("pd",):
            # unknown third-party
            if name not in ("annotations",):
                needed_from_import.add(name)

    # tabulate: to_markdown 사용 여부
    analysis_src = (ROOT / "analysis.py").read_text(encoding="utf-8") if (ROOT / "analysis.py").is_file() else ""
    if "to_markdown" in analysis_src:
        needed_from_import.add("tabulate")

    for pkg in sorted(needed_from_import):
        results.append(
            check(
                f"import 대응 {pkg}",
                pkg in pkgs,
                "requirements에 있음" if pkg in pkgs else "requirements에 없음",
            )
        )

    # 불필요하게 많은 패키지 경고(실패는 아님) — 배포본에 없어야 할 것
    unnecessary = [p for p in pkgs if p not in REQUIRED_PACKAGES]
    results.append(
        check(
            "불필요 패키지 최소화",
            len(unnecessary) == 0,
            "추가 없음" if not unnecessary else f"검토: {', '.join(unnecessary)}",
        )
    )

    for token in MUST_IGNORE:
        ok = token in gi_text
        results.append(
            check(
                f".gitignore 에 {token}",
                ok,
                "규칙 있음" if ok else "규칙 없음",
            )
        )

    # 비밀·가상환경이 폴더에 실제로 없는지
    results.append(
        check(
            ".env 파일 없음",
            not (ROOT / ".env").exists(),
            "없음" if not (ROOT / ".env").exists() else "있음 — Git에 넣지 마세요",
        )
    )
    results.append(
        check(
            ".venv 폴더 없음",
            not (ROOT / ".venv").exists(),
            "없음" if not (ROOT / ".venv").exists() else "있음 — 배포 폴더에 두지 마세요",
        )
    )
    results.append(
        check(
            "secrets.toml 없음",
            not (ROOT / ".streamlit" / "secrets.toml").exists(),
            "없음",
        )
    )

    # 교육용 data는 추적 대상(무시되면 안 됨)
    results.append(
        check(
            "data/ 샘플 존재",
            (ROOT / "data" / "holidays_2026.json").is_file()
            and (ROOT / "data" / "inquiries_sample.csv").is_file(),
            "교육용 샘플 있음",
        )
    )
    # gitignore가 data/ 전체를 막으면 안 됨
    data_blocked = bool(re.search(r"(?m)^\s*data/?\s*$", gi_text))
    results.append(
        check(
            "data/ 를 gitignore하지 않음",
            not data_blocked,
            "data/ 는 커밋 대상(교육용 샘플)" if not data_blocked else "data/ 무시 중 — 수정 필요",
        )
    )

    # 패키지 import 가능 (로컬 venv)
    for mod, label in (("streamlit", "streamlit"), ("pandas", "pandas"), ("tabulate", "tabulate")):
        try:
            m = __import__(mod)
            ver = getattr(m, "__version__", "?")
            results.append(check(f"로컬 import {label}", True, str(ver)))
        except Exception as exc:  # noqa: BLE001
            results.append(check(f"로컬 import {label}", False, str(exc)))

    results.append(check("Python", True, sys.executable))

    failed = [r for r in results if not r["ok"]]
    overall = len(failed) == 0

    lines = [
        "# requirements.txt · .gitignore 점검 결과",
        "",
        f"시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"폴더: `{ROOT}`",
        f"전체: {'통과 — GitHub 준비로 넘어가도 됩니다' if overall else '미통과 — FAIL을 고치세요'}",
        "",
        "## requirements.txt (현재)",
        "",
        "```",
        req_text.strip() or "(비어 있음)",
        "```",
        "",
        "## .gitignore 핵심 규칙",
        "",
        "- `.venv/`, `.env`, `secrets.toml`, `__pycache__/`, `outputs/`",
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
            "1. FAIL이 있으면 requirements / gitignore만 최소 수정",
            "2. 이 폴더를 GitHub 공개 저장소에 푸시 (로그인은 브라우저)",
            "3. Streamlit Community Cloud에서 `app.py`로 Deploy",
            "",
        ]
    )
    RESULT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"결과 저장: {RESULT_MD}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
