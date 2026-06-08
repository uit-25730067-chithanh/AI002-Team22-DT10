# CHƯƠNG 5: THỰC NGHIỆM VÀ ĐÁNH GIÁ

## 5.1. Thiết lập thực nghiệm

Để đánh giá mô hình học máy một cách khách quan và mô phỏng thực tế khi triển khai, đồ án thiết lập quy trình thực nghiệm như sau:
- **Phân chia dữ liệu (Temporal Split):** Tập dữ liệu được phân chia dựa trên mốc thời gian để tránh hiện tượng rò rỉ dữ liệu tương lai (data leakage) - một lỗi phổ biến trong phân tích chuỗi thời gian nếu chia ngẫu nhiên (random split).
  - **Tập Huấn luyện (Train Set):** Dữ liệu từ 01/01/2020 đến 31/12/2024 (sau preprocess còn 708 mẫu dữ liệu tháng).
  - **Tập Kiểm thử (Test Set):** Dữ liệu từ 01/01/2025 đến hết chu kỳ thu thập năm 2025 (bao gồm 144 mẫu dữ liệu tháng).
  - **Freshness Holdout:** Dữ liệu 01/2026 đến 04/2026 được crawl và giữ lại để kiểm tra độ mới, không đưa vào tập test mặc định.
- **Mô hình thực nghiệm:** Sử dụng thuật toán `RandomForestRegressor` từ thư viện Scikit-Learn với cấu hình baseline mặc định: số lượng cây quyết định `n_estimators=100`, hạt giống ngẫu nhiên `random_state=42`.

## 5.2. Kết quả Metrics trên tập Test 2025 (Reliability)

Sau khi huấn luyện trên tập Train 2020–2024, mô hình được dự báo trên tập Test chính thức năm 2025. Kết quả các độ đo thu được như sau:

| Độ đo đánh giá | Giá trị đạt được | Đơn vị tính | Ý nghĩa thực tiễn |
| :--- | :---: | :---: | :--- |
| **MAE** (Sai số tuyệt đối trung bình) | **14,474** | VND/kg | Trung bình mỗi kg cà phê dự báo bị lệch khoảng 14.5k VND so với giá thực tế. |
| **RMSE** (Sai số bình phương trung bình dạng căn) | **17,874** | VND/kg | Phản ánh mức độ lệch lớn nhất, nhấn mạnh sai số ở các huyện có giá biến động cực đoan. |
| **$R^2$** (Hệ số xác định) | **-1.2244** | Không có | Âm, phản ánh giới hạn ngoại suy của baseline khi giá năm 2025 tăng mạnh. |

### Giải thích nguyên nhân hệ số xác định $R^2$ bị âm:
Kết quả $R^2$ bị âm là một hiện tượng kỹ thuật quan trọng cần được báo cáo trung thực (Transparency). Nguyên nhân cốt lõi là **sự dịch chuyển phân phối giá cực đoan năm 2025 (biến cố Thiên nga đen - Black Swan)**:
1. **Giá cà phê tăng phi mã:** Giai đoạn 2020–2024, giá cà phê nhân xô tại Tây Nguyên thấp hơn rõ rệt so với năm 2025. Bước sang năm 2025, do biến động thị trường toàn cầu, giá vọt lên mức lịch sử **100,000 – 120,000 VND/kg**.
2. **Hạn chế ngoại suy của mô hình cây quyết định (Extrapolation Limit):** Các mô hình dựa trên cây quyết định như Random Forest không có khả năng dự đoán ra ngoài miền giá trị mục tiêu đã thấy trong tập huấn luyện. Sự chênh lệch lớn giữa trần tập train và giá thực tế năm 2025 dẫn đến sai số MAE lớn và kéo $R^2$ xuống âm.

Việc trình bày trung thực chỉ số này chứng minh tư duy phản biện khoa học của nhóm phát triển, khẳng định đây là mô hình **baseline** và chỉ ra sự cần thiết của việc thu thập thêm dữ liệu hoặc so sánh với các mô hình time-series có khả năng ngoại suy (như linear regression kết hợp trôi xu hướng hoặc các mô hình học sâu) trong tương lai.

## 5.3. Đánh giá 5 Trục AI Bền vững (Responsible AI Evaluation)

Hệ thống được kiểm thử thực nghiệm chi tiết dựa trên kịch bản kiểm thử 5 trục:

```text
               [ 5 TRỤ CỘT AI BỀN VỮNG ]
    ┌──────────────┬──────────────┼──────────────┬──────────────┐
    ▼              ▼              ▼              ▼              ▼
Reliability       Bias       Robustness    Social Impact  Transparency
(Time split)  (Coverage)    (Sanitizer)     (Disclaimer)    (Features)
```

### 5.3.1. Trục 1: Reliability (Tính tin cậy)
- **Phương pháp kiểm chứng:** Thực hiện phân chia dữ liệu theo thời gian (Temporal Split) để kiểm tra độ tin cậy thực tế.
- **Kết quả:** Mô hình bám sát xu hướng tăng giá của thị trường nhưng bị giới hạn về biên độ tăng do giới hạn của mô hình cây. Sai số MAE 14.5k VND/kg được hiển thị trực tiếp cho người dùng dưới dạng **Khoảng tin cậy (Confidence Interval)** bao quanh giá dự báo trên giao diện, giúp nông dân nhận thức được biên độ an toàn của dự đoán.

### 5.3.2. Trục 2: Bias (Tính thiên lệch)
- **Phương pháp kiểm chứng:** Audit tỷ lệ dòng giá quan sát thật theo tỉnh/area trên dataset chính thức 2020-2026/04.
- **Kết quả:** Kon Tum đạt 88.16%, Lâm Đồng 86.84%, Đắk Lắk/Gia Lai 77.63%, Đắk Nông thấp nhất 60.53%. Area yếu nhất là Cư M'gar, Gia Nghĩa, Chư Prông và Đắk R'lấp.
- **Giải pháp giảm thiểu:** Khi demo, ưu tiên Kon Tum, Di Linh, Ea H'leo, Buôn Hồ, Bảo Lộc, Lâm Hà, Pleiku, Ia Grai. Với Gia Nghĩa, Chư Prông, Cư M'gar, Đắk R'lấp cần hiển thị/nhắc cảnh báo dữ liệu có nhiều proxy/nội suy hơn.

### 5.3.3. Trục 3: Robustness (Kháng nhiễu)
- **Phương pháp kiểm chứng:** Kiểm tra lớp validate đầu vào ở tầng API và chạy chương trình stress test tự động để bơm nhiễu cực đoan (Black Swan) vào riêng tập Test năm 2025 nhằm đo lường sai lệch dự báo định lượng.
- **Kết quả:**
  - **Validate request:** Backend hiện dùng Pydantic schema, API key và kiểm tra category theo feature đã train để chặn các input ngoài range hoặc ngoài tập dữ liệu huấn luyện. Repo hiện tại không triển khai hàm `sanitize_inputs` riêng và không có luồng LLM production để đánh giá Prompt Injection.
  - **Stress Test kịch bản cực đoan (Black Swan):**
    - *Kịch bản 1 (Giá sụp đổ 50% - price_crash):* Sai số MAE tăng từ **14,474** lên **24,538** VND/kg (**+69.5%**). Điều này cho thấy mô hình chịu tác động rất lớn khi thị trường tài chính biến động mạnh do đặc thù mô hình phụ thuộc nhiều vào giá trễ.
    - *Kịch bản 2 (Nhiệt độ tăng vọt lên 45°C - heat_wave):* Sai số MAE hầu như giữ nguyên ở mức **14,472** VND/kg (**+0.0%**). Điều này cho thấy baseline hiện gần như không nhạy với shock nhiệt độ vì trọng số của feature nhiệt độ trong mô hình rất thấp.
    - *Kịch bản 3 (Kết hợp cả hai biến cố - both):* Sai số MAE đạt **24,541** VND/kg (**+69.6%**).

### 5.3.4. Trục 4: Social Impact (Tác động xã hội)
- **Phương pháp kiểm chứng:** Kiểm nghiệm thực tế giao diện mobile-first React/Vite/Tailwind đã hiện thực tại thư mục `frontend/` và xác nhận kết quả phản hồi của backend kèm disclaimer.
- **Kết quả:** Giao diện có màn chào, menu chọn tác vụ, nút bấm lớn, tương phản cao, tách riêng luồng Dự báo Giá và Khuyến nghị Canh tác. Ứng dụng hỗ trợ lưu kết quả thủ công bằng `localStorage` và xem chi tiết lịch sử để nông dân có thể đối chiếu lại input, kết quả, lý do và disclaimer khi mạng không ổn định. Chân trang kết quả luôn bắt buộc hiển thị Disclaimer để giảm thiểu rủi ro nông dân tự ý ra quyết định tài chính sai lệch. Điều này đóng góp vào tác động xã hội thực tế của hệ thống.

### 5.3.5. Trục 5: Transparency (Tính minh bạch / giải thích được)
- **Phương pháp kiểm chứng:** Trích xuất Feature Importance từ mô hình huấn luyện Random Forest.
- **Kết quả:** Hệ thống làm rõ các đặc trưng đóng góp lớn nhất vào dự đoán:
  - `lag_1d` (Giá trễ 1 kỳ trước): **50.5%**
  - `rolling_avg_7d` (Trung bình trượt giá 7 kỳ trước): **46.9%**
  - Các yếu tố khí hậu (lượng mưa, nhiệt độ): **< 1%**
- **Giải thích cho nông dân:** Mô hình minh bạch hóa việc giá cà phê được quyết định bởi đà tăng trưởng của giá thị trường trong quá khứ gần, chứ thời tiết tháng này thay đổi nhẹ không phải là nguyên nhân làm thay đổi ngay lập tức giá bán. Điều này giúp nông dân hiểu đúng bản chất vận hành của mô hình và thị trường.
