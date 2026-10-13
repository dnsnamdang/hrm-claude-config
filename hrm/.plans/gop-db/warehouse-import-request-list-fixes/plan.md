# Plan — Sửa màn danh sách ĐNNK (`warehouse-import-requests/index.vue`)

Nguồn yêu cầu (user, 2026-10-07): *"đề nghị nhập kho: Đổi text 'Thao tác' => 'hành động' /
Lịch sử tại cột thao tác đang ko hiển thị"* (kèm screenshot cột hành động).

Màn: `pages/finance/warehouse-import-requests/index.vue` (ĐNNK). Nhánh `gop_db` → tài liệu ở
`.plans/gop-db/`.

## Task A — Đổi nhãn cột hành động "Thao tác" → "Hành động"

- [x] `index.vue:438`: `label`/`title` của cột `action` đổi `'Thao tác'` → `'Hành động'`.
- [x] Verify Playwright 127.0.0.1:3000: header bảng giờ là **"Hành động"** (đủ 15 cột, cột cuối
      đúng chữ mới).

## Task B — "Lịch sử" ở ĐNNK mở popup RỖNG ("Chưa có lịch sử thao tác nào")

### Root cause (ĐÃ xác định — systematic-debugging Phase 1, KHÔNG phải bug code)

Luồng đọc + popup + wiring **đều đúng**. Bấm "Xem lịch sử" PDNNK-08539 → gọi đúng endpoint
`GET catalog-histories/warehouse_import_requests/8539` (200) → rỗng vì **không có dữ liệu**.

Bằng chứng DB (`erp_hrm_check`, chỉ-đọc):
- `catalog_histories` (bảng HRM đọc, key `table_name`): **0 dòng** cho `warehouse_import_requests`
  (cả bảng chỉ có **1 dòng** tổng — của `product_export_requests`). HRM chỉ ghi bảng này khi phiếu
  được tạo/sửa qua `Modules/Finance/.../WarehouseImportRequestService` (trait `LogsCatalogHistory`).
- **Mọi** phiếu ĐNNK hiện có (PDNNK-08539… tạo 2026-07→09) do **luồng ERP** tạo/xử lý → KHÔNG đi qua
  service HRM → chưa từng ghi `catalog_histories`.
- Lịch sử THẬT của các phiếu này nằm ở bảng ERP **`warehouse_import_request_histories`**:
  **29.215 dòng**, riêng id 8539 có **3 dòng** (received_time / approved_time / change_stock_time).
  Cấu trúc KHÁC HẲN: diff theo cột (`column_name, old_value, new_value, version_id`), **không có**
  `action` / `changed_by` / người thực hiện như catalog_histories.

Kết luận: đây là gotcha gộp DB (2 cơ chế lịch sử song song: ERP per-column vs HRM action-based),
không phải lỗi màn. Phiếu tạo MỚI qua luồng HRM sẽ có lịch sử bình thường.

### Hướng xử lý — USER CHỐT **HƯỚNG B** ("theo đề xuất", 2026-10-07)

- [ ] **A. Giữ nguyên, coi là đúng dữ liệu.** (không chọn)
- [x] **B. Đọc kèm lịch sử ERP** `warehouse_import_request_histories` và trộn vào kết quả
      `catalog-histories/warehouse_import_requests/{id}`. **ĐÃ LÀM** — không ghi prod.
- [ ] **C. Backfill** `catalog_histories`. (không chọn — ghi prod + mất `changed_by`/`action`)

### Giải thích cho user: bảng `warehouse_import_request_histories` sinh từ đâu

Bảng này do **luồng ERP tự ghi ngầm**, không phải HRM, nên user chưa từng thấy nó:
`ERP/.../app/Model/Warehouse/WarehouseImportRequest.php` có `boot()` đăng ký hook
`self::updating(fn => $model->saveHistory())`. Mỗi lần phiếu ĐNNK được **cập nhật**, `saveHistory()`:
1. tạo 1 dòng `warehouse_import_request_versions` (`employee_id` = người đang thao tác, hoặc
   `config('admin')` khi chạy ngầm);
2. so `getOriginal()` vs `getAttributes()` **chỉ với 6 cột** trong `HISTORY_FIELDS`
   (`approved_time`, `note`, `comment`, `received_time`, `change_stock_time`, `rejected_time`);
3. mỗi cột đổi → 1 dòng `warehouse_import_request_histories` (`column_name`, `old_value`, `new_value`);
4. nếu không cột nào đổi thì xoá luôn version vừa tạo.
ERP **không có màn UI nào** hiển thị bảng này (chỉ ghi để audit ngầm) → đó là lý do user không biết
nó tồn tại. 3 dòng của PDNNK-08539 chính là 3 mốc duyệt: nhận đề nghị → duyệt → nhập kho.

### Thực hiện Hướng B — `hrm-api/app/Services/CatalogHistoryService.php`

- [x] **Edit 1** — whitelist `TABLES['warehouse_import_requests']['columns']` thêm nhãn 6 cột mốc
      ERP (`received_time`→"Thời điểm nhận đề nghị", `approved_time`→"Thời điểm duyệt",
      `change_stock_time`→"Thời điểm nhập kho", `rejected_time`→"Thời điểm từ chối", +`note`,`comment`).
- [x] **Edit 2** — thêm WIR vào hằng `LEGACY_VERSION_TABLES` với `time_col => 'created_at'` +
      `actor_col => 'employee_id'` (bảng ERP dùng tên cột khác bản HRM accounts/type_accounts).
- [x] **Edit 3** — tổng quát hoá `legacyVersionLogs()`: đọc `$timeCol`/`$actorCol` từ map (mặc định
      `time`/`created_by` giữ nguyên hành vi accounts/type_accounts), thay mọi chỗ cứng
      `orderByDesc('time')`, `pluck('created_by')`, `$version->created_by` (dòng 972), `$version->time`.
      `php -l` sạch.

- [x] **Verify Playwright** (127.0.0.1:3000, 2026-10-07): bấm "Xem lịch sử" PDNNK-08539 → popup hiện
      **đủ 3 dòng** ERP: (1) 15/09 14:12 *Thời điểm nhập kho* (2) 15/09 14:11 *Thời điểm duyệt*
      (3) 15/09 14:11 *Thời điểm nhận đề nghị*; người thực hiện **DNS Admin — PHÒNG KINH DOANH
      THƯƠNG MẠI** (resolve từ `employee_id` ERP qua `actorsOf`), nhãn cột tiếng Việt đúng. Console
      chỉ còn lỗi socket.io :8891 benign, KHÔNG có 500/404/403 ở endpoint catalog-histories.
- [x] Commit + push gop_db (2026-10-07): hrm-api `c50c56973` → sau rebase lên origin = `0de29369c`.

## Task C — "Làm mới" không về "không sort" (mũi tên ↓ vẫn ở Ngày tạo)

Nguồn yêu cầu (user, 2026-10-07): *"sort khi làm mới chưa về mặc định … mặc định theo tôi
hiểu là ko sort hiện hình như vẫn đang sort"* (màn danh sách ĐNNK).

### Root cause (systematic-debugging Phase 1 — KHÔNG phải lỗi wiring)

`handleReset()` reset ĐÚNG về `initialFilters`. Nhưng `initialFilters` có sẵn
`sort_field: 'created_at', sort_dir: 'desc'` → đó là "mặc định CÓ sort", nên sau Làm mới
cột Ngày tạo vẫn vẽ mũi tên ↓. Verify Playwright: sort cột Mã phiếu (↑) → bấm Làm mới →
mũi tên nhảy ĐÚNG về Ngày tạo ↓ (reset chạy tốt, chỉ là default có sort).

Dòng `sort_field: 'created_at'` ở FE là **THỪA**: BE `index()` của cả 4 màn finance đều có
nhánh `else { $query->orderByDesc(TABLE.id) }` khi FE không gửi `sort_field` → tức **API đã
tự trả mới-nhất-trước (id desc)**. Bỏ default sort ở FE ⇒ không mũi tên + thứ tự KHÔNG đổi
(id desc ≈ created_at desc). Đã kiểm 4 controller:
- ĐNNK `WarehouseImportRequestController::index` (Finance) — else `orderByDesc(id)` ✓
- ĐNXK `ProductExportRequestController::index` (Assign) — else `orderByDesc(id)` ✓
- YCXH `WarehouseExportRequestController::index` (Assign) — else `orderByDesc(id)` ✓
- Phiếu xuất `ProductExportController::index` (Assign) — else `orderByDesc(id)` ✓

### Quyết định (user chốt 2026-10-07): **Hướng B — sửa CẢ 4 màn finance**

Dự án đang có 2 quy ước (finance = `created_at desc`; customer-care/assign = `sort_field: ''`).
User chọn đồng bộ 4 màn finance về kiểu "không sort" (giống customer-care).

### Thực hiện — FE, chỉ đổi `initialFilters` (sort_field/sort_dir → rỗng)

- [x] `pages/finance/product-export-requests/index.vue:258-259`
- [x] `pages/finance/product-exports/index.vue:174-175`
- [x] `pages/finance/warehouse-export-requests/index.vue:282-283`
- [x] `pages/finance/warehouse-import-requests/index.vue:281-282`
      → `sort_field: ''`, `sort_dir: ''` (handleReset/filterState tự dùng lại initialFilters).
- [x] Verify Playwright 127.0.0.1:3000 (2026-10-07):
      - ĐNNK `warehouse-import-requests`: load + bấm Làm mới → `activeSortArrows: []` (KHÔNG mũi tên);
        dòng đầu **PDNNK-08539** → 08538 → 01886 (id desc, mới-nhất-trước) ✓.
      - Phiếu xuất `product-exports` (spot-check): `activeSortArrows: []`; dòng đầu **PXH-34590** →
        34581 → 34580 (id desc) ✓.
- [x] Commit + push gop_db (2026-10-07): hrm-client Task C `3f3ff6428` + Task A `60460da93`,
      sau rebase lên origin → đầu nhánh `e99d40b7e`.

## Checkpoint
### Checkpoint — Task B (Hướng B) xong + verify (2026-10-07)
Vừa hoàn thành: Task A (đổi nhãn). Task B theo Hướng B: sửa `CatalogHistoryService` (3 edit, chỉ
ảnh hưởng WIR nhờ default `time`/`created_by` cho accounts/type_accounts) để trộn lịch sử ERP
`warehouse_import_request_histories` vào popup; Playwright verify PDNNK-08539 ra đủ 3 dòng, actor +
nhãn đúng, không ghi prod.
Đang làm dở: không.
Bước tiếp theo: chờ user xác nhận commit/push (cả 2 task A+B gói chung) — chưa tự commit.
Blocked: commit/push chờ user.
