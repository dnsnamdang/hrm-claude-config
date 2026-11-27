# Fix: Lưu báo giá lỗi "Column 'product_trade_name' cannot be null" — @khoipv

URL lỗi (demo): `/plan/quotation/add?project_id=959` → bấm Lưu → `SQLSTATE[23000] 1048 Column 'product_trade_name' cannot be null (insert into quotation_tab_products ...)`.

## Phase 1 — Điều tra (XONG)

- [x] Demo: dự án 959 có 1 hàng id **1119** `TB-SH-1107` (Máy xét nghiệm sinh hóa tự động, CM-400) — danh mục `products.trade_name = null`.
- [x] FE `pages/plan/quotation/components/GeneralComponent.vue:1509` gán `product_trade_name: product.trade_name` → gửi null.
- [x] BE `QuotationService::syncGroups()` fill thẳng → cột `quotation_tab_products.product_trade_name` NOT NULL → 1048.
- [x] Cùng ràng buộc NOT NULL: `bid_package_products`, `contract_products`, `contract_product_kpis` → hàng này kết xuất sang gói thầu / HĐ cũng sẽ lỗi. Các bảng ủy quyền, HĐ mua, đơn mua đều nullable.
- [x] Nguồn dữ liệu thiếu: form hàng hóa (`ProductRequest`) + mẫu hàng hóa (`ProductTemplateRequest`) đều `required`. Import Excel đang dùng (`ProductImport`) bắt buộc Tên thương mại từ commit `d36a796d` (22/12/2025); 13 hàng ở local thiếu tên đều import 22/12/2025 trước bản fix đó. `ProductImportV2` (không được gọi ở đâu) vẫn chưa bắt buộc.

## Phase 2 — Fix (user chọn làm cả A + B, trên nhánh `master`)

- [x] Checkout `master` repo `hrm-thanhan-api` (đã khớp origin)
- [x] **A** — Migration `database/migrations/2026_11_27_100000_alter_product_trade_name_nullable.php`: `product_trade_name` → `VARCHAR(255) NULL` ở `quotation_tab_products`, `bid_package_products`, `contract_products`, `contract_product_kpis` (raw SQL, không phụ thuộc doctrine). `down()` đổi null → '' rồi trả về NOT NULL.
- [x] **B** — `ProductImportV2::$requiredFields` thêm `'trade_name' => 'Tên thương mại'` (đồng bộ với `ProductImport` đang dùng)
- [x] `php -l` + chạy migrate local + kiểm tra `information_schema` + insert thử dòng `quotation_tab_products` có `product_trade_name = null` (rollback) — local: migrate → rollback → migrate đều OK (mỗi lần ~15–20s do ALTER dựng lại bảng), 4 bảng `IS_NULLABLE = YES`, insert null thành công
- [ ] User test trên demo sau deploy + `php artisan migrate`: tạo lại báo giá dự án 959 → Lưu được
- [ ] (Tuỳ chọn) bổ sung Tên thương mại cho 13 hàng thiếu (local: 994, 1119, 1120, 1124, 1131, 1133, 1134, 1142–1144, 1168–1170)

### Checkpoint — 2026-11-27
Vừa hoàn thành: migration nullable 4 bảng + `ProductImportV2` bắt buộc Tên thương mại (nhánh `master` repo API, chưa commit)
Đang làm dở: —
Bước tiếp theo: user review + commit/push → deploy API + `php artisan migrate` → tạo lại báo giá dự án 959 trên demo
Blocked:
