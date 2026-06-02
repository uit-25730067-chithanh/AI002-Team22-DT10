# Báo cáo cuối kỳ AI002 - Đề tài DT10 (AI Coffee Farming)

Thư mục này chứa toàn bộ nội dung báo cáo cuối kỳ của đề tài DT10: **AI dự báo canh tác & giá cà phê cho nông dân Tây Nguyên**. Báo cáo được cấu trúc thành các tệp Markdown riêng biệt tương ứng với từng chương để dễ quản lý, soạn thảo và review.

---

## 1. Trạng thái các Chương (Status Table)

| Chương | Nội dung chính | File | Owner | Trạng thái |
| :--- | :--- | :--- | :--- | :--- |
| **Bìa & Đóng góp** | Trang bìa, thông tin thành viên, bảng phân công nhiệm vụ | [00-cover-and-metadata.md](00-cover-and-metadata.md) | Nhóm trưởng | Pending |
| **Chương 1** | Giới thiệu đề tài, bối cảnh thực tiễn, mục tiêu, phạm vi và giới hạn | [01-introduction.md](01-introduction.md) | Phúc / Thịnh | Pending |
| **Chương 2** | Cơ sở lý thuyết: Học có giám sát, Random Forest Regressor, các độ đo MAE/RMSE/R², Responsible AI | [02-theoretical-background.md](02-theoretical-background.md) | Thịnh / Thanh | Pending |
| **Chương 3** | Dữ liệu & Thiết kế: Nguồn dữ liệu, Tiền xử lý, Kiến trúc 4 tầng Responsible AI, Explainability Engine | [03-data-and-design.md](03-data-and-design.md) | Thanh / Sơn | Completed |
| **Chương 4** | Hiện thực hóa: Feature engineering, API validation, category guard, contract backend và định hướng tích hợp frontend | [04-implementation.md](04-implementation.md) | Thanh / Phúc | Completed |
| **Chương 5** | Thực nghiệm & Đánh giá: Thiết lập split temporal, kết quả metrics thật trên tập Test 2025, Kịch bản test 5 trục | [05-experiments-and-evaluation.md](05-experiments-and-evaluation.md) | Sơn / Thanh | Completed |
| **Chương 6** | Kết luận đạt được, hạn chế mô hình và định hướng phát triển tương lai | [06-conclusion-and-future-work.md](06-conclusion-and-future-work.md) | Sơn / Phúc | Completed |
| **Phụ lục** | Tài liệu tham khảo, API Request/Response mẫu, Link Github, Screenshots demo | [appendices.md](appendices.md) | Cả nhóm | Completed |

---

## 2. Quy ước Thuật ngữ và Viết tắt

Để đảm bảo tính nhất quán của báo cáo học thuật, các thuật ngữ sau đây được quy định như sau:

- **Ngôn ngữ chính:** Tiếng Việt.
- **Giữ nguyên thuật ngữ tiếng Anh đối với:**
  - Tên mô hình: `Random Forest`, `XGBoost`.
  - Các kỹ thuật: `feature engineering`, `one-hot encoding`, `temporal split` (phân chia dữ liệu theo thời gian), `data leakage` (rò rỉ dữ liệu), `outliers` (ngoại lai).
  - Tên các độ đo: `MAE`, `RMSE`, `R-squared` / `R²`.
  - Công nghệ backend: `FastAPI`, `Pydantic`, `Uvicorn`, `endpoints`.
  - 5 Trụ cột AI Bền vững: `Reliability` (Tính tin cậy), `Bias` (Tính thiên vị/không thiên vị), `Robustness` (Kháng nhiễu), `Social Impact` (Tác động xã hội), `Explainability` / `Transparency` (Tính minh bạch/giải thích được).
- **LaTeX Format:** Các công thức toán học phải được viết đúng định dạng LaTeX. Ví dụ:
  - MAE: $$MAE = \frac{1}{n} \sum_{i=1}^{n} |y_{i} - \hat{y}_{i}|$$
  - RMSE: $$RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_{i} - \hat{y}_{i})^2}$$
  - R²: $$R^2 = 1 - \frac{\sum (y_{i} - \hat{y}_{i})^2}{\sum (y_{i} - \bar{y})^2}$$

---

## 3. Cách biên dịch báo cáo (Word / PDF)

1. **Markdown Review:** Các thành viên review trực tiếp trên Github hoặc VS Code.
2. **Convert sang DOCX:** Sử dụng lệnh `pandoc` hoặc import vào Word khi nội dung Markdown đã được chốt 100%.
