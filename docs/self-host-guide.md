# Hướng dẫn chạy Backend Local và Self-host

Tài liệu này dành cho thành viên cần chạy backend FastAPI để test frontend, demo nội bộ hoặc host nhanh trên một máy Linux. Không cần hiểu sâu về Python, chỉ cần làm đúng từng bước.

## 1. Khi nào dùng tài liệu này

| Nhu cầu | Nên làm |
| --- | --- |
| Test frontend trên máy cá nhân | Chạy mục 2, 3 và 4 |
| Demo nội bộ qua cùng mạng LAN | Chạy mục 2, 3, 4 và mở port máy host |
| Host lâu dài trên server Linux | Làm thêm mục 6 và 7 |
| Deploy public cho cả team | Người phụ trách backend chọn nền tảng, sau đó chia sẻ base URL và API key nội bộ |

## 2. Chuẩn bị môi trường

Mở terminal tại thư mục gốc repo, sau đó chạy:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 3. Cấu hình API key

API key dùng để chặn người ngoài gọi `/predict` và `/model/info`. Không commit key, không gửi key vào group công khai.

macOS/Linux:

```bash
export AI002_API_KEY="replace-with-team-demo-key"
```

Windows PowerShell:

```powershell
$env:AI002_API_KEY="replace-with-team-demo-key"
```

Team lead lấy key thật từ kênh nội bộ của nhóm. Nếu chưa có key, tự tạo một chuỗi dài khó đoán rồi chia riêng cho người cần test.

## 4. Chạy backend local

macOS/Linux:

```bash
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Windows PowerShell:

```powershell
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Sau khi chạy thành công:

- Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`
- API base URL cho frontend local: `http://localhost:8000`

## 5. Test nhanh API

Health check không cần API key:

```bash
curl http://localhost:8000/health
```

Endpoint protected cần header `X-API-Key`:

```bash
curl -H "X-API-Key: replace-with-team-demo-key" \
  http://localhost:8000/model/info
```

Kết quả thường gặp:

| Kết quả | Ý nghĩa | Cách xử lý |
| --- | --- | --- |
| `200` | API chạy đúng | Có thể nối frontend |
| `401` | Thiếu hoặc sai API key | Kiểm tra header `X-API-Key` |
| `503` | Thiếu cấu hình hoặc model chưa sẵn sàng | Kiểm tra `AI002_API_KEY`, `model/best_model/model.pkl` |
| `422` | Payload sai schema hoặc category ngoài tập train | So lại với API handoff doc |

## 6. Self-host trên Linux bằng systemd

Chỉ dùng khi cần server chạy nền ổn định. Ví dụ repo nằm ở `/opt/ai002`.

Tạo file service:

```bash
sudo nano /etc/systemd/system/ai002-backend.service
```

Nội dung mẫu:

```ini
[Unit]
Description=AI002 Coffee Forecast Backend
After=network.target

[Service]
WorkingDirectory=/opt/ai002
Environment=AI002_API_KEY=replace-with-team-demo-key
ExecStart=/opt/ai002/venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Khởi động service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ai002-backend
sudo systemctl start ai002-backend
sudo systemctl status ai002-backend
```

Xem log khi lỗi:

```bash
sudo journalctl -u ai002-backend -n 100 --no-pager
```

## 7. Nginx reverse proxy

Nếu cần domain public, dùng Nginx chuyển request về FastAPI.

```nginx
server {
    server_name api.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Sau đó cấu hình HTTPS bằng Certbot theo hướng dẫn hệ điều hành/server đang dùng.

## 8. Lưu ý cho frontend

- Gọi `GET /health` trước demo để kiểm tra backend đã thức.
- Gọi `/predict` và `/model/info` kèm header `X-API-Key`.
- Nếu browser báo CORS, báo Team 2 thêm domain frontend vào FastAPI trước khi demo public.
- Không hard-code API key thật vào file frontend được commit lên Git.

## 9. Bàn giao cho frontend

Khi backend đã chạy ở local, LAN hoặc server public, người phụ trách backend chỉ cần gửi cho frontend:

- API base URL, ví dụ `http://localhost:8000` hoặc URL server public
- API key nội bộ để gửi qua header `X-API-Key`
- Trạng thái `/health`
- Ghi chú nếu server có cold start, giới hạn mạng nội bộ hoặc CORS

## 10. Tài liệu liên quan

- API contract: `docs/discussions/2026-05-13-api-handoff-team2-real-data.md`
- Sửa lỗi thường gặp: `docs/troubleshooting.md`
