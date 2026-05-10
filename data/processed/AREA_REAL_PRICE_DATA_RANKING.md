# Area Real Price Data Ranking

File này tổng hợp lượng dữ liệu giá cà phê **crawl thật** theo từng khu vực/tỉnh trong giai đoạn 2022-2025, để chọn khu vực phù hợp nhất cho phân tích và train mô hình.

## Tổng quan dataset

- Raw price rows: **5,731** dòng giá crawl thật.
- Weekly processed rows: **2,520** dòng, trong đó **1,831** dòng có giá thật ở cấp khu vực (**72.7%**).
- Monthly processed rows: **576** dòng, trong đó **498** dòng có giá thật ở cấp khu vực (**86.5%**).
- `avg_price_vnd_per_kg` đã được fill đủ để train thử nghiệm.
- `observed_price_vnd_per_kg` mới là giá crawl thật; nếu trống thì giá ở `avg_price_vnd_per_kg` là proxy/interpolation.

## Độ phủ theo tỉnh

Một tỉnh được tính là có giá thật trong kỳ nếu **ít nhất một khu vực thuộc tỉnh đó** có `observed_price_vnd_per_kg`.

### Weekly province coverage

| Province | Observed weeks | Total weeks | Coverage | Đạt >75%? |
|---|---:|---:|---:|---|
| Gia Lai | 198 | 210 | 94.3% | Có |
| Lâm Đồng | 198 | 210 | 94.3% | Có |
| Đắk Lắk | 197 | 210 | 93.8% | Có |
| Kon Tum | 194 | 210 | 92.4% | Có |
| Đắk Nông | 88 | 210 | 41.9% | Không |

### Monthly province coverage

| Province | Observed months | Total months | Coverage | Đạt >90%? |
|---|---:|---:|---:|---|
| Đắk Lắk | 48 | 48 | 100.0% | Có |
| Gia Lai | 48 | 48 | 100.0% | Có |
| Kon Tum | 48 | 48 | 100.0% | Có |
| Lâm Đồng | 48 | 48 | 100.0% | Có |
| Đắk Nông | 38 | 48 | 79.2% | Không |

## Nguồn dữ liệu crawl được

| Source | Raw rows |
|---|---:|
| VnBusiness | 2,961 |
| Báo Nông nghiệp và Môi trường | 1,380 |
| Báo Nghệ An | 580 |
| Vinanet | 525 |
| Báo Đà Nẵng | 108 |
| Công Thương | 85 |
| HomeUp | 72 |
| Báo Mới | 11 |
| Kamereo | 8 |
| Thương hiệu Công luận | 1 |

## Ranking khu vực theo dữ liệu thật

| Rank | Province | Area | Raw rows | Weekly observed | Monthly observed | Date range | Ghi chú |
|---:|---|---|---:|---:|---:|---|---|
| 1 | Lâm Đồng | Di Linh | 448 | 141/210 | 43/48 | 2022-03-21 -> 2025-12-30 | Khu vực mạnh nhất để train |
| 2 | Đắk Lắk | Ea H'leo | 426 | 141/210 | 43/48 | 2022-03-21 -> 2025-12-29 | Rất phù hợp |
| 3 | Đắk Lắk | Buôn Hồ | 418 | 141/210 | 43/48 | 2022-03-21 -> 2025-12-29 | Rất phù hợp |
| 4 | Lâm Đồng | Bảo Lộc | 417 | 140/210 | 43/48 | 2022-03-21 -> 2025-12-30 | Rất phù hợp |
| 5 | Lâm Đồng | Lâm Hà | 417 | 140/210 | 43/48 | 2022-03-21 -> 2025-12-30 | Rất phù hợp |
| 6 | Gia Lai | Pleiku | 426 | 139/210 | 43/48 | 2022-03-21 -> 2025-12-30 | Phù hợp |
| 7 | Kon Tum | Kon Tum | 241 | 119/210 | 41/48 | 2022-03-21 -> 2025-12-30 | Monthly tốt, weekly thấp hơn nhóm đầu |
| 8 | Gia Lai | Ia Grai | 262 | 105/210 | 40/48 | 2022-03-21 -> 2025-12-30 | Dữ liệu trung bình |
| 9 | Đắk Lắk | Cư M'gar | 203 | 88/210 | 38/48 | 2022-03-21 -> 2025-12-29 | Ít hơn nhóm đầu |
| 10 | Đắk Nông | Gia Nghĩa | 203 | 88/210 | 38/48 | 2022-11-15 -> 2025-12-29 | Độ phủ thấp hơn |
| 11 | Gia Lai | Chư Prông | 203 | 88/210 | 38/48 | 2022-03-21 -> 2025-12-29 | Độ phủ thấp hơn |
| 12 | Đắk Nông | Đắk R'lấp | 0 | 0/210 | 0/48 |  | Không có giá observed riêng |

## Khuyến nghị chọn province/khu vực

- Nếu chỉ cần **1 province đạt ngưỡng**, chọn **Lâm Đồng**, **Gia Lai**, hoặc **Đắk Lắk**. Cả ba đều đạt weekly >75% và monthly 100% ở cấp tỉnh.
- Nếu cần một khu vực cụ thể có dữ liệu thật mạnh nhất, chọn **Di Linh (Lâm Đồng)**, **Ea H'leo (Đắk Lắk)**, hoặc **Buôn Hồ (Đắk Lắk)**.
- Với bài tập AI cơ bản, monthly là lựa chọn ổn định hơn weekly vì độ phủ giá thật cao hơn.
- Không nên chọn **Đắk R'lấp** làm khu vực chính vì không có observed price riêng; dữ liệu khu vực này hiện là fill/proxy.

## File liên quan

- `data/raw/coffee_price_all_areas_daily_2022_2025.csv`: dữ liệu giá crawl thật dạng daily.
- `data/processed/weekly/coffee_environment_all_areas_weekly_2022_2025.csv`: dataset weekly đã merge môi trường, thổ nhưỡng và giá.
- `data/processed/monthly/coffee_environment_all_areas_monthly_2022_2025.csv`: dataset monthly đã merge môi trường, thổ nhưỡng và giá.
- `data/processed/area_real_price_data_ranking.csv`: bảng ranking dạng CSV.
