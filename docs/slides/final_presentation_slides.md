# SLIDE THUYẾT TRÌNH ĐỒ ÁN CUỐI KỲ - ĐỀ TÀI DT10

**Môn học:** Tư duy Trí tuệ Nhân tạo (AI002)  
**Đề tài:** AI Dự báo Kế hoạch Canh tác Mùa vụ & Giá Cà phê cho Nông dân Tây Nguyên  
**Tác giả:** Nhóm 10 (Đặng Chí Thanh, Hoàng Cao Sơn)  
**Định dạng Slide:** Được cập nhật khớp với mã nguồn Frontend `slidesData.ts` (không bao gồm Speaker Notes).

---

## Slide 1: Trang bìa

- **Tiêu đề:** AI Hỗ Trợ Canh Tác & Dự Báo Giá Cà Phê
- **Phân hệ đề tài:** Đề tài DT10 - Tư duy Trí tuệ Nhân tạo (AI002)
- **Giảng viên hướng dẫn:** TS. Phan Thế Duy
- **Nhóm thực hiện:** Nhóm 10
  - Đặng Chí Thanh (Trưởng nhóm - MSSV: 25730067)
  - Hoàng Cao Sơn (Thành viên - MSSV: 25730061)

---

## Slide 1.1: Thành viên Đặng Chí Thanh (Nhóm trưởng)

- **Họ và tên:** Đặng Chí Thanh
- **MSSV:** 25730067
- **Nhiệm vụ phân công:**
  - Kỹ thuật Machine Learning (Preprocess dữ liệu, Feature Engineering, Random Forest Baseline).
  - Phát triển Backend API bằng FastAPI (Định nghĩa contract API).
  - Xây dựng Web UI (Frontend) và tích hợp liên kết API với giao diện trực quan.
  - Phụ trách AI Bền vững: Trục Reliability (Tính tin cậy), Transparency (Minh bạch) & Social Impact.

---

## Slide 1.2: Thành viên Hoàng Cao Sơn

- **Họ và tên:** Hoàng Cao Sơn
- **MSSV:** 25730061
- **Nhiệm vụ phân công:**
  - Đánh giá và kiểm toán dữ liệu (Real Data Audit).
  - Thu thập dữ liệu lịch sử giá & thời tiết (Crawler) và đánh giá độ phủ dữ liệu (Data Coverage).
  - Viết kịch bản stress test tự động cho API đánh giá biên độ sai số.
  - Phụ trách AI Bền vững: Trục Robustness (Kháng nhiễu) & Bias (Tính thiên lệch).

---

## Slide 2: Bối cảnh & Vấn đề Nông hộ

- **Hình ảnh minh họa:** `/slide-06.png`
- **Nội dung chính:**
  - Biến đổi khí hậu cực đoan: Nhiệt độ tăng, lượng mưa thất thường ảnh hưởng trực tiếp năng suất.
  - Bất đối xứng thông tin thị trường: Nông dân thiếu dữ liệu khách quan, dễ bị ép giá.
  - Quyết định cảm tính: Việc canh tác, bán hàng phần lớn dựa dẫm kinh nghiệm truyền thống.

---

## Slide 3: Mục tiêu & Phạm vi

- **Nội dung chính:**
  - Mục tiêu cốt lõi: Cung cấp công cụ dự báo giá và khuyến nghị canh tác.
  - Định hướng thiết kế: Hiện thực hóa 5 Trụ cột AI Bền vững (Responsible AI).
  - Phạm vi áp dụng: 5 tỉnh Tây Nguyên (2020–2026).
- **Tuyên bố miễn trừ trách nhiệm (Disclaimer):** Hệ thống mang tính chất tham khảo học thuật. Không thay thế tư vấn chuyên môn/thương mại.

---

## Slide 4: Quy trình Xử lý Dữ liệu

- **Luồng xử lý (Flow steps):**
  1. Dữ liệu thô hàng ngày (Raw Daily Prices & Weather)
  2. Dataset Tuần (3,972 dòng)
  3. Dataset Tháng (912 dòng, 18 cột, 77.96% observed) - Baseline
- **Nội dung chính:**
  - Độ phủ dữ liệu thực tế (Observed coverage): Đạt 77.96% trên toàn bộ dataset tháng.
  - Giảm nhiễu: Bỏ qua biến động giá ảo trong ngày/tuần.
  - Tính đồng bộ: Chu kỳ sinh trưởng và thời tiết tương thích theo tháng.
  - Nguyên lý KISS: Dữ liệu nhỏ gọn, nhẹ nhàng, tối ưu tài nguyên.

---

## Slide 5: Kiến trúc 4 Tầng

- **Nội dung chính:**
  - Tầng 4: Presentation Layer (Mobile UI tối ưu di động, Disclaimer).
  - Tầng 3: AI Core Layer (FastAPI, Model Random Forest, Pydantic guard).
  - Tầng 2: Filtering Layer (Nội suy giá trị, Khử nhiễu cảm biến lỗi).
  - Tầng 1: Data Layer (Crawler thu thập tự động giá & thời tiết).

---

## Slide 6: Phương pháp Kỹ thuật & Đặc trưng

- **Nội dung chính:**
  - Mô hình học máy: Random Forest Regressor (Ensemble Bagging).
  - Cyclic Encoding: Mã hóa chu kỳ tháng bằng hàm Sin/Cos (Giữ tính liền mạch T12-T1).
  - Area-based Lags: Đặc trưng tự hồi quy được cô lập theo huyện, hiểu là kỳ trước/7 kỳ trước trong baseline monthly.
  - Mục tiêu cốt lõi: Chống rò rỉ dữ liệu (Data Leakage) chéo địa lý.

---

## Slide 7: Kết quả Định lượng (Tập Test 2025)

- **Chỉ số đánh giá (Metrics):**
  - MAE: 14,474 VND/kg
  - RMSE: 17,874 VND/kg
  - R²: -1.2244 (Âm)
- **Nội dung chính:**
  - Trình bày trung thực R² âm do Giới hạn Ngoại suy (Extrapolation Limit).
  - Tập Train (2020-2024): Miền giá thấp hơn chiếm đa số trong lịch sử cũ.
  - Thực tế 2025 (Black Swan): Giá bùng nổ vượt ngưỡng 100k - 131.5k VND/kg.
  - Mô hình bị giới hạn bởi trần dữ liệu đã học và xu hướng kéo về trung bình quá khứ.

---

## Slide 8: Robustness (Kháng nhiễu)

- **Nội dung chính:**
  - Bảo vệ 1: Validate request ở tầng API chặn dữ liệu dị thường.
  - Bảo vệ 2: Category Guard chỉ cho phép dự báo danh mục thuộc tập train.
  - Kết quả Stress Test: Khi có cú sốc giá cực đoan, MAE tăng 69.5%.
  - Sốc nhiệt 45°C gần như không làm đổi sai số: MAE 14,472 VND/kg (+0.0%).
  - Khi kết hợp sốc giá và sốc thời tiết cùng lúc, MAE tăng 69.6%.
  - Kết luận: Hệ thống nhạy cảm với sốc giá nhưng chống chịu tốt với sốc thời tiết.

---

## Slide 9: Bias & Social Impact

- **Thiên lệch địa lý (Bias):**
  - Kon Tum: Độ phủ 88.2% | Lâm Đồng: 86.8%.
  - Đắk Lắk/Gia Lai: Độ phủ trung bình 77.6%.
  - Đắk Nông: Phủ 60.5% ➔ Luôn hiển thị cảnh báo tin cậy thấp tại vùng này.
  - Area cần cảnh báo: Gia Nghĩa, Chư Prông, Cư M'gar, Đắk R'lấp.
- **Tác động xã hội (Social Impact):**
  - Giao diện tối ưu Mobile-first, tương phản cao, nút chạm kích thước lớn.
  - Hỗ trợ xem lại lịch sử Offline (lưu qua localStorage).
  - Neo chặt Disclaimer dưới chân trang, ngăn rủi ro quyết định sai.

---

## Slide 10: Transparency (Tính minh bạch)

- **Tỷ lệ đóng góp đặc trưng (Feature Importance - Chart Data):**
  - Giá tháng trước (lag_1d): 50.5%
  - Đà giá TT (rolling_avg_7d): 46.9%
  - Thời tiết & Yếu tố khác: 2.6%
- **Nội dung chính:**
  - AI làm sáng tỏ lý do dự báo: Đà giá lịch sử (kỳ gần) đóng vai trò quyết định chính.
  - Ngăn chặn nhận định cảm tính (Ví dụ: Mưa đột ngột hôm nay không làm rớt ngay giá bán ngày mai).

---

## Slide 11: Giao diện Di động (Mobile UI)

- **Nội dung chính:**
  - Định hướng thiết kế Neo-Brutalism: Tương phản cao, phù hợp đọc dưới nắng gắt ngoài rẫy.
  - Biệt lập tác vụ: Phân tách rõ luồng 'Dự báo Giá' và 'Khuyến nghị Canh tác'.
  - An toàn dữ liệu: Lưu dự báo ngoại tuyến, hỗ trợ kết nối mạng 3G yếu chập chờn.
  - Minh bạch đầu ra: Trực quan hóa mức đóng góp của đặc trưng và khuyến nghị rõ ràng.

---

## Slide 12: Kết luận & Hướng Phát triển

- **Nội dung chính:**
  - Kết luận:
    - Đã Vận hành thành công cấu trúc AI End-to-End.
    - Tích hợp hiện thực thành công 5 Trụ cột AI Bền vững vào hệ thống.
    - Trung thực báo cáo giới hạn do ngoại suy mô hình cây Quyết định.
  - Hướng phát triển:
    - Nghiên cứu mô hình hỗ trợ xu hướng tốt hơn (Linear trend, Prophet, XGBoost v2).
    - Tiến hành huấn luyện Localized models dành riêng cho các vi khí hậu (tiểu vùng).

---

## Slide 13: Tài liệu Tham khảo

- **Nội dung chính:**
  - Breiman, L. (2001). Random Forests. Machine Learning. DOI: 10.1023/A:1010933404324.
  - Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. JMLR 12(85):2825-2830.
  - Microsoft Responsible AI Standard v2 & Reference Guide.
  - Open-Meteo Historical Weather API.
  - Nguồn giá trong manifest: Báo Công Thương, Nông nghiệp & Môi trường, Kinh tế Đô thị, Vinanet.

---

## Slide 14: Xin Chân Thành Cảm Ơn

- **Nội dung phụ:** Questions & Answers
- **Nội dung chính:** Trân trọng cảm ơn TS. Phan Thế Duy và các bạn đã theo dõi báo cáo.
