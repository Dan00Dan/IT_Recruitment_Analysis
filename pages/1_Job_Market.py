
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# 1. CONFIGURATION
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TABLES_DIR = PROJECT_ROOT / "results" / "tables"

st.set_page_config(
    page_title="Job Market | Vietnam IT Recruitment",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. THEME - BLUE & WHITE ANALYTICS
# =========================================================

st.markdown(
    """
    <style>
    /* GLOBAL */

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

    h1, h2, h3, h4 {
        color: #102A43 !important;
        font-weight: 750 !important;
    }

    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: #334E68;
    }

    /* SIDEBAR */

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

    [data-testid="stSidebarNav"] {
        display: none;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span {
        color: #D9E6F2;
    }

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

    /* KPI */

    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #D9E2EC;
        border-radius: 13px;
        padding: 18px 20px;
        box-shadow: 0 3px 10px rgba(16, 42, 67, 0.05);
        min-height: 115px;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] * {
        color: #526D82 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] * {
        color: #126E82 !important;
        font-weight: 800 !important;
    }

    /* CHARTS */

    [data-testid="stPlotlyChart"] {
        background-color: #FFFFFF;
        border: 1px solid #E1E8F0;
        border-radius: 12px;
        padding: 10px;
    }

    /* TABLES */

    [data-testid="stDataFrame"] {
        background-color: #FFFFFF;
        border: 1px solid #E1E8F0;
        border-radius: 10px;
    }

    /* FOOTER */

    footer {
        visibility: hidden;
    }

    hr {
        border-color: #D9E2EC;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 3. SHARED VISUAL SIDEBAR
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

    st.page_link("app.py", label="Overview", icon="🏠")
    st.page_link("pages/1_Job_Market.py", label="Job Market", icon="💼")
    st.page_link("pages/2_Skills_Analysis.py", label="Skills Analysis", icon="🧠")
    st.page_link("pages/3_Salary_Analysis.py", label="Salary Analysis", icon="💰")
    st.page_link("pages/4_Recruitment_Trends.py", label="Recruitment Trends", icon="📈")
    st.page_link("pages/5_Forecasting.py", label="Forecasting", icon="🔮")

    st.divider()

    st.markdown(
        """
        <div class="sidebar-footer">
            <div class="sidebar-footer-title">CHUYÊN ĐỀ 2</div>
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
# 4. LOAD DATA
# =========================================================

@st.cache_data
def load_csv(filename):
    path = TABLES_DIR / filename

    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path, encoding="utf-8-sig")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="utf-8")


city_df = load_csv("jobs_by_city.csv")
role_df = load_csv("jobs_by_role.csv")


# =========================================================
# 5. DATA VALIDATION
# =========================================================

if not city_df.empty:
    if {"city", "job_count"}.issubset(city_df.columns):
        city_df["job_count"] = pd.to_numeric(
            city_df["job_count"],
            errors="coerce"
        ).fillna(0)
    else:
        city_df = pd.DataFrame()

if not role_df.empty:
    if {"role", "job_count"}.issubset(role_df.columns):
        role_df["job_count"] = pd.to_numeric(
            role_df["job_count"],
            errors="coerce"
        ).fillna(0)
    else:
        role_df = pd.DataFrame()


# =========================================================
# 6. CHART STYLE
# =========================================================

def apply_chart_style(fig, height=420):
    fig.update_layout(
        height=height,
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Arial",
            size=13,
            color="#172B4D"
        ),
        title_font=dict(
            family="Arial",
            size=17,
            color="#102A43"
        ),
        legend=dict(
            font=dict(size=12, color="#172B4D"),
            title_font=dict(color="#102A43")
        ),
        xaxis=dict(
            title_font=dict(color="#102A43", size=13),
            tickfont=dict(color="#243B53", size=12),
            gridcolor="#E2E8F0",
            zerolinecolor="#CBD5E1"
        ),
        yaxis=dict(
            title_font=dict(color="#102A43", size=13),
            tickfont=dict(color="#243B53", size=12),
            gridcolor="#E2E8F0",
            zerolinecolor="#CBD5E1"
        ),
        margin=dict(l=15, r=25, t=35, b=15)
    )

    return fig


# =========================================================
# 7. HEADER
# =========================================================

st.title("Job Market Analysis")

st.markdown(
    """
    <p style="
        color:#526D82;
        font-size:15px;
        font-weight:500;
        margin-top:-8px;
    ">
        Explore IT recruitment demand across cities
        and job positions in Vietnam.
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# 8. MARKET KPIs
# =========================================================

total_jobs = (
    city_df["job_count"].sum()
    if not city_df.empty else 0
)

total_cities = (
    city_df["city"].nunique()
    if not city_df.empty else 0
)

total_roles = (
    role_df["role"].nunique()
    if not role_df.empty else 0
)

top_city = (
    city_df.loc[city_df["job_count"].idxmax(), "city"]
    if not city_df.empty and total_jobs > 0
    else "N/A"
)

top_role = (
    role_df.loc[role_df["job_count"].idxmax(), "role"]
    if not role_df.empty and role_df["job_count"].sum() > 0
    else "N/A"
)

st.markdown(
    '<div class="section-title">Market Indicators</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Job Postings", f"{total_jobs:,.0f}")
col2.metric("Recruitment Cities", f"{total_cities:,}")
col3.metric("Job Categories", f"{total_roles:,}")
col4.metric("Leading Recruitment City", str(top_city))

st.divider()


# =========================================================
# 9. RECRUITMENT BY CITY
# =========================================================

st.markdown(
    '<div class="section-title">Recruitment Demand by City</div>',
    unsafe_allow_html=True
)

if not city_df.empty:

    city_plot = city_df.sort_values(
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
        color_continuous_scale=["#B8D8E8", "#126E82"],
        labels={
            "city": "City",
            "job_count": "Job Postings"
        }
    )

    fig_city.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        cliponaxis=False,
        textfont=dict(
            family="Arial",
            color="#102A43",
            size=12
        )
    )

    fig_city.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Number of Job Postings",
        yaxis_title=""
    )

    st.plotly_chart(
        apply_chart_style(fig_city, 480),
        use_container_width=True
    )

else:
    st.warning("City recruitment data is unavailable.")


# =========================================================
# 10. CITY RECRUITMENT SHARE
# =========================================================

if not city_df.empty:

    st.markdown(
        '<div class="section-title">City Recruitment Share</div>',
        unsafe_allow_html=True
    )

    fig_city_share = px.pie(
        city_df,
        names="city",
        values="job_count",
        hole=0.55,
        color_discrete_sequence=px.colors.qualitative.Safe
    )

    fig_city_share.update_traces(
        textposition="inside",
        textinfo="percent",
        insidetextfont=dict(
            color="#FFFFFF",
            size=12,
            family="Arial"
        ),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Job Postings: %{value:,.0f}<br>"
            "Share: %{percent}<extra></extra>"
        )
    )

    fig_city_share.update_layout(
        height=440,
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Arial",
            size=13,
            color="#172B4D"
        ),
        legend=dict(
            font=dict(color="#172B4D", size=12),
            title=dict(
                text="City",
                font=dict(color="#102A43")
            )
        ),
        margin=dict(l=10, r=10, t=20, b=10)
    )

    st.plotly_chart(
        fig_city_share,
        use_container_width=True
    )


st.divider()


# =========================================================
# 11. RECRUITMENT BY JOB ROLE
# =========================================================

st.markdown(
    '<div class="section-title">Recruitment Demand by Job Role</div>',
    unsafe_allow_html=True
)

if not role_df.empty:

    role_plot = role_df.sort_values(
        "job_count",
        ascending=True
    )

    fig_role = px.bar(
        role_plot,
        x="job_count",
        y="role",
        orientation="h",
        text="job_count",
        color="job_count",
        color_continuous_scale=["#B8D8E8", "#126E82"],
        labels={
            "role": "Job Role",
            "job_count": "Job Postings"
        }
    )

    fig_role.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        cliponaxis=False,
        textfont=dict(
            family="Arial",
            color="#102A43",
            size=12
        )
    )

    fig_role.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Number of Job Postings",
        yaxis_title=""
    )

    st.plotly_chart(
        apply_chart_style(fig_role, 520),
        use_container_width=True
    )

else:
    st.warning("Job role data is unavailable.")


# =========================================================
# 12. JOB MARKET RANKING
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">Recruitment Ranking</div>',
    unsafe_allow_html=True
)

rank_col1, rank_col2 = st.columns(2)


# -------------------------
# 12.1 CITY RANKING
# -------------------------

with rank_col1:

    st.markdown("#### Top Recruitment Cities")

    if not city_df.empty:

        city_ranking = (
            city_df
            .sort_values("job_count", ascending=False)
            .reset_index(drop=True)
        )

        city_ranking.index = city_ranking.index + 1

        display_city = city_ranking.copy()

        if "percentage" in display_city.columns:
            display_city["percentage"] = pd.to_numeric(
                display_city["percentage"],
                errors="coerce"
            ).map(
                lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A"
            )

        display_city = display_city.rename(
            columns={
                "city": "City",
                "job_count": "Job Postings",
                "percentage": "Market Share"
            }
        )

        st.dataframe(
            display_city,
            use_container_width=True,
            hide_index=False,
            height=420,
            column_config={
                "City": st.column_config.TextColumn(
                    "City",
                    width="medium"
                ),
                "Job Postings": st.column_config.NumberColumn(
                    "Job Postings",
                    format="%d"
                ),
                "Market Share": st.column_config.TextColumn(
                    "Market Share"
                )
            }
        )

    else:
        st.info("No city ranking data available.")


# -------------------------
# 12.2 ROLE RANKING
# -------------------------

with rank_col2:

    st.markdown("#### Top Job Categories")

    if not role_df.empty:

        role_ranking = (
            role_df
            .sort_values("job_count", ascending=False)
            .reset_index(drop=True)
        )

        role_ranking.index = role_ranking.index + 1

        display_role = role_ranking.copy()

        if "percentage" in display_role.columns:
            display_role["percentage"] = pd.to_numeric(
                display_role["percentage"],
                errors="coerce"
            ).map(
                lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A"
            )

        display_role = display_role.rename(
            columns={
                "role": "Job Role",
                "job_count": "Job Postings",
                "percentage": "Market Share"
            }
        )

        st.dataframe(
            display_role,
            use_container_width=True,
            hide_index=False,
            height=420,
            column_config={
                "Job Role": st.column_config.TextColumn(
                    "Job Role",
                    width="medium"
                ),
                "Job Postings": st.column_config.NumberColumn(
                    "Job Postings",
                    format="%d"
                ),
                "Market Share": st.column_config.TextColumn(
                    "Market Share"
                )
            }
        )

    else:
        st.info("No job role ranking data available.")


# =========================================================
# 13. FOOTER
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
        CHUYÊN ĐỀ 2 · Job Market Analysis
        <br>
        Van Lang University
    </div>
    """,
    unsafe_allow_html=True
)
