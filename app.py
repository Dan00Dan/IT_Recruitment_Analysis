
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# 1. PROJECT CONFIGURATION
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent
TABLES_DIR = PROJECT_ROOT / "results" / "tables"

st.set_page_config(
    page_title="Vietnam IT Recruitment Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. PROFESSIONAL BLUE & WHITE THEME
# =========================================================

st.markdown(
    """
    <style>
    /* ===== GLOBAL ===== */

    .stApp,
    [data-testid="stAppViewContainer"] {
        background-color: #F3F6FA;
        color: #243B53;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }

    /* ===== MAIN TEXT ===== */

    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: #334E68;
    }

    [data-testid="stMarkdownContainer"] strong {
        color: #102A43;
    }

    h1, h2, h3, h4 {
        color: #102A43 !important;
        font-weight: 700 !important;
    }

    /* ===== MAIN TITLES ===== */

    .main-title {
        font-size: 32px;
        font-weight: 800;
        color: #102A43;
        margin-bottom: 5px;
        letter-spacing: -0.5px;
    }

    .sub-title {
        color: #627D98;
        font-size: 14px;
        margin-bottom: 25px;
    }

    .section-title {
        color: #102A43;
        font-size: 21px;
        font-weight: 750;
        margin-top: 15px;
        margin-bottom: 14px;
    }

    /* ===== SIDEBAR ===== */

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #102A43 0%,
            #153B5B 100%
        );
        border-right: 1px solid #294D6B;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
    }

    /* Hide Streamlit's default navigation */
    [data-testid="stSidebarNav"] {
        display: none;
    }

    /* Sidebar text */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span {
        color: #D9E6F2;
    }

    /* Project logo */
    .project-logo {
        width: 58px;
        height: 58px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(
            135deg,
            #FFFFFF 0%,
            #DCEBFA 100%
        );
        border-radius: 15px;
        color: #153B5B;
        font-size: 27px;
        font-weight: 900;
        letter-spacing: -2px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
        margin-bottom: 15px;
    }

    .sidebar-brand-title {
        color: #FFFFFF;
        font-size: 19px;
        font-weight: 800;
        letter-spacing: 0.4px;
        line-height: 1.4;
    }

    .sidebar-brand-subtitle {
        color: #AFC5D9;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-top: 5px;
    }

    .sidebar-label {
        color: #AFC5D9;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.6px;
        margin: 8px 0 10px 2px;
    }

    /* Sidebar page links */
    [data-testid="stSidebar"] [data-testid="stPageLink"] a {
        border-radius: 9px;
        padding: 9px 11px;
        color: #D9E6F2 !important;
        transition: background-color 0.2s ease;
    }

    [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {
        background-color: rgba(255, 255, 255, 0.12);
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"] {
        background-color: #FFFFFF;
        color: #153B5B !important;
        font-weight: 700;
    }

    [data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"] * {
        color: #153B5B !important;
    }

    /* Sidebar divider */
    [data-testid="stSidebar"] hr {
        border-color: #355875;
        margin: 18px 0;
    }

    .sidebar-footer {
        background-color: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 10px;
        padding: 13px;
        margin-top: 25px;
    }

    .sidebar-footer-title {
        color: #FFFFFF;
        font-size: 12px;
        font-weight: 750;
        margin-bottom: 5px;
    }

    .sidebar-footer-text {
        color: #B8CCDE;
        font-size: 11px;
        line-height: 1.6;
    }

    /* ===== KPI CARDS ===== */

    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #D9E2EC;
        border-radius: 13px;
        padding: 18px 20px;
        box-shadow: 0 3px 10px rgba(16, 42, 67, 0.05);
        min-height: 115px;
    }

    [data-testid="stMetricLabel"] {
        color: #526D82 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        color: #126E82 !important;
        font-size: 29px !important;
        font-weight: 800 !important;
    }

    [data-testid="stMetricDelta"] {
        color: #237A57 !important;
    }

    /* ===== CHARTS ===== */

    [data-testid="stPlotlyChart"] {
        background-color: #FFFFFF;
        border: 1px solid #E1E8F0;
        border-radius: 12px;
        padding: 10px;
    }

    /* ===== TABLES ===== */

    [data-testid="stDataFrame"] {
        background-color: #FFFFFF;
        border-radius: 10px;
    }

    /* ===== INPUTS ===== */

    .stSelectbox label,
    .stMultiSelect label,
    .stDateInput label,
    .stTextInput label {
        color: #243B53 !important;
        font-weight: 600;
    }

    [data-baseweb="select"] > div {
        background-color: #FFFFFF;
        border-color: #CBD5E1;
    }

    /* ===== ALERTS ===== */

    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* ===== DIVIDERS ===== */

    hr {
        border-color: #D9E2EC;
    }

    /* ===== FOOTER ===== */

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 3. SIDEBAR BRANDING & NAVIGATION
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="project-logo">IT.</div>

        <div class="sidebar-brand-title">
            IT RECRUITMENT<br>ANALYTICS
        </div>

        <div class="sidebar-brand-subtitle">
            DATA ANALYTICS PLATFORM
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-label">NAVIGATION</div>',
        unsafe_allow_html=True
    )

    st.page_link(
        "app.py",
        label="Overview",
        icon="🏠"
    )

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

    st.divider()

    st.markdown(
        """
        <div class="sidebar-footer">
            <div class="sidebar-footer-title">
                CHUYÊN ĐỀ 2
            </div>
            <div class="sidebar-footer-text">
                Vietnam IT Recruitment<br>
                Data Analysis Project
                <br><br>
                Van Lang University
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 4. DATA LOADING
# =========================================================

@st.cache_data
def load_csv(filename):
    file_path = TABLES_DIR / filename

    if not file_path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(file_path, encoding="utf-8-sig")
    except UnicodeDecodeError:
        return pd.read_csv(file_path, encoding="utf-8")


kpi_df = load_csv("eda_kpi_summary.csv")
city_df = load_csv("jobs_by_city.csv")
role_df = load_csv("jobs_by_role.csv")
skill_df = load_csv("top_skills.csv")
trend_df = load_csv("monthly_recruitment_trend.csv")
salary_df = load_csv("salary_disclosure.csv")


# =========================================================
# 5. HELPER FUNCTIONS
# =========================================================

def get_kpi(metric_name, default=0):
    if kpi_df.empty:
        return default

    if not {"Metric", "Value"}.issubset(kpi_df.columns):
        return default

    matched = kpi_df[
        kpi_df["Metric"].astype(str).str.strip().str.lower()
        == metric_name.strip().lower()
    ]

    if matched.empty:
        return default

    return matched.iloc[0]["Value"]


def format_number(value):
    try:
        return f"{float(value):,.0f}"
    except (ValueError, TypeError):
        return "N/A"


def format_percentage(value):
    try:
        return f"{float(value):.1f}%"
    except (ValueError, TypeError):
        return "N/A"


# =========================================================
# 6. PLOTLY THEME
# =========================================================

def style_chart(fig, height=390):
    fig.update_layout(
        height=height,
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Arial",
            size=12,
            color="#243B53"
        ),
        title_font=dict(
            color="#102A43",
            size=17
        ),
        xaxis=dict(
            title_font=dict(color="#334E68"),
            tickfont=dict(color="#486581"),
            gridcolor="#E8EEF4",
            zerolinecolor="#D9E2EC"
        ),
        yaxis=dict(
            title_font=dict(color="#334E68"),
            tickfont=dict(color="#486581"),
            gridcolor="#E8EEF4",
            zerolinecolor="#D9E2EC"
        ),
        margin=dict(
            l=10,
            r=20,
            t=25,
            b=15
        )
    )

    return fig


# =========================================================
# 7. HEADER
# =========================================================

st.markdown(
    '<div class="main-title">'
    'Vietnam IT Recruitment Analytics'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Data-driven insights into Vietnam IT recruitment market'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# 8. KPI OVERVIEW
# =========================================================

total_jobs = get_kpi("Total Job Postings")
companies = get_kpi("Companies")
cities = get_kpi("Cities")

total_jobs_value = format_number(total_jobs)
companies_value = format_number(companies)
cities_value = format_number(cities)

if not salary_df.empty and {
    "Salary Status", "Percentage"
}.issubset(salary_df.columns):

    salary_available = salary_df.loc[
        salary_df["Salary Status"].astype(str).str.strip()
        == "Salary Available",
        "Percentage"
    ]

    salary_rate = (
        salary_available.iloc[0]
        if not salary_available.empty else 0
    )

else:
    salary_rate = 0


st.markdown(
    '<div class="section-title">Market Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Job Postings", total_jobs_value)
col2.metric("Companies", companies_value)
col3.metric("Recruitment Cities", cities_value)
col4.metric("Salary Disclosure", format_percentage(salary_rate))

st.markdown("")
st.divider()


# =========================================================
# 9. RECRUITMENT DISTRIBUTION
# =========================================================

st.markdown(
    '<div class="section-title">Recruitment Distribution</div>',
    unsafe_allow_html=True
)

left_col, right_col = st.columns(2)


# -------------------------
# 9.1 RECRUITMENT BY CITY
# -------------------------

with left_col:

    st.markdown("#### Recruitment by City")

    if not city_df.empty and {
        "city", "job_count"
    }.issubset(city_df.columns):

        city_plot = city_df.copy()

        city_plot["job_count"] = pd.to_numeric(
            city_plot["job_count"],
            errors="coerce"
        ).fillna(0)

        city_plot = city_plot.sort_values(
            "job_count",
            ascending=True
        )

        fig_city = px.bar(
            city_plot,
            x="job_count",
            y="city",
            orientation="h",
            text="job_count",
            color="job_count",
            color_continuous_scale=["#B8E0E5", "#126E82"],
            labels={
                "job_count": "Number of Jobs",
                "city": "City"
            }
        )

        fig_city.update_traces(
            texttemplate="%{text:,.0f}",
            textposition="outside",
            cliponaxis=False,
            textfont=dict(color="#243B53", size=11)
        )

        fig_city.update_layout(
            coloraxis_showscale=False,
            xaxis_title="Number of Job Postings",
            yaxis_title=""
        )

        fig_city = style_chart(fig_city, 390)

        st.plotly_chart(
            fig_city,
            use_container_width=True
        )

    else:
        st.warning("City data is unavailable.")


# -------------------------
# 9.2 RECRUITMENT BY ROLE
# -------------------------

with right_col:

    st.markdown("#### Recruitment by Job Role")

    if not role_df.empty and {
        "role", "job_count"
    }.issubset(role_df.columns):

        role_plot = role_df.copy()

        role_plot["job_count"] = pd.to_numeric(
            role_plot["job_count"],
            errors="coerce"
        ).fillna(0)

        role_plot = (
            role_plot
            .sort_values("job_count", ascending=True)
            .tail(10)
        )

        fig_role = px.bar(
            role_plot,
            x="job_count",
            y="role",
            orientation="h",
            text="job_count",
            color="job_count",
            color_continuous_scale=["#B8E0E5", "#126E82"],
            labels={
                "job_count": "Number of Jobs",
                "role": "Job Role"
            }
        )

        fig_role.update_traces(
            texttemplate="%{text:,.0f}",
            textposition="outside",
            cliponaxis=False,
            textfont=dict(color="#243B53", size=11)
        )

        fig_role.update_layout(
            coloraxis_showscale=False,
            xaxis_title="Number of Job Postings",
            yaxis_title=""
        )

        fig_role = style_chart(fig_role, 390)

        st.plotly_chart(
            fig_role,
            use_container_width=True
        )

    else:
        st.warning("Job role data is unavailable.")


st.divider()


# =========================================================
# 10. TOP IT SKILLS
# =========================================================

st.markdown(
    '<div class="section-title">Top IT Skills in Demand</div>',
    unsafe_allow_html=True
)

if not skill_df.empty and {
    "skill_name", "job_count"
}.issubset(skill_df.columns):

    skill_plot = skill_df.copy()

    skill_plot["job_count"] = pd.to_numeric(
        skill_plot["job_count"],
        errors="coerce"
    ).fillna(0)

    skill_plot = (
        skill_plot
        .sort_values("job_count", ascending=False)
        .head(10)
        .sort_values("job_count", ascending=True)
    )

    fig_skill = px.bar(
        skill_plot,
        x="job_count",
        y="skill_name",
        orientation="h",
        text="job_count",
        color="job_count",
        color_continuous_scale=["#B8E0E5", "#126E82"],
        labels={
            "job_count": "Number of Job Postings",
            "skill_name": "Skill"
        }
    )

    fig_skill.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        cliponaxis=False,
        textfont=dict(color="#243B53", size=11)
    )

    fig_skill.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Number of Job Postings",
        yaxis_title=""
    )

    fig_skill = style_chart(fig_skill, 430)

    st.plotly_chart(
        fig_skill,
        use_container_width=True
    )

else:
    st.warning("Skill data is unavailable.")


st.divider()


# =========================================================
# 11. RECRUITMENT TREND
# =========================================================

st.markdown(
    '<div class="section-title">Recruitment Trend</div>',
    unsafe_allow_html=True
)

if not trend_df.empty and {
    "month", "job_count"
}.issubset(trend_df.columns):

    trend_plot = trend_df.copy()

    trend_plot["month"] = pd.to_datetime(
        trend_plot["month"],
        errors="coerce"
    )

    trend_plot["job_count"] = pd.to_numeric(
        trend_plot["job_count"],
        errors="coerce"
    )

    trend_plot = (
        trend_plot
        .dropna(subset=["month", "job_count"])
        .sort_values("month")
    )

    if not trend_plot.empty:

        fig_trend = px.line(
            trend_plot,
            x="month",
            y="job_count",
            markers=True,
            labels={
                "month": "Month",
                "job_count": "Number of Jobs"
            }
        )

        fig_trend.update_traces(
            line=dict(color="#126E82", width=3),
            marker=dict(
                size=8,
                color="#126E82",
                line=dict(color="#FFFFFF", width=2)
            )
        )

        fig_trend = style_chart(fig_trend, 370)

        fig_trend.update_layout(
            xaxis_title="Month",
            yaxis_title="Number of Job Postings",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig_trend,
            use_container_width=True
        )

    else:
        st.warning("No valid recruitment trend records were found.")

else:
    st.warning("Recruitment trend data is unavailable.")


# =========================================================
# 12. FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:#526D82;
        padding:18px;
        font-size:13px;
    ">
        <b style="color:#102A43;">
            Vietnam IT Recruitment Analytics
        </b>
        <br>
        CHUYÊN ĐỀ 2 · Data Analytics Project
        <br>
        Van Lang University
    </div>
    """,
    unsafe_allow_html=True
)
