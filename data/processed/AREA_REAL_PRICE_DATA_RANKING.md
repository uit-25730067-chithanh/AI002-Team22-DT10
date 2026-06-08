# Area Real Price Data Ranking

File này tổng hợp độ phủ dữ liệu giá cà phê quan sát thật theo từng khu vực/tỉnh trong dataset chính thức 2020-2026.

## Tổng quan dataset

- Weekly processed rows: **3,972** dòng.
- Monthly processed rows: **912** dòng.
- Monthly observed rows: **711/912** dòng (**77.96%**).
- `avg_price_vnd_per_kg` đã được fill đủ để train baseline.
- `observed_price_vnd_per_kg` là giá quan sát thật; nếu trống thì `avg_price_vnd_per_kg` là proxy/interpolation.

## Monthly province coverage

| Province | Coverage | Đánh giá |
|---|---:|---|
| Kon Tum | 88.16% | Mạnh nhất |
| Lâm Đồng | 86.84% | Tốt |
| Đắk Lắk | 77.63% | Trung bình khá |
| Gia Lai | 77.63% | Trung bình khá |
| Đắk Nông | 60.53% | Cần cảnh báo |

## Ranking khu vực theo dữ liệu thật

| Rank | Province | Area | Monthly coverage | Ghi chú |
|---:|---|---|---:|---|
| 1 | Kon Tum | Kon Tum | 88.16% | Mạnh nhất |
| 2 | Lâm Đồng | Di Linh | 86.84% | Phù hợp demo |
| 3 | Lâm Đồng | Bảo Lộc | 86.84% | Phù hợp demo |
| 4 | Lâm Đồng | Lâm Hà | 86.84% | Phù hợp demo |
| 5 | Đắk Lắk | Buôn Hồ | 86.84% | Phù hợp demo |
| 6 | Đắk Lắk | Ea H'leo | 86.84% | Phù hợp demo |
| 7 | Gia Lai | Pleiku | 86.84% | Phù hợp demo |
| 8 | Gia Lai | Ia Grai | 86.84% | Phù hợp demo |
| 9 | Đắk Nông | Đắk R'lấp | 61.84% | Cần cảnh báo |
| 10 | Đắk Lắk | Cư M'gar | 59.21% | Cần cảnh báo |
| 11 | Đắk Nông | Gia Nghĩa | 59.21% | Cần cảnh báo |
| 12 | Gia Lai | Chư Prông | 59.21% | Cần cảnh báo |

## Khuyến nghị chọn province/khu vực

- Nếu cần demo vùng có dữ liệu tốt, chọn **Kon Tum**, **Di Linh**, **Bảo Lộc**, **Lâm Hà**, **Ea H'leo**, **Buôn Hồ**, **Pleiku**, hoặc **Ia Grai**.
- Cần cảnh báo khi demo **Đắk R'lấp**, **Cư M'gar**, **Gia Nghĩa**, hoặc **Chư Prông** vì tỷ lệ proxy/nội suy cao hơn.
- Monthly là lựa chọn ổn định hơn weekly vì giảm nhiễu ngắn hạn và dễ giải thích trong báo cáo.

## File liên quan

- `data/raw/coffee_price_all_areas_daily_2020_2026.csv`: dữ liệu giá public-source dạng daily.
- `data/processed/weekly/coffee_environment_all_areas_weekly_2020_2026.csv`: dataset weekly đã merge môi trường, thổ nhưỡng và giá.
- `data/processed/monthly/coffee_environment_all_areas_monthly_2020_2026.csv`: dataset monthly đã merge môi trường, thổ nhưỡng và giá.
- `data/processed/area_real_price_data_ranking.csv`: bảng ranking dạng CSV.
