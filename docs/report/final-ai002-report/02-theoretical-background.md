# CHƯƠNG 2: CƠ SỞ LÝ THUYẾT

## 2.1. Học có giám sát (Supervised Learning)

Học có giám sát (Supervised Learning) là một trong những phương pháp nền tảng của Trí tuệ Nhân tạo và Học máy. Phương pháp này hoạt động dựa trên một tập dữ liệu huấn luyện đã được gán nhãn trước, biểu diễn dưới dạng các cặp dữ liệu:
$$D = \{(x_{1}, y_{1}), (x_{2}, y_{2}), \dots, (x_{n}, y_{n})\}$$
Trong đó:
- $x_{i} \in \mathbb{R}^d$ đại diện cho vector đặc trưng đầu vào (các biến thời tiết, thông số đất, đặc trưng lịch sử).
- $y_{i}$ đại diện cho nhãn hoặc giá trị mục tiêu đầu ra cần dự báo (giá cà phê tại thời điểm tương ứng).

Mục tiêu của thuật toán học có giám sát là tìm kiếm một hàm ánh xạ $f: X \to Y$ sao cho sai số dự báo $f(x_{i}) - y_{i}$ trên tập dữ liệu thử nghiệm là nhỏ nhất. Đối với bài toán dự báo giá cà phê, vì giá trị mục tiêu $y_{i}$ là một biến liên tục (continuous variable) nằm trong tập số thực, bài toán này được phân loại vào nhóm **Học hồi quy (Regression)**.

## 2.2. Thuật toán Random Forest Regression

Thuật toán **Random Forest** (Rừng ngẫu nhiên), giới thiệu bởi Leo Breiman vào năm 2001, là một thuật toán học máy mạnh mẽ thuộc nhóm **Học kết hợp (Ensemble Learning)**. Thuật toán này hoạt động bằng cách xây dựng và kết hợp dự đoán từ một số lượng lớn các Cây Quyết định (Decision Trees) độc lập.

```text
               [ Vector Đặc Trưng Đầu Vào x ]
              /              |              \
      [Cây Quyết Định 1] [Cây Quyết Định 2] [Cây Quyết Định K]
             |               |               |
         Dự đoán y1      Dự đoán y2      Dự đoán yK
              \              |              /
               [ Trung Bình Cộng Dự Đoán ]
                             |
                     [ Kết quả cuối ŷ ]
```

Nguyên lý hoạt động của Random Forest dựa trên hai cơ chế cốt lõi:
1. **Bagging (Bootstrap Aggregating):** Mỗi cây quyết định trong rừng được huấn luyện trên một tập dữ liệu con (bootstrap sample) được chọn ngẫu nhiên bằng cách lấy mẫu có hoàn lại (sampling with replacement) từ tập huấn luyện gốc.
2. **Chọn đặc trưng ngẫu nhiên (Random Feature Selection):** Tại mỗi nút phân nhánh của mỗi cây, thuật toán chỉ chọn ngẫu nhiên một nhóm nhỏ các đặc trưng thay vì xem xét toàn bộ các đặc trưng có sẵn. Điều này làm giảm sự tương quan giữa các cây quyết định trong rừng.

Công thức dự báo cuối cùng của Random Forest Regression cho một mẫu thử nghiệm mới $x$ là trung bình cộng kết quả dự báo từ $K$ cây thành phần:
$$\hat{y} = \frac{1}{K} \sum_{k=1}^{K} T_{k}(x)$$
Trong đó $T_{k}(x)$ là giá trị dự đoán của cây quyết định thứ $k$.

**Lý do lựa chọn thuật toán Random Forest:**
- **Kiểm soát overfitting tốt:** Việc trung bình hóa kết quả của nhiều cây độc lập giúp giảm phương sai (variance) của mô hình mà không làm tăng độ lệch (bias).
- **Đánh giá mức độ quan trọng của đặc trưng (Feature Importance):** Cung cấp cơ chế định lượng tầm ảnh hưởng của từng đặc trưng đầu vào thông qua chỉ số giảm độ tinh khiết trung bình (Mean Decrease Impurity - MDI), hỗ trợ đắc lực cho trụ cột minh bạch (Explainability).
- **Khả năng làm việc với dữ liệu phi tuyến:** Nắm bắt tốt các mối quan hệ tương tác phức tạp giữa thời tiết và giá nông sản mà không yêu cầu chuẩn hóa dữ liệu đầu vào quá phức tạp (KISS).

## 2.3. Các độ đo đánh giá mô hình

Để đánh giá định lượng chất lượng dự báo của mô hình trên tập kiểm thử độc lập, đồ án áp dụng ba độ đo tiêu chuẩn trong bài toán hồi quy:

### Sai số Tuyệt đối Trung bình (Mean Absolute Error - MAE)

MAE đo lường độ lớn trung bình của các sai số dự báo mà không quan tâm đến hướng (dương hay âm) của sai số:
$$MAE = \frac{1}{n} \sum_{i=1}^{n} |y_{i} - \hat{y}_{i}|$$
MAE trực quan vì nó phản ánh trực tiếp sai số giá trung bình theo đơn vị VND/kg, giúp nông dân dễ dàng hình dung mức độ chênh lệch thực tế.

### Sai số Bình phương Trung bình dạng Căn (Root Mean Squared Error - RMSE)

RMSE đo lường độ lệch chuẩn của các phần dư (residuals). Nó phạt nặng các sai số dự báo lớn do có bước bình phương:
$$RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_{i} - \hat{y}_{i})^2}$$
RMSE giúp nhóm phát triển phát hiện các trường hợp dự báo sai lệch nghiêm trọng (outliers trong sai số).

### Hệ số Xác định (R-squared - $R^2$)

$R^2$ biểu thị tỷ lệ phương sai của biến mục tiêu được giải thích bởi các biến độc lập trong mô hình:
$$R^2 = 1 - \frac{\sum_{i=1}^{n} (y_{i} - \hat{y}_{i})^2}{\sum_{i=1}^{n} (y_{i} - \bar{y})^2}$$
Trong đó $\bar{y}$ là giá trị trung bình của dữ liệu thực tế:
$$\bar{y} = \frac{1}{n} \sum_{i=1}^{n} y_{i}$$
Giá trị $R^2 \approx 1$ thể hiện mô hình giải thích hoàn hảo dữ liệu; $R^2 \approx 0$ nghĩa là mô hình dự báo không tốt hơn giá trị trung bình; $R^2 < 0$ xảy ra khi mô hình dự báo tệ hơn cả việc sử dụng một hằng số làm kết quả dự đoán (chỉ ra sự dịch chuyển phân phối dữ liệu nghiêm trọng).

## 2.4. Khung lý thuyết AI có trách nhiệm (Responsible AI)

Trọng tâm của môn học AI002 là việc áp dụng tư duy thiết kế AI bền vững thông qua 5 trụ cột Responsible AI:

1. **Reliability (Tính tin cậy):** Đảm bảo hệ thống vận hành ổn định trên thực tế. Đánh giá độ tin cậy bằng các độ đo định lượng rõ ràng, áp dụng cơ chế phân chia dữ liệu theo thời gian (Temporal Split) để chống rò rỉ thông tin tương lai, phản ánh đúng hiệu năng thực tế của mô hình khi triển khai.
2. **Bias & Fairness (Tính thiên lệch và công bằng):** Đánh giá sự khác biệt về chất lượng dữ liệu giữa các địa phương nghiên cứu. Cảnh báo rõ ràng cho nông dân ở những vùng có độ phủ dữ liệu thấp (thiếu giá thực tế) để tránh đưa ra quyết định sai lầm.
3. **Robustness (Kháng nhiễu):** Đảm bảo hệ thống không bị sập hay trả về kết quả phi lý khi gặp dữ liệu lỗi (do cảm biến thời tiết hỏng, mất dữ liệu mạng) hoặc các nỗ lực tấn công bẻ lái từ người dùng (prompt injection).
4. **Social Impact (Tác động xã hội):** Đặt lợi ích của nhóm người dùng yếu thế (nông dân nhỏ lẻ) làm trung tâm. Thiết kế giao diện di động nhẹ, dễ truy cập qua kết nối mạng 3G yếu, tích hợp các điều khoản miễn trừ trách nhiệm (disclaimer) rõ ràng để bảo vệ người nông dân khỏi các rủi ro tài chính.
5. **Explainability (Tính minh bạch / giải thích được):** Cung cấp các thông tin bóc tách độ ảnh hưởng của đặc trưng (Feature Importance), giúp người dùng hiểu rõ tại sao mô hình đưa ra mức dự báo đó (ví dụ: do giá tháng trước tăng hay do lượng mưa tháng này giảm).
