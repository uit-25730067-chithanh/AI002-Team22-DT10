# CHƯƠNG 3: DỮ LIỆU & THIẾT KẾ HỆ THỐNG

## 3.1. Thu thập dữ liệu và Phân tích độ phủ

Hệ thống sử dụng dữ liệu tích hợp từ các nguồn public: dữ liệu giá cà phê từ trang tin thị trường nông sản, dữ liệu khí tượng lịch sử từ API thời tiết, và hồ sơ đất theo khu vực tại Tây Nguyên.

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

| Tỉnh | Tỉ lệ dữ liệu giá quan sát thật (Monthly baseline 2020-2026/04) | Đánh giá chất lượng dữ liệu |
| :--- | :---: | :--- |
| **Kon Tum** | 88.16% | Mạnh nhất, nhưng chỉ có 1 area khảo sát. |
| **Lâm Đồng** | 86.84% | Tốt, phù hợp demo vì các area có độ phủ đều. |
| **Đắk Lắk** | 77.63% | Chất lượng trung bình khá, Cư M'gar yếu hơn hai area còn lại. |
| **Gia Lai** | 77.63% | Chất lượng trung bình khá, Chư Prông yếu hơn hai area còn lại. |
| **Đắk Nông** | 60.53% | Thấp nhất, cần cảnh báo khi demo. |

**Định hướng thiết kế giảm thiểu Bias:**
- Khi chạy thử nghiệm và demo, ưu tiên sử dụng dữ liệu của các khu vực có tỷ lệ quan sát thật cao như: **Kon Tum, Di Linh, Ea H'leo, Buôn Hồ, Bảo Lộc, Lâm Hà, Pleiku, Ia Grai**.
- Cần cảnh báo khi dùng **Gia Nghĩa, Chư Prông, Cư M'gar, Đắk R'lấp** vì đây là các area có nhiều proxy/nội suy hơn trong dataset mới.
- Bias nguồn vẫn đáng kể vì dữ liệu phụ thuộc vào các trang tin public. Vì vậy giá trong hệ thống là giá tham khảo, không phải giao dịch chính thức.

## 3.2. Quy trình xử lý dữ liệu (Raw → Weekly → Monthly)

Dữ liệu thô cào về hàng ngày (`raw daily`) chứa nhiều nhiễu biến động ngắn hạn do tâm lý thị trường và có nhiều lỗ hổng mất mát dữ liệu do lỗi crawler hoặc lỗi kết nối. Quy trình tổng hợp dữ liệu trải qua các bước:

```text
[ Dữ liệu thô hàng ngày (Raw Daily) ]
                │
                ▼ (Lọc trùng, điền khuyết thiếu)
[ Tập dữ liệu tuần (Weekly Dataset) ] ── (3,972 dòng, dùng tham khảo)
                │
                ▼ (Trung bình hóa theo tháng)
[ Tập dữ liệu tháng (Monthly Dataset) ] ─ (912 dòng 2020-2026/04, 77.96% observed)
```

**Lý do lựa chọn tập dữ liệu tháng (Monthly Dataset) làm baseline chính:**
1. **Kiểm soát nhiễu:** Dữ liệu tháng loại bỏ các biến động đột biến trong ngày/tuần, giúp mô hình học máy nắm bắt tốt hơn xu hướng chu kỳ dài hạn của giá nông sản.
2. **Đồng bộ thời tiết:** Các chu kỳ canh tác nông nghiệp và thời tiết thường được tính theo tháng hoặc mùa vụ. Việc sử dụng dữ liệu tháng giúp các đặc trưng khí hậu (nhiệt độ, lượng mưa) mang tính đại diện cao hơn cho sinh trưởng của cây cà phê.
3. **KISS & YAGNI:** Tập dữ liệu tháng có kích thước gọn nhẹ (912 dòng, 18 cột), giúp mô hình Random Forest huấn luyện nhanh mà vẫn giữ pipeline dễ giải thích. Điều này tránh việc lãng phí tài nguyên tính toán (vấn đề xanh hóa AI).

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

Đáp ứng trụ cột **Transparency (Minh bạch)**, hệ thống không chỉ trả về giá dự báo đơn thuần mà đính kèm cơ cấu đóng góp của các yếu tố đầu vào và khuyến nghị nông học tương ứng. 

Cấu trúc thiết kế của API response cho endpoint `/predict` được quy định rõ khớp với Pydantic schema:

```json
{
  "predicted_price_vnd": 122474.05,
  "confidence_interval": [119235.25, 125712.85],
  "top_features": [
    {
      "feature": "rolling_avg_7d",
      "importance": 0.469,
      "input_value": 84000.0,
      "explanation": "rolling_avg_7d có mức quan trọng cao (46.90%) với giá trị hiện tại 84000.00."
    },
    {
      "feature": "lag_1d",
      "importance": 0.505,
      "input_value": 86000.0,
      "explanation": "lag_1d có mức quan trọng cao (50.50%) với giá trị hiện tại 86000.00."
    },
    {
      "feature": "year",
      "importance": 0.0196,
      "input_value": 2025.0,
      "explanation": "year có mức quan trọng cao (1.96%) với giá trị hiện tại 2025.00."
    }
  ],
  "model_version": "20260608_004601__rf_monthly_baseline",
  "farming_recommendation": {
    "action": "growth_care",
    "season_type": "rainy_season",
    "confidence": 0.85,
    "reasoning": "Tháng 6 thuộc mùa mưa, cần chăm sóc sinh trưởng và phòng nấm bệnh. Điều kiện đất và thời tiết hiện tại không có cảnh báo lớn.",
    "warnings": [],
    "next_action_month": 7,
    "next_action": "growth_care",
    "advisory_type": "rule_based"
  },
  "disclaimer": "Dự báo giá và gợi ý canh tác chỉ mang tính tham khảo, không thay thế tư vấn tài chính hoặc tư vấn nông nghiệp tại địa phương."
}
```

Thông qua phản hồi JSON này, giao diện người dùng sẽ vẽ một biểu đồ thanh ngang đơn giản từ `top_features` để nông dân hiểu rằng: *"Giá dự báo tháng tới tăng/giảm chủ yếu là do ảnh hưởng của rolling average và giá trễ gần nhất, trong khi yếu tố thời tiết/đất hiện có trọng số rất thấp"*. Việc này giúp giảm thiểu việc nông dân diễn giải sai lệch rằng thời tiết tháng này thay đổi sẽ làm thay đổi hoàn toàn giá bán ngày mai. Đồng thời, trường `farming_recommendation` cung cấp các hành động cụ thể (như bón phân, tưới nước) và lý giải nông học đi kèm để nông hộ tham khảo.
