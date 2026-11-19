# Plan — Đồng bộ màn CHI TIẾT YCXH với Tạo/Sửa (read-only)

Nguồn: user — "đồng bộ lại màn chi tiết yêu cầu xuất hàng form thông tin chung với màn tạo và sửa",
"giống cả style và box chi tiết hàng hoá nhưng chỉ read-only". Hướng B. Duyệt short design 14/10.

## Tasks

### BE (hrm-api) — enrich `show()`
- [x] Task 1: `$products` select thêm `firm_contract_tab_product_id`.
- [x] Task 2: Thêm field per-type vào `$resource`:
      - Loại 3: `expected_borrow_date` / `return_date` (dd/mm/yyyy).
      - Loại 6: `import_warehouse_name` (code - name).
      - Loại 14: `firm_contract_id` / `firm_contract_code` / `firm_tab_vat_percent` / `customer_unit` /
        `delivery_place` (reuse `firmContractDisplaySnapshot`).
- [x] Task 3: Loại 14 — build `product_groups` gom `$products` theo nhóm hàng hóa
      (details.firm_contract_tab_product_id → firm_contract_tab_products → firm_contract_tabs.name).
      Helper riêng `buildShowProductGroups()` (nhóm không khớp → tab_id 0 'Hàng hóa', đẩy cuối).
- [x] Task 4: `php -l` — không lỗi cú pháp. KHÔNG đụng editData/helper dùng chung.

### FE (hrm-client) — nhánh readonly `ProductExportRequestForm.vue`
- [x] Task 5: "Thông tin chung" — thêm `.fld` vào các col; đổi nhãn khớp create/sửa ("Loại phiếu"→"Loại yêu cầu");
      ô Hợp đồng nhãn động `detailContractLabel` + `detailShowContractField` (giữ nuxt-link HĐ HRM).
- [x] Task 6: Bổ sung field per-type read-only (gate check loại tường minh):
      loại 14 Nhóm VAT (`detailFirmVatText`) + Chọn nhóm hàng hóa (`detailFirmTabNamesText`) + Tên viết tắt +
      Địa chỉ giao hàng (trong ro-panel); loại 7 Gửi đến công ty + Chọn kiểu nhập kho + Phiếu yêu cầu chuyển hàng
      (chips `detailTransferRequests`, không nút xóa); loại 3 Ngày cần mượn / Ngày trả; loại 6 Kho nhập.
- [x] Task 7: "Danh sách hàng hoá" → đổi title "Chi tiết hàng hoá"; `detailIsSale` gồm [21, 14];
      thêm computed `detailProductGroups` + `detailIsFirmTabs`.
- [x] Task 8: Dựng nhánh bảng theo loại: loại 14 b-tabs theo `product_groups` (bảng sale + pay-box tổng),
      loại 21 bảng phẳng sale, loại 20/7/manual bảng phẳng non-sale (Tổng cộng). BỎ cột-sống + công cụ nhập.
- [x] Task 9: Kiểm FE thô: grep `<input`/`<select`/`<button` thô ngoài V2Base nhánh readonly (691-1140) = RỖNG.

### Verify
- [x] Task 10: Playwright — đã mở & đối chiếu 6 phiếu:
      - **14** (39254): b-tabs "Nhóm 1" + bảng 18 cột sale + pay-box tổng; panel khách hàng có Tên viết tắt + Địa chỉ giao hàng; Nhóm VAT 8%, Chọn nhóm hàng hóa "Nhóm 1". ✓
      - **21** (35676): bảng phẳng sale 18 cột + pay-box, không tabs. ✓
      - **20** (35675): bảng phẳng non-sale 10 cột + dòng Tổng cộng, không pay-box. ✓
      - **7** (35665): Gửi đến công ty + Chọn kiểu nhập kho "Nhập về kho" + chip "PYCCH-07358" (không nút xóa) + bảng non-sale. ✓
      - **3** (35685): Ngày cần mượn 24/08/2026 + Ngày trả dự kiến 28/08/2026 (dd/mm/yyyy). ✓
      - **6** (35607): Kho nhập "SG - Kho Sài Gòn"; `rawEditableInTable=0` → đã bỏ cột-sống + công cụ nhập. ✓
      - Không lỗi JS thật (chỉ favicon/websocket).

### Chỉnh theo phản hồi user (14/10)
- [x] Task 11: "Cần lắp đặt" đổi từ `V2BaseInput` 'Có'/'Không' sang `V2BaseRadio :options="needRepairOptions" disabled`
      (mirror create/sửa). Verify: 2 radio Có/Không, disabled, đúng giá trị.
- [x] Task 12: Bỏ 3 ô metadata "Người duyệt" / "Thời gian nhận" / "Thời gian duyệt" khỏi "Thông tin chung"
      (chỉ giữ "Phòng ban"). Verify: 3 nhãn không còn, loại 14 & 21.
- [x] Task 13: Chi tiết loại 14 thêm tab "Hàng hóa (*)" chung ở ĐẦU (mirror `firmRenderTabs`):
      computed `detailFirmRenderTabs` prepend tab chung + các tab nhóm (tập con).
- [x] Task 13b (sửa ngữ nghĩa — user: "tab hàng hoá chẳng có dữ liệu"): đối chiếu màn Sửa 39254 thấy
      `firmCommonLines` = gộp TOÀN BỘ dòng mọi nhóm (tab chung = full list), nhóm là tập con. FIX `detailFirmRenderTabs`
      cho tab chung `lines = detailProducts` (toàn bộ), guard đổi sang `!detailProducts.length`.
      Verify (39254): tab "Hàng hóa (*)" 2 dòng + "Nhóm 1" 2 dòng — khớp màn Sửa.

### Fix 2 bug màn CHI TIẾT (14/10 — user kèm 2 screenshot, màn tham khảo customer-care/services)
- [x] Task 14 (BUG 1 — Dung lượng tệp trống): `attachmentSizes()` cũ đọc cột `files.file_size` nhưng
      URL đính kèm lưu qua `attachment_urls[]` để `file_size = null` (FE không gửi size) → cột trống.
      FIX đổi `ProductExportRequestController::attachmentSizes($id, BillPaymentAttachmentService $attachments)`:
      lấy `$urls = $req->files()->pluck('file_path')->all()` → `$attachments->sizes($urls)` (HTTP HEAD S3
      song song `Http::pool`, khuôn customer-care / bill-payment). Thêm
      `use Modules\Finance\Services\BillPaymentAttachmentService;`. Lấy kích thước THẬT live, fix luôn phiếu cũ.
      `php -l` OK. Verify: endpoint 39254 trả `{...:244114, ...:161279}`, cột Dung lượng hiện "238.4 KB" / "157.5 KB".
- [x] Task 15 (BUG 2 — tên tệp trong lịch sử không bấm tải được): `attachmentRows()` cũ set
      `__name = fileName` (tên trần) + field 'Tệp' → SiValue không thấy URL để linkify → in chữ thường.
      FIX đổi theo khuôn `ServiceService::attachmentRowsForLog()`: `__name = $url` (URL đầy đủ) + `__brief => true`,
      bỏ field 'Tệp'; dùng hằng `CatalogHistoryService::ROW_KEY/ROW_NAME/ROW_BRIEF`. Thêm
      `use App\Services\CatalogHistoryService;`. `php -l` OK. Verify: log mới sinh qua `logAttachmentChanged`
      lưu `new_value` chứa `__name = URL`; FE render 2 `<a class="si-file-link">`, click mở modal xem trước ảnh S3.
      LƯU Ý: chỉ log MỚI clickable — log cũ ghi trước fix là snapshot bất biến, giữ nguyên (không backfill audit).
- [x] Task 16: `php -l` 2 file BE (Controller + Service) — không lỗi cú pháp. Xác nhận hằng CatalogHistoryService
      ROW_KEY=__key (giữ nguyên) / ROW_NAME=__name / ROW_BRIEF=__brief.

### Nút "Không duyệt" màn chi tiết (14/10 — user: "erp có nút Không duyệt còn hrm k có … triển khai cho khớp erp")
Khảo sát ERP: nút "Không duyệt" (show.blade.php) hiện khi `canDeny()` = `canApprove()` (luồng thường)
|| `canProductExport()` (xuất thẳng) — **áp cho MỌI loại**, chỉ cần status "Chờ duyệt" (2) + quyền
"Kế toán kho" + cùng công ty (loại 7 theo công ty xuất). ERP `deny()` set status→Đang tạo, lưu lý do
vào cột `comment`, phiếu con `parent_request_id`→Đã hủy, gửi notification. HRM: lý do KHÔNG bắt buộc
(user chốt), KHÔNG notification (HRM chưa có). Chữ nút: skill button-convention dòng 161 chuẩn hoá về
"Từ chối" nhưng **user chốt giữ "Không duyệt"** (bám ERP) — đã confirm 14/10.
- [x] Task 17 (BE Entity): thêm `canReject()` vào `ProductExportRequest` — status==CHO_DUYET(2) +
      `isCurrentEmployeeHasPermission('Kế toán kho')` + khớp công ty (loại 7 → `export_company_id`,
      khác → `company_id`). Mirror ERP canDeny (= canApprove||canProductExport, mọi loại). `php -l` OK.
- [x] Task 18 (BE Controller + route): `ProductExportRequestController::reject($id, $service)` — gate
      `canReject()` → 403; `reason` nullable (trim); status 2→3; lưu `comment`=lý do (khớp ERP); phiếu con
      `parent_request_id`→STATUS_DA_HUY_PHIEU(6); `logStatusChanged($req,$statusBefore,$reason ?: null)`;
      KHÔNG notification. Route `POST /assign/product-export-requests/{id}/reject`. `php -l` OK.
- [x] Task 19 (FE): computed `detailCanReject` = `detailCanCreateWarehouseRequest || detailCanCreateProductExport`
      (status 2 + Kế toán kho, mọi loại). Nút "Không duyệt" (`primary status="danger"`, icon
      `ri-close-circle-line`) trong `#custom-actions` ĐẶT TRƯỚC nút Hủy, `v-if="detailCanReject"`.
      Method `rejectRequestRO()` mirror `cancelRequestRO`: `$confirm` showInput textarea không bắt buộc,
      POST `.../reject` payload `{reason}`, success → toast + `$router.push('/finance/product-export-requests')`.
- [x] Task 20 (Verify Playwright, bản ghi 39303 type 3 status 2): nút hiện (cùng "Lập đề nghị xuất kho",
      không có Hủy/Xóa/Sửa vì status≠3 — khớp danh sách) → popup "Lý do không duyệt" không bắt buộc →
      confirm → DB status 2→3 ✓, `comment`="Sai thông tin kho xuất, cần lập lại" ✓,
      `catalog_histories` dòng `change_status` "Chờ duyệt"→"Đang tạo" + note ✓, về màn danh sách ✓.
      Đã khôi phục bản ghi 39303 về status=2/comment=NULL + xoá dòng history test. Không lỗi JS mới.

### Fix màn TẠO/SỬA YCXH nhập tay (14/10 — user kèm screenshot: "validate text phải màu đỏ chứ. và màn sửa cũng phải lấy tồn ra như màn tạo")
File: `pages/finance/product-export-requests/components/ManualLinesTable.vue` (bảng dòng hàng nhập tay,
dùng chung create/edit/detail qua `ProductExportRequestForm.vue`).
- [x] Task 21 (text validate SL không đỏ): `.fld-err` CHỈ khai ở form cha trong `<style scoped>` →
      không chạm `<div class="fld-err">` nằm trong component con này → text "Số lượng phải lớn hơn 0." /
      "Bắt buộc phải nhập" ra màu mặc định (đen). FIX khai `.fld-err { color:#dc2626; font-size:12px }`
      ngay trong `<style scoped>` của `ManualLinesTable.vue` (khớp màu đỏ validate chuẩn #dc2626).
- [x] Task 22 (cột Tồn trống ở màn SỬA): watcher `stockKey` KHÔNG `immediate`. Màn Tạo: child mount khi
      dòng còn rỗng → thêm dòng → stockKey đổi → watcher chạy → `loadStocks()`. Màn Sửa: `isManualType`
      bật sau khi nạp `form.type`, lúc child mount thì `warehouse_id` + dòng ĐÃ set → stockKey đã mang
      giá trị cuối ngay lúc mount → watcher non-immediate không chạy → `stocks={}` → cột Tồn "—".
      (Watcher anh em `unitsKey` vốn `immediate: true` nên ĐVT edit vẫn ra.) FIX đổi `stockKey` sang
      `{ immediate: true, handler() {...} }` (mirror `unitsKey`).
- [x] Task 23 (Verify Playwright, bản ghi 39303 type 3 status 3 — editable bởi user 13):
      màn SỬA → `stock-of-products` fire (immediate watcher) trả `{"48464-40":{available_export_qty:5}}`
      → cột **Tồn = 5** (trước fix: "—") ✓; đặt qty=0 → text lỗi "Số lượng phải lớn hơn 0." render
      `rgb(220,38,38)` = #dc2626, 12px, viền ô đỏ ✓ (screenshot xác nhận). Console sạch (chỉ dev-mode
      noise: menu-settings 400, favicon, reexport warning — không liên quan). Đã xoá 3 png +
      `.playwright-mcp` ở root workspace; giữ nguyên `HRM/hrm-client/.playwright-mcp` (tracked).

## Ghi chú
- DB local `erp_hrm_check`; API :8000, client :3000 chạy sẵn.
- Nút "Không duyệt" chạm 3 file: `ProductExportRequest.php` (entity) + `ProductExportRequestController.php` +
  `Routes/api.php` (BE) và `ProductExportRequestForm.vue` (FE). CHƯA commit.
- KHÔNG commit/push khi chưa được yêu cầu.
- Fix 2 bug chạm 2 file BE: `ProductExportRequestController.php` + `ProductExportRequestService.php` (CHƯA commit).
- Log lịch sử là snapshot ghi tại thời điểm thay đổi → fix BUG 2 chỉ áp cho log phát sinh SAU fix;
  muốn các log cũ cũng bấm được phải backfill `catalog_histories.new_value` (ghi đè audit) — CHỜ user quyết.
- Fix Task 21-22 chạm 1 file FE: `ManualLinesTable.vue` (CHƯA commit) — chỉ FE, không đụng BE.
