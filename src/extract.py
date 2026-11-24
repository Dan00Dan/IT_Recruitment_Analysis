"""
Module Extract (Trích xuất dữ liệu)
Đọc toàn bộ tệp CSV thô từ thư mục data/raw/ và trả về các DataFrame gốc.
"""
import os
import pandas as pd


def extract_all(raw_dir: str) -> dict[str, pd.DataFrame]:
    """
    Đọc toàn bộ tệp dữ liệu thô từ thư mục raw_dir.
    Trả về dict ánh xạ tên nguồn -> DataFrame.
    """
    # Danh sách các tệp cần đọc và tên nguồn tương ứng
    file_map = {
        "ITViec":           "ITViec_data.csv",
        "TopCV":            "TopCV_jobs.csv",
        "JobDescriptions":  "job_descriptions.csv",
        "VietnamWorks":     "vietnamworks_jobs.csv",
    }

    dataframes = {}
    total_rows = 0

    for source_name, filename in file_map.items():
        filepath = os.path.join(raw_dir, filename)
        if not os.path.exists(filepath):
            print(f"  [CẢNH BÁO] Không tìm thấy tệp: {filepath}. Bỏ qua.")
            continue

        df = pd.read_csv(filepath)
        dataframes[source_name] = df
        total_rows += len(df)
        print(f"  -> Đọc {source_name}: {len(df):>5} dòng, {len(df.columns)} cột")

    print(f"  => Tổng cộng: {total_rows} bản ghi thô từ {len(dataframes)} nguồn.")
    return dataframes
