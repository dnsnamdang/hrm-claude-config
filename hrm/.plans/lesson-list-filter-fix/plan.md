# Plan — Fix lọc màn Danh sách bài học (Training)

@junfoke

## Bối cảnh

Màn `/training/lessons` — ô tìm kiếm không áp dụng điều kiện lọc, vẫn trả toàn bộ dữ liệu.

**Root cause:** `buildQueryString` (`hrm-client/utils/url-action.js`) giữ nguyên tên key, không map.
FE gửi `keyword`, BE `LessonService::searchByFilter` đọc `$request->quick_search` → không khớp → BE bỏ qua.

`LessonService.php` là file DUY NHẤT trong workspace dùng `quick_search` (106 file BE khác dùng `keyword`)
→ đây là ngoại lệ sai convention, sửa BE (không sửa FE — 105 màn FE khác đang dùng `keyword`).

Chỉ `pages/training/lessons/index.vue` gọi endpoint này → đổi tên param không phá consumer nào.

### Bảng lệch param (cùng 1 root cause)

| FE gửi | BE đọc (sai) | Hậu quả |
|---|---|---|
| `keyword` | `quick_search` | Ô tìm kiếm chết ← lỗi user báo |
| `per_page` | `limit` | Luôn 10 dòng/trang |
| `sort_field` / `sort_dir` | `sortBy` / `sortDesc` | Sort cột không ăn |
| `updated_from` / `updated_to` | `from_date` / `to_date` | Lọc khoảng ngày chết |

Các filter trùng tên vẫn chạy đúng: `training_type_id`, `type`, `study_mode`, `status`, `created_by`, `updated_by`.

### Lỗi phát sinh — Xuất Excel (user chốt sửa luôn 2026-07-15)

`LessonController::export` gọi `getExportData`, KHÔNG gọi `searchByFilter`. Hệ quả:
1. `getExportData` chỉ xử lý `code`, `name`, `training_type_id`, `status`, `type` → FE gửi `keyword`, `study_mode`, `created_by`, `updated_by`, `updated_from`, `updated_to` đều bị bỏ qua → **export luôn dump toàn bộ bảng**.
2. `getExportData` **thiếu permission check** `created_by = -1` mà `searchByFilter` có (dòng 53) → user không có quyền "Quản lý bài học" export vẫn ra full data (lỗ hổng lộ dữ liệu).

## Quyết định kỹ thuật

- Tách filter dùng chung thành `private applyFilters($query, $request)` → cả `searchByFilter` + `getExportData` gọi
  → hết trùng lặp, export tự động có permission check + đủ filter.
- **Giữ nguyên thứ tự mặc định `id desc`**: FE luôn gửi `sort_dir='asc'` kể cả khi `sort_field` rỗng
  (vì `buildQueryString` loại `''` nhưng `sort_dir` có default `'asc'`). Nếu map thẳng → list lật ngược = regression.
  → chỉ áp `sort_dir` KHI `sort_field` có giá trị.
- Không sửa FE. Không migration. Không permission mới. Không đụng hàm dùng chung.

## Tasks

### BE — `Modules/Training/Services/Lesson/LessonService.php`

- [x] B1: Thêm `private applyFilters($query, $request)` — permission check + toàn bộ filter, dùng tên param theo convention FE (`keyword`, `updated_from`, `updated_to`) + giữ `code`/`name`
- [x] B2: `searchByFilter` — gọi `applyFilters`; đổi `limit`→`per_page`, `sortBy`/`sortDesc`→`sort_field`/`sort_dir` (giữ default `id desc`)
- [x] B3: `getExportData` — gọi `applyFilters` (nhận permission check + đủ filter), giữ `orderBy('id','desc')->get()`

### Verify — API thật localhost:8000, tài khoản namdangit (DNS ADMIN update)

- [x] V1: `php -l` LessonService.php — No syntax errors
- [x] V2: Grep sạch, không còn `quick_search` / `sortDesc` / `from_date` trong Lesson service + controller
- [x] V3: `keyword` CHẠY — `keyword=onboarding` → 1 dòng (LESS-0004); `keyword=LESS-0018` → 1 dòng; tiếng Việt `Quy%20tr%C3%ACnh` → đúng 2 dòng (LESS-0004 + LESS-0001); keyword vô nghĩa → total=0. **Trước fix: luôn trả 14 dòng.**
- [x] V4: Không regression thứ tự — FE mặc định (`sort_dir=asc` + `sort_field` rỗng) vẫn ra `id desc`: LESS-0018, 0017, 0016...
- [x] V5: `per_page=2` → cắt đúng 2 dòng; `sort_field=code&sort_dir=asc` → tăng dần / `desc` → giảm dần; `updated_from=2026-06-01` → 4 dòng, `updated_to=2026-04-25` → 4 dòng (khớp data DB)
- [x] V6: Export áp filter — không filter 21 dòng → `keyword=Quy trình` 9 dòng → `updated_from=2026-06-01` 11 dòng. **Trước fix: luôn 21 dòng.** Permission check đã áp (tinker không auth → 0 dòng).
- [ ] V7: User verify bằng mắt trên browser (Playwright bị khoá profile do Chrome khác đang mở — chưa chạy được UI test)

### B4 — Fix SQL error khi sort (phát sinh từ B2, user báo 2026-07-15)

Lỗi: `SQLSTATE[42S22] Unknown column 'updatedAt' in 'order clause'` khi bấm sort cột "Cập nhật".
Root cause: FE gửi `sort_field` = **key cột của bảng FE** (`updatedAt`, camelCase — xem `tableColumns` index.vue:436), KHÔNG phải tên cột DB (`updated_at`). B2 đưa thẳng `sort_field` vào `orderBy()` → SQL nổ.
Lỗi này bị che trước đây vì `sortBy` không bao giờ được đọc (luôn sort `id`) — sửa param mới làm nó lộ ra.
Convention có sẵn: `Modules/Assign/Services/ApplicationService.php:74` dùng whitelist `['updatedAt' => 'updated_at']` → copy pattern, KHÔNG tự nghĩ cách khác.

- [x] B4: Whitelist `$allowedSortFields = ['updatedAt' => 'updated_at']` (màn này chỉ 1 cột sortable). Field không có trong whitelist → bỏ qua. `sort_dir` chỉ nhận `asc`/`desc`, còn lại fallback `desc`. Luôn append `orderBy('id','desc')` làm tiebreak (giống ApplicationService) → phân trang ổn định.
- [x] V8: URL user báo lỗi `?page=1&per_page=10&sort_field=updatedAt&sort_dir=asc` → **200 OK**, sort đúng updated_at tăng dần (04-24 đầu). Hết lỗi SQL.
- [x] V9: `sort_dir=desc` → 06-04 đầu (đảo đúng)
- [x] V10: Không sort → vẫn `id desc` (LESS-0018 đầu, không regression)
- [x] V11: `sort_field=badcol` → bỏ qua, KHÔNG lỗi SQL (whitelist chặn cột lạ = hết rủi ro orderBy cột tuỳ ý)
- [x] V12: `sort_dir=xxx` rác → fallback desc, không lỗi
- [x] V13: Lọc + sort đồng thời (`keyword=Quy trình` + `updatedAt asc`) → 2 dòng đúng thứ tự

## Ghi chú môi trường

DB local có 14 bài học, `LESS-0003` = "Tài liệu an toàn lao động" — KHÁC ảnh user gửi (`LESS-0003` = "Quy định chung của công ty", 3 bài).
→ Ảnh user chụp từ môi trường khác (dev-hrm). Fix nằm ở BE nên không phụ thuộc data.

Lưu ý tooling: `curl --data-urlencode` trên Windows làm hỏng tiếng Việt → phải percent-encode UTF-8 thủ công khi test. Không phải lỗi app.

## Checkpoint

### Checkpoint — 2026-07-15
Vừa hoàn thành: B1-B3 code xong + V1-V6 verify PASS trên API thật. Root cause: FE gửi `keyword`/`per_page`/`sort_field`/`sort_dir`/`updated_from`/`updated_to`, BE `LessonService` đọc `quick_search`/`limit`/`sortBy`/`sortDesc`/`from_date`/`to_date` — file DUY NHẤT sai convention trong 106 file BE. Đã gộp filter vào `applyFilters` dùng chung cho list + export (export nhờ đó có permission check + đủ filter).
Đang làm dở: không.
Bước tiếp theo: user hard-refresh browser → verify mắt màn /training/lessons (V7).
Blocked: Playwright không chạy được — Chrome đang giữ profile lock.
