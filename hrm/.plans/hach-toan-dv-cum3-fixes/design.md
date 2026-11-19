# Cụm ③ — Fix bug Hạch toán dịch vụ HĐBH / HDDV (Redmine, assignee Trần Cư)

6 ticket QA trên các màn đã port ERP→HRM. Chia 4 màn × 2 loại hợp đồng:

| Loại HĐ | YC hạch toán (request)            | Phiếu hạch toán (voucher)   |
| ------- | --------------------------------- | --------------------------- |
| HĐBH    | `service-accounting-requests`     | `service-accounting`        |
| HDDV    | `wr-accounting-service-requests`  | `wr-accounting-services`    |

Ticket ↔ màn:
- **#12030** — YC HDDV Danh sách → `wr-accounting-service-requests`
- **#12003** — YC HĐBH Danh sách → `service-accounting-requests`
- **#12024** — Phiếu HĐBH Danh sách → `service-accounting`
- **#12008** — YC HĐBH Tạo mới → `service-accounting-requests/create`
- **#12010** — YC HĐBH Chi tiết → `service-accounting-requests/_id`
- **#12026** — Phiếu HĐBH Chi tiết → `service-accounting/_id`

Thứ tự làm: nhẹ → nặng. #12030 (list) → #12003 (list) → #12024 (list) → #12010/#12026 (detail parity) → #12008 (create, nặng nhất, nhiều ảnh prnt.sc + lệch data ERP).

---

## #12030 — YC HDDV Danh sách (3 bug)

Màn: `hrm-client/pages/finance/wr-accounting-service-requests/index.vue`
BE: `hrm-api/Modules/Finance/Entities/WrAccountingServiceRequest/WrAccountingServiceRequest.php` (`applyFilters`)

### Hiện trạng rà được
- **bug① quick-search**: FE placeholder đã = "Tìm theo số phiếu, số hợp đồng" (đúng). Nhưng BE
  `applyFilters` keyword (dòng 352-356) còn OR `customer_name` → lệch placeholder. Reviewer khoanh đỏ
  "khách hàng" trong ảnh = muốn quick-search CHỈ số phiếu + số hợp đồng.
- **bug② link số HĐ**: cột `contractCode` đang hiện chữ, không link (comment cũ "HĐ DV CHƯA PORT").
  Thực tế màn chi tiết HĐ DV **đã port** = `/customer-care/wr-service-contracts/{id}`. Resource list
  **đã trả sẵn** `wr_service_contract_id` (dòng 34). → FE chỉ cần render link mở tab mới.
- **bug③ sort cột Tổng thanh toán**: cột KHÔNG tồn tại ở cả ERP lẫn HRM. `total_cost` lưu JSON nhóm
  (other_cost + delivery_cost). → **User chốt BỎ QUA bug③**, hỏi lại reviewer (nghi nhầm màn).

### Quyết định đã chốt
- **QĐ-30.1 (bug①)**: BE bỏ `->orWhere('customer_name', 'like', $keyword)` khỏi keyword → quick-search
  chỉ khớp `code` (số phiếu) + `wrServiceContract.code` (số HĐ). Cập nhật comment dòng 348.
- **QĐ-30.2 (bug②)**: cột Số hợp đồng render `<a :href target="_blank">` tới
  `/customer-care/wr-service-contracts/{wr_service_contract_id}` khi có id; không id → hiện chữ thường.
  Dùng class `v2-cell-link` sẵn có (KHÔNG nuxt-link vì mở tab mới).
- **QĐ-30.3 (bug③)**: KHÔNG làm; để lại câu hỏi cho reviewer. Cột Tổng thanh toán không có ở ERP gốc.

### Phạm vi KHÔNG làm
- Không thêm cột Tổng thanh toán, không migration, không đụng luồng ghi.
- Không đổi quyền, không đổi Resource ngoài field đã có.

---

## #12003 — YC HĐBH Danh sách (4 bug)

Màn: `hrm-client/pages/finance/service-accounting-requests/index.vue`
BE: `ServiceAccountingRequest::applyFilters` (đã hỗ trợ đủ key) + `ServiceAccountingRequestListResource`

### Hiện trạng rà được
- **bug1 hyperlink Số HĐ + giãn ô/xuống dòng**: cột `contractCode` đang hiện chữ trơn (comment cũ
  "HĐ hãng CHƯA PORT → để link trống"). HĐ hãng (FirmContract) **vẫn chưa có màn chi tiết trong HRM**
  (chỉ có picker modal). NHƯNG đã có helper chung `utils/contract-link.js` → `contractLink(type, id)`:
  FirmContract (`App\Model\Sale\Firm\Contract\FirmContract`) rơi vào `ERP_ROUTES` → mở ERP
  `/admin/sale/firm-contracts/{id}` ở **tab mới** (user chốt 2026-09-29, quy ước `erp-link.js`: màn chưa
  port vẫn cho bấm, mở sang ERP). Resource đang trả `contract_id` nhưng THIẾU `contract_type`.
- **bug2 cột hành động thiếu "Hạch toán dịch vụ"**: thực tế `getRowActions` **ĐÃ có** action
  `accounting` (icon `ri-calculator-line`, gate `is_can_accounting`) → `/finance/service-accounting/create?service_accounting_request_id={id}`.
  Màn đích đã port. ERP gốc cột action = Sửa / Xóa / Hạch toán dịch vụ — HRM parity (thêm Không duyệt,
  Lịch sử). ⇒ bug2 đã xong từ Phase 2, chỉ VERIFY.
- **bug3 bộ lọc thiếu Mã / Người duyệt / Người yêu cầu**: ERP có 7 lọc (code=Mã, contract_code, status,
  approver_id=Người duyệt, customer, created_by=Người lập, request_by=Người yêu cầu). HRM FE chỉ phơi 1 ô
  employee nhãn "Người tạo" nhưng gửi `requester_id` → BE map `requester_id` = contractable.created_by =
  **Người yêu cầu** (người lập HĐ) ⇒ ô "Người tạo" bị **mislabel** (đang lọc nhầm theo người lập HĐ).
  BE đã hỗ trợ đủ 3 key `created_by` / `approver_id` / `requester_id`.
- **bug4 đổi "Số phiếu" → "Mã phiếu"**: cột header, filter `code`, quick-search placeholder, export field.

### Quyết định đã chốt
- **QĐ-03.1 (bug1)**: Resource thêm `'contract_type' => $item->contractable_type` (FQN ERP, khớp key
  `contractLink`). FE cột Số HĐ dùng `contractLink(item.contract_type, item.contract_id)`: có `href` →
  `<a :href target="_blank" rel="noopener">`; có `to` → nuxt-link; null → chữ thường. Cột cho **xuống
  dòng** (`cellClass: 'text-wrap'`) + nới rộng (minWidth 240px). KHÔNG port màn HĐ hãng.
- **QĐ-03.2 (bug2)**: GIỮ NGUYÊN — action đã đúng. Chỉ verify hiện khi phiếu Chờ duyệt + có quyền.
  - **Cập nhật 06/11 (ảnh dev):** dev, DNS Admin, phiếu 02819 Chờ duyệt: ERP có nút, HRM chỉ có Lịch sử. Code đúng;
    local cùng tài khoản (id 13) có đủ nút. Lệch do cách cấp quyền: ERP `Gate::before` cho role web "Super Admin"
    qua mọi quyền, còn HRM `canAccounting()` đòi dòng `role_has_permissions` thật. DNS Admin chỉ có quyền nhờ
    dòng role 18 ↔ quyền api 101913, mà seeder CHỈ tạo quyền, KHÔNG gán ⇒ dev có thể thiếu dòng này (hoặc dev
    chưa deploy bản có nút; CHƯA xác nhận được vì không vào được DB dev). Không đổi code quyền, chờ user chốt.
- **QĐ-03.3 (bug3)**: FE sửa ô "Người tạo" từ key `requester_id` → `created_by` (đúng nghĩa người tạo
  phiếu); THÊM ô "Người duyệt" (`approver_id`) + ô "Người yêu cầu" (`requester_id`). 3 ô employee khớp
  ERP. `initialStateForm` thêm `created_by`, `approver_id` (giữ `requester_id`). BE không đổi.
- **QĐ-03.4 (bug4)**: đổi mọi nhãn "Số phiếu" → "Mã phiếu" (cột `code`, filter `code`, placeholder quick
  search, export field `code`). Quick-search GIỮ tìm theo khách hàng (ticket không yêu cầu bỏ).

### Phạm vi KHÔNG làm
- Không port màn chi tiết HĐ hãng (ngoài scope — link ra ERP theo quy ước sẵn).
- Không sửa BE `applyFilters` (đã hỗ trợ đủ key); không migration; không đụng luồng ghi/quyền.

---

## #12024 — Phiếu HĐBH Danh sách (4 bug)

Màn: `hrm-client/pages/finance/service-accounting/index.vue` (PHIẾU hạch toán = voucher, KHÁC màn YC).
BE: `ServiceAccounting` entity + `ServiceAccountingService` + `ServiceAccountingListResource` + `CatalogHistoryService`.

### Hiện trạng rà được
- **bug1 thiếu "Tạo mới"**: màn phiếu HRM (Phase 2) cố tình bỏ "Tạo mới" vì phiếu sinh từ YC. ERP gốc
  CÓ nút "Tạo mới" độc lập + popup chọn YC "Chờ duyệt". Reviewer muốn parity → thêm lại. Admin có đủ quyền
  `Hạch toán dịch vụ HĐBH` nhưng FE không phơi nút.
- **bug2 "người lập" → "người tạo"**: cột `creatorName`, filter `created_by`, export `creator_name` đang
  nhãn "Người lập"; export `created_at` nhãn "Ngày lập". Đổi hết sang "Người tạo"/"Ngày tạo" (parity #12003).
- **bug3 link Số hợp đồng**: cột `contractCode` hiện chữ trơn (comment cũ "HĐ hãng CHƯA PORT"). Giống
  #12003: Resource thiếu `contract_type` → FE không dựng được `contractLink`. Thêm → mở ERP tab mới.
- **bug4 Lịch sử lỗi + không hiển thị trạng thái** (ROOT CAUSE đã xác nhận):
  - (a) Bảng `service_accounting` KHÔNG đăng ký trong `CatalogHistoryService::TABLES`/`GATED_TABLES` →
    `tableConfig()` trả null → endpoint `catalog-histories/service_accounting/{id}` lỗi ("Lịch sử lỗi").
  - (b) `ServiceAccountingService` KHÔNG dùng trait `LogsCatalogHistory` → store/update/approve/destroy
    CHƯA từng ghi dòng lịch sử nào, đặc biệt không ghi đổi trạng thái ("không hiển thị trạng thái").
  - Mẫu đúng để nhân bản: `ServiceAccountingRequestService` (request, cùng module) — đã log đủ.
  - Cột phí voucher (`service_accounting_costs`) có `name` + `total_price` giống request → `details_rows`
    nhân bản y hệt `snapshotOf()` của request.

### Quyết định đã chốt
- **QĐ-24.1 (bug1) — USER CHỐT HƯỚNG A (port ERP 1:1)**: thêm nút "Tạo mới" độc lập trên toolbar màn phiếu
  (v-if `scopeMeta.can_create`), dẫn `/finance/service-accounting/create`. Màn create mở **popup chọn YC
  "Chờ duyệt"** (bám `BaseSearchModal` ERP): nguồn dữ liệu reuse `GET finance/service-accounting-requests?status=2`
  (CHO_DUYET = tập YC đủ điều kiện, vì tạo phiếu sẽ đẩy YC sang DA_HACH_TOAN). Chọn YC → nạp form.
  Nới `ServiceAccountingEditForm` KHÔNG còn redirect 404 khi thiếu `srcRequestId` — thay bằng mở picker.
  BE chỉ thêm: const `PERMISSION_ACCOUNTING` + `canCreate()` ở entity; `'can_create'` vào `meta()`.
  KHÔNG thêm endpoint mới.
- **QĐ-24.2 (bug2)**: đổi mọi nhãn "Người lập"→"Người tạo" (cột `creatorName`, filter `created_by`, export
  `creator_name`) + "Ngày lập"→"Ngày tạo" (export `created_at`). Chỉ FE text.
- **QĐ-24.3 (bug3)**: Resource `ServiceAccountingListResource` thêm `'contract_type' => $item->contractable_type`.
  FE import `contractLink`, cột `#cell-contractCode` dùng `contractLink(item.contract_type, item.contract_id)`
  → `href` tab mới / `to` nuxt-link / chữ trơn. Thêm `cellClass: 'text-wrap'` + nới rộng cột (parity #12003).
- **QĐ-24.4 (bug4)**:
  - Đăng ký `service_accounting` vào `CatalogHistoryService::TABLES` (label "phiếu hạch toán dịch vụ HĐBH",
    columns: contract_code/customer_name/type/payed_cost/note/status/details_rows).
  - `ServiceAccountingService` `use LogsCatalogHistory`: `catalogTable()`, `catalogColumns()`,
    `catalogDisplay()` (status→STATUSES, type→TYPES), `snapshotOf()` (override virtual keys), log create
    (store), log update + logStatus (update, chụp before trước khi fill), log delete (destroy), log status
    draft→approved (approveAndPost). Nhân bản 1:1 `ServiceAccountingRequestService`.

### Phạm vi KHÔNG làm
- Không port màn chi tiết HĐ hãng (link ra ERP theo quy ước).
- Không đụng HDDV voucher `wr_accounting_services` (đã đăng ký bảng nhưng cũng chưa log — NGOÀI scope #12024).
- Không thêm endpoint BE cho bug1; không migration; không đổi luồng duyệt/hạch toán.

## #12010 — YC HĐBH Chi tiết + #12026 — Phiếu HĐBH Chi tiết

Ticket #12010: "Chi tiết: đang ko khớp, đồng bộ dạng sang hrm theo các màn khác" + annotation ảnh:
BỔ SUNG khối thông tin khách hàng · CSS lại phần tổng chi phí như ERP · BỎ badge "Chờ duyệt" ở header.
Ticket #12026 (phiếu): bug1 "bỏ các trường ko cần thiết" (vd "Mã phiếu" ghi BỎ) · bug2 "CSS Chi tiết
chi phí về dạng bảng" · THÊM link HĐ · "CHƯA LẤY ĐC ĐỊA CHỈ QUA" · "BỔ SUNG THÊM CÁC TRƯỜNG, TAB".

### Hiện trạng
- Bảng `service_accounting_requests` / `service_accounting` LEAN — KHÔNG có cột snapshot khách hàng.
  Dữ liệu KH lấy qua quan hệ `contractable` = `FirmContract` (`firm_contracts`), bảng này CÓ sẵn:
  `customer_id, customer_name, customer_type, customer_address, customer_mobile, customer_fax,
  customer_contact_name, customer_contact_phone, identity_card_number`… + quan hệ `customer`
  (`customers.code`, `customers.short_name`).
- ERP `customer_unit` (Tên viết tắt) = `customer.short_name` (xác nhận qua `ServiceQuotationController`);
  `identity_card_number` (CMT/MST) = snapshot trên firm_contract; contact name/phone chỉ hiện khi
  `customer_type > 1` (tổ chức).
- `detailData()` ĐÃ eager-load `contractable.customer` + `employeeCreate.info`; `files` đã trả sẵn.

### Quyết định đã chốt (user chốt 2026-11-06, đều hướng Recommended)
- **QĐ-10.1 (khối KH) — FULL PARITY như ERP qua quan hệ HĐ.** BE `detailData()` thêm:
  `contract_type` (= `contractable_type`, để link), `customer_code` (customer.code),
  `customer_short_name` (customer.short_name = Tên viết tắt), `customer_type` (int, điều khiển hiện contact),
  `identity_card_number` (CMT/MST, snapshot HĐ), `customer_contact_name`, `customer_contact_phone`.
  FE thêm các ô CHỈ-ĐỌC: Mã KH · Khách hàng · Tên viết tắt · CMT/MST · Điện thoại · Địa chỉ ·
  (nếu `customer_type > 1`) Người liên hệ + ĐT liên hệ · File đính kèm (dùng `FileAttachmentTable`/`V2BaseFile`).
- **QĐ-10.2 (link HĐ)**: ô "Số hợp đồng" dùng `contractLink(form.contract_type, form.contract_id)` →
  FirmContract mở ERP tab mới (`:8001`). Có link thì render `<a>` / `nuxt-link`, không có thì chữ trơn
  (bỏ ô disabled + comment "CHƯA PORT").
- **QĐ-10.3 (badge) — BỎ badge trạng thái ở header**, theo ERP (reviewer ghi BỎ). Giữ `CreatorInfoLine`.
  Trạng thái vẫn thấy ở cột danh sách + nút hành động. (Lệch convention HRM nhưng user chốt theo ERP.)
- **QĐ-10.4 (CSS tổng chi phí)**: gộp 3 dòng tổng (Tổng trước thuế / Tiền VAT / Tổng thanh toán) vào
  `<tfoot>` CÙNG bảng chi phí có viền (bám ERP), BỎ bảng `summary-table` float riêng.
- **QĐ-26.1 (#12026 bug1)**: màn phiếu `service-accounting/_id` — bỏ trường thừa ("Mã phiếu" khỏi khối
  thông tin chung; mã đã nằm ở tiêu đề màn), đồng bộ khối KH + link HĐ + CSS tổng như QĐ-10.*.
- **QĐ-26.2 (#12026 bug2 + layout)**: GIỮ single-page HRM (KHÔNG tách tab như ERP). Phần tài khoản hạch
  toán (nếu có: DT 5113 / giá vốn 632 / nợ 1311 / chiết khấu 5211 / thuế 33311) gom thành 1
  `V2BaseFormSection` riêng, KHÔNG dựng tab. Chi tiết chi phí về dạng bảng có viền + tfoot như QĐ-10.4.

### Phạm vi KHÔNG làm (#12010/#12026)
- KHÔNG thêm cột snapshot KH vào bảng phiếu (đọc qua quan hệ HĐ).
- KHÔNG tách tab; KHÔNG đổi luồng duyệt/hạch toán; KHÔNG migration.

## #12008 — YC HĐBH Tạo/Sửa (9 lỗi)

Nguồn: ticket + 8 ảnh đính kèm + 7 ảnh user gửi 06/11. Đối chiếu ERP
`resources/views/sale/service_accounting_requests/form.blade.php`, `formJs.blade.php:75`, `FirmContractDatatable.php:332,434`.

### Nguyên nhân gốc lỗi 6 (popup hiện cả HĐ không có chi phí)
HRM lọc `whereHas('support_accounting')` — gần như HĐ nào cũng có, nên không lọc được gì. ERP lọc
`type=has_costs` = `whereHas('all_costs')` + có hiệu lực + do mình lập + `whereNull('is_zt')`.

### Quyết định đã chốt (tự chốt, user CHƯA xác nhận — báo lại khi xong)
- **QĐ-08.1 (lỗi 1)**: user chốt 06/11: dùng mẫu chung, đã có thì để vậy. Form YC đã dùng `V2Footer`; bỏ `mr-2 mb-2` tự thêm ở màn Chi tiết YC, Chi tiết phiếu, form Sửa phiếu để khoảng cách do `.group-select-btn` lo (đo 5px, nút cùng hàng; form Sửa chưa đo vì thiếu phiếu sửa được).
- **QĐ-08.2 (lỗi 2,5,9 File đính kèm)**: dùng `V2BaseAttachmentSection` + adapter `attachmentFiles.js`,
  CHỈ hiện sau khi chọn HĐ (bám ERP `ng-if="form.contractable"`). BE thêm `GET /{id}/attachment-sizes`.
  Màn Chi tiết đổi sang cùng khối ở chế độ `readonly`.
- **QĐ-08.3 (lỗi 3)**: ô HĐ dùng `V2BasePickerInput` (khoá ở màn Sửa); bấm × dọn HĐ + KH + chi phí + file.
- **QĐ-08.4 (lỗi 4)**: `FirmContractPickerModal` viết lại theo khuôn `WarehouseImportSearchModal` (size xl,
  `V2BaseDataTable`, bấm cả dòng để chọn). Ghi chú cũ "lỗi 4 đã xong" là SAI.
- **QĐ-08.5 (lỗi 5)**: nhãn "Kiểu hạch toán"; trái Kiểu + HĐ, phải Ghi chú; bỏ ô Kinh doanh; khối KH chỉ hiện sau khi chọn HĐ.
- **QĐ-08.6 (lỗi 6)**: sửa 06/11, bản cũ thiếu `type = HOP_DONG` và miễn chi phí cho kiểu 3 nên HRM hiện nhiều hơn ERP (509 và 8.544 so với 321). Nay khớp popup ERP (`searchContract`, `has_costs`, `firm`) ở mọi kiểu: loại Hợp đồng, có hiệu lực, do mình lập, không ZT, có `all_costs`. Giữ `support_accounting` (không làm giảm số: 321/321 đều có). FE bỏ gửi `type`.
- **QĐ-08.7 (lỗi 7)**: cột STT, ô chọn tất cả (bỏ qua dòng đã xuất), "Dịch vụ đi kèm"/"Chi phí"; tổng vào `<tfoot>`,
  VAT chỉ hiện khi có %; placeholder "Nhập ghi chú". KHÔNG thêm cột Ghi chú theo dòng của ERP kiểu 2,3.
- **QĐ-08.8 (lỗi 8)**: thiếu dữ liệu thì toast + giữ lỗi inline; 422 từ BE cũng toast.
- **QĐ-08.9 (lỗi 9)**: bỏ badge trạng thái ở màn Sửa; khối KH đủ trường như ERP.

### Phạm vi KHÔNG làm
- Không thêm swal cảnh báo khi đổi HĐ của ERP; không đổi luồng duyệt; không migration.
