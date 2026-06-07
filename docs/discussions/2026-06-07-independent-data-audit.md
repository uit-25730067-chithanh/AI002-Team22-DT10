# Independent Data Audit - Team 2

**Ngay:** 2026-06-07
**Trang thai:** Phase 4 audit

## Summary

- Dataset moi la public reference dataset do Team 2 tu crawl lai.
- Old dataset chi dung lam baseline so sanh.
- Monthly dataset moi co source evidence fields: `source_url_count`, `source_names`.

## Dataset size

- Old monthly rows: `576`
- New monthly rows: `912`
- New period range: `2020-01-01` -> `2026-04-01`

## New fill-method distribution

| fill_method | rows | rate |
| --- | --- | --- |
| observed | 711 | 0.7796 |
| interpolated_area | 157 | 0.1721 |
| province_proxy | 44 | 0.0482 |

## Province comparison

| province | old_total_rows | old_observed_rows | old_observed_rate | new_total_rows | new_observed_rows | new_observed_rate | delta_observed_rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Dak Lak | 144 | 134 | 0.9306 | 228 | 177 | 0.7763 | -0.1543 |
| Dak Nong | 96 | 38 | 0.3958 | 152 | 92 | 0.6053 | 0.2095 |
| Gia Lai | 144 | 134 | 0.9306 | 228 | 177 | 0.7763 | -0.1543 |
| Kon Tum | 48 | 48 | 1.0 | 76 | 67 | 0.8816 | -0.1184 |
| Lam Dong | 144 | 144 | 1.0 | 228 | 198 | 0.8684 | -0.1316 |

## Area comparison top changes

| province | area | old_total_rows | old_observed_rows | old_observed_rate | new_total_rows | new_observed_rows | new_observed_rate | delta_observed_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Dak Nong | Dak R'lap | 48 | 0 | 0.0 | 76 | 47 | 0.6184 | 0.6184 |
| Kon Tum | Kon Tum | 48 | 48 | 1.0 | 76 | 67 | 0.8816 | -0.1184 |
| Dak Lak | Buon Ho | 48 | 48 | 1.0 | 76 | 66 | 0.8684 | -0.1316 |
| Dak Lak | Ea H'leo | 48 | 48 | 1.0 | 76 | 66 | 0.8684 | -0.1316 |
| Gia Lai | Ia Grai | 48 | 48 | 1.0 | 76 | 66 | 0.8684 | -0.1316 |
| Gia Lai | Pleiku | 48 | 48 | 1.0 | 76 | 66 | 0.8684 | -0.1316 |
| Lam Dong | Bao Loc | 48 | 48 | 1.0 | 76 | 66 | 0.8684 | -0.1316 |
| Lam Dong | Di Linh | 48 | 48 | 1.0 | 76 | 66 | 0.8684 | -0.1316 |
| Lam Dong | Lam Ha | 48 | 48 | 1.0 | 76 | 66 | 0.8684 | -0.1316 |
| Dak Lak | Cu M'gar | 48 | 38 | 0.7917 | 76 | 45 | 0.5921 | -0.1996 |
| Dak Nong | Gia Nghia | 48 | 38 | 0.7917 | 76 | 45 | 0.5921 | -0.1996 |
| Gia Lai | Chu Prong | 48 | 38 | 0.7917 | 76 | 45 | 0.5921 | -0.1996 |

## Baseline candidate ranges

| candidate | start | end | rows | observed_rows | observed_rate |
| --- | --- | --- | --- | --- | --- |
| 2020-2026_04 | 2020-01-01 | 2026-04-30 | 912 | 711 | 0.7796 |
| 2021-2026_04 | 2021-01-01 | 2026-04-30 | 768 | 683 | 0.8893 |
| 2022-2026_04 | 2022-01-01 | 2026-04-30 | 624 | 587 | 0.9407 |

## Area replacement decision

- Chua thay area trong Phase 4.
- Ly do: 12 area hien tai deu co processed rows va weather day du.
- Phase 5 se chon baseline range dua tren candidate table.

## Known limitations

- Raw price moi phu thuoc nhieu vao Nong Nghiep Moi Truong.
- Kinh Te Do Thi timeout trong Phase 3.
- Vinanet seed URLs chua parse duoc rows.

## Unresolved Questions

- Phase 5 chon 2020-2026/04 hay 2022-2026/04 dua tren trade-off observed rate vs thoi gian dai hon.
