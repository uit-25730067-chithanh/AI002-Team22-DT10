# 🌾 Phân tích giá cả thị trường nông nghiệp bằng AI

> Bài tập nhóm - Môn Tư duy Trí tuệ Nhân tạo

## 📋 Giới thiệu

Dự án xây dựng mô hình AI để **phân tích và dự đoán giá cả thị trường nông nghiệp**, hỗ trợ nông dân và các bên liên quan đưa ra quyết định kinh doanh hiệu quả hơn.

## 📁 Cấu trúc dự án

```
TDTNTT_BaiTapNhom/
│
├── docs/                           # Tài liệu & báo cáo
│   ├── slides/                     # Slide thuyết trình (PPT/PDF)
│   ├── report/                     # Báo cáo Word/PDF
│   └── references/                 # Tài liệu tham khảo, papers
│
├── data/                           # Dữ liệu
│   ├── raw/                        # Dữ liệu thô (crawl về, chưa xử lý)
│   ├── processed/                  # Dữ liệu đã clean & xử lý
│   │   ├── train/                  # Dữ liệu huấn luyện (~70-80%)
│   │   ├── test/                   # Dữ liệu kiểm thử (~10-15%)
│   │   └── validation/             # Dữ liệu validation (~10-15%)
│   └── external/                   # Dữ liệu từ nguồn bên ngoài
│
├── crawler/                        # Code crawl dữ liệu giá nông sản
│
├── notebooks/                      # Jupyter Notebooks (EDA, thử nghiệm)
│
├── model/                          # AI/ML Model
│   ├── training/                   # Code huấn luyện model
│   ├── evaluation/                 # Code đánh giá model
│   └── saved/                      # Model đã train (weights, pkl, h5...)
│
├── backend/                        # Backend API (Python)
│   ├── main.py                     # Entry point
│   ├── api/                        # Route definitions
│   ├── services/                   # Business logic
│   └── config/                     # Cấu hình
│
├── frontend/                       # Frontend đơn giản
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
│
├── requirements.txt                # Python dependencies
└── README.md                       # File này
```