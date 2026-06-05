# SLIDE THUYẾT TRÌNH ĐỒ ÁN CUỐI KỲ - ĐỀ TÀI DT10

**Môn học:** Tư duy Trí tuệ Nhân tạo (AI002)  
**Đề tài:** AI Dự báo Kế hoạch Canh tác Mùa vụ & Giá Cà phê cho Nông dân Tây Nguyên  
**Tác giả:** Nhóm 10 (Đào Vĩnh Bảo Phúc, Đặng Chí Thanh, Hoàng Cao Sơn, Tăng Phước Thịnh)  
**Định dạng Slide:** Có thể trình chiếu trực tiếp từ Markdown hoặc dùng để nhập vào Google Slides/PowerPoint.

---

## Slide 1: Trang bìa
* **Tiêu đề:** AI hỗ trợ canh tác & Dự báo giá Cà phê cho Nông dân Tây Nguyên
* **Phân hệ đề tài:** Đề tài DT10 - Tư duy Trí tuệ Nhân tạo (AI002)
* **Giảng viên hướng dẫn:** TS. Phan Thế Duy
* **Nhóm thực hiện:** Nhóm 10
  - Đào Vĩnh Bảo Phúc (Nhóm trưởng - MSSV: 25730053)
  - Đặng Chí Thanh (Kỹ thuật ML & Backend - MSSV: 25730067)
  - Hoàng Cao Sơn (Đánh giá & Kiểm toán AI - MSSV: 25730061)
  - Tăng Phước Thịnh (Dữ liệu khí hậu - MSSV: 25730071)
* **Speaker Notes:** 
  > Xin chào Thầy và các bạn. Hôm nay Nhóm 10 xin đại diện trình bày đồ án cuối kỳ môn Tư duy Trí tuệ Nhân tạo với đề tài DT10: AI dự báo kế hoạch canh tác mùa vụ và giá cà phê cho nông dân Tây Nguyên. Trọng tâm của đồ án không nằm ở việc xây dựng mô hình Deep Learning phức tạp mà tập trung vào việc áp dụng tư duy thiết kế hệ thống AI bền vững và có trách nhiệm đến tay người nông dân nhỏ lẻ.

---

## Slide 1.1: Thành viên Đào Vĩnh Bảo Phúc (Nhóm trưởng)
* **Họ và tên:** Đào Vĩnh Bảo Phúc
* **MSSV:** 25730053
* **Nhiệm vụ phân công:** Thu thập dữ liệu (Crawler), Xây dựng Web UI (Frontend) và hỗ trợ lập báo cáo, slide.
* **Phụ trách AI Bền vững:** Trục Social Impact (Tác động xã hội).
* **Speaker Notes:**
  > Trình bày tóm tắt vai trò điều phối dự án và định hướng thiết kế giao diện Mobile-first tối ưu cho nông dân ở khu vực mạng 3G yếu.

---

## Slide 1.2: Thành viên Tăng Phước Thịnh
* **Họ và tên:** Tăng Phước Thịnh
* **MSSV:** 25730071
* **Nhiệm vụ phân công:** Crawl dữ liệu thời tiết, xây dựng tài liệu nghiên cứu giá và hỗ trợ thiết kế, liên kết API với giao diện UI.
* **Speaker Notes:**
  > Nhấn mạnh quá trình thu thập, đồng bộ các thông số khí hậu với chu kỳ giá cà phê và việc kết nối hệ thống xuyên suốt.

---

## Slide 1.3: Thành viên Đặng Chí Thanh
* **Họ và tên:** Đặng Chí Thanh
* **MSSV:** 25730067
* **Nhiệm vụ phân công:** Đảm nhiệm kỹ thuật Machine Learning (Feature Engineering, Preprocessing, Train thuật toán Random Forest Baseline) và viết Backend API bằng FastAPI.
* **Phụ trách AI Bền vững:** Trục Reliability (Tính tin cậy) và Explainability (Tính minh bạch/giải thích được).
* **Speaker Notes:**
  > Nêu bật quá trình thiết kế lõi AI kiểm soát mức độ quan trọng của đặc trưng (Feature Importance) và xử lý backend.

---

## Slide 1.4: Thành viên Hoàng Cao Sơn
* **Họ và tên:** Hoàng Cao Sơn
* **MSSV:** 25730061
* **Nhiệm vụ phân công:** Đánh giá và kiểm toán dữ liệu (Real Data Audit), đồng thời viết kịch bản stress test tự động cho API.
* **Phụ trách AI Bền vững:** Trục Robustness (Kháng nhiễu) và Bias (Tính thiên lệch).
* **Speaker Notes:**
  > Tóm tắt về các phát hiện khi đánh giá độ lệch dữ liệu địa lý giữa các tỉnh và quá trình mô phỏng các kịch bản nhiễu cực đoan (Black Swan).

---


## Slide 2: Bối cảnh thực tiễn & Vấn đề nông hộ
* **Vấn đề 1: Biến đổi khí hậu cực đoan**
  - Thời tiết Tây Nguyên biến động mạnh (nhiệt độ tăng, lượng mưa thất thường, khô hạn kéo dài).
  - Ảnh hưởng trực tiếp đến năng suất và chất lượng hạt cà phê.
* **Vấn đề 2: Bất đối xứng thông tin thị trường**
  - Giá cà phê biến động liên tục theo sàn thế giới.
  - Nông dân thiếu dữ liệu khách quan, dễ bị ép giá bởi thương lái.
* **Vấn đề 3: Quyết định cảm tính**
  - Việc tưới nước, bón phân, chọn thời điểm bán chủ yếu dựa vào kinh nghiệm cá nhân truyền thống.
* **Speaker Notes:**
  > Cà phê là xương sống kinh tế Tây Nguyên. Tuy nhiên, nông dân nhỏ lẻ đang kẹt giữa hai gọng kìm: một bên là thời tiết cực đoan do biến đổi khí hậu, một bên là thị trường giá cả bấp bênh. Họ thiếu công cụ hỗ trợ ra quyết định khoa học, dẫn đến việc bán non hoặc bón phân tưới nước sai thời điểm.

---

## Slide 3: Mục tiêu đề tài & Phạm vi giới hạn
* **Mục tiêu cốt lõi:**
  - Đồng hành cùng nông dân Tây Nguyên qua công cụ dự báo giá và khuyến nghị canh tác.
  - Hiện thực hóa hệ thống dựa trên **5 Trụ cột AI Bền vững** (Responsible AI).
* **Phạm vi địa lý:** 5 tỉnh Tây Nguyên (Đắk Lắk, Gia Lai, Đắk Nông, Lâm Đồng, Kon Tum) giai đoạn 2022–2025.
* **Tuyên bố miễn trừ trách nhiệm (Disclaimer):**
  - Hệ thống chỉ mang tính chất tham khảo học thuật.
  - Không thay thế lời khuyên tài chính thương mại hay tư vấn chuyên môn.
* **Speaker Notes:** 
  > Dự án hướng tới xây dựng một hệ thống AI thực tế, tập trung giải quyết bài toán của nông dân tại 5 tỉnh Tây Nguyên. Chúng tôi xác lập rõ disclaimer ngay từ đầu: AI là công cụ tham khảo hỗ trợ ra quyết định, không phải là quyết định thay cho người dân để đảm bảo tính an toàn về trách nhiệm pháp lý.

---

## Slide 4: Quy trình xử lý dữ liệu (Data-to-AI Flow)
* **Luồng dữ liệu:**
  ```text
  [Raw Daily Prices & Weather] -> [Weekly Dataset (2520 dòng)] -> [Monthly Dataset (576 dòng)]
  ```
* **Lý do chọn Monthly Dataset làm baseline:**
  - **Giảm nhiễu:** Bỏ qua biến động giá ảo trong ngày/tuần.
  - **Đồng bộ:** Chu kỳ thời tiết và sinh trưởng cây trồng tương thích tốt nhất theo tháng.
  - **Nguyên lý KISS:** Dữ liệu nhỏ gọn (576 dòng, 16 cột), mô hình huấn luyện cực nhanh, tiết kiệm điện năng tính toán.
* **Speaker Notes:**
  > Chúng tôi crawl dữ liệu giá cà phê thực tế hàng ngày và dữ liệu thời tiết. Sau khi lọc nhiễu, chúng tôi tổng hợp thành bộ dữ liệu tháng. Chọn dữ liệu tháng giúp nắm bắt xu hướng trung hạn tốt hơn và bám sát nguyên tắc KISS (Keep It Simple, Stupid), giúp mô hình chạy nhanh và gọn nhẹ.

---

## Slide 5: Kiến trúc hệ thống 4 tầng (Responsible AI Architecture)
* **Tầng 1: Data Layer** (Crawler thu thập tự động dữ liệu giá & thời tiết).
* **Tầng 2: Filtering Layer** (Nội suy giá trị thiếu; Lớp lọc khử nhiễu cảm biến lỗi).
* **Tầng 3: AI Core Layer** (Backend FastAPI; load model Random Forest Regressor; xác thực đầu vào qua Pydantic).
* **Tầng 4: Presentation Layer** (Giao diện di động nhẹ, hiển thị dự báo, giải thích & disclaimer).
* **Speaker Notes:**
  > Hệ thống được cấu trúc 4 tầng rõ rệt. Điểm đặc biệt nằm ở tầng thứ 2: Filtering Layer đóng vai trò bảo vệ hệ thống khỏi dữ liệu nhiễu trước khi đưa vào mô hình AI ở tầng 3. Tầng 4 được tối ưu hóa hiển thị trực quan thông tin giải thích mô hình cho người nông dân.

---

## Slide 6: Phương pháp Kỹ thuật & Đặc trưng
* **Mô hình:** Random Forest Regressor (Ensemble Bagging).
* **Kỹ thuật Đặc trưng (Feature Engineering):**
  - **Mã hóa chu kỳ tháng (Cyclic Encoding):** Biến đổi tháng qua hàm $sin$/$cos$ để giữ tính liền mạch thời gian (tháng 12 sát tháng 1).
  - **Đặc trưng tự hồi quy theo khu vực (Area-based Lags):** Nhóm theo huyện trước khi tính toán `lag_1d` (tháng trước), `lag_7d` và `rolling_avg_7d` để **chống rò rỉ dữ liệu (data leakage) địa lý**.
* **Speaker Notes:**
  > Chúng tôi chọn Random Forest vì tính ổn định và khả năng xuất Feature Importance. Khi làm feature engineering, chúng tôi xử lý các thuộc tính trễ giá theo từng huyện riêng biệt để tránh rò rỉ dữ liệu huyện này sang huyện khác, đảm bảo tính đúng đắn về mặt thống kê.

---

## Slide 7: Kết quả Định lượng tập Test 2025 (Reliability)
* **Kết quả thực nghiệm:**
  - **MAE:** 13,552 VND/kg
  - **RMSE:** 16,754 VND/kg
  - **R²:** -0.9044 (Trình bày trung thực số âm)
* **Giải thích R² âm (Giới hạn ngoại suy):**
  - Tập huấn luyện (2022-2024) có miền giá cà phê thấp (**35k - 70k VND/kg**).
  - Tập kiểm thử (2025) chứng kiến giá cà phê tăng vọt lịch sử (**100k - 120k VND/kg**).
  - Mô hình cây quyết định chỉ dự đoán tối đa mức trần đã học (~78k VND/kg), gây ra độ lệch lớn so với thực tế 2025.
* **Speaker Notes:**
  > Chúng tôi kiểm thử mô hình trên dữ liệu năm 2025. MAE đạt 13.5k VND/kg và R² bị âm. Chúng tôi trình bày trung thực chỉ số âm này. Nguyên nhân là năm 2025 giá cà phê thực tế tăng phi mã lên hơn 100k/kg, vượt ngoài miền dữ liệu huấn luyện 2022-2024. Mô hình cây quyết định không thể ngoại suy vượt trần tập train. Đây là giới hạn kỹ thuật quan trọng giúp chúng tôi nhận thức rõ tính tin cậy của mô hình khi gặp biến cố lớn.

---

## Slide 8: Responsible AI - Trục Robustness (Kháng nhiễu)
* **Bảo vệ 1: Validate request ở tầng API**
  - Pydantic schema chặn nhiệt độ, lượng mưa, độ ẩm, tháng, năm nằm ngoài range hợp lý.
  - API key bảo vệ `/predict` và `/model/info`.
* **Bảo vệ 2: Category guard theo model đã train**
  - `PredictorService` chỉ chấp nhận `province`, `area`, `coffee_type`, `dominant_soil_type` nằm trong tập feature của model.
  - Input ngoài tập train bị trả `422` thay vì dự báo âm thầm.
* **Speaker Notes:**
  > Trong repo hiện tại, lớp Robustness được hiện thực bằng validate ở tầng API và kiểm tra category theo model đã train. Nhóm không claim có một sanitizer riêng hay một lớp guardrails cho LLM production, vì các thành phần đó chưa có trong codebase này.

---

## Slide 9: Responsible AI - Trục Bias & Social Impact
* **Trục Bias (Thiên lệch dữ liệu địa lý):**
  - Tỉ lệ dữ liệu cào thật: Lâm Đồng/Kon Tum (100%), Đắk Lắk/Gia Lai (93%), Đắk Nông (39.6%).
  - *Giải pháp:* Hiển thị nhãn cảnh báo độ tin cậy thấp tại Đắk Nông, hướng dẫn nông dân tham chiếu khu vực lân cận.
* **Trục Social Impact (Tác động xã hội):**
  - **Phương pháp kiểm chứng:** Kiểm nghiệm thực tế giao diện di động React/Vite/Tailwind tại `frontend/` và kết quả phản hồi kèm disclaimer từ backend.
  - **Kết quả thực tiễn:** Giao diện có màn chào, menu chọn tác vụ, nút bấm lớn, tương phản cao, tách riêng luồng Dự báo Giá và Khuyến nghị Canh tác.
  - **Hỗ trợ ngoại tuyến:** Lưu trữ bằng `localStorage` và xem chi tiết lịch sử (đối chiếu input, kết quả, lý do và disclaimer) khi mạng chập chờn.
  - **Ràng buộc an toàn:** Chân trang luôn bắt buộc hiển thị Disclaimer để tránh nông dân ra quyết định tài chính sai lệch.
* **Speaker Notes:**
  > Về trục Bias, chúng tôi phát hiện dữ liệu Đắk Nông cào được rất ít (chỉ 39.6%). Do đó hệ thống sẽ cảnh báo nông dân Đắk Nông rằng độ tin cậy dự báo vùng này thấp hơn Lâm Đồng để tránh họ ra quyết định sai. Về tác động xã hội (Social Impact), chúng tôi kiểm nghiệm thực tế giao diện di động React/Vite/Tailwind kết nối backend. Giao diện được tối ưu hóa mobile-first với màn chào rõ ràng, nút lớn tương phản cao chống chói nắng, hỗ trợ lưu trữ cục bộ qua localStorage để xem lịch sử khi mất mạng, và đặc biệt chân trang luôn hiển thị Disclaimer bắt buộc nhằm tránh các rủi ro quyết định kinh tế sai lệch cho người nông dân.

---

## Slide 10: Responsible AI - Trục Transparency (Tính minh bạch)
* **Giải thích mô hình qua Feature Importance:**
  - Đà tăng giá thị trường gần đây (`rolling_avg_7d`): **72.8%**
  - Giá tháng trước (`lag_1d`): **22.2%**
  - Các yếu tố khí hậu ngắn hạn (nhiệt độ, lượng mưa): **< 1%**
* **Ý nghĩa:**
  - AI minh bạch lý do dự báo: Giá cà phê phụ thuộc vào đà giá lịch sử, tránh để nông dân hiểu sai rằng thời tiết thay đổi nhẹ sẽ thay đổi ngay lập tức giá bán ngày mai.
* **Speaker Notes:**
  > Với trục Transparency, mô hình bóc tách rõ tầm ảnh hưởng của các biến. 72.8% giá trị dự báo được quyết định bởi trung bình trượt giá quá khứ gần. Điều này minh bạch hóa thuật toán, giúp nông dân hiểu rằng đà giá thị trường là yếu tố quyết định chính chứ không phải các yếu tố thời tiết ngắn hạn, giúp họ bình tĩnh phân tích thông tin.

---

## Slide 11: Hiện thực Giao diện di động (Mobile-first UI)
* **Tối ưu trải nghiệm:** Giao diện React/Vite tối ưu hóa theo phong cách Neo-Brutalism (tương phản cao), phân tách luồng Giá và Canh tác rõ ràng.
* **Tương tác trực quan & an toàn:** 
  - Nút bấm và ô nhập liệu lớn (>= 48px) dễ thao tác, độ tương phản cao chống chói nắng.
  - Hỗ trợ lưu kết quả dự báo ngoại tuyến (Offline Storage) qua `localStorage`.
* **Định dạng hiển thị:** Kết quả trực quan gồm giá dự báo, khoảng dao động, lý giải thanh đóng góp đặc trưng và khuyến nghị canh tác tiếng Việt dễ hiểu.
* **Speaker Notes:**
  > Chúng tôi đã hiện thực một giao diện di động bằng React. Giao diện phân tách tính năng thành các luồng độc lập, bám sát mental model của người nông dân. Ứng dụng hỗ trợ lưu trữ cục bộ để xem lại dự báo khi không có mạng, thiết kế theo triết lý Social Impact với các nút bấm lớn dễ ấn, biểu đồ giải thích trực quan và tích hợp đầy đủ cảnh báo thiên lệch dữ liệu.

---

## Slide 12: Kết luận & Hướng phát triển
* **Kết luận:**
  - Hệ thống baseline đã vận hành end-to-end, lồng ghép thành công tư duy AI bền vững vào cấu trúc code.
  - Báo cáo trung thực các hạn chế kỹ thuật (R² âm, bias địa lý).
* **Hướng phát triển:**
  - Mở rộng dữ liệu lịch sử trước năm 2022.
  - So sánh Random Forest với các mô hình hỗ trợ học xu hướng tốt hơn (Prophet, XGBoost, LSTM).
  - Huấn luyện mô hình localized riêng cho từng tiểu vùng.
* **Speaker Notes:**
  > Tóm lại, dự án DT10 đã hoàn thiện khung baseline vững chắc và tích hợp Responsible AI vào code thực tế. Trong tương lai, chúng tôi sẽ mở rộng dữ liệu và thử nghiệm các mô hình có khả năng học xu hướng tốt hơn như Prophet hay XGBoost để giải quyết triệt để bài toán ngoại suy khi thị trường biến động cực đoan. Xin cảm ơn Thầy và các bạn đã lắng nghe.

---

## Slide 13: Kết luận & Tài liệu tham khảo
* **Kết luận:**
  - Hệ thống baseline AI DT10 đã vận hành thực tế end-to-end, tích hợp thành công 5 Trụ cột AI Bền vững vào cấu trúc phần mềm (từ backend đến frontend).
  - Đã nhận diện và báo cáo trung thực các hạn chế về mặt thuật toán (giới hạn ngoại suy dẫn đến R² âm) và sự thiên lệch địa lý do dữ liệu.
* **Tài liệu tham khảo nổi bật:**
  - Breiman, L. (2001). *Random Forests*. Machine Learning.
  - *Scikit-learn: Machine Learning in Python*.
  - Microsoft Responsible AI Standard.
  - Nguồn dữ liệu: Trang tin thị trường nông sản Việt Nam và Open-Meteo API.
* **Speaker Notes:**
  > Tổng kết ngắn gọn giá trị cốt lõi nhóm đã đạt được và trích dẫn các nền tảng khoa học nhóm đã sử dụng.

---

## Slide 14: Q&A và Lời cảm ơn (Thank You)
* **Tiêu đề:** Xin chân thành cảm ơn!
* **Nội dung:** Cảm ơn TS. Phan Thế Duy và các bạn đã chú ý lắng nghe phần trình bày đồ án Đề tài DT10 của Nhóm 10.
* **Q&A:** Xin mời Thầy và các bạn đặt câu hỏi.
* **Speaker Notes:**
  > Tạm dừng, mỉm cười và chuẩn bị tinh thần trả lời câu hỏi phản biện từ hội đồng.
