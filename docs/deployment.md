# Triển khai hệ thống (Deployment)

## Nền tảng: Cloudflare Pages

## Dự án

- Dự án Cloudflare Pages: `ai002-coffee-frontend`
- Nhánh chính thức (Production branch): `main`
- Nguồn mã nguồn Frontend: `frontend/`
- Thư mục đầu ra (Output folder): Thư mục sản phẩm production của Vite trong `frontend/` (thường là `frontend/dist`)

## URL

- URL Triển khai (Deployment URL): `https://493f51a8.ai002-coffee-frontend.pages.dev`
- URL Dự án chính thức (Project URL): `https://ai002-coffee-frontend.pages.dev`

## Lệnh biên dịch (Compile Command)

```bash
cd frontend
npm run compile
```

## Lệnh xuất bản (Publish Command)

```bash
cd frontend
PATH=$HOME/.nvm/versions/node/v22.12.0/bin:$PATH wrangler pages deploy dist --project-name ai002-coffee-frontend --commit-dirty=true
```

Thay thế `dist` (nếu khác) bằng thư mục đầu ra được tạo ra bởi lệnh biên dịch production của Vite.

## Biến môi trường (Environment Variables)

Frontend sử dụng các biến môi trường của Vite tại thời điểm biên dịch:

- `VITE_API_BASE_URL`: URL gốc của backend API công khai.
- `VITE_AI002_API_KEY`: Khóa API dùng thử được gửi dưới dạng header `X-API-Key`.

Nếu các biến này không được cấu hình trước khi biên dịch/xuất bản, frontend sẽ tự động dùng giá trị mặc định là `http://127.0.0.1:8000` (chỉ hoạt động trên máy local).

## Khôi phục phiên bản cũ (Rollback)

```bash
wrangler pages deployment list --project-name ai002-coffee-frontend
```

Sử dụng giao diện Cloudflare Dashboard > Pages > `ai002-coffee-frontend` > Deployments để chuyển đổi (promote) hoặc khôi phục (rollback) một bản triển khai.

## Ghi chú (Notes)

- Bản triển khai đầu tiên được tạo vào ngày 04-06-2026.
- Lệnh `npm run compile` đã chạy thành công trước khi xuất bản.
- Lệnh kiểm tra `curl -I` tại local bị lỗi bắt tay TLS (handshake error), nhưng Wrangler báo cáo đã triển khai thành công lên Cloudflare.
