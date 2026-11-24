
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
    page_title="Skills Analysis | Vietnam IT Recruitment",
    page_icon="🧠",
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

st.title("Skills Analysis")

st.caption(
    "Phân tích các kỹ năng công nghệ được yêu cầu "
    "trong thị trường tuyển dụng IT Việt Nam."
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
    top_skills = load_csv("top_skills.csv")
    skill_by_role = load_csv("skill_by_role.csv")
    skill_rate = load_csv("skill_requirement_rate.csv")

except Exception as error:
    st.error(f"Không thể tải dữ liệu: {error}")
    st.stop()


# =========================================================
# 6. VALIDATE DATA
# =========================================================

required_top = {
    "skill_name",
    "job_count",
    "percentage"
}

required_role = {
    "skill_name"
}

required_rate = {
    "skill_name",
    "job_count",
    "percentage",
    "requirement_rate"
}

if not required_top.issubset(top_skills.columns):
    st.error("Cấu trúc file top_skills.csv không đúng.")
    st.write("Các cột hiện có:", list(top_skills.columns))
    st.stop()

if not required_role.issubset(skill_by_role.columns):
    st.error("Cấu trúc file skill_by_role.csv không đúng.")
    st.write("Các cột hiện có:", list(skill_by_role.columns))
    st.stop()

if not required_rate.issubset(skill_rate.columns):
    st.error("Cấu trúc file skill_requirement_rate.csv không đúng.")
    st.write("Các cột hiện có:", list(skill_rate.columns))
    st.stop()


# =========================================================
# 7. DATA PREPARATION
# =========================================================

for column in ["job_count", "percentage"]:
    top_skills[column] = pd.to_numeric(
        top_skills[column],
        errors="coerce"
    )

for column in ["job_count", "percentage", "requirement_rate"]:
    skill_rate[column] = pd.to_numeric(
        skill_rate[column],
        errors="coerce"
    )

top_skills["skill_name"] = (
    top_skills["skill_name"].astype("string").str.strip()
)

skill_rate["skill_name"] = (
    skill_rate["skill_name"].astype("string").str.strip()
)

skill_by_role["skill_name"] = (
    skill_by_role["skill_name"].astype("string").str.strip()
)

top_skills = top_skills.dropna(
    subset=["skill_name", "job_count"]
)

skill_rate = skill_rate.dropna(
    subset=["skill_name", "job_count", "requirement_rate"]
)

top_skills = top_skills[
    top_skills["skill_name"].ne("")
    & (top_skills["job_count"] >= 0)
].copy()

skill_rate = skill_rate[
    skill_rate["skill_name"].ne("")
    & (skill_rate["job_count"] >= 0)
].copy()

if top_skills.empty or skill_rate.empty:
    st.warning("Không có dữ liệu hợp lệ để thực hiện phân tích.")
    st.stop()

top_skills = top_skills.sort_values(
    "job_count",
    ascending=False
).reset_index(drop=True)

skill_rate = skill_rate.sort_values(
    "requirement_rate",
    ascending=False
).reset_index(drop=True)


# Prepare skill-role matrix
role_matrix = skill_by_role.copy()

role_columns = [
    column
    for column in role_matrix.columns
    if column != "skill_name"
]

for column in role_columns:
    role_matrix[column] = pd.to_numeric(
        role_matrix[column],
        errors="coerce"
    ).fillna(0)

role_matrix = role_matrix.dropna(
    subset=["skill_name"]
)

# Limit charts to top 15 skills
top_15 = top_skills.head(15).copy()
rate_top_15 = skill_rate.head(15).copy()


# =========================================================
# 8. KPI OVERVIEW
# =========================================================

total_skills = top_skills["skill_name"].nunique()

top_skill = top_skills.iloc[0]
top_skill_name = str(top_skill["skill_name"]).upper()
top_skill_count = int(top_skill["job_count"])
top_skill_rate = float(top_skill["percentage"])

st.subheader("Tổng quan kỹ năng")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "Tổng số kỹ năng",
        f"{total_skills:,}"
    )

with k2:
    st.metric(
        "Kỹ năng nổi bật nhất",
        top_skill_name
    )

with k3:
    st.metric(
        "Số tin tuyển dụng",
        f"{top_skill_count:,}"
    )

with k4:
    st.metric(
        "Tỷ lệ yêu cầu",
        f"{top_skill_rate:.2f}%"
    )

st.divider()


# =========================================================
# 9. TOP 15 SKILLS
# =========================================================

st.subheader("Top 15 kỹ năng được yêu cầu nhiều nhất")

st.caption(
    "Thống kê số lượng tin tuyển dụng có yêu cầu từng kỹ năng."
)

fig_top = px.bar(
    top_15.sort_values("job_count", ascending=True),
    x="job_count",
    y="skill_name",
    orientation="h",
    text="job_count",
    color="job_count",
    color_continuous_scale="Blues",
    labels={
        "job_count": "Số tin tuyển dụng",
        "skill_name": "Kỹ năng"
    }
)

fig_top.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside",
    textfont=dict(
        family="Arial",
        size=12,
        color="#102A43"
    ),
    cliponaxis=False
)

fig_top.update_layout(
    height=570,
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
        title="Số tin tuyển dụng",
        tickfont=dict(size=12, color="#172B4D")
    ),
    yaxis=dict(
        title="",
        automargin=True,
        tickfont=dict(size=13, color="#172B4D")
    ),
    coloraxis_showscale=False,
    margin=dict(l=20, r=70, t=25, b=45)
)

st.plotly_chart(
    fig_top,
    use_container_width=True,
    config={"displayModeBar": False}
)


# =========================================================
# 10. SKILL REQUIREMENT RATE
# =========================================================

st.divider()

st.subheader("Tỷ lệ yêu cầu kỹ năng")

st.caption(
    "Tỷ lệ phần trăm tin tuyển dụng có yêu cầu kỹ năng "
    "trên tổng số tin tuyển dụng trong bộ dữ liệu."
)

fig_rate = px.bar(
    rate_top_15.sort_values(
        "requirement_rate",
        ascending=True
    ),
    x="requirement_rate",
    y="skill_name",
    orientation="h",
    text="requirement_rate",
    color="requirement_rate",
    color_continuous_scale="Teal",
    labels={
        "requirement_rate": "Tỷ lệ yêu cầu (%)",
        "skill_name": "Kỹ năng"
    }
)

fig_rate.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside",
    textfont=dict(
        family="Arial",
        size=12,
        color="#102A43"
    ),
    cliponaxis=False
)

fig_rate.update_layout(
    height=570,
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
        title="Tỷ lệ yêu cầu (%)",
        tickfont=dict(size=12, color="#172B4D")
    ),
    yaxis=dict(
        title="",
        automargin=True,
        tickfont=dict(size=13, color="#172B4D")
    ),
    coloraxis_showscale=False,
    margin=dict(l=20, r=85, t=25, b=45)
)

st.plotly_chart(
    fig_rate,
    use_container_width=True,
    config={"displayModeBar": False}
)


# =========================================================
# 11. SKILL BY JOB ROLE - HEATMAP
# =========================================================

st.divider()

st.subheader("Mối quan hệ giữa kỹ năng và vị trí công việc")

st.caption(
    "Heatmap thể hiện số lượng tin tuyển dụng yêu cầu "
    "từng kỹ năng trong từng nhóm vị trí IT. "
    "Biểu đồ tập trung vào 20 kỹ năng có tổng lượt xuất hiện cao nhất."
)

if role_columns and not role_matrix.empty:

    heatmap_data = role_matrix.set_index("skill_name")

    heatmap_data["_total"] = heatmap_data.sum(axis=1)

    heatmap_data = (
        heatmap_data
        .sort_values("_total", ascending=False)
        .head(20)
        .drop(columns="_total")
    )

    fig_heatmap = px.imshow(
        heatmap_data,
        labels={
            "x": "Nhóm vị trí công việc",
            "y": "Kỹ năng",
            "color": "Số tin tuyển dụng"
        },
        color_continuous_scale="Blues",
        aspect="auto",
        text_auto=True
    )

    fig_heatmap.update_traces(
        textfont=dict(
            family="Arial",
            size=11,
            color="#102A43"
        ),
        hovertemplate=(
            "Kỹ năng: %{y}<br>"
            "Vị trí: %{x}<br>"
            "Số tin tuyển dụng: %{z:,.0f}"
            "<extra></extra>"
        )
    )

    fig_heatmap.update_layout(
        height=650,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(
            family="Arial",
            size=12,
            color="#172B4D"
        ),
        xaxis=dict(
            title="Nhóm vị trí công việc",
            side="bottom",
            tickangle=-35,
            tickfont=dict(size=11, color="#172B4D")
        ),
        yaxis=dict(
            title="Kỹ năng",
            tickfont=dict(size=12, color="#172B4D")
        ),
        coloraxis_colorbar=dict(
            title="Số tin tuyển dụng",
            tickfont=dict(size=11, color="#172B4D")
        ),
        margin=dict(l=30, r=30, t=25, b=140)
    )

    st.plotly_chart(
        fig_heatmap,
        use_container_width=True,
        config={"displayModeBar": False}
    )

else:
    st.info(
        "Không có đủ dữ liệu nhóm vị trí để xây dựng Heatmap."
    )


# =========================================================
# 12. SKILL DATA TABLE
# =========================================================

st.divider()

st.subheader("Bảng xếp hạng kỹ năng")

st.caption(
    "Danh sách kỹ năng được sắp xếp theo số lượng tin tuyển dụng "
    "có yêu cầu, từ cao xuống thấp."
)

display_skills = top_skills[
    ["skill_name", "job_count", "percentage"]
].copy()

display_skills.columns = [
    "Kỹ năng",
    "Số tin tuyển dụng",
    "Tỷ lệ (%)"
]

display_skills["Tỷ lệ (%)"] = (
    display_skills["Tỷ lệ (%)"].round(2)
)

st.dataframe(
    display_skills,
    use_container_width=True,
    hide_index=True,
    height=420,
    column_config={
        "Kỹ năng": st.column_config.TextColumn(
            "Kỹ năng",
            width="medium"
        ),
        "Số tin tuyển dụng": st.column_config.NumberColumn(
            "Số tin tuyển dụng",
            format="%d"
        ),
        "Tỷ lệ (%)": st.column_config.NumberColumn(
            "Tỷ lệ (%)",
            format="%.2f%%"
        )
    }
)


# =========================================================
# 13. FOOTER
# =========================================================

st.divider()

st.caption(
    "Nguồn dữ liệu: Data Warehouse – IT Recruitment Analysis | "
    "Vietnam IT Recruitment Analytics"
)
