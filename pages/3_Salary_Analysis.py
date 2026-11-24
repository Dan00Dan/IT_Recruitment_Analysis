
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
    page_title="Salary Analysis | Vietnam IT Recruitment",
    page_icon="💰",
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

st.title("Salary Analysis")

st.caption(
    "Phân tích mức lương tuyển dụng IT theo vị trí công việc, "
    "cấp độ kinh nghiệm và tình trạng công khai lương."
)


# =========================================================
# 5. LOAD DATA
# =========================================================

@st.cache_data
def load_csv(filename):
    file_path = TABLE_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy file dữ liệu: {file_path}"
        )

    try:
        return pd.read_csv(file_path, encoding="utf-8-sig")
    except UnicodeDecodeError:
        return pd.read_csv(file_path, encoding="utf-8")


try:
    salary_role = load_csv("salary_by_role.csv")
    salary_level = load_csv("salary_by_level.csv")
    salary_disclosure = load_csv("salary_disclosure.csv")

except Exception as error:
    st.error(f"Không thể tải dữ liệu: {error}")
    st.stop()


# =========================================================
# 6. VALIDATE DATA
# =========================================================

salary_metrics = {
    "job_count",
    "median_salary",
    "mean_salary",
    "min_salary",
    "max_salary"
}

required_role = {"role"} | salary_metrics
required_level = {"level"} | salary_metrics

required_disclosure = {
    "Salary Status",
    "Job Count",
    "Percentage"
}

if not required_role.issubset(salary_role.columns):
    st.error("Cấu trúc salary_by_role.csv không đúng.")
    st.write("Các cột hiện có:", list(salary_role.columns))
    st.stop()

if not required_level.issubset(salary_level.columns):
    st.error("Cấu trúc salary_by_level.csv không đúng.")
    st.write("Các cột hiện có:", list(salary_level.columns))
    st.stop()

if not required_disclosure.issubset(
    salary_disclosure.columns
):
    st.error("Cấu trúc salary_disclosure.csv không đúng.")
    st.write(
        "Các cột hiện có:",
        list(salary_disclosure.columns)
    )
    st.stop()


# =========================================================
# 7. DATA PREPARATION
# =========================================================

numeric_columns = [
    "job_count",
    "median_salary",
    "mean_salary",
    "min_salary",
    "max_salary"
]

for column in numeric_columns:
    salary_role[column] = pd.to_numeric(
        salary_role[column],
        errors="coerce"
    )

    salary_level[column] = pd.to_numeric(
        salary_level[column],
        errors="coerce"
    )

salary_disclosure["Job Count"] = pd.to_numeric(
    salary_disclosure["Job Count"],
    errors="coerce"
)

salary_disclosure["Percentage"] = pd.to_numeric(
    salary_disclosure["Percentage"],
    errors="coerce"
)

salary_role["role"] = (
    salary_role["role"].astype("string").str.strip()
)

salary_level["level"] = (
    salary_level["level"].astype("string").str.strip()
)

salary_disclosure["Salary Status"] = (
    salary_disclosure["Salary Status"]
    .astype("string")
    .str.strip()
)

salary_role = salary_role.dropna(
    subset=["role", "median_salary"]
)

salary_level = salary_level.dropna(
    subset=["level", "median_salary"]
)

salary_disclosure = salary_disclosure.dropna(
    subset=["Salary Status", "Job Count", "Percentage"]
)

salary_role = salary_role[
    salary_role["role"].ne("")
    & (salary_role["median_salary"] > 0)
].copy()

salary_level = salary_level[
    salary_level["level"].ne("")
    & (salary_level["median_salary"] > 0)
].copy()

salary_disclosure = salary_disclosure[
    salary_disclosure["Salary Status"].ne("")
    & (salary_disclosure["Job Count"] >= 0)
    & (salary_disclosure["Percentage"] >= 0)
].copy()

if salary_role.empty:
    st.warning("Không có dữ liệu mức lương hợp lệ theo vị trí.")
    st.stop()

if salary_level.empty:
    st.warning("Không có dữ liệu mức lương hợp lệ theo cấp độ.")
    st.stop()

if salary_disclosure.empty:
    st.warning("Không có dữ liệu về tình trạng công khai lương.")
    st.stop()

salary_role = salary_role.sort_values(
    "median_salary",
    ascending=False
).reset_index(drop=True)

salary_level = salary_level.sort_values(
    "median_salary",
    ascending=False
).reset_index(drop=True)


# =========================================================
# 8. CALCULATE KPIs
# =========================================================

# Total records classified in salary disclosure table
total_salary_jobs = int(
    salary_disclosure["Job Count"].sum()
)

# Find records with disclosed salary
available_salary = salary_disclosure[
    salary_disclosure["Salary Status"]
    .str.contains("available", case=False, na=False)
]

if not available_salary.empty:

    disclosed_jobs = int(
        available_salary["Job Count"].sum()
    )

    disclosure_rate = float(
        available_salary["Percentage"].sum()
    )

else:
    disclosed_jobs = 0
    disclosure_rate = 0.0

# Median of median salaries across job roles
overall_median = float(
    salary_role["median_salary"].median()
)


# =========================================================
# 9. KPI OVERVIEW
# =========================================================

st.subheader("Tổng quan mức lương")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "Tin trong thống kê công khai lương",
        f"{total_salary_jobs:,}"
    )

with k2:
    st.metric(
        "Tin có công khai lương",
        f"{disclosed_jobs:,}"
    )

with k3:
    st.metric(
        "Tỷ lệ công khai lương",
        f"{disclosure_rate:.2f}%"
    )

with k4:
    st.metric(
        "Median lương giữa các vị trí",
        f"{overall_median:.1f} triệu"
    )

st.caption(
    "Đơn vị mức lương: triệu VNĐ/tháng. "
    "Median tổng quan là trung vị của các mức lương trung vị theo vị trí."
)

st.divider()


# =========================================================
# 10. SALARY BY JOB ROLE
# =========================================================

st.subheader("Mức lương theo vị trí công việc")

st.caption(
    "So sánh mức lương trung vị giữa các nhóm vị trí IT. "
    "Mức lương được tính bằng triệu VNĐ/tháng."
)

role_chart_data = salary_role.sort_values(
    "median_salary",
    ascending=True
)

fig_role = px.bar(
    role_chart_data,
    x="median_salary",
    y="role",
    orientation="h",
    text="median_salary",
    color="median_salary",
    color_continuous_scale="Blues",
    labels={
        "median_salary": "Lương trung vị (triệu VNĐ)",
        "role": "Vị trí"
    }
)

fig_role.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside",
    textfont=dict(
        family="Arial",
        size=12,
        color="#102A43"
    ),
    cliponaxis=False
)

fig_role.update_layout(
    height=600,
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font=dict(
        family="Arial",
        size=13,
        color="#172B4D"
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor="#DCE4ED",
        zeroline=False,
        title="Lương trung vị (triệu VNĐ/tháng)",
        tickfont=dict(size=12, color="#172B4D")
    ),
    yaxis=dict(
        title="",
        automargin=True,
        tickfont=dict(size=12, color="#172B4D")
    ),
    coloraxis_showscale=False,
    margin=dict(l=20, r=80, t=25, b=45)
)

st.plotly_chart(
    fig_role,
    use_container_width=True,
    config={"displayModeBar": False}
)


# =========================================================
# 11. SALARY BY EXPERIENCE LEVEL
# =========================================================

st.divider()

st.subheader("Mức lương theo cấp độ kinh nghiệm")

st.caption(
    "Phân tích sự khác biệt về mức lương giữa các cấp độ "
    "kinh nghiệm trong tuyển dụng IT."
)

level_chart_data = salary_level.copy()

fig_level = px.bar(
    level_chart_data,
    x="level",
    y="median_salary",
    text="median_salary",
    color="median_salary",
    color_continuous_scale="Teal",
    labels={
        "level": "Cấp độ",
        "median_salary": "Lương trung vị (triệu VNĐ)"
    }
)

fig_level.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside",
    textfont=dict(
        family="Arial",
        size=12,
        color="#102A43"
    ),
    cliponaxis=False
)

fig_level.update_layout(
    height=460,
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    font=dict(
        family="Arial",
        size=13,
        color="#172B4D"
    ),
    xaxis=dict(
        title="Cấp độ kinh nghiệm",
        tickfont=dict(size=12, color="#172B4D")
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="#DCE4ED",
        zeroline=False,
        title="Lương trung vị (triệu VNĐ/tháng)",
        tickfont=dict(size=12, color="#172B4D")
    ),
    coloraxis_showscale=False,
    margin=dict(l=30, r=60, t=25, b=55)
)

st.plotly_chart(
    fig_level,
    use_container_width=True,
    config={"displayModeBar": False}
)


# =========================================================
# 12. SALARY DISCLOSURE
# =========================================================

st.divider()

st.subheader("Tình trạng công khai mức lương")

st.caption(
    "Thể hiện số lượng và tỷ trọng tin tuyển dụng "
    "có hoặc không công khai mức lương."
)

col_chart, col_info = st.columns(
    [1.5, 1],
    gap="large"
)

with col_chart:

    fig_disclosure = px.pie(
        salary_disclosure,
        names="Salary Status",
        values="Job Count",
        hole=0.58,
        color_discrete_sequence=[
            "#1677B8",
            "#B8C9D9",
            "#5B9BD5",
            "#DCE6F1"
        ]
    )

    fig_disclosure.update_traces(
        textposition="inside",
        textinfo="percent+label",
        textfont=dict(
            family="Arial",
            size=12,
            color="#102A43"
        ),
        hovertemplate=(
            "%{label}<br>"
            "Số tin: %{value:,.0f}<br>"
            "Tỷ lệ: %{percent}"
            "<extra></extra>"
        )
    )

    fig_disclosure.update_layout(
        height=420,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Arial",
            size=12,
            color="#172B4D"
        ),
        showlegend=True,
        legend=dict(
            font=dict(
                size=11,
                color="#172B4D"
            )
        ),
        margin=dict(l=15, r=15, t=25, b=25)
    )

    st.plotly_chart(
        fig_disclosure,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with col_info:

    st.markdown("#### Thống kê công khai lương")

    st.metric(
        "Tin có công khai lương",
        f"{disclosed_jobs:,}"
    )

    st.metric(
        "Tỷ lệ công khai",
        f"{disclosure_rate:.2f}%"
    )

    st.markdown(
        """
        **Ý nghĩa phân tích**

        - Cho biết mức độ minh bạch về lương trong tin tuyển dụng.
        - Hỗ trợ đánh giá khả năng tiếp cận thông tin thu nhập.
        - Cung cấp cơ sở để xem xét tình trạng công khai lương
          trên thị trường tuyển dụng IT.
        """
    )


# =========================================================
# 13. SALARY DATA TABLE - ROLE
# =========================================================

st.divider()

st.subheader("Chi tiết mức lương theo vị trí")

display_role = salary_role[
    [
        "role",
        "job_count",
        "median_salary",
        "mean_salary",
        "min_salary",
        "max_salary"
    ]
].copy()

display_role.columns = [
    "Vị trí",
    "Số tin tuyển dụng",
    "Lương trung vị",
    "Lương trung bình",
    "Lương thấp nhất",
    "Lương cao nhất"
]

salary_table_columns = [
    "Lương trung vị",
    "Lương trung bình",
    "Lương thấp nhất",
    "Lương cao nhất"
]

for column in salary_table_columns:
    display_role[column] = (
        display_role[column].round(2)
    )

st.dataframe(
    display_role,
    use_container_width=True,
    hide_index=True,
    height=420
)


# =========================================================
# 14. SALARY DATA TABLE - LEVEL
# =========================================================

st.divider()

st.subheader("Chi tiết mức lương theo cấp độ")

display_level = salary_level[
    [
        "level",
        "job_count",
        "median_salary",
        "mean_salary",
        "min_salary",
        "max_salary"
    ]
].copy()

display_level.columns = [
    "Cấp độ",
    "Số tin tuyển dụng",
    "Lương trung vị",
    "Lương trung bình",
    "Lương thấp nhất",
    "Lương cao nhất"
]

for column in salary_table_columns:
    display_level[column] = (
        display_level[column].round(2)
    )

st.dataframe(
    display_level,
    use_container_width=True,
    hide_index=True,
    height=350
)


# =========================================================
# 15. FOOTER
# =========================================================

st.divider()

st.caption(
    "Nguồn dữ liệu: Data Warehouse – IT Recruitment Analysis | "
    "Vietnam IT Recruitment Analytics"
)
