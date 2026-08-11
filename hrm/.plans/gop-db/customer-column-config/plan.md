# Plan — Tuỳ chỉnh cột màn khách hàng (`/assign/customers`)

Nhánh: `gop_db` (hrm-api + hrm-client) · Phụ trách: @khoipv
Design: `.plans/gop-db/customer-column-config/design.md`
Spec: `docs/superpowers/specs/gop-db/2026-08-10-customer-column-config-design.md`

---

## Phase 1 — Backend

- [x] BE migration `2026_08_10_000001_add_customers_to_column_customizations_table.php` — cột JSON `customers` nullable, PHPDoc `up()`/`down()` theo khuôn `add_meetings_to_...` — **đã chạy migrate**
- [x] BE `Modules/Human/Entities/ColumnCustomization.php` — thêm `'customers' => 'array'` vào `$casts`
- [x] BE `CustomerService.php` — tách 2 private method dùng chung `joinExtraColumns()` + `vehicleManufactNamesSql()` (tránh trùng alias khi `exportQuery()` gọi lại `index()`)
- [x] BE `CustomerService::index()` — thêm `parent_name` / `vehicle_manufact_names` / `creator_name` / `editor_name`, **gate sau cờ `with_extra_columns`**
- [x] BE `CustomerService::exportQuery()` — tự tắt cờ + tự gọi `joinExtraColumns()`, bỏ phần join đã trùng
- [x] BE `CustomerListResource` — trả thêm 7 field mới (`short_name` đã có sẵn từ trước)
- [x] BE đo `paginate()` trước/sau → quyết định gate (số đo ở checkpoint)
- [x] BE verify `php -l` sạch

## Phase 2 — Frontend

- [x] FE `pages/assign/customers/index.vue` — `allColumns` 18 cột (`label`/`title`/`isVisible`, 2 cột đầu gắn `locked`)
- [x] FE — computed `defaultTableColumns` (merge cấu hình đã lưu) + `customizableColumns` (bỏ cột khoá) + `tableColumns` (khoá đứng đầu + phần còn lại theo cấu hình) + `needsExtraColumns`
- [x] FE — data `columnFields` / `columnFieldsLoaded`, method `getFields()` / `updateColumns()` / `configColumns()`, `created()` gọi `getFields()` TRƯỚC `loadData()`
- [x] FE — nút icon `ri-layout-column-line` (secondary, cuối toolbar) + `<ColumnCustomizationModal :table="'customers'">`
- [x] FE — `loadData()` gửi `with_extra_columns` theo `needsExtraColumns` (không nhét vào `buildApiFilters()` để export/popup không dính)
- [x] FE — 8 template cell mới, 8 cột mặc định ẩn
- [x] FE verify parse sạch (vue-template-compiler + babel)

## Phase 3 — Verify tự động (đã chạy trên DB gop_db thật)

- [x] 3 luồng dùng chung `index()`: popup **không** join thêm · danh sách có đủ 8 field · export không trùng alias kể cả khi client gửi cờ
- [x] Dữ liệu thật: KH `29TPHPTH-5` → `parent_name` = "CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT", `creator_name` = "Nguyễn Văn Thái"
- [x] Round-trip cấu hình: POST lưu → GET đọc lại đúng thứ tự + ẩn/hiện, cast về array (đã khôi phục dữ liệu nguyên trạng sau test)
- [x] Test logic cột FE (nạp thẳng source computed từ index.vue) — 4 kịch bản, 17/17 check PASS: chưa lưu cấu hình · đã lưu (ẩn/bật/đảo thứ tự) · cấu hình cũ khi code thêm cột mới · cấu hình còn cột đã gỡ
- [x] Cấu hình cột KHÔNG ảnh hưởng file xuất (export tự tắt cờ, bộ cột cố định)

---

### Checkpoint — 2026-08-10
Vừa hoàn thành: toàn bộ Phase 1 + 2 + 3.
Số đo: `COUNT` phân trang 0,12s → 0,43s khi thêm 5 leftJoin (42.077 KH) → **gate bằng cờ `with_extra_columns`**;
`paginate(10)` màn danh sách 0,468s (không cờ) → 0,555s (có cờ).
Bẫy đã dính: modal chung dùng `b-form-checkbox :value="column.key"` → cột hiện mặc định phải khai
`isVisible: '<đúng key>'`, để `undefined` là modal bỏ tích hết → bấm OK ẩn sạch bảng. Đã sửa cả 10 cột.
Đang làm dở: không có.
Bước tiếp theo: user build FE → test tay Phase 4.
Blocked: không có.

## Phase 4 — Test tay (user)

- [x] Mở modal, ẩn/hiện + kéo thả, bấm OK → bảng đổi đúng, F5 vẫn giữ
- [x] Đăng nhập user khác → cấu hình riêng, không dính nhau
- [x] Popup chọn KH (Dự án TKT / Meeting) vẫn chạy bình thường, không chậm đi

---

### Checkpoint — 2026-08-11 (HOÀN THÀNH)
Vừa hoàn thành: user test trình duyệt xong Phase 4 → **feature HOÀN THÀNH**.
Đang làm dở: không có.
Bước tiếp theo: không có (đã chuyển sang mục "Hoàn thành" ở `.plans/gop-db/STATUS.md`).
Blocked: không có.
