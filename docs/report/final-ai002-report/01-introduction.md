# CHƯƠNG 1: GIỚI THIỆU ĐỀ TÀI

## 1.1. Bối cảnh thực tiễn và Vấn đề

Ngành cà phê là một trong những ngành nông nghiệp xuất khẩu chủ lực của Việt Nam, đóng vai trò kinh tế chiến lược đối với quốc gia nói chung và khu vực Tây Nguyên nói riêng. Các tỉnh Tây Nguyên (bao gồm Đắk Lắk, Gia Lai, Đắk Nông, Lâm Đồng và Kon Tum) chiếm phần lớn diện tích canh tác và sản lượng cà phê Robusta cả nước. Tuy nhiên, chuỗi giá trị ngành hàng này hiện đối mặt với hai thách thức lớn:
1. **Biến đổi khí hậu cực đoan:** Thời tiết tại Tây Nguyên ngày càng biến động thất thường, gây ảnh hưởng trực tiếp đến năng suất, chất lượng hạt và dịch bệnh cây trồng. Các yếu tố như nhiệt độ trung bình tăng, lượng mưa phân bổ không đều và độ ẩm đất suy giảm đe dọa trực tiếp đến tính bền vững của các nông hộ.
2. **Biến động thị trường nông sản:** Giá cà phê trong nước phụ thuộc lớn vào giá sàn thế giới (London) và chịu ảnh hưởng từ các yếu tố cung cầu toàn cầu. Việc thiếu kênh thông tin khách quan, tin cậy khiến người nông dân nhỏ lẻ dễ bị thương lái ép giá, hoặc đưa ra các quyết định canh tác, thu hoạch và bán hàng cảm tính, dẫn đến rủi ro tài chính cao.

Hiện nay, mặc dù các công nghệ phân tích dữ liệu và Trí tuệ Nhân tạo (AI) đã phát triển mạnh mẽ, việc ứng dụng các giải pháp này đến tay người nông dân vẫn còn rất hạn chế. Phần lớn các mô hình dự báo hiện đại hoạt động như một "hộp đen" (Blackbox) phức tạp, thiếu tính minh bạch (Transparency) và không chú trọng đến khả năng chống chịu lỗi dữ liệu thực địa (Robustness). Do đó, việc xây dựng một hệ thống AI hỗ trợ dự báo giá và lập kế hoạch canh tác dựa trên các nguyên tắc thiết kế bền vững là vô cùng cần thiết.

## 1.2. Mục tiêu của đề tài

Đề tài hướng đến thiết kế và hiện thực hóa một hệ thống AI đồng hành cùng người nông dân trong việc theo dõi thị trường giá cả và điều chỉnh kế hoạch canh tác theo điều kiện khí hậu địa phương. Các mục tiêu cụ thể gồm:
- **Xây dựng Data Pipeline tự động:** Thu thập dữ liệu lịch sử giá cà phê Robusta và các thông số thời tiết thực địa theo vùng tại 5 tỉnh Tây Nguyên.
- **Huấn luyện mô hình học máy Baseline:** Áp dụng mô hình học máy truyền thống Random Forest Regression có tính giải thích cao để dự báo xu hướng biến động giá.
- **Thiết kế Kiến trúc AI Bền vững:** Hiện thực hóa hệ thống tuân thủ 5 Trụ cột AI có trách nhiệm (Reliability, Bias, Robustness, Social Impact, Transparency), đặt lợi ích của người nông dân ở vị trí trung tâm.
- **Triển khai ứng dụng thực tế:** Xây dựng API backend đáp ứng tốc độ phản hồi nhanh và một giao diện người dùng tối giản, thân thiện với thiết bị di động (Mobile-first UI).

## 1.3. Phạm vi và Giới hạn (Disclaimers)

Để đảm bảo kỳ vọng thực tế cho người dùng cuối và đánh giá chính xác năng lực hệ thống, đồ án xác lập các giới hạn nghiên cứu sau:
- **Phạm vi địa lý:** Dữ liệu chỉ tập trung phân tích tại 5 tỉnh trọng điểm Tây Nguyên bao gồm Đắk Lắk, Gia Lai, Đắk Nông, Lâm Đồng và Kon Tum trong giai đoạn từ năm 2022 đến 2025.
- **Đặc trưng đầu vào:** Mô hình dự báo dựa vào các chỉ số khí tượng cơ bản (nhiệt độ, lượng mưa, độ ẩm) kết hợp các đặc trưng tự tương quan thời gian (lag, rolling average price). Mô hình chưa tích hợp các biến vĩ mô khác như giá phân bón, chi phí nhân công, sâu bệnh hay chính sách xuất khẩu.
- **Tuyên bố miễn trừ trách nhiệm (Disclaimer):** Kết quả dự báo và các khuyến nghị canh tác của hệ thống chỉ mang tính chất tham khảo cho học tập và nghiên cứu thực nghiệm. Hệ thống không đưa ra lời khuyên giao dịch tài chính hay tư vấn nông nghiệp pháp lý chính thức. Người nông dân cần tự đối chiếu với giá sàn thương lái tại địa phương và tình hình đất đai thực địa.

## 1.4. Phương pháp thực hiện

Quy trình thực hiện đề tài áp dụng mô hình phát triển Agile kết hợp với quy trình phát triển AI Bền vững qua các bước:
1. **Thu thập và Làm sạch dữ liệu:** Xây dựng Crawler tự động cào giá cà phê hàng ngày và đồng bộ dữ liệu thời tiết theo tháng.
2. **Phân tích dữ liệu khám phá (EDA):** Phân tích tương quan giữa các yếu tố thời tiết và giá cà phê, đánh giá độ phủ dữ liệu thực tế tại từng địa phương.
3. **Kỹ thuật Đặc trưng (Feature Engineering):** Xây dựng các biến trễ (Lag 1 tháng), trung bình trượt (rolling mean 3 tháng) và biến đổi chu kỳ tháng (sin/cos month) để mô hình nắm bắt tính mùa vụ.
4. **Huấn luyện và Đánh giá:** Phân chia tập dữ liệu theo thời gian (Temporal Split) để tránh rò rỉ dữ liệu tương lai. Huấn luyện Random Forest Regression và đánh giá thông qua MAE, RMSE, R².
5. **Hiện thực hóa lớp bảo vệ:** Viết code xử lý ngoại lệ đầu vào cảm biến khí tượng cực đoan (Robustness) và thiết lập cấu hình Prompt an toàn chống bẻ lái ngôn ngữ (Reliability).
6. **Xây dựng API Backend & UI Demo:** Triển khai API bằng FastAPI và thiết kế giao diện demo mobile-first phục vụ nông dân.
