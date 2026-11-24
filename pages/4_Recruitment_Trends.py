
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
    page_title="Recruitment Trends | Vietnam IT Recruitment",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. GLOBAL STYLE
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #F3F6FA;
        color: #172B4D;
    }

    [data-testid="stHeader"] {
        background-color: transparent;
    }

    [data-testid="stSidebar"] {
        background-color: #102A43;
        border-right: 1px solid #243F5A;
    }

    [data-testid="stSidebar"] > div:first-child {
        background-color: #102A43;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF;
    }

    [data-testid="stSidebarNav"] {
        display: none;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #D9E7F5;
    }

    .project-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 4px 18px 4px;
        border-bottom: 1px solid rgba(255,255,255,0.15);
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
        color: #FFFFFF;
        font-size: 15px;
        font-weight: 700;
        line-height: 1.4;
    }

    .project-subtitle {
        color: #B8CCE0;
        font-size: 11px;
        margin-top: 3px;
    }

    [data-testid="stSidebar"] a {
        color: #EAF2F8 !important;
        border-radius: 8px;
        padding: 8px 10px;
    }

    [data-testid="stSidebar"] a:hover {
        background-color: #243F5A;
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] a[aria-current="page"] {
        background-color: #1D4E89 !important;
        color: #FFFFFF !important;
        font-weight: 700;
    }

    .sidebar-section {
        color: #91AFCB;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        margin: 20px 0 8px 4px;
    }

    .sidebar-footer {
        border-top: 1px solid rgba(255,255,255,0.15);
        margin-top: 30px;
        padding-top: 14px;
        color: #B8CCE0;
        font-size: 11px;
        line-height: 1.7;
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
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 2px 8px rgba(16, 42, 67, 0.04);
    }

    [data-testid="stMetricLabel"] {
        color: #52677F !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        color: #075985 !important;
        font-size: 25px !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricValue"] div {
        color: #075985 !important;
    }

    [data-testid="stCaptionContainer"] p {
        color: #52677F !important;
        font-size: 13px !important;
    }

    [data-testid="stDataFrame"] {
        background-color: #FFFFFF;
        border-radius: 10px;
    }

    div[data-testid="stPlotlyChart"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 2px 8px rgba(16, 42, 67, 0.03);
    }

    .insight-box {
        background-color: #FFFFFF;
        border: 1px solid #DCE4ED;
        border-left: 4px solid #075985;
        border-radius: 10px;
        padding: 16px 22px;
        margin: 12px 0;
        box-shadow: 0 2px 8px rgba(16, 42, 67, 0.03);
    }

    .insight-box p,
    .insight-box li {
        color: #334E68 !important;
        font-size: 14px !important;
        line-height: 1.8;
    }

    .insight-box strong {
        color: #075985 !important;
        font-weight: 700 !important;
    }

    .insight-box ul {
        margin-top: 0;
        margin-bottom: 0;
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
                <div class="project-name">Vietnam IT<br>Recruitment Analytics</div>
                <div class="project-subtitle">Data Analytics Dashboard</div>
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
    st.page_link("pages/1_Job_Market.py", label="Job Market", icon="💼")
    st.page_link("pages/2_Skills_Analysis.py", label="Skills Analysis", icon="🧠")
    st.page_link("pages/3_Salary_Analysis.py", label="Salary Analysis", icon="💰")
    st.page_link("pages/4_Recruitment_Trends.py", label="Recruitment Trends", icon="📈")
    st.page_link("pages/5_Forecasting.py", label="Forecasting", icon="🔮")

    st.markdown(
        """
        <div class="sidebar-footer">
            <b>VIETNAM IT RECRUITMENT</b><br>
            Recruitment Market Intelligence<br>
            Data-driven Insights
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 4. PAGE HEADER
# =========================================================

st.title("Recruitment Trends")

st.caption(
    "Phân tích xu hướng tuyển dụng nhân sự IT theo thời gian, "
    "dựa trên dữ liệu thống kê theo tháng và theo tuần."
)

st.divider()


# =========================================================
# 5. LOAD DATA
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


monthly_file = TABLE_DIR / "monthly_recruitment_trend.csv"
weekly_file = TABLE_DIR / "weekly_recruitment_data.csv"

monthly_df = load_csv(monthly_file)
weekly_df = load_csv(weekly_file)


# =========================================================
# 6. DATA VALIDATION AND PROCESSING
# =========================================================

# Process monthly data
if not monthly_df.empty:

    required_monthly = {
        "month",
        "job_count"
    }

    if required_monthly.issubset(monthly_df.columns):

        monthly_df["month"] = pd.to_datetime(
            monthly_df["month"],
            errors="coerce"
        )

        monthly_df["job_count"] = pd.to_numeric(
            monthly_df["job_count"],
            errors="coerce"
        )

        monthly_df = (
            monthly_df
            .dropna(subset=["month", "job_count"])
            .sort_values("month")
            .reset_index(drop=True)
        )

        if "month_label" not in monthly_df.columns:
            monthly_df["month_label"] = (
                monthly_df["month"].dt.strftime("%m/%Y")
            )

    else:
        monthly_df = pd.DataFrame()


# Process weekly data
if not weekly_df.empty:

    required_weekly = {
        "post_date",
        "job_count"
    }

    if required_weekly.issubset(weekly_df.columns):

        weekly_df["post_date"] = pd.to_datetime(
            weekly_df["post_date"],
            errors="coerce"
        )

        weekly_df["job_count"] = pd.to_numeric(
            weekly_df["job_count"],
            errors="coerce"
        )

        weekly_df = (
            weekly_df
            .dropna(subset=["post_date", "job_count"])
            .sort_values("post_date")
            .reset_index(drop=True)
        )

    else:
        weekly_df = pd.DataFrame()


# Remove negative values
if not monthly_df.empty:
    monthly_df = monthly_df[
        monthly_df["job_count"] >= 0
    ].copy()

if not weekly_df.empty:
    weekly_df = weekly_df[
        weekly_df["job_count"] >= 0
    ].copy()


# =========================================================
# 7. KPI OVERVIEW
# =========================================================

monthly_total = (
    monthly_df["job_count"].sum()
    if not monthly_df.empty
    else 0
)

monthly_average = (
    monthly_df["job_count"].mean()
    if not monthly_df.empty
    else 0
)

if not monthly_df.empty:

    peak_month_row = monthly_df.loc[
        monthly_df["job_count"].idxmax()
    ]

    peak_month = str(peak_month_row["month_label"])
    peak_month_jobs = float(peak_month_row["job_count"])

else:
    peak_month = "N/A"
    peak_month_jobs = 0


if not weekly_df.empty:

    peak_week_row = weekly_df.loc[
        weekly_df["job_count"].idxmax()
    ]

    peak_week = peak_week_row["post_date"].strftime(
        "%d/%m/%Y"
    )

    peak_week_jobs = float(
        peak_week_row["job_count"]
    )

else:
    peak_week = "N/A"
    peak_week_jobs = 0


st.subheader("Tổng quan xu hướng tuyển dụng")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Tổng tin theo tháng",
        f"{monthly_total:,.0f}"
    )

with col2:
    st.metric(
        "Trung bình tin/tháng",
        f"{monthly_average:,.1f}"
    )

with col3:
    st.metric(
        "Tháng tuyển dụng cao nhất",
        peak_month
    )

    st.caption(
        f"{peak_month_jobs:,.0f} tin tuyển dụng"
    )

with col4:
    st.metric(
        "Tuần tuyển dụng cao nhất",
        peak_week
    )

    st.caption(
        f"{peak_week_jobs:,.0f} tin tuyển dụng"
    )

st.caption(
    "Các chỉ số được tính từ dữ liệu tổng hợp theo tháng và theo tuần. "
    "Tổng tin theo tháng là tổng các giá trị trong bảng thống kê tháng."
)

st.divider()


# =========================================================
# 8. MONTHLY RECRUITMENT TREND
# =========================================================

st.subheader("Xu hướng tuyển dụng theo tháng")

st.caption(
    "Biến động số lượng tin tuyển dụng IT qua từng tháng."
)

if not monthly_df.empty:

    fig_monthly = px.line(
        monthly_df,
        x="month",
        y="job_count",
        markers=True,
        labels={
            "month": "Thời gian",
            "job_count": "Số lượng tin tuyển dụng"
        }
    )

    fig_monthly.update_traces(
        line=dict(
            color="#075985",
            width=3
        ),
        marker=dict(
            size=8,
            color="#0EA5E9"
        ),
        hovertemplate=(
            "Tháng: %{x|%m/%Y}<br>"
            "Số tin tuyển dụng: %{y:,.0f}"
            "<extra></extra>"
        )
    )

    fig_monthly.update_layout(
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
            tickformat="%m/%Y",
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
        fig_monthly,
        use_container_width=True,
        config={"displayModeBar": False}
    )

else:

    st.warning(
        "Không tìm thấy dữ liệu hợp lệ trong "
        "monthly_recruitment_trend.csv."
    )


# =========================================================
# 9. WEEKLY RECRUITMENT TREND
# =========================================================

st.divider()

st.subheader("Xu hướng tuyển dụng theo tuần")

st.caption(
    "Theo dõi số lượng tin tuyển dụng được tổng hợp theo từng tuần."
)

if not weekly_df.empty:

    fig_weekly = px.bar(
        weekly_df,
        x="post_date",
        y="job_count",
        labels={
            "post_date": "Ngày đại diện tuần",
            "job_count": "Số lượng tin tuyển dụng"
        }
    )

    fig_weekly.update_traces(
        marker_color="#0EA5E9",
        marker_line_color="#075985",
        marker_line_width=0.5,
        hovertemplate=(
            "Ngày: %{x|%d/%m/%Y}<br>"
            "Số tin tuyển dụng: %{y:,.0f}"
            "<extra></extra>"
        )
    )

    fig_weekly.update_layout(
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
                size=11
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
        fig_weekly,
        use_container_width=True,
        config={"displayModeBar": False}
    )

else:

    st.warning(
        "Không tìm thấy dữ liệu hợp lệ trong "
        "weekly_recruitment_data.csv."
    )


# =========================================================
# 10. MONTHLY DATA TABLE
# =========================================================

st.divider()

st.subheader("Chi tiết dữ liệu tuyển dụng theo tháng")

if not monthly_df.empty:

    monthly_display = monthly_df.copy()

    monthly_display["month"] = (
        monthly_display["month"].dt.strftime("%m/%Y")
    )

    monthly_display = monthly_display.rename(
        columns={
            "month": "Tháng",
            "month_label": "Nhãn thời gian",
            "job_count": "Số lượng tin tuyển dụng"
        }
    )

    display_columns = [
        column
        for column in [
            "Tháng",
            "Nhãn thời gian",
            "Số lượng tin tuyển dụng"
        ]
        if column in monthly_display.columns
    ]

    st.dataframe(
        monthly_display[display_columns],
        use_container_width=True,
        hide_index=True,
        height=350
    )

else:

    st.info(
        "Chưa có dữ liệu tuyển dụng theo tháng."
    )


# =========================================================
# 11. WEEKLY DATA TABLE
# =========================================================

st.divider()

st.subheader("Chi tiết dữ liệu tuyển dụng theo tuần")

if not weekly_df.empty:

    weekly_display = weekly_df.copy()

    weekly_display["post_date"] = (
        weekly_display["post_date"].dt.strftime("%d/%m/%Y")
    )

    weekly_display = weekly_display.rename(
        columns={
            "post_date": "Ngày đại diện tuần",
            "job_count": "Số lượng tin tuyển dụng"
        }
    )

    st.dataframe(
        weekly_display,
        use_container_width=True,
        hide_index=True,
        height=350
    )

else:

    st.info(
        "Chưa có dữ liệu tuyển dụng theo tuần."
    )


# =========================================================
# 12. DATA INTERPRETATION
# =========================================================

st.divider()

st.subheader("Tổng quan nhận xét")

if not monthly_df.empty:

    st.markdown(
        f"""
        <div class="insight-box">
            <ul>
                <li>
                    Dữ liệu thống kê theo tháng ghi nhận
                    <strong>{monthly_total:,.0f} tin tuyển dụng</strong>.
                </li>
                <li>
                    Số lượng tin tuyển dụng trung bình đạt
                    <strong>{monthly_average:,.1f} tin/tháng</strong>.
                </li>
                <li>
                    Tháng có số lượng tin tuyển dụng cao nhất là
                    <strong>{peak_month}</strong>,
                    với <strong>{peak_month_jobs:,.0f} tin</strong>.
                </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.info(
        "Chưa đủ dữ liệu để đưa ra nhận xét theo tháng."
    )


if not weekly_df.empty:

    st.markdown(
        f"""
        <div class="insight-box">
            <ul>
                <li>
                    Dữ liệu theo tuần ghi nhận
                    <strong>{len(weekly_df):,} mốc thời gian</strong>.
                </li>
                <li>
                    Tuần có số lượng tin tuyển dụng cao nhất là
                    <strong>{peak_week}</strong>,
                    với <strong>{peak_week_jobs:,.0f} tin</strong>.
                </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.info(
        "Chưa đủ dữ liệu để đưa ra nhận xét theo tuần."
    )


# =========================================================
# 13. FOOTER
# =========================================================

st.divider()

st.caption(
    "Nguồn dữ liệu: Data Warehouse – IT Recruitment Analysis | "
    "Vietnam IT Recruitment Analytics"
)
