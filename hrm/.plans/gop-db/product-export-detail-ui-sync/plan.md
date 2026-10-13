# Plan — Đồng bộ UI màn Chi tiết Yêu cầu xuất hàng (Redmine feedback)

Nguồn: Redmine "[ERP => HRM] Yêu cầu xuất hàng - Xem chi tiết - Đồng bộ UI" (Nguyễn Minh Hằng →
Trần Cư). Phản ánh: màn `finance/product-export-requests/{id}` (Xem chi tiết YCXH) "thông tin hiển
thị chưa đồng bộ với các màn khác". Lấy `finance/bill-income-requests/2540` làm CHUẨN.

## Chẩn đoán — "đồng bộ" là về QUY ƯỚC UI, không phải thêm field

Màn chi tiết hiện tại (`_id/index.vue`) là 1 trang standalone tự dựng, vi phạm loạt quy ước dùng
chung mà các màn chi tiết khác (bill-income) đã theo:

| Vi phạm hiện tại | Chuẩn (bill-income) |
| --- | --- |
| Khối `.c-section` / `.section-header` tự chế | `V2BaseFormSection` |
| Ô rỗng in `—` | Để **TRỐNG HẲN** (`{{ x \|\| '' }}`) |
| `$bvModal.msgBoxConfirm()` (Hủy/Xóa) | `$confirm()` / `base-confirm-modal` |
| `.export-actionbar` cố định tự dựng | `V2Footer` (readonly) |
| `.text-muted` cho "Không có dòng hàng" (ĐỎ trong hrm-client) | xám `#6b7280` |
| Trang detail tách rời form Tạo/Sửa | Detail REUSE form với prop `readonly` (kiến trúc bill-income) |

## Hướng đã chốt (user chọn "Hướng A", phiên trước) — Full refactor

1. Thêm chế độ `readonly` vào `ProductExportRequestForm.vue` (hiện chỉ có create/edit).
2. Viết lại `_id/index.vue` thành wrapper mỏng reuse form ở chế độ readonly (mirror
   `bill-income-requests/_id/index.vue`).

### Quyết định data-flow (đã chốt)

- 2 endpoint dữ liệu KHÁC shape nhau:
  - **editData** (`${id}/edit-data`, chỉ bản nháp): `product_lines`/`selected_lines`, dùng cho
    chế độ SỬA (`applyInitialData`).
  - **show** (`assign/product-export-requests/${id}`): trả cờ quyền `is_can_edit/cancel/delete`,
    `code/status/status_name/status_color`, `type/type_name`, field HĐ, snapshot KH, field B (xuất
    thẳng/lắp đặt/vận chuyển/km), `files`, và mảng **products PHẲNG** cho MỌI loại. **KHÔNG** trả
    `warehouse_id/import_warehouse_id/expected_borrow_date/return_date/customer_id`.
- Vì `show` khác shape editData (products phẳng, thiếu các id) → KHÔNG reuse được input Tạo/Sửa như
  bill-income. → Chế độ readonly dùng **nhánh `v-else` riêng** tiêu thụ đúng field của `show`.
- Body Tạo/Sửa hiện tại bọc trong `v-if="!readonly"` (gần như KHÔNG đụng → gần zero regression).
- Form TỰ fetch `show` khi `readonly && requestId` trong `mounted` (map vào view-model readonly +
  `detailFlags`, emit `loaded`).
- KHÔNG đổi BE.

## Task

### FE — `ProductExportRequestForm.vue`
- [x] Thêm props `readonly` (Boolean, default false) + `requestId` ([String, Number], null).
- [x] Thêm data: `detailFlags` (is_can_edit/is_can_cancel/is_can_delete), `detail` (view-model từ
      show), `detailProducts` (mảng phẳng), `detailFiles`.
- [x] Bọc toàn bộ body Tạo/Sửa hiện tại trong `<template v-if="!readonly">` (general-info section +
      product-detail section + 3 modal).
- [x] Thêm nhánh `<template v-else>` readonly: V2BaseFormSection "Thông tin chung" (mã, loại, HĐ
      link, KH, phòng ban, người lập/duyệt, ngày tạo/nhận/duyệt) + block KH&xuất bán (loại 20/21) +
      Ghi chú + File đính kèm + bảng hàng hoá phẳng (cột giá cho loại 21) + pay-box (loại 21). Ô
      rỗng để trống; badge trạng thái không cần (đã ở page title). Dùng lại style `.er-table`/
      `.pay-box` sẵn có trong form.
- [x] Thêm `<slot name="after-content">` ĐẶT TRƯỚC footer readonly (V2Footer position:fixed).
- [x] `<V2Footer v-if="readonly">` với `#custom-actions`: Sửa (is_can_edit) / Lập đề nghị xuất kho
      (status===2 && perm 'Kế toán kho') / Hủy (is_can_cancel, danger) / Xóa (is_can_delete, danger)
      — dùng `$confirm()` cho Hủy/Xóa. `url-back="/finance/product-export-requests"`.
- [x] `mounted`: nếu `readonly && requestId` → fetch show, map view-model + detailFlags, emit
      `loaded`; KHÔNG chạy applyInitialData/fetchTypeOptions nặng nếu không cần (vẫn cần type/company
      cho computed? — readonly dùng field từ show, không cần options → chỉ fetch show).
- [x] Guard `snapshotSource()` → `if (this.readonly) return null` (khỏi dirty-tracking).
- [x] Guard `onSubmitClick`/submit handlers → `if (this.readonly) return`.
- [x] Thêm computed/method readonly: isSaleDetail(type===21), rowPrice/rowAmount/paymentSummary/
      nonSaleTotals tính trên `detailProducts` (port từ index.vue cũ), canCreateWarehouseRequest.

### FE — `_id/index.vue` (viết lại thành wrapper mỏng)
- [x] `<ProductExportRequestForm :request-id="requestId" mode="edit" readonly @loaded="onLoaded">`
      + `#after-content` = `<SystemInfoSection entity-type="product_export_requests"
      :entity-id="requestId" endpoint-base="catalog-histories">`.
- [x] Script: name 'ProductExportRequestShow', layout 'default-sidebar', mixins [PageTitleMixin],
      computed pageTitle (buildStatusTitle) + requestId; method onLoaded lưu code+status cho title.

### Verify
- [x] Playwright 127.0.0.1:3000: mở chi tiết 1 YCXH (bản ghi 40337, loại 14 "Xuất bán hàng",
      status 2), đối chiếu với bill-income-requests/2540; test lại create/edit không regression.
- [x] File giữ LF (cả 2 file hiện LF). CHƯA commit/push (chờ user).

## Checkpoint
### Checkpoint — bắt đầu (2026-09-18)
Vừa hoàn thành: tạo plan.md, đọc lại index.vue cũ + form script head, xác nhận nhánh gop_db + LF.
Đang làm: thêm readonly vào ProductExportRequestForm.vue.
Bước tiếp theo: sửa form → wrapper → verify Playwright.
Blocked: không

### Checkpoint — XONG code + verify Playwright (2026-09-18)
Vừa hoàn thành: cả 2 file FE (form readonly + wrapper mỏng) code xong, verify thật trên trình duyệt.
- `ProductExportRequestForm.vue`: nhánh `v-else` readonly + props `readonly`/`requestId` + guard
  snapshotSource/onSubmitClick + V2Footer readonly + fetch `show` trong mounted. Body Tạo/Sửa bọc
  `v-if="!readonly"`. Cân bằng thẻ template 32/32, không sót em-dash trong nhánh readonly.
- `_id/index.vue`: wrapper mỏng reuse form `readonly` + `#after-content` = SystemInfoSection.
- **Verify readonly (bản ghi 40337, loại 14 "Xuất bán hàng", status 2 Chờ duyệt):**
  section "Thông tin chung" + "Danh sách hàng hoá"; 10 cặp kv đúng, ô rỗng (Người duyệt / Thời gian
  duyệt) để TRỐNG HẲN; bảng hàng hoá phẳng 9 cột (STT/Mã/Tên/Thương hiệu/Model/ĐVT/SL/Đơn giá/Thành
  tiền) 2 dòng + dòng "Tổng cộng" (SL 1, 700,000); footer "Xem lịch sử" (SystemInfoSection) +
  "Quay lại" (V2Footer). KH block (loại 20/21) + pay-box (loại 21) đúng KHÔNG hiện; nút quyền
  (Sửa/Hủy/Xóa/Lập đề nghị xuất kho) đúng KHÔNG hiện (DNS Admin không phải người tạo, phiếu không
  phải nháp). Đã chụp screenshot `product-export-request-40337-detail.png`.
- **Đối chiếu chuẩn bill-income-requests/2540 (TPV.DNTT0826.00024):** cùng khuôn — V2BaseFormSection
  cards + mục Lịch sử nhúng + V2Footer "Quay lại". Parity đạt (bill-income thêm "In phiếu" vì có màn
  in; YCXH không thuộc scope task này). Console error là môi trường (SCSS build warn "flex-end mixed
  support" ở nhiều component + Vue dev-mode; xuất hiện cả trên màn chuẩn CHƯA sửa) — không do refactor.
- **Regression create/edit:** mở `/create` render sạch, không lỗi Nuxt; đúng nhánh không-readonly
  (section "Thông tin chung"/"File đính kèm"/"Chi tiết hàng hoá" + footer "Lưu nháp / Lưu và gửi
  duyệt / Lưu và tiếp tục / Quay lại"). `v-if="!readonly"` không phá create/edit (edit dùng chung
  đúng nhánh này).
- **Giới hạn kiểm thử:** DB erp_new KHÔNG có bản ghi loại 20/21 → bảng giá bán (17 cột) + pay-box
  của loại 21 và block KH của loại 20/21 chưa test được với data thật; logic port nguyên từ
  index.vue cũ (đã đối chiếu `git show HEAD` khớp) nên hành vi không đổi so với màn gốc.
- **Mutation test-only đã REVERT:** đã xoá dòng cấp quyền tạm `role_has_permissions (100870,18,1)`
  (đếm 1→0). DB sạch như trước.
- File cả 2 vẫn LF (0 CR). CHƯA commit/push — chờ user yêu cầu.
Bước tiếp theo: chờ user chốt commit lên nhánh gop_db.
Blocked: không

---

## Phase 2 — Đồng bộ thêm field nghiệp vụ màn chi tiết cho loại KHÁC 20/21 (2026-10-06)

Bối cảnh: user gửi 2 screenshot (ERP PYCXH-40340 vs HRM PYCXH-35634, đều loại 99 "Xuất khác").
Màn chi tiết HRM hiện chỉ hiện khối Xuất thẳng/Cần lắp đặt/Vận chuyển/Số km trong section
"Khách hàng & xuất bán" GATE theo `detailIsContract` (loại 20/21) → loại 99 không thấy gì.
ERP show.blade hiện các field này cho mọi loại phù hợp (theo ng-if từng field).

Nguyên tắc (skill erp-to-hrm-screen): THÊM field nghiệp vụ ERP có mà HRM thiếu, cho đúng loại;
GIỮ look HRM + field thừa của HRM. "Ghi nhận chi phí HĐ" (type 99, contract_costable) BỎ QUA:
mọi bản ghi type-99 trong erp_hrm_check đều `contract_costable_id=null` → luôn trống, HRM không
có luồng gắn costable. Nếu sau này có data thì bổ sung sau.

### BE — `ProductExportRequestController::show()`
- [x] Thêm `avatar` vào select dòng hàng (`product_export_request_details`).
- [x] Thêm `warehouse_name` = `code - name` tra từ `warehouses` theo `warehouse_id` (null nếu không có).
- [x] Thêm `has_delivery` = `in_array((int)$req->type, ProductExportRequest::getHasDeliveryTypes(), true)`.
- [x] Thêm `need_install` = (int) $req->need_install.
- [x] Thêm `need_warehouse` = `(int)$req->type !== 7 && !(int)$req->is_export_direct` (parity ERP getter).

### FE — `ProductExportRequestForm.vue` nhánh readonly
- [x] Section "Thông tin chung" (hoặc section mới "Thông tin xuất kho") hiện cho loại KHÁC 20/21:
      Xuất thẳng, Kho xuất (khi need_warehouse), Vận chuyển (khi has_delivery), Số km dự kiến
      (khi has_delivery && transition_type==2), Cần lắp đặt (need_install, khi type!=18 && type!=19).
      Giữ nguyên section "Khách hàng & xuất bán" cho 20/21.
- [x] Thêm cột "Hình ảnh tham khảo" (avatar) vào bảng hàng hoá readonly (cả 2 biến thể header + row).

### Verify
- [x] Playwright 127.0.0.1:3000: mở PYCXH loại 99 (vd 35634; 35532 có transition_type=2 + km=7 để
      test Số km). Đối chiếu ERP PYCXH-40340.
- [x] LF. CHƯA commit/push.

## Checkpoint
### Checkpoint — Phase 2 XONG + verify Playwright (2026-10-06)
Vừa hoàn thành: đồng bộ thêm field nghiệp vụ màn chi tiết YCXH cho loại KHÁC 20/21 (focus loại 99).
- BE `ProductExportRequestController::show()`: thêm `avatar` vào select dòng hàng; thêm
  `warehouse_name` (= `code - name` tra `warehouses` theo warehouse_id), `has_delivery`
  (getHasDeliveryTypes), `need_install` (int), `need_warehouse` (type!=7 && !is_export_direct).
- FE `ProductExportRequestForm.vue` nhánh readonly: thêm section "Thông tin xuất kho"
  (v-if !detailIsContract) gồm Xuất thẳng / Kho xuất (need_warehouse) / Vận chuyển (has_delivery) /
  Số km dự kiến (has_delivery && transition_type==2) / Cần lắp đặt (need_install, type!=18&&!=19);
  thêm cột "Hình ảnh tham khảo" (avatar, img) vào bảng hàng hoá — cả 2 biến thể header + row,
  chỉnh colspan Tổng cộng 6→7 và empty-row 17/9→18/10; thêm css .er-ref-img.
- "Ghi nhận chi phí HĐ" (contract_costable loại 99) BỎ QUA: mọi bản ghi type-99 có costable=null.
- Verify Playwright 127.0.0.1:3000:
  * PYCXH-35532 (tt=2, km=7, warehouse_id=2): section đủ 5 field (Xuất thẳng Không / Kho xuất
    LN - Liên Ninh / Vận chuyển Công ty vận chuyển / Số km 7 / Cần lắp đặt Không); ảnh tham khảo
    render đúng trong bảng; Tổng cộng căn cột đúng.
  * PYCXH-35634 (tt=1): "Số km dự kiến" ẩn đúng (chỉ còn 4 field), Kho xuất SG - Kho Sài Gòn,
    Vận chuyển Nhân viên vận chuyển.
- Section 20/21 "Khách hàng & xuất bán" GIỮ NGUYÊN (gate !detailIsContract không đụng). LF sạch,
  PHP lint OK. CHƯA commit/push — chờ user.
Bước tiếp theo: chờ user chốt commit lên nhánh gop_db.
Blocked: không
