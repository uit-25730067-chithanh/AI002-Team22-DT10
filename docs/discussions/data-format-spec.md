# Quy chuẩn Định dạng Dữ liệu (Team 2 ↔ Team 1)

**Ngày:** 2026-04-25  
**Trạng thái:** Bản nháp — chờ Team 1 xác nhận  
**Quyết định:** Dùng SQLite cho truy vấn có cấu trúc (nếu cần) + CSV cho time-series hàng ngày (KISS).

## 1. Định dạng CSV Đầu ra (Định dạng Trao đổi Chính)

Team 1 crawler xuất ra file CSV với các cột sau:

| Cột                    | Kiểu  | Mô tả                       | Ví dụ      |
| ---------------------- | ----- | --------------------------- | ---------- |
| `date`                 | date  | Ngày ghi nhận (YYYY-MM-DD)  | 2023-11-15 |
| `avg_temp_c`           | float | Nhiệt độ trung bình (°C)    | 23.5       |
| `rainfall_mm`          | float | Lượng mưa hàng ngày (mm)    | 12.0       |
| `humidity_pct`         | float | Độ ẩm tương đối (%)         | 82.0       |
| `sunshine_hours`       | float | Số giờ nắng (giờ)           | 6.5        |
| `month`                | int   | Tháng (1-12)                | 11         |
| `historical_price_vnd` | float | Giá cà phê nội địa (VND/kg) | 65000.0    |

### Ràng buộc

- **Phạm vi ngày:** Ưu tiên 2020-01-01 đến hiện tại. Tối thiểu: 2022-01-01.
- **Tần suất:** Mỗi ngày một dòng. Thiếu ngày được chấp nhận (pipeline sẽ xử lý khoảng trống).
- **Nguồn giá:** Giá bán buôn nội địa (vùng Tây Nguyên) nếu có; nếu không thì dùng chỉ báo toàn cầu kèm ghi chú chuyển đổi.

## 2. Thiên vị & Hạn chế Vùng miền (Trụ cột 2)

> **QUAN TRỌNG:** Dữ liệu huấn luyện từ vùng Tây Nguyên (Đắk Lắk, Lâm Đồng, Gia Lai, Kon Tum).  
> Khi áp dụng dự đoán cho vùng khác, response API phải kèm cảnh báo:  
> _"Dữ liệu huấn luyện từ vùng Tây Nguyên, dự đoán có thể sai lệch ở vùng khác."_

Hạn chế này được ghi nhận từ tầng dữ liệu trở lên để đảm bảo tính minh bạch.

## 3. Quyết định Lưu trữ (KISS)

- **CSV thô** (`data/raw/`): file dump nguyên bản từ Team 1, không sửa đổi.
- **CSV đã xử lý / SQLite** (`data/processed/`): dữ liệu đã làm sạch, engineer feature, dùng cho pipeline model.
- **Không dùng PostgreSQL / MySQL** — độ phức tạp không xứng đáng với phạm vi đề tài.

## 4. Tham chiếu Dữ liệu Giả lập (Mock Data)

Trong khi chờ Team 1 giao data thật, Team 2 dùng mock data để phát triển local.

| File                    | Đường dẫn                            | Push được Git?                                             | Mục đích           |
| ----------------------- | ------------------------------------ | ---------------------------------------------------------- | ------------------ |
| Full mock (1200 dòng)   | `data/raw/mock_coffee_data.csv`      | **Không** — `data/raw/` bị gitignore (chính sách file lớn) | Train & test local |
| Mẫu xem trước (50 dòng) | `data/sample/mock_coffee_sample.csv` | **Có** — Team 1 xem cấu trúc không cần chạy code           | Tham khảo nhanh    |
| Script sinh data        | `scripts/generate_mock_data.py`      | **Có** — ai cũng tái tạo được full dataset                 | Tái lập kết quả    |

**Đặc điểm mock data:**

- ~5% NaN (test khả năng xử lý missing data — Robustness)
- ~2% outliers vô lý (test độ chịu đựng của pipeline)
- Hiệu ứng mùa vụ thu hoạch (tháng 11-3 giá cao hơn)

**Team 1:** Mở `data/sample/mock_coffee_sample.csv` để xem chính xác định dạng cột mà Team 2 cần crawler xuất ra.

## 5. Bước Tiếp theo

Team 1 xác nhận lại tên cột và phạm vi ngày có thể crawl. Nhắn Zalo/Slack 5-6 dòng là đủ — không cần viết tài liệu dài dòng.
