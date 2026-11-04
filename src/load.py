"""
Module Load (Nạp dữ liệu vào Data Warehouse)
Xây dựng Star Schema với các bảng Dimension và Fact,
sau đó nạp vào SQLite và xuất CSV phục vụ Power BI.

Thiết kế lũy đẳng (Idempotent): Mỗi lần chạy sẽ xóa sạch bảng cũ
và nạp lại toàn bộ dữ liệu mới, đảm bảo không bao giờ bị trùng lặp.
"""
import os
import re
import sqlite3
import pandas as pd
import numpy as np


def _impute_missing_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Bù khuyết ngày đăng cho các nguồn không có ngày (TopCV, JobDescriptions)
    dựa trên dải ngày thu thập thực tế (2025-10-22 đến 2025-12-10).
    Cố định seed=42 để đảm bảo tính lũy đẳng (chạy lại luôn ra kết quả y hệt).
    """
    df = df.copy()
    known_dates = df["post_date"].dropna()
    if len(known_dates) == 0:
        start_date, end_date = "2025-10-22", "2025-12-10"
    else:
        start_date, end_date = known_dates.min(), known_dates.max()

    date_pool = pd.date_range(start=start_date, end=end_date, freq="D").strftime("%Y-%m-%d").values
    missing_mask = df["post_date"].isna()
    if missing_mask.any():
        rng = np.random.RandomState(42)
        df.loc[missing_mask, "post_date"] = rng.choice(date_pool, size=missing_mask.sum())
    return df


def _build_dim_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tạo bảng chiều DIM_DATE từ cột post_date.
    """
    dates_known = pd.to_datetime(df["post_date"].dropna().unique())

    if len(dates_known) == 0:
        dates_known = pd.to_datetime(["2025-11-01"])

    date_range = pd.date_range(start=dates_known.min(), end=dates_known.max(), freq="D")

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
    return dim_date


def _build_dim_city(df: pd.DataFrame) -> pd.DataFrame:
    """Tạo bảng chiều DIM_CITY."""
    cities = sorted(df["city"].dropna().unique())
    return pd.DataFrame({
        "city_id": range(1, len(cities) + 1),
        "city_name": cities,
    })


def _build_dim_role(df: pd.DataFrame) -> pd.DataFrame:
    """Tạo bảng chiều DIM_ROLE."""
    roles = sorted(df["role_category"].dropna().unique())
    return pd.DataFrame({
        "role_id": range(1, len(roles) + 1),
        "role_name": roles,
    })


def _build_dim_level(df: pd.DataFrame) -> pd.DataFrame:
    """Tạo bảng chiều DIM_LEVEL."""
    levels = sorted(df["job_level"].dropna().unique())
    return pd.DataFrame({
        "level_id": range(1, len(levels) + 1),
        "level_name": levels,
    })


def _build_dim_company(df: pd.DataFrame) -> pd.DataFrame:
    """Tạo bảng chiều DIM_COMPANY."""
    companies = sorted(df["company"].dropna().unique())
    return pd.DataFrame({
        "company_id": range(1, len(companies) + 1),
        "company_name": companies,
    })


def _clean_skill_name(raw: str) -> str:
    """Loại bỏ triệt để dấu ngoặc vuông, ngoặc đơn, nháy kép khỏi tên kỹ năng."""
    s = str(raw).strip()
    # Loại bỏ mọi ký tự [], '', ""
    s = re.sub(r"[\[\]\'\"]+", "", s).strip()
    return s


def _build_dim_skill(df: pd.DataFrame) -> pd.DataFrame:
    """Tạo bảng chiều DIM_SKILL (bóc tách từng kỹ năng riêng lẻ)."""
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


def _build_fact_job_postings(
    df: pd.DataFrame,
    dim_date: pd.DataFrame,
    dim_city: pd.DataFrame,
    dim_role: pd.DataFrame,
    dim_level: pd.DataFrame,
    dim_company: pd.DataFrame,
) -> pd.DataFrame:
    """Xây dựng bảng Fact chính: FACT_JOB_POSTINGS."""
    # Tạo lookup dictionaries cho hiệu suất
    date_lookup = dict(zip(dim_date["full_date"], dim_date["date_id"]))
    city_lookup = dict(zip(dim_city["city_name"], dim_city["city_id"]))
    role_lookup = dict(zip(dim_role["role_name"], dim_role["role_id"]))
    level_lookup = dict(zip(dim_level["level_name"], dim_level["level_id"]))
    company_lookup = dict(zip(dim_company["company_name"], dim_company["company_id"]))

    fact = pd.DataFrame({
        "job_id": df["job_id"].astype(int),
        "date_id": df["post_date"].map(date_lookup).astype(int),
        "city_id": df["city"].map(city_lookup).astype(int),
        "role_id": df["role_category"].map(role_lookup).astype(int),
        "level_id": df["job_level"].map(level_lookup).astype(int),
        "company_id": df["company"].map(company_lookup).astype(int),
        "salary_min": df["salary_min"],
        "salary_max": df["salary_max"],
        "salary_avg": df["salary_avg"],
        "exp_years_min": df["exp_years_min"],
        "is_negotiable": df["is_negotiable"],
        "source": df["source"],
    })

    return fact


def _build_fact_job_skills(
    df: pd.DataFrame,
    dim_skill: pd.DataFrame,
    dim_date: pd.DataFrame,
    dim_city: pd.DataFrame,
    dim_role: pd.DataFrame,
) -> pd.DataFrame:
    """
    Xây dựng bảng Fact kỹ năng: FACT_JOB_SKILLS.
    Bóc tách (explode) từng kỹ năng riêng lẻ theo từng tin tuyển dụng.
    Đây là bảng trung tâm phục vụ biểu đồ "Top kỹ năng theo thời gian".
    """
    skill_lookup = dict(zip(dim_skill["skill_name"], dim_skill["skill_id"]))
    date_lookup = dict(zip(dim_date["full_date"], dim_date["date_id"]))
    city_lookup = dict(zip(dim_city["city_name"], dim_city["city_id"]))
    role_lookup = dict(zip(dim_role["role_name"], dim_role["role_id"]))

    rows = []
    for _, row in df.iterrows():
        if pd.isna(row["skills_list"]) or not str(row["skills_list"]).strip():
            continue
        skills = [_clean_skill_name(s) for s in str(row["skills_list"]).split(",")]
        skills = [s for s in skills if s and s != "[]"]
        for skill_name in skills:
            sid = skill_lookup.get(skill_name)
            if sid is None:
                continue
            rows.append({
                "job_id": row["job_id"],
                "skill_id": sid,
                "date_id": date_lookup.get(row.get("post_date")),
                "city_id": city_lookup.get(row.get("city")),
                "role_id": role_lookup.get(row.get("role_category")),
                "salary_avg": row.get("salary_avg"),
            })

    fact_skills = pd.DataFrame(rows)
    fact_skills["job_id"] = fact_skills["job_id"].astype(int)
    fact_skills["skill_id"] = fact_skills["skill_id"].astype(int)
    fact_skills["date_id"] = fact_skills["date_id"].astype(int)
    fact_skills["city_id"] = fact_skills["city_id"].astype(int)
    fact_skills["role_id"] = fact_skills["role_id"].astype(int)
    return fact_skills


def load_to_warehouse(df_clean: pd.DataFrame, warehouse_dir: str) -> dict[str, pd.DataFrame]:
    """
    Xây dựng Star Schema và nạp vào Data Warehouse.
    
    Thiết kế lũy đẳng: xóa sạch toàn bộ dữ liệu cũ trước khi nạp mới.
    Hỗ trợ 2 đích:
      1. SQLite database (it_recruitment_dwh.db)
      2. Các tệp CSV riêng lẻ (để Power BI đọc trực tiếp)
    
    Trả về dict chứa toàn bộ các bảng Fact/Dim.
    """
    os.makedirs(warehouse_dir, exist_ok=True)

    # ====== Bù khuyết ngày đăng cho 100% bản ghi ======
    df_clean = _impute_missing_dates(df_clean)

    # ====== Xây dựng các bảng Dimension ======
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

    print("  -> Xây dựng bảng DIM_SKILL (bóc tách kỹ năng)...")
    dim_skill = _build_dim_skill(df_clean)

    # ====== Xây dựng các bảng Fact ======
    print("  -> Xây dựng bảng FACT_JOB_POSTINGS...")
    fact_jobs = _build_fact_job_postings(
        df_clean, dim_date, dim_city, dim_role, dim_level, dim_company
    )

    print("  -> Xây dựng bảng FACT_JOB_SKILLS (bóc tách kỹ năng theo từng tin)...")
    fact_skills = _build_fact_job_skills(
        df_clean, dim_skill, dim_date, dim_city, dim_role
    )

    # ====== Tập hợp toàn bộ bảng ======
    tables = {
        "dim_date":           dim_date,
        "dim_city":           dim_city,
        "dim_role":           dim_role,
        "dim_level":          dim_level,
        "dim_company":        dim_company,
        "dim_skill":          dim_skill,
        "fact_job_postings":  fact_jobs,
        "fact_job_skills":    fact_skills,
    }

    # ====== 1. Nạp vào SQLite (Truncate & Full Refresh - Lũy đẳng) ======
    db_path = os.path.join(warehouse_dir, "it_recruitment_dwh.db")
    print(f"  -> Nạp vào SQLite: {db_path}")

    conn = sqlite3.connect(db_path)
    try:
        for table_name, table_df in tables.items():
            # Xóa bảng cũ hoàn toàn rồi tạo lại -> đảm bảo lũy đẳng
            table_df.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.commit()
    finally:
        conn.close()

    # ====== 2. Xuất CSV (ghi đè) cho Power BI đọc trực tiếp ======
    print("  -> Xuất các tệp CSV cho Power BI...")
    for table_name, table_df in tables.items():
        csv_path = os.path.join(warehouse_dir, f"{table_name}.csv")
        table_df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    # ====== 3. Xuất bảng phẳng chính (giữ tương thích ngược) ======
    processed_dir = os.path.join(os.path.dirname(warehouse_dir), "processed")
    os.makedirs(processed_dir, exist_ok=True)
    df_clean.to_csv(
        os.path.join(processed_dir, "it_jobs_cleaned.csv"),
        index=False, encoding="utf-8-sig",
    )

    # ====== In thống kê ======
    print("  => Thống kê Data Warehouse:")
    for table_name, table_df in tables.items():
        print(f"     {table_name:25s} : {len(table_df):>6} dòng")

    return tables
