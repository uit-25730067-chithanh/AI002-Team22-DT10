# Kịch bản thuyết trình phần của Sơn (Slide 10 - Hết)

## Phạm vi slide của Sơn

- Slide 10: Responsible AI - Trục Robustness (Kháng nhiễu)
- Slide 11: Responsible AI - Trục Bias & Social Impact
- Slide 12: Responsible AI - Trục Transparency (Tính minh bạch)
- Slide 13: Hiện thực Giao diện di động (Mobile-first UI)
- Slide 14: Kết luận & Hướng phát triển
- Slide 15: Kết luận & Tài liệu tham khảo
- Slide 16: Q&A và Lời cảm ơn (Thank You)

## Lưu ý về thời gian

Tổng thời gian trình bày là 10 phút, chia đôi mỗi người khoảng 5 phút. Nội dung dưới đây được thiết kế với độ dài vừa phải, nhịp điệu tự nhiên, nhấn mạnh vào các thông điệp cốt lõi để anh có thể nói thoải mái trong vòng 4-5 phút mà không bị gấp.

## Hướng dẫn sử dụng

1. Ký hiệu **[click]** dùng để anh bấm chuyển hiệu ứng hoặc qua slide.
2. Các phần **> Backup Q&A** là câu trả lời an toàn chuẩn bị sẵn nếu Thầy hoặc hội đồng hỏi xoáy vào điểm yếu.
3. Chú ý giữ giọng điệu tự tin, đặc biệt khi nói về điểm yếu của mô hình (R² âm), vì đồ án này đề cao "sự trung thực và AI có trách nhiệm" hơn là một con số độ chính xác ảo tưởng.

---

## Slide 10: Responsible AI - Trục Robustness (Kháng nhiễu)

**[click]** Dạ vâng, xin cảm ơn phần trình bày về kiến trúc và kết quả mô hình của Thanh.

Tiếp theo, em xin đi vào giá trị cốt lõi của đề tài: áp dụng **5 Trụ cột AI Bền vững (Responsible AI)** vào thực tế. Trụ cột đầu tiên là **Robustness - Tính kháng nhiễu**.

Thực tế là, dữ liệu đẩy lên app đôi khi sẽ bị sai lệch cực đoan. Vì vậy, để ngăn hệ thống nhắm mắt dự báo sai, nhóm đã thiết lập 2 lớp khiên bảo vệ.

- **[click] Lớp 1:** Dùng Pydantic ở tầng API chặn đứng dữ liệu phi lý ngay từ cửa (ví dụ nhiệt độ âm ở Tây Nguyên).
- **[click] Lớp 2:** Dùng `Category guard`. Nếu người dùng nhập tỉnh ngoài vùng Tây Nguyên, API lập tức báo lỗi 422 từ chối dự báo, thay vì đưa ra kết quả sai lệch.

Để kiểm chứng, tụi em đã chạy **Stress Test** bằng dữ liệu cực đoan. Kết quả rất rõ ràng: khi ép hệ thống chịu mức nhiệt độ sốc 45 độ C, sai số gần như bất động (tăng 0.0%). Tuy nhiên, khi tạo ra cú sốc giá, sai số lập tức vọt lên gần 70%.
Qua đó chứng minh được rằng, hệ thống có sức chống chịu cực kỳ vững vàng trước nắng nóng bất thường, nhưng lại khá nhạy cảm với sốc giá.

> **Chốt slide:** Tinh thần ở đây là: "Thà từ chối dự báo, còn hơn đưa ra một dự báo sai khiến nông dân chịu thiệt hại".

---

## Slide 11: Responsible AI - Trục Bias & Social Impact

**[click]** Trụ cột tiếp theo là **Bias (Sự thiên lệch)** và **Social Impact (Tác động xã hội)**.

Đầu tiên là về dữ liệu, tỷ lệ phân bổ ở các vùng là không đồng đều. Lấy ví dụ, Kon Tum hay Lâm Đồng thu thập được gần 90% dữ liệu thực, nhưng Đắk Nông thì chỉ được khoảng 60%.
Do đó, thay vì che giấu, nhóm chọn cách minh bạch hóa. Cụ thể là khi tra cứu tại các vùng thiếu hụt như Gia Nghĩa, Chư Prông, Cư M'gar hay Đắk R'lấp, ứng dụng sẽ tự động hiện nhãn cảnh báo: _"Độ tin cậy thấp, bà con nên tham khảo vùng lân cận"_.

**[click]** Chuyển sang khía cạnh **Tác động xã hội (Social Impact)**, mục tiêu của nhóm là đảm bảo AI thực sự đến được tay người nông dân.
Vì vậy, thay vì làm các hệ thống phức tạp, nhóm chọn hướng Mobile-first. Mọi thiết kế từ nút bấm lớn, chế độ Offline cho đến các cảnh báo an toàn đều hướng tới việc hỗ trợ và bảo vệ bà con tốt nhất. Cụ thể giao diện đó trông như thế nào, em sẽ trình bày rõ hơn ở Slide 13.

---

## Slide 12: Responsible AI - Trục Transparency (Tính minh bạch)

**[click]** Trụ cột thứ tư là **Transparency - Tính minh bạch**. Nghĩa là AI không được làm "hộp đen", mà nó phải giải thích được TẠI SAO lại đưa ra mức giá đó.

Để làm được điều này, nhóm đã dùng kỹ thuật Feature Importance để bóc tách, và kết quả cho thấy:

- **Hơn 50%** quyết định đến từ giá tháng trước.
- **Gần 47%** đến từ đà tăng giá 7 ngày qua.
- **[click]** Đáng chú ý là, các yếu tố khí hậu như nhiệt độ, lượng mưa chỉ đóng góp **khoảng 2.6%** vào biến động giá ngắn hạn.

Chính việc minh bạch hóa con số này sẽ giúp nông dân dập tắt được các "tin đồn" giá ảo do thời tiết. Qua đó AI chứng minh rõ một điều: Giá cà phê phụ thuộc đà thị trường vĩ mô nhiều hơn, chứ không phải là do thời tiết ngày mai.

> **Backup Q&A / Câu hỏi hội đồng:** Nếu Thầy hỏi _"Vậy đưa thời tiết vào làm gì nếu nó đóng góp ít?"_
> **Trả lời:** "Dạ thưa Thầy, thời tiết ngắn hạn ít tác động lên GIÁ, nhưng nó lại tác động trực tiếp lên NĂNG SUẤT và KẾ HOẠCH CANH TÁC (lịch tưới nước, bón phân). Việc bóc tách này giúp nông dân phân định: nhìn giá thì theo dõi thị trường, còn nhìn thời tiết là lo canh tác ạ."

---

## Slide 13: Hiện thực Giao diện di động (Mobile-first UI)

**[click]** Và phần tiếp theo trên màn hình đây chính là tổng quan về **Giao diện di động (Mobile UI)** mà em vừa nhắc tới.

Về mặt thiết kế, nhóm áp dụng phong cách Neo-Brutalism. Trọng tâm không phải là sự bóng bẩy, mà là tính **thực dụng**. Với độ tương phản cao và nút chạm lớn, giao diện này cực kỳ dễ đọc và dễ thao tác ngay cả dưới cái nắng gắt ngoài rẫy.

Về luồng sử dụng, hệ thống phân tách biệt lập hoàn toàn hai tác vụ: Dự báo Giá và Tư vấn Canh tác.
Bên cạnh đó, để hỗ trợ môi trường mạng 3G yếu hoặc chập chờn, nhóm đã tích hợp bộ nhớ Offline để xem lại lịch sử. Cuối cùng, nhằm minh bạch đầu ra và đảm bảo an toàn, ứng dụng luôn hiển thị rõ khuyến nghị và neo cứng một dòng thông báo **Tuyên bố miễn trừ trách nhiệm** ở cuối màn hình.

---

## Slide 14 & 15: Kết luận & Hướng phát triển

**[click]** Tóm lại ở phần kết luận, nhóm 22 đã xây dựng thành công một **hệ thống baseline AI vận hành end-to-end**, chạy thực tế từ Backend cho tới Frontend. Và điều quan trọng nhất là tụi em đã "nhúng" trọn vẹn triết lý **AI Bền vững (Responsible AI)** vào trong hệ thống.

Tuy nhiên, về mặt hạn chế, mô hình Random Forest đã gặp khó khăn khi ngoại suy sự kiện giá bùng nổ năm 2025, khiến R² bị âm. Mặc dù vậy, nhóm xem đây là một sự phản ánh trung thực về giới hạn của thuật toán trước biến cố thiên nga đen (Black Swan).

**[click]** Dựa vào đó, hướng phát triển tương lai của nhóm sẽ bao gồm:

1. Thứ nhất, thu thập dữ liệu lịch sử sâu hơn về trước năm 2020.
2. Thứ hai, thử nghiệm các thuật toán chuỗi thời gian mạnh hơn như **Prophet** hay **XGBoost** để khắc phục triệt để lỗi ngoại suy.
3. Và cuối cùng là xây dựng mô hình Localized, tinh chỉnh riêng cho từng vùng thổ nhưỡng.

**[click]** Trên slide là các tài liệu tham khảo cốt lõi, đặc biệt là bộ tiêu chuẩn Responsible AI của Microsoft.

---

## Slide 16: Q&A và Lời cảm ơn (Thank You)

**[click]** Dạ vâng, bài báo cáo của nhóm 22 đến đây là kết thúc.

Nhóm xin cảm ơn TS. Phan Thế Duy đã truyền đạt những tư duy nền tảng cực kỳ thực tế trong môn học này. Cảm ơn Thầy và các bạn đã lắng nghe.

Sau đây, nhóm rất mong nhận được những góp ý và phản biện từ hội đồng ạ. Xin kính mời Thầy!
_(Mỉm cười, gật đầu chào và chuẩn bị tinh thần trả lời)_
