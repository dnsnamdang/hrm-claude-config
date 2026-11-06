# Plan — Cụm ③ Fix bug Hạch toán DV HĐBH/HDDV

Xem `design.md`. Làm từng ticket, verify Playwright trước khi báo xong. KHÔNG commit khi chưa được yêu cầu.

## #12030 — YC HDDV Danh sách

### bug① — quick-search chỉ số phiếu + số HĐ (BE)
- [x] `WrAccountingServiceRequest::applyFilters` — bỏ dòng `->orWhere('customer_name', 'like', $keyword)`.
- [x] Cập nhật comment "Ô tìm nhanh: mã phiếu / số hợp đồng" (bỏ "tên khách hàng").

### bug② — link cột Số hợp đồng → tab mới (FE)
- [x] `index.vue` template `#cell-contractCode`: khi có `item.wr_service_contract_id` → render
      `<a class="v2-cell-link field-line" :href="'/customer-care/wr-service-contracts/' + id" target="_blank" rel="noopener">`; không có id → `<div class="field-line ...">` chữ thường.
- [x] Xoá comment cũ "màn HĐ dịch vụ CHƯA PORT".

### bug③ — sort Tổng thanh toán
- [x] BỎ QUA (user chốt). Ghi chú hỏi lại reviewer: ERP gốc không có cột này.

### Kiểm thử
- [x] Playwright `http://127.0.0.1:3000/finance/wr-accounting-service-requests`: quick-search gửi
      `keyword`, BE không còn match tên KH; cột Số HĐ là link `target=_blank` sang chi tiết HĐ DV.
      - bug① (API, token DNS Admin, `type=all`): keyword "TRỌNG THIỆN" (tên KH) → 0 kết quả ✓;
        "YCHTDV.2025000001" (số phiếu) → 1 ✓; "THACOTRONGTHIEN" (số HĐ) → 1 (id=21) ✓.
      - bug② (DOM, inject `type=all` để bảng có data): 3/3 dòng cột Số HĐ là
        `<a href="/customer-care/wr-service-contracts/{id}" target="_blank" rel="noopener" class="v2-cell-link field-line">` ✓.
- [x] grep self-check element thô = rỗng (chỉ `<a>` link, không phải element form).

## #12003 — YC HĐBH Danh sách

### bug1 — hyperlink Số hợp đồng + giãn ô/xuống dòng
- [x] BE `ServiceAccountingRequestListResource`: thêm `'contract_type' => $item->contractable_type`.
- [x] FE `index.vue`: import `contractLink` từ `@/utils/contract-link`; cột `#cell-contractCode` dùng
      `contractLink(item.contract_type, item.contract_id)` → `href` (ERP tab mới) / `to` (nuxt-link) / chữ thường.
- [x] Cột `contractCode`: `cellClass: 'text-wrap'` + `minWidth: 240px` cho xuống dòng; bỏ comment cũ "CHƯA PORT".

### bug2 — action Hạch toán dịch vụ
- [x] ĐÃ có sẵn (`getRowActions` key `accounting`, gate `is_can_accounting`, đích `/finance/service-accounting/create`). Chỉ verify.
- [x] 06/11: verify local bằng DNS Admin (id 13): có Hạch toán dịch vụ + Không duyệt, bấm mở `/finance/service-accounting/create?service_accounting_request_id=3612`.
- [ ] Dev: kiểm tra role Super admin (18) đã được gán `Hạch toán yêu cầu làm dịch vụ` (+ `Hạch toán dịch vụ HĐBH`) chưa — seeder không gán.

### bug3 — lọc Mã / Người duyệt / Người yêu cầu
- [x] `initialStateForm`: thêm `created_by`, `approver_id` (giữ `requester_id`).
- [x] `filterFields`: ô hiện tại key `requester_id` nhãn "Người tạo" → đổi key `created_by` (giữ nhãn "Người tạo").
- [x] `filterFields`: THÊM ô `approver_id` nhãn "Người duyệt" + ô `requester_id` nhãn "Người yêu cầu" (select employeeOptions).
- [x] "Mã" = bug4 (filter `code` đổi nhãn "Mã phiếu").

### bug4 — đổi "Số phiếu" → "Mã phiếu"
- [x] Cột `code` label/title → "Mã phiếu".
- [x] Filter `code` label → "Mã phiếu".
- [x] Quick-search placeholder → "Tìm theo mã phiếu, số hợp đồng, khách hàng".
- [x] Export field `code` name → "Mã phiếu".

### Kiểm thử
- [x] Playwright: cột Số HĐ là link ERP `target=_blank` + xuống dòng khi dài (`white-space:normal`, href
      `…/admin/sale/firm-contracts/{id}`); panel lọc có Người tạo/Người yêu cầu/Người duyệt + Mã phiếu;
      action Hạch toán dịch vụ hiện với phiếu Chờ duyệt, ẩn với Đã hạch toán.
- [x] grep self-check element thô = rỗng.
## #12024 — Phiếu HĐBH Danh sách

Màn: `hrm-client/pages/finance/service-accounting/index.vue` + `components/ServiceAccountingEditForm.vue`.
BE: `ServiceAccounting` + `ServiceAccountingService` + `ServiceAccountingListResource` + `CatalogHistoryService`.
**Quyết định chốt: bug1 = hướng A (port ERP standalone "Tạo mới" + popup chọn YC).** Xem design.md QĐ-24.*.

### bug2 — "Người lập" → "Người tạo" (FE text, nhẹ nhất)
- [x] `index.vue` cột `creatorName` label+title → "Người tạo".
- [x] filterFields `created_by` label → "Người tạo".
- [x] exportFields `creator_name` name → "Người tạo"; `created_at` name "Ngày lập" → "Ngày tạo".

### bug3 — link Số hợp đồng (BE + FE, giống #12003)
- [x] BE `ServiceAccountingListResource`: thêm `'contract_type' => $item->contractable_type`; bỏ comment "CHƯA PORT".
- [x] FE `index.vue`: import `contractLink`; `#cell-contractCode` dùng `contractLink(item.contract_type, item.contract_id)` → href tab mới / to / chữ trơn.
- [x] Cột `contractCode`: `cellClass: 'text-wrap'` + nới `minWidth: 240px`.

### bug4 — Lịch sử lỗi + không hiển thị trạng thái (BE)
- [x] `CatalogHistoryService::TABLES`: đăng ký `service_accounting` (label + columns contract_code/customer_name/type/payed_cost/note/status/details_rows).
- [x] `ServiceAccountingService` `use LogsCatalogHistory`: catalogTable/catalogColumns/catalogDisplay/snapshotOf.
- [x] store → logCreate; update → chụp before+statusBefore trước fill, logUpdate + logStatus; destroy → logDelete; approveAndPost → logStatus draft→approved.

### bug1 — Tạo mới + popup chọn YC (BE nhẹ + FE nặng nhất)
- [x] BE entity `ServiceAccounting`: const `PERMISSION_ACCOUNTING` + `canCreate()`.
- [x] BE `ServiceAccountingService::meta()`: thêm `'can_create' => ServiceAccounting::canCreate()`.
- [x] FE `index.vue`: scopeMeta thêm `can_create`; loadData gán; toolbar thêm nút "Tạo mới" v-if `scopeMeta.can_create` → `$router.push('/finance/service-accounting/create')`.
- [x] FE tạo `components/AccountingRequestPickerModal.vue` (copy RequestSearchModal): nguồn `finance/service-accounting-requests?status=2`, cột code/contract_code/customer_label/created_at, emit select.
- [x] FE `ServiceAccountingEditForm.vue`: bỏ redirect 404 khi thiếu srcRequestId → mở picker; chọn YC xong set srcRequestId + loadYc.

### Kiểm thử
- [x] Playwright `http://127.0.0.1:3000/finance/service-accounting`: nút Tạo mới hiện (admin); popup chọn YC Chờ duyệt (17 YC) → nạp form prefill; cột Số HĐ link ERP :8001 tab mới; nhãn "Người tạo"; Lịch sử mở SẠCH (không còn "Lịch sử lỗi") → phiếu cũ hiện "Chưa có lịch sử thao tác nào." (các phiếu cũ sinh trước khi gắn trait nên chưa có dòng).
  - ⚠️ CHƯA kiểm "hiện dòng tạo/đổi trạng thái" trên phiếu THẬT: cần tạo 1 phiếu mới, mà việc đó đẩy YC nguồn sang "Đã hạch toán" (mutate data). Để lại; logic logCreate/logStatus đã review ở code.
- [x] grep self-check element thô: chỉ còn `<button class="close">` (nút X header popup — pattern chuẩn ~10 picker đang dùng), không phải vi phạm V2Base.

## #12010 — YC HĐBH Chi tiết (ĐÃ XONG)

Màn `service-accounting-requests/_id` (component `ServiceAccountingRequestDetail.vue`). Đồng bộ dạng với các màn khác theo quyết định QĐ-10.*.

- [x] BE `ServiceAccountingRequestService::detailData()`: bổ sung khối KH đầy đủ lấy từ snapshot HĐ (`contract_type`, `contract_id`, `contract_code`, `customer_code/name/short_name/type`, `identity_card_number`, `customer_address/mobile/contact_name/contact_phone`) + `files` (TableFileHelper). PHP lint OK.
- [x] FE: bỏ `V2BaseBadge` "Chờ duyệt" ở header (QĐ-10.3, chỉ còn CreatorInfoLine); Số hợp đồng → ô link `contractLink()` (FirmContract mở ERP :8001); thêm đủ trường KH + block Người liên hệ/ĐT liên hệ khi `customer_type > 1`; tổng chi phí dời vào `<tfoot>` cùng bảng (QĐ-10.4); thêm `FileAttachmentTable` khi có file.
- [x] Playwright `127.0.0.1:3000/finance/service-accounting-requests/3606`: mọi trường đúng, không còn badge, link ERP mở đúng, tfoot tổng hiển thị.

## #12026 — Phiếu HĐBH Chi tiết (ĐÃ XONG)

Màn `service-accounting/_id` (component `ServiceAccountingForm.vue` + `CostTable.vue`). Theo QĐ-26.1 (giống #12010) + QĐ-26.2 (1 trang, không tab).

- [x] BE `ServiceAccountingService::detailData()`: thêm `contract_type`; FIX bug "chưa lấy được địa chỉ" — đọc `optional($contract)->customer_address` (snapshot HĐ) thay cho `optional($customer)->address_text` (thường rỗng); tương tự `customer_mobile` theo HĐ; bổ sung `customer_short_name/type`, `identity_card_number`, `customer_contact_name/phone`. `$customerName` ưu tiên snapshot HĐ. PHP lint OK. (Phiếu KHÔNG có quan hệ `files` → không thêm khối file.)
- [x] FE `ServiceAccountingForm.vue`: bỏ trường "Mã phiếu" (bug1, mã đã ở tiêu đề màn); bỏ badge trạng thái ở header (parity #12010); Số hợp đồng → ô link `contractLink()`; bổ sung khối KH (Mã KH, Tên viết tắt, CMT/MST, Người liên hệ + ĐT liên hệ khi `customer_type > 1`); thêm style `.link-field` + `.v2-cell-link`.
- [x] FE `CostTable.vue`: bug2 — dồn 3 dòng tổng (Tổng trước thuế / Tiền VAT / Tổng thanh toán) vào `<tfoot>` của bảng viền (bỏ `summary-table` nổi), bám CSS #12010.
- [x] grep self-check element thô: chỉ còn `<div class="form-control ... link-field">` (idiom ô-link chỉ-đọc copy từ `CoordinationDetail.vue`) + `<button class="close">` header popup — không vi phạm V2Base.
- [x] Playwright `127.0.0.1:3000/finance/service-accounting/3045` (KH tổ chức, có địa chỉ): KHÔNG còn "Mã phiếu", KHÔNG badge, Số HĐ link ERP :8001 (`.../firm-contracts/24570`), Mã KH `99TBAPTA-8`, CMT/MST `5200896689-005`, **Địa chỉ đã hiện** "Đường Tây Yên Tử…", Người liên hệ `Anh Bình` + ĐT liên hệ `0918575366`, bảng chi phí viền + tfoot 60,000 / VAT 8% 4,800 / 64,800. Console chỉ lỗi socket.io :8891 (không liên quan).

## #12008 — YC HĐBH Tạo/Sửa (code xong, chưa commit)

Theo QĐ-08.* trong design.md.

- [x] BE: `FirmContract::all_costs()`; `firmContractList` lọc theo kiểu + `whereNull('is_zt')`; `contractCustomerBlock()` dùng chung; `attachmentSizes` + route.
- [x] FE: viết lại `FirmContractPickerModal.vue`; sửa `ServiceAccountingRequestForm.vue`; `ServiceAccountingRequestDetail.vue` đổi khối file.
- [x] FE footer: bỏ `mr-2 mb-2` ở custom-actions (đo trước 17/17/5px, sau 5/5/5px, cùng hàng).
- [x] Playwright 127.0.0.1:3000 (NV 215): popup 62 HĐ khớp SQL, kiểu 3 = 288; lọc/sort/chọn dòng; × dọn hết; toast + inline; chọn tất cả; tfoot 1,595,400,000 / VAT 8% 127,632,000 / 1,723,032,000; lưu nháp, Sửa pre-tick, upload, Chi tiết readonly, attachment-sizes 200. Phiếu test 3748 đã xoá khỏi DB local.
- [x] File test `tanphat_hrm/test12008pdf-1793948329-t9Sl.pdf` đã xoá khỏi S3 (06/11, qua `CmcS3Helper::deleteByUrl`).
- [x] Commit local, CHƯA push: api `73d354d52`, client `2cbaee23b` (develop).
- [x] Kế toán bán hàng (role 100005) lập phiếu: gán `Hạch toán dịch vụ HĐBH` (101914) cty 1,2,3,4,8 trên DB LOCAL → POST 403 thành 422. Dev/prod chưa gán.
- [x] Kế toán bán hàng: user chốt xem THEO CÔNG TY (101478) cty 1,2,3,4,8, đã gán LOCAL.
- [ ] Dev/prod: admin gán tay 2 quyền cho Kế toán bán hàng ở màn Chức vụ HRM, từng công ty (user chốt 06/11). Đọc code: form giữ quyền ERP, chưa bấm Lưu thử.
- [x] QĐ-08.1 đã chốt (mẫu chung V2Footer).
- [x] QĐ-08.2 user chốt giữ như ERP (06/11).
- [x] QĐ-08.6 sửa theo user: HRM khớp số hợp đồng ERP; 6 NV nhiều HĐ nhất khớp ở mọi kiểu, popup thật NV 27 = 17.

## #12058 — YC hạch toán dịch vụ HDDV Danh sách (06/11/2026)
- [x] Nguyên nhân: FE không gửi `type`, BE mặc định lọc `created_by = người đăng nhập`.
- [x] `pages/finance/wr-accounting-service-requests/index.vue`: `loadData()` và `runExport` gửi `type: 'all'`.
- [x] Playwright 127.0.0.1:3000: request có `type=all`, bảng hiện 10 dòng của người lập khác.

- 2026-11-06: đã commit local trên develop, api `ecbb395c8` / client `5ee34182a`, chưa push.
