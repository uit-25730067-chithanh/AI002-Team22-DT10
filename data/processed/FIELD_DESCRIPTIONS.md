# Mô tả các field trong dữ liệu processed

Tài liệu này mô tả ý nghĩa các cột trong các file CSV tại `data/processed/weekly` và `data/processed/monthly`.

Các file trong hai thư mục này có cùng schema. Khác biệt chính là mức tổng hợp thời gian:

- `weekly`: dữ liệu được tổng hợp theo tuần.
- `monthly`: dữ liệu được tổng hợp theo tháng.
- `coffee_environment_all_areas_<freq>_2022_2025.csv`: chứa tất cả khu vực.
- `coffee_environment_<area>_<freq>_2022_2025.csv`: chỉ chứa dữ liệu của một khu vực cụ thể.

## Danh sách field

| Field | Kiểu dữ liệu | Đơn vị / giá trị | Ý nghĩa |
|---|---|---|---|
| `period_start` | Date | `YYYY-MM-DD` | Ngày bắt đầu của kỳ dữ liệu. Với file tuần là ngày bắt đầu tuần; với file tháng là ngày đầu tháng. |
| `period_end` | Date | `YYYY-MM-DD` | Ngày kết thúc của kỳ dữ liệu. Với file tuần là ngày kết thúc tuần; với file tháng là ngày cuối tháng. |
| `province` | Text | Tên tỉnh | Tỉnh nơi khu vực cà phê được ghi nhận, ví dụ `Dak Lak`, `Lam Dong`, `Gia Lai`. |
| `area` | Text | Tên khu vực | Khu vực/thị trường địa phương được theo dõi, ví dụ `Buon Ho`, `Cu M'gar`, `Bao Loc`. |
| `coffee_type` | Text | Loại cà phê | Loại cà phê của chuỗi giá. Hiện dữ liệu mặc định là `Robusta / ca phe nhan xo noi dia`. |
| `avg_price_vnd_per_kg` | Number / nullable | VND/kg | Giá cà phê trung bình trong kỳ, tính theo đồng Việt Nam trên mỗi kg. Giá trị được làm tròn đến số nguyên. Có thể trống nếu không có dữ liệu giá tương ứng cho kỳ đó. |
| `avg_temperature_c` | Number | Độ C | Nhiệt độ trung bình trong kỳ tại khu vực. Được tính từ dữ liệu thời tiết ngày và làm tròn 3 chữ số thập phân. |
| `avg_humidity_percent` | Number | % | Độ ẩm không khí trung bình trong kỳ tại khu vực. Được tính từ dữ liệu thời tiết ngày và làm tròn 3 chữ số thập phân. |
| `total_rainfall_mm` | Number | mm | Tổng lượng mưa trong kỳ tại khu vực. Với file tuần là tổng mưa trong tuần; với file tháng là tổng mưa trong tháng. |
| `avg_soil_moisture_0_7cm` | Number | m³/m³ | Độ ẩm đất trung bình ở lớp đất 0-7 cm trong kỳ. Đây là giá trị trung bình từ dữ liệu ngày và làm tròn 3 chữ số thập phân. |
| `dominant_soil_type` | Text | Loại đất | Nhóm đất chủ đạo của khu vực, ví dụ `Dat do bazan`, `Dat do vang tren bazan`. Đây là đặc trưng tĩnh theo khu vực, không thay đổi theo ngày/tuần/tháng. |
| `soil_score` | Integer | 1-5 | Điểm đánh giá mức độ phù hợp của đất với cây cà phê. Điểm càng cao nghĩa là điều kiện đất càng phù hợp. |
| `soil_data_confidence` | Text | `low`, `medium`, `high` | Mức độ tin cậy của thông tin đất theo khu vực. `high` là có bằng chứng cụ thể hơn; `low` thường là thông tin tổng quát cấp vùng/tỉnh hoặc thiếu nguồn chi tiết cấp huyện. |

## Diễn giải `soil_score`

| `soil_score` | Ý nghĩa |
|---:|---|
| 5 | Rất phù hợp với cà phê; thường là đất đỏ bazan hoặc nhóm đất liên quan chặt với vùng cà phê. |
| 4 | Phù hợp; thường là đất bazan hoặc đất đỏ vàng, nhưng bằng chứng có thể ở mức tổng quát theo khu vực. |
| 3 | Trung bình; vẫn có thể trồng cà phê nhưng không phải nhóm đất ưu tiên nhất. |
| 2 | Mức phù hợp thấp; có thể gặp hạn chế về độ dốc, thoái hóa, dinh dưỡng hoặc nước. |
| 1 | Không rõ hoặc không phù hợp; thiếu bằng chứng đáng tin cậy hoặc khu vực không nổi bật về cà phê. |

## Ghi chú sử dụng

- Các field thời tiết và độ ẩm đất là biến thay đổi theo thời gian.
- Các field `dominant_soil_type`, `soil_score`, `soil_data_confidence` là biến tĩnh theo khu vực.
