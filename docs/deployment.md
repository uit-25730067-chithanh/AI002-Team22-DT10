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

## GitHub Actions

Repo dùng workflow `.github/workflows/deploy-cloudflare-pages.yml` để tự động xuất bản frontend lên Cloudflare Pages khi có thay đổi trong `frontend/**` trên nhánh `main`.

Luồng CI:

1. Pull request vào `main`: cài dependency và chạy `npm run compile`.
2. Push vào `main`: cài dependency, chạy `npm run compile`, rồi xuất bản lên Cloudflare Pages.
3. Có thể chạy thủ công bằng tab GitHub Actions > Deploy Cloudflare Pages > Run workflow.

GitHub Secrets bắt buộc:

- `CLOUDFLARE_ACCOUNT_ID`: ID tài khoản Cloudflare.
- `CLOUDFLARE_API_TOKEN`: token có quyền xuất bản Cloudflare Pages.
- `VITE_AI002_API_KEY`: khóa API demo được nhúng vào frontend tại thời điểm compile.

GitHub Variables khuyến nghị:

- `VITE_API_BASE_URL`: URL backend public.

Nếu chưa có backend public, chỉ nên dùng deployment này để kiểm tra giao diện tĩnh. Luồng gọi API sẽ không hoạt động đúng ngoài local nếu `VITE_API_BASE_URL` vẫn trỏ về `127.0.0.1`.

Lưu ý bảo mật: mọi biến có tiền tố `VITE_` đều được đóng gói vào JavaScript phía trình duyệt. Vì vậy `VITE_AI002_API_KEY` không được là khóa bí mật có quyền rộng. Chỉ dùng demo key giới hạn quyền hoặc proxy backend nếu cần giữ khóa thật ở phía server.

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
- GitHub Actions workflow đã được thêm để deploy tự động cho frontend.
