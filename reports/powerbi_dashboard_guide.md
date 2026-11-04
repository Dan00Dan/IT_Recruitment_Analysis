# Hướng Dẫn Kết Nối Power BI & Thiết Kế Dashboard Tuyển Dụng IT

Tài liệu này dành cho thành viên trong nhóm phụ trách vẽ Dashboard trên **Power BI Desktop**, kết nối trực tiếp với kho dữ liệu (**Data Warehouse**) đã được xử lý chuẩn hóa.

---

## 1. Dữ liệu đầu vào

Thư mục chứa dữ liệu:
```
data/warehouse/
```
Gồm 8 tệp CSV UTF-8 theo mô hình Star Schema:
* **Các bảng Dimension (Chiều phân tích):**
  - `dim_date.csv`: Thời gian đăng tin (ngày, tháng `10/2025`, `11/2025`, `12/2025`, quý, năm).
  - `dim_city.csv`: Tỉnh / Thành phố làm việc (Hà Nội, TP.HCM, Đà Nẵng, Cần Thơ...).
  - `dim_role.csv`: Nhóm vị trí IT (Backend, Frontend, Fullstack, Data/AI, DevOps, Mobile...).
  - `dim_level.csv`: Cấp bậc (Intern/Fresher, Junior, Middle, Senior, Lead/Manager).
  - `dim_company.csv`: Tên 1.755 doanh nghiệp tuyển dụng.
  - `dim_skill.csv`: Danh mục 1.952 kỹ năng công nghệ đã chuẩn hóa.
* **Các bảng Fact (Bảng dữ kiện / đo lường):**
  - `fact_job_postings.csv`: 4.207 tin tuyển dụng kèm mức lương trung bình, năm kinh nghiệm.
  - `fact_job_skills.csv`: 24.172 dòng bóc tách kỹ năng phục vụ phân tích nhu cầu công nghệ.

---

## 2. Các bước nạp dữ liệu vào Power BI Desktop

1. Mở **Power BI Desktop**.
2. Trên thanh menu Home, chọn **Get Data** > **Text/CSV**.
3. Duyệt đến thư mục `IT_Recruitment_Analysis/data/warehouse/` và nạp lần lượt cả 8 tệp CSV trên.
4. Kiểm tra phần *File Origin* là `65001: Unicode (UTF-8)` và bấm **Load**.

---

## 3. Thiết lập Mô hình Quan hệ (Model View - Star Schema)

Chuyển sang tab **Model view** (biểu tượng thứ 3 bên trái màn hình) và nối các trường khóa `_id`:

* `dim_date[date_id]` (1) ───< (Many) `fact_job_postings[date_id]`
* `dim_city[city_id]` (1) ───< (Many) `fact_job_postings[city_id]`
* `dim_role[role_id]` (1) ───< (Many) `fact_job_postings[role_id]`
* `dim_level[level_id]` (1) ───< (Many) `fact_job_postings[level_id]`
* `dim_company[company_id]` (1) ───< (Many) `fact_job_postings[company_id]`

* `dim_skill[skill_id]` (1) ───< (Many) `fact_job_skills[skill_id]`
* `dim_date[date_id]` (1) ───< (Many) `fact_job_skills[date_id]`
* `dim_city[city_id]` (1) ───< (Many) `fact_job_skills[city_id]`
* `dim_role[role_id]` (1) ───< (Many) `fact_job_skills[role_id]`

---

## 4. Tạo các Measure DAX cần thiết

Nhấp chuột phải vào bảng `fact_job_postings` > chọn **New measure**:

1. **Tổng số tin tuyển dụng:**
   ```dax
   Tổng Tin Tuyển Dụng = COUNTROWS(fact_job_postings)
   ```
2. **Mức lương trung bình (Triệu VNĐ/tháng):**
   ```dax
   Lương Trung Bình = ROUND(AVERAGE(fact_job_postings[salary_avg]), 1)
   ```
3. **Số lượt yêu cầu kỹ năng:**
   ```dax
   Lượt Yêu Cầu Kỹ Năng = COUNTROWS(fact_job_skills)
   ```

---

## 5. Thiết kế các biểu đồ (Tham khảo ảnh mẫu `reports/dashboard_mockup.png`)

### 1. Bốn thẻ Card ở hàng trên:
* **Card 1:** `[Tổng Tin Tuyển Dụng]` (Kết quả: 4.207 tin)
* **Card 2:** `[Lương Trung Bình]` (Kết quả: 38.5 triệu VNĐ)
* **Card 3:** `fact_job_postings[company_id]` (chọn Distinct Count: 1.755 công ty)
* **Card 4:** `dim_skill[skill_id]` (chọn Distinct Count: 1.952 kỹ năng)

### 2. Biểu đồ Xu hướng Kỹ năng theo thời gian (Line chart - Trọng tâm đề tài):
* **Visual:** **Line chart** (Biểu đồ đường).
* **X-axis:** Kéo `dim_date[month_year]` (chỉ giữ cấp Month).
* **Y-axis:** Kéo measure `[Lượt Yêu Cầu Kỹ Năng]`.
* **Legend:** Kéo `dim_skill[skill_name]`.
* **Filters on this visual:** Bấm vào `skill_name` > Filter type chọn **Top N** > nhập số `5` > ô *By value* kéo `[Lượt Yêu Cầu Kỹ Năng]` vào > bấm **Apply filter**.

### 3. Biểu đồ Top 10 Kỹ năng được săn đón nhất (Bar chart):
* **Visual:** **Clustered bar chart** (Thanh ngang).
* **Y-axis:** Kéo `dim_skill[skill_name]`.
* **X-axis:** Kéo measure `[Lượt Yêu Cầu Kỹ Năng]`.
* **Filters on this visual:** Bấm vào `skill_name` > Filter type chọn **Top N** > nhập số `10` > ô *By value* kéo `[Lượt Yêu Cầu Kỹ Năng]` vào > bấm **Apply filter**.

### 4. Biểu đồ Mức lương theo vị trí IT (Bar chart):
* **Visual:** **Clustered bar chart** (Thanh ngang).
* **Y-axis:** Kéo `dim_role[role_name]`.
* **X-axis:** Kéo measure `[Lương Trung Bình]`.
* Sắp xếp giảm dần theo mức lương.

### 5. Biểu đồ Cơ cấu việc làm theo địa lý (Donut chart):
* **Visual:** **Donut chart**.
* **Legend:** Kéo `dim_city[city_name]`.
* **Values:** Kéo measure `[Tổng Tin Tuyển Dụng]`.
