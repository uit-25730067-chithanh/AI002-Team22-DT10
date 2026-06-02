# Inventory và Chuẩn hóa Nguồn Nội dung cho Báo cáo cuối kỳ DT10

## 1. Inventory nguồn tài liệu hiện có và Mức độ sử dụng

| Nguồn tài liệu | Nội dung chính | Mức độ sử dụng | Cách tích hợp vào báo cáo final |
| :--- | :--- | :--- | :--- |
| **Draft PDF V4** (`tmp/Bao_Cao_AI_Nong_Nghiep_4_Tinh_Tay_Nguyen_Tong_Hop_V4.docx.pdf`) | Outline thô, bối cảnh ngành cà phê, cơ sở lý thuyết RF/MAE/RMSE, kịch bản test 5 trục định tính. | Dùng lại ~60% | Giữ bối cảnh thực tiễn (Chương 1), bổ sung và chuẩn hóa công thức toán học (Chương 2), làm sạch bảng kịch bản test 5 trục (Chương 5). |
| **5 Pillars Checkpoint & Audit** (`docs/discussions/5-pillars-checkpoint.md`, `2026-05-13-real-data-audit-team2-son.md`) | Thống kê dataset thật (576 dòng monthly, 86.5% observed price), metrics RF (MAE 13.5k, RMSE 16.7k, R² -0.9044), bảng phân tích độ phủ (Lâm Đồng, Kon Tum, Đắk Lắk, Gia Lai, Đắk Nông). | Dùng lại 100% | Đưa trực tiếp vào Chương 3 (Dữ liệu & Thiết kế) và Chương 5 (Thực nghiệm & Đánh giá). |
| **API Handoff & Contract** (`docs/discussions/2026-05-13-api-handoff-team2-real-data.md`) | Request/Response schema, validation, và disclaimer mẫu. | Dùng lại 100% | Đưa vào Chương 3 (kiến trúc) và Phụ lục (Request/Response mẫu). |
| **Codebase thật** (`backend/`, `model/`) | File `preprocess.py`, `train_rf.py`, `routes.py`, `predictor.py` | Dùng lại 100% | Dùng làm minh chứng code cho Chương 4 (Hiện thực hóa) và giải thích tính Robustness (khử nhiễu). |
| **CS115 PDF chuẩn cấu trúc** | Trang bìa, TOC, List of Figures/Tables, đóng góp thành viên, cấu trúc học thuật. | Tham khảo cấu trúc | Áp dụng cấu trúc học thuật chuyên nghiệp vào final Markdown và file Word/PDF. |

---

## 2. Phần nội dung dùng lại từ V4 (Cần tinh chỉnh)
- **Giới thiệu đề tài (Bối cảnh):** Giữ nguyên phần bối cảnh trồng cà phê Tây Nguyên (Đắk Lắk, Gia Lai, Đắk Nông, Lâm Đồng).
- **Cơ sở lý thuyết:** Giữ nguyên các định nghĩa về Học có giám sát, Random Forest Regression, các độ đo MAE/RMSE/R2 nhưng cần chuẩn hóa LaTeX cho các công thức theo rule `naming-conventions.md`.
- **Kịch bản kiểm thử 5 trục:** Bảng kịch bản TC_REL_01 -> TC_EXP_05 rất tốt, cần giữ nguyên và bổ sung kết quả chạy thực tế của hệ thống.

---

## 3. Phần cần viết mới hoàn toàn
- **Tóm tắt báo cáo (Abstract):** Cần tóm tắt ngắn gọn đề tài, mô hình, kết quả metrics thực tế và định hướng 5 trục Responsible AI.
- **Phân tích dữ liệu chi tiết (Chương 3):** Thống kê số dòng (576 dòng), số cột (16 cột), giải thích chi tiết các thuộc tính dữ liệu thật (thay vì các bảng thuộc tính thô trong V4).
- **Phân tích Bias dữ liệu (Chương 3 & 5):** Thống kê độ phủ observed price theo tỉnh để minh chứng cho trục Bias (Lâm Đồng 100% vs Đắk Nông 39.6%).
- **Hiện thực hóa Robustness & Explainability (Chương 4):** Viết rõ code giải thích (`PredictorService` trích xuất `feature_importances_`) và code khử nhiễu input (`sanitize_inputs` xử lý nhiệt độ cực đoan và độ ẩm = 0).
- **Đánh giá thực nghiệm với metrics thật (Chương 5):** Cần báo cáo trung thực R² âm (-0.9044) và giải thích nguyên nhân do phân phối giá 2025 thay đổi mạnh.
- **Giao diện di động (Mobile-first) & Kịch bản demo (Chương 4 & Phụ lục):** Cần cập nhật định hướng di động cho nông dân (chụp màn hình hoặc mô tả demo).

---

## 4. Danh sách Hình ảnh / Biểu đồ / Screenshot cần có
1. **Sơ đồ luồng dữ liệu (Data-to-AI Flow):** Dựng lại bằng Mermaid hoặc vẽ sơ đồ (Chương 3).
2. **Sơ đồ kiến trúc hệ thống 4 tầng (Responsible AI Architecture):** Chương 3.
3. **Biểu đồ Feature Importance của Random Forest:** Lưu hình hoặc bảng giá trị (Chương 5).
4. **Biểu đồ so sánh giá dự báo và giá thực tế năm 2025:** Chương 5 (Reliability).
5. **Screenshot giao diện Frontend (Mobile-first):** Phụ lục (hoặc hình vẽ mô phỏng UI nếu chưa có frontend thật).

---

## 5. Câu hỏi cần chốt với các thành viên
- **Gửi Phúc & Thịnh:**
  1. Frontend đã chạy kết nối với API `/predict` chưa? Có screenshot demo thực tế trên mobile/responsive không?
  2. Chúng ta nộp báo cáo bằng định dạng Word (.docx) hay PDF (từ Word/LaTeX)?
- **Gửi Sơn:**
  1. Có cần bổ sung thêm kết quả stress test nào cho API không, hay dùng kết quả trong checklist hiện tại?
