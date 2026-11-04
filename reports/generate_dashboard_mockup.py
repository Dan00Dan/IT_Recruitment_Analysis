"""
Script tạo ảnh mẫu Dashboard trực quan chuẩn Power BI
Sử dụng dữ liệu thật từ Data Warehouse.
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Cài đặt font chữ hỗ trợ tiếng Việt trên Windows
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'Tahoma', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WAREHOUSE_DIR = os.path.join(BASE_DIR, 'data', 'warehouse')
OUTPUT_PATH = os.path.join(BASE_DIR, 'reports', 'dashboard_mockup.png')

# 1. Đọc dữ liệu từ warehouse
dim_date = pd.read_csv(os.path.join(WAREHOUSE_DIR, 'dim_date.csv'))
dim_city = pd.read_csv(os.path.join(WAREHOUSE_DIR, 'dim_city.csv'))
dim_role = pd.read_csv(os.path.join(WAREHOUSE_DIR, 'dim_role.csv'))
dim_skill = pd.read_csv(os.path.join(WAREHOUSE_DIR, 'dim_skill.csv'))
fact_jobs = pd.read_csv(os.path.join(WAREHOUSE_DIR, 'fact_job_postings.csv'))
fact_skills = pd.read_csv(os.path.join(WAREHOUSE_DIR, 'fact_job_skills.csv'))

# 2. Tính toán các chỉ số KPI
total_jobs = len(fact_jobs)
avg_salary = fact_jobs['salary_avg'].mean()
total_companies = fact_jobs['company_id'].nunique()
total_skills = len(dim_skill)

# 3. Tính toán dữ liệu các biểu đồ
# Top 10 Kỹ năng
skill_counts = fact_skills['skill_id'].value_counts().head(10).reset_index()
skill_counts.columns = ['skill_id', 'count']
top10_skills = skill_counts.merge(dim_skill, on='skill_id').sort_values('count', ascending=True)

# Top 5 Kỹ năng theo thời gian
top5_skill_ids = skill_counts.head(5)['skill_id'].tolist()
m_skills = fact_skills[fact_skills['skill_id'].isin(top5_skill_ids)].merge(dim_date, on='date_id').merge(dim_skill, on='skill_id')
pivot_skills = m_skills.groupby(['month_year', 'skill_name']).size().unstack()
months_order = ['10/2025', '11/2025', '12/2025']
months_labels = ['Tháng 10', 'Tháng 11', 'Tháng 12']
pivot_skills = pivot_skills.reindex(months_order)

# Lương theo nhóm vị trí (Top 8 vị trí có nhiều tin nhất)
role_stats = fact_jobs.groupby('role_id').agg(
    avg_sal=('salary_avg', 'mean'),
    count=('job_id', 'count')
).reset_index().merge(dim_role, on='role_id')
top_roles = role_stats.sort_values('count', ascending=False).head(8).sort_values('avg_sal', ascending=True)

# Phân bố việc làm theo thành phố
city_counts = fact_jobs['city_id'].value_counts().reset_index()
city_counts.columns = ['city_id', 'count']
city_data = city_counts.merge(dim_city, on='city_id')
top_cities = city_data.head(4).copy()
other_count = city_data.iloc[4:]['count'].sum()
if other_count > 0:
    other_row = pd.DataFrame([{'city_id': 0, 'count': other_count, 'city_name': 'Khác'}])
    top_cities = pd.concat([top_cities, other_row], ignore_index=True)

# ==================== VẼ DASHBOARD ====================
fig = plt.figure(figsize=(19.2, 10.8), facecolor='#F3F4F6')

# 1. Header (Banner trên cùng)
ax_header = fig.add_axes([0.02, 0.91, 0.96, 0.07], facecolor='#1E293B')
ax_header.axis('off')
rect_header = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.01,rounding_size=0.02",
                                    facecolor='#0F172A', edgecolor='none', transform=ax_header.transAxes)
ax_header.add_patch(rect_header)
ax_header.text(0.02, 0.62, "IT RECRUITMENT MARKET & SKILLS ANALYSIS DASHBOARD",
              fontsize=18, fontweight='bold', color='#FFFFFF', transform=ax_header.transAxes)
ax_header.text(0.02, 0.22, "Báo cáo Phân tích Tuyển dụng IT & Nhu cầu Kỹ năng Công nghệ tại Việt Nam | Nguồn: Data Warehouse Star Schema",
              fontsize=11, color='#94A3B8', transform=ax_header.transAxes)
ax_header.text(0.98, 0.45, "Power BI Design Mockup",
              fontsize=12, fontweight='bold', color='#38BDF8', ha='right', transform=ax_header.transAxes)

# 2. Bốn thẻ KPI Cards
kpis = [
    {"label": "TỔNG SỐ TIN TUYỂN DỤNG", "val": f"{total_jobs:,}", "unit": "tin", "color": "#2563EB", "sub": "100% dữ liệu đã làm sạch"},
    {"label": "MỨC LƯƠNG TRUNG BÌNH", "val": f"{avg_salary:.1f}", "unit": "Tr VNĐ/tháng", "color": "#059669", "sub": "Định lượng chuẩn hóa"},
    {"label": "CÔNG TY TUYỂN DỤNG", "val": f"{total_companies:,}", "unit": "doanh nghiệp", "color": "#D97706", "sub": "Toàn thị trường CNTT"},
    {"label": "KỸ NĂNG CÔNG NGHỆ", "val": f"{total_skills:,}", "unit": "kỹ năng", "color": "#7C3AED", "sub": "Đã bóc tách chuẩn hóa"}
]

card_w = 0.2275
gap = 0.0165
for i, kpi in enumerate(kpis):
    x_pos = 0.02 + i * (card_w + gap)
    ax_card = fig.add_axes([x_pos, 0.79, card_w, 0.10], facecolor='none')
    ax_card.axis('off')
    
    card_bg = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02,rounding_size=0.06",
                                    facecolor='#FFFFFF', edgecolor='#E2E8F0', linewidth=1.5,
                                    transform=ax_card.transAxes)
    ax_card.add_patch(card_bg)
    stripe = patches.Rectangle((0.01, 0.15), 0.02, 0.7, facecolor=kpi['color'],
                              transform=ax_card.transAxes)
    ax_card.add_patch(stripe)
    
    ax_card.text(0.06, 0.72, kpi['label'], fontsize=10, fontweight='bold', color='#64748B', transform=ax_card.transAxes)
    ax_card.text(0.06, 0.32, kpi['val'], fontsize=22, fontweight='heavy', color='#0F172A', transform=ax_card.transAxes)
    ax_card.text(0.06 + len(kpi['val'])*0.045 + 0.02, 0.36, kpi['unit'], fontsize=10, fontweight='semibold', color=kpi['color'], transform=ax_card.transAxes)
    ax_card.text(0.06, 0.12, kpi['sub'], fontsize=9, color='#94A3B8', transform=ax_card.transAxes)

# 3. Bốn Biểu đồ chính
# Biểu đồ 1: Xu hướng Top 5 Kỹ năng theo thời gian
ax1 = fig.add_axes([0.02, 0.42, 0.47, 0.34], facecolor='#FFFFFF')
ax1.set_title("1. Xu Hướng Nhu Cầu Top 5 Kỹ Năng Theo Thời Gian (Đề tài trọng tâm)",
              fontsize=13, fontweight='bold', color='#0F172A', pad=15, loc='left')

colors_top5 = {'JavaScript': '#F59E0B', 'Java': '#DC2626', 'Python': '#2563EB', 'Git': '#4F46E5', 'AWS': '#059669'}
markers = ['o', 's', '^', 'D', 'v']

x_coords = np.arange(len(months_labels))
for idx, skill in enumerate(pivot_skills.columns):
    y_vals = pivot_skills[skill].values
    col = colors_top5.get(skill, '#64748B')
    ax1.plot(x_coords, y_vals, marker=markers[idx % len(markers)], linewidth=3,
             markersize=8, label=skill, color=col)
    for x_i, y_i in zip(x_coords, y_vals):
        ax1.annotate(f"{y_i}", (x_i, y_i), textcoords="offset points", xytext=(0, 7),
                     ha='center', fontsize=9, fontweight='bold', color=col)

ax1.set_xticks(x_coords)
ax1.set_xticklabels(months_labels, fontsize=11, fontweight='semibold', color='#334155')
ax1.set_ylabel("Số lượt tin yêu cầu kỹ năng", fontsize=10, color='#64748B')
ax1.grid(axis='y', linestyle='--', alpha=0.5, color='#CBD5E1')
ax1.set_ylim(0, max(pivot_skills.max()) * 1.18)
ax1.legend(loc='upper right', frameon=True, facecolor='#F8FAFC', edgecolor='#E2E8F0', fontsize=10)
for spine in ax1.spines.values():
    spine.set_color('#E2E8F0')

# Biểu đồ 2: Top 10 Kỹ năng được săn đón nhất
ax2 = fig.add_axes([0.51, 0.42, 0.47, 0.34], facecolor='#FFFFFF')
ax2.set_title("2. Top 10 Kỹ Năng Công Nghệ Được Săn Đón Nhất",
              fontsize=13, fontweight='bold', color='#0F172A', pad=15, loc='left')

bars = ax2.barh(top10_skills['skill_name'], top10_skills['count'],
                color='#3B82F6', height=0.65, edgecolor='none')
for bar in bars[-3:]:
    bar.set_color('#1D4ED8')

for bar in bars:
    w = bar.get_width()
    ax2.text(w + 12, bar.get_y() + bar.get_height()/2, f"{int(w):,} tin",
             va='center', fontsize=9.5, fontweight='bold', color='#1E293B')

ax2.set_xlabel("Số lượng tin tuyển dụng yêu cầu", fontsize=10, color='#64748B')
ax2.grid(axis='x', linestyle='--', alpha=0.5, color='#CBD5E1')
ax2.set_xlim(0, top10_skills['count'].max() * 1.15)
for spine in ax2.spines.values():
    spine.set_color('#E2E8F0')

# Biểu đồ 3: Mức lương trung bình theo vai trò IT
ax3 = fig.add_axes([0.02, 0.05, 0.47, 0.33], facecolor='#FFFFFF')
ax3.set_title("3. Mức Lương Trung Bình Theo Nhóm Vị Trí IT (Triệu VNĐ/tháng)",
              fontsize=13, fontweight='bold', color='#0F172A', pad=15, loc='left')

bars_sal = ax3.barh(top_roles['role_name'], top_roles['avg_sal'],
                    color='#10B981', height=0.65, edgecolor='none')
for bar in bars_sal[-2:]:
    bar.set_color('#047857')

for bar in bars_sal:
    w = bar.get_width()
    ax3.text(w + 0.8, bar.get_y() + bar.get_height()/2, f"{w:.1f} tr",
             va='center', fontsize=9.5, fontweight='bold', color='#065F46')

ax3.set_xlabel("Mức lương trung bình (Triệu VNĐ/tháng)", fontsize=10, color='#64748B')
ax3.grid(axis='x', linestyle='--', alpha=0.5, color='#CBD5E1')
ax3.set_xlim(0, top_roles['avg_sal'].max() * 1.15)
for spine in ax3.spines.values():
    spine.set_color('#E2E8F0')

# Biểu đồ 4: Cơ cấu việc làm theo Thành phố
ax4 = fig.add_axes([0.51, 0.05, 0.47, 0.33], facecolor='#FFFFFF')
ax4.set_title("4. Phân Bố Tin Tuyển Dụng Theo Khu Vực Địa Lý",
              fontsize=13, fontweight='bold', color='#0F172A', pad=15, loc='left')

donut_colors = ['#3B82F6', '#60A5FA', '#93C5FD', '#F59E0B', '#94A3B8']
wedges, texts, autotexts = ax4.pie(
    top_cities['count'],
    labels=top_cities['city_name'],
    autopct='%1.1f%%',
    pctdistance=0.75,
    colors=donut_colors[:len(top_cities)],
    startangle=140,
    textprops={'fontsize': 10, 'fontweight': 'semibold', 'color': '#1E293B'},
    wedgeprops={'width': 0.45, 'edgecolor': '#FFFFFF', 'linewidth': 2}
)
for autotext in autotexts:
    autotext.set_color('#0F172A')
    autotext.set_fontsize(9.5)
    autotext.set_fontweight('bold')

center_circle = plt.Circle((0, 0), 0.50, fc='#FFFFFF')
ax4.add_artist(center_circle)
ax4.text(0, 0.08, "TỔNG CỘNG", ha='center', va='center', fontsize=9, fontweight='bold', color='#64748B')
ax4.text(0, -0.08, f"{total_jobs:,}", ha='center', va='center', fontsize=16, fontweight='heavy', color='#0F172A')

# Lưu ảnh chất lượng cao
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
plt.savefig(OUTPUT_PATH, dpi=120, bbox_inches='tight')
plt.close()
print(f"-> Đã tạo ảnh mẫu Dashboard thành công tại: {OUTPUT_PATH}")
