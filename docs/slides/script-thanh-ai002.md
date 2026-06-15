# SCRIPT THUYẾT TRÌNH - Đặng Chí Thanh (AI002)

**Đề tài:** AI Dự báo Kế hoạch Canh tác Mùa vụ & Giá Cà phê cho Nông dân Tây Nguyên
**Tổng thời gian dự kiến:** ~5 phút

---

## MỞ ĐẦU & GIỚI THIỆU (SLIDE 1, 1.1, 1.2)

Dạ em xin chào thầy Phan Thế Duy cùng tất cả các bạn.

Hôm nay, nhóm 22 chúng em xin phép trình bày về đề tài: _"AI Hỗ trợ Canh tác và Dự báo Giá Cà phê cho nông dân vùng Tây Nguyên"_.

Nhóm em gồm có hai thành viên. Em là Thanh, trưởng nhóm, đảm nhận phần xây dựng mô hình Machine Learning, viết Backend API, thiết kế Web UI, cũng như phụ trách 3 trụ cột Bền vững là: Độ tin cậy (Reliability), Tính minh bạch (Transparency) và Tác động Xã hội (Social Impact).

Còn anh Sơn sẽ phụ trách đánh giá dữ liệu, xây dựng hệ thống crawler tự động, thiết lập stress test, và đảm nhận 2 trụ cột là: Tính kháng nhiễu (Robustness) và Tính thiên lệch (Bias).

Và để bắt đầu, em xin đi thẳng vào bối cảnh, lý do vì sao nhóm lại chọn bài toán này.

---

## BỐI CẢNH & VẤN ĐỀ (SLIDE 4)

Nhìn vào bối cảnh thực tế ở Tây Nguyên, năng suất cà phê đang bị ảnh hưởng rất nặng bởi biến đổi khí hậu. Cụ thể là nhiệt độ thì ngày càng tăng, còn lượng mưa lại cực kỳ thất thường.

Nhưng cái khó nhất của người nông dân không chỉ nằm ở thời tiết, mà là sự bất đối xứng về thông tin thị trường. Nông dân thường thiếu những dữ liệu khách quan, dẫn tới việc rất dễ bị thương lái ép giá. Hầu hết các quyết định như khi nào thu hoạch, khi nào xuất bán... đa phần chỉ dựa dẫm vào cảm tính hoặc kinh nghiệm truyền thống.

Từ nỗi đau thực tế đó, nhóm em đã đặt ra mục tiêu cho dự án này.

---

## MỤC TIÊU & PHẠM VI (SLIDE 5)

Mục tiêu cốt lõi của nhóm là tạo ra một công cụ giúp người nông dân dự báo giá và nhận được các khuyến nghị canh tác hợp lý.

Tuy nhiên, định hướng thiết kế mà nhóm muốn nhấn mạnh là không chỉ làm ra một con AI chạy được, mà phải là một **AI Bền vững** – tức là được hiện thực hóa dựa trên 5 trụ cột của Responsible AI.

Phạm vi của hệ thống hiện tại bao phủ 5 tỉnh Tây Nguyên, với dữ liệu từ năm 2020 đến 2026. Ở đây nhóm em cũng xin có một **tuyên bố miễn trừ trách nhiệm** rõ ràng ngay từ đầu: hệ thống này mang tính chất tham khảo học thuật, hoàn toàn không thay thế cho các quyết định thương mại hay tư vấn chuyên môn.

---

## QUY TRÌNH XỬ LÝ DỮ LIỆU (SLIDE 6)

Về phần quy trình dữ liệu, nhóm đi theo đúng nguyên lý KISS: giữ mọi thứ thật đơn giản, nhẹ nhàng và tối ưu tài nguyên.

Thay vì ôm đồm dữ liệu theo từng ngày với rất nhiều biến động giá ảo do nhiễu, nhóm em đã tổng hợp từ dữ liệu thô hàng ngày, gộp thành tuần, rồi chốt lại ở mức **dữ liệu tháng** làm baseline.

Cách làm này không chỉ giảm nhiễu hiệu quả, mà còn giúp tập dữ liệu ăn khớp hoàn hảo với chu kỳ sinh trưởng của cây cà phê và chu kỳ thời tiết. Và với tập dữ liệu tháng này, nhóm em đạt được độ phủ quan sát thực tế lên tới gần 78%.

---

## KIẾN TRÚC HỆ THỐNG (SLIDE 7)

Từ nền tảng dữ liệu đó, nhóm em đã xây dựng một hệ thống end-to-end hoàn chỉnh với 4 tầng kiến trúc.

Dưới cùng là **Data Layer** với các công cụ crawler chạy tự động để thu thập giá và thời tiết.
Tầng thứ 2 là **Filtering Layer**, chuyên lo việc làm sạch dữ liệu, nội suy các điểm thiếu và khử lỗi từ các cảm biến.
Lên tới tầng 3 là **AI Core Layer**, nơi mô hình Random Forest hoạt động bên trong FastAPI, được bảo vệ bởi các Pydantic Guard.
Và tầng trên cùng là **Presentation Layer**, cung cấp một giao diện Mobile UI tối ưu hóa trực tiếp cho thiết bị di động của người nông dân.

---

## PHƯƠNG PHÁP KỸ THUẬT (SLIDE 8)

Đi sâu hơn một chút vào kỹ thuật của mô hình AI, nhóm em chọn thuật toán Random Forest Regression.

Điểm quan trọng nhất ở đây là kỹ thuật xử lý đặc trưng. Thứ nhất, để máy hiểu được tính lặp lại của các tháng trong năm – ví dụ khoảng cách giữa tháng 12 và tháng 1 cũng giống như tháng 1 và tháng 2 – nhóm em áp dụng **Cyclic Encoding** thông qua hàm Sin/Cos.

Thứ hai, để giúp AI hiểu được đà giá, nhóm sử dụng các đặc trưng trễ (Area-based Lags) nhưng được cô lập tính toán theo từng huyện. Việc này nhằm mục đích cốt lõi là ngăn chặn triệt để tình trạng rò rỉ dữ liệu (Data Leakage) chéo giữa các vùng địa lý khác nhau.

---

## KẾT QUẢ ĐỊNH LƯỢNG & GIỚI HẠN (SLIDE 9)

Sau khi huấn luyện, câu hỏi quan trọng nhất là: Khi chạy thực tế trên tập dữ liệu của năm 2025 thì kết quả ra sao?

Kết quả định lượng cho thấy sai số tuyệt đối trung bình (MAE) rơi vào khoảng hơn 14 ngàn đồng một ký, và sai số trung bình bình phương (RMSE) khoảng gần 18 ngàn đồng.

Nhưng nếu mọi người nhìn lên slide, mọi người sẽ thấy chỉ số R bình phương (R²) của mô hình bị âm (cụ thể là -1.22). Tại sao lại như vậy? Thay vì che giấu, nhóm em quyết định báo cáo con số này một cách trung thực nhất để thể hiện đúng nguyên tắc Minh bạch (Transparency) của AI.

> **Chú thích học thuật cho Thanh:**
> - **MAE (Mean Absolute Error - Sai số tuyệt đối trung bình):** Hiểu đơn giản là mức lệch trung bình giữa giá mô hình dự báo và giá thật. Đoán lệch trung bình khoảng 14k/kg.
> - **RMSE (Root Mean Squared Error - Sai số căn trung bình bình phương):** Chỉ số đo lường sai số mà trong đó các lỗi dự báo lệch lớn sẽ bị phạt nặng hơn.

Nguyên nhân R² âm là do nhóm đã đối mặt với một sự kiện "Thiên nga đen" (Black Swan). Tập dữ liệu huấn luyện từ 2020 đến 2024 xoay quanh mức giá khá thấp. Tuy nhiên, bước sang năm 2025, giá cà phê thực tế bùng nổ dữ dội, có những lúc đạt hơn 131 ngàn đồng/kg.

Bản chất của mô hình cây quyết định (Decision Tree/Random Forest) có một giới hạn gọi là Giới hạn Ngoại suy (Extrapolation Limit). Nó không thể dự báo ra những con số vượt quá mức trần dữ liệu mà nó từng học. Do đó, các dự báo của mô hình trong năm 2025 liên tục bị kéo về mức trung bình của quá khứ, gây ra sai số lớn và làm R² bị âm.

Và chính từ sự kiện sốc giá cực đoan này, chúng ta nhận ra rằng: một hệ thống AI thực tế không thể chỉ dựa vào một con số dự báo tĩnh, mà nó cần phải có khả năng kháng nhiễu và các rào chắn bảo vệ.

Đó cũng là sự chuyển giao qua nửa sau của hệ thống. Ngay bây giờ, em xin nhường lời lại cho anh Sơn, để anh Sơn trình bày về cách hệ thống xử lý các cú sốc (Robustness) và đảm bảo tính công bằng (Bias). Xin mời anh Sơn.

---
