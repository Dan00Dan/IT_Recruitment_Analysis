
"""
Module Load - Nạp dữ liệu vào Data Warehouse.

Xây dựng Star Schema gồm các bảng Dimension và Fact,
sau đó nạp vào SQLite và xuất CSV phục vụ Power BI.

Quy ước:
- ID = 0 đại diện cho dữ liệu không xác định (Unknown).
- Không tự tạo ngày đăng cho bản ghi thiếu ngày.
- Giữ lại toàn bộ bản ghi tuyển dụng trong FACT_JOB_POSTINGS.
- Không ghi đè file it_jobs_cleaned.csv gốc.
"""

import os
import re
import sqlite3
import pandas as pd


# =========================================================
# 1. XỬ LÝ DỮ LIỆU ĐẦU VÀO
# =========================================================

def _impute_missing_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Không tự tạo ngày đăng cho bản ghi thiếu dữ liệu.
    Chuyển ngày không hợp lệ thành NaT.
    """
    df = df.copy()
    df["post_date"] = pd.to_datetime(
        df["post_date"], errors="coerce"
    )
    return df


# =========================================================
# 2. XÂY DỰNG CÁC BẢNG DIMENSION
# =========================================================

def _build_dim_date(df: pd.DataFrame) -> pd.DataFrame:
    """Tạo DIM_DATE; date_id = 0 đại diện ngày không xác định."""

    dates_known = pd.to_datetime(
        df["post_date"], errors="coerce"
    ).dropna()

    columns = [
        "date_id", "full_date", "year", "month",
        "week", "day_of_week", "month_year", "quarter"
    ]

    unknown = pd.DataFrame([{
        "date_id": 0,
        "full_date": "Unknown",
        "year": 0,
        "month": 0,
        "week": 0,
        "day_of_week": "Unknown",
        "month_year": "Unknown",
        "quarter": 0,
    }], columns=columns)

    if dates_known.empty:
        return unknown

    date_range = pd.date_range(
        start=dates_known.min().normalize(),
        end=dates_known.max().normalize(),
        freq="D"
    )

    dim_date = pd.DataFrame({
        "date_id": range(1, len(date_range) + 1),
        "full_date": date_range.strftime("%Y-%m-%d"),
        "year": date_range.year,
        "month": date_range.month,
        "week": date_range.isocalendar().week.values,
        "day_of_week": date_range.day_name(),
        "month_year": date_range.strftime("%m/%Y"),
        "quarter": date_range.quarter,
    })

    return pd.concat([unknown, dim_date], ignore_index=True)


def _build_dim_city(df: pd.DataFrame) -> pd.DataFrame:
    """Tạo DIM_CITY; city_id = 0 đại diện thành phố không xác định."""

    cities = sorted(
        df["city"].dropna().astype(str).str.strip().unique()
    )
    cities = [city for city in cities if city]

    dim = pd.DataFrame({
        "city_id": range(1, len(cities) + 1),
        "city_name": cities,
    })

    unknown = pd.DataFrame([{
        "city_id": 0,
        "city_name": "Unknown"
    }])

    return pd.concat([unknown, dim], ignore_index=True)


def _build_dim_role(df: pd.DataFrame) -> pd.DataFrame:
    """Tạo DIM_ROLE; role_id = 0 đại diện vai trò không xác định."""

    roles = sorted(
        df["role_category"].dropna().astype(str).str.strip().unique()
    )
    roles = [role for role in roles if role]

    dim = pd.DataFrame({
        "role_id": range(1, len(roles) + 1),
        "role_name": roles,
    })

    unknown = pd.DataFrame([{
        "role_id": 0,
        "role_name": "Unknown"
    }])

    return pd.concat([unknown, dim], ignore_index=True)


def _build_dim_level(df: pd.DataFrame) -> pd.DataFrame:
    """Tạo DIM_LEVEL; level_id = 0 đại diện cấp bậc không xác định."""

    levels = sorted(
        df["job_level"].dropna().astype(str).str.strip().unique()
    )
    levels = [level for level in levels if level]

    dim = pd.DataFrame({
        "level_id": range(1, len(levels) + 1),
        "level_name": levels,
    })

    unknown = pd.DataFrame([{
        "level_id": 0,
        "level_name": "Unknown"
    }])

    return pd.concat([unknown, dim], ignore_index=True)


def _build_dim_company(df: pd.DataFrame) -> pd.DataFrame:
    """Tạo DIM_COMPANY; company_id = 0 đại diện công ty không xác định."""

    companies = sorted(
        df["company"].dropna().astype(str).str.strip().unique()
    )
    companies = [company for company in companies if company]

    dim = pd.DataFrame({
        "company_id": range(1, len(companies) + 1),
        "company_name": companies,
    })

    unknown = pd.DataFrame([{
        "company_id": 0,
        "company_name": "Unknown"
    }])

    return pd.concat([unknown, dim], ignore_index=True)


def _clean_skill_name(raw: str) -> str:
    """Làm sạch tên kỹ năng."""

    skill = str(raw).strip()
    skill = re.sub(r"[\[\]\'\"]+", "", skill).strip()

    return skill


def _build_dim_skill(df: pd.DataFrame) -> pd.DataFrame:
    """Tạo DIM_SKILL bằng cách tách các kỹ năng riêng lẻ."""

    all_skills = set()

    for skills_str in df["skills_list"].dropna():
        for skill in str(skills_str).split(","):
            skill = _clean_skill_name(skill)

            if skill and skill != "[]":
                all_skills.add(skill)

    skills_sorted = sorted(all_skills)

    return pd.DataFrame({
        "skill_id": range(1, len(skills_sorted) + 1),
        "skill_name": skills_sorted,
    })


# =========================================================
# 3. XÂY DỰNG FACT_JOB_POSTINGS
# =========================================================

def _build_fact_job_postings(
    df: pd.DataFrame,
    dim_date: pd.DataFrame,
    dim_city: pd.DataFrame,
    dim_role: pd.DataFrame,
    dim_level: pd.DataFrame,
    dim_company: pd.DataFrame,
) -> pd.DataFrame:
    """
    Xây dựng FACT_JOB_POSTINGS.

    Các khóa ngoại không xác định được ánh xạ về ID = 0.
    Không loại bỏ bản ghi thiếu ngày, thành phố hoặc công ty.
    """

    date_lookup = dict(zip(
        dim_date["full_date"], dim_date["date_id"]
    ))

    city_lookup = dict(zip(
        dim_city["city_name"], dim_city["city_id"]
    ))

    role_lookup = dict(zip(
        dim_role["role_name"], dim_role["role_id"]
    ))

    level_lookup = dict(zip(
        dim_level["level_name"], dim_level["level_id"]
    ))

    company_lookup = dict(zip(
        dim_company["company_name"], dim_company["company_id"]
    ))

    post_dates = pd.to_datetime(
        df["post_date"], errors="coerce"
    )

    date_keys = (
        post_dates.dt.strftime("%Y-%m-%d")
        .map(date_lookup)
        .fillna(0)
        .astype(int)
    )

    city_values = df["city"].apply(
        lambda x: str(x).strip() if pd.notna(x) and str(x).strip() else None
    )

    company_values = df["company"].apply(
        lambda x: str(x).strip() if pd.notna(x) and str(x).strip() else None
    )

    role_values = df["role_category"].apply(
        lambda x: str(x).strip() if pd.notna(x) and str(x).strip() else None
    )

    level_values = df["job_level"].apply(
        lambda x: str(x).strip() if pd.notna(x) and str(x).strip() else None
    )

    fact = pd.DataFrame({
        "job_id": df["job_id"].astype(str).str.strip(),
        "date_id": date_keys,
        "city_id": city_values.map(city_lookup).fillna(0).astype(int),
        "role_id": role_values.map(role_lookup).fillna(0).astype(int),
        "level_id": level_values.map(level_lookup).fillna(0).astype(int),
        "company_id": company_values.map(company_lookup).fillna(0).astype(int),
        "salary_min": df["salary_min"],
        "salary_max": df["salary_max"],
        "salary_avg": df["salary_avg"],
        "exp_years_min": df["exp_years_min"],
        "is_negotiable": df["is_negotiable"],
        "source": df["source"],
    })

    return fact


# =========================================================
# 4. XÂY DỰNG FACT_JOB_SKILLS
# =========================================================

def _build_fact_job_skills(
    df: pd.DataFrame,
    dim_skill: pd.DataFrame,
    dim_date: pd.DataFrame,
    dim_city: pd.DataFrame,
    dim_role: pd.DataFrame,
) -> pd.DataFrame:
    """
    Xây dựng FACT_JOB_SKILLS.

    Mỗi dòng biểu diễn một kỹ năng thuộc một tin tuyển dụng.
    Các khóa ngày, thành phố, vai trò không xác định dùng ID = 0.
    """

    skill_lookup = dict(zip(
        dim_skill["skill_name"], dim_skill["skill_id"]
    ))

    date_lookup = dict(zip(
        dim_date["full_date"], dim_date["date_id"]
    ))

    city_lookup = dict(zip(
        dim_city["city_name"], dim_city["city_id"]
    ))

    role_lookup = dict(zip(
        dim_role["role_name"], dim_role["role_id"]
    ))

    rows = []

    for _, row in df.iterrows():

        if pd.isna(row["skills_list"]):
            continue

        skills_text = str(row["skills_list"]).strip()

        if not skills_text:
            continue

        skills = [
            _clean_skill_name(skill)
            for skill in skills_text.split(",")
        ]

        skills = list(dict.fromkeys(
            skill for skill in skills if skill and skill != "[]"
        ))

        post_date = pd.to_datetime(
            row["post_date"], errors="coerce"
        )

        date_key = (
            date_lookup.get(post_date.strftime("%Y-%m-%d"), 0)
            if pd.notna(post_date) else 0
        )

        city = (
            str(row["city"]).strip()
            if pd.notna(row["city"]) and str(row["city"]).strip()
            else None
        )

        role = (
            str(row["role_category"]).strip()
            if pd.notna(row["role_category"]) and str(row["role_category"]).strip()
            else None
        )

        city_key = city_lookup.get(city, 0)
        role_key = role_lookup.get(role, 0)

        for skill_name in skills:

            skill_id = skill_lookup.get(skill_name)

            if skill_id is None:
                continue

            rows.append({
                "job_id": str(row["job_id"]).strip(),
                "skill_id": int(skill_id),
                "date_id": int(date_key),
                "city_id": int(city_key),
                "role_id": int(role_key),
                "salary_avg": row["salary_avg"],
            })

    columns = [
        "job_id", "skill_id", "date_id",
        "city_id", "role_id", "salary_avg"
    ]

    return pd.DataFrame(rows, columns=columns)


# =========================================================
# 5. NẠP DỮ LIỆU VÀO DATA WAREHOUSE
# =========================================================

def load_to_warehouse(
    df_clean: pd.DataFrame,
    warehouse_dir: str
) -> dict[str, pd.DataFrame]:
    """
    Xây dựng Star Schema và nạp vào Data Warehouse.

    Đích dữ liệu:
    1. SQLite: it_recruitment_dwh.db
    2. CSV: các bảng Dimension và Fact.

    Không ghi đè it_jobs_cleaned.csv gốc.
    """

    os.makedirs(warehouse_dir, exist_ok=True)

    # Chuẩn hóa ngày nhưng không tạo ngày giả.
    df_clean = _impute_missing_dates(df_clean)

    print("  -> Xây dựng bảng DIM_DATE...")
    dim_date = _build_dim_date(df_clean)

    print("  -> Xây dựng bảng DIM_CITY...")
    dim_city = _build_dim_city(df_clean)

    print("  -> Xây dựng bảng DIM_ROLE...")
    dim_role = _build_dim_role(df_clean)

    print("  -> Xây dựng bảng DIM_LEVEL...")
    dim_level = _build_dim_level(df_clean)

    print("  -> Xây dựng bảng DIM_COMPANY...")
    dim_company = _build_dim_company(df_clean)

    print("  -> Xây dựng bảng DIM_SKILL...")
    dim_skill = _build_dim_skill(df_clean)

    print("  -> Xây dựng bảng FACT_JOB_POSTINGS...")
    fact_jobs = _build_fact_job_postings(
        df_clean,
        dim_date,
        dim_city,
        dim_role,
        dim_level,
        dim_company
    )

    print("  -> Xây dựng bảng FACT_JOB_SKILLS...")
    fact_skills = _build_fact_job_skills(
        df_clean,
        dim_skill,
        dim_date,
        dim_city,
        dim_role
    )

    tables = {
        "dim_date": dim_date,
        "dim_city": dim_city,
        "dim_role": dim_role,
        "dim_level": dim_level,
        "dim_company": dim_company,
        "dim_skill": dim_skill,
        "fact_job_postings": fact_jobs,
        "fact_job_skills": fact_skills,
    }

    # Kiểm tra số lượng bản ghi trước khi ghi dữ liệu.
    if len(fact_jobs) != len(df_clean):
        raise ValueError(
            f"FACT_JOB_POSTINGS có {len(fact_jobs)} dòng, "
            f"nhưng dữ liệu đầu vào có {len(df_clean)} dòng."
        )

    if fact_jobs["job_id"].nunique() != len(fact_jobs):
        raise ValueError(
            "Phát hiện job_id trùng trong FACT_JOB_POSTINGS."
        )

    # Nạp vào SQLite.
    db_path = os.path.join(
        warehouse_dir, "it_recruitment_dwh.db"
    )

    print(f"  -> Nạp vào SQLite: {db_path}")

    conn = sqlite3.connect(db_path)

    try:
        for table_name, table_df in tables.items():
            table_df.to_sql(
                table_name,
                conn,
                if_exists="replace",
                index=False
            )

        conn.commit()

    finally:
        conn.close()

    # Xuất CSV cho Power BI.
    print("  -> Xuất CSV cho Power BI...")

    for table_name, table_df in tables.items():

        csv_path = os.path.join(
            warehouse_dir, f"{table_name}.csv"
        )

        table_df.to_csv(
            csv_path,
            index=False,
            encoding="utf-8-sig"
        )

    # In thống kê.
    print("\n===== THỐNG KÊ DATA WAREHOUSE =====")

    for table_name, table_df in tables.items():
        print(
            f"{table_name:25s}: {len(table_df):>7,} dòng"
        )

    print("\n===== KIỂM TRA DỮ LIỆU =====")
    print(f"Số bản ghi đầu vào: {len(df_clean):,}")
    print(f"Số tin trong Fact:  {len(fact_jobs):,}")
    print(
        "Tin thiếu ngày đăng:",
        int((fact_jobs["date_id"] == 0).sum())
    )
    print(
        "Tin thiếu thành phố:",
        int((fact_jobs["city_id"] == 0).sum())
    )
    print(
        "Tin thiếu công ty:",
        int((fact_jobs["company_id"] == 0).sum())
    )

    return tables
