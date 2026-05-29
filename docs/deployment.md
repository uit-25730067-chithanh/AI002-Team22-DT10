# Hướng Triển Khai Backend trên Render

## Tổng quan

Backend FastAPI được triển khai trên Render Web Service để cung cấp API dự báo giá cà phê cho frontend và demo. Tài liệu này mô tả cấu hình, quy trình setup, CI/CD workflow và bảo mật API.

## Cấu hình Platform

| Thông số       | Giá trị                                                |
| -------------- | ------------------------------------------------------ |
| Platform       | Render Web Service                                     |
| Account        | `25730067@ms.uit.edu.vn`                               |
| Service Name   | `ai002-coffee-api`                                     |
| Runtime        | Python                                                 |
| Build Command  | `pip install -r requirements.txt`                      |
| Start Command  | `uvicorn backend.main:app --host 0.0.0.0 --port $PORT` |
| Production URL | `https://ai002-coffee-api.onrender.com`                |

## CI/CD GitHub Actions

Backend sử dụng GitHub Actions để tự động test và deploy lên Render:

### Workflow Structure

```yaml
# .github/workflows/ci-cd.yml
on:
  push:
    branches: [main]
    paths: ["backend/**", "model/**", "requirements.txt"]
  pull_request:
    branches: [main]
    paths: ["backend/**", "model/**", "requirements.txt"]

jobs:
  test:
    - Chạy pytest tests/ai-tests/
    - Chạy flake8 lint (max-line-length=120)
    - Chạy bandit security scan (không fail build)
  deploy:
    - Chỉ chạy khi test pass và push vào main
    - Gọi Render deploy hook URL
```

### Path Filter

Workflow chỉ trigger khi thay đổi:

- `backend/**` - Backend API code
- `model/**` - Model training code
- `requirements.txt` - Dependencies

Thay đổi frontend, crawler, docs sẽ không trigger deploy.

### Setup GitHub Secret

1. Vào GitHub repo: Settings → Secrets and variables → Actions
2. Thêm secret:
   - Name: `RENDER_DEPLOY_HOOK_URL`
   - Value: `<render-deploy-hook-url>`

### Disable Render Native Integration

**QUAN TRỌNG:** Tắt Render native GitHub integration để tránh double deploy:

1. Đăng nhập Render dashboard với account `25730067@ms.uit.edu.vn`
2. Vào service `ai002-coffee-api`
3. Tab "Events" → tìm GitHub integration settings
4. Disable native GitHub integration (disconnect repo hoặc turn off auto-deploy)

## Quy trình Setup trên Render

### Bước 1: Kết nối Repository

1. Đăng nhập vào Render dashboard với account `25730067@ms.uit.edu.vn`
2. Kết nối GitHub repository `uit-25730053-baophuc/AI002_BaiTapNhom`

### Bước 2: Tạo Web Service

1. Tạo New Web Service
2. Cấu hình thủ công (không dùng render.yaml):
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

### Bước 3: Cấu hình Environment Variable

1. Trong tab Environment, thêm biến:
   - Key: `AI002_API_KEY`
   - Value: Khóa API private cho team demo (không commit vào repo)
2. Lưu cấu hình

### Bước 4: Triển khai

1. Setup GitHub secret `RENDER_DEPLOY_HOOK_URL`
2. Disable Render native GitHub integration
3. Push code vào main → GitHub Actions tự động test và deploy
4. Chờ build thành công và service running
5. Xác nhận production URL

## Bảo mật Endpoint

| Endpoint        | Method | Protected | Auth Required | Mô tả                                        |
| --------------- | ------ | --------- | ------------- | -------------------------------------------- |
| `/`             | GET    | Không     | None          | Trang chào công khai                         |
| `/health`       | GET    | Không     | None          | Health check công khai cho Render monitoring |
| `/docs`         | GET    | Không     | None          | Swagger UI công khai                         |
| `/openapi.json` | GET    | Không     | None          | OpenAPI spec công khai                       |
| `/model/info`   | GET    | Có        | API Key       | Trả về metadata model, features, version     |
| `/predict`      | POST   | Có        | API Key       | Trả về dự báo giá + khuyến nghị canh tác     |

## Cấu hình API Key

| Thông số                      | Giá trị                                             |
| ----------------------------- | --------------------------------------------------- |
| Env Var Name                  | `AI002_API_KEY`                                     |
| Header Name                   | `X-API-Key`                                         |
| Hành vi khi key sai           | `401 Unauthorized`                                  |
| Hành vi khi env var không set | `503 Service Unavailable`                           |
| Phương thức so sánh           | Constant-time comparison (`secrets.compare_digest`) |

## Lưu ý Bảo mật

- API key chỉ là **demo gate**, không phải auth production
- Key ở client-side có thể bị extract từ browser/frontend
- Rotate key nếu chia sẻ ngoài team
- Không commit key vào repo
- Không log key trong app logs

## Định dạng Báo cáo Lỗi

Thành viên team (Phúc, Thịnh, Sơn) báo lỗi với thông tin:

1. **Endpoint**: `/predict`, `/model/info`, v.v.
2. **Request Payload**: JSON body hoặc query params
3. **Status Code**: HTTP response code
4. **Response Body**: Thông báo lỗi đầy đủ
5. **Timestamp**: Thời gian xảy ra lỗi
6. **Browser Console**: Nếu là lỗi integration frontend

Ví dụ:

```
Endpoint: POST /predict
Payload: {"province": "Dak Lak", "month": 5, ...}
Status: 422
Response: {"detail": "Invalid coffee_type value"}
Timestamp: 2026-05-27 10:30:00
Console: None
```

## Chiến lược Deploy Branch

- **Hiện tại**: GitHub Actions deploy tự động khi push vào main (sau khi tests pass)
- **Không enforce branch protection**: Dự án học tập, không muốn rào cản
- **Path filter**: Chỉ deploy khi thay đổi backend/model/requirements

## Ghi chú Vận hành

- **Cold Start**: Render Free tier có thể mất 30-60s trên request đầu tiên sau khi idle
- **Pre-demo**: Gọi `/health` trước demo để warm up service
- **Rollback**: Dùng Render dashboard Events -> previous deploy -> Manual Deploy
- **Logs**: Nguồn chính để điều tra incident trong Render dashboard

## Tài liệu Liên quan

- API Handoff: `docs/discussions/2026-05-13-api-handoff-team2-real-data.md`
- Project Roadmap: `docs/project-roadmap.md`
- Code Standards: `docs/code-standards.md`
