
import os
import pandas as pd

from src.load import load_to_warehouse


# Xác định thư mục dự án
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Đường dẫn dữ liệu đầu vào và Data Warehouse
INPUT_FILE = os.path.join(
    BASE_DIR, "data", "processed", "it_jobs_combined.csv"
)

WAREHOUSE_DIR = os.path.join(
    BASE_DIR, "data", "warehouse"
)


def main():
    print("===== COMBINED ETL PIPELINE =====")

    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"Không tìm thấy file: {INPUT_FILE}")

    # Đọc dữ liệu đã kết hợp
    df = pd.read_csv(INPUT_FILE)

    print(f"So dong dau vao: {len(df)}")
    print(f"So job_id duy nhat: {df['job_id'].nunique()}")

    # Kiểm tra dữ liệu đầu vào
    if df["job_id"].isna().any():
        raise ValueError("Du lieu co job_id bi thieu.")

    if df["job_id"].duplicated().any():
        raise ValueError("Du lieu co job_id bi trung.")

    # Nạp dữ liệu vào Data Warehouse
    load_to_warehouse(df, WAREHOUSE_DIR)

    print("\n===== ETL HOAN TAT =====")


if __name__ == "__main__":
    main()
