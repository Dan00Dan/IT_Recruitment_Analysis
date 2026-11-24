import pandas as pd
from pathlib import Path

path = Path("data/processed/it_jobs_weekly.csv")
df = pd.read_csv(path)
df["post_date"] = pd.to_datetime(df["post_date"])

# Kiểm tra mô hình trên 2 tuần cuối
pred_11 = df["job_count"].iloc[7:10].mean()
pred_12 = df["job_count"].iloc[8:11].mean()

actual = df["job_count"].iloc[10:12].to_numpy()
predicted = [pred_11, pred_12]

mae = sum(abs(a-p) for a, p in zip(actual, predicted)) / 2
mape = sum(abs(a-p)/a for a, p in zip(actual, predicted)) / 2 * 100

# Dự báo 2 tuần tiếp theo
forecast_1 = df["job_count"].iloc[-3:].mean()
forecast_2 = (df["job_count"].iloc[-2:].sum() + forecast_1) / 3

forecast = pd.DataFrame({
    "post_date": ["2026-11-01", "2026-11-08"],
    "predicted_job_count": [
        round(forecast_1),
        round(forecast_2)
    ]
})

forecast.to_csv(
    "data/processed/it_jobs_forecast.csv",
    index=False,
    encoding="utf-8-sig"
)

print("=== ĐÁNH GIÁ MÔ HÌNH ===")
print("MAE:", round(mae, 2))
print("MAPE:", round(mape, 2), "%")

print("\n=== DỰ BÁO 2 TUẦN ===")
print(forecast.to_string(index=False))
print("\nĐã tạo: data/processed/it_jobs_forecast.csv")
