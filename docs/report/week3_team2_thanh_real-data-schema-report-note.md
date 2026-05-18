# Note báo cáo phần việc của Thanh — Week 3 Data thật

**Ngày note:** 2026-05-18  
**Người báo cáo:** Thanh  
**Báo cho:** em Phúc / Team 1 / Team 2  
**Roadmap:** Tuần 3 — Data thật  
**Phạm vi:** Phần Thanh xử lý/review schema và luồng dữ liệu. Không nhận phần crawler/build dataset của Team 1 hoặc audit/evaluation của Sơn.

## 1. Tóm tắt ngắn để báo miệng

Tuần 3, anh chuyển phần chuẩn bị của Team 2 từ mock/foundation sang dữ liệu thật. Việc chính là đọc processed weekly/monthly từ Team 1, chọn monthly all-areas làm dataset baseline, đối chiếu schema thật với pipeline model/API, kiểm tra ranking độ phủ khu vực và đồng bộ roadmap/handoff để team thống nhất luồng crawler → processed data → model → API → frontend.

## 2. Mapping theo roadmap

| Roadmap item                               | Trạng thái | Phần Thanh báo cáo                                     | Bằng chứng                                          |
| ------------------------------------------ | ---------- | ------------------------------------------------------ | --------------------------------------------------- |
| Team 1 có processed weekly/monthly dataset | Xong       | Nhận và đọc cấu trúc dataset để chọn hướng train       | `data/processed/monthly/`, `data/processed/weekly/` |
| Team 2 đọc và chuẩn hóa schema real-data   | Xong       | Đối chiếu schema thật và chuẩn bị mapping cho pipeline | `model/preprocess.py`                               |
| Có xếp hạng độ phủ dữ liệu theo khu vực    | Xong       | Dùng ranking để hiểu khu vực nào phù hợp baseline      | `data/processed/area_real_price_data_ranking.csv`   |
| Phúc review lại docs data flow             | Chờ review | Đồng bộ roadmap/handoff để Phúc xác nhận assumptions   | `docs/project-roadmap.md`                           |

## 3. Quyết định dùng dữ liệu

| Nhóm dữ liệu      | Vai trò trong tuần 3                         | Quyết định                            |
| ----------------- | -------------------------------------------- | ------------------------------------- |
| Raw daily price   | Nguồn gốc giá thật, không version trong repo | Không train trực tiếp trong repo      |
| Weekly processed  | Có thể thử nghiệm sau                        | Chưa dùng làm baseline chính          |
| Monthly processed | Ổn định hơn, phù hợp KISS                    | Chọn làm dataset chính                |
| Area ranking      | Kiểm tra độ phủ vùng                         | Dùng để giải thích bias/coverage risk |

Lý do chọn monthly: ít nhiễu hơn weekly, ổn định hơn cho baseline và dễ giải thích trong báo cáo.

## 4. Việc Thanh đã làm

- **Đọc data thật:** Kiểm tra các file processed mà Team 1 đưa vào repo.
- **Chốt dataset train chính:** Chọn `data/processed/monthly/coffee_environment_all_areas_monthly_2022_2025.csv`.
- **Chuẩn bị schema mapping:** Xác định các field cần đưa vào model/API như `province`, `area`, giá, weather, soil và categorical fields.
- **Kiểm tra độ phủ:** Dùng ranking khu vực để biết dữ liệu không đều, tránh nói model đại diện toàn bộ vùng.
- **Đồng bộ roadmap/handoff:** Ghi rõ luồng crawler → processed data → preprocess → model → API → frontend trong tài liệu hiện có.

## 5. Phần không nhận là việc của Thanh

| Nội dung                       | Người/phần chính theo roadmap | Cách nhắc nếu cần                          |
| ------------------------------ | ----------------------------- | ------------------------------------------ |
| Crawl raw price/weather        | Phúc, Thịnh                   | Team 1 đã cung cấp processed dataset       |
| Build processed weekly/monthly | Phúc, Thịnh                   | Thanh dùng output để train baseline        |
| Kiểm toán bias độ phủ chi tiết | Sơn                           | Thanh chỉ dùng ranking làm ngữ cảnh        |
| 5 Pillars checkpoint           | Sơn                           | Thanh tham chiếu khi chuẩn bị report/slide |

## 6. Việc cần Phúc review

- **Nguồn raw chính:** Giá crawl từ nguồn nào là nguồn chuẩn.
- **Cách build processed:** Weekly/monthly có logic aggregate như team crawler mong muốn chưa.
- **Ý nghĩa field:** `price_fill_method`, `price_observations`, soil/weather fields.
- **Khu vực yếu:** Các vùng có độ phủ thấp cần disclaimer hoặc hạn chế chọn trên UI.

## 7. Tin nhắn ngắn có thể gửi team

```text
Tuần 3 phần của anh đã đọc data thật Team 1 build, chốt dùng monthly all-areas làm dataset baseline, kiểm tra ranking độ phủ khu vực và đồng bộ roadmap/handoff để cả nhóm nhìn rõ luồng crawler → processed data → model → API → frontend. Phần crawler/build data là của Phúc/Thịnh, phần audit bias chi tiết là của Sơn; anh dùng các output đó để chuẩn bị pipeline train real-data ở tuần 4.
```
