# CHƯƠNG 3: DỮ LIỆU & THIẾT KẾ HỆ THỐNG

## 3.1. Thu thập dữ liệu và Phân tích độ phủ

Hệ thống sử dụng dữ liệu tích hợp từ hai nguồn chính: dữ liệu giá cà phê thực tế cào từ các trang tin thị trường nông sản và dữ liệu khí tượng từ các trạm quan trắc/API thời tiết lịch sử tại khu vực Tây Nguyên.

### 3.1.1. Thuộc tính dữ liệu (Schema)

Tập dữ liệu tích hợp bao gồm các thuộc tính sau:
- **Địa lý:** Tỉnh (`province`), Huyện/Khu vực (`area`).
- **Thời gian:** Ngày bắt đầu chu kỳ (`period_start`).
- **Khí tượng:** Nhiệt độ trung bình (`avg_temperature_c`), Lượng mưa (`total_rainfall_mm`), Độ ẩm trung bình (`avg_humidity_percent`).
- **Đất đai:** Độ tin cậy dữ liệu đất (`soil_data_confidence`) - là một chỉ số danh mục biểu thị mức độ chất lượng đất đai tại địa phương.
- **Giá cà phê:** Giá cà phê trung bình trong chu kỳ (`avg_price_vnd_per_kg`) và giá cà phê quan sát thực tế cào từ crawler (`observed_price_vnd_per_kg`).

### 3.1.2. Phân tích độ phủ dữ liệu thật và Bias địa lý

Khi đưa dữ liệu thật vào phân tích, nhóm phát triển phát hiện sự chênh lệch lớn về mật độ dữ liệu quan sát thực tế (`observed price`) giữa các tỉnh. Đây là minh chứng quan trọng của **trục Bias (Tính thiên lệch)** trong Responsible AI. 

Thống kê chi tiết tỷ lệ dòng có dữ liệu giá cào thật trên tổng số dòng theo từng tỉnh:

| Tỉnh | Tỉ lệ phủ dữ liệu (Monthly) | Tỉ lệ phủ dữ liệu (Weekly) | Đánh giá chất lượng dữ liệu |
| :--- | :---: | :---: | :--- |
| **Lâm Đồng** | 100.0% | 94.0% | Rất mạnh, giá thu thập đầy đủ, là vùng tối ưu để demo hệ thống. |
| **Kon Tum** | 100.0% | 92.4% | Rất mạnh, tuy nhiên số lượng khu vực khảo sát ít hơn Lâm Đồng. |
| **Đắk Lắk** | 93.1% | 76.5% | Chất lượng tốt, dữ liệu dùng ổn định. |
| **Gia Lai** | 93.1% | 75.4% | Chất lượng tốt, dữ liệu dùng ổn định. |
| **Đắk Nông** | 39.6% | 21.0% | **Yếu**, dữ liệu bị đứt gãy nhiều, cần cảnh báo bias vùng miền. |

**Định hướng thiết kế giảm thiểu Bias:**
- Khi chạy thử nghiệm và demo, ưu tiên sử dụng dữ liệu của các khu vực có độ phủ cao như: **Di Linh, Ea H'leo, Buôn Hồ, Bảo Lộc, Lâm Hà, Pleiku**.
- Tuyệt đối tránh sử dụng huyện **Đắk R'lấp (Đắk Nông)** làm ví dụ demo chính vì tỷ lệ dữ liệu crawl thật rất thấp, hầu hết các điểm giá tại đây phải sử dụng thuật toán nội suy hoặc gán giá trị trung bình tỉnh làm proxy. Hệ thống sẽ hiển thị cảnh báo độ tin cậy thấp trên giao diện khi người dùng chọn Đắk Nông.

## 3.2. Quy trình xử lý dữ liệu (Raw → Weekly → Monthly)

Dữ liệu thô cào về hàng ngày (`raw daily`) chứa nhiều nhiễu biến động ngắn hạn do tâm lý thị trường và có nhiều lỗ hổng mất mát dữ liệu do lỗi crawler hoặc lỗi kết nối. Quy trình tổng hợp dữ liệu trải qua các bước:

```text
[ Dữ liệu thô hàng ngày (Raw Daily) ]
                │
                ▼ (Lọc trùng, điền khuyết thiếu)
[ Tập dữ liệu tuần (Weekly Dataset) ] ── (2,520 dòng, 72.7% observed)
                │
                ▼ (Trung bình hóa theo tháng)
[ Tập dữ liệu tháng (Monthly Dataset) ] ─ (576 dòng, 86.5% observed)
```

**Lý do lựa chọn tập dữ liệu tháng (Monthly Dataset) làm baseline chính:**
1. **Kiểm soát nhiễu:** Dữ liệu tháng loại bỏ các biến động đột biến trong ngày/tuần, giúp mô hình học máy nắm bắt tốt hơn xu hướng chu kỳ dài hạn của giá nông sản.
2. **Đồng bộ thời tiết:** Các chu kỳ canh tác nông nghiệp và thời tiết thường được tính theo tháng hoặc mùa vụ. Việc sử dụng dữ liệu tháng giúp các đặc trưng khí hậu (nhiệt độ, lượng mưa) mang tính đại diện cao hơn cho sinh trưởng của cây cà phê.
3. **KISS & YAGNI:** Tập dữ liệu tháng có kích thước gọn nhẹ (576 dòng, 16 cột), giúp mô hình Random Forest huấn luyện cực nhanh (dưới 1 giây) mà vẫn đảm bảo độ chính xác đáng tin cậy. Điều này tránh việc lãng phí tài nguyên tính toán (vấn đề xanh hóa AI).

## 3.3. Kiến trúc hệ thống 4 tầng (Responsible AI Architecture)

Hệ thống được thiết kế theo kiến trúc 4 tầng phân tách trách nhiệm rõ ràng, tích hợp các cơ chế bảo vệ AI có trách nhiệm:

```text
┌──────────────────────────────────────────────────────────┐
│ 1. Data Layer (Crawler & Data Sources)                   │
└───────────────┬──────────────────────────────────────────┘
                │
┌───────────────▼──────────────────────────────────────────┐
│ 2. Filtering Layer (Làm sạch & Khử nhiễu khí tượng)      │
└───────────────┬──────────────────────────────────────────┘
                │
┌───────────────▼──────────────────────────────────────────┐
│ 3. AI Core Layer (FastAPI Server & RandomForestRegressor)│
└───────────────┬──────────────────────────────────────────┘
                │
┌───────────────▼──────────────────────────────────────────┐
│ 4. Presentation Layer (Mobile-first UI & Disclaimer)      │
└──────────────────────────────────────────────────────────┘
```

1. **Tầng 1 - Data Layer (Tầng dữ liệu):** Crawler thu thập tự động dữ liệu giá cà phê thực tế cào từ internet và dữ liệu thời tiết API. Kết quả lưu trữ dưới dạng file CSV cục bộ.
2. **Tầng 2 - Filtering Layer (Tầng lọc và khử nhiễu):** Thực hiện tiền xử lý dữ liệu. Nội suy các giá trị giá cà phê bị thiếu, đồng thời áp dụng lớp khử nhiễu (Sanitization) đối với các thông số khí tượng bất thường trước khi đưa vào mô hình (Robustness).
3. **Tầng 3 - AI Core Layer (Tầng nhân AI):** Chạy backend **FastAPI**. Tải mô hình Random Forest đã được huấn luyện sẵn, tiếp nhận request qua endpoint `/predict`, thực hiện validate dữ liệu đầu vào bằng **Pydantic** và trả về kết quả dự báo kèm định lượng mức độ đóng góp đặc trưng (Explainability).
4. **Tầng 4 - Presentation Layer (Tầng hiển thị):** Giao diện web được thiết kế tối giản, tải nhanh trên điện thoại di động (Mobile-first). Hiển thị trực quan con số dự báo giá, khoảng tin cậy, biểu đồ giải thích đặc trưng và tuyên bố từ chối trách nhiệm giao dịch tài chính (Social Impact).

## 3.4. Thiết kế thành phần giải thích mô hình (Explainability Engine)

Đáp ứng trụ cột **Transparency (Minh bạch)**, hệ thống không chỉ trả về giá dự báo đơn thuần mà đính kèm cơ cấu đóng góp của các yếu tố đầu vào. 

Cấu trúc thiết kế của API response cho endpoint `/predict` được quy định rõ:

```json
{
  "province": "Lam Dong",
  "area": "Di Linh",
  "predicted_price_vnd": 85200.0,
  "confidence_interval": [81400.0, 89000.0],
  "explainability_metrics": {
    "rolling_avg_7d_impact": 72.8,
    "lag_1d_impact": 22.2,
    "year_impact": 1.96,
    "temperature_impact": 0.08,
    "rainfall_impact": 0.09
  },
  "model_version": "20260513_155830__rf_real_monthly",
  "disclaimer": "Dự báo AI chỉ mang tính chất tham khảo học tập, không thay thế cho quyết định tài chính thực tế của nông hộ."
}
```

Thông qua phản hồi JSON này, giao diện người dùng sẽ vẽ một biểu đồ thanh ngang đơn giản để nông dân hiểu rằng: *"Giá dự báo tháng tới tăng/giảm chủ yếu là do ảnh hưởng của đà giá lịch sử gần đây chiếm 72.8%, trong khi yếu tố nhiệt độ hay lượng mưa chỉ đóng góp dưới 1%"*. Việc này giúp giảm thiểu việc nông dân diễn giải sai lệch rằng thời tiết tháng này thay đổi sẽ làm thay đổi hoàn toàn giá bán ngày mai.
