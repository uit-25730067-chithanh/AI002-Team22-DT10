# Giao diện Demo Dự báo Giá & Khuyến nghị Canh tác Cà phê (DT10)

Thư mục này chứa mã nguồn của giao diện người dùng phục vụ demo và kiểm thử hệ thống. Giao diện được thiết kế theo triết lý **Social Impact & Accessibility** để có thể chạy mượt mà ngay cả trên thiết bị di động cấu hình yếu tại vùng sâu Tây Nguyên.

## 1. Công nghệ (React + Vite)

- Được nâng cấp từ phiên bản Vanilla tĩnh ban đầu.
- **Framework:** React + TypeScript + Vite.
- **Design System:** Tailwind CSS, `lucide-react`, Neo-Brutalism thân thiện với người dùng (nút bấm lớn, tương phản cao, dễ nhìn ngoài nắng). Không còn dùng CSS Modules cho component styling.
- **Phân tách tính năng:** Cung cấp 2 luồng tính năng riêng biệt: Dự báo Giá và Khuyến nghị Canh tác, bám sát mental model của người dùng thực tế.
- **Local Storage:** Chỉ lưu kết quả khi người dùng bấm **Lưu kết quả này**, hỗ trợ xem lại offline và xem chi tiết từng kết quả (tối đa 20 kết quả).

## 2. Hướng dẫn chạy Demo

Vì sử dụng Vite, bạn cần cài đặt NodeJS và chạy bằng npm:

```bash
cd frontend
npm install
npm run dev
```

Sau đó mở trình duyệt truy cập: `http://localhost:5173` (hoặc cổng mà Vite báo).

## 3. Các bước thực hiện Demo trên UI

1. **Khởi động Backend:** Đảm bảo server uvicorn của backend đang chạy (tại cổng `8000`).

   ```bash
   uvicorn backend.main:app --reload
   ```

2. **Cấu hình API:** Mặc định frontend gọi `http://127.0.0.1:8000`.
3. **Dự báo Giá:** Vào "Dự Báo Giá Cà Phê", điền thông tin và click "Nhận Dự Báo Giá". Nhận kết quả và "Lưu kết quả này".
4. **Khuyến nghị Canh tác:** Vào "Khuyến Nghị Canh Tác", điền thời tiết dự kiến và click "Nhận Khuyến Nghị Canh Tác". Backend hiện vẫn gọi chung `/predict`, frontend chỉ lấy phần khuyến nghị canh tác để hiển thị.
5. **Lịch sử:** Xem lại các kết quả đã lưu trong tab Lịch Sử, bấm "Xem chi tiết" để xem input, kết quả, lý do và disclaimer.
6. **Kiểm tra Bias Warning:** Thử chọn tỉnh Đắk Nông, hệ thống sẽ cảnh báo về dữ liệu (do khu vực này ít dữ liệu trong tập train).
