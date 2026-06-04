# UX Brief & Hướng dẫn Tích hợp Frontend Mobile-First (Gửi Phúc & Thịnh)

**Người gửi:** Đặng Chí Thanh (Team 2)  
**Ngày gửi:** 2026-06-02  
**Mục tiêu:** Cung cấp định hướng thiết kế giao diện di động (Mobile-First) và cách tích hợp API `/predict` bảo mật cho Team 1.

---

## 1. Tại sao phải là Mobile-First?

Đối tượng người dùng cuối của đề tài DT10 là các hộ nông dân trồng cà phê nhỏ lẻ tại Tây Nguyên. Đặc thù công việc của họ là làm việc ngoài thực địa (vườn/rẫy cà phê). Do đó:
- **Thiết bị truy cập chính:** Điện thoại thông minh (smartphone) tầm trung hoặc giá rẻ.
- **Điều kiện mạng:** Sóng di động (3G/4G) yếu hoặc không ổn định tại vùng sâu, vùng xa.
- **Điều kiện sử dụng:** Ánh sáng mặt trời trực tiếp ngoài trời rẫy rất mạnh, gây lóa mắt.

**Nguyên tắc thiết kế UX:**
1. **Layout một cột (Single Column):** Toàn bộ giao diện xếp chồng theo chiều dọc, không chia cột ngang.
2. **Kích thước chạm (Touch Target):** Các nút bấm, ô nhập liệu (input) phải có chiều cao tối thiểu **48px** để dễ bấm bằng ngón tay khi đang làm việc.
3. **Cỡ chữ lớn (Min 16px):** Tiêu đề và kết quả số phải rõ ràng.
4. **Độ tương phản cao:** Sử dụng văn bản màu đen hoặc xám rất đậm trên nền trắng/sáng để dễ đọc dưới trời nắng.
5. **Kiến trúc linh hoạt:** Sử dụng React/Vite và Tailwind CSS để tách biệt logic Giá và Canh tác, đồng thời tích hợp `localStorage` để xem lại kết quả khi mạng chập chờn.

---

## 2. Luồng Giao diện Di động Tối thiểu (Minimum Viable Mobile Flow)

Quy trình trải nghiệm của người nông dân được tối giản hóa qua 3 phần trên một trang duy nhất (Single Page Application):

### Bước 1: Form Nhập thông tin (Màn hình Input)
- **Chọn địa phương:** Một ô chọn tỉnh (`province`) gồm Lâm Đồng, Đắk Lắk, Gia Lai, Kon Tum, Đắk Nông. Sau khi chọn tỉnh, ô chọn huyện (`area`) sẽ hiển thị các huyện tương ứng đã được học trong mô hình (tránh lỗi gửi sai huyện).
- **Tháng dự báo:** Mặc định là tháng hiện tại hoặc tháng tiếp theo (người dùng có thể kéo chọn 1-12).
- **Thông tin thời tiết (Tùy chọn):** Tự động điền giá trị trung bình lịch sử thông qua API thời tiết, nông dân có thể tự chỉnh sửa nhiệt độ, lượng mưa nếu muốn giả định kịch bản thời tiết cực đoan.
- **Giá cà phê gần nhất:** Nông dân nhập giá bán ngày hôm nay tại đại lý thu mua.

### Bước 2: Hiển thị Dự báo & Khuyến nghị (Màn hình Kết quả)
- **Giá dự báo:** Hiển thị số lớn nổi bật (ví dụ: **85,200 VND/kg**).
- **Khoảng tin cậy:** Hiển thị bên dưới dạng chữ nhỏ hơn: *(Dao động từ 81,400 - 89,000 VND/kg)* để nông dân hình dung biên độ biến động.
- **Hành động canh tác:** Hiển thị thẻ màu (ví dụ thẻ xanh cho "Chăm sóc sau thu hoạch", thẻ vàng cho "Tưới nước chống hạn").
- **Lý do khuyến nghị:** Một đoạn văn bản tiếng Việt ngắn gọn giải thích từ rule-engine.

### Bước 3: Giải thích & Disclaimer (Màn hình Minh bạch & An toàn)
- **Biểu đồ phần trăm ảnh hưởng (Explainability):** Dùng các thanh ngang CSS đơn giản biểu thị mức độ quan trọng:
  - Đà tăng giá thị trường: `[█████████] 72%`
  - Giá tháng trước: `[██] 22%`
  - Yếu tố thời tiết: `[] <1%`
- **Khung miễn trừ trách nhiệm (Disclaimer):** Bắt buộc hiển thị ở chân trang: *"Thông tin dự báo chỉ mang tính tham khảo. Hãy đối chiếu với đại lý thu mua địa phương trước khi quyết định bán."*

---

## 3. Hướng dẫn tích hợp API `/predict` bảo mật

Để gọi API thành công từ Frontend, Team 1 cần lưu ý cấu hình HTTP client:

### 3.1. Phương thức và URL
- **Method:** `POST`
- **Endpoint:** `/predict`
- **Tài liệu tham khảo chi tiết:** [Phụ lục 2 của báo cáo](../final-ai002-report/appendices.md#phu-luc-2-api-requestresponse-mau-json)

### 3.2. Cấu hình Headers (Bảo mật)
Do hệ thống được thiết lập cơ chế bảo mật khóa API (API Key) nhằm bảo vệ hạ tầng, frontend bắt buộc phải gửi Header `X-API-Key` kèm theo:
```http
POST /predict
Content-Type: application/json
X-API-Key: YOUR_AI002_API_KEY
```
*(Lưu ý: Không hardcode API key vào mã nguồn Javascript public; hãy lấy từ cấu hình môi trường hoặc cấu hình proxy backend nếu deploy).*

### 3.3. Xử lý lỗi `422 Unprocessable Entity`
Khi nông dân nhập một huyện hoặc thuộc tính ngoài danh mục đã học của mô hình Random Forest, API sẽ trả về lỗi `422`. Frontend cần bắt lỗi này và hiển thị thông báo thân thiện:
- Ví dụ: *"Huyện Đắk R'lấp hiện chưa có đủ dữ liệu giá. Xin vui lòng chọn Ea H'leo hoặc Di Linh để xem dự báo đại diện."*
