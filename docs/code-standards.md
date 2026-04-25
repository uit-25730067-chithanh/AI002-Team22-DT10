# 🛠 Tiêu chuẩn Code & Quy tắc (Code Standards)

Nhằm đảm bảo sự đồng bộ trong team và bám sát triết lý **Sustainable AI Design Thinking**, tất cả thành viên **Team 10** thống nhất tuân thủ các quy tắc sau:

## 1. Nguyên tắc cốt lõi

- **KISS & YAGNI:** Giữ mọi thứ đơn giản. Không sử dụng database phức tạp (chỉ dùng CSV/SQLite) hoặc các mô hình Deep Learning "hộp đen" nếu không thực sự cần thiết.
- **Tuân thủ 5 Trụ cột:** Mỗi dòng code, mỗi module phải xem xét tác động đến 5 yếu tố: Reliability, Bias, Robustness, Social Impact, và Transparency.

## 2. Git Workflow

- **Nhánh `main`:** Cần luôn sạch sẽ, chứa code có thể chạy được và báo cáo hoàn chỉnh. (Tuyệt đối không push thẳng lên nhánh này).
- **Thực hiện công việc:** Tạo nhánh `feature/<tên-việc>`, ví dụ: `feature/setup-fastapi`, `feature/random-forest-baseline`.
- **Hợp nhất:** Cần tạo Pull Request (PR) và cho **Phúc**, **Thanh**, **Thịnh**, **Sơn** review trước khi gộp vào `main`.
- **Commit:** Sử dụng **Conventional Commits** (ví dụ: `feat:`, `fix:`, `docs:`, `refactor:`). Commit thường xuyên, mỗi commit chỉ chứa một thay đổi nhỏ (atomic).
- **Quy ước Scope (khuyến nghị):** Để dễ trace từ commit -> plan, nên dùng scope mô tả vị trí task:
  - Format: `type(phase{N}/task{M}/{scope}): description`
  - Ví dụ: `feat(phase1/task1_2/data): add mock data generator`, `docs(phase2/task2_5/test): add stress test report`
  - Nếu commit không thuộc task plan cụ thể, scope có thể ngắn gọn như `feat(api): add health endpoint`.

## 3. Tiêu chuẩn Mã nguồn & Ngôn ngữ (Python - Team 2)

- **Đặt tên (Naming):** Biến, hàm, lớp **bắt buộc 100% bằng Tiếng Anh** (ví dụ: `train_model`, `predict_price`).
- **Chú thích (Comments):**
  - **Tiếng Anh (Ưu tiên):** Dùng cho các chú thích ngắn gọn (What/How), ví dụ: `# Initialize RandomForestClassifier`.
  - **Tiếng Việt (Linh hoạt):** Được phép dùng để giải thích các **logic xử lý ML phức tạp hoặc lý do (Why)** đằng sau việc xử lý dữ liệu để đảm bảo các thành viên trong team đều hiểu (minh bạch - Transparency).
- **Định dạng:** Tuân thủ phong cách code **PEP 8** (khuyến nghị dùng `black`, `ruff format` hoặc các công cụ auto-format).
- **Kiểu dữ liệu:** **Bắt buộc dùng Type hinting** (đặc biệt trong các route của FastAPI và model của Pydantic).

## 4. Quản lý Tệp

- Mọi file sinh ra tạm thời, nháp cá nhân, kết quả test AI đặt ở thư mục `tmp/` hoặc `tests/ai-tests/` (đã được gitignore).
- Các dữ liệu thô và file xử lý trung gian lưu tại `data/` và tuân thủ quy tắc không push file data lớn lên git.
- Các báo cáo hàng tuần hoặc tài liệu chính thức cần được lưu trong folder `docs/`.

## 5. Chính sách AI và Quality Control

- **Sử dụng AI:** Chúng ta sử dụng AI (Claude/ChatGPT/Copilot/Gemini/etc...) để lập trình, nghiên cứu và lấy tài liệu tham khảo. Tuy nhiên, **KHÔNG** nhắm mắt copy-paste mà không kiểm chứng.
- **Làm chủ mã nguồn:** Owner của đoạn code / logic AI / API cần hiểu rõ và giải thích **đạt 100% logic** cho reviewer trước khi PR được duyệt.

## 6. Tiêu chuẩn Ký hiệu Toán học (LaTeX Standards) - Nếu có

Để đảm bảo các công thức toán học (ví dụ: Loss function, Metrics) được hiển thị chính xác và đồng nhất trên GitHub:

- **Nhóm chỉ số dưới (Subscript Grouping):** Luôn sử dụng ngoặc nhọn `{}` cho tất cả các chỉ số dưới. Đúng: `y_{i}`, `\hat{y}_{i}`. Sai: `y_i`.
- **Định dạng Khối công thức:** Các khối công thức dùng cặp ký hiệu `$$` phải được đặt trên dòng riêng và **bắt buộc có dòng trống** bao quanh.
- **Sử dụng ký hiệu chuẩn:** Không dùng ký tự Unicode toán học (như `θ`, `∇`) trực tiếp trong file Markdown. Luôn sử dụng lệnh LaTeX tương ứng.
- **Đồng bộ Math-to-Code:** Khi đặt tên biến trong code, cố gắng giữ sự tương quan với công thức (ví dụ: `y_pred` cho $\hat{y}$).
