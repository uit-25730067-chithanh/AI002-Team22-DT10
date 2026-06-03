# CHƯƠNG 4: PHƯƠNG PHÁP THIẾT KẾ VÀ HIỆN THỰC

## 4.1. Tiền xử lý (Preprocess) và Kỹ thuật Đặc trưng (Feature Engineering)

Quy trình tiền xử lý dữ liệu được thiết kế tập trung vào việc đảm bảo tính sạch sẽ, nhất quán và tránh rò rỉ thông tin trong mô hình học máy. Các bước xử lý trong tệp [preprocess.py](file:///Users/tcdtist/dev/uit/ai002/model/preprocess.py) bao gồm:

### 4.1.1. Chuẩn hóa Schema và Loại bỏ Rác

- Áp dụng ánh xạ đổi tên cột để đồng bộ hóa dữ liệu từ crawler về schema huấn luyện thống nhất.
- Chuyển đổi định dạng ngày tháng `period_start` sang kiểu dữ liệu `datetime`.
- Loại bỏ các bản ghi không có nhãn mục tiêu (`historical_price_vnd` bị trống).

### 4.1.2. Điền Khuyết thiếu (Missing Data Imputation)

Đáp ứng trục **Robustness**, hệ thống điền dữ liệu khuyết thiếu bằng cách:

- Đối với dữ liệu số (như nhiệt độ, lượng mưa, độ ẩm): điền bằng giá trị trung vị (median) của thuộc tính đó để không làm méo mó phân phối xác suất chung của biến.
- Đối với dữ liệu danh mục (như phương pháp thu thập giá, chất lượng đất): điền giá trị `"unknown"`.

### 4.1.3. Giới hạn Ngoại lai (Capping Outliers)

Thay vì xóa bỏ các dòng dữ liệu có giá trị ngoại lai (outliers) - điều này sẽ làm giảm đáng kể kích thước tập dữ liệu huấn luyện vốn đã nhỏ - hệ thống áp dụng kỹ thuật **Winsorization** (giới hạn trên và dưới ở phân vị 1% và 99%):

```python
lower = df[col].quantile(0.01)
upper = df[col].quantile(0.99)
df[col] = df[col].clip(lower=lower, upper=upper)
```

Giải pháp này giúp khử nhiễu cảm biến nhiệt độ/lượng mưa bất thường mà không làm mất đi các mẫu giá cà phê thực tế tăng đột biến trong năm 2024-2025.

### 4.1.4. Kỹ thuật Đặc trưng (Feature Engineering)

Nhằm nắm bắt tính mùa vụ và xu hướng tương quan thời gian, mô hình sinh thêm các thuộc tính:

- **Biến đổi chu kỳ tháng (Cyclic Encoding):** Mã hóa tháng theo hàm lượng giác sin/cos giúp mô hình hiểu được khoảng cách giữa tháng 12 và tháng 1 là liền kề, thay vì xem chúng là hai giá trị cách xa nhau nhất (1 và 12).
  $$month\_sin = \sin\left(\frac{2 \pi \times month}{12}\right)$$
  $$month\_cos = \cos\left(\frac{2 \pi \times month}{12}\right)$$
- **Đặc trưng tự hồi quy theo khu vực (Area-based Time-series Features):** Nhóm dữ liệu theo huyện (`area`) trước khi tính toán các biến trễ (Lag) và biến trượt (Rolling). Việc này cực kỳ quan trọng để **tránh rò rỉ dữ liệu (data leakage) chéo địa lý** (ví dụ: giá huyện Ea H'leo không bị lẫn vào cách tính trễ của huyện Di Linh).
  - `lag_1d`: Giá cà phê của huyện đó trong tháng trước.
  - `lag_7d`: Giá cà phê của huyện đó 7 chu kỳ trước.
  - `rolling_avg_7d`: Trung bình trượt của `lag_1d` trong 7 kỳ gần nhất.

## 4.2. Hiện thực lớp bảo vệ khử nhiễu đầu vào (Robustness)

Trục **Robustness** được hiện thực hóa thông qua hai tầng kiểm soát lỗi dữ liệu đầu vào:

### 4.2.1. Xác thực tự động qua Pydantic Schema

Tại tệp [prediction.py](file:///Users/tcdtist/dev/uit/ai002/backend/schemas/prediction.py), lớp `PredictionRequest` sử dụng các ràng buộc kiểu và phạm vi (Type & Range constraints) để reject ngay các payload bất hợp lý từ frontend:

- Lượng mưa phải nằm trong khoảng: `ge=0.0, le=1000.0`
- Nhiệt độ phải nằm trong khoảng sinh lý: `ge=10.0, le=45.0`
- Độ ẩm không khí: `ge=0.0, le=100.0`
- Giá lịch sử: `ge=30000.0, le=200000.0`

### 4.2.2. Điền giá trị an toàn mặc định (Sanitizer)

Trong tệp [predictor.py](file:///Users/tcdtist/dev/uit/ai002/backend/services/predictor.py), hàm `_build_feature_row` xử lý trường hợp frontend gửi thiếu các thuộc tính tùy chọn:

- Nếu độ ẩm trống (`None`) -> tự động gán `75.0` (độ ẩm trung bình Tây Nguyên).
- Nếu độ ẩm đất trống -> gán `0.24`.
- Nếu soil score trống -> gán `5.0`.
- Nếu thiếu giá kỳ trước -> gán giá trị mặc định an toàn `90,000 VND/kg`.

### 4.2.3. Kiểm tra danh mục đã học (Trained Categories Validation)

Nếu người dùng nhập một tỉnh hoặc huyện không có trong tập huấn luyện (ví dụ: một huyện ở miền Bắc), mô hình Random Forest với one-hot encoding sẽ tạo ra vector toàn số 0 và dự báo sai lệch nghiêm trọng. Để ngăn chặn điều này, hệ thống kiểm tra trực tiếp danh mục đầu vào:

```python
available_values = self._category_values(feature_names, prefix)
if available_values and selected_value not in available_values:
    allowed = ", ".join(sorted(available_values))
    raise ValueError(f"Giá trị `{prefix}` không hợp lệ: {selected_value}. Giá trị hợp lệ: {allowed}")
```

Hệ thống sẽ trả về mã lỗi HTTP `422 Unprocessable Entity` giải thích chi tiết danh sách các huyện được mô hình hỗ trợ thay vì đưa ra dự báo sai âm thầm.

## 4.3. Hiện thực lớp bảo vệ request và response (Reliability & Robustness)

Repo hiện tại không triển khai một luồng LLM production riêng cho phần giải thích hay tư vấn, nên không nên mô tả cơ chế `Prompt Guardrails` như một thành phần đang chạy thật. Thay vào đó, lớp bảo vệ đang được hiện thực bằng các thành phần có mặt trong code:

- **API key guard:** endpoint `/predict` và `/model/info` yêu cầu header `X-API-Key`.
- **Pydantic validation:** các trường như nhiệt độ, lượng mưa, độ ẩm, tháng, năm đều bị giới hạn range hợp lý ngay tại schema.
- **Category validation theo model đã train:** `PredictorService` kiểm tra `province`, `area`, `coffee_type`, `price_fill_method`, `dominant_soil_type` và `soil_data_confidence` theo `feature_names` của model để tránh suy luận trên giá trị ngoài tập train.
- **Response disclaimer:** backend luôn trả disclaimer để giảm rủi ro người dùng hiểu dự báo như khuyến nghị tài chính bắt buộc.

Bộ bảo vệ này không giải quyết mọi rủi ro, nhưng đủ phù hợp với scope KISS/YAGNI của đồ án: ưu tiên chặn input sai, giữ contract rõ ràng, và buộc hệ thống trả về cảnh báo minh bạch.

## 4.4. Hiện thực giao diện Web di động (Mobile-first UI)

Nhắm tới đối tượng người dùng cuối là những nông hộ nhỏ lẻ tại các vùng sâu vùng xa, giao diện người dùng (Frontend) được thiết kế theo định hướng **Social Impact (Tác động xã hội)**:

### 4.4.1. Thiết kế Mobile-first và Responsive

- Layout được bố cục thành một cột đơn giản, các trường nhập liệu có kích thước lớn (chiều cao tối thiểu 48px) giúp nông dân dễ dàng thao tác bằng ngón tay ngay cả khi đang làm việc trên rẫy.
- Sử dụng bảng màu có độ tương phản cao (Chữ đen/xám đậm trên nền sáng) để tăng khả năng đọc dưới ánh sáng mặt trời trực tiếp ngoài trời nắng.

### 4.4.2. Trải nghiệm người dùng và Kiến trúc React

- Giao diện được nâng cấp lên kiến trúc **React + Vite + Tailwind CSS**, sử dụng TypeScript để đảm bảo tính an toàn của dữ liệu đầu vào và theme coffee/cream/leaf để phù hợp bối cảnh cà phê Tây Nguyên.
- Tách biệt hai luồng "Dự báo Giá" và "Khuyến nghị Canh tác" để phù hợp với định hình tâm lý (mental model) của nông dân, những người thường chỉ quan tâm đến một trong hai tính năng tại một thời điểm.
- Hỗ trợ tính năng **Lưu lịch sử kết quả (Offline Storage)** thông qua `localStorage` khi người dùng bấm "Lưu kết quả này", giúp nông dân xem lại input, kết quả, lý do dự báo/khuyến nghị và disclaimer mà không cần kết nối mạng liên tục.

### 4.4.3. Hiển thị Disclaimer rõ ràng

- Ở cuối màn hình hiển thị dự báo, hệ thống bắt buộc hiển thị một khung cảnh báo nổi bật: _"Dự báo chỉ mang tính chất tham khảo. Hãy tham khảo thêm giá đại lý thu mua tại địa phương trước khi bán hàng."_ để bảo vệ người dân khỏi các rủi ro kinh doanh.
