# 📊 Báo cáo Tuần 1 – Phân tích giá cà phê (Phước Thịnh)

---

## 1. Mục tiêu

- Xác định các yếu tố ảnh hưởng đến giá cà phê  
- Xác định mức giá quan trọng nhất để làm mục tiêu dự báo (target)  

---

## 2. Các yếu tố ảnh hưởng đến giá cà phê

Giá cà phê chịu tác động bởi nhiều yếu tố, có thể chia thành các nhóm sau:

### 2.1 Yếu tố kinh tế (Economic Factors)
- Giá cà phê kỳ hạn Robusta (thị trường London)  
- Giá cà phê kỳ hạn Arabica (thị trường New York)  
- Tỷ giá USD/VND  

👉 Biến động giá thế giới ảnh hưởng trực tiếp đến giá cà phê nội địa.

---

### 2.2 Yếu tố nông nghiệp (Agricultural Factors)
- Sản lượng cà phê  
- Diện tích trồng  
- Năng suất  

👉 Khi nguồn cung tăng → giá có xu hướng giảm và ngược lại.

---

### 2.3 Yếu tố khí hậu (Climate Factors)
- Lượng mưa  
- Nhiệt độ  
- Chỉ số ENSO (El Niño / La Niña)  

👉 Thời tiết cực đoan có thể làm giảm năng suất và đẩy giá tăng.

---

### 2.4 Yếu tố chi phí & cạnh tranh (Cost & Competition)
- Giá phân bón  
- Chi phí lao động  
- Giá nhiên liệu  
- Cây trồng cạnh tranh (tiêu, cao su, …)  

👉 Chi phí sản xuất tăng sẽ làm giá cà phê tăng theo.

---

### 2.5 Yếu tố chính sách (Policy Factors)
- Thuế xuất khẩu  
- Hiệp định thương mại (EVFTA, CPTPP)  
- Quy định môi trường (EUDR)  

👉 Chính sách có thể ảnh hưởng đến chi phí và khả năng xuất khẩu.

---

## 3. Xác định giá mục tiêu (Target Price)

👉 **Giá được chọn: Giá thu mua tại vườn (farm-gate price, đơn vị VND/kg)**  

### Lý do lựa chọn:
- Phản ánh trực tiếp thu nhập của nông dân  
- Thể hiện rõ giá thực tế trên thị trường  
- Phù hợp để làm biến mục tiêu (target/label) cho mô hình AI  

👉 Các mức giá khác (giá kỳ hạn, tỷ giá, …) sẽ được sử dụng làm biến đầu vào (features).

---

## 4. Định hướng dữ liệu (Phục vụ xây dựng dataset)

Để phục vụ xây dựng mô hình, dataset cần bao gồm:

- Giá thu mua tại vườn (biến mục tiêu – target)  
- Giá cà phê thế giới (Robusta, Arabica)  
- Tỷ giá USD/VND  
- Dữ liệu thời tiết (lượng mưa, nhiệt độ, ENSO)  
- Dữ liệu sản lượng và nông nghiệp  

👉 Dataset sẽ sử dụng **giá tại vườn làm target** và các yếu tố còn lại làm **features** cho mô hình Machine Learning.

👉 Phần nguồn dữ liệu cụ thể và phương pháp thu thập (API/Web Scraping) sẽ do nhóm phụ trách dữ liệu triển khai.

---

## 5. Kết luận

Giá cà phê chủ yếu phụ thuộc vào:
- Cung (sản lượng)  
- Cầu (thị trường)  
- Điều kiện thời tiết  

👉 Giá thu mua tại vườn là lựa chọn phù hợp nhất để làm mục tiêu dự báo.

---
