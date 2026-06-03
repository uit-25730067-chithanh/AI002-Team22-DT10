# CHƯƠNG 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

## 6.1. Kết quả đạt được và Bài học

Đồ án đã hiện thực hóa thành công hệ thống **AI dự báo kế hoạch canh tác và giá cà phê cho nông dân Tây Nguyên (DT10)** đáp ứng đầy đủ các tiêu chuẩn kỹ thuật cốt lõi và tích hợp thành công tư duy thiết kế hệ thống AI bền vững.

### Các kết quả nổi bật bao gồm:
- **Data Pipeline tự động:** Đồng bộ hóa thành công dữ liệu giá cà phê thực tế cào hàng ngày từ crawler và dữ liệu khí tượng theo tháng tại 5 tỉnh Tây Nguyên giai đoạn 2022–2025.
- **Model học máy thực tế:** Huấn luyện thành công mô hình Random Forest Regressor đóng vai trò baseline chạy end-to-end, có khả năng trích xuất Feature Importance tăng tính minh bạch.
- **Backend API tin cậy:** Triển khai API bằng FastAPI, tự động validate kiểu dữ liệu đầu vào bằng Pydantic và tích hợp lớp bảo vệ API Key bảo mật.
- **Responsible AI thực chiến:** Lồng ghép thành công 5 Trụ cột AI có trách nhiệm vào mã nguồn (lọc dữ liệu cảm biến lỗi - Robustness, cảnh báo thiếu dữ liệu vùng - Bias, giao diện di động dung lượng nhẹ và hiển thị disclaimer - Social Impact).

### Bài học kinh nghiệm:
Đối với các bài toán AI ứng dụng trong đời sống xã hội thực tế (đặc biệt hỗ trợ nhóm người dùng yếu thế như nông dân nhỏ lẻ), việc chạy theo các mô hình Deep Learning quá phức tạp nhưng thiếu tính giải thích là không thực tế. Thay vào đó, việc xử lý dữ liệu sạch, đảm bảo tính kháng nhiễu cảm biến, kiểm toán thiên lệch địa lý và giải thích rõ ràng cơ chế hoạt động của mô hình là những yếu tố quyết định sự chấp nhận và tin tưởng của người dùng đối với hệ thống.

## 6.2. Hạn chế của hệ thống

Nhóm phát triển thẳng thắn nhìn nhận các hạn chế kỹ thuật hiện tại của hệ thống baseline:
1. **Giới hạn dự đoán ngoại suy (Extrapolation Limit):** Thuật toán Random Forest không thể dự báo giá trị mục tiêu vượt quá phạm vi giá trị lớn nhất trong tập huấn luyện (Train Set 2022-2024 chỉ ghi nhận giá tối đa ~78,000 VND/kg). Khi giá cà phê thực tế năm 2025 vọt lên trên 100,000 VND/kg do biến động thị trường toàn cầu, mô hình baseline bị lệch biên độ lớn, dẫn đến chỉ số R² âm.
2. **Mất cân bằng dữ liệu địa lý (Geographical Bias):** Tỷ lệ dữ liệu cào thật tại tỉnh Đắk Nông rất thấp (39.6% ở tập tháng, 21% ở tập tuần), dẫn đến các khuyến nghị tại khu vực này có sai số lớn hơn và thiếu tính công bằng so với tỉnh Lâm Đồng hay Kon Tum.
3. **Chỉ số đất đai đơn giản hóa (Soil Score Limitation):** Thuộc tính điểm số đất đai (`soil_score`) và loại đất trong mô hình mới dừng ở mức tham khảo giáo dục/minh họa, chưa phản ánh được kết quả khảo sát mẫu đất thực nghiệm thực địa của từng hộ nông dân.

## 6.3. Hướng phát triển tương lai

Để khắc phục các hạn chế trên và phát triển hệ thống thành một ứng dụng thương mại thực tế, các hướng nghiên cứu tiếp theo bao gồm:
- **Mở rộng chiều dài chuỗi dữ liệu:** Thu thập dữ liệu lịch sử giá cà phê từ trước năm 2022 (ví dụ giai đoạn 2015-2021) để mô hình có cơ hội học qua nhiều chu kỳ biến động giá lớn.
- **Thử nghiệm các mô hình có khả năng ngoại suy:** Nghiên cứu và so sánh hiệu năng của Random Forest với các thuật toán có khả năng học xu hướng tăng trưởng (như Linear Regression kết hợp trôi xu hướng, ARIMA, Prophet, XGBoost v2, hoặc mô hình mạng Nơ-ron Recurrent LSTM).
- **Mô hình hóa cục bộ (Localized Forecasting):** Huấn luyện các mô hình dự báo riêng biệt cho từng tiểu vùng khí hậu hoặc từng tỉnh để giảm thiểu sai số chênh lệch địa lý và loại bỏ bias vùng miền.
- **Tích hợp IoT thực địa:** Kết nối trực tiếp hệ thống với các trạm cảm biến IoT đo độ ẩm đất, lượng mưa tại vườn của nông dân thay vì sử dụng API thời tiết tổng hợp cấp huyện, giúp đưa ra khuyến nghị canh tác cá nhân hóa chính xác cao.
