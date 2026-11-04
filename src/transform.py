"""
Module Transform (Biến đổi & Làm sạch dữ liệu)
Thực hiện toàn bộ quy trình: khử trùng lặp, lọc phi IT, chuẩn hóa lương/thành phố/vai trò/cấp bậc/kỹ năng,
hợp nhất đa nguồn và khử trùng lặp logic liên nguồn.
"""
import re
import ast
import pandas as pd
import numpy as np


# ========== HẰNG SỐ VÀ TỪ ĐIỂN ==========

# Tỷ giá quy đổi: 1 USD = 0.0254 triệu VNĐ (tức 25.400 VNĐ)
USD_TO_VND_MILLION = 25.4 / 1000

# Từ khóa nhận diện công việc KHÔNG thuộc ngành IT
NON_IT_KEYWORDS = [
    "cnc", "nx cam", "vận hành máy", "kỹ thuật điện", "xử lý nước",
    "iso 22000", "haccp", "vietgap", "thị trường", "cơ khí",
    "sửa chữa điện", "phay cnc", "tiện cnc", "bảo trì hệ thống xử lý",
]

# Danh sách kỹ năng công nghệ chuẩn để quét bù khuyết
TECH_KEYWORDS = [
    "Python", "Java", "C++", "C#", ".NET", "ASP.NET", "JavaScript", "TypeScript",
    "React", "ReactJS", "Vue", "VueJS", "Angular", "NodeJS", "Node.js", "PHP",
    "Golang", "Go", "Swift", "Kotlin", "Flutter", "React Native", "SQL", "MySQL",
    "PostgreSQL", "MongoDB", "Redis", "Oracle", "Docker", "Kubernetes", "K8s",
    "AWS", "Azure", "GCP", "CI/CD", "Git", "Linux", "Spring Boot", "Spring",
    "Django", "FastAPI", "Flask", "Laravel", "Kafka", "Spark", "TensorFlow",
    "PyTorch", "HTML", "CSS", "Tailwind", "Bootstrap", "Selenium", "Cypress",
    "JMeter", "Postman", "GraphQL", "REST API", "Microservices", "Hadoop",
    "Tableau", "Power BI",
]


# ========== CÁC HÀM XỬ LÝ ==========

def is_it_job(title: str) -> bool:
    """Kiểm tra xem tiêu đề công việc có thuộc ngành IT hay không."""
    t_lower = str(title).lower()
    return not any(kw in t_lower for kw in NON_IT_KEYWORDS)


def parse_salary(val) -> tuple:
    """
    Phân tích chuỗi lương tự do -> (salary_min, salary_max, salary_avg, is_negotiable).
    Đơn vị đầu ra: Triệu VNĐ/tháng.
    """
    if pd.isna(val):
        return None, None, None, True

    val_str = str(val).strip()
    val_lower = val_str.lower()

    # Nhận diện tin thỏa thuận / không công khai lương
    negotiable_keywords = [
        "love it", "negotiable", "attractive", "thương lượng", "thoả thuận",
        "thỏa thuận", "competitive", "discuss", "nego", "hấp dẫn",
        "tùy năng lực", "month salary", "acttractive",
    ]
    if any(k in val_lower for k in negotiable_keywords):
        return None, None, None, True

    # Lương năm USD ($55k/year, $18k/year)
    year_match = re.search(r'\$?(\d+)\s*k?\s*(?:/year|per year)', val_lower)
    if year_match:
        usd_year = float(year_match.group(1)) * 1000
        vnd_monthly = (usd_year * USD_TO_VND_MILLION) / 12
        return round(vnd_monthly, 1), round(vnd_monthly, 1), round(vnd_monthly, 1), False

    is_usd = bool(re.search(r'\$|usd', val_lower))

    # Chuẩn hóa chuỗi số (xóa dấu phẩy/chấm phân cách ngàn)
    cleaned = re.sub(r'(\d),(\d)', r'\1\2', val_str)
    cleaned = re.sub(r'(\d+)\.(\d{3})\.(\d{3})', r'\1\2\3', cleaned)
    cleaned = re.sub(r'(\d+)\.(\d{3})', r'\1\2', cleaned)

    # Số tiền VNĐ đầy đủ (25000000 -> 25 triệu)
    vnd_full_match = re.findall(r'(\d{7,9})', cleaned)
    if vnd_full_match and not is_usd:
        nums = [float(x) / 1_000_000 for x in vnd_full_match]
        if len(nums) == 1:
            if any(k in val_lower for k in ["tới", "up to", "dưới"]):
                return None, round(nums[0], 1), round(nums[0], 1), False
            return round(nums[0], 1), None, round(nums[0], 1), False
        elif len(nums) >= 2:
            return round(nums[0], 1), round(nums[1], 1), round((nums[0] + nums[1]) / 2, 1), False

    # Khoảng lương: X - Y
    range_match = re.search(
        r'(\d+(?:\.\d+)?)\s*(?:tr|m|triệu|k|\$)?\s*(?:-|–|to)\s*(\d+(?:\.\d+)?)', cleaned
    )
    if range_match:
        n1, n2 = float(range_match.group(1)), float(range_match.group(2))
        if is_usd:
            v1 = n1 * 25.4 if n1 < 100 else n1 * USD_TO_VND_MILLION
            v2 = n2 * 25.4 if n2 < 100 else n2 * USD_TO_VND_MILLION
        else:
            v1, v2 = n1, n2
        return round(v1, 1), round(v2, 1), round((v1 + v2) / 2, 1), False

    # Dạng Up to / Tới X
    upto_match = re.search(
        r'(?:up to|upto|tới|dưới|<|nhỏ hơn)\s*\$?(\d+(?:\.\d+)?)', cleaned, re.IGNORECASE
    )
    if upto_match:
        n = float(upto_match.group(1))
        v = (n * 25.4 if n < 100 else n * USD_TO_VND_MILLION) if is_usd else n
        return None, round(v, 1), round(v, 1), False

    # Dạng From / Từ X
    from_match = re.search(
        r'(?:from|từ|trên|lớn hơn|>)\s*\$?(\d+(?:\.\d+)?)', cleaned, re.IGNORECASE
    )
    if from_match:
        n = float(from_match.group(1))
        v = (n * 25.4 if n < 100 else n * USD_TO_VND_MILLION) if is_usd else n
        return round(v, 1), None, round(v, 1), False

    return None, None, None, True


def standardize_city(val) -> str:
    """Chuẩn hóa địa chỉ tự do về tên tỉnh/thành phố chuẩn."""
    if not val or pd.isna(val):
        return "Không xác định"
    s = str(val).lower()

    if "not specified" in s or "chưa xác định" in s:
        return "Không xác định"
    if "remote" in s or "toàn quốc" in s:
        return "Remote / Toàn quốc"
    if any(k in s for k in ["hồ chí minh", "ho chi minh", "hcm", "sài gòn", "sai gon",
                             "thu duc", "thủ đức", "qtsc"]):
        return "Hồ Chí Minh"
    if any(k in s for k in ["hà nội", "ha noi", "cau giay", "cầu giấy", "ba đình",
                             "ba dinh", "đống đa", "dong da", "hai bà trưng", "hai ba trung"]):
        return "Hà Nội"
    if "đà nẵng" in s or "da nang" in s:
        return "Đà Nẵng"
    if "cần thơ" in s or "can tho" in s:
        return "Cần Thơ"
    if "hải phòng" in s or "hai phong" in s:
        return "Hải Phòng"
    if "bình dương" in s or "binh duong" in s:
        return "Bình Dương"
    if "bắc ninh" in s or "bac ninh" in s:
        return "Bắc Ninh"
    if "đồng nai" in s or "dong nai" in s:
        return "Đồng Nai"
    return "Khác"


def classify_role(title: str, original_role=None) -> str:
    """Phân loại chức danh công việc về 12 nhóm vai trò IT chuẩn."""
    combined = f"{str(original_role)} {str(title)}".lower()

    if any(k in combined for k in ["fullstack", "full-stack", "full stack"]):
        return "Fullstack Developer"
    if any(k in combined for k in ["mobile", "ios", "android", "flutter", "react native",
                                    "swift", "kotlin"]):
        return "Mobile Developer"
    if any(k in combined for k in ["frontend", "front-end", "front end", "reactjs",
                                    "react js", "vue", "angular"]):
        return "Frontend Developer"
    if any(k in combined for k in ["backend", "back-end", "back end", "java", "python",
                                    "golang", "go dev", "php", ".net", "nodejs", "node.js"]):
        return "Backend Developer"
    if any(k in combined for k in ["qa", "qc", "tester", "testing", "test",
                                    "quality assurance", "kiem thu", "kiểm thử"]):
        return "QA / QC / Tester"
    if any(k in combined for k in ["devops", "cloud", "sre", "system", "sysadmin",
                                    "infrastructure", "ha tang", "hạ tầng"]):
        return "DevOps / Cloud / System"
    if any(k in combined for k in ["data engineer", "data analyst", "data scientist", "ai",
                                    "machine learning", "deep learning", "nlp", "llm",
                                    "bi analyst", "du lieu", "dữ liệu"]):
        return "Data / AI / Machine Learning"
    if any(k in combined for k in ["security", "an toan thong tin", "an toàn thông tin",
                                    "bao mat", "bảo mật", "cyber", "pentest"]):
        return "Security / Network"
    if any(k in combined for k in ["business analyst", "ba ", "po ", "product owner",
                                    "project manager", "pm ", "scrum master"]):
        return "BA / PM / Product"
    if any(k in combined for k in ["embedded", "iot", "nhung", "nhúng", "firmware",
                                    "hardware", "vi mach", "vi mạch"]):
        return "Embedded / IoT"
    if any(k in combined for k in ["software engineer", "lap trinh vien", "lập trình viên",
                                    "developer", "engineer"]):
        return "Software Engineer (Chung)"
    return "Other IT Roles"


def extract_experience_and_level(title: str, exp_text=None, level_text=None) -> tuple:
    """Trích xuất số năm kinh nghiệm tối thiểu và suy luận cấp bậc nghề nghiệp."""
    combined = f"{str(title)} {str(exp_text)} {str(level_text)}".lower()

    years = None
    m = re.search(
        r'(?:từ|at least|tối thiểu|minimum)?\s*(\d+)(?:\+|\s*-\s*\d+)?\s*(?:năm|year|years)',
        combined,
    )
    if m:
        try:
            years = float(m.group(1))
        except ValueError:
            years = None

    if any(k in combined for k in ["intern", "thực tập", "fresher", "trainee"]):
        level = "Intern / Fresher"
        if years is None:
            years = 0.0
    elif any(k in combined for k in ["lead", "trưởng nhóm", "manager", "quản lý",
                                      "director", "architect", "giám đốc", "head"]):
        level = "Lead / Manager"
    elif any(k in combined for k in ["senior", "sr.", "chuyên gia"]):
        level = "Senior"
    elif any(k in combined for k in ["junior", "jr."]):
        level = "Junior"
    elif any(k in combined for k in ["middle", "mid-level", "mid level"]):
        level = "Middle"
    elif years is not None:
        if years < 1:
            level = "Intern / Fresher"
        elif years < 2:
            level = "Junior"
        elif years < 4:
            level = "Middle"
        elif years < 7:
            level = "Senior"
        else:
            level = "Lead / Manager"
    else:
        level = "Không xác định"

    return years, level


def parse_and_impute_skills(skills_val, text_fallback: str = "") -> str:
    """Chuẩn hóa danh sách kỹ năng và bù khuyết từ tiêu đề nếu thiếu."""
    extracted = set()

    if pd.notna(skills_val):
        s_val = str(skills_val).strip()

        # Dạng list/chuỗi chứa dấu nháy ngoặc vuông: "['.NET'] ['Microservices']"
        quoted = re.findall(r"['\"]([^'\"\n\[\]]+)['\"]", s_val)
        if quoted:
            for item in quoted:
                item_clean = item.strip().strip("[]'\"").strip()
                if item_clean and item_clean != "[]":
                    extracted.add(item_clean)

        # Nếu chưa trích xuất được -> tách theo dấu phẩy/chấm phẩy/pipe/space
        if not extracted:
            parts = re.split(r'[,;|\n]+', s_val)
            for p in parts:
                p_clean = p.strip().strip("[]'\"").strip()
                if p_clean and p_clean != "[]" and len(p_clean) < 30:
                    words = p_clean.split()
                    if len(words) > 1 and all(w in TECH_KEYWORDS or len(w) <= 12 for w in words):
                        for w in words:
                            extracted.add(w)
                    else:
                        extracted.add(p_clean)

    # Bù khuyết từ tiêu đề nếu danh sách kỹ năng trống
    if not extracted and text_fallback:
        t_clean = str(text_fallback)
        for kw in TECH_KEYWORDS:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, t_clean, re.IGNORECASE):
                extracted.add(kw)

    return ", ".join(sorted(extracted))


# ========== HÀM XỬ LÝ TỪNG NGUỒN DỮ LIỆU ==========

def _transform_itviec(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Biến đổi và chuẩn hóa dữ liệu ITViec."""
    df = df_raw.drop_duplicates().copy()
    df = df[df["job_names"].apply(is_it_job)].copy()

    # Chuẩn hóa lương
    sal = [parse_salary(s) for s in df["salaries"]]
    df["salary_min"] = [s[0] for s in sal]
    df["salary_max"] = [s[1] for s in sal]
    df["salary_avg"] = [s[2] for s in sal]
    df["is_negotiable"] = [s[3] for s in sal]

    # Chuẩn hóa thành phố, vai trò, cấp bậc, kỹ năng
    df["city"] = df["locate_names"].apply(standardize_city)
    df["role_category"] = [classify_role(t, p) for t, p in zip(df["job_names"], df["position_names"])]

    exp = [extract_experience_and_level(t, e) for t, e in zip(df["job_names"], df["exp_skills"])]
    df["exp_years_min"] = [e[0] for e in exp]
    df["job_level"] = [e[1] for e in exp]

    df["skills_list"] = [parse_and_impute_skills(sk, t) for sk, t in zip(df["array_skills"], df["job_names"])]
    df["source"] = "ITViec"
    df["post_date"] = pd.to_datetime(
        df["post_dates_formatted"], format="%d/%m/%Y %H:%M", errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    # Ánh xạ về schema chung
    return df.rename(columns={"job_names": "job_title", "company_names": "company"})[
        ["job_title", "company", "city", "role_category", "job_level", "exp_years_min",
         "salary_min", "salary_max", "salary_avg", "is_negotiable", "skills_list",
         "source", "post_date"]
    ]


def _transform_topcv(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Biến đổi và chuẩn hóa dữ liệu TopCV."""
    df = df_raw.drop_duplicates().copy()
    df = df[df["title"].apply(is_it_job)].copy()

    sal = [parse_salary(s) for s in df["salary"]]
    df["salary_min"] = [s[0] for s in sal]
    df["salary_max"] = [s[1] for s in sal]
    df["salary_avg"] = [s[2] for s in sal]
    df["is_negotiable"] = [s[3] for s in sal]

    df["city"] = df["location"].apply(standardize_city)
    df["role_category"] = [classify_role(t) for t in df["title"]]

    exp = [extract_experience_and_level(t, level_text=l) for t, l in zip(df["title"], df["level"])]
    df["exp_years_min"] = [e[0] for e in exp]
    df["job_level"] = [e[1] for e in exp]

    df["skills_list"] = [parse_and_impute_skills(sk, t) for sk, t in zip(df["skills"], df["title"])]
    df["source"] = "TopCV"
    df["post_date"] = np.nan

    return df.rename(columns={"title": "job_title"})[
        ["job_title", "company", "city", "role_category", "job_level", "exp_years_min",
         "salary_min", "salary_max", "salary_avg", "is_negotiable", "skills_list",
         "source", "post_date"]
    ]


def _transform_job_descriptions(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Biến đổi và chuẩn hóa dữ liệu job_descriptions."""
    df = df_raw.drop_duplicates().copy()

    df["salary_min"] = np.nan
    df["salary_max"] = np.nan
    df["salary_avg"] = np.nan
    df["is_negotiable"] = True

    df["city"] = df["city"].apply(standardize_city)
    df["role_category"] = [classify_role(t, r) for t, r in zip(df["title"], df["it_role_type"])]

    exp = [extract_experience_and_level(t, exp_text=d) for t, d in zip(df["title"], df["description"])]
    df["exp_years_min"] = [e[0] for e in exp]
    df["job_level"] = [e[1] for e in exp]

    df["skills_list"] = [
        parse_and_impute_skills(f"{str(l)} {str(k)}", t)
        for l, k, t in zip(df["main_programming_languages"], df["key_technologies"], df["title"])
    ]
    df["source"] = df["site"].fillna("JobDescriptions")
    df["post_date"] = np.nan

    return df.rename(columns={"title": "job_title"})[
        ["job_title", "company", "city", "role_category", "job_level", "exp_years_min",
         "salary_min", "salary_max", "salary_avg", "is_negotiable", "skills_list",
         "source", "post_date"]
    ]


# ========== HÀM TRANSFORM CHÍNH ==========

def transform_all(raw_dataframes: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Biến đổi từng nguồn dữ liệu, hợp nhất về schema chung và khử trùng lặp liên nguồn.
    Trả về DataFrame sạch hoàn chỉnh.
    """
    parts = []

    # Xử lý từng nguồn
    transform_map = {
        "ITViec":          _transform_itviec,
        "TopCV":           _transform_topcv,
        "JobDescriptions": _transform_job_descriptions,
    }

    for source_name, transform_fn in transform_map.items():
        if source_name in raw_dataframes:
            df_part = transform_fn(raw_dataframes[source_name])
            parts.append(df_part)
            print(f"  -> {source_name}: {len(df_part)} dòng sạch")

    if not parts:
        raise ValueError("Không có nguồn dữ liệu nào để xử lý!")

    # Hợp nhất toàn bộ
    df_merged = pd.concat(parts, ignore_index=True)
    n_before = len(df_merged)

    # Khử trùng lặp logic liên nguồn theo bộ ba (company, job_title, city)
    # Ưu tiên giữ bản ghi có lương (is_negotiable=False xếp trước)
    df_merged["_clean_company"] = df_merged["company"].astype(str).str.lower().str.strip()
    df_merged["_clean_title"] = df_merged["job_title"].astype(str).str.lower().str.strip()
    df_merged = df_merged.sort_values(by=["is_negotiable"], ascending=True)
    df_final = df_merged.drop_duplicates(subset=["_clean_company", "_clean_title", "city"]).copy()
    df_final = df_final.drop(columns=["_clean_company", "_clean_title"])
    df_final = df_final.reset_index(drop=True)

    # Gán job_id (khóa chính cho bảng Fact)
    df_final.insert(0, "job_id", range(1, len(df_final) + 1))

    n_after = len(df_final)
    print(f"  -> Khử trùng lặp liên nguồn: {n_before} -> {n_after} (loại bỏ {n_before - n_after})")
    print(f"  => Tổng cộng: {n_after} bản ghi IT sạch hoàn chỉnh.")

    return df_final
