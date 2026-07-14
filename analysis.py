"""공휴일·문의 데이터 로딩과 분석 공통 로직.

교육용 샘플 데이터는 프로젝트 루트의 data/ 폴더를 상대 경로로 읽습니다.
"""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import pandas as pd

# app.py · analysis.py 가 같은 폴더에 있을 때 프로젝트 루트
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"


def load_holidays() -> pd.DataFrame:
    holidays = pd.read_json(DATA / "holidays_2026.json")
    holidays["date"] = pd.to_datetime(holidays["date"])
    return holidays.sort_values("date").reset_index(drop=True)


def load_inquiries() -> pd.DataFrame:
    inquiries = pd.read_csv(DATA / "inquiries_sample.csv")
    inquiries["date"] = pd.to_datetime(inquiries["date"])
    inquiries["count"] = inquiries["count"].astype(int)
    return inquiries


def attach_holiday_flags(inquiries: pd.DataFrame, holidays: pd.DataFrame) -> pd.DataFrame:
    """문의에 휴일 여부(is_holiday)와 공휴일명(holiday_name) 컬럼을 붙입니다."""
    holiday_map = dict(zip(holidays["date"], holidays["name"]))
    result = inquiries.copy()
    result["holiday_name"] = result["date"].map(holiday_map)
    result["is_holiday"] = result["holiday_name"].notna()
    result["holiday_name"] = result["holiday_name"].fillna("-")
    return result


def daily_counts(inquiries: pd.DataFrame) -> pd.Series:
    """날짜별 문의 건수 합계."""
    return inquiries.groupby("date")["count"].sum()


def compare_eve_and_holiday(
    inquiries: pd.DataFrame, holidays: pd.DataFrame
) -> pd.DataFrame:
    """휴일 전날과 당일 문의 건수를 비교합니다.

    연휴처럼 공휴일이 이어지면, 전날도 공휴일인 쌍은
    '진짜 전날(평일) vs 당일' 요약에서 제외합니다.
    """
    by_day = daily_counts(inquiries)
    holiday_dates = set(holidays["date"])
    rows: list[dict] = []

    for _, holiday in holidays.iterrows():
        holiday_date = holiday["date"]
        eve_date = holiday_date - timedelta(days=1)
        holiday_count = int(by_day.get(holiday_date, 0))
        eve_count = int(by_day.get(eve_date, 0))
        eve_is_holiday = eve_date in holiday_dates
        has_inquiry_data = (holiday_date in by_day.index) or (eve_date in by_day.index)
        use_in_summary = has_inquiry_data and not eve_is_holiday

        rows.append(
            {
                "holiday_name": holiday["name"],
                "eve_date": eve_date.strftime("%Y-%m-%d"),
                "eve_count": eve_count,
                "holiday_date": holiday_date.strftime("%Y-%m-%d"),
                "holiday_count": holiday_count,
                "diff_eve_minus_holiday": eve_count - holiday_count,
                "eve_is_holiday": eve_is_holiday,
                "has_inquiry_data": has_inquiry_data,
                "use_in_summary": use_in_summary,
            }
        )

    return pd.DataFrame(rows)


def summary_rows(comparison: pd.DataFrame) -> pd.DataFrame:
    """전날/당일 합계 계산에 쓸 행만 고릅니다."""
    return comparison[comparison["use_in_summary"]].copy()


def format_date_column(df: pd.DataFrame, column: str = "date") -> pd.DataFrame:
    out = df.copy()
    out[column] = pd.to_datetime(out[column]).dt.strftime("%Y-%m-%d")
    return out


def holidays_table(holidays: pd.DataFrame) -> pd.DataFrame:
    view = format_date_column(holidays.rename(columns={"name": "공휴일명"}))
    return view[["date", "공휴일명"]].rename(columns={"date": "날짜"})


def inquiries_with_flags_table(flagged: pd.DataFrame) -> pd.DataFrame:
    view = format_date_column(flagged)
    return view.rename(
        columns={
            "date": "날짜",
            "category": "분류",
            "channel": "채널",
            "count": "건수",
            "is_holiday": "휴일여부",
            "holiday_name": "공휴일명",
        }
    )[["날짜", "분류", "채널", "건수", "휴일여부", "공휴일명"]]


def comparison_table(comparison: pd.DataFrame) -> pd.DataFrame:
    return comparison.rename(
        columns={
            "holiday_name": "공휴일명",
            "eve_date": "전날",
            "eve_count": "전날건수",
            "holiday_date": "당일",
            "holiday_count": "당일건수",
            "diff_eve_minus_holiday": "전날-당일",
            "eve_is_holiday": "전날도공휴일",
            "use_in_summary": "요약포함",
        }
    )[
        [
            "공휴일명",
            "전날",
            "전날건수",
            "당일",
            "당일건수",
            "전날-당일",
            "전날도공휴일",
            "요약포함",
        ]
    ]


def build_markdown_report(
    holidays: pd.DataFrame,
    flagged: pd.DataFrame,
    comparison: pd.DataFrame,
) -> str:
    holiday_view = holidays_table(holidays)
    flagged_view = inquiries_with_flags_table(flagged)
    compare_view = comparison_table(comparison)
    comparable = summary_rows(comparison)

    total_eve = int(comparable["eve_count"].sum()) if len(comparable) else 0
    total_holiday = int(comparable["holiday_count"].sum()) if len(comparable) else 0

    lines = [
        "# 공휴일 · 문의 워밍업 리포트",
        "",
        "교육용 샘플 데이터(`data/holidays_2026.json`, `data/inquiries_sample.csv`) 기준입니다.",
        "",
        "## 1. 공휴일 목록",
        "",
        holiday_view.to_markdown(index=False),
        "",
        "## 2. 문의별 휴일 여부",
        "",
        flagged_view.to_markdown(index=False),
        "",
        f"- 전체 문의 행: **{len(flagged_view)}**건",
        f"- 휴일 당일 문의 행: **{int(flagged['is_holiday'].sum())}**건",
        "",
        "## 3. 휴일 전날 vs 당일 문의 건수 비교",
        "",
        "- 표에는 모든 공휴일을 보여 줍니다.",
        "- **요약**에는 문의 데이터가 있고, 전날이 공휴일이 아닌 경우만 넣습니다.",
        "",
        compare_view.to_markdown(index=False),
        "",
        "### 요약",
        "",
        f"- 요약에 포함한 공휴일 수: **{len(comparable)}**",
        f"- 전날 문의 합계: **{total_eve}**",
        f"- 당일 문의 합계: **{total_holiday}**",
        f"- 전날 − 당일 차이: **{total_eve - total_holiday}**",
        "",
    ]
    return "\n".join(lines)


def save_outputs(
    holidays: pd.DataFrame,
    flagged: pd.DataFrame,
    comparison: pd.DataFrame,
) -> dict[str, Path]:
    """실행 시 outputs/에 리포트를 새로 만듭니다 (교육용 샘플 기준)."""
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    csv_path = OUTPUTS / "inquiry_holiday_report.csv"
    comparison_path = OUTPUTS / "eve_vs_holiday.csv"
    md_path = OUTPUTS / "report.md"

    inquiries_with_flags_table(flagged).to_csv(
        csv_path, index=False, encoding="utf-8-sig"
    )
    comparison_table(comparison).to_csv(
        comparison_path, index=False, encoding="utf-8-sig"
    )
    md_path.write_text(
        build_markdown_report(holidays, flagged, comparison),
        encoding="utf-8",
    )

    return {
        "csv": csv_path,
        "comparison_csv": comparison_path,
        "report_md": md_path,
    }
