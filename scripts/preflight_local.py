"""4단계: 로컬 실행 · 배포 전 자동 테스트.

1) 패키지 import
2) 교육용 샘플 데이터 로드·분석 숫자 확인
3) Streamlit AppTest로 app.py 기동 오류 여부 확인

실행:
  ..\\.venv\\Scripts\\python.exe scripts\\preflight_local.py
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(parents=True, exist_ok=True)
RESULT_MD = OUTPUTS / "preflight_local.md"


def check(name: str, ok: bool, detail: str) -> dict:
    status = "OK" if ok else "FAIL"
    line = f"[{status}] {name}: {detail}"
    print(line)
    return {"name": name, "ok": ok, "detail": detail, "line": line}


def main() -> int:
    results: list[dict] = []

    # --- 1) 패키지 ---
    for mod in ("streamlit", "pandas", "tabulate"):
        try:
            m = __import__(mod)
            ver = getattr(m, "__version__", "?")
            results.append(check(f"패키지 {mod}", True, str(ver)))
        except Exception as exc:  # noqa: BLE001
            results.append(check(f"패키지 {mod}", False, str(exc)))

    # --- 2) 데이터·분석 ---
    try:
        from analysis import (
            attach_holiday_flags,
            compare_eve_and_holiday,
            load_holidays,
            load_inquiries,
            save_outputs,
            summary_rows,
        )

        holidays = load_holidays()
        inquiries = load_inquiries()
        flagged = attach_holiday_flags(inquiries, holidays)
        comparison = compare_eve_and_holiday(inquiries, holidays)
        comparable = summary_rows(comparison)

        results.append(
            check(
                "공휴일 개수",
                len(holidays) == 10,
                f"{len(holidays)} (기대 10)",
            )
        )
        results.append(
            check(
                "문의 행 수",
                len(inquiries) == 18,
                f"{len(inquiries)} (기대 18)",
            )
        )
        results.append(
            check(
                "요약 공휴일 수",
                len(comparable) == 3,
                f"{len(comparable)} (기대 3)",
            )
        )

        total_eve = int(comparable["eve_count"].sum()) if len(comparable) else 0
        total_holiday = int(comparable["holiday_count"].sum()) if len(comparable) else 0
        results.append(
            check(
                "전날·당일 합계",
                total_eve == 126 and total_holiday == 28,
                f"전날 {total_eve}, 당일 {total_holiday} (기대 126/28)",
            )
        )

        paths = save_outputs(holidays, flagged, comparison)
        results.append(
            check(
                "outputs/report.md 생성",
                paths["report_md"].is_file(),
                str(paths["report_md"].relative_to(ROOT)),
            )
        )
    except Exception as exc:  # noqa: BLE001
        results.append(check("데이터·분석 파이프라인", False, str(exc)))

    # --- 3) Streamlit AppTest (브라우저 로그인 없음) ---
    try:
        from streamlit.testing.v1 import AppTest

        at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
        at.run()
        has_exc = bool(at.exception)
        detail = "예외 없음" if not has_exc else str(at.exception)
        results.append(check("Streamlit AppTest 기동", not has_exc, detail))

        # 제목 텍스트가 렌더되는지 (요소가 있으면 OK)
        titles = [t.value for t in at.title]
        title_ok = any("공휴일" in str(v) for v in titles)
        results.append(
            check(
                "화면 제목 렌더",
                title_ok or len(at.main) > 0,
                f"title={titles!r}" if titles else "main 요소 존재",
            )
        )
    except Exception as exc:  # noqa: BLE001
        results.append(check("Streamlit AppTest 기동", False, str(exc)))

    results.append(check("프로젝트 경로", True, str(ROOT)))
    results.append(check("Python", True, sys.executable))

    failed = [r for r in results if not r["ok"]]
    overall = len(failed) == 0

    lines = [
        "# 로컬 실행 · 배포 전 테스트 결과",
        "",
        f"시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"폴더: `{ROOT}`",
        f"전체: {'통과 — GitHub / Cloud 배포로 진행 가능' if overall else '미통과 — FAIL을 고치세요'}",
        "",
        "## 검사 결과",
        "",
    ]
    for r in results:
        lines.append(f"- {r['line']}")

    lines.extend(
        [
            "",
            "## 사람이 한 번 더 볼 때 (선택)",
            "",
            "```powershell",
            f"cd {ROOT}",
            r"..\.venv\Scripts\streamlit.exe run app.py",
            "```",
            "",
            "브라우저: http://localhost:8501  (로그인·API 키 불필요)",
            "",
            "## 다음에 할 일",
            "",
            "1. 이 폴더만 GitHub 공개 저장소에 푸시 (브라우저에서 로그인)",
            "2. https://share.streamlit.io 에서 Deploy — Main file: `app.py`",
            "",
        ]
    )
    RESULT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"결과 저장: {RESULT_MD}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
