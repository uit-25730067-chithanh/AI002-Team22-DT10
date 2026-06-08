# PHỤ LỤC

## Phụ lục 1: Tài liệu tham khảo

1. Breiman, L. (2001). *Random Forests*. Machine Learning, 45(1), 5-32.
2. Pedregosa, F., et al. (2011). *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research, 12, 2825-2830.
3. FastAPI Official Documentation: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
4. Pydantic Documentation: [https://docs.pydantic.dev/](https://docs.pydantic.dev/)
5. Microsoft Responsible AI Standard: [https://www.microsoft.com/en-us/ai/responsible-ai](https://www.microsoft.com/en-us/ai/responsible-ai)
6. Trang tin thị trường nông sản Việt Nam (giacaphe.com, tintaynguyen.com).
7. Nguồn dữ liệu khí tượng Open-Meteo API.

---

## Phụ lục 2: API Request/Response mẫu (JSON)

### API Request mẫu (`POST /predict`)
Request gửi từ Frontend lên Backend chứa đầy đủ các thông số khí tượng, đất đai và lịch sử giá cà phê:
```json
{
  "province": "Lam Dong",
  "area": "Di Linh",
  "avg_temperature_c": 22.5,
  "total_rainfall_mm": 120.0,
  "avg_humidity_percent": 80.0,
  "avg_soil_moisture_0_7cm": 0.28,
  "soil_score": 4.5,
  "soil_data_confidence": "high",
  "coffee_type": "Robusta / ca phe nhan xo noi dia",
  "price_fill_method": "observed",
  "dominant_soil_type": "Dat do bazan",
  "month": 10,
  "year": 2025,
  "latest_price_vnd_per_kg": 85000.0,
  "rolling_avg_price_vnd_per_kg": 83000.0,
  "price_observations": 1.0
}
```

### API Response mẫu
Phản hồi từ Backend trả về giá dự báo, khoảng tin cậy, các đặc trưng giải thích quan trọng và gợi ý canh tác:
```json
{
  "predicted_price_vnd": 85200.0,
  "confidence_interval": [
    81400.0,
    89000.0
  ],
  "top_features": [
    {
      "feature": "rolling_avg_7d",
      "importance": 0.469,
      "input_value": 83000.0,
      "explanation": "rolling_avg_7d có mức quan trọng cao (46.90%) với giá trị hiện tại 83000.00."
    },
    {
      "feature": "lag_1d",
      "importance": 0.505,
      "input_value": 85000.0,
      "explanation": "lag_1d có mức quan trọng cao (50.50%) với giá trị hiện tại 85000.00."
    },
    {
      "feature": "year",
      "importance": 0.0196,
      "input_value": 2025.0,
      "explanation": "year có mức quan trọng cao (1.96%) với giá trị hiện tại 2025.00."
    }
  ],
  "model_version": "20260513_155830__rf_real_monthly",
  "farming_recommendation": {
    "action": "post_harvest_care",
    "season_type": "rainy_season",
    "confidence": 0.9,
    "reasoning": "Tháng 10 ở Lâm Đồng là giai đoạn thu hoạch rộ và bắt đầu chăm sóc sau thu hoạch. Điều kiện đất và thời tiết hiện tại không có cảnh báo lớn. Đây là gợi ý rule-based để tham khảo.",
    "warnings": [],
    "next_action_month": 11,
    "next_action": "post_harvest_care",
    "advisory_type": "rule_based"
  },
  "disclaimer": "Dự báo giá và gợi ý canh tác chỉ mang tính tham khảo, không thay thế tư vấn tài chính hoặc tư vấn nông nghiệp tại địa phương."
}
```

---

## Phụ lục 3: Minh chứng Demo & Giao diện người dùng (Mô phỏng Mobile UI)

Giao diện người dùng được thiết kế tối giản, trực quan hóa trên màn hình điện thoại di động giúp nông dân dễ tiếp cận ngoài thực địa:

```text
┌──────────────────────────────────────────┐
│   AI COFFEE FARMING - ĐỀ TÀI DT10        │
├──────────────────────────────────────────┤
│ Chọn Tỉnh:  [ Lâm Đồng            | v ]  │
│ Chọn Huyện: [ Di Linh             | v ]  │
│ Tháng dự báo: [ 10 ]                     │
│                                          │
│ [ DỰ BÁO GIÁ CÀ PHÊ & KHUYẾN NGHỊ ]      │
├──────────────────────────────────────────┤
│ KẾT QUẢ DỰ BÁO:                          │
│ Giá dự báo:  85,200 VND/kg               │
│ Khoảng giá:  81,400 - 89,000 VND/kg      │
│                                          │
│ GỢI Ý CANH TÁC:                          │
│ Hành động:  Chăm sóc sau thu hoạch       │
│ Mùa vụ:     Mùa mưa                      │
│ Lý do:      Tháng 10 thu hoạch rộ và bắt │
│             đầu dưỡng cây.               │
│                                          │
│ GIẢI THÍCH MÔ HÌNH:                      │
│ - Xu hướng giá 3 tháng qua:   [█████] 72%│
│ - Giá tháng trước:            [█]     22%│
│ - Các yếu tố khí hậu khác:            <1%│
├──────────────────────────────────────────┤
│ Cảnh báo: Không có cảnh báo thời tiết xấu│
│                                          │
│ * Lưu ý: Dự báo chỉ mang tính chất tham  │
│ khảo học tập, không thay thế tư vấn tài │
│ chính và thu mua thương lái địa phương.  │
└──────────────────────────────────────────┘
```

---

## Phụ lục 4: Đường dẫn mã nguồn và Dữ liệu

### Cấu trúc mã nguồn chính trên repository:
- **Tập dữ liệu huấn luyện:** [coffee_environment_all_areas_monthly_2020_2026.csv](../../../data/processed/monthly/coffee_environment_all_areas_monthly_2020_2026.csv)
- **Module tiền xử lý:** [preprocess.py](../../../model/preprocess.py)
- **Module huấn luyện Random Forest:** [train_rf.py](../../../model/train_rf.py)
- **Entrypoint Backend API:** [main.py](../../../backend/main.py)
- **Định nghĩa API Routes:** [routes.py](../../../backend/api/routes.py)
- **Định nghĩa Request/Response Validation:** [prediction.py](../../../backend/schemas/prediction.py)
- **Predictor Service logic:** [predictor.py](../../../backend/services/predictor.py)
- **Farming Advisory rule engine:** [farming_advisory.py](../../../backend/services/farming_advisory.py)
