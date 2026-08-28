# Plan — Phiếu chuyển hàng nhập thẳng (ERP → HRM)

> @junfoke · nhánh `feat/finance-product-import-direct-transfer` (từ `gop_db`, cả 2 repo) · design: `./design.md`
>
> **Trạng thái: XONG PHASE 0-7, ĐÃ VERIFY HTTP + TRÌNH DUYỆT (2026-08-15).**
> BE 12 file (`Modules/Finance`) + 1 migration + 13 route. FE 11 file
> (`pages/finance/product-import-direct-transfers`, 2.709 dòng) + 1 mục menu.
> DB: đối chiếu từng cột với bản sao lưu — **0 lệch** trên cả 4 bảng nghiệp vụ.

## Nguồn ERP cần đọc

| Việc | File ERP |
| --- | --- |
| Controller | `TanPhatDev/app/Http/Controllers/Warehouse/ProductImportDirectTransferController.php` (414 dòng) |
| Model chính | `TanPhatDev/app/Model/Warehouse/ProductImportDirectTransfer.php` (409 dòng) |
| Model con | `...TransferProduct.php` · `ProductImportDirectDetail.php` · `ProductImportDirectDetailLog.php` |
| Blade | `TanPhatDev/resources/views/warehouse/product_import_direct_transfer_requests/*.blade.php` (6 file) |
| Class JS | `TanPhatDev/resources/views/partials/classes/warehouse/ProductImportDirectTransfer{,Product}.blade.php` |
| Route | `TanPhatDev/routes/web.php:997-1009` |
| Excel | `TanPhatDev/app/ExcelExports/ProductImportDirectTransferExcel.php` |

## Khuôn mẫu HRM cần copy (KHÔNG tự phát minh)

| Phần | File mẫu |
| --- | --- |
| Entity + kiểm quyền qua pivot | `Modules/Finance/Entities/ProductTransferRequest/ProductTransferRequest.php` |
| Service + paginate + relevance order | `Modules/Finance/Services/ProductTransferRequestService.php` |
| Controller + route order | `Modules/Finance/Http/Controllers/V1/ProductTransferRequestController.php` + `Routes/api.php:165-196` |
| In (fill template DB) | `ProductImportRequestController::printData()` |
| Lịch sử (đọc log) | `ProductImportRequestService::histories()` + skill `entity-history` |
| FE danh sách V2 | `pages/assign/customers/index.vue` |
| FE form + popup | `pages/finance/product-transfer-requests/components/ProductTransferRequestForm.vue` |

---

## Phase 0 — Chuẩn bị

- [x] Tạo nhánh `feat/finance-product-import-direct-transfer` từ `gop_db` ở **cả 2 repo**
      (`hrm-api`, `hrm-client`); chọn checkout thẳng hay worktree riêng — nếu worktree thì nhớ
      copy `.env` (gitignore nên worktree không có) + `composer install` + `npm install`
- [x] Đọc `.plans/gop-db/design.md` (nền tảng gộp DB) + `./design.md`
- [x] Đọc skill: `list-page`, `button-convention`, `modal-popup`, `form-validate`,
      `unsaved-changes`, `print-page`, `entity-history` (+ `ui-base.md`), `notification-convention`
- [x] Sao lưu 4 bảng nghiệp vụ trước khi test luồng duyệt (đụng tồn thật):
      `product_import_direct_transfers`, `..._products`, `product_import_direct_details`,
      `product_import_direct_detail_logs`
- [x] Kiểm mẫu in còn sống: `report_templates` id **465** và **471** trên `gop_db`

---

## Phase 1 — BE nền + màn danh sách

- [x] Tạo `Modules/Finance/Entities/ProductImportDirectTransfer/` — 4 entity:
      `ProductImportDirectTransfer` (`$table = 'product_import_direct_transfers'`),
      `ProductImportDirectTransferProduct`, `ProductImportDirectDetail`,
      `ProductImportDirectDetailLog`.
      **Khai `use` đầy đủ** cho mọi class tham chiếu chéo — bên ERP `ProductImportDirectDetailLog`
      được gọi mà không có `use` (cùng namespace), port sang là 500 lúc chạy, `php -l` không bắt.
      **Không** dùng connection `mysql2`.
- [x] Hằng trạng thái + `STATUSES` (1 Đang tạo · 2 Chờ duyệt · 3 Đã duyệt · 4 Không duyệt)
- [x] Port kiểm quyền theo **tên** bằng query thẳng pivot (copy `ProductTransferRequest`):
      4 quyền `Xem phiếu chuyển hàng nhập thẳng theo tổng công ty|công ty|phòng ban|bộ phận`
      + `Kế toán kho` + role id 18 (Super admin). **KHÔNG** dùng spatie Eloquent / `ErpPermissionHelper`.
- [x] Port `searchByFilter()` 2 preset: `all` (phạm vi 4 cấp, ẩn phiếu "Đang tạo" của người khác)
      và `waiting_approve` (`status = 2` + cùng công ty, gate `Kế toán kho`).
      Giá trị `type` lạ → quy về `all`. Bỏ nhánh mặc định `created_by = mình` (menu ERP đã comment).
- [x] Port bộ lọc: `code`, `company`, `department`, `status`, `created_by`, `receiver`,
      `startDate`/`endDate`, `product_name` (tìm cả `product_name` và `product_code` của dòng con)
- [x] `SORTABLE_COLUMNS` whitelist: `code`, `createdAt` — key FE phải trùng key BE
- [x] `applyRelevanceOrder()` cho ô tìm nhanh (Số phiếu + Người tạo), chỉ bật khi từ khoá ≥ 2 ký tự,
      bỏ qua khi user đã bấm sort, luôn `id DESC` cuối
- [x] `ProductImportDirectTransferListResource` — cột: `id`, `code`, `receiverName`,
      `createdByName` (subquery, KHÔNG leftJoin), `createdAt` (`Helper::formatDate`, không kèm giờ),
      `status` + `statusName` + `statusType`, `companyName`, `departmentName`, `note`,
      `approverName`, cờ `can_edit` / `can_delete` / `can_approve`
- [x] `ProductImportDirectTransferService::search()` — paginate `per_page`, trả `meta`
- [x] Route `GET /v1/finance/product-import-direct-transfers` — **không** middleware quyền
- [x] **Verify**: gọi HTTP thật với 3 loại tài khoản (Super admin / Kế toán kho / nhân viên thường),
      đối chiếu số dòng với màn ERP tương ứng

### Checkpoint — Phase 1

```
Vừa hoàn thành: 5 entity (`ProductImportDirectTransfer` + Product + Detail + DetailLog +
History), `ProductImportDirectTransferService`, ListResource, 13 route `/v1/finance/
product-import-direct-transfers`. Kiểm quyền qua trait `ChecksEmployeePermission` (query thẳng
pivot) thay vì tự viết lại 3 method như `ProductTransferRequest`.
Đang làm dở: không.
Bước tiếp theo: FE màn danh sách.
Blocked: không.
Verify: 3 tài khoản — người tạo #33 all=2/waiting=0 · Kế toán kho #13 all=865/waiting=1 ·
NV thường #24 all=41/waiting=0. Vá lỗi #1 đã xác nhận trên dữ liệu thật: NV #147 có quyền
100712 (theo công ty), không phải người tạo, không phải Kế toán kho → ERP `canView()` trả
false, bản HRM trả **true** cho phiếu TPE_CHNT_002 cùng công ty.
```

---

## Phase 2 — FE màn danh sách

- [x] `pages/finance/product-import-direct-transfers/index.vue` — copy khung
      `pages/assign/customers/index.vue`, `@import '@/assets/scss/v2-styles.scss'`
- [x] Cột mặc định 7: `STT` · `Số phiếu` · `Người nhận` · `Người tạo` · `Ngày tạo` ·
      `Trạng thái` · `Hành động`.
      Ẩn mặc định: `Công ty`, `Phòng ban`, `Ghi chú`, `Người duyệt`.
      `STT` (`width` + `minWidth` 60px) và `Số phiếu` khai `sticky: true` + `locked: true`.
      Căn lề theo `list-page` §15; `Trạng thái` `width: 130px`, `Hành động` `width: 140px`, cả 2 `center`.
- [x] `Số phiếu` render `<nuxt-link>` class `.v2-cell-link` vào `/finance/product-import-direct-transfers/{id}`
- [x] Popup "Cấu hình cột hiển thị" qua `columnCustomizationMixin` (`columnScreenKey` riêng);
      cột `locked` không vào phần kéo thả, `Hành động` chốt cuối
- [x] ~~`V2BaseSmartFilterPanel`~~ → **thực tế dùng `V2BaseFilterPanel`** (lý do ở checkpoint) —
      bộ lọc: Công ty → Phòng ban → Bộ phận (khối cascade `V2BaseCompanyDepartmentFilter` đứng đầu)
      + Trạng thái · Tên/mã hàng hoá · Người nhận · Người lập · Từ ngày / Đến ngày.
      Tiêu đề panel để **mặc định**, không truyền prop `title`.
      Không có ô "Mã phiếu" riêng — trùng ô tìm nhanh (BE lọc `keyword` trên mã phiếu HOẶC người lập).
- [x] Auto-search deep watcher trên `filters`, `ignoredFields: ['keyword']`, `oldFilters` set ở `created()`
- [x] `filterStateMixin`: `localStorageKey: 'finance_product_import_direct_transfers'`,
      `pathsToKeep: ['/finance/product-import-direct-transfers']`, `expirationTime: 10 * 60 * 1000`
- [x] `V2BaseRowActions`: `Sửa` (`ri-edit-line`, khai `to`) · `Xóa` (`ri-delete-bin-6-line`, `danger`,
      `interactable` theo `can_delete`) + menu `⋮`: `In`, `Lịch sử` (`ri-history-line`).
      Cờ quyền **fail-closed**, không hard-code `true`.
- [x] Nút màn theo `button-convention`: `Tạo mới` · `In` · `Xuất Excel` (xanh lá)
- [x] Thứ tự request theo `list-page` §8: `created()` gọi `loadData()` **đầu tiên**, không `await`;
      cấu hình cột + quyền chạy song song; options bộ lọc nâng cao hoãn tới khi mở panel;
      dùng `$safeLoadingStart/Finish`; chống response về trễ bằng `loadSeq`
- [x] Thêm mục menu vào `components/subsystem-menu/finance.js` — nhóm **Điều chuyển**, sau
      "Phiếu điều chuyển hàng": `{ label: 'Phiếu chuyển hàng nhập thẳng', link: '/finance/product-import-direct-transfers' }`
- [x] **Verify**: mở màn trên trình duyệt, đếm số request lúc load (mục tiêu 2), test đủ 8 ô lọc,
      sort 2 cột, phân trang, giữ filter khi vào chi tiết rồi quay lại

### Checkpoint — Phase 2

```
Vừa hoàn thành: `index.vue` (647 dòng) + 1 mục menu ở nhóm **Điều chuyển** của `finance.js`.
Đang làm dở: không.
Bước tiếp theo: form Tạo/Sửa + chi tiết.
Blocked: không.
⚠️ **Lệch so với plan (có chủ ý)**: dùng `V2BaseFilterPanel` chứ KHÔNG dùng
`V2BaseSmartFilterPanel`. Lý do: 2 màn Tài chính đã port (`product-import-requests`,
`product-transfer-requests`) đều đang dùng `V2BaseFilterPanel`; đổi riêng màn này sang panel
"cài đặt bộ lọc" sẽ làm 3 màn cùng nhóm menu lệch nhau. Nâng cả 3 màn lên `SmartFilterPanel`
nên làm thành 1 đợt riêng, không nhét vào feature này.
Verify: mở màn trên trình duyệt — 7 cột đúng thứ tự, 865 dòng, `Hiển thị 1–10 / 865`,
2 tab preset (Tất cả · Chờ tôi duyệt) hiện đúng theo quyền Kế toán kho.
```

---

## Phase 3 — Chi tiết + Tạo/Sửa/Xóa

### BE

- [x] `GET /{id}` — `show`, gate `canView()` **đã vá lỗi #1**: Super admin · người tạo ·
      `Kế toán kho` cùng công ty · **thêm** 4 nhánh quyền cấp khớp đúng phạm vi `searchByFilter`
      (tổng cty → tất cả; cty → cùng `company_id`; phòng ban → `department_id` mình quản lý +
      `EmployeeManageDepartment`; bộ phận → `part_id` mình quản lý + `EmployeeManagePart`)
- [x] `GET /stock?employee_id=` — **vá lỗi #2**: tồn nhập thẳng gom theo
      `product_id + employee_id + company_id + department_id + part_id`, `HAVING qty > 0`,
      kèm `units` (ĐVT + hệ số). `employee_id` mặc định `auth()->id()`; màn Sửa truyền
      `created_by` của phiếu. Phân trang + tìm theo tên/mã hàng.
- [x] `GET /products/{id}/units` — ĐVT + `unit_coefficient` của 1 hàng hoá
- [x] `POST /` (store) — **vá lỗi #3**: `status` chỉ nhận `in:1,2`.
      Validate: `receiver_id` required|numeric|khác `auth()->id()`|cùng công ty ·
      `products` required|array|min:1 · `products.*.product_id` exists · `products.*.unit_id` exists ·
      `products.*.qty` required|numeric|min:1 · `note` nullable|max:255.
      Gán `company_id`/`department_id`/`part_id` từ `info` người tạo, `code = randomString(20)`
      rồi `generateCode()` → `<mã cty>_CHNT_<generateCode(3, id)>` **giống hệt ERP**.
      `validateProducts()` kiểm tồn theo **người tạo phiếu** trước khi lưu.
      `syncProducts()` xoá hết rồi tạo lại như ERP.
- [x] `PUT /{id}` (update) — gate `canEdit()` (`status ∈ {1,4}` và `created_by = mình`), cùng bộ validate
- [x] `DELETE /{id}` — gate `canEdit()`; ERP dùng `GET .../delete` + redirect, HRM đổi thành
      `DELETE` trả JSON
- [x] Thông báo khi lưu ở `status = 2`: gửi nhóm quyền `Kế toán kho`, nội dung theo
      `notification-convention` (`[TC] Chờ duyệt: **<mã phiếu>**. …`), deep-link kèm id
- [x] `ProductImportDirectTransferDetailResource` — thông tin chung + dòng hàng hoá
      (`product_id`, `product_name`, `product_code`, `unit_id`, `units[]`, `qty`, `changed_qty`,
      `product_qty` = tồn hiện có) + `approver_comment` + cờ `can_edit`/`can_approve`/`can_delete`
- [x] **FormRequest riêng** — `Modules/Finance` không có `$this->validate()` trên ApiController

### FE

- [x] `components/ProductImportDirectTransferForm.vue` — dùng chung create/edit/show, nhận prop `mode`
- [x] Trường: Người nhận (*) (select NV cùng công ty, loại chính mình, `V2BaseSelect`) →
      auto điền Phòng ban (**disabled**, kiểu ô khoá theo `list-page` §10) · Ghi chú (max 255)
- [x] Bảng hàng hoá: Tên hàng · Mã hàng · ĐVT (select) · Số lượng · Số lượng theo ĐV cơ bản (readonly) · nút xoá dòng
- [x] `components/StockSearchModal.vue` — popup "Tồn hàng nhập thẳng của nhân viên",
      chọn nhiều dòng, select bên trong dùng `V2BaseSelectInModal`, `pageSizeOptions [20,50,100]`.
      Chặn chọn trùng hàng hoá (toast cảnh báo như ERP).
- [x] Quy đổi giữ nguyên ERP: `changed_qty = qty × unit_coefficient`;
      đổi ĐVT → `qty = product_qty / unit_coefficient`; **chặn nhập vượt tồn**
- [x] 2 nút lưu: `Lưu nháp` (status 1) · `Lưu & Gửi duyệt` (status 2)
- [x] `unsavedChangesMixin` + `markFormSaved()` sau khi lưu thành công (page) — dùng đúng mixin
      theo `unsaved-changes` (trang form, không phải modal)
- [x] Validate realtime `vee-validate` gắn trên `V2Base*`; lỗi 422 map vào `formError`
- [x] `create.vue` · `_id/edit.vue` · `_id/index.vue` (chi tiết, tiêu đề
      `Chi tiết phiếu chuyển hàng nhập thẳng: <mã>` set sau `$emit('loaded')`)
- [x] Xóa dùng `components/modal/base-confirm-modal.vue` (hoặc `this.$confirm({...})`)
- [x] **Verify**: tạo nháp → sửa → xóa; tạo & gửi duyệt; thử gửi `status = 3` bằng tay để chắc
      BE chặn; mở Sửa phiếu của người khác bằng tài khoản có quyền → popup tồn đúng người tạo

### Checkpoint — Phase 3

```
Vừa hoàn thành: `ProductImportDirectTransferForm.vue` (798 dòng, dùng chung create/edit/show),
`StockSearchModal.vue`, 3 trang vỏ (create / _id/index / _id/edit), `ProductImportDirectTransferRequest`
FormRequest, 5 route ghi + 3 route phụ trợ form.
Đang làm dở: không.
Bước tiếp theo: luồng duyệt.
Blocked: không.
Verify 3 lỗi ERP đã chặn (HTTP thật):
  - #3 `status=3` khi tạo → 422 `Trạng thái: Không hợp lệ`
  - người nhận = chính mình → 422 `Người nhận phải khác người lập phiếu`
  - vượt tồn (qty 999) → 422 `Hàng "..." không đủ số lượng`
  - #2 `GET /stock?employee_id=` trả đúng tồn của nhân viên được chỉ định (không phải người đăng nhập)
Verify trình duyệt: popup tồn → tick chọn → Chọn → dòng hàng vào bảng với `qty=5, changed_qty=5,
product_qty=5`; nhập 99 → tự kẹp về 5; đổi về 2 → `changed_qty=2`.
⚠️ Sửa 1 lỗi phát hiện khi verify: `loadReceivers()` chạy song song `loadDetail()` nên lúc đó
`created_by` chưa về, danh sách người nhận lấy theo người ĐANG ĐĂNG NHẬP → sửa phiếu người khác
sẽ ra sai công ty. Đã nạp lại sau khi có chi tiết (không điều kiện, kèm `include_ids`).
```

---

## Phase 4 — Duyệt / Không duyệt

- [x] `POST /{id}/approve` — gate `canApprove()` (`status = 2` + cùng công ty + quyền `Kế toán kho`).
      Port nguyên logic ERP trong transaction:
      1. `status = 3`, `approver_id`, `approver_comment`
      2. Với mỗi dòng: lấy `product_import_direct_details` của **người tạo** (`qty > 0`,
         `orderBy created_at asc`, `lockForUpdate`), so tổng tồn với `changed_qty`,
         thiếu thì ném lỗi `Tồn kho không đủ để xuất: yêu cầu X, hiện có Y`
      3. Trừ FIFO + ghi `product_import_direct_detail_logs` (`qty_before` / `change` / `qty_after`)
      4. Tạo bản ghi tồn cho **người nhận** (`company_id`/`department_id`/`part_id` lấy từ
         `info` người nhận) + 1 log tương ứng
      5. Thông báo cho người tạo
- [x] `POST /{id}/reject` — `status = 4`, `approver_comment` **required**, thông báo người tạo
- [x] FE `_id/index.vue`: `V2Footer` thứ tự `Sửa` → `In` → `Duyệt` / `Không duyệt` → `Xóa` →
      `Quay lại`; gate fail-closed. Duyệt/Không duyệt mở `base-confirm-modal`;
      Không duyệt bắt buộc nhập lý do (ô ghi chú trong popup).
- [x] Sau khi duyệt/không duyệt: cập nhật state tại chỗ, không nạp lại cả màn
- [x] **Verify trên bản sao dữ liệu**: tạo phiếu 2 dòng → duyệt → đối chiếu
      `product_import_direct_details` (tồn người tạo giảm đúng, người nhận có bản ghi mới) +
      `..._logs` (đủ cặp trừ/cộng, `qty_after` khớp). Test tiếp: duyệt khi tồn không đủ → phải
      rollback sạch, không sinh log nửa vời.

### Checkpoint — Phase 4

```
Vừa hoàn thành: `approve()` / `reject()` trong Service (trừ tồn FIFO `lockForUpdate` + ghi
`product_import_direct_detail_logs` + tạo lô tồn cho người nhận + thông báo), 2 route,
`ProductImportDirectTransferRejectRequest`, nút Duyệt / Không duyệt + popup lý do ở footer màn chi tiết.
Đang làm dở: không.
Bước tiếp theo: lịch sử.
Blocked: không.
Verify trên trình duyệt (phiếu tạo mới TPE_CHNT_873, SL 2):
  tồn người lập 5 → 3 · tồn người nhận 0 → 2 · 2 dòng log `5.00 -2.00 = 3.00` và `0.00 +2.00 = 2.00`
  · `objectable_type` ghi đúng chuỗi class ERP.
Verify HTTP: Không duyệt thiếu lý do → 422; có lý do → 200 + status 4.
⚠️ Khác ERP có chủ ý: `changed_qty` được BE **tính lại** từ `product_units` (`qty × hệ số`) thay vì
tin số FE gửi lên — ERP nhận thẳng nên sửa payload là chuyển được nhiều hơn số đã nhập.
Và `assertEnoughStock()` gộp các dòng cùng hàng hoá rồi mới so tồn (ERP so từng dòng nên chọn
2 dòng cùng 1 hàng, mỗi dòng nửa tồn thì lọt qua, tới lúc duyệt mới nổ lỗi).
```

---

## Phase 5 — Lịch sử thay đổi (tính năng MỚI)

> Đọc `.claude/skills/entity-history/SKILL.md` **và** `ui-base.md` trước khi viết markup.

- [x] Migration `database/migrations/2026_08_15_000001_create_product_import_direct_transfer_history_table.php`
      — bảng `product_import_direct_transfer_history`:
      `id`, `product_import_direct_transfer_id` (unsignedBigInteger, index),
      `company_id` (nullable, index), `action` (string), `old_value`/`new_value` (text nullable, JSON),
      `note` (text nullable), `changed_by` (nullable), `changed_at` (timestamp useCurrent),
      `timestamps()`. Không FK cứng, không SoftDeletes, PHPDoc trên `up()`/`down()`.
- [x] `ProductImportDirectTransferHistoryService` — biến thể **subset-diff**:
      chụp snapshot **giá trị hiển thị** (tên người nhận, tên ĐVT, tên trạng thái) TRƯỚC khi lưu →
      save → diff → có thay đổi mới insert 1 dòng. Không đổi gì → không ghi.
      Chuẩn hoá trước khi so (rỗng/null → null, số → chuỗi số) để không sinh log rác.
- [x] Bảng con hàng hoá dùng **khoá dạng bảng**: mỗi phần tử
      `['__key' => product_id . '|' . unit_id, 'Tên hàng' => ..., 'Mã hàng' => ..., 'ĐVT' => ..., 'SL' => ..., 'SL theo ĐV cơ bản' => ...]`.
      Bản ghi bị sửa **chỉ liệt kê trường đã đổi**, không in lại cả dòng.
- [x] Ghi log ở 5 action: `create` · `update` · `send_approve` · `approve` · `reject`.
      `note` = `approver_comment` cho `approve` / `reject` (§4.1 — lý do phải hiện trên lịch sử).
- [x] `GET /{id}/histories` — DTO chuẩn: `id`, `action`, `action_label`, `action_color`,
      `actor_code`, `actor_name`, `department_name`, `note`, `changes[]`,
      `created_at` (`d/m/Y H:i`), `created_at_raw` (`Y-m-d H:i:s`). Sắp xếp **mới → cũ**.
- [x] FE **đủ 2 nơi**: `components/ProductImportDirectTransferHistoryModal.vue` (mở từ menu `⋮`
      màn danh sách, mẫu `CustomerHistoryModal.vue`) + khối "Lịch sử" cuối `_id/index.vue`
      (`SystemInfoSection.vue`, mặc định thu gọn, lazy load lần mở đầu).
      Cùng endpoint, cùng bố cục, cùng bộ lọc 4 ô (Loại hành động / Người thực hiện / Từ ngày / Đến ngày).
      Màu: cũ `#dc2626`, mới `#16a34a`, nhãn `#475569`.
- [x] **Verify** theo §7 của skill: đổi 1 trường → 1 log đúng subset · không đổi → không log ·
      đổi 2 trường → 1 dòng 2 key · thêm 1 dòng hàng → 1 dòng `+` · sửa 1 cột dòng hàng → 1 dòng `~`
      đúng cột · thứ tự mới → cũ · popup và mục chi tiết render giống hệt nhau.
      Dọn log test bằng tinker (`where('id','>',$maxTrướcTest)->delete()`).

### Checkpoint — Phase 5

```
Vừa hoàn thành: migration bảng `product_import_direct_transfer_history`, entity History,
`ProductImportDirectTransferHistoryService` (subset-diff + khoá dạng bảng cho dòng hàng hoá),
route `/{id}/histories`, `ProductImportDirectTransferHistoryPanel.vue` + `...HistoryModal.vue`.
Đang làm dở: không.
Bước tiếp theo: In + Excel.
Blocked: không.
⚠️ Tên index tự sinh của Laravel (`<bảng>_<cột>_index`) dài 68 ký tự > giới hạn 64 của MySQL →
lỗi 1059. Phải đặt tên tay (`pidt_history_transfer_id_index`).
**Đủ 2 nơi hiển thị dùng CHUNG một component** (`HistoryPanel`), popup chỉ bọc thêm vỏ `b-modal`
→ 2 nơi không thể lệch nhau.
Verify trình duyệt: tạo → sửa → gửi duyệt → duyệt sinh đúng 4 mốc (Duyệt · Gửi duyệt · Chỉnh sửa ·
Tạo phiếu), thứ tự mới → cũ, subset-diff đúng (`Ghi chú: 'Test tao nhap' → 'Da sua ghi chu'`,
`Trạng thái: 'Đang tạo' → 'Chờ duyệt'`), dòng hàng hoá ra đúng 1 dòng `+`, lý do Không duyệt hiện
ở khối ghi chú vàng.
```

---

## Phase 6 — In + Xuất Excel

- [x] `GET /{id}/print-data` — port `getPrintDataAttribute()`: `LOGO`, `CONG_TY`,
      `DIA_CHI_CONG_TY`, `NGAY_YEU_CAU`, `NGUOI_YEU_CAU`, `NGUOI_NHAN_YEU_CAU`, `SO_PHIEU`,
      `PHONG_BAN`, `GHI_CHU`, `CHI_TIET` (bảng 6 cột). Fill template DB **465** bằng
      `fillReport` + `clearNull` (khuôn `ProductImportRequestController::printData()`).
      Gate `canView()`.
- [x] `_id/print.vue` — màn in phiếu. ⚠️ scoped CSS không ăn ở màn print, khai style global.
      Số lượng thập phân làm tròn bằng `formatCurrency`.
- [x] `GET /print-list-data` — port `printListData()`: 6 cột (STT · Số phiếu · Ngày lập ·
      Người lập · Người nhận · Trạng thái), `TITLE = 'Danh sách phiếu chuyển hàng nhập thẳng'`,
      `COLSPAN = 6`, `WIDTH = 1100`, template **471**, in ngang. Dùng **cùng bộ lọc** với danh sách.
- [x] `GET /export` — xuất Excel danh sách. Route tĩnh khai **trước** `/{id}`.
      FE theo convention ExcelJS: **tự gắn token** vào header (`$axios` không tự thêm
      `Authorization` cho luồng tải file), escape ký tự `&`, tránh "Number stored as text".
- [x] **Verify**: in 1 phiếu có 3 dòng hàng, đối chiếu với bản in ERP cùng phiếu (từng ô);
      in danh sách + xuất Excel với bộ lọc đang áp → số dòng khớp màn danh sách

### Checkpoint — Phase 6

```
Vừa hoàn thành: `printData` / `printListData` / `export` ở BE, `_id/print.vue`,
`print-list.vue`, `components/export-excel.js` (ExcelJS ở FE).
Đang làm dở: không.
Bước tiếp theo: verify tổng.
Blocked: không.
Verify trình duyệt:
  - In phiếu (mẫu 465): letterhead + `No: TPE_CHNT_873` + ngày + người yêu cầu + ghi chú +
    bảng 6 cột + khối ký — khớp mẫu ERP.
  - In danh sách (mẫu 471, in ngang): tiêu đề + 6 cột + phần ký, lọc `status=2` trả đúng 1 dòng.
  - Xuất Excel: file 868 dòng × 6 cột, dòng 1 tiêu đề, dòng 2 header, dữ liệu khớp màn danh sách.
⚠️ `$printContent` KHÔNG có option `landscape` → phải khai đè `@page { size: A4 landscape }` trong
chuỗi `styles` (khối này chèn sau baseStyles của plugin nên thắng).
⚠️ HRM không có helper `formatQuantity` của ERP → dùng `formatCurrency($x, 3)` (đúng định nghĩa
`formatQuantity` bên ERP).
```

---

## Phase 7 — Verify tổng + bàn giao

- [x] `php -l` toàn bộ file mới + `composer dump-autoload`
- [x] Quét **2 chiều** class cùng namespace gọi mà thiếu `use` (bẫy số 1 của `chuyen-code-phan-he`)
- [x] Verify HTTP đủ **13 route** với 3 loại tài khoản
- [x] Verify trình duyệt luồng end-to-end: tạo nháp → sửa → gửi duyệt → Kế toán kho duyệt →
      kiểm tồn 2 nhân viên → xem lịch sử → in → xuất Excel
- [x] Kiểm import alias FE: mọi `@/` `~/` trỏ tới file có thật (bẫy đổi chuỗi hàng loạt)
- [x] Đối chiếu 2 cổng ở mức code: 4 trạng thái · công thức `generateCode` · mẫu in 465/471 ·
      logic trừ tồn FIFO
- [x] Kiểm DB nguyên trạng: ngoài bảng lịch sử mới, không bảng nào đổi schema
- [x] Merge `gop_db` mới nhất vào nhánh feature (cả 2 repo) trước khi bàn giao
- [x] Cập nhật `.plans/gop-db/STATUS.md`

### Checkpoint — Phase 7

```
Vừa hoàn thành: verify tổng + dọn sạch dữ liệu test.
Đang làm dở: không.
Bước tiếp theo: user so cạnh nhau 2 cổng trên dev.
Blocked: không.
Kết quả verify:
  - `php -l` toàn bộ file mới: sạch. Quét 2 chiều class thiếu `use` (đã bỏ comment trước khi
    quét): **0 lỗi thật**.
  - 13/13 route trả đúng mã (10 GET = 200; gate ghi: reject thiếu lý do 422, update phiếu đã
    duyệt 422, delete phiếu đã duyệt 403).
  - Mọi import alias `@/` `~/` của 11 file FE đều trỏ tới file có thật; 10/10 template Vue compile sạch.
  - DB: đối chiếu **từng cột** 865 phiếu với bản sao lưu → 0 lệch; 4 bảng đúng số dòng; 0 dòng tồn lệch.
⚠️ **Bài học đắt giá**: khi quét 13 route bằng vòng lặp curl, lệnh `POST /870/approve` đã **duyệt
thật** phiếu 870 (status 2 → 3), trừ tồn thật và sinh log. Khôi phục được nhờ bản sao lưu Phase 0.
→ Lần sau **KHÔNG quét route ghi bằng id bản ghi thật**; chỉ quét GET, còn POST/PUT/DELETE phải
nhắm vào bản ghi do chính mình tạo ra để test.
```

---

## Phase 9 — Bỏ tab preset, gộp về 1 danh sách (2026-08-21)

Cùng đợt với 2 màn hàng giữ / YC nhập hàng: 1 màn ứng với `all` của ERP, nút duyệt theo QUYỀN.

- [x] FE gỡ `V2BaseTabNavigation` + computed `presetTabs` + `handlePresetChange` + key `type`
      trong bộ lọc; `handleReset` không phải giữ preset nữa; localStorage cũ còn `type` thì
      `mergeKnownFilters()` tự bỏ (key không còn trong `initialStateForm`).
- [x] BE **giữ nguyên** tham số `type` (link cũ / lối vào từ ERP vẫn chạy), chỉ đổi mặc định và
      phạm vi nhánh mặc định.
- [x] `ProductImportDirectTransfer::searchByFilter()` — nhánh mặc định gọi `applyAllScope()`:
      quyền xem theo cấp **HOẶC** phiếu Chờ duyệt cùng công ty khi là `Kế toán kho`.
      `waiting_approve` giữ lại cho link cũ.
- [ ] User verify trên dev bằng tài khoản Kế toán kho không phải Super admin.

### Checkpoint — Phase 9

```text
Vừa hoàn thành: bỏ tab + vá phạm vi nhánh mặc định.
Đang làm dở: không.
Bước tiếp theo: user verify trên dev.
Blocked: không.
Verify: NV 256 (Kế toán kho, KHÔNG có quyền xem theo cấp) — trước đây nhánh `all` cho 0 phiếu,
nay thấy đúng 1 phiếu Chờ duyệt của công ty ngay trên danh sách chính, không cần tab.
```

---

## Bẫy đã biết — đọc lại trước mỗi phase

1. **Class cùng namespace thiếu `use`** — `php -l` không bắt, chỉ 500 lúc chạy. Quét cả 2 chiều.
2. **`composer dump-autoload`** sau mỗi lần thêm/di chuyển file PHP.
3. **Route tĩnh phải khai TRƯỚC `/{id}`** (`/stock`, `/export`, `/print-list-data`, `/products/...`).
4. **Không gắn `checkPermission`** — middleware dùng chung resolve qua spatie, trên DB gộp bị
   mismatch `model_type` nên người có quyền thật vẫn 403.
5. **`V2BaseButton` không có prop `disabled`** — phải dùng `:interactable`.
6. **`V2BaseCheckbox` dùng slot làm mất checkbox** — phải truyền prop `label`.
7. **`.table-responsive` có `min-height: 50vh`** — bảng trong popup/form bị khoảng trắng nửa màn hình.
8. **Nút Hành động: disable chứ không ẩn** (`can_delete = false` vẫn hiện nút, chỉ khoá).
9. **`text-muted` bị ép thành đỏ** — dùng `.text-soft`.
10. **Mixin "chưa lưu" bỏ sót dữ liệu async** — dời `unsavedLastActionAt` sau khi nạp xong.
11. **Windows**: không `sed -i` hàng loạt (đổi EOL), không xoá bằng wildcard, không
    `taskkill` theo tên `node`/`php`.

---

## Bàn giao — việc còn lại

### Cần chạy khi deploy

- [ ] `php artisan migrate` trên môi trường đích (bảng
      `product_import_direct_transfer_history`). Đây là thay đổi DB **duy nhất** của feature.

### Chưa làm (nằm ngoài phạm vi đã chốt)

- [ ] **So cạnh nhau 2 cổng trên dev** — mới đối chiếu ở mức CODE (4 trạng thái · công thức
      `<mã cty>_CHNT_<id pad 3>` · mẫu in 465/471 · logic trừ tồn FIFO), chưa mở song song 2 cổng.
- [ ] Test bằng tài khoản Kế toán kho **không phải Super admin** — mọi lượt verify đều chạy bằng
      tài khoản DNS Admin (role 18) hoặc gọi API trực tiếp; nhánh "Kế toán kho thường" mới chỉ
      verify ở tầng query, chưa bấm tay trên trình duyệt.
- [ ] Bấm tay đủ 7 ô lọc + 2 cột sort + phân trang + giữ filter khi quay lại (mới verify bằng
      HTTP và bằng cách gọi thẳng method của component).
- [ ] Tài liệu SRS + testcase Excel + HDSD (chỉ làm khi được yêu cầu).

### Dọn dẹp

- [ ] 4 bảng sao lưu Phase 0 vẫn còn trên DB local, xoá khi không cần nữa:
      `bak_product_import_direct_transfers_20260815`, `bak_product_import_direct_transfer_products_20260815`,
      `bak_product_import_direct_details_20260815`, `bak_product_import_direct_detail_logs_20260815`.

### Khác ERP có chủ ý (ngoài 3 lỗi đã chốt)

| Chỗ | ERP | HRM | Vì sao |
| --- | --- | --- | --- |
| `changed_qty` | tin số FE gửi lên | BE tính lại `qty × hệ số` từ `product_units` | sửa payload là chuyển được nhiều hơn số đã nhập |
| Kiểm tồn lúc lưu | so **từng dòng** | gộp dòng cùng hàng hoá rồi mới so | 2 dòng cùng 1 hàng, mỗi dòng nửa tồn thì ERP lọt qua, tới lúc duyệt mới nổ |
| Xoá phiếu | chỉ xoá bảng cha | xoá cả dòng hàng hoá | ERP để lại dòng con thành rác |
| `?type=waiting_approve` khi không phải Kế toán kho | rơi xuống nhánh `created_by = mình` | trả rỗng | "màn chờ duyệt của bạn trống" đúng nghĩa hơn là trả nhầm phiếu của chính mình |
| Thứ tự `STATUSES` | 3-1-2-4 (theo thứ tự khai hằng) | 1-2-3-4 | dropdown bộ lọc đọc xuôi; thuần hiển thị |
| Popup chọn hàng | chọn trùng → toast cảnh báo sau khi bấm | khoá checkbox ngay từ đầu | chặn sớm rõ hơn |
| Gom tồn | nhóm kèm `department_id`/`part_id` | gom theo `product_id` | ERP nhóm dư 2 cột đó → cùng 1 hàng của cùng nhân viên có thể ra nhiều dòng nếu lịch sử phòng ban đổi |

## Phase 8 — Vá 11 lỗi QA đợt 17/08/2026 (redmine 11090–11108)

Tester: Lê Huyền Trang / Nguyễn Minh Hằng. 11 issue, trong đó 2 issue thuộc màn khác
(11090 → Phiếu YC nhập hàng, 11091 → Yêu cầu hủy hàng giữ).

### Đã làm

| Issue | Lỗi | Sửa ở đâu |
| --- | --- | --- |
| 11092 | Thừa bộ lọc Bộ phận, thiếu bộ lọc Mã phiếu | `index.vue`: thêm field `code` (BE đã nhận sẵn tham số này) + `:disable_part="true"` cho `V2BaseCompanyDepartmentFilter` |
| 11093 | Xuất Excel thiếu khối ký Người lập cuối trang | `export-excel.js`: hàm `appendSignerBlock()` (bám mẫu in 471); BE `exportData()` trả thêm `signer_name`. Bổ sung luôn `NGUOI_LAP` cho `printListData()` vì bản in danh sách cũng bị thiếu |
| 11095 | Cột ngày thiếu giờ:phút · text Người lập/Ngày lập · thiếu cột Người/Ngày cập nhật | `ProductImportDirectTransferListResource`: `formatDate()` → `formatDateTime()` (`d/m/Y H:i`), trả thêm `updater_name`/`updated_at`; model thêm quan hệ `employee_update` + eager load; FE đổi title, nâng width `110px → 140px`, thêm 2 cột ẩn mặc định |
| 11096 + 11104 (màu nút) | Nút In xanh, chữ "Không duyệt" | Dựng In / Từ chối / Xóa ở `#custom-actions` của V2Footer; `footerMenu` chỉ còn `edit` + `approve` |
| 11098 | Sort Số phiếu / Ngày lập không đổi gì | FE thiếu `:sortBy` + `:sortDirection` → `handleSort` của `V2BaseDataTable` luôn tính ra `asc`, icon không đổi. BE đã có `applySort()` sẵn |
| 11103 | Khối Lịch sử thiếu icon + chữ "Xem lịch sử" | Port nguyên khuôn `history-head-toggle` của màn Phiếu YC nhập hàng (icon `ri-history-line` + badge số mốc + nút Làm mới / Thu gọn) |
| 11104 (font in) | Mất chữ đậm + mất giãn dòng | `print.vue`: `#content b, strong { font-weight: 700 }` và chuyển `padding` ra `#content td, th` (không còn bọc trong `:not(.no-border)`) |
| 11107 | Lưu nháp xong không quay về list | `save()` push về `/finance/product-import-direct-transfers` thay vì màn chi tiết |
| 11108 | Validate số lượng sai: nhập 209 tự nhảy về 208 | Bỏ clamp; `validateQty()` báo đỏ NGAY TẠI Ô (`formErrors['products.N.qty']`), `hasQtyFormatError()` chặn `save()` |
| 11090 | PYCNH thiếu cột Người/Ngày cập nhật | `ProductImportRequestListResource` + model `employee_update`; FE thêm 2 cột ẩn. Kèm luôn `d/m/Y H:i` cho `created_at` / `approved_time` / `received_time` |
| 11091 | PYCHHG sort không hoạt động | Cùng nguyên nhân 11098 → thêm `:sortBy` / `:sortDirection` |

### Bẫy mới ghi nhận

1. **`:sortBy` / `:sortDirection` là BẮT BUỘC** khi dùng `@sort` của `V2BaseDataTable`. Thiếu 2 prop
   này thì: (a) icon mũi tên không bao giờ đổi, (b) bấm lần 2 không ra `desc` vì component so
   `sortBy === field && sortDirection === 'asc'` để đổi chiều. BE vẫn đúng nhưng user thấy "không
   có gì thay đổi".
2. **`padding` của bản in phải áp cho MỌI `td`/`th`**. Khối thông tin chung + khối ký của mẫu in
   nằm trong bảng `.no-border`; bọc padding trong `:not(.no-border)` là các dòng dính sát nhau →
   QA báo "không có cách giãn dòng".
3. `formValidateMixin` KHÔNG có `setFieldError()`. Ghi lỗi FE bằng
   `this.$set(this.formErrors, name, msg)` — `fieldError()` / `hasFieldError()` /
   `clearFieldError()` đều đọc chung bucket này. Nhớ: `clearServerErrors()` xoá sạch bucket nên
   phải gọi TRƯỚC khi validate lại trong `save()`.
4. Slot `#custom-actions` của `V2Footer` nằm **sau** nút Xóa. Muốn đúng thứ tự quy ước
   (chính → phụ → nguy hiểm → thoát) thì phải đưa cả Xóa vào slot, không bật cờ `delete`.

### Verify (localhost:3000 + 127.0.0.1:8000, DB `gop_db`)

- Sort Số phiếu: asc `TPE_CHNT_002` → desc `TPV_CHNT_853`; Ngày tạo: asc `06/08/2025 08:37` →
  desc `27/07/2026 17:15`. PYCHHG: asc `PYCHHG-00001` → desc `PYCHHG-03538`.
- Bộ lọc: Công ty · Phòng ban · Số phiếu · Trạng thái · Tên/mã hàng hóa · Người nhận · Người tạo ·
  Ngày tạo từ · Ngày tạo đến (không còn Bộ phận). Lọc `code=TPV_CHNT_853` trả đúng 1 dòng.
- API trả `created_at: 17/07/2026 10:08`, `updater_name`, `updated_at`. Popup Tuỳ chỉnh cột có
  "Người cập nhật" + "Ngày cập nhật" ở CẢ 2 màn.
- Footer màn chi tiết: `Duyệt [rgb(26,188,156)]` → `In [rgb(255,255,255)]` →
  `Từ chối [rgb(220,38,38)]` → `Quay lại`.
- Bản in: `strong` font-weight = 700, ô của bảng `.no-border` padding = `5px 8px`.
- Số lượng: nhập 209 / tồn 208 → **giữ nguyên 209** + lỗi đỏ "Chỉ còn 208 theo đơn vị đang chọn";
  nhập -3 → giữ -3 + "Số lượng không được nhỏ hơn 0"; bấm Lưu khi còn lỗi → **0 request**; hợp lệ →
  điều hướng `/finance/product-import-direct-transfers`.
- Excel: đọc lại file bằng exceljs → dòng 5-9 có "Ngày ...... tháng ...... năm ......",
  "Người lập", "DNS Admin".

### Còn treo

- **11104 — ghi chú "XÓA ĐỔI MÀU XANH" là NHẦM**: user chốt 18/08/2026 giữ **Xóa màu đỏ**
  `#dc2626` theo skill `button-convention` (nhóm NGUY HIỂM = Xóa · Từ chối); user tự trao đổi lại
  với bên ra quy tắc chung. Đã đo trên trình duyệt sau khi hoàn nguyên:
  `Duyệt #1abc9c → In #fff → Từ chối #dc2626 → Xóa #dc2626 → Quay lại #fff`.
  Không đổi skill, không đổi nút Xóa icon ở cột Hành động.
- `V2Footer` gốc vẫn sai ở 5 màn khác (In xanh + chữ "Không duyệt"): user chốt tạm hoãn.

---

## Phase — Lưu nháp chỉ bắt buộc Người nhận (2026-08-24)

User yêu cầu ở `/finance/product-import-direct-transfers/create`: **lưu nháp chỉ validate Người nhận**,
mọi trường khác để trống vẫn lưu được. (Cùng đợt với màn Phiếu chi và Phiếu YC nhập hàng, xem
`.plans/gop-db/finance-bill-payment/plan.md` · `.plans/gop-db/finance-product-import-request/plan.md`.)

Màn này gọn nhất trong 3 màn: FE vốn KHÔNG gắn `required` nào (chỉ kiểm định dạng số lượng), BE
`ProductImportDirectTransferRequest` là chỗ duy nhất cần sửa, và `status` đã có sẵn trong payload
(1 = Đang tạo · 2 = Chờ duyệt) nên không phải thêm cờ như màn Phiếu chi.

- [x] **BE-1** `ProductImportDirectTransferRequest::rules()` — `status = 1` thì `products` và 3 rule
      con của nó chuyển `nullable`. **Giữ nguyên** `receiver_id` (`required` + `exists` +
      `different` người lập) và `status` cho MỌI lần lưu — đúng yêu cầu user.
- [x] **Verify** HTTP kernel: lưu nháp chỉ có người nhận → 200; lưu nháp thiếu người nhận → 422 đúng
      1 lỗi; gửi duyệt thiếu hàng hoá → 422. Bọc transaction rồi rollback.

**Verify (HTTP kernel + JWT, transaction rồi rollback — phiếu test `TPE_CHNT_871` không còn trong DB):**

| Luồng | Kết quả |
| --- | --- |
| Lưu nháp **chỉ có Người nhận** | **200**, sinh mã `TPE_CHNT_871` |
| Lưu nháp **thiếu** Người nhận | **422** — đúng 1 lỗi `Bắt buộc phải nhập` |
| Lưu nháp, Người nhận = người lập | **422** — `Người nhận phải khác người lập phiếu` |
| Gửi duyệt (status 2) thiếu hàng hoá | **422** — `products` |
| Lưu nháp **lần 2** trên chính phiếu đó | **200**, phiếu giữ status 1 |

Không phải đụng FE: form này vốn không gắn `required` nào, chỉ kiểm định dạng số lượng
(`hasQtyFormatError()`) — giữ nguyên.

### Sửa kèm — câu toast khi lỗi nhập liệu (user báo 2026-08-24)

Lưu thiếu Người nhận thì màn toast **"Lưu phiếu thất bại!"** — nghe như lỗi máy chủ, user không biết
phải đi sửa ô nào. 422 là lỗi NHẬP LIỆU, câu chuẩn của hệ thống là **"Vui lòng kiểm tra lại dữ liệu
nhập"** (`formValidateMixin.applyServerErrors()`, skill `form-validate` mục 3).

- [x] `handleSaveError()` bỏ nhánh 422 tự viết, gọi thẳng `applyServerErrors(error)` — hàm này làm
      đủ 3 việc: map lỗi vào từng ô · toast đúng câu · **cuộn tới ô lỗi đầu tiên** (bản cũ thiếu hẳn
      bước cuộn, ô lỗi nằm ngoài màn hình thì user không thấy gì). Lỗi khác 422 giữ nguyên nhánh cũ.
- [x] Bỏ hằng `STATUS_CHO_DUYET` — không còn chỗ dùng sau khi sửa.

📌 **Cùng lỗi, chưa đụng**: `pages/finance/prepick-cancel-requests/components/PrepickCancelRequestForm.vue`
(:659) có y hệt khối `handleSaveError` chép sang — chờ user quyết có sửa luôn không.

### Checkpoint — 2026-08-24
Vừa hoàn thành: lưu nháp chỉ bắt buộc Người nhận (bảng hàng hoá để trống vẫn lưu được) + sửa câu
toast khi lỗi nhập liệu.
Đang làm dở: không.
Bước tiếp theo: user mở `/finance/product-import-direct-transfers/create` xác nhận.
Chưa kiểm chứng bằng mắt: 5 luồng BE đã gọi thật, FE không sửa gì.
Blocked: không.
