
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TABLE_DIR = PROJECT_ROOT / "results" / "tables"

st.set_page_config(
    page_title="Forecasting | Vietnam IT Recruitment",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. GLOBAL UI STYLE
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #F3F6FA;
        color: #172B4D;
    }

    [data-testid="stSidebar"] {
        background-color: #102A43;
        border-right: 1px solid #243F5A;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebarNav"] {
        display: none;
    }

    .project-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 4px 22px 4px;
        border-bottom: 1px solid rgba(255,255,255,0.16);
        margin-bottom: 22px;
    }

    .project-logo {
        width: 48px;
        height: 48px;
        min-width: 48px;
        border-radius: 12px;
        background: #FFFFFF;
        color: #075985 !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 23px;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .project-name {
        color: #FFFFFF !important;
        font-size: 15px;
        font-weight: 700;
        line-height: 1.4;
    }

    .project-subtitle {
        color: #B8C9D9 !important;
        font-size: 11px;
        margin-top: 3px;
    }

    [data-testid="stSidebar"] [data-testid="stPageLink"] a {
        border-radius: 8px;
        padding: 8px 10px;
        transition: background-color 0.2s ease;
    }

    [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {
        background-color: #243F5A;
    }

    [data-testid="stSidebar"] [data-testid="stPageLink"] p {
        color: #FFFFFF !important;
        font-size: 14px;
    }

    .sidebar-section {
        color: #9FB3C8 !important;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        margin: 20px 0 8px 4px;
    }

    .sidebar-footer {
        color: #B8C9D9 !important;
        font-size: 11px;
        line-height: 1.6;
        border-top: 1px solid rgba(255,255,255,0.16);
        padding-top: 14px;
        margin-top: 28px;
    }

    h1, h2, h3 {
        color: #102A43 !important;
        font-weight: 700 !important;
    }

    p, label {
        color: #334E68;
    }

    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #DCE4ED;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 2px 8px rgba(16, 42, 67, 0.04);
    }

    [data-testid="stMetricLabel"] {
        color: #486581 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        color: #075985 !important;
        font-size: 25px !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricDelta"] {
        display: none;
    }

    [data-testid="stCaptionContainer"] p {
        color: #52677F !important;
        font-size: 13px !important;
    }

    [data-testid="stDataFrame"] {
        background-color: #FFFFFF;
        border-radius: 10px;
    }

    .section-caption {
        color: #52677F !important;
        font-size: 14px;
        margin-top: -8px;
        margin-bottom: 15px;
    }

    .insight-box {
        background-color: #FFFFFF;
        border: 1px solid #DCE4ED;
        border-left: 4px solid #075985;
        border-radius: 10px;
        padding: 16px 22px;
        margin: 12px 0;
        box-shadow: 0 2px 8px rgba(16, 42, 67, 0.04);
    }

    .insight-box p,
    .insight-box li,
    .insight-box strong {
        color: #172B4D !important;
        font-size: 14px !important;
        line-height: 1.9;
    }

    .insight-box strong {
        color: #075985 !important;
        font-weight: 700 !important;
    }

    .insight-box ul {
        margin: 0;
        padding-left: 22px;
    }

    hr {
        border-color: #D9E2EC;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 3. SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="project-brand">
            <div class="project-logo">IT.</div>
            <div>
                <div class="project-name">
                    Vietnam IT Recruitment
                </div>
                <div class="project-subtitle">
                    Analytics Dashboard
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-section">MAIN MENU</div>',
        unsafe_allow_html=True
    )

    st.page_link("app.py", label="Overview", icon="🏠")
    st.page_link(
        "pages/1_Job_Market.py",
        label="Job Market",
        icon="💼"
    )
    st.page_link(
        "pages/2_Skills_Analysis.py",
        label="Skills Analysis",
        icon="🧠"
    )
    st.page_link(
        "pages/3_Salary_Analysis.py",
        label="Salary Analysis",
        icon="💰"
    )
    st.page_link(
        "pages/4_Recruitment_Trends.py",
        label="Recruitment Trends",
        icon="📈"
    )
    st.page_link(
        "pages/5_Forecasting.py",
        label="Forecasting",
        icon="🔮"
    )

    st.markdown(
        """
        <div class="sidebar-footer">
            <strong>Vietnam IT Recruitment Analytics</strong><br>
            Data-driven insights into the IT labor market.<br><br>
            Academic Project
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 4. LOAD DATA
# =========================================================

@st.cache_data
def load_csv(file_path):

    if not file_path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(
            file_path,
            encoding="utf-8-sig"
        )
    except UnicodeDecodeError:
        return pd.read_csv(
            file_path,
            encoding="utf-8"
        )


backtest_file = TABLE_DIR / "it_jobs_backtest.csv"
forecast_file = TABLE_DIR / "it_jobs_forecast.csv"

backtest_df = load_csv(backtest_file)
forecast_df = load_csv(forecast_file)


# =========================================================
# 5. DATA VALIDATION AND PROCESSING
# =========================================================

required_backtest = {
    "post_date",
    "job_count",
    "predicted_jobs",
    "absolute_error",
    "percentage_error"
}

required_forecast = {
    "post_date",
    "predicted_jobs"
}


if not backtest_df.empty:

    if required_backtest.issubset(backtest_df.columns):

        backtest_df["post_date"] = pd.to_datetime(
            backtest_df["post_date"],
            errors="coerce"
        )

        numeric_columns = [
            "job_count",
            "predicted_jobs",
            "absolute_error",
            "percentage_error"
        ]

        for column in numeric_columns:
            backtest_df[column] = pd.to_numeric(
                backtest_df[column],
                errors="coerce"
            )

        backtest_df = (
            backtest_df
            .dropna(
                subset=[
                    "post_date",
                    "job_count",
                    "predicted_jobs"
                ]
            )
            .sort_values("post_date")
            .reset_index(drop=True)
        )

    else:
        st.error(
            "Cấu trúc file it_jobs_backtest.csv không đúng."
        )
        st.write("Các cột hiện có:", list(backtest_df.columns))
        st.stop()


if not forecast_df.empty:

    if required_forecast.issubset(forecast_df.columns):

        forecast_df["post_date"] = pd.to_datetime(
            forecast_df["post_date"],
            errors="coerce"
        )

        forecast_df["predicted_jobs"] = pd.to_numeric(
            forecast_df["predicted_jobs"],
            errors="coerce"
        )

        forecast_df = (
            forecast_df
            .dropna(
                subset=["post_date", "predicted_jobs"]
            )
            .sort_values("post_date")
            .reset_index(drop=True)
        )

    else:
        st.error(
            "Cấu trúc file it_jobs_forecast.csv không đúng."
        )
        st.write("Các cột hiện có:", list(forecast_df.columns))
        st.stop()


# =========================================================
# 6. PAGE HEADER
# =========================================================

st.title("Recruitment Forecasting")

st.markdown(
    """
    <div class="section-caption">
        Đánh giá kết quả dự báo số lượng tin tuyển dụng IT
        thông qua dữ liệu kiểm thử và dự báo cho các tuần tiếp theo.
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# 7. CALCULATE FORECAST METRICS
# =========================================================

if not backtest_df.empty:

    mae = backtest_df["absolute_error"].mean()
    mape = backtest_df["percentage_error"].mean()

    actual_total = backtest_df["job_count"].sum()
    predicted_total = backtest_df["predicted_jobs"].sum()

    backtest_count = len(backtest_df)

else:

    mae = 0
    mape = 0
    actual_total = 0
    predicted_total = 0
    backtest_count = 0


if not forecast_df.empty:

    forecast_total = forecast_df["predicted_jobs"].sum()
    forecast_average = forecast_df["predicted_jobs"].mean()
    forecast_count = len(forecast_df)

    highest_forecast = forecast_df.loc[
        forecast_df["predicted_jobs"].idxmax()
    ]

    highest_forecast_date = (
        highest_forecast["post_date"].strftime("%d/%m/%Y")
    )

    highest_forecast_jobs = highest_forecast["predicted_jobs"]

else:

    forecast_total = 0
    forecast_average = 0
    forecast_count = 0
    highest_forecast_date = "N/A"
    highest_forecast_jobs = 0


# =========================================================
# 8. KPI OVERVIEW
# =========================================================

st.subheader("Tổng quan kết quả dự báo")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "MAE",
        f"{mae:,.2f}" if not backtest_df.empty else "N/A"
    )

with col2:
    st.metric(
        "MAPE",
        f"{mape:.2f}%" if not backtest_df.empty else "N/A"
    )

with col3:
    st.metric(
        "Tổng tin dự báo",
        f"{forecast_total:,.0f}"
        if not forecast_df.empty else "N/A"
    )

with col4:
    st.metric(
        "Trung bình tin dự báo/tuần",
        f"{forecast_average:,.1f}"
        if not forecast_df.empty else "N/A"
    )

st.caption(
    "MAE: sai số tuyệt đối trung bình. "
    "MAPE: sai số phần trăm tuyệt đối trung bình."
)

st.divider()


# =========================================================
# 9. BACKTEST: ACTUAL VS PREDICTED
# =========================================================

st.subheader("Đánh giá mô hình bằng dữ liệu Backtest")

st.markdown(
    """
    <div class="section-caption">
        So sánh số lượng tin tuyển dụng thực tế với kết quả
        dự báo tại cùng thời điểm kiểm thử.
    </div>
    """,
    unsafe_allow_html=True
)

if not backtest_df.empty:

    backtest_chart = backtest_df[
        ["post_date", "job_count", "predicted_jobs"]
    ].copy()

    backtest_chart = backtest_chart.melt(
        id_vars="post_date",
        value_vars=[
            "job_count",
            "predicted_jobs"
        ],
        var_name="data_type",
        value_name="jobs"
    )

    backtest_chart["data_type"] = (
        backtest_chart["data_type"].map({
            "job_count": "Thực tế",
            "predicted_jobs": "Dự báo"
        })
    )

    fig_backtest = px.bar(
        backtest_chart,
        x="post_date",
        y="jobs",
        color="data_type",
        barmode="group",
        color_discrete_map={
            "Thực tế": "#075985",
            "Dự báo": "#38BDF8"
        },
        labels={
            "post_date": "Thời gian",
            "jobs": "Số lượng tin tuyển dụng",
            "data_type": "Loại dữ liệu"
        }
    )

    fig_backtest.update_traces(
        hovertemplate=(
            "Ngày: %{x|%d/%m/%Y}<br>"
            "Số lượng: %{y:,.2f}"
            "<extra></extra>"
        )
    )

    fig_backtest.update_layout(
        height=420,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(
            family="Arial",
            size=13,
            color="#172B4D"
        ),
        legend=dict(
            title="",
            font=dict(
                color="#172B4D",
                size=13
            )
        ),
        xaxis=dict(
            title="Thời gian",
            tickformat="%d/%m/%Y",
            tickfont=dict(
                color="#172B4D",
                size=12
            ),
            title_font=dict(
                color="#172B4D",
                size=14
            ),
            showgrid=False
        ),
        yaxis=dict(
            title="Số lượng tin tuyển dụng",
            tickfont=dict(
                color="#172B4D",
                size=12
            ),
            title_font=dict(
                color="#172B4D",
                size=14
            ),
            gridcolor="#DCE4ED",
            rangemode="tozero"
        ),
        margin=dict(
            l=25,
            r=25,
            t=25,
            b=25
        ),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font=dict(color="#172B4D")
        )
    )

    st.plotly_chart(
        fig_backtest,
        use_container_width=True,
        config={"displayModeBar": False}
    )

else:

    st.warning(
        "Không có dữ liệu backtest hợp lệ để đánh giá mô hình."
    )


# =========================================================
# 10. FORECAST RESULTS
# =========================================================

st.divider()

st.subheader("Dự báo số lượng tin tuyển dụng trong tương lai")

st.markdown(
    """
    <div class="section-caption">
        Số lượng tin tuyển dụng dự kiến trong các tuần tiếp theo
        theo kết quả đầu ra của mô hình dự báo.
    </div>
    """,
    unsafe_allow_html=True
)

if not forecast_df.empty:

    fig_forecast = px.line(
        forecast_df,
        x="post_date",
        y="predicted_jobs",
        markers=True,
        labels={
            "post_date": "Thời gian",
            "predicted_jobs": "Số lượng tin dự báo"
        }
    )

    fig_forecast.update_traces(
        line=dict(
            color="#075985",
            width=3
        ),
        marker=dict(
            size=10,
            color="#0EA5E9",
            line=dict(
                color="#075985",
                width=1
            )
        ),
        hovertemplate=(
            "Ngày: %{x|%d/%m/%Y}<br>"
            "Số tin dự báo: %{y:,.0f}"
            "<extra></extra>"
        )
    )

    fig_forecast.update_layout(
        height=420,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(
            family="Arial",
            size=13,
            color="#172B4D"
        ),
        xaxis=dict(
            title="Thời gian",
            tickformat="%d/%m/%Y",
            tickfont=dict(
                color="#172B4D",
                size=12
            ),
            title_font=dict(
                color="#172B4D",
                size=14
            ),
            showgrid=False
        ),
        yaxis=dict(
            title="Số lượng tin tuyển dụng dự báo",
            tickfont=dict(
                color="#172B4D",
                size=12
            ),
            title_font=dict(
                color="#172B4D",
                size=14
            ),
            gridcolor="#DCE4ED",
            rangemode="tozero"
        ),
        margin=dict(
            l=25,
            r=25,
            t=25,
            b=25
        ),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font=dict(color="#172B4D")
        )
    )

    st.plotly_chart(
        fig_forecast,
        use_container_width=True,
        config={"displayModeBar": False}
    )

else:

    st.warning(
        "Không tìm thấy dữ liệu dự báo hợp lệ."
    )


# =========================================================
# 11. BACKTEST DETAIL TABLE
# =========================================================

st.divider()

st.subheader("Chi tiết kết quả Backtest")

if not backtest_df.empty:

    backtest_display = backtest_df.copy()

    backtest_display["post_date"] = (
        backtest_display["post_date"].dt.strftime("%d/%m/%Y")
    )

    backtest_display = backtest_display.rename(
        columns={
            "post_date": "Ngày",
            "job_count": "Số lượng thực tế",
            "predicted_jobs": "Số lượng dự báo",
            "absolute_error": "Sai số tuyệt đối",
            "percentage_error": "Sai số phần trăm (%)"
        }
    )

    backtest_display = backtest_display.round(2)

    st.dataframe(
        backtest_display,
        use_container_width=True,
        hide_index=True,
        height=250
    )

else:

    st.info("Chưa có dữ liệu Backtest.")


# =========================================================
# 12. FORECAST DETAIL TABLE
# =========================================================

st.subheader("Chi tiết kết quả dự báo")

if not forecast_df.empty:

    forecast_display = forecast_df.copy()

    forecast_display["post_date"] = (
        forecast_display["post_date"].dt.strftime("%d/%m/%Y")
    )

    forecast_display = forecast_display.rename(
        columns={
            "post_date": "Ngày dự báo",
            "predicted_jobs": "Số lượng tin tuyển dụng dự báo"
        }
    )

    forecast_display[
        "Số lượng tin tuyển dụng dự báo"
    ] = forecast_display[
        "Số lượng tin tuyển dụng dự báo"
    ].round(0)

    st.dataframe(
        forecast_display,
        use_container_width=True,
        hide_index=True,
        height=220
    )

else:

    st.info("Chưa có dữ liệu dự báo.")


# =========================================================
# 13. DATA INTERPRETATION
# =========================================================

st.divider()

st.subheader("Tổng quan nhận xét")

if not backtest_df.empty:

    st.markdown(
        f"""
        <div class="insight-box">
            <ul>
                <li>
                    Tập dữ liệu Backtest hiện có
                    <strong>{backtest_count} tuần kiểm thử</strong>.
                </li>
                <li>
                    Sai số tuyệt đối trung bình (MAE) đạt
                    <strong>{mae:,.2f} tin</strong>.
                </li>
                <li>
                    Sai số phần trăm trung bình (MAPE) đạt
                    <strong>{mape:.2f}%</strong>.
                </li>
                <li>
                    Tổng số tin tuyển dụng thực tế trong giai đoạn
                    kiểm thử là <strong>{actual_total:,.0f} tin</strong>,
                    trong khi tổng dự báo là
                    <strong>{predicted_total:,.2f} tin</strong>.
                </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.info(
        "Chưa đủ dữ liệu để đưa ra nhận xét Backtest."
    )


if not forecast_df.empty:

    st.markdown(
        f"""
        <div class="insight-box">
            <ul>
                <li>
                    Mô hình đưa ra dự báo cho
                    <strong>{forecast_count} tuần tiếp theo</strong>.
                </li>
                <li>
                    Tổng số tin tuyển dụng dự kiến là
                    <strong>{forecast_total:,.0f} tin</strong>.
                </li>
                <li>
                    Trung bình mỗi tuần dự kiến có
                    <strong>{forecast_average:,.1f} tin tuyển dụng</strong>.
                </li>
                <li>
                    Mức dự báo cao nhất thuộc về tuần
                    <strong>{highest_forecast_date}</strong>,
                    với <strong>{highest_forecast_jobs:,.0f} tin</strong>.
                </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.info(
        "Chưa có dữ liệu để đưa ra nhận xét dự báo."
    )


# =========================================================
# 14. FORECASTING LIMITATIONS
# =========================================================

st.subheader("Lưu ý khi diễn giải kết quả")

st.markdown(
    """
    <div class="insight-box">
        <ul>
            <li>
                Kết quả Backtest hiện chỉ bao gồm một số ít mốc thời gian,
                vì vậy các chỉ số MAE và MAPE chỉ phản ánh tập kiểm thử
                hiện có.
            </li>
            <li>
                Dự báo được trình bày theo dữ liệu đầu ra của mô hình,
                không phải số lượng tin tuyển dụng đã được quan sát thực tế.
            </li>
            <li>
                Cần bổ sung thêm dữ liệu kiểm thử ở nhiều giai đoạn
                để đánh giá độ ổn định và khả năng tổng quát hóa
                của mô hình.
            </li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 15. FOOTER
# =========================================================

st.divider()

st.caption(
    "Vietnam IT Recruitment Analytics | "
    "Recruitment Forecasting"
)
