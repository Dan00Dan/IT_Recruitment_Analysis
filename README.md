# IT Recruitment Data Analysis in Vietnam

<p align="center">
  <b>Phân tích dữ liệu tuyển dụng IT Việt Nam</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white">
  <img src="https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white">
</p>

## 📌 Giới thiệu

Dự án phân tích dữ liệu tuyển dụng ngành Công nghệ Thông tin tại Việt Nam từ nhiều nền tảng tuyển dụng như ITViec, TopCV và Job Descriptions.

Dự án tập trung khảo sát:

- Xu hướng tuyển dụng IT tại Việt Nam.
- Phân bố mức lương theo vai trò và cấp bậc.
- Nhu cầu kỹ năng công nghệ trên thị trường.
- Cơ cấu cấp bậc tuyển dụng.
- Xu hướng tuyển dụng theo thời gian và thành phố.

Quy trình thực hiện bao gồm thu thập dữ liệu, làm sạch, tích hợp, xây dựng Data Warehouse, phân tích khám phá dữ liệu và trực quan hóa bằng Power BI.

---

## 📁 Cấu trúc thư mục

```text
IT_Recruitment_Analysis/
├── data/
│   ├── raw/
│   │   ├── ITViec_data.csv
│   │   ├── TopCV_jobs.csv
│   │   ├── job_descriptions.csv
│   │   └── vietjobs_sample.csv
│   ├── interim/
│   ├── processed/
│   └── warehouse/
│       ├── it_recruitment_dwh.db
│       ├── dim_date.csv
│       ├── dim_city.csv
│       ├── dim_role.csv
│       ├── dim_level.csv
│       ├── dim_company.csv
│       ├── dim_skill.csv
│       ├── fact_job_postings.csv
│       └── fact_job_skills.csv
├── src/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── notebooks/
│   ├── 01_data_profiling.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_data_integration.ipynb
│   └── 04_exploratory_analysis.ipynb
├── reports/
│   ├── data_quality/
│   ├── cleaning_log.xlsx
│   └── data_dictionary.xlsx
├── run_etl_pipeline.py
├── requirements.txt
└── README.md
```

---

## 🛠️ Công nghệ sử dụng

| Công nghệ | Mục đích |
|---|---|
| Python | Xử lý và phân tích dữ liệu |
| Pandas, NumPy | Làm sạch, biến đổi và tích hợp dữ liệu |
| Matplotlib, Seaborn | Trực quan hóa dữ liệu |
| Jupyter Notebook | Phân tích khám phá dữ liệu |
| SQLite | Lưu trữ Data Warehouse |
| Power BI | Xây dựng dashboard phân tích |

---

## 🚀 ETL Pipeline

Dự án xây dựng quy trình ETL tự động gồm 3 giai đoạn:

```text
       ┌───────────────────┐
       │    DATA SOURCES  │
       │ ITViec / TopCV   │
       │ Job Descriptions │
       └─────────┬─────────┘
                 │
                 ▼
       ┌───────────────────┐
       │      EXTRACT      │
       │ Trích xuất dữ liệu│
       └─────────┬─────────┘
                 │
                 ▼
       ┌───────────────────┐
       │    TRANSFORM      │
       │ Làm sạch dữ liệu  │
       │ Chuẩn hóa dữ liệu │
       │ Khử trùng lặp     │
       └─────────┬─────────┘
                 │
                 ▼
       ┌───────────────────┐
       │       LOAD        │
       │ Data Warehouse    │
       └─────────┬─────────┘
                 │
                 ▼
       ┌───────────────────┐
       │   DATA ANALYSIS   │
       │     Power BI      │
       │  Python / EDA     │
       └───────────────────┘
```

### Chạy toàn bộ ETL Pipeline

```powershell
py run_etl_pipeline.py
```

Pipeline tự động thực hiện:

1. **Extract:** Đọc dữ liệu gốc từ `data/raw/`.
2. **Transform:** Làm sạch, chuẩn hóa, khử trùng lặp và xử lý dữ liệu.
3. **Load:** Xây dựng Star Schema và nạp dữ liệu vào `data/warehouse/`.

---

## 🗄️ Data Warehouse – Star Schema

Dự án sử dụng mô hình Star Schema với 6 bảng Dimension và 2 bảng Fact.

```text
                       DIM_DATE
                          │
                          │
DIM_CITY ─────── FACT_JOB_POSTINGS ─────── DIM_ROLE
                          │
                          │
DIM_LEVEL ─────────────────┼────────────── DIM_COMPANY


                       FACT_JOB_SKILLS
                          │
                          │
                       DIM_SKILL
```

### Các bảng Dimension

| Bảng | Nội dung |
|---|---|
| `dim_date` | Thông tin thời gian |
| `dim_city` | Thông tin thành phố |
| `dim_role` | Thông tin vai trò nghề nghiệp |
| `dim_level` | Thông tin cấp bậc |
| `dim_company` | Thông tin công ty |
| `dim_skill` | Danh mục kỹ năng |

### Các bảng Fact

| Bảng | Nội dung | Số bản ghi |
|---|---|---:|
| `fact_job_postings` | Tin tuyển dụng | 4.207 |
| `fact_job_skills` | Kỹ năng gắn với tin tuyển dụng | 24.172 |

---

## 📊 Phân tích dữ liệu

### 1. Tổng quan thị trường tuyển dụng

- Tổng số tin tuyển dụng.
- Lương trung vị.
- Số công ty tuyển dụng.
- Số tin tuyển dụng theo thành phố.
- Số tin tuyển dụng theo vai trò.

### 2. Phân tích kỹ năng

- Top 15 kỹ năng được yêu cầu nhiều nhất.
- Kỹ năng theo vai trò tuyển dụng.
- Tỷ lệ tin tuyển dụng yêu cầu kỹ năng.

### 3. Xu hướng tuyển dụng

- Xu hướng số tin tuyển dụng theo thời gian.
- Biến động số lượng tin tuyển dụng theo ngày đăng.

### 4. Phân tích mức lương

- Lương trung vị theo vai trò.
- Lương trung vị theo cấp bậc.
- Tỷ lệ tin tuyển dụng có công khai mức lương.

---

## 📈 Power BI Dashboard

Dashboard được xây dựng với 4 trang phân tích chính:

| Trang | Nội dung |
|---|---|
| Overview | Tổng quan thị trường tuyển dụng IT |
| Skills | Phân tích kỹ năng được yêu cầu |
| Trends | Xu hướng tuyển dụng theo thời gian |
| Salary | Phân tích mức lương và công khai lương |

---

## 📦 Kết quả xử lý dữ liệu

| Nội dung | Kết quả |
|---|---:|
| Dữ liệu thô ban đầu | 4.876 |
| Dữ liệu sau biến đổi | 4.792 |
| Bản ghi trùng lặp được loại bỏ | 585 |
| Dữ liệu tuyển dụng cuối cùng | 4.207 |
| Số bảng Dimension | 6 |
| Số bảng Fact | 2 |
| Số công ty tuyển dụng | 1.755 |
| Số thành phố | 11 |
| Số nhóm vai trò | 12 |
| Số kỹ năng trong Data Warehouse | 1.952 |
| Liên kết kỹ năng – tin tuyển dụng | 24.172 |

---

## ⚙️ Cài đặt và sử dụng

### 1. Clone repository

```bash
git clone https://github.com/HoLeTrungBao/IT_Recruitment_Analysis.git
cd IT_Recruitment_Analysis
```

### 2. Tạo môi trường ảo

```powershell
py -m venv .venv
```

### 3. Kích hoạt môi trường

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 5. Chạy ETL

```powershell
py run_etl_pipeline.py
```

### 6. Phân tích dữ liệu

Mở các notebook trong thư mục `notebooks/` bằng Jupyter Notebook hoặc VS Code.

---

## 👥 Contributors

Dự án được thực hiện trong khuôn khổ học phần Chuyên đề 2.

---

<p align="center">
  <i>IT Recruitment Data Analysis in Vietnam</i>
</p>
