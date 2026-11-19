# Plan — Fix: Yêu cầu xuất hàng thiếu popup confirm khi Hủy sửa (chưa lưu)

Phụ trách: @namdangit · Nhánh: gop_db

## Bối cảnh / Bug
Màn `finance/product-export-requests/{id}/edit` (Sửa yêu cầu xuất hàng): sửa thông tin rồi
bấm **Quay lại** KHÔNG hiện popup confirm "Thông tin chưa lưu" như quy tắc chung (QLDA_002/008).
Màn mẫu làm đúng: `finance/bill-income-requests/{id}/edit`.

## Nguyên nhân gốc
Trang vỏ `edit.vue` gắn `unsavedChangesMixin` và uỷ quyền `unsavedSnapshotSource()` sang
`this.$refs.form.snapshotSource()`. Nhưng form con nằm sau `v-else-if="initialData"` (chỉ render
sau khi fetch xong, tức SAU `mounted`). Khi mixin đăng ký `$watch(() => this.unsavedSnapshot())`
trong `mounted`, `$refs.form` còn `undefined` → getter trả `null`, KHÔNG chạm reactive data nào
→ watcher không gom được dependency → KHÔNG bao giờ nổ lại khi user gõ → `unsavedUserChanged`
luôn `false` → `isFormDirty()` luôn `false` → không hỏi.
(create.vue không bị vì render form ngay, nhưng đang phụ thuộc thời điểm render — fragile.)

## Cách sửa (theo skill unsaved-changes §2b — "trang vỏ + form con", giống màn bill-income)
- [x] Form con `ProductExportRequestForm.vue`: gắn `unsavedChangesMixin`, override
      `unsavedSnapshotSource()` → `snapshotSource()`, `markFormPristine()` ở cuối hàm load (nextTick).
- [x] Trang vỏ `_id/edit.vue`: đổi sang `unsavedChildFormMixin`; bỏ `unsavedSnapshotSource`/`onFormReady`;
      gọi `this.$refs.form?.markFormSaved()` sau khi PUT thành công.
- [x] Trang vỏ `create.vue`: đổi tương tự (nhất quán + hết phụ thuộc thời điểm render).
- [x] Verify Playwright: dirty→Quay lại hiện popup; Ở lại giữ data; không sửa→Quay lại thoát thẳng;
      F5/điều hướng khi dirty → dialog beforeunload.

### Checkpoint — 2026-10-09
Vừa hoàn thành: fix 3 file + verify Playwright 4 ca (edit PYCXH-35690) — tất cả PASS.
Đang làm dở: không
Bước tiếp theo: (tuỳ user) commit trên gop_db khi được yêu cầu.
Blocked:

## File đã sửa
- hrm-client/pages/finance/product-export-requests/components/ProductExportRequestForm.vue
- hrm-client/pages/finance/product-export-requests/_id/edit.vue
- hrm-client/pages/finance/product-export-requests/create.vue

## Bug 2 — Đề nghị xuất kho (ĐNXK, warehouse-export-requests) Hủy sửa thiếu popup
- [x] Kiểm tra `warehouse-export-requests/_id/edit.vue` + `create.vue`: **KHÔNG có bug**.
      Khác kiến trúc màn YCXH: ĐNXK là **form inline ngay trong page route** (không phải vỏ + form con),
      nên gắn `unsavedChangesMixin` TRỰC TIẾP là đúng — `this.form` khai reactive sẵn trong `data()`
      → watcher ở `mounted()` gom đủ dependency (không dính bẫy `$refs` undefined sau `v-else-if` như YCXH).
      `unsavedSnapshotSource()` gộp `warehouse_id/note/bear_the_shipping/rows(+files ở create)`;
      `markFormPristine()` cuối `fetchData` (nextTick); `markFormSaved()` trước mọi `$router.push`.
- [x] Verify Playwright trên PDNXK-31063 (tạm set status=3 để sửa, đã revert về 4):
      sửa Ghi chú (gõ phím) → Đóng → **hiện popup** "Thông tin chưa lưu" ✓ ;
      đổi select Kho xuất (select2) → Đóng → **hiện popup** ✓ ;
      Ở lại → giữ nguyên dữ liệu ✓ ; Thoát → về danh sách ✓ ; F5/điều hướng khi dirty → beforeunload ✓.
- Kết luận: ĐNXK đã làm đúng skill unsaved-changes từ đầu → **không cần sửa code**.

### Checkpoint — 2026-10-09 (bug 2)
Vừa hoàn thành: xác minh ĐNXK (edit + create) đã có guard chưa-lưu hoạt động đúng — không bug.
Đang làm dở: không
Bước tiếp theo: không có (chờ user nếu còn màn khác cần rà).
Blocked:

## Bug 3 — Phiếu xuất hàng (product-exports) Hủy sửa thiếu popup
- [x] Rà kiến trúc màn `pages/finance/product-exports/`: chỉ có **3 file** — `index.vue` (danh sách),
      `create.vue` (DUY NHẤT là form — "Lập phiếu xuất hàng") và `_id/index.vue` (xem chi tiết, không form).
      **KHÔNG có `_id/edit.vue`, KHÔNG có `components/*Form*.vue`** → không có màn "Sửa", cũng không có
      kiến trúc vỏ+form con như YCXH, nên bẫy `$refs` sau `v-else-if` về mặt kiến trúc không xảy ra được.
- [x] Kiểm tra `create.vue`: **KHÔNG có bug**. Form **inline** gắn `unsavedChangesMixin` trực tiếp (dòng 422);
      `note/rows/arrange/executors` đều khai reactive trong `data()` → watcher ở `mounted()` gom đủ dependency.
      `unsavedSnapshotSource()` (522) gộp `note / rows(+accs từng kho) / arrange(+executors)`;
      `markFormPristine()` cuối `fetchData` trong nextTick (578); `markFormSaved()` ở nhánh lưu thành công (936)
      trước khi set `done=true`; `goBack()` (947) → `/finance/product-export-requests`.
- [x] Verify Playwright trên PXK-30296 (status=2 Chờ duyệt, cty 1 — điều kiện `assertCanExportGoods`, read-only
      không lưu gì, không đụng data):
      gõ Ghi chú (keydown thật) → Quay lại → **hiện popup** "Thông tin chưa lưu" ✓ ;
      Ở lại → giữ nguyên ghi chú "a", dialog đóng ✓ ; Thoát → về `/finance/product-export-requests` ✓ ;
      mở mới không sửa gì → Quay lại → **thoát thẳng, không hỏi** (không false-positive) ✓.
- Kết luận: product-exports đã làm đúng skill unsaved-changes từ đầu → **không cần sửa code**.
  Màn này chỉ có luồng Tạo (không có Sửa) nên "lỗi tương tự" như YCXH không tồn tại ở đây.

### Checkpoint — 2026-10-09 (bug 3)
Vừa hoàn thành: xác minh Phiếu xuất hàng (product-exports/create.vue) đã có guard chưa-lưu hoạt động đúng — không bug (4/4 ca Playwright PASS).
Đang làm dở: không
Bước tiếp theo: không có (chờ user nếu còn màn khác cần rà).
Blocked:

## UI danh sách Phiếu xuất hàng (`finance/product-exports/index.vue`) — 7 yêu cầu
User rà màn danh sách, chốt 6/7 cần sửa (item 7 "tab tiêu đề = Phiếu xuất hàng" đã đúng sẵn qua
`document.title`). Peer erp-hrm-9b làm màn Tạo (`create.vue`) + Lịch sử (Phase 2), KHÔNG đụng
`index.vue` → làm song song, tôi nhận trọn danh sách + phần BE danh sách. Item 2 chốt: ô trống để HẲN TRỐNG.

- [x] **Item 1 — Sort:** bỏ `sortable` cột Trạng thái; thêm `sortable` cột Khách hàng + Phiếu xuất kho.
      BE `index()` đổi `allowedSort` → `$sortMap`: bỏ `status`, thêm `customer_name` (cột bảng chính) +
      `warehouse_export_code` (alias join → map `warehouse_exports.code` khi orderBy).
- [x] **Item 2 — Bỏ dấu `—`:** mọi cell template bỏ `|| '—'`, ô trống render rỗng (khuôn bill-incomes #11432).
- [x] **Item 3 — Mã phiếu thành link:** `cell-code` → `<nuxt-link class="v2-cell-link field-line">`
      vào `/finance/product-exports/{id}`; GỠ nút "Xem chi tiết" (eye) ở cột Thao tác + method `goDetail`.
- [x] **Item 4 — Cột Phiếu xuất kho:** bỏ icon `ri-external-link-line`, dùng class `v2-cell-link field-line`
      (navy + gạch chân đứt, giống Mã phiếu) — vẫn mở ERP qua `goErpWarehouseExport`.
- [x] **Item 5 — Đổi nhãn:** "Người lập"→"Người tạo", "Ngày lập"→"Ngày tạo" (cột bảng + filter + EXPORT_COLUMNS).
- [x] **Item 6 — Thêm cột Ngày cập nhật, Người cập nhật:** FE 2 cột + cell template; BE Resource
      thêm `updated_at` + `updater_name` (eager-load `employee_update.info.department` ở list + detail query);
      EXPORT_COLUMNS + FE export-excel.js thêm 2 field.
- [x] **Item 7 — Tab tiêu đề = "Phiếu xuất hàng":** đã đúng sẵn.
- [x] Verify Playwright (PXH-34590…): header đúng (Trạng thái hết sort, Khách hàng/Phiếu xuất kho có sort),
      Mã phiếu là link → điều hướng sang chi tiết, Phiếu xuất kho link không icon, ô trống rỗng hẳn,
      2 cột cập nhật có data; sort `warehouse_export_code` + `customer_name` đều **API 200** (alias join OK).

### Checkpoint — 2026-10-09 (UI danh sách product-exports)
Vừa hoàn thành: 6 item UI + BE danh sách (sort map, 2 cột cập nhật, nhãn Người/Ngày tạo), verify Playwright 7/7 PASS.
Đang làm dở: không
Bước tiếp theo: (tuỳ user) commit gop_db khi được yêu cầu. Lưu ý peer erp-hrm-9b làm create.vue song song — BE controller có sửa trên đĩa (ngoài vùng của tôi, lint sạch).
Blocked:

### File sửa (đợt UI danh sách)
- hrm-client/pages/finance/product-exports/index.vue
- hrm-client/pages/finance/product-exports/components/export-excel.js
- hrm-api/Modules/Assign/Http/Controllers/Api/V1/ProductExportController.php (index allowedSort, buildListQuery/detailForShow with(), EXPORT_COLUMNS)
- hrm-api/Modules/Assign/Transformers/ProductExportResource.php (updated_at + updater_name)

## Bộ lọc danh sách Phiếu xuất hàng (`finance/product-exports/index.vue`) — sửa bộ lọc (Redmine #5919)
User chốt: ẨN 3 bộ lọc + THÊM 9 bộ lọc + dấu "x" xóa nhanh ô text.
Khuôn vàng: màn chị em `finance/product-export-requests/index.vue` + BE `ProductExportRequestController` (đã
làm sẵn warehouse select, customer remote, created_by/approver employee select, product_name text).
Peer b3f31d làm `create.vue` + 2 modal picker Phase 3 — mình CHỈ đụng khối bộ lọc của `index.vue`, tránh `create.vue`.

**Dấu "x":** ĐÃ CÓ SẴN — `V2BaseFilterFieldControl.vue:54-66` render nút × cho mọi ô `type:'text'/'number'`
khi `hasValue` (Redmine #11170). Ô tìm nhanh cũng có (`V2BaseSmartFilterPanel.vue:88`). Nghĩa là mọi ô
text khai trong `filterFields` tự có × — chỉ cần verify live. KHÔNG tự dựng mới.

- [x] **Ẩn 3 bộ lọc:** Bộ phận (`part_id`) + Nhân viên (`employee_id`) → đặt `:disable_part="true"`
      `:disable_employee="true"` cho `V2BaseCompanyDepartmentFilter`, sửa `resetKeys` org + `inputCount` org=2
      (chỉ còn Công ty + Phòng ban). Gỡ field `product_export_request_code` (Mã YCXH) khỏi `filterFields`.
- [x] **Thêm 9 bộ lọc** (map data model đã xác minh):
      1. Tên/mã hàng hóa → `product_name` (text) → BE join `product_export_details`→`products` (code/name).
      2. Người tạo → `created_by` (select `employeeOptions` từ `$store.state.employeeOptions`).
      3. Người yêu cầu → `requester` (select employee) → BE: created_by của `product_export_requests` nguồn. ⚠️CHỜ xác nhận ERP.
      4. Người đề nghị → `proposer` (select employee) → BE: ⚠️nguồn CHƯA rõ (PER không có cột proposer). CHỜ ERP/user.
      5. Khách hàng → `customer_id` (V2BaseSelectRemote, slot `#field-customer_id`, fetchCustomers) → `product_exports.customer_id`.
      6. Phiếu xuất kho → `warehouse_export_code` (text) → BE `warehouse_exports.code like`.
      7. Mã phiếu → `code` (text) → BE đã có param `code`.
      8. Phòng ban yêu cầu → `request_department_id` (select department) → BE `product_export_requests.department_id`. ⚠️CHỜ ERP.
      9. Kho → `warehouse_id` (select `warehouseOptions`) → BE đã có param `warehouse_id`.
- [x] FE: thêm `employeeOptions` computed, `warehouseOptions`+`loadWarehouses()`, `fetchCustomers`+`customerInitialOption`,
      khai key mới trong `initialFilters`, slot `#field-customer_id`. `ignoredFields` đã computed qua `textFilterKeys` → ô text mới tự chờ Enter.
- [x] BE `ProductExportController::buildListQuery`: thêm xử lý `product_name`, `created_by`, `requester`,
      `proposer`, `customer_id`, `warehouse_export_code`, `request_department_id` (join PER); endpoint `warehouses` cho ô Kho.
- [x] Verify Playwright: 3 ô bị ẩn không còn; 9 ô mới lọc đúng (API 200, kết quả khớp); dấu × hiện khi ô text có chữ, bấm xóa sạch.

### Chốt mapping "Người yêu cầu / Người đề nghị" (user chốt — soi gương ERP y nguyên, KỂ CẢ nhãn ngược)
- **Người yêu cầu** (`requester`) = `product_export_requests.created_by` (người lập YCXH nguồn).
- **Người đề nghị** (`proposer`) = `warehouse_export_requests.created_by` (người lập ĐNXK) — qua `whereExists`.
- **Phòng ban yêu cầu** (`request_department_id`) = `product_export_requests.department_id`.
- ⚠️ Nhãn ERP đảo trực giác (yêu cầu↔đề nghị) nhưng giữ nguyên để khớp ERP 1-1 (user xác nhận "ok").
- Đa số phiếu (HĐ hãng, điều chuyển…) KHÔNG có PER/ĐNXK nên 3 ô này rỗng với phần lớn phiếu — ĐÚNG như ERP, không phải bug.

### Checkpoint — 2026-10-09 (bộ lọc #5919)
Vừa hoàn thành: ẩn 3 bộ lọc + thêm 9 bộ lọc + dấu × (có sẵn) — 7 edit FE + 1 BE; verify Playwright PASS
(14 ô lọc đúng thứ tự, 3 ô ẩn biến mất, `GET /assign/product-exports?product_name=máy&page=1&per_page=20 => [200]`
lọc đúng 34436→9454, × hiện ở ô text, popup "Cài đặt bộ lọc" đúng 14 dòng không còn field cũ). Test data đã revert (Làm mới).
Đang làm dở: không
Bước tiếp theo: (tuỳ user) commit gop_db khi được yêu cầu. CHƯA commit.
Blocked:

### File sửa (đợt bộ lọc #5919)
- hrm-client/pages/finance/product-exports/index.vue (disable_part/disable_employee, filterFields +9/-1, slot #field-customer_id, employeeOptions/departmentOptions/warehouseOptions/loadWarehouses/fetchCustomers/customerInitialOption)
- hrm-api/Modules/Assign/Http/Controllers/Api/V1/ProductExportController.php (buildListQuery: +7 handler, gỡ product_export_request_code)
