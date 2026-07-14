"""공휴일 · 문의 워밍업 대시보드 (Community Cloud 배포용).

실행:
  streamlit run app.py

data/ 아래 교육용 샘플 데이터를 상대 경로로 읽습니다.
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from analysis import (
    attach_holiday_flags,
    compare_eve_and_holiday,
    comparison_table,
    holidays_table,
    inquiries_with_flags_table,
    load_holidays,
    load_inquiries,
    save_outputs,
    summary_rows,
)

ROOT = Path(__file__).resolve().parent


@st.cache_data
def get_dataset():
    holidays = load_holidays()
    inquiries = load_inquiries()
    flagged = attach_holiday_flags(inquiries, holidays)
    comparison = compare_eve_and_holiday(inquiries, holidays)
    return holidays, flagged, comparison


def main() -> None:
    st.set_page_config(page_title="공휴일 문의 워밍업", layout="wide")
    st.title("공휴일 · 문의 워밍업 대시보드")
    st.caption(
        "교육용 샘플 데이터로 공휴일 표, 휴일 여부, 전날/당일 문의 건수를 확인합니다."
    )

    holidays, flagged, comparison = get_dataset()
    comparable = summary_rows(comparison)

    total_eve = int(comparable["eve_count"].sum()) if len(comparable) else 0
    total_holiday = int(comparable["holiday_count"].sum()) if len(comparable) else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("공휴일 수", len(holidays))
    c2.metric("문의 행 수", len(flagged))
    c3.metric("휴일 당일 문의 행", int(flagged["is_holiday"].sum()))
    c4.metric("전날 − 당일(요약)", total_eve - total_holiday)

    st.subheader("1. 공휴일 목록 (날짜 · 공휴일명)")
    st.dataframe(holidays_table(holidays), width="stretch", hide_index=True)

    st.subheader("2. 문의 + 휴일 여부")
    flagged_view = inquiries_with_flags_table(flagged)
    only_holiday = st.checkbox("휴일 문의만 보기", value=False)
    view = flagged_view[flagged_view["휴일여부"]] if only_holiday else flagged_view
    st.dataframe(view, width="stretch", hide_index=True)

    st.subheader("3. 휴일 전날 vs 당일 문의 건수")
    st.dataframe(comparison_table(comparison), width="stretch", hide_index=True)
    st.caption(
        "요약에는 '요약포함=True'인 행만 사용합니다. "
        "전날도 공휴일인 연휴 둘째 날 등은 제외합니다."
    )

    if len(comparable):
        if total_eve > total_holiday:
            st.info(
                f"요약 기준: 전날 합계({total_eve})가 당일 합계({total_holiday})보다 많습니다."
            )
        else:
            st.info(f"요약 기준: 전날 합계 {total_eve}, 당일 합계 {total_holiday}.")

    if "report_saved" not in st.session_state:
        paths = save_outputs(holidays, flagged, comparison)
        st.session_state["report_saved"] = str(paths["report_md"].relative_to(ROOT))

    if st.button("outputs/report.md 다시 저장"):
        paths = save_outputs(holidays, flagged, comparison)
        st.session_state["report_saved"] = str(paths["report_md"].relative_to(ROOT))
        st.success(f"다시 저장했습니다: `{st.session_state['report_saved']}`")
    else:
        st.caption(f"저장됨: `{st.session_state['report_saved']}`")


if __name__ == "__main__":
    main()
