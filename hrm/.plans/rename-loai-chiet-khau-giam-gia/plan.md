# Plan — Đổi tên "Loại chiết khấu" → "Loại giảm giá"

## Phase 1 — Rename UI + tiền tố mã

- [x] **T1. BE tiền tố mã** `Modules/Assign/Entities/DiscountType.php::getNextCode()`: `'CK-'` → `'GG-'`. Bản ghi cũ giữ nguyên mã.
- [x] **T2. FE menu** `components/menu-sidebar.js` (dòng 380): label `'Loại chiết khấu'` → `'Loại giảm giá'`. GIỮ nguyên `isShow: ['Quản lý danh mục loại chiết khấu']` (permission).
- [x] **T3. FE modal Thêm/Sửa/Xem** `components/modal/discount-type-modal.vue`:
  - Tiêu đề (dòng 30): "Xem/Sửa/Thêm loại chiết khấu" → "... loại giảm giá".
  - Nhãn "Mã loại CK" → "Mã loại giảm giá"; "Tên loại CK *" → "Tên loại giảm giá *".
  - Placeholder "VD: CK khách hàng thân thiết" → "VD: Giảm giá khách hàng thân thiết".
- [x] **T4. FE danh sách/bộ lọc/thao tác** `pages/assign/discount-types/index.vue`:
  - Tiêu đề bộ lọc (d7), tiêu đề danh sách (d70, d348), itemLabel (d74), placeholder search (d11).
  - Tooltip khoá/mở/sửa/xoá (d193, d228, d238): "loại CK" → "loại giảm giá".
  - Cột "Tên loại chiết khấu" (d391) → "Tên loại giảm giá".
  - Confirm/toast (d399, d408, d417, d421, d662, d672, d679): "loại chiết khấu"/"loại CK" → "loại giảm giá".
- [x] **T5. Verify** `php -l` DiscountType.php OK; grep sạch "chiết khấu"/"CK" trong 2 file catalog + menu.
- [ ] **T6. Verify E2E** (user): menu hiện "Loại giảm giá"; vào danh sách/tạo/sửa/xem tiêu đề + nhãn đúng; tạo mới → mã `GG-YYYY-XXXXX`; bản ghi cũ giữ `CK-`.

## Phase 2 — Đổi tên QUYỀN cho đồng bộ (permission rename)

> Đổi tên quyền `Quản lý danh mục loại chiết khấu` → `Quản lý danh mục loại giảm giá`. Giữ nguyên `id=1090` → phân quyền đã gán (pivot `role_has_permissions.permission_id=1090`) không mất. Theo convention: sửa trực tiếp `PermissionsTableSeeder.php`, KHÔNG migration.

- [x] **P1. Seeder** `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (dòng 1090): đổi `name` + `display_name` → "Quản lý danh mục loại giảm giá"; sửa comment "// Danh mục loại giảm giá". Giữ `id=1090`, `group='Danh mục'`, `type=4`.
- [x] **P2. Middleware** `Modules/Assign/Routes/api.php` (7 route discount-types, dòng 650–659): `checkPermission:Quản lý danh mục loại chiết khấu` → `...loại giảm giá`.
- [x] **P3. Menu** `components/menu-sidebar.js` (dòng 382): `isShow: ['Quản lý danh mục loại chiết khấu']` → `['Quản lý danh mục loại giảm giá']`.
- [x] **P4. Verify** `php -l` seeder + api.php OK; grep sạch chuỗi quyền cũ toàn repo (trừ Migrations lịch sử).
- [ ] **P5. Verify E2E** (user): **BẮT BUỘC chạy lại seeder** `php artisan db:seed --class="Modules\Timesheet\Database\Seeders\PermissionsTableSeeder"` (+ reset cache spatie) trên mỗi môi trường → tên quyền đổi trong DB; user có quyền vẫn thao tác được (id không đổi); route trả 403 đúng khi thiếu quyền.

> ⚠️ LƯU Ý DEPLOY: middleware giờ check tên MỚI. Nếu DB chưa reseed (vẫn tên cũ) → mọi thao tác discount-types bị 403. Phải reseed permission đồng thời khi deploy code.

## Phase 3 — Đổi nhãn "Chiết khấu/CK" → "Giảm giá/GG" trên toàn màn Báo giá

> Đồng bộ nhãn hiển thị (label/tiêu đề cột/từ khóa/message/button) liên quan Chiết khấu trên tất cả màn Báo giá (tạo/sửa/xem/in/Excel). GIỮ nguyên: tên biến (`discountMethod`, `hasCk`), khóa dữ liệu (`discount_*`), class CSS, công thức, và alias import cũ (`'CK(%)'`, `'Chiết khấu(%)'` — để file Excel cũ vẫn import được).

- [x] **Q1. FE edit.vue** (tạo/sửa): CK→GG (Không GG, GG mặt hàng, GG tổng, GG(%)/(₫), Đơn giá sau GG, GG phân bổ tự động, Phân bổ GG, Loại GG, Thành tiền GG, Tổng GG, Thêm khoản GG, sau GG (trước VAT), TSLN trước/sau GG, GG:/Sau GG:) + "Giảm giá tổng đơn hàng" + message inline (GG (%) phải trong 0–100%, GG không được lớn hơn đơn giá bán, GG vận chuyển...) + toast/confirm ("dữ liệu giảm giá", "Phân bổ giảm giá tự động", "phân bổ lại giảm giá"). Alias import: label→GG, thêm 'GG(%)'/'GG(₫)'/'Giảm giá(...)', GIỮ 'CK(%)'/'Chiết khấu(%)'.
- [x] **Q2. FE index.vue** (xem): toàn bộ nhãn CK/Chiết khấu → GG/Giảm giá (badge, cột, section, footer TSLN, tổng doanh thu trước/sau GG).
- [x] **Q3. FE component in** `QuotationPrintPreview.vue` + `QuotationPrintConfigModal.vue`: nhãn cột (GG (%), GG (₫), Đơn giá sau GG, GG phân bổ) + Tổng giảm giá + doanh thu trước/sau GG + Giảm giá.
- [x] **Q4. FE** `QuotationSubmitModal.vue` (Tổng giảm giá, Tổng bán sau GG) + `QuotationHistoryModal.vue` (nhãn tab "Giảm giá").
- [x] **Q5. BE Excel** `resources/views/exports/bom_list.blade.php`: bảng tổng hợp (Giảm giá, Thành tiền sau GG, doanh thu trước/sau GG, TSLN trước/sau GG, "GG: {tên}", Tổng GG, Tổng thành tiền giảm giá).
- [x] **Q6. BE** `QuotationController.php` (message "Đã phân bổ giảm giá", lỗi GG%/GG₫), `QuotationService.php` (methodLabels 'Không GG/GG theo...', message phân bổ/validate giảm giá), `QuotationHistory.php` ('Cập nhật giảm giá', giữ key `update_discount`).
- [x] **Q7. Rà soát catalog sót** (từ Phase 1): `DiscountTypeRequest.php` (Tên loại giảm giá), `DiscountTypeController.php` (message loại giảm giá), api.php comment.
- [x] **Q8. Verify** `php -l` tất cả file BE OK; grep sạch — mọi "CK/chiết khấu" còn lại chỉ là comment nội bộ + alias import (chủ đích). Công thức/khóa dữ liệu không đụng.
- [ ] **Q9. Verify E2E** (user): build FE + hard-refresh → màn tạo/sửa/xem/in/Excel hiển thị "Giảm giá/GG"; validate CK% inline hiện "GG (%)..."; import file Excel cũ (header CK) vẫn nhận nhờ alias; số liệu/tính toán không đổi.

### Checkpoint — 2026-07-01
Vừa hoàn thành: Phase 1 (BE prefix + FE rename nhãn catalog) + Phase 2 (rename quyền seeder/middleware/menu) + Phase 3 (rename nhãn Chiết khấu→Giảm giá toàn màn Báo giá: FE edit/view/print/submit/history + Excel blade + BE controller/service/history). php -l toàn bộ OK. Chỉ đổi text hiển thị; giữ biến/khóa/công thức/alias import.
Đang làm dở: (không)
Bước tiếp theo: user build FE + **reseed PermissionsTableSeeder** + E2E (T6 + P5 + Q9). Kiểm mã mới = GG-, quyền đổi tên nhưng phân quyền cũ giữ nguyên, import Excel cũ vẫn chạy.
Blocked:
