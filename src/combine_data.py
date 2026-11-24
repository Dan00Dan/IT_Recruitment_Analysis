import pandas as pd
import numpy as np
import re
from pathlib import Path

old_path = Path("data/processed/it_jobs_cleaned.csv")
new_path = Path("data/raw/step-07-jev-extracted.jsonl")
out_path = Path("data/processed/it_jobs_combined.csv")

old = pd.read_csv(old_path)
new = pd.read_json(new_path, lines=True)

# Chỉ giữ tin được xác định là IT
new = new[new["is_tech"].astype(str).str.lower() == "tech"].copy()

def get_category(x, key):
    return x.get(key) if isinstance(x, dict) else None

def parse_date(value):
    if pd.isna(value):
        return pd.NaT
    try:
        number = float(value)
        if number > 1e11:
            return pd.to_datetime(number, unit="ms", errors="coerce")
    except (ValueError, TypeError):
        pass
    return pd.to_datetime(value, format="mixed", errors="coerce")

def parse_salary(value):
    if pd.isna(value):
        return np.nan, np.nan, np.nan, False
    s = str(value).lower()
    if any(x in s for x in ["thỏa thuận", "thương lượng", "negotiable",
                             "sign in", "login to view"]):
        return np.nan, np.nan, np.nan, True
    if not any(x in s for x in ["triệu", "million", "mil", "vnd"]):
        return np.nan, np.nan, np.nan, False
    nums = [float(x.replace(",", ".")) for x in
            re.findall(r"\d+(?:[.,]\d+)?", s)]
    if not nums:
        return np.nan, np.nan, np.nan, False
    lo, hi = (nums[0], nums[1]) if len(nums) >= 2 else (nums[0], nums[0])
    return lo, hi, (lo + hi) / 2, False

salary_values = new["salary"].apply(parse_salary)

new_df = pd.DataFrame({
    "job_id": new["job_url"].fillna(
        new["site"].astype(str) + "_" + new.index.astype(str)
    ).astype(str),
    "job_title": new["title"],
    "company": new["company"],
    "city": new["location"],
    "role_category": new["classification"].apply(
        lambda x: get_category(x, "title_category")
    ),
    "job_level": new["experience_level"].fillna(
        new["classification"].apply(
            lambda x: get_category(x, "seniority_category")
        )
    ),
    "exp_years_min": pd.to_numeric(
        new["experience_months"], errors="coerce"
    ) / 12,
    "salary_min": [x[0] for x in salary_values],
    "salary_max": [x[1] for x in salary_values],
    "salary_avg": [x[2] for x in salary_values],
    "is_negotiable": [x[3] for x in salary_values],
    "skills_list": new["skills"].apply(
        lambda x: ", ".join(map(str, x)) if isinstance(x, list)
        else (str(x) if pd.notna(x) else np.nan)
    ),
    "source": new["site"],
    "post_date": new["date_posted"].apply(parse_date)
})

# Chuẩn hóa kiểu dữ liệu và nội dung để đối chiếu trùng
def norm(series):
    return (series.fillna("").astype(str).str.lower()
            .str.replace(r"\s+", " ", regex=True).str.strip())

old["job_id"] = old["job_id"].astype(str)
old["post_date"] = pd.to_datetime(old["post_date"], errors="coerce")
old["dedup_key"] = (
    norm(old["job_title"]) + "|" +
    norm(old["company"]) + "|" + norm(old["city"])
)
new_df["dedup_key"] = (
    norm(new_df["job_title"]) + "|" +
    norm(new_df["company"]) + "|" + norm(new_df["city"])
)

# Chỉ đối chiếu khi có đủ tiêu đề và công ty
old_keys = set(old.loc[
    norm(old["job_title"]).ne("") & norm(old["company"]).ne(""),
    "dedup_key"
])
valid_new = norm(new_df["job_title"]).ne("") & norm(new_df["company"]).ne("")
duplicate = valid_new & new_df["dedup_key"].isin(old_keys)

new_df = new_df.loc[~duplicate].copy()
new_df = new_df.drop_duplicates(subset=["dedup_key"])

# Gộp theo đúng 14 cột dữ liệu cũ
old = old.drop(columns=["dedup_key"], errors="ignore")
new_df = new_df.drop(columns=["dedup_key"], errors="ignore")
result = pd.concat([old, new_df], ignore_index=True)

result.to_csv(out_path, index=False, encoding="utf-8-sig")

print("\n===== KẾT QUẢ GỘP DỮ LIỆU =====")
print("Dữ liệu cũ:", len(old))
print("Tin IT mới ban đầu:", 3031)
print("Tin trùng bị loại:", int(duplicate.sum()))
print("Tin mới sau xử lý:", len(new_df))
print("TỔNG DỮ LIỆU CUỐI:", len(result))
print("Số cột:", len(result.columns))
print("File đã tạo:", out_path)
