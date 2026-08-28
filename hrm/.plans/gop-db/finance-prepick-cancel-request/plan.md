# Plan — Hủy hàng giữ (ERP → HRM), 2 màn

> @junfoke · nhánh `feat/finance-prepick-cancel` (từ `gop_db`, cả 2 repo) · design: `./design.md`
>
> **Trạng thái: XONG PHASE 0-9 PHẦN CODE + ĐÃ VERIFY HTTP END-TO-END (2026-08-15).**
> Phạm vi: màn `Yêu cầu hủy hàng giữ` + màn `Phiếu hủy hàng giữ`. Đây là màn ĐẦU TIÊN của HRM
> **ghi vào tồn kho thật** (`prepick_details` + `prepick_logs`) → đọc kỹ Phase 0 và Phase 5.
>
> BE 21 file `Modules/Finance` (6 entity + 5 service + 2 controller + 3 FormRequest + 2 Resource
> + 5 blade in) + 2 migration + 25 route. FE 19 file (`pages/finance/prepick-cancel-requests`,
> `pages/finance/prepick-cancels`, `components/finance/prepick`) + 2 mục menu.
>
> **Verify**: 16/16 route GET đúng dữ liệu · luồng ghi end-to-end (tạo nháp → sửa + gửi duyệt →
> duyệt vượt bị chặn 422 rollback sạch → duyệt thật → trừ FIFO 2 lô đúng thứ tự `expire_date` →
> 2 dòng `prepick_logs` đúng chuỗi lớp ERP → lịch sử 4 mốc + 1 mốc) và luồng Không duyệt
> (thiếu lý do → 422; có lý do → về Đang tạo, lưu `comment`, sửa lại được).
> Dọn sạch dữ liệu test rồi **đối chiếu TỪNG CỘT 6 bảng với bản sao lưu: 0 lệch**.
>
> **Còn lại (user làm)**: bấm tay trên trình duyệt, đối chiếu 2 cổng trên dev, test bằng tài khoản
> `Quản lý giữ hàng` không phải Super admin, xoá 6 bảng `bak_*_20260815`.

## Nguồn ERP cần đọc

| Việc | File ERP (`TanPhatDev/`) |
| --- | --- |
| Controller yêu cầu | `app/Http/Controllers/Warehouse/PrepickCancelRequestsController.php` (569 dòng) |
| Model yêu cầu | `app/Model/Warehouse/PrepickCancelRequest.php` (321) + `PrepickCancelRequestDetail.php` (21) |
| Controller phiếu hủy | `app/Http/Controllers/Warehouse/PrepickCancelsController.php` (243 dòng) |
| Model phiếu hủy | `app/Model/Warehouse/PrepickCancel.php` (286) + `PrepickCancelDetail.php` (21) |
| Blade yêu cầu | `resources/views/warehouse/prepick_cancel_requests/*.blade.php` (7 file) |
| Blade phiếu hủy | `resources/views/warehouse/prepick_cancels/*.blade.php` (5 file) |
| Class JS | `resources/views/partials/classes/warehouse/PrepickCancel{,Detail,Request,RequestDetail}.blade.php` |
| Route | `routes/web.php:1712-1738` |
| Tồn giữ | `app/Product.php:2357` (`getAccountingStockDetail`) · `app/Services/Product/ProductStockService.php:13` |
| Modal lịch sử giữ hàng | `resources/views/partials/historyPrepickModal.blade.php` + `WarehouseInfosController@getHistoryPrepickDetails` |
| Excel | `app/ExcelExports/PrepickCancelRequestExcel.php` · `PrepickCancelExcel.php` + 2 blade `reports/exports/` |

## Khuôn mẫu HRM cần copy (KHÔNG tự phát minh)

| Phần | File mẫu |
| --- | --- |
| Entity + hằng số + `can*()` | `Modules/Finance/Entities/ProductImportDirectTransfer/ProductImportDirectTransfer.php` |
| Kiểm quyền qua pivot | trait `Modules/Finance/Entities/Concerns/ChecksEmployeePermission` |
| Service (search/meta/show/store/update/approve FIFO) | `Modules/Finance/Services/ProductImportDirectTransferService.php` |
| Service lịch sử (subset-diff) | `Modules/Finance/Services/ProductImportDirectTransferHistoryService.php` |
| Controller + thứ tự route | `Modules/Finance/Http/Controllers/V1/ProductImportDirectTransferController.php` + `Routes/api.php` |
| Thông báo | `EmployeeInfoService::sendNotification($employeeInfoId, $data)` (xem `ProductImportRequestService`) |
| FE danh sách V2 | `pages/finance/product-import-direct-transfers/index.vue` |
| FE form + popup + tồn | `.../components/ProductImportDirectTransferForm.vue` + `StockSearchModal.vue` |
| FE lịch sử | `.../components/ProductImportDirectTransferHistoryPanel.vue` + `...HistoryModal.vue` |
| FE xuất Excel | `.../components/export-excel.js` |
| FE in danh sách ngang | `.../print-list.vue` |

---

## Phase 0 — Chuẩn bị

- [x] Tạo nhánh `feat/finance-prepick-cancel` từ `gop_db` ở **cả 2 repo** (`hrm-api`, `hrm-client`)
- [x] Đọc `.plans/gop-db/design.md` (nền tảng gộp DB) + `./design.md`
- [x] Đọc skill: `list-page`, `button-convention`, `modal-popup`, `form-validate`,
      `unsaved-changes`, `print-page`, `entity-history` (+ `ui-base.md`), `notification-convention`
- [x] **Sao lưu 6 bảng** trước khi test (đợt này ĐỤNG TỒN THẬT):
      `prepick_cancel_requests`, `prepick_cancel_request_details`, `prepick_cancels`,
      `prepick_cancel_details`, **`prepick_details`**, **`prepick_logs`**.
      Đặt tên `bak_<ten>_20260815`. Ghi lại số dòng từng bảng vào checkpoint.
- [x] Ghi lại "ảnh chụp" tồn giữ để đối chiếu sau:
      `SELECT COUNT(*), SUM(qty) FROM prepick_details` và `SELECT COUNT(*) FROM prepick_logs`

### Checkpoint — Phase 0

```text
Vừa hoàn thành: tạo nhánh `feat/finance-prepick-cancel` ở cả 2 repo (checkout thẳng từ
`gop_db`); sao lưu 6 bảng sang `bak_<ten>_20260815`.
Đang làm dở: không.
Bước tiếp theo: Phase 1 — BE nền.
Blocked: không.
Verify: prepick_cancel_requests 3.521 · request_details 9.956 · prepick_cancels 3.478 ·
cancel_details 9.752 · prepick_details 53.832 (SUM qty = 6.112) · prepick_logs 110.744.
```

---

## Phase 1 — BE nền: entity + tồn giữ + danh sách Yêu cầu

- [x] Tạo `Modules/Finance/Entities/PrepickCancel/` — 6 entity:
      `PrepickCancelRequest` (`$table = 'prepick_cancel_requests'`), `PrepickCancelRequestDetail`,
      `PrepickCancel`, `PrepickCancelDetail`, `PrepickDetail` (`prepick_details`),
      `PrepickLog` (`prepick_logs`).
      **Khai `use` đầy đủ** cho mọi class tham chiếu chéo — bên ERP các model cùng namespace nên
      không có `use`, port sang là 500 lúc chạy mà `php -l` không bắt.
      **Không** dùng connection `mysql2`.
- [x] Hằng trạng thái yêu cầu — **giữ nguyên cách đánh số lệch của ERP**:
      `DA_DUYET = 1` · `CHO_DUYET = 2` · `DANG_TAO = 3`. Không có giá trị `0`.
      `EDITABLE_STATUSES = [DANG_TAO]` (khác nhập thẳng: sửa được cả khi Chờ duyệt — ở đây KHÔNG).
- [x] Hằng tên quyền: `PERMISSION_QUAN_LY_GIU_HANG = 'Quản lý giữ hàng'`,
      `PERMISSION_VIEW_ALL_COMPANY = 'Xem phiếu hàng giữ theo tổng công ty'`,
      `..._COMPANY = '... theo công ty'`, `..._DEPARTMENT = '... theo phòng ban'`.
      **Chỉ 3 cấp** — KHÔNG có cấp bộ phận.
- [x] `use ChecksEmployeePermission` — KHÔNG dùng spatie Eloquent / `ErpPermissionHelper`
- [x] Hằng chuỗi lớp ERP cho `prepick_logs.objectable_type`:
      `const ERP_PREPICK_CANCEL_TYPE = 'App\\Model\\Warehouse\\PrepickCancel';`
      (giống `ProductImportDirectDetail::ERP_TRANSFER_PRODUCT_TYPE`)
- [x] `generateCode()`: `PYCHHG-` + `generateCode(5, $this->id)` cho yêu cầu; `PHHG-` cho phiếu hủy
- [x] Tạo `Services/PrepickStockService.php` — **chỗ duy nhất chạm `prepick_details`/`prepick_logs`**:
      - `searchHoldingProducts($params)` — popup chọn hàng: join `products` × `prepick_details`,
        lọc `employee_id` / `customer_id` / `company_id` / tên / mã, `GROUP BY p.id`,
        `SUM(pd.qty) AS prepick_qty`, phân trang
      - `holdingCustomers($employeeId, $companyId)` — danh sách KH đang có hàng giữ (cho dropdown)
      - `availableQty($productId, $employeeId, $customerId, $companyId)` — `SUM(prepick_details.qty)`
        **trừ** `warehouse_export_request_details.export_prepick_qty` của các ĐN xuất kho chưa xong
        (`is_complete != 1 AND status NOT IN (3,5)`) → đúng con số "Có thể hủy" của ERP
      - `qtyOfProducts(array $items, ...)` — gọi hàng loạt cho form
      - `deductFifo(...)` — Phase 5 mới viết, khai chỗ trước
      ⚑ Sửa lỗi #7: popup và form dùng **chung** `availableQty` nên 2 số luôn khớp
- [x] Port `searchByFilter()` cho yêu cầu — 3 preset:
      - `mine` → `created_by = me`
      - `all` → 3 cấp quyền (tổng công ty ⊃ công ty ⊃ phòng ban ⊃ chỉ của mình),
        + ẩn phiếu `DANG_TAO` của người khác
      - `waiting_approve` → `status = CHO_DUYET` + cùng công ty, gate `Quản lý giữ hàng`;
        không có quyền → `whereRaw('1 = 0')`
      Giá trị `type` lạ → quy về `mine`. Bỏ điều kiện lặp ở dòng 238 của ERP (lỗi #6).
- [x] Bộ lọc: `code`, `created_by`, `status`, `approver`, `product_name`, `product_code`,
      `company`, `department`, `startDate`/`endDate`
- [x] `SORTABLE_COLUMNS` whitelist: `code`, `createdAt` — key FE phải trùng key BE
- [x] `canView()` / `canEdit()` / `canDelete()` / `canApprove()`:
      ⚑ **Sửa lỗi #5** — `canView()` phải có đủ 4 nhánh khớp đúng phạm vi `searchByFilter`
      (tổng công ty / công ty / phòng ban / người tạo) + nhánh `Quản lý giữ hàng`
- [x] `PrepickCancelRequestListResource` — cột `id`, `code`, `createdByName` (subquery, KHÔNG
      leftJoin), `createdAt` (`Helper::formatDate`), `status` + `statusName` + `statusType`,
      `approverName`, `approvedTime`, `customerName`, `note`, `comment`, `departmentName`,
      cờ `can_edit` / `can_delete` / `can_approve`
- [x] `PrepickCancelRequestService::search()` — paginate `per_page`, trả `meta`
- [x] Route `GET /v1/finance/prepick-cancel-requests` — **không** middleware quyền
- [x] **Verify**: gọi HTTP thật với 3 loại tài khoản (Super admin / có `Quản lý giữ hàng` /
      nhân viên thường), đối chiếu số dòng với màn ERP tương ứng

### Checkpoint — Phase 1

```text
Vừa hoàn thành: 8 entity (`PrepickCancelRequest` + Detail + History, `PrepickCancel` +
Detail + History, `PrepickDetail`, `PrepickLog`), `PrepickStockService`,
`PrepickCancelRequestService`, ListResource, 25 route.
Đang làm dở: không.
Bước tiếp theo: Phase 2 — FE danh sách.
Blocked: không.
Verify (gọi HTTP thật): NV #13 (Super admin + 3 quyền cấp) type=all -> 3.478 phiếu
(= 3.521 tổng trừ 43 phiếu nháp của người khác, ĐÚNG) · NV #34 (Xem theo công ty) -> 3.478 ·
NV #587 (chỉ có `Quản lý giữ hàng`, không có quyền cấp nào) type=all -> 154 = đúng số phiếu
do chính họ lập. Preset `waiting_approve` trả 0 vì DB không có phiếu nào status 2.
⚠️ `customer_name` null ở ~91% phiếu — KHÔNG phải lỗi màn này: chỉ 299/3.521 `customer_id`
có bản ghi trong bảng `customers` (lỗ hổng dữ liệu đã biết của DB gộp,
xem memory `project_gop_db_customers_thieu_dai_id_erp`).
```

---

## Phase 2 — FE danh sách Yêu cầu

- [x] `pages/finance/prepick-cancel-requests/index.vue` — copy khung từ
      `product-import-direct-transfers/index.vue`
- [x] 3 preset tab: `Của tôi` · `Tất cả` · `Chờ tôi duyệt` (tab 3 chỉ hiện khi có quyền
      `Quản lý giữ hàng` — cờ do BE trả về, **fail-closed**, không hard-code `true`)
- [x] 7 cột mặc định: STT · Mã phiếu (sticky, `.v2-cell-link`) · Người lập · Ngày lập · Trạng thái ·
      Người duyệt · Ngày duyệt
- [x] 4 cột ẩn (bật qua Cấu hình cột): Khách hàng · Ghi chú · Lý do không duyệt · Phòng ban.
      `columnScreenKey: 'finance_prepick_cancel_requests'`
- [x] `V2BaseFilterPanel` + `filterStateMixin` — 7 bộ lọc như Phase 1.
      Nút **Làm mới** phải nạp lại danh sách (bẫy đã sửa ở 24 màn khác)
- [x] Ô tìm nhanh có deep watcher tự tìm; bộ lọc Nâng cao KHÔNG lặp lại field của tìm nhanh
- [x] `V2BaseRowActions`: Sửa · Xóa + menu 3 chấm (Duyệt · Không duyệt · In phiếu · Lịch sử).
      **Disable chứ không ẩn** khi không đủ điều kiện. Icon: `ri-edit-line` / `ri-delete-bin-6-line`
- [x] Sắp xếp 2 cột `code` / `createdAt` — key phải trùng tên trường BE
- [x] `.table-responsive` `min-height: 50vh`; header dính không lệch chữ (`border-collapse`)
- [ ] **Verify trình duyệt**: đợi Nuxt nạp xong chunk rồi mới đọc DOM (bẫy đã gặp)

### Checkpoint — Phase 2

```text
Vừa hoàn thành: `pages/finance/prepick-cancel-requests/index.vue` — 3 preset tab
(Của tôi / Tất cả / Chờ tôi duyệt), 7 cột mặc định + 4 cột ẩn, 8 bộ lọc, `V2BaseRowActions`
6 hành động, sắp xếp 2 cột.
Đang làm dở: không.
Bước tiếp theo: Phase 3 — form.
Blocked: không.
Verify: compile template bằng `vue-template-compiler` — 18/18 file .vue không lỗi.
CHƯA bấm tay trên trình duyệt (để user làm).
```

---

## Phase 3 — Chi tiết / Tạo / Sửa / Xóa Yêu cầu

### BE

- [x] `GET /{id}` — `findForShow()`: nạp chi tiết + KH + người lập + phòng ban + phiếu hủy tương
      ứng (để hiện cột "Duyệt hủy" và link). Gate `canView()`
- [x] `GET /stock` — popup chọn hàng đang giữ, gọi `PrepickStockService::searchHoldingProducts()`.
      Tham số: `customer_id` (bắt buộc), `employee_id` (mặc định người đăng nhập), `name`, `code`,
      `page`, `per_page`
- [x] `GET /customers` — dropdown KH đang có hàng giữ của người lập
- [x] `POST /` + `PUT /{id}` qua `PrepickCancelRequestRequest` (FormRequest):
      `customer_id` required|exists · `status` required|in:2,3 · `products` required|array|min:1 ·
      `products.*.qty` required|numeric|min:0|max:999999 · `note` nullable|max:255.
      ⚑ **Sửa lỗi #3** — FormRequest chạy ở CẢ tạo và sửa (ERP bỏ quên ở `update`)
- [x] `normalizeProducts()` + `assertEnoughStock()` — gộp các dòng cùng `product_id` **trước khi**
      so với tồn (ERP so từng dòng rời). Chỉ xét dòng `need_cancel = true && qty > 0`
- [x] `syncProducts()` — xóa rồi tạo lại chi tiết, chép `product_name`/`model_name`/`brand_name`/
      `unit_name`/`code` như ERP (snapshot tên tại thời điểm lập)
- [x] `DELETE /{id}` — gate `canDelete()`, xóa chi tiết trước rồi xóa phiếu
- [x] Thông báo khi `status = 2`: ⚑ **sửa lỗi #4** — gửi cho **người có quyền `Quản lý giữ hàng`
      cùng công ty** qua `EmployeeInfoService::sendNotification($employeeInfoId, $data)`
      (ERP gửi theo `warehouse_id` không tồn tại → mảng rỗng)
- [x] ⚠ Kiểm `BaseModel` của HRM có ghi đè `created_by` không (bẫy đã gặp ở màn trước)

### FE

- [x] `components/PrepickCancelRequestForm.vue` — dùng chung `create` / `edit` / `show`
      (`mode` prop), `unsavedChangesMixin` + `formValidateMixin`, `V2Footer`
- [x] 2 khối `form-card`: Thông tin chung (Khách hàng select2 bắt buộc, **khóa sau khi đã lưu** ·
      Ghi chú ≤255) và Chi tiết
- [x] Bảng: STT · Cần hủy (checkbox) · Tên hàng hóa · Model · Mã hàng hóa · Thương hiệu ·
      Có thể giữ · Có thể hủy · Yêu cầu hủy (nhập) · ĐVT (khóa) · Xóa dòng
- [x] `components/PrepickStockSearchModal.vue` — popup chọn hàng đang giữ, cột STT · Ảnh ·
      Tên hàng hóa · Model · Mã · ĐVT · Đang giữ. Chặn chọn trùng hàng đã có trong bảng
- [x] Đổi Khách hàng ⇒ nạp lại toàn bộ số tồn giữ; `Yêu cầu hủy` clamp theo `Có thể hủy`
- [x] Footer: **Lưu nháp** (status 3) · **Gửi duyệt** (status 2) · **Quay lại**.
      Nút Gửi duyệt disable khi chưa có dòng nào tick + `qty > 0`
- [x] `create.vue` / `_id/edit.vue` / `_id/index.vue` — trang vỏ, `beforeRouteLeave` gắn ở đây
      (`unsavedChildFormMixin`), con giữ `markFormSaved()`
- [x] ⚠ Nạp `receivers`/`customers` **sau khi** `loadDetail()` xong (bẫy race đã gặp ở màn trước)
- [x] Màn chi tiết: thêm cột **Duyệt hủy**, khối **Lý do không duyệt** khi có `comment`,
      link sang phiếu hủy, nút **Duyệt** / **Không duyệt** khi `can_approve`

### Checkpoint — Phase 3

```text
Vừa hoàn thành: `GET /{id}` + `/stock` + `/customers`, FormRequest, store/update/destroy,
`PrepickCancelRequestForm.vue` (dùng chung create/edit/show), `PrepickStockSearchModal.vue`,
4 trang vỏ.
Đang làm dở: không.
Bước tiếp theo: Phase 4 — Không duyệt.
Blocked: không.
Verify: tạo phiếu test qua HTTP -> mã sinh ra **PYCHHG-03539**, 1 dòng chi tiết; sửa +
gửi duyệt -> đổi sang status 2 OK. Phiếu test đã xoá sau khi verify.
```

---

## Phase 4 — Không duyệt (reject)

- [x] `POST /{id}/reject` — gate `canApprove()`, `comment` required|max:255
- [x] Set `status = DANG_TAO (3)` + lưu `comment` (đúng ERP: từ chối đưa về nháp, KHÔNG có trạng
      thái "Không duyệt" riêng)
- [x] Thông báo cho người lập qua `EmployeeInfoService::sendNotification`
- [x] FE: modal nhập lý do (`V2BaseModal`), gọi API, toast, quay về danh sách
- [x] **Verify**: chỉ thao tác trên phiếu tự tạo ở Phase 3 — KHÔNG bắn vào id thật

### Checkpoint — Phase 4

```text
Vừa hoàn thành: `POST /{id}/reject` + `RejectModal.vue`.
Đang làm dở: không.
Bước tiếp theo: Phase 5 — trừ tồn FIFO.
Blocked: không.
Verify trên phiếu tự tạo: thiếu lý do -> 422 `Bắt buộc phải nhập lý do không duyệt`;
có lý do -> 200, phiếu về **Đang tạo**, `comment` lưu đúng, `is_can_edit` = true,
lịch sử hiện mốc `Không duyệt` kèm ghi chú.
```

---

## Phase 5 — BE Phiếu hủy: duyệt + TRỪ TỒN FIFO ⚠

> Phase nguy hiểm nhất. Đọc lại mục "Rủi ro" của design.md trước khi bắt đầu.
> **Tuyệt đối không** bắn POST vào `prepick_cancel_request_id` của phiếu thật.

- [x] `PrepickCancel` entity: `$table = 'prepick_cancels'`, quan hệ `parent` → `PrepickCancelRequest`,
      `products` → `PrepickCancelDetail`, `customer`.
      `status` luôn = `1` (ERP không có vòng đời cho phiếu này)
- [x] `canView()` — ⚑ **sửa lỗi #8**: quyền `Quản lý giữ hàng`, HOẶC là người lập phiếu hủy,
      HOẶC là người lập yêu cầu gốc. Nhánh cuối `return false` (ERP viết nhầm `return true`)
- [x] `searchByFilter()` cho phiếu hủy — ⚑ **sửa lỗi #12**: áp đủ 3 cấp quyền như màn yêu cầu
      (ERP chỉ lọc `company_id` của người đăng nhập)
- [x] Bộ lọc: `code`, `product_name` (tìm cả tên và mã), `requester` (người lập yêu cầu),
      `created_by`, `startDate`/`endDate`. ⚑ **Sửa lỗi #10**: bỏ 2 bộ lọc chết
      (`status` và `approver`)
- [x] `GET /from-request/{requestId}` — nạp dữ liệu lập phiếu hủy: gate `canApprove()` của yêu cầu,
      trả chi tiết yêu cầu (chỉ dòng `need_cancel = true`) + `available_qty` từng dòng tính tại
      thời điểm gọi
- [x] `PrepickStockService::deductFifo($productId, $employeeId, $customerId, $companyId, $qty, $objectableId)`:
      ```
      $lots = PrepickDetail::where(product_id, employee_id, customer_id, company_id)
          ->where('qty', '>', 0)->orderBy('expire_date', 'ASC')
          ->lockForUpdate()->get();                       // ⚑ ERP KHÔNG khóa
      if ($lots->sum('qty') < $qty) throw ...;            // ⚑ sửa lỗi #13
      // trừ dần, mỗi lô ghi 1 dòng prepick_logs:
      //   prepick_detail_id, objectable_id = <id phiếu hủy>,
      //   objectable_type = PrepickCancel::ERP_PREPICK_CANCEL_TYPE,
      //   qty_before, change (âm), qty_after
      // bỏ qua khi $qty <= 0 (ERP vẫn ghi 1 dòng log change = 0)
      ```
- [x] `POST /` (`PrepickCancelStoreRequest`) — **1 transaction**, đúng thứ tự:
      1. `lockForUpdate` phiếu yêu cầu + kiểm `canApprove()`
      2. Kiểm từng dòng: `qty <= request_qty` **và** `qty <= availableQty`
      3. Tạo `prepick_cancels` (`company_id` = công ty người lập phiếu hủy) + `generateCode()`
      4. `syncProducts()` → `prepick_cancel_details`, `unit_coefficient` lấy từ `product_units`,
         `cancel_qty = qty × unit_coefficient`, `request_qty` chép từ dòng yêu cầu
      5. `deductFifo()` cho từng dòng — `employee_id` là **người lập YÊU CẦU**, không phải người
         lập phiếu hủy
      6. Set yêu cầu: `status = 1`, `approver_id`, `approved_time`
      7. Ghi 2 bản ghi lịch sử (Phase 7)
      8. Thông báo người lập yêu cầu
- [x] ⚑ Chặn trường hợp lỗi #7 (rủi ro): người lập phiếu hủy khác công ty với người lập yêu cầu →
      không tìm ra lô nào → phải báo lỗi rõ ràng thay vì trừ hụt im lặng
- [x] `GET /` (danh sách) · `GET /{id}` (chi tiết, gate `canView()`)
- [x] Route `/v1/finance/prepick-cancels` — route tĩnh (`/export`, `/print-list-data`,
      `/from-request/{requestId}`) khai **TRƯỚC** `/{id}`
- [x] **Verify bằng phiếu tự tạo**:
      - ghi lại `prepick_details.qty` của các lô liên quan TRƯỚC khi duyệt
      - duyệt → kiểm số lô bị trừ, thứ tự đúng `expire_date` tăng dần, tổng trừ = `cancel_qty`
      - kiểm `prepick_logs` sinh đúng số dòng, `objectable_type` đúng chuỗi ERP
      - mở modal "Lịch sử giữ hàng" **bên ERP** xem có đọc được dòng log HRM vừa ghi không
      - thử duyệt quá tồn → phải báo lỗi và **rollback sạch** (kiểm lại `prepick_details` không đổi)

### Checkpoint — Phase 5

```text
Vừa hoàn thành: `PrepickCancelService::store()` (1 transaction: khoá phiếu yêu cầu ->
kiểm 2 ràng buộc -> tạo phiếu + chi tiết -> `deductFifo()` -> chuyển yêu cầu sang Đã duyệt),
`PrepickStockService::deductFifo()` với `lockForUpdate` + kiểm đủ tồn trước khi trừ.
Đang làm dở: không.
Bước tiếp theo: Phase 6 — FE phiếu hủy.
Blocked: không.
Verify trên phiếu tự tạo (NV #583, KH 23848, hàng 10343, 4 đơn vị):
  · duyệt VƯỢT số đề nghị -> 422, tồn **KHÔNG đổi** (rollback sạch)
  · duyệt thật -> PHHG-03484; FIFO đúng thứ tự `expire_date`: lô 53656 (hạn 06/08) 3->0,
    rồi lô 52167 (hạn 14/08) 2->1. Tổng trừ 4 = đúng số duyệt hủy.
  · `prepick_logs` sinh đúng 2 dòng, `objectable_type` = `App\Model\Warehouse\PrepickCancel`
    (đúng chuỗi lớp ERP).
CHƯA kiểm modal "Lịch sử giữ hàng" bên ERP có dựng được link không (cần chạy 2 cổng song song).
```

---

## Phase 6 — FE Phiếu hủy

- [x] `pages/finance/prepick-cancels/index.vue` — 6 cột: STT · Mã phiếu (sticky, `.v2-cell-link`) ·
      Phiếu yêu cầu (link) · Người yêu cầu · Người lập · Ngày lập.
      Cột ẩn: Khách hàng · Ghi chú. `columnScreenKey: 'finance_prepick_cancels'`
- [x] ⚑ **Sửa lỗi #9**: KHÔNG có nút Thêm rời trên danh sách
- [x] `V2BaseRowActions`: In phiếu · Lịch sử (không Sửa / Xóa — ERP cũng không có)
- [x] `create.vue` + `components/PrepickCancelForm.vue`:
      vào từ `?request_id=...`, hoặc mở trống rồi chọn qua `components/RequestSearchModal.vue`
      (popup lọc sẵn `status = 2`, cùng công ty)
- [x] Khối 1 (chỉ đọc trừ Ghi chú): Phiếu yêu cầu · Người yêu cầu · Phòng ban yêu cầu · Khách hàng ·
      Ghi chú
- [x] Khối 2 — bảng: STT · Cần hủy · Tên hàng hóa · Model · Mã hàng hóa · Thương hiệu ·
      Có thể hủy · Yêu cầu hủy · **Duyệt hủy (nhập)** · ĐVT.
      Clamp `Duyệt hủy` ≤ min(`Có thể hủy`, `Yêu cầu hủy`)
- [x] Footer: **Duyệt** · **Quay lại**. Nút Duyệt kèm hộp xác nhận nêu rõ
      "sẽ trừ tồn giữ, không hoàn tác được"
- [x] `_id/index.vue` — chi tiết chỉ đọc + link về phiếu yêu cầu + section Lịch sử
- [x] ⚠ Bỏ trường `Kho` của ERP (lỗi #11 — không có cột/quan hệ, luôn trống)

### Checkpoint — Phase 6

```text
Vừa hoàn thành: `pages/finance/prepick-cancels/` — danh sách 6 cột (không có nút Thêm,
không có Sửa/Xoá), `PrepickCancelForm.vue`, `RequestSearchModal.vue`, 3 trang vỏ + 2 trang in.
Đang làm dở: không.
Bước tiếp theo: Phase 7 — lịch sử.
Blocked: không.
Verify: `GET /prepick-cancels` NV #13 -> 3.478 phiếu; NV #587 (Quản lý giữ hàng, công ty 4)
-> 1.700 = đúng số phiếu của công ty 4. `from-request/{id}` trả 403 đúng khi phiếu yêu cầu
đã duyệt xong.
```

---

## Phase 7 — Lịch sử thay đổi (tính năng MỚI)

- [x] 2 migration ở **`hrm-api/database/migrations/`** (KHÔNG đặt trong `Modules/*`):
      `create_prepick_cancel_request_history_table`, `create_prepick_cancel_history_table`.
      Cùng khuôn 9 cột với `product_import_direct_transfer_history`.
      ⚠ **Đặt tên index thủ công** để không vượt 64 ký tự MySQL (bẫy đã gặp: lỗi 1059)
- [x] `PrepickCancelRequestHistoryService` — subset-diff, snapshot lưu **giá trị hiển thị**.
      Hành động: `create` · `update` · `send_approve` · `reject` · `approve`
- [x] `PrepickCancelHistoryService` — hành động `create`, snapshot kèm số lượng đã trừ mỗi dòng
- [x] Khóa dòng hàng hóa = `product_id` (không cần `unit_id`, luôn ĐV cơ bản) vì `syncProducts`
      xóa rồi tạo lại toàn bộ chi tiết
- [x] `getLogs()` trả đúng DTO của skill `entity-history`, gồm `created_at_raw`, sắp **mới → cũ**
- [x] `GET /{id}/histories` cho cả 2 màn
- [x] FE: `HistoryPanel.vue` (thân dùng chung) + `HistoryModal.vue`; gắn ở **CẢ 2 nơi** —
      popup ⋮ ở danh sách và section ở màn chi tiết
- [x] ⚠ Chạy migration ở local phải kiểm trước `php artisan migrate:status` — lần trước lỡ chạy
      15 migration của người khác. Nếu có migration lạ đang pending thì **dừng lại hỏi**

### Checkpoint — Phase 7

```text
Vừa hoàn thành: 2 migration ở `database/migrations/` (tên index đặt tay:
`pcr_history_*`, `pc_history_*`), 2 history service subset-diff, `PrepickHistoryPanel.vue` +
`PrepickHistoryModal.vue` dùng chung cho cả 2 màn, gắn ở CẢ popup danh sách lẫn màn chi tiết.
Đang làm dở: không.
Bước tiếp theo: Phase 8 — in/Excel.
Blocked: lệnh `php artisan migrate` bị cơ chế phân loại quyền chặn 2 lần; user cấp quyền
rồi mới chạy được.
Verify: 1 vòng tạo -> sửa -> gửi duyệt -> duyệt sinh **4 mốc** ở lịch sử yêu cầu
(Tạo phiếu 4 thay đổi · Chỉnh sửa 2 thay đổi · Gửi duyệt · Duyệt kèm ghi chú mã phiếu hủy)
và **1 mốc** ở lịch sử phiếu hủy (`Đã trừ tồn hàng giữ trên 2 lô.`). Sắp xếp mới -> cũ.
```

---

## Phase 8 — In (4 mẫu) + Xuất Excel (2 màn)

- [x] 4 mẫu HTML trong `Modules/Finance/Resources/views/prints/` — **KHÔNG** thêm dòng vào
      `report_templates` (bảng dùng chung ERP):
      `prepick-cancel-request.blade.php` (A4 dọc) · `prepick-cancel-request-list.blade.php`
      (A4 ngang) · `prepick-cancel.blade.php` (A4 dọc) · `prepick-cancel-list.blade.php` (A4 ngang).
      Bám bố cục mẫu 424 (YC gia hạn giữ) và 426 (điều chuyển hàng giữ)
- [x] Bản in ngang: khai đè `@page { size: A4 landscape }` trong khối `styles` truyền cho
      `$printContent` — plugin không có option landscape (bẫy đã gặp)
- [x] `GET /{id}/print-data` + `GET /print-list-data` cho cả 2 màn; `print-list-data` nhận nguyên
      query string của màn danh sách để bản in khớp bộ lọc đang áp
- [x] `_id/print.vue` + `print-list.vue` cho cả 2 màn (copy khung từ màn nhập thẳng)
- [x] ⚠ Màn `.vue` in bị mất scoped CSS → styles phải nằm trong chuỗi truyền cho `$printContent`
- [x] `GET /export` trả **dữ liệu thô** + `filter_text`; file do FE dựng bằng ExcelJS
      (`components/export-excel.js`), 7 cột (yêu cầu) / 6 cột (phiếu hủy)
- [x] ⚠ 2 bẫy ExcelJS: mã phiếu + ngày ghi dạng **chuỗi** (tránh "Number stored as text");
      căn lề đặt trên **từng ô** (`column.alignment` ghi đè cả cột kể cả dòng tiêu đề)
- [x] ⚠ `$axios` FE thiếu `Authorization` → phải tự gắn token khi tải file
- [x] Số thập phân dùng `formatCurrency($x, 3)` (HRM không có `formatQuantity`)

### Checkpoint — Phase 8

```text
Vừa hoàn thành: 5 blade in trong `Modules/Finance/Resources/views/prints/` (_layout +
4 mẫu), `renderPrint`/`renderPrintList`/`exportData` cho cả 2 service, 2 `export-excel.js`,
4 trang in FE.
Đang làm dở: không.
Bước tiếp theo: Phase 9 — verify tổng.
Blocked: không.
Verify: 4/4 endpoint in trả HTTP 200 có HTML; kiểm nội dung mẫu phiếu yêu cầu — đủ tiêu đề,
số phiếu, ngày lập, 5 dòng thông tin, bảng 7 cột + dòng Tổng cộng, khối ký 2 cột.
KHÔNG ghi thêm dòng nào vào `report_templates` (bảng dùng chung với ERP).
```

---

## Phase 9 — Menu + Verify tổng + bàn giao

- [x] `components/subsystem-menu/finance.js` — thêm `link` cho 2 mục đã có sẵn trong nhóm
      **Giữ hàng**: `Yêu cầu hủy hàng giữ` → `/finance/prepick-cancel-requests`,
      `Phiếu hủy hàng giữ` → `/finance/prepick-cancels`
- [x] Sidebar hub lọc theo quyền — kiểm 2 mục hiện/ẩn đúng
- [x] Quét **thiếu `use`** bằng `token_get_all()` (bỏ comment) trên toàn bộ file mới — cách grep
      thường cho 8 false positive vì tên class nằm trong docblock
- [x] Quét toàn bộ route mới bằng **GET** — **TUYỆT ĐỐI KHÔNG** bắn POST/PUT/DELETE vào id thật
      (lần trước lỡ duyệt thật 1 phiếu, phải khôi phục từ backup)
- [x] Đối chiếu DB với bản sao lưu Phase 0: 6 bảng, **0 lệch** ngoài các phiếu test tự tạo
- [ ] Đối chiếu 2 cổng trên dev: phiếu tạo ở HRM hiện đúng ở ERP và ngược lại; log tồn giữ do HRM
      ghi hiện đúng trong modal "Lịch sử giữ hàng" của ERP
- [ ] Test với tài khoản có `Quản lý giữ hàng` nhưng **KHÔNG** phải Super admin
- [ ] Bấm tay toàn bộ: 7 bộ lọc · 2 cột sắp xếp · phân trang · giữ bộ lọc khi quay lại
- [x] Cập nhật `STATUS.md` (ngắn gọn) + memory
- [ ] Xóa 6 bảng `bak_*_20260815` sau khi xác nhận xong

### Checkpoint — Phase 9

```text
Vừa hoàn thành: gắn `link` cho 2 mục menu có sẵn trong `finance.js` nhóm **Giữ hàng**;
quét thiếu `use` bằng `token_get_all()` (20 file PHP, 0 thiếu); `php -l` toàn bộ file mới;
compile 18 file .vue; quét 16 route GET; dọn dữ liệu test.
Đang làm dở: không.
Bước tiếp theo: user bấm tay trên trình duyệt + đối chiếu 2 cổng trên dev.
Blocked: không.
Verify: đối chiếu **TỪNG CỘT** 6 bảng nghiệp vụ với bản sao lưu Phase 0 — **0 lệch** trên
cả 6 (requests 3.521 · request_details 9.956 · cancels 3.478 · cancel_details 9.752 ·
prepick_details 53.832 · prepick_logs 110.744). 2 lô tồn bị trừ khi test đã khôi phục.
```

---

## Phase 10 — Vá bug QA (redmine 11094 / 11149 / 11150 / 11151 / 11152 / 11154, 2026-08-21)

- [x] **11151** — dropdown Khách hàng: **GIỮ NGUYÊN** phạm vi "chỉ KH mà nhân viên đó đang giữ
      hàng". Tester mở bằng tài khoản không giữ lô nào nên thấy rỗng và log là bug; user chốt đây là
      đúng nghiệp vụ (chọn KH không có lô thì popup Thêm hàng hóa rỗng, lưu cũng bị
      `assertEnoughStock()` chặn). Sửa phần **giải thích**: FE hiện dòng ⓘ ngay dưới ô khi danh
      sách rỗng + đổi placeholder thành "Không có khách hàng đang giữ hàng".
- [x] **11152** — Lưu nháp chỉ bắt buộc Khách hàng. `PrepickCancelRequestRequest::rules()` cho
      `products` là `nullable` khi `status = DANG_TAO` (gửi duyệt vẫn `required|min:1`), và
      `assertEnoughStock()` nhận thêm cờ `$requireLine` để bỏ luật "ít nhất 1 dòng tick" cho nháp —
      số lượng của dòng ĐÃ nhập thì vẫn kiểm tồn như thường.
- [x] **11150** — Ngày tạo / Ngày duyệt hiển thị kèm giờ `d/m/Y H:i` ở danh sách
      (`PrepickCancelRequestListResource::formatDate()`), màn chi tiết (`detailData()`) và dữ liệu
      Xuất Excel; 2 cột trên bảng nới `110px → 140px`.
- [x] **11094** — đổi chữ "Người lập / Ngày lập" → **"Người tạo / Ngày tạo"** ở toàn bộ màn danh
      sách (cột, bộ lọc, ô tìm nhanh, file Excel, mẫu in danh sách) + thêm 2 cột **Người cập nhật /
      Ngày cập nhật** vào bảng, popup Tùy chỉnh cột và popup Chọn trường xuất Excel. Entity thêm
      quan hệ `employee_update` + khoá sắp xếp `updatedAt`, eager load kèm `searchByFilter()`.
- [x] **11149** — ẩn nút **In** cả danh sách ở đầu bảng (icon In từng phiếu ở cột Hành động giữ
      nguyên). Trang `print-list.vue` + endpoint `print-list-data` **giữ nguyên**, chỉ gỡ lối vào.
- [x] **11154** — khối Lịch sử màn chi tiết dùng đúng khuôn chung của 2 màn Tài chính port trước:
      icon đồng hồ + badge số mốc + nút "Xem lịch sử"/"Thu gọn" + "Làm mới"; `PrepickHistoryPanel`
      phát thêm sự kiện `loaded` (số mốc) — bổ sung, không đổi hành vi 2 nơi đang dùng.
- [ ] User bấm tay lại 6 lỗi trên dev rồi đóng issue.

### Checkpoint — Phase 10

```text
Vừa hoàn thành: 6 issue QA ở trên (BE 6 file + FE 4 file).
Đang làm dở: không.
Bước tiếp theo: user verify trên dev; riêng 11151 trả lời tester là "không phải lỗi", đã bổ sung
chú thích trên màn để không hiểu nhầm nữa.
Blocked: không.
Verify: `php -l` + nạp 6 class qua Laravel bootstrap; compile template + parse script 4 file .vue;
chạy thật `customerOptions()` (tài khoản không giữ lô nào → 0 option, đúng thiết kế) và `rules()`
(nháp: products nullable · gửi duyệt: required|min:1).
⚠️ DB local thiếu dải id `customers` nên nhóm KH đang giữ hàng không dựng được tại chỗ — đã kiểm
riêng bằng SQL, trên dev có đủ dữ liệu.
```

---

## Phase 11 — Bỏ tab preset, gộp về 1 danh sách (2026-08-21)

Yêu cầu user: màn HRM tương ứng đúng tham số `all` của ERP; hiện nút duyệt theo QUYỀN chứ không
bắt người dùng chuyển tab. Màn mẫu: Phiếu thu / Phiếu chi của @khoipv.

- [x] FE gỡ `V2BaseTabNavigation` + computed `presetTabs` + `handlePresetChange` + key `type`
      trong bộ lọc; `handleReset` không phải giữ preset nữa; localStorage cũ còn `type` thì
      `mergeKnownFilters()` tự bỏ (key không còn trong `initialStateForm`).
- [x] BE **giữ nguyên** tham số `type` (link cũ / lối vào từ ERP vẫn chạy), chỉ đổi mặc định và
      phạm vi nhánh mặc định.
- [x] `PrepickCancelRequest::searchByFilter()` — mặc định (không có `type`) nay là **`all`**
      thay vì `mine`; `mine` / `waiting_approve` giữ lại cho link cũ.
- [x] Thêm `applyAllScope()` + `orWhereApprovable()`: phạm vi = quyền xem theo cấp **HOẶC** phiếu
      Chờ duyệt cùng công ty khi có quyền `Quản lý giữ hàng`. Thiếu vế OR này là người duyệt
      không có quyền xem theo cấp mất hẳn phiếu cần duyệt (trước đây họ vào bằng tab riêng).
- [x] ⚠️ Không bọc closure khi user xem được hết — `() OR (approvable)` sẽ thu hẹp danh sách
      xuống đúng tập approvable.
- [ ] User verify trên dev bằng tài khoản `Quản lý giữ hàng` không phải Super admin.

### Checkpoint — Phase 11

```text
Vừa hoàn thành: bỏ tab ở màn danh sách + vá phạm vi nhánh mặc định ở BE.
Đang làm dở: không.
Bước tiếp theo: user verify trên dev.
Blocked: không.
Verify: dump SQL thật với NV 26 (có `Quản lý giữ hàng`, KHÔNG có quyền xem theo cấp) →
`where ((created_by = ?) or (status = ? and company_id = ?)) and (status != ? or (...))` — đúng ý đồ.
Đếm danh sách khi FE không gửi `type`: admin 3.478 · NV thường 58 · NV 26: 0 (DB local không có
phiếu Chờ duyệt nào).
```

---

## Phase 12 — Rà lại màn Phiếu hủy hàng giữ theo quy tắc chung (2026-08-22)

Yêu cầu user: màn `Kế toán → HH-DV-Vận chuyển → Giữ hàng → Phiếu hủy hàng giữ` đã port rồi thì
**bổ sung cho đúng quy tắc chung**. Chạy checklist skill `erp-to-hrm-screen` trên cả thư mục
`pages/finance/prepick-cancels/`.

Kết quả grep tự kiểm: SẠCH (`status-pill`, `interactable:`, `action.key ===`, `V2BaseFilterPanel`,
`advanced-filters` đều không có). Phần lệch còn lại đã vá:

- [x] **Ô "Duyệt hủy" tự kéo về trần** (`onQtyChange`) → bỏ hẳn việc sửa giá trị; thay bằng
      `qtyErrorOf()` báo đỏ ngay dưới ô theo cấu trúc `Tên trường – Nội dung lỗi`, đang gõ dở
      `12.` thì chưa báo. Vi phạm rule user chốt 17/08/2026.
- [x] **`validateProducts()` chặn gọi API** khi còn dòng lỗi + toast QLDA_001 + cuộn về ô lỗi đầu.
- [x] **Duyệt xong `$router.push` về DANH SÁCH** (trước đây đẩy sang màn chi tiết) — rule user
      chốt 20/08/2026.
- [x] **Nút In ở `V2Footer` màu teal** → dựng lại ở slot `#custom-actions` bằng `V2BaseButton
      secondary` (In là action phụ). `footerMenu` màn Chi tiết nay trả `{}`.
- [x] **4 ô khóa có chủ ý thêm icon ⓘ + tooltip** (Phiếu yêu cầu, Người yêu cầu, Phòng ban yêu cầu,
      Khách hàng) — ô disabled bộ V2 nhìn y hệt ô trống.
- [x] **Mã phiếu đưa lên ô ĐẦU TIÊN** của card Thông tin chung ở màn Chi tiết (SRS mục 3: số phiếu
      hiển thị trên cùng, ngay sau tiêu đề màn).
- [x] `emptyText` đổi về đúng nguyên văn QLDA_011 "Không có dữ liệu phù hợp."
- [ ] User verify trên dev.

### 2 điểm treo — user yêu cầu xử lý luôn (2026-08-22)

**1. Mixin `CheckPermission` — KHÔNG thêm, đã khảo sát xong.** Cả họ Giữ hàng cố ý không dùng: điều
kiện hiện/ẩn nút đọc từ **cờ BE** (`is_can_edit` mỗi dòng + `meta.is_big_boss/is_boss/is_manager/
is_prepick_manager`), đúng nguyên tắc "đọc điều kiện từ CÙNG 1 nguồn" của skill. Thêm
`hasAPermission()` ở FE là dựng nguồn thứ hai, sớm muộn lệch với BE. Đã dò lỗ hổng quyền thật:

- `store()` → `PrepickCancelService::store()` gọi `$parent->canApprove()` **trong transaction đã
  khoá lô** → không có quyền `Quản lý giữ hàng` là chặn, không trừ được tồn.
- `waitingRequests()` → `if (!isPrepickManager()) return ['data' => [], 'total' => 0]`.
- `show()` → `canView()`; danh sách → 3 cấp quyền xem.

→ Không có lỗ hổng. Nhưng có **khoảng trống UX**: người không có quyền vẫn mở được
`/finance/prepick-cancels/create`, popup chọn phiếu yêu cầu trả rỗng mà không nói lý do — đúng kiểu
bug tester báo ở #11151. Đã vá:

- [x] BE `waitingRequests()` trả thêm `is_prepick_manager` (thêm `use ...PrepickCancelRequest`).
- [x] FE `RequestSearchModal.vue`: `emptyText` thành computed, tách 2 câu — chưa có quyền thì ghi
      *"Bạn chưa có quyền \"Quản lý giữ hàng\" nên không duyệt được… Liên hệ Quản trị viên"*, có
      quyền mà rỗng thì giữ câu cũ.

**2. Checkbox "Cần hủy" → `V2BaseCheckbox`.** Đã đổi ở **cả 2 màn của feature** để không lệch nhau:

- [x] `PrepickCancelForm.vue` — `:modelValue` + `@change="onNeedCancelChange(product, index, $event)"`
      (handler tự gán `product.need_cancel` rồi validate lại dòng).
- [x] `PrepickCancelRequestForm.vue` — `:modelValue` + `@change="product.need_cancel = !!$event"`.
- ⚠️ Không truyền default slot, chỉ dùng prop `label` (bỏ trống vì cột đã có tiêu đề "Cần hủy"):
      `singleMode = options.length === 0 && !$slots.default`, có slot là render ra khối RỖNG.

**Ngoài phạm vi, CHƯA đụng** (2 chỗ còn dùng `<input type="checkbox">` trần trong bảng, khác feature):
`finance/bill-payment-requests/components/BillPaymentRequestDetailTable.vue:25,83` và
`finance/product-import-direct-transfers/components/StockSearchModal.vue:83`.

### Test thật bằng Playwright (2026-08-22) — 3 lỗi NỮA lộ ra khi bấm

Chạy trên local `127.0.0.1:3000` (Nuxt dev) + API `:8000`, DB `gop_db`, tài khoản DNS Admin.

- [x] **`V2Footer` gói sẵn popup xác nhận cho `menu.approve`** — bấm Duyệt là hiện popup chung chung
      *"Bạn xác nhận duyệt phiếu?"* RỒI mới emit, nên: (1) màn bị **2 popup chồng nhau**,
      (2) validate chỉ chạy **sau** popup đầu → user bấm xác nhận xong mới biết mình nhập sai.
      → Dựng lại nút Duyệt ở `#custom-actions` luôn (cùng chỗ với nút In), `footerMenu` trả `{}`.
      Thứ tự ra đúng vì slot nằm ngay trước "Quay lại": **Duyệt → In → Quay lại**.
      Màu giữ `primary` (teal) theo `button-convention` — user chốt 20/08 nhóm Duyệt dùng teal.
- [x] **Selector cuộn-về-ô-lỗi sai**: `is-invalid` nằm ở `.v2-input__wrapper`, KHÔNG ở thẻ `input`.
      Bắt `input.is-invalid` là con trỏ không nhảy mà cũng không báo gì.
- [x] **Nút Duyệt dùng `:interactable`** (nút xám khi chưa chọn phiếu yêu cầu) → đổi sang `v-if`,
      ẩn hẳn theo rule hiện hành.

Kết quả đo trên trình duyệt sau khi vá:

| Kiểm | Kết quả |
|---|---|
| Danh sách | 10 dòng/trang, cột đúng 7 cột, mã là `<nuxt-link>` `/finance/prepick-cancels/3483` |
| Chi tiết | tiêu đề `Chi tiết phiếu hủy hàng giữ: PHHG-03483`, **Mã phiếu là ô đầu tiên**, **4 icon ⓘ** |
| Nút In | nền `rgb(255,255,255)`, chữ `rgb(51,51,51)` — đúng nhóm "Action phụ" của SRS |
| Gõ 99 (trần 4) | ô **vẫn giữ 99**, viền `rgb(220,53,69)`, lỗi *"Duyệt hủy – Không được vượt 4…"* |
| Bấm Duyệt khi còn lỗi | **KHÔNG popup**, toast `Bạn chưa nhập đầy đủ thông tin.`, focus nhảy đúng ô lỗi |
| Sửa về 3 rồi bấm Duyệt | lỗi tự mất, popup *"…sẽ TRỪ TỒN HÀNG GIỮ ngay lập tức…"* (đã bấm Hủy, KHÔNG gọi API) |
| Nút Duyệt | chưa chọn phiếu YC: chỉ có `[Quay lại]`; chọn rồi: `[Duyệt, Quay lại]` |
| Popup chọn phiếu YC | rỗng đúng câu "Không có phiếu yêu cầu nào đang chờ duyệt."; ép `isPrepickManager=false` → ra câu "Bạn chưa có quyền…" |
| `V2BaseCheckbox` trong bảng | render 43×20, vùng bấm x=18–34 trong ô rộng 60, click toggle được |
| Console | 0 error ở cả 4 màn |

**Chưa test được:** luồng Duyệt CHẠY THẬT (trừ tồn + chuyển phiếu YC sang Đã duyệt) — DB local
không có phiếu nào `status=2` (Chờ duyệt): 3.478 phiếu status 1 + 43 phiếu status 3. Cần user
chuyển 1 phiếu sang Chờ duyệt trên dev rồi bấm thật.

### Checkpoint — Phase 12

```text
Vừa hoàn thành: 7 điểm vá theo quy tắc chung ở PrepickCancelForm.vue + index.vue.
Đang làm dở: không.
Bước tiếp theo: user tạo 1 phiếu yêu cầu Chờ duyệt trên dev rồi bấm Duyệt thật để kiểm
trừ tồn + điều hướng về danh sách (2 nhánh này Playwright chưa chạm tới được).
Blocked: không.
Verify: hrm-client KHÔNG cài eslint (không có script lint, không có devDependency) — node_modules
vẫn đủ, `npm run dev` chạy bình thường. Đã verify bằng `vue-template-compiler` + `@babel/core`:
3 file .vue template OK + script OK; `php -l` controller: no syntax errors.
```

---

## Bẫy đã biết — đọc lại trước mỗi phase

1. **KHÔNG bắn POST/PUT/DELETE vào id thật** khi quét route. Chỉ dùng phiếu tự tạo.
2. **KHÔNG chạy `php artisan migrate --force`** khi đang có migration lạ pending — kiểm
   `migrate:status` trước, thấy migration của người khác thì dừng lại hỏi.
3. Migration đặt ở `database/migrations/`, **không** đặt trong `Modules/*/Database/Migrations`.
4. Tên index MySQL tối đa 64 ký tự — đặt tên thủ công.
5. Không dùng `mysql2` / `DB_CONNECTION_SECOND` trên `gop_db`.
6. Quyền ERP guard `web` ≠ guard `api` mặc định → dùng trait `ChecksEmployeePermission`,
   không dùng `hasPermissionTo()`.
7. Route tĩnh phải khai TRƯỚC `/{id}`.
8. `ApiController` không có `$this->validate()` → dùng FormRequest.
9. `responseJson` chỉ nhận 3 tham số → gói `total` vào trong payload `data`.
10. HRM không có `formatQuantity` → `formatCurrency($x, 3)`.
11. `V2BaseButton` không có prop `disabled`, dùng `:interactable`.
12. `V2BaseCheckbox` dùng slot sẽ mất checkbox ở chế độ đơn → dùng prop `label`.
13. `text-muted` bị ép thành đỏ → dùng `.text-soft`.
14. Bộ lọc V2 không dùng option "Tất cả", dùng placeholder.
15. Đọc DOM trên trình duyệt phải đợi Nuxt nạp xong chunk.
16. Windows: không `taskkill` theo tên tiến trình, không xóa bằng wildcard, không `sed -i` hàng loạt.
17. **`$request->get()` KHÔNG đọc được body JSON** — đó là API của Symfony, chỉ đọc query string và
    POST form params. Payload của FE là JSON nên phải dùng `$request->input()`. Đã dính thật ở
    `reject()`: lý do không duyệt lưu vào DB thành chuỗi rỗng. Toàn bộ file của feature này đã đổi
    sang `input()`.
18. **KHÔNG viết script sửa hàng loạt bằng `preg_replace` rồi `file_put_contents` thẳng.**
    Regex sai → `preg_replace` trả `null` → ghi đè file thành RỖNG. Đã mất trắng 2 service và phải
    dựng lại. Nếu buộc phải làm script, luôn có chốt: kiểm nội dung mới khác rỗng / dài hơn nội
    dung cũ TRƯỚC khi ghi. Sửa vài chỗ thì dùng thẳng công cụ sửa file.

---

## Bàn giao — việc còn lại

### Cần chạy khi deploy

```bash
cd hrm-api && php artisan migrate
# 2 migration: 2026_08_15_000002 (prepick_cancel_request_history)
#              2026_08_15_000003 (prepick_cancel_history)
```

Không cần seed quyền: dùng lại 4 quyền ERP đã có (`Quản lý giữ hàng` 100427 + 3 quyền
`Xem phiếu hàng giữ theo ...` 100839-100841).

### Chưa làm — cần user/QA

- Bấm tay trên trình duyệt: 8 bộ lọc · 2 cột sắp xếp · phân trang · giữ bộ lọc khi quay lại ·
  popup chọn hàng · popup chọn phiếu yêu cầu · cấu hình cột · 4 bản in
- Đối chiếu 2 cổng trên dev: phiếu tạo ở HRM hiện đúng ở ERP và ngược lại
- **Mở modal "Lịch sử giữ hàng" bên ERP** xem có dựng được link tới phiếu hủy do HRM tạo không
  (đã verify `objectable_type` ghi đúng chuỗi `App\Model\Warehouse\PrepickCancel`, nhưng chưa chạy
  2 cổng song song để nhìn tận mắt)
- Test bằng tài khoản có `Quản lý giữ hàng` nhưng **KHÔNG** phải Super admin (đợt verify dùng
  NV #13 là Super admin làm người duyệt)
- SRS + testcase + HDSD

### Dọn dẹp

6 bảng sao lưu vẫn còn trên DB local, **cố ý giữ lại** làm lưới an toàn cho tới khi user test xong:

```sql
DROP TABLE bak_prepick_cancel_requests_20260815;
DROP TABLE bak_prepick_cancel_request_details_20260815;
DROP TABLE bak_prepick_cancels_20260815;
DROP TABLE bak_prepick_cancel_details_20260815;
DROP TABLE bak_prepick_details_20260815;
DROP TABLE bak_prepick_logs_20260815;
```

### Khác ERP có chủ ý (ngoài 13 lỗi đã liệt kê ở design.md)

| # | Khác biệt | Lý do |
|---:|---|---|
| 1 | Danh sách yêu cầu có **3 preset tab** thay vì 2 route riêng (`index` / `forAccounting`) | Gộp về 1 mục menu, đúng cách đã làm ở màn nhập thẳng |
| 2 | `waiting_approve` với người không có quyền trả **rỗng** thay vì rơi về "phiếu của tôi" | Trả rỗng đúng nghĩa "màn chờ duyệt của bạn trống" hơn là trả nhầm danh sách khác |
| 3 | Danh sách **phiếu hủy** siết theo 3 cấp quyền | ERP cho mọi người trong công ty xem hết mọi phiếu hủy — rò dữ liệu |
| 4 | ĐVT trên form **bỏ hẳn ô chọn**, chỉ hiện chữ | `prepick_details` không có `unit_id`; ERP có ô nhưng đã `disabled` sẵn |
| 5 | Popup chọn hàng hiển thị **`available_qty`** (đã trừ ĐN xuất kho chưa xong) thay vì `SUM(qty)` thô | Để khớp cột "Có thể hủy" trên form (lỗi #7) |
| 6 | Lô tồn tra theo **công ty của người lập YÊU CẦU**, không phải công ty người duyệt | ERP dùng công ty kế toán nên 2 người khác công ty là trừ hụt im lặng |
| 7 | Mẫu in dựng trong code HRM, **không ghi vào `report_templates`** | Bảng dùng chung với ERP — tránh đụng dữ liệu ERP |
| 8 | Bỏ 2 bộ lọc chết + 1 trường hiển thị chết ở màn phiếu hủy | Lỗi #10, #11 |
| 9 | Không có nút "Thêm" rời ở danh sách phiếu hủy | Lỗi #9 (ERP trỏ nhầm sang màn Tạo yêu cầu nhập hàng) |
| 10 | Nút Duyệt kèm hộp xác nhận nêu rõ "sẽ trừ tồn giữ, không hoàn tác được" | Thao tác không đảo ngược được |

---

## Phase — Bỏ "Không duyệt" khỏi màn danh sách (2026-08-24)

Đồng bộ quy tắc mới ở `.claude/skills/list-page/SKILL.md` mục 1. ⚠️ Khác 2 màn phiếu thu/chi:
ở đây "Không duyệt" mở `RejectModal` NGAY TẠI DANH SÁCH → bỏ nút thì gỡ luôn modal khỏi màn danh
sách. Đã xác nhận màn chi tiết (`components/PrepickCancelRequestForm.vue` chế độ `show`) có sẵn
nút "Không duyệt" ở `V2Footer` + `RejectModal` riêng nên không mất chức năng.

- [x] Xóa action `key: 'reject'` + `case 'reject'` trong `pages/finance/prepick-cancel-requests/index.vue`
- [x] Gỡ phần `RejectModal` chỉ còn phục vụ nút vừa bỏ: block template, import, khai `components`,
      state `rejectItem`, handler `handleRejected`

### Checkpoint — 2026-08-24
Vừa hoàn thành: bỏ "Không duyệt" + gỡ `RejectModal` khỏi màn danh sách Yêu cầu hủy hàng giữ
(file `components/RejectModal.vue` GIỮ NGUYÊN — màn chi tiết vẫn import).
Đang làm dở: không.
Bước tiếp theo: user xác nhận trên trình duyệt, đặc biệt luồng Không duyệt ở màn chi tiết.
Chưa kiểm chứng bằng mắt: chỉ parse template + script.
Blocked: không.

---


## Đợt vá Redmine 24/08/2026 (#11192–#11197) — nhánh `gop_db`

QA (Lê Huyền Trang) test màn Yêu cầu hủy hàng giữ trên `hrm-crm`, 5 issue:

| Issue | Nội dung | Xử lý |
|---|---|---|
| #11192 | Lưu nháp / Lưu và gửi duyệt / Không duyệt đều ra màn Chi tiết | `save()` + `onRejected()` push về **danh sách** |
| #11192 | Nhập quá "Có thể hủy" bị tự kéo về trần + toast | Bỏ tự sửa số; `qtyErrorOf()` + `validateProducts()` báo đỏ ngay dưới ô, chưa sạch lỗi thì không gọi API |
| #11192 | "Thiếu bộ lọc so với ERP" | **Không phải lỗi code**: 8 ô lọc vẫn khai đủ, tài khoản test đã tắt `org` / `created_by` / `approver` / `startDate` trong popup "Cài đặt bộ lọc" (`filter_customizations` id 7, user 13) → bật lại trong popup là hiện |
| #11193 | Bấm "Quay lại" ở màn Lập phiếu hủy → không thấy bản ghi | `url-back` động: vào từ `?request_id=` thì quay về **chi tiết phiếu yêu cầu**; ô tìm nhanh màn Phiếu hủy tìm thêm theo mã phiếu yêu cầu (`PYCHHG-…`) |
| #11195 | Excel danh sách thiếu khối ký | `addSignatureBlock()` — "Ngày…Tháng…Năm…" + "Người lập (Ký, họ tên)", canh giữa 3 cột cuối, không kẻ khung |
| #11196 | Nút In màu teal | Bỏ cờ `menu.print`, dựng lại nút In `secondary` ở slot `#custom-actions` (giống màn phiếu hủy) |
| #11197 | Bỏ tick "Cần hủy" nhưng lưu vẫn ghi nhận hàng hóa | **Khác ERP có chủ ý**: bỏ tick = bỏ hàng hoá khỏi phiếu — FE lọc trước khi gửi, BE `normalizeProducts()` bỏ dòng `need_cancel = false`; màn Chi tiết chỉ hiện dòng `need_cancel` (phiếu cũ do ERP lập có dòng bỏ tick) |
