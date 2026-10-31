# Chuyến xe chở hàng — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Chuyển trọn luồng Chuyến xe chở hàng (ERP `deliveryTrip.*`) sang HRM — màn Vận chuyển + phiếu xuất kho gắn chuyến — giữ nguyên cách tính ERP; phiếu hạch toán vẫn ở ERP.

**Architecture:** BE trong `Modules/Transport` cạnh Chuyến xe khác (entity ghi riêng, service đọc / ghi / in), các hàm tra cước-xe-tuyến tách ra service dùng chung của module; phần chuyến xe của PNK tách ra service dùng chung rồi PXK (`Modules/Assign`) gọi lại. FE `pages/transport/delivery-trips` khuôn `pages/transport/other-delivery-trips`; popup tạo chuyến là component dùng lại ở form PXK / PNK.

**Tech Stack:** Laravel (hrm-api, PHPUnit 9), Nuxt 2 / Vue 2 (hrm-client, V2Base*), MySQL `gop_db`.

**Spec:** `hrm-claude-config/hrm/docs/superpowers/specs/gop-db/2026-10-31-chuyen-xe-cho-hang-design.md` (đọc kèm — mục 4, 6.3, 7, 8, 10, 11).

## Global Constraints

- Cách tính giữ NGUYÊN ERP (user 31/10): đi 2 chiều chỉ ×2 km định mức, **cước không ×2**; trần = cước 1 chiều + cước vượt trội; `is_company_sp` y JSA:53-79 (không tự tắt); `company_pay` y C:572-574; `driver_cost` = `depreciation` = `loading_cost` = 0.
- Chỉ 2 chỗ khác ERP về cách hiện: vượt trần → báo đỏ (không kéo về); chia cước dòng cuối nhận phần lẻ, dung sai tổng 0,01.
- Trạng thái: 2 Đang tạo (xám) · 4 Đang chạy (vàng) · 1 Chờ hạch toán (vàng) · 6 Không duyệt (đỏ) · 5 Đang hạch toán (vàng) · 3 Đã hạch toán (xanh).
- Mã `{company.code}_CXCH_{generateCode(5, id)}`; tên `{TP|supplier.code} - {payload} - {BSX} - d/m/Y-H:i` (trùng thì thêm giây — như CXK).
- Quyền tên y ERP qua trait `ChecksEmployeePermission` (khuôn CXK): Thủ kho (vào màn), Xem chuyến xe theo tổng công ty / công ty / phòng ban (đã có api), **Hạch toán chuyến xe chở hàng** (thêm api cuối seeder, `type` 22), Hạch toán vận chuyển (nhận thông báo).
- BE chặn đúng điều kiện nút: thiếu quyền 403, sai trạng thái 409 `"Trạng thái đã bị thay đổi. Vui lòng load lại trang"`, ngoài phạm vi 404.
- Thông báo: Kết thúc → quyền Hạch toán vận chuyển cùng công ty; Không duyệt → người tạo. Prefix `[CXCH]`, ≤ 120 ký tự (skill notification-convention).
- Không commit / push (rule project) — user tự yêu cầu. Làm trên nhánh `feat/chuyen-xe-cho-hang` cả 2 repo.
- Mọi UI theo checklist skill `erp-to-hrm-screen` (V2BaseSmartFilterPanel floating, V2BaseBadge, V2Footer, CreatorInfoLine, SystemInfoSection, ô rỗng để trống, số `1,234,567.89`).

## Review Focus

1. Công ty chưa có bảng giá / tải trọng không có trong bảng giá → form duyệt báo "Chưa có bảng giá hiệu lực", không 500 (ERP crash C:423) — test ở Task 4.
2. Hai người duyệt xuất phát 2 chuyến cùng xe gần như cùng lúc → chỉ 1 chuyến được Đang chạy (`lockForUpdate` xe) — test ở Task 5.
3. PXK gỡ chuyến đã Đang chạy / Chờ hạch toán → bị chặn, chuyến không mất phiếu — test ở Task 10.
4. Chuyến có cả PXK lẫn PNK → Duyệt xe xuất phát xét step của cả 2 loại, link đúng loại phiếu — test ở Task 4.
5. Chia cước 1.000.000 cho 3 phiếu → tổng các dòng đúng bằng cước thực tế, BE nhận — test ở Task 5.

---

### Task 0: Nhánh làm việc

- [x] **Step 1:** Cả `hrm-api` và `hrm-client`: `git fetch origin && git switch -c feat/chuyen-xe-cho-hang origin/develop`. Kiểm `git log -1 origin/develop` có commit Chuyến xe khác (`feat(transport): màn Chuyến xe khác`).
- [x] **Step 2:** Chạy `php vendor/bin/phpunit Modules/Transport/Tests/Feature/OtherDeliveryTripApiTest.php` → `OK (5 tests, 90 assertions)` làm mốc.

### Task 1: Tách tra cứu dùng chung của phân hệ Vận chuyển

**Files:**
- Create: `hrm-api/Modules/Transport/Services/Delivery/DeliveryLookupService.php`
- Create: `hrm-api/Modules/Transport/Services/Concerns/FormatsDeliveryValues.php`
- Modify: `hrm-api/Modules/Transport/Services/OtherDeliveryTrip/OtherDeliveryTripService.php:256-605` (+ chỗ gọi trong WriteService / PrintService / Controller)

**Interfaces:**
- Produces `DeliveryLookupService`: `priceList(bool $fallbackLatest)`, `vehicles(?int $keepId = null): array`, `vehicleInfo(int $vehicleId): ?array` (bỏ tham số trip — phần phụ thuộc chuyến để lại CXK), `vehicleCategories(): array`, `vehiclePayloads(int $categoryId): array`, `extraPrice(int $categoryId, int $payloadId): array`, `roadCost(int $roadId, int $categoryId, int $payloadId): array`, `roads(Request $r): array`, `employees(Request $r): array`, `employeeOption(int $id): ?array`, `static vatPercent(?int $companyId = null): float`. Docblock "Nơi đang dùng: Chuyến xe khác, Chuyến xe chở hàng".
- Produces trait `FormatsDeliveryValues`: `static num($v): ?float`, `static dmy($v): string`, `static dmyHi($v): string`, `static employeeLabel($deptCode, $fullname): string`.

- [x] **Step 1:** Chuyển nguyên thân các hàm trên sang 2 file mới (không sửa logic); `OtherDeliveryTripService` inject `DeliveryLookupService`, các hàm cũ còn được gọi từ controller CXK thì ủy quyền 1 dòng hoặc controller gọi thẳng service mới.
- [x] **Step 2:** `php vendor/bin/phpunit Modules/Transport/Tests/Feature/OtherDeliveryTripApiTest.php` → vẫn `OK (5 tests, 90 assertions)`.

### Task 2: Chuyến xe khác về cách tính ERP (đi 2 chiều không ×2 cước)

**Files:**
- Modify: `hrm-api/Modules/Transport/Services/OtherDeliveryTrip/OtherDeliveryTripWriteService.php:379-392` (trần), `OtherDeliveryTripPrintService.php` (`$recipe` trong `detailPairs`)
- Modify: `hrm-client/pages/transport/other-delivery-trips/components/OtherDeliveryTripForm.vue:179,806,1068` (hint, `costCeiling`, `applyFormula`)
- Test: `hrm-api/Modules/Transport/Tests/Feature/OtherDeliveryTripApiTest.php:~210`
- Doc: spec CXK mục 1 Q4 + mục 6 công thức → "giữ ERP (user 31/10/2026)"

- [x] **Step 1:** Sửa test 2 chiều: chuyến cước tuyến `C`, đi 2 chiều, vượt trội 0 → lưu `total_cost_transition = 2C` trả **422** lỗi trần; `= C` lưu OK; `delivery_recipe` = `C`.
- [x] **Step 2:** Chạy test → FAIL (đang cho 2C).
- [x] **Step 3:** Bỏ hệ số `(is_two_way ? 2 : 1)` ở trần BE, cước theo công thức ở bản in và `costCeiling` / `applyFormula` / hint FE (km định mức vẫn ×2).
- [x] **Step 4:** Chạy test → PASS. Mở form tuyến cố định tick Đi 2 chiều: cước mặc định không đổi, hint "Tối đa: cước theo công thức + cước vượt trội."

### Task 3: Entity, quyền, phạm vi

**Files:**
- Create: `hrm-api/Modules/Transport/Entities/DeliveryTrip/DeliveryTrip.php`, `DeliveryTripActivity.php` (bảng `delivery_trips`, `activity_has_delivery_trips`)
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (cuối file)
- Test: `hrm-api/Modules/Transport/Tests/Feature/DeliveryTripApiTest.php` (fixture khuôn `OtherDeliveryTripApiTest`)

**Interfaces:**
- Produces hằng `DANG_TAO=2, DANG_CHAY=4, CHO_HACH_TOAN=1, KHONG_DUYET=6, DANG_HACH_TOAN=5, DA_HACH_TOAN=3`; `TYPE_ALL='all'`, `TYPE_WAITING='waiting'`; `PERMISSION_ACCESS='Thủ kho'`, `PERMISSION_ACCOUNTING='Hạch toán chuyến xe chở hàng'`, `PERMISSION_ACCOUNTING_NOTIFY='Hạch toán vận chuyển'`, 3 hằng Xem chuyến xe (dùng lại tên ở `OtherDeliveryTrip`).
- Produces `static statusMetaOf($status): array{name,type,color}`, `static canAccess(): bool`, `static scopedQuery(string $type): Builder`, `activities()`, `warehouseExports()`, `warehouseImports()`, `generateCode(): void`, `formKind(): string` (`'shipping'|'other'|'company'` theo `is_sent` → `!vehicle.is_tanphat`), `canView/canEdit/canDelete/canStart/canFinish/canDeny/canAccounting(): bool`, `abilities(): array` (`can_edit, can_delete, can_start, can_finish, can_deny, can_accounting`).
- Điều kiện đúng spec mục 4 / 5 (M:327-364); `canStart` xét cả PXK step 3 lẫn PNK step `DANG_NHAP`; `waiting` = status 1 + công ty mình, gate `PERMISSION_ACCOUNTING`.

- [x] **Step 1:** Test `test_scope_and_abilities`: (a) không quyền Thủ kho → 403 danh sách; (b) chuyến Đang tạo của người khác không hiện ở `all`, hiện khi status 1; (c) `waiting` không quyền hạch toán → 403, có quyền → chỉ status 1 cùng công ty; (d) `abilities` của chuyến status 2 có 1 PXK step 2 → `can_start=false`, step 3 → `true`; có thêm PNK chưa `DANG_NHAP` → `false`; (e) chuyến có phiếu → `can_delete=false`.
- [x] **Step 2:** Chạy → FAIL (chưa có route — test chạy sau Task 4 route index; viết entity trước, assert qua `abilities()` cho (d)(e)).
- [x] **Step 3:** Viết entity + seeder `$this->perm(['name' => 'Hạch toán chuyến xe chở hàng', 'display_name' => 'Hạch toán chuyến xe chở hàng', 'group' => 'Chuyến xe', 'type' => 22, 'sort_order' => 7])`; `php artisan permission:sync --dry-run` chỉ báo thêm 1 quyền.
- [x] **Step 4:** Chạy test phần (d)(e) → PASS.

### Task 4: Service đọc + route danh sách / chi tiết / dữ liệu form duyệt

**Files:**
- Create: `hrm-api/Modules/Transport/Services/DeliveryTrip/DeliveryTripService.php`
- Create: `hrm-api/Modules/Transport/Http/Controllers/V1/DeliveryTrip/DeliveryTripController.php`
- Modify: `hrm-api/Modules/Transport/Routes/api.php` (group `/delivery-trips`, route tĩnh trước `/{id}`, KHÔNG checkPermission — controller kiểm `canAccess()` như CXK)
- Test: `DeliveryTripApiTest.php`

**Interfaces:**
- Consumes Task 1, Task 3.
- Produces `listQuery(Request): Builder` (lọc spec 6.1: `code, name, vehicle_id, supplier_id, voucher_code, status, created_by, cost_from, cost_to, approved_from, approved_to, keyword`; sort `sort_by`/`sort_dir` mặc định `created_at desc`), `listRows($items): array` (khoá: `code, name, plate_name, supplier_name, vouchers[{type,id,code}], total_cost_transition, status_text, status_color, creator_name, created_at, approved_time` + `abilities`), `filterOptions(): array`, `detail(DeliveryTrip): array` (đủ cột 3.1 + `form_kind`, `vehicle`, `vouchers`, `activities[{id, voucher_type, voucher_id, voucher_code, customer_name, road_name, km, total_cost_transition, requester_name, is_bulky, is_company_sp, contract_value}]`, `default_road` (tuyến chuyến hoặc phiếu đầu — M:285-291), `price` = `{road_cost, extra_price, km_actual}` hoặc `price_error` "Chưa có bảng giá hiệu lực", `company_pay_km`, `pay_value_order`, `vat_percent`, `reason_deny`, `abilities`).
- Routes: `GET /`, `/filter-options`, `/form-meta`, `/lookups/*` (ủy quyền DeliveryLookupService), `GET /{id}`.

- [x] **Step 1:** Test `test_list_filters_and_detail`: danh sách lọc `status=1` chỉ ra status 1; `voucher_code` theo mã PXK; dòng có `vouchers` gồm cả PXK và PNK đúng `type`; `detail` chuyến xe ngoài không có bảng giá → `price_error` = "Chưa có bảng giá hiệu lực" và HTTP 200; `form_kind` = `shipping` khi `is_sent=1`.
- [x] **Step 2:** Chạy → FAIL. **Step 3:** Viết service + controller + route. **Step 4:** Chạy Task 3 + 4 → PASS.

### Task 5: Ghi — tạo / sửa / xoá / xuất phát / kết thúc / không duyệt

**Files:**
- Create: `hrm-api/Modules/Transport/Services/DeliveryTrip/DeliveryTripWriteService.php`
- Modify: controller + route (`POST /`, `PUT /{id}`, `DELETE /{id}`, `POST /{id}/start`, `/{id}/finish`, `/{id}/deny`, `/upload-files`, `/{id}/attachment-sizes`, `DELETE /{id}/files`, `/{id}/histories`, `/{id}/histories/filter-options`)
- Modify: `hrm-api/app/Services/CatalogHistoryService.php` (khai `delivery_trips` — khuôn `other_delivery_trips`)
- Test: `DeliveryTripApiTest.php`

**Interfaces:**
- Produces `store(array): DeliveryTrip` (popup spec 6.2: không gửi hàng bắt `vehicle_id, vehicle_category_id, vehicle_payload_id`; gửi hàng bắt `vehicle_id, driver_id, employee_id, note`), `update(DeliveryTrip, array)` (chỉ `vehicle_id`, `is_two_way`; sinh lại `name`), `destroy(DeliveryTrip)` (gỡ `tmp_warehouse_export_lot_details.delivery_trip_id`, xoá activity, xoá chuyến), `start(DeliveryTrip, array)`, `finish(DeliveryTrip, array)`, `deny(DeliveryTrip, string $reason)`.
- Rule start/finish theo `formKind()` y C:452-512 trừ: bỏ `loading_cost`; `km_start` (start) / `km_finish` (finish) bắt khi `vehicle_company_id` = công ty người dùng; ghi chú `diff_note` bắt khi `diff_cost != 0` hoặc `business_trip_cost != 0` (company) / `diff_cost != 0` (other); file bắt khi có `toll_cost` mà chưa có file; finish company: `total_km_suggest ≤ total_km_real`, ≠ `total_km_rated` thì bắt `diff_note` + file; trần `total_cost_transition ≤ road_cost + price_additional` (không ×2); `|Σ activities.total_cost_transition − total_cost_transition| ≤ 0.01`; shipping: `total_cost_shipping`, `sender_id` bắt buộc.
- Ghi y C:555-660 (VAT, `company_pay`, `cost_need_allocation`, `total_packages`, `date_start_run` khi 4, `total_km_suggest` + `date_finish_run` khi 1, `approved_time`, cập nhật từng activity theo khoá phiếu: cước, `driver_cost / n`, VAT, lái xe, `is_bulky`, `is_company_sp`). Start: trong transaction `lockForUpdate` các chuyến cùng `vehicle_id` rồi chặn "Xe có chuyến đang chạy!".
- Thông báo (sau commit): finish → `[CXCH] Chờ hạch toán: <b>{code}</b>.` tới quyền Hạch toán vận chuyển cùng công ty, link chi tiết HRM; deny → `[CXCH] Không duyệt: <b>{code}</b>. {lý do cắt}` tới người tạo.

- [x] **Step 1:** Test `test_create_edit_delete`, `test_start_finish_flow` (xe ngoài: start 422 khi thiếu tuyến; trần: cước 1 chiều `C` + vượt trội `P`, đi 2 chiều, gửi `C+P+1` → 422, `C+P` → OK, `total_km_rated = 2 × km`; start → 4; chuyến thứ 2 cùng xe start → 422 "Xe có chuyến đang chạy!"; finish → 1, có thông báo; chia 1.000.000 cho 3 dòng `333333.33, 333333.33, 333333.34` → OK), `test_deny_and_refinish` (deny thiếu lý do 422; không quyền 403; status 2 → 409; deny → 6 + `reason_deny`; người tạo finish lại → 1), `test_shipping_kind` (bắt `sender_id`, không bắt tuyến), `test_forbidden_actions` (người khác sửa/xoá/start → 403; xoá chuyến có phiếu → 409).
- [x] **Step 2:** Chạy → FAIL. **Step 3:** Viết WriteService + route + lịch sử (trait `LogsCatalogHistory`, `BuildsAttachmentHistoryChange`). **Step 4:** Chạy → PASS.

### Task 6: In + Excel

**Files:**
- Create: `hrm-api/Modules/Transport/Services/DeliveryTrip/DeliveryTripPrintService.php`, `Exports/DeliveryTrip/DeliveryTripExport.php`, `Resources/views/prints/delivery_trip.blade.php`, `delivery_trip_list.blade.php`, `Resources/views/exports/delivery_trip.blade.php`
- Modify: controller + route (`GET /export-rows`, `/print-list-data`, `/{id}/print-data`, `/{id}/export`)

**Interfaces:** khuôn y hệt `OtherDeliveryTripPrintService` (`detailPairs / detailHtml / excelData / listHtml / exportRows`, `EXPORT_COLUMNS` = cột spec 6.1). Nhãn mẫu 328 (spec 7 #6); cước theo công thức = cước 1 chiều; "Đi 2 chiều" đọc cột chuyến; không có bảng giá → ô trống, không lỗi. File `chi_tiet_chuyen_xe_{code}.xlsx`.

- [x] **Step 1:** Test `test_print_and_export`: `print-data` chuyến đi 2 chiều chứa "Đi 2 chiều: Có"; chuyến không bảng giá → 200; `/{id}/export` ô số kiểu `n`; người ngoài phạm vi → 404.
- [x] **Step 2:** FAIL → **Step 3:** viết → **Step 4:** PASS (đọc lại file bằng PhpSpreadsheet theo skill export-excel §7).

### Task 7: FE danh sách + popup tạo/sửa + menu

**Files:**
- Create: `hrm-client/pages/transport/delivery-trips/index.vue`, `components/constants.js` (`DT_API='transport/delivery-trips'`, `DT_LIST='/transport/delivery-trips'`, `DT_TYPES`), `components/row-actions.js` (`dtRowActions(item)`, `runDtAction(vm, action, item)` — Sửa (mở popup), Xoá, Duyệt xe xuất phát, Kết thúc chuyến xe, Không duyệt (về chi tiết), Hạch toán chuyến xe (ERP `/admin/warehouse/delivery_trip_accounting/create?delivery_trip_id=`), In, Xuất Excel, Lịch sử)
- Create: `hrm-client/components/transport/DeliveryTripFormModal.vue` — popup Tạo/Sửa dùng chung (props `tripId?`; emit `saved(trip {id, name})`), `unsavedModalMixin`
- Modify: `hrm-client/components/subsystem-menu/transport.js:28` → `{ label: 'Chuyến xe chở hàng', link: '/transport/delivery-trips', isShow: ['Thủ kho'] }` + `{ label: 'Chuyến xe chở hàng chờ hạch toán', link: '/transport/delivery-trips?type=waiting', isShow: ['Hạch toán chuyến xe chở hàng'] }`

- [x] **Step 1:** Dựng theo `pages/transport/other-delivery-trips/index.vue` (mixin, `columnScreenKey='transport_delivery_trips'`, `localStorageKey` riêng, `V2BaseSmartFilterPanel floating`, cột + lọc spec 6.1, cột Phiếu link qua `utils/stock-voucher-link.js`).
- [x] **Step 2:** Verify Playwright 1366px (gán tạm quyền vào `role_has_permissions` theo memory, gỡ sau): chụp danh sách, lọc Trạng thái (chờ ≥ 3s), tạo chuyến xe ngoài + gửi hàng qua popup, sửa đổi xe, xoá; đếm request vào màn = 1.

### Task 8: FE form duyệt / chi tiết (3 kiểu)

**Files:**
- Create: `hrm-client/pages/transport/delivery-trips/components/DeliveryTripApproveForm.vue` (props `mode: 'start'|'finish'|'show'`, `recordId`), `_id/index.vue`, `_id/start.vue`, `_id/finish.vue`

**Interfaces:** Consumes `detail` Task 4 (`form_kind`, `price`, `activities`…) và API Task 5. Công thức FE đúng spec 6.3 (không ×2 cước; trần báo đỏ; chia dòng cuối nhận phần lẻ; `is_company_sp` = `km ≤ company_pay_km && is_bulky && contract_value ≥ pay_value_order`, chỉ bật khi tick, không tự tắt — y JSA); `price_error` hiện lỗi đỏ dưới ô cước và chặn gửi. Footer `V2Footer` slot: start "Duyệt xe xuất phát" / finish "Kết thúc chuyến xe" (primary) / show theo `can_*`: Không duyệt (danger, popup nhập lý do bắt buộc), Hạch toán (ERP), Sửa, Xoá, In, Xuất Excel. Khoá ô có ⓘ (không ở chi tiết).

- [x] **Step 1:** Dựng component; Lịch sử `SystemInfoSection` ở chi tiết.
- [x] **Step 2:** Verify Playwright: chuyến xe ngoài có PXK (step 3) → start (đổi tuyến, tick 2 chiều: km định mức ×2, cước không đổi; nhập vượt trần → đỏ) → finish → chi tiết status Chờ hạch toán → Không duyệt có lý do → finish lại; chuyến gửi hàng start/finish. Chụp ảnh từng màn, so `other-delivery-trips`.

### Task 9: Tách phần chuyến xe của PNK ra service dùng chung (Q2 đã duyệt)

**Files:**
- Create: `hrm-api/Modules/Finance/Services/Delivery/StockVoucherTripService.php`
- Modify: `hrm-api/Modules/Finance/Services/WarehouseImportWriteService.php:300-315, 803-829, 974-986, 1188-1245` (gọi service mới)

**Interfaces:**
- Produces `tripOptions(Request): array` (chuyến status 2 + `include_ids`, trả thêm `plate_name`), `sync(string $column, int $voucherId, array $trips): void` (`$column` ∈ `warehouse_export_id|warehouse_import_id`; chuyến phải status 2), `update(string $column, int $voucherId, array $trips, bool $keepTransition): void` (giữ chuyến 1/3/4 — bắt buộc còn trong danh sách; chuyến mới ∈ {1,2,4}; đổi hình thức → trả chuyến chỉ còn gắn phiếu này về 2, xoá liên kết), `guardSend(array $tripIds): void` (còn chuyến status 2 → 422 "Bạn cần duyệt xe xuất phát trước khi gửi"), `hasUnapproved(string $column, int $voucherId): bool`, `copy(string $column, int $fromId, int $toId): void` (re-export / re-import, gọi SAU khi lưu phiếu con). Docblock "Nơi đang dùng: PNK, PXK".

- [x] **Step 1:** Chạy test PNK hiện có (`grep -l "trip" Modules/Finance/Tests -r`) làm mốc. **Step 2:** Chuyển thân hàm (không đổi hành vi). **Step 3:** Test PNK vẫn PASS + test mới `StockVoucherTripServiceTest` (sync chuyến status 4 → lỗi; update gỡ chuyến status 4 → lỗi; copy chép đúng `warehouse_export_id` mới). **Step 4:** Verify tay form PNK chọn chuyến vẫn chạy.

### Task 10: PXK BE gắn chuyến

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/WarehouseExportService.php` (`createFromExportRequest` :25-81, `updateAndSend` :240-268, `reExport` :275-332, bỏ dòng docblock :273 "Không port trips"), `Http/Controllers/Api/V1/WarehouseExportController.php` (`createDataFromRequest` :349-388, `storeFromRequest`/`update`/`reExport` rule :146,185,452, `show` :87, `pickOrEditPayload` :298), `Entities/Warehouse/WarehouseExport.php:113-120` (`trips()`, `has_unapproved_trip` thật)
- Modify: `hrm-api/Modules/Assign/Routes/api.php` (`GET assign/warehouse-exports/trip-options` → `StockVoucherTripService::tripOptions`)
- Test: `hrm-api/Modules/Assign/Tests/Feature/WarehouseExportTripTest.php`

**Interfaces:** request `transition_type ∈ {1,2,3}`, khi 2: `trips[].delivery_trip_id` (required, distinct); màn sửa thêm `road_id`, `total_km_actual` (1..999999), `transition_note` (bắt khi ≠ `total_km_expected`) — miễn khi có chuyến `is_sent`. Tạo từ đề nghị: `transition_type` + `total_km_expected` lấy từ YCXH (`product_export_requests`). Response `show` / edit thêm `transition_type, transition_type_name, road {id,name}, total_km_expected, total_km_actual, transition_note, trips[{delivery_trip_id, name, status}]`.

- [x] **Step 1:** Test: tạo PXK hình thức 2 với chuyến status 4 → 422; với chuyến 2 → có dòng `activity_has_delivery_trips`; sửa thiếu tuyến (không gửi hàng) → 422, có chuyến gửi hàng → OK; gửi duyệt khi chuyến còn 2 → 422 "Bạn cần duyệt xe xuất phát trước khi gửi"; gỡ chuyến status 4 → 422; đổi sang hình thức 1 → chuyến chỉ gắn phiếu này về 2 + xoá liên kết; re-export chép chuyến với `warehouse_export_id` = phiếu con.
- [x] **Step 2:** FAIL → **Step 3:** viết → **Step 4:** PASS + test PXK hiện có của module Assign vẫn PASS.

### Task 11: PXK FE + nút tạo nhanh chuyến ở PXK / PNK

**Files:**
- Create: `hrm-client/components/transport/StockVoucherTripsField.vue` — khối "Hình thức vận chuyển" (radio 3 lựa chọn; khi 2: danh sách chuyến `V2BaseSelectRemote` `trip-options` + nút "+" mở `DeliveryTripFormModal`, chuyến 1/3/4 khoá + ẩn nút xoá; màn sửa thêm Tuyến (khoá khi có chuyến 1/4) / Km dự kiến (khoá) / Km chốt / Ghi chú vận chuyển); props `value`, `mode: 'create'|'edit'|'show'`, `tripApi`, `errors`
- Modify: `hrm-client/pages/finance/warehouse-exports/create.vue:201`, `_id/edit.vue:216`, `_id/re-export.vue:262`, `_id/index.vue` (bỏ cố định `transition_type: 1`, gắn khối trên); `pages/finance/warehouse-imports/components/WarehouseImportForm.vue:68-128` (thêm nút "+" tạo nhanh — dùng lại modal, không đổi phần còn lại)

- [x] **Step 1:** Dựng component + gắn PXK; PNK chỉ thêm nút "+".
- [x] **Step 2:** Verify Playwright: PXK từ đề nghị có YCXH hình thức 2 → khối hiện sẵn → "+" tạo chuyến → chọn → lưu; sửa: tuyến + km chốt lệch → bắt ghi chú; chi tiết hiện khối chỉ xem; PNK "+" tạo chuyến được chọn ngay.

### Task 12: Nghiệm thu luồng trọn + tài liệu

- [x] **Step 1:** Playwright luồng trọn (1366px): tạo chuyến → PXK chọn chuyến → lấy hàng / lưu (step 3) → Duyệt xe xuất phát → gửi PXK → Kết thúc → chờ hạch toán (`?type=waiting`) → Không duyệt → Kết thúc lại → nút Hạch toán mở ERP. Chụp ảnh từng bước; đóng browser; gỡ quyền tạm.
- [x] **Step 2:** Chạy toàn bộ test Transport + PXK + PNK → PASS.
- [x] **Step 3:** Đối chiếu ngược ERP (Bước 5) + ngang màn CXK / PNK (Bước 5b) theo skill `erp-to-hrm-screen`, chạy khối grep tự kiểm trên `pages/transport/delivery-trips` + `components/transport`.
- [x] **Step 4:** Cập nhật `.plans/gop-db/STATUS.md`, plan này, memory `project_bbgn_van_chuyen.md`; báo user (không commit).

## Checkpoint — 2026-10-31
Vừa hoàn thành: Task 0-12 (BE + FE + test + nghiệm thu tay local). Test: Transport 14/215, StockVoucherTripService 4/13, PNK Type7 4/18, PXK Assign 36 pass / 9 skip (có sẵn).
Đang làm dở: —. Review toàn nhánh xong: sửa C1 (đổi hình thức gỡ được chuyến đang chạy → chặn cả PXK + PNK — user chốt), I1 (không duyệt chéo công ty), I3 (xe ngoài của công ty mình bị bắt km ẩn), M1, M2. Test: Transport 16/218, PXK 37 pass / 9 skip.
Bước tiếp theo: user review + commit (2 repo, nhánh feat/chuyen-xe-cho-hang); thử lưu PXK có chuyến trên dev (local ĐNXK lỗi dữ liệu lô có sẵn).
Blocked: —

## Ngày 31/10/2026 (@junfoke)
- [x] 31/10/2026 — Làm chuyển đổi erp->hrm: Chuyến xe chở hàng - 100% code (BE Modules/Transport + PXK gắn chuyến + tách StockVoucherTripService dùng chung PNK/PXK + DeliveryLookupService dùng chung CXK; FE danh sách, popup tạo/sửa, form duyệt 3 kiểu, chi tiết, in, Excel, menu; CXK về cách tính ERP không ×2 cước). Playwright local đạt. CHƯA commit.
- [x] 31/10/2026 — Khảo sát luồng ERP Chuyến xe chở hàng (tạo → gắn phiếu kho → duyệt xuất phát 3 kiểu → kết thúc → hạch toán/không duyệt) + đối chiếu HRM; viết spec `2026-10-31-chuyen-xe-cho-hang-design.md` (qua reviewer) + plan 12 task. User chốt: làm trọn luồng trên HRM (gồm PXK gắn chuyến), giữ nguyên cách tính ERP, có popup tạo nhanh chuyến ở PXK/PNK, không làm tab Bốc xếp và chuyến theo nhóm hàng lúc lấy hàng.
- [x] 31/10/2026 — Sửa theo review toàn nhánh (mỗi lỗi có test): PXK đổi hình thức vận chuyển gỡ được chuyến đang chạy (C1); kế toán công ty khác "Không duyệt" được chuyến (I1); xe ngoài của công ty mình bị bắt nhập km ở ô ẩn (I3); M1 so lại phiếu trong transaction, M2 escape từ khoá tìm chuyến.
- [x] 31/10/2026 — Theo user: PNK cũng chặn đổi hình thức khi chuyến đã xuất phát / chờ hạch toán / đã hạch toán ("Không được gỡ chuyến xe đã duyệt."); chuyến Đang hạch toán vẫn gỡ được và lối "chờ hạch toán" + nút "Tạo chuyến xe" vẫn cần quyền Thủ kho — giữ như ERP. Test: dùng chung 5/5, PNK 4/4, PXK gắn chuyến 5/5.
