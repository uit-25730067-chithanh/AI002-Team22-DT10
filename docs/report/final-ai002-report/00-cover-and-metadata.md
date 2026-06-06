# TRANG BÌA & THÔNG TIN ĐÓNG GÓP

## ĐẠI HỌC QUỐC GIA THÀNH PHỐ HỒ CHÍ MINH
### TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN
### KHOA KHOA HỌC MÁY TÍNH

---

# ĐỒ ÁN MÔN HỌC
## MÔN: TƯ DUY TRÍ TUỆ NHÂN TẠO (AI002)

## ĐỀ TÀI: AI DỰ BÁO KẾ HOẠCH CANH TÁC MÙA VỤ VÀ GIÁ CÀ PHÊ CHO NÔNG DÂN
### MÃ ĐỀ TÀI: DT10

**Giảng viên hướng dẫn:** TS. Phan Thế Duy  
**Lớp:** AI002.F21.CN1.TTNT  

---

## Danh sách thành viên và Bảng phân công đóng góp

| STT | Mã Sinh Viên | Họ và Tên | Nhiệm Vụ Phân Công (Chi tiết Kỹ thuật & Trục AI) | Hoàn Thành (%) |
| :-- | :----------- | :-------- | :------------------------------------------------ | :-------------- |
| 1   | 25730067     | Đặng Chí Thanh (Trưởng nhóm) | Kỹ thuật ML (Feature Engineering, Preprocessing, Train RF Baseline), Viết Backend API (FastAPI), Xây dựng Web UI (Frontend) và liên kết API với UI. Phụ trách trục Reliability, Explainability và Social Impact. | 100%            |
| 2   | 25730061     | Hoàng Cao Sơn | Đánh giá và kiểm toán dữ liệu (Real Data Audit), Thu thập dữ liệu lịch sử giá & thời tiết (Crawler), Viết kịch bản stress test cho API, Phụ trách trục Robustness và Bias. | 100%            |

---

## Tóm tắt báo cáo (Abstract)

Đề tài **DT10: AI dự báo kế hoạch canh tác mùa vụ và giá cà phê cho nông dân** được phát triển nhằm hỗ trợ các hộ nông dân trồng cà phê tại khu vực Tây Nguyên (Đắk Lắk, Gia Lai, Đắk Nông, Lâm Đồng, Kon Tum) đưa ra các quyết định canh tác và kinh doanh dựa trên dữ liệu. Trọng tâm của đồ án là việc hiện thực hóa và đánh giá hệ thống dựa trên **5 Trụ cột của AI Bền vững (Responsible AI)** bao gồm: Tính tin cậy (Reliability), Tính không thiên vị (Bias), Kháng nhiễu (Robustness), Tác động xã hội (Social Impact), và Tính minh bạch/giải thích được (Explainability).

Về mặt kỹ thuật, hệ thống sử dụng thuật toán **Random Forest Regressor** để dự báo giá cà phê dựa trên dữ liệu giá lịch sử cùng các đặc trưng khí tượng (nhiệt độ, lượng mưa, độ ẩm). Dữ liệu được thu thập định kỳ theo tháng (monthly) từ năm 2022 đến 2025. Mô hình được huấn luyện trên dữ liệu giai đoạn 2022–2024 và đánh giá độc lập trên dữ liệu năm 2025 (phân chia theo chuỗi thời gian - temporal split). Kết quả thực nghiệm cho thấy mô hình baseline đạt sai số tuyệt đối trung bình (MAE) là **13,552 VND/kg**, sai số bình phương trung bình dạng căn (RMSE) là **16,754 VND/kg**.

Nhằm đảm bảo tính bền vững và thực tế, hệ thống tích hợp lớp lọc khử nhiễu dữ liệu cảm biến lỗi (nhiệt độ cực đoan hoặc độ ẩm mất dữ liệu đột ngột), cảnh báo thiên lệch dữ liệu địa lý giữa các tỉnh (độ phủ Lâm Đồng 100% so với Đắk Nông 39.6%), xây dựng cấu hình hệ thống nhắc nhở (Prompt Guardrails) an toàn chống bẻ lái ngôn ngữ, và cung cấp khả năng bóc tách mức độ đóng góp đặc trưng (Feature Importance) giúp người nông dân dễ dàng đối chiếu lý do đưa ra dự báo. Hệ thống backend được xây dựng bằng **FastAPI** và bàn giao thông tin đầu ra chi tiết cho lớp giao diện di động (Mobile-first UI), giúp người dùng cuối tiếp cận dữ liệu một cách trực quan, tối ưu và bình đẳng.
