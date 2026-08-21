# Phiếu chuyển hàng nhập thẳng (ERP → HRM) — design

> Phụ trách: @junfoke · Bắt đầu: 2026-08-15 · Nhánh: `feat/finance-product-import-direct-transfer`
> (checkout từ `gop_db`, cả 2 repo — checkout thẳng, KHÔNG dùng worktree)
> Khuôn mẫu bám theo: `.plans/gop-db/finance-product-transfer-request/` (@khoipv) và
> `.plans/gop-db/finance-product-import-request/` (@junfoke)
>
> **Trạng thái: CODE DONE + ĐÃ VERIFY (2026-08-15)** — xem `plan.md` (checkpoint từng phase +
> mục "Bàn giao — việc còn lại"). BE 12 file + 1 migration + 13 route; FE 11 file + 1 mục menu.
> Đối chiếu từng cột 865 phiếu với bản sao lưu: 0 lệch.

## Mục tiêu

Port màn ERP **"Phiếu chuyển hàng nhập thẳng"** (`admin/warehouse/product_import_direct_transfer_requests`)
sang HRM phân hệ **Tài chính**, nhóm **Điều chuyển** (`hubGroup: 'Hàng hoá - Dịch vụ - Vận chuyển'`),
đứng cạnh mục "Phiếu điều chuyển hàng" đã port.

**HRM là bản thay thế lâu dài** — 2 cổng chạy song song trên cùng bảng của DB gộp,
**KHÔNG đổi schema 4 bảng nghiệp vụ**.

### Nghiệp vụ

Hàng "nhập thẳng" là hàng về thẳng tay **nhân viên**, không qua kho — tồn ghi ở
`product_import_direct_details` theo `employee_id`. Phiếu này **điều chuyển tồn nhập thẳng từ
người lập sang một nhân viên khác cùng công ty**, do **Kế toán kho** duyệt. Khi duyệt: trừ tồn
FIFO của người lập, ghi log, tạo bản ghi tồn cho người nhận.

## Hiện trạng ERP

| Thành phần | Số liệu |
| --- | --- |
| `Warehouse\ProductImportDirectTransferController` | 414 dòng |
| `Model\Warehouse\ProductImportDirectTransfer` | 409 dòng (+ `...TransferProduct`, `ProductImportDirectDetail`, `...DetailLog`) |
| Blade | 6 file (`index` · `create` · `edit` · `show` · `form` 187 dòng · `formJs` 111 dòng) |
| Route ERP | 13 route `productImportDirectTransfers.*` (`routes/web.php:997-1009`) |
| Trạng thái | 4 dùng thật: 1 Đang tạo · 2 Chờ duyệt · 3 Đã duyệt · 4 Không duyệt (hằng `HUY = 0` khai nhưng không dùng) |
| Mẫu in | `ReportTemplate::YEU_CAU_CHUYEN_HANG_NHAP_THANG = 465` (phiếu) · `DANH_SACH_PHIEU_DIEU_CHUYEN_HANG_NHAP_THANG = 471` (danh sách) |
| Xuất Excel | `app/ExcelExports/ProductImportDirectTransferExcel.php` (danh sách) |

Quy mô **nhỏ hơn nhiều** so với Phiếu YC nhập hàng: 1 loại phiếu, 4 trạng thái, 1 luồng duyệt,
không file đính kèm, không chi phí, không dòng con khách hàng.

### Dữ liệu trên `gop_db` (đo 2026-08-15)

| Bảng | Số dòng |
| --- | --- |
| `product_import_direct_transfers` | 865 |
| `product_import_direct_transfer_products` | 2.349 |
| `product_import_direct_details` (tồn) | 15.834 |
| `product_import_direct_detail_logs` | 32.730 |

### 2 lối vào menu ERP

| `type` | Lọc | Lối vào |
| --- | --- | --- |
| `all` | Phạm vi theo 4 quyền cấp; ẩn phiếu "Đang tạo" của người khác | `Kho > Nhập - xuất hàng` |
| `waiting_approve` | `status = 2` + cùng công ty, gate quyền `Kế toán kho` | Menu `Chờ duyệt` |
| *(rỗng / `index`)* | `created_by = mình` | Đã comment khỏi menu |

## Quyết định đã chốt (user 2026-08-15)

1. **Phân hệ Tài chính**, nhóm **Điều chuyển** của `finance.js` — không đưa vào Bán hàng
   (ô xám `sale-hub.js:101` chỉ là danh sách gợi ý, `YC nhập hàng` ở đó cũng đã port về Tài chính)
   và không đưa vào Kho (phân hệ đó vẫn `hidden + erpGhost`).
2. **1 mục menu duy nhất** — 1 màn danh sách nhận `?type=`, mặc định `all`; preset
   `waiting_approve` hiện theo quyền `Kế toán kho`. Không tách 2 mục như ERP.
3. **Sửa 3 lỗi của bản ERP** (mục "3 lỗi sẽ sửa"). Lỗ hổng loại "giữ nguyên như ERP" không có ở màn này.
4. **Bổ sung tab Lịch sử** — tính năng MỚI, ERP không có.
5. **Port đủ**: In phiếu (mẫu 465) · In danh sách (mẫu 471) · Xuất Excel danh sách.
6. **Ngoài phạm vi**: màn báo cáo "Danh sách hàng xuất nhập thẳng" (`productImportDirectDetails`,
   sơ đồ v1.6 dòng 443) và "Báo cáo tồn hàng nhập xuất thẳng" — vẫn ở ERP.

## Phân quyền

Dùng lại **nguyên** quyền ERP, **không tạo quyền mới**:

| Quyền | id trên `gop_db` | guard | Vai trò |
| --- | --- | --- | --- |
| Xem phiếu chuyển hàng nhập thẳng theo tổng công ty | 100711 | web | Phạm vi danh sách + `canView` |
| … theo công ty | 100712 | web | |
| … theo phòng ban | 100713 | web | |
| … theo bộ phận | 100714 | web | |
| Kế toán kho | 100080 (web) / 1136 (api) | | Duyệt / Không duyệt + preset `waiting_approve` |

**Cách kiểm tra quyền**: query thẳng pivot `employee_has_roles` / `role_has_permissions` /
`employee_has_permissions` theo **tên quyền**, KHÔNG dùng spatie Eloquent, KHÔNG dùng
`ErpPermissionHelper`. Lý do đã verify ở `ProductTransferRequest` (docblock entity):

- **Guard mismatch**: quyền ERP có `guard_name = web`, guard mặc định app là `api` →
  `hasPermissionTo($name)` ném `PermissionDoesNotExist`.
- **`model_type` mismatch**: `employee_has_roles` có 2 giá trị cho cùng 1 nhân viên
  (`App\Employee` gán từ ERP và `Modules\Timesheet\Entities\Employee` gán từ HRM); quan hệ
  morphToMany của spatie lọc theo `get_class($this)` nên bỏ sót toàn bộ role gán từ ERP.

Route **không gắn** middleware `checkPermission` / `erpPermission` — chặn trong Entity
(`searchByFilter` + `canView` + `canEdit` + `canApprove`) như 3 màn Finance đã port.

## 3 lỗi ERP sẽ sửa

| # | Hiện trạng ERP | Sửa ở HRM |
| --- | --- | --- |
| 1 | `canView()` (`ProductImportDirectTransfer.php:166`) chỉ cho Super Admin / người tạo / Kế toán kho cùng công ty → người có quyền 100711-714 **thấy dòng ở danh sách nhưng bấm vào ra `not_found`** | Bổ sung 4 nhánh quyền cấp, khớp đúng phạm vi của `searchByFilter` |
| 2 | `getEmployeeProductImportDirect()` luôn lấy tồn của **người đang đăng nhập**, trong khi `validateProducts()` lúc lưu lại kiểm theo tồn của **người tạo phiếu** → vào Sửa phiếu người khác thì popup hiện sai hàng | `GET /stock` nhận `employee_id`: màn Tạo = mình, màn Sửa = `created_by` của phiếu; popup và validate dùng chung một nguồn |
| 3 | `store()`/`update()` gán thẳng `$request->status` không validate → client gửi `status = 3` là phiếu tự "Đã duyệt", bỏ qua Kế toán kho | `store`/`update` chỉ nhận `status ∈ {1, 2}`; sang 3/4 **chỉ** qua route `approve` / `reject` (đã gate `canApprove`) |

## Cấu trúc code

### BE — `Modules/Finance`

```
Entities/ProductImportDirectTransfer/
    ProductImportDirectTransfer.php          # bảng product_import_direct_transfers
    ProductImportDirectTransferProduct.php   # ..._products
    ProductImportDirectDetail.php            # tồn nhập thẳng theo nhân viên
    ProductImportDirectDetailLog.php         # log biến động tồn
    ProductImportDirectTransferHistory.php   # BẢNG MỚI (lịch sử)
Services/ProductImportDirectTransferService.php
Services/ProductImportDirectTransferHistoryService.php
Http/Controllers/V1/ProductImportDirectTransferController.php
Http/Requests/ProductImportDirectTransfer/ProductImportDirectTransferRequest.php
Transformers/ProductImportDirectTransferResource/{ListResource,DetailResource}.php
```

⚠️ **Migration KHÔNG đặt trong module.** Cả project để chung ở `database/migrations/` để chạy
bằng `php artisan migrate` — file của feature này là
`database/migrations/2026_08_15_000001_create_product_import_direct_transfer_history_table.php`.
(`Modules/*/Database/Migrations` có sẵn nhưng là bản cũ, không dùng cho code mới.)

### API — 13 route, prefix `/v1/finance/product-import-direct-transfers`

| Method | Path | Việc |
| --- | --- | --- |
| GET | `/` | Danh sách, `?type=all\|waiting_approve` |
| GET | `/stock` | Tồn nhập thẳng theo `employee_id` (popup chọn hàng) |
| GET | `/products/{id}/units` | ĐVT + hệ số của 1 hàng hoá |
| GET | `/export` | Xuất Excel danh sách |
| GET | `/print-list-data` | Dữ liệu in danh sách (mẫu 471) |
| POST | `/` | Tạo (status 1 hoặc 2) |
| PUT | `/{id}` | Sửa (status 1 hoặc 2) |
| DELETE | `/{id}` | Xóa |
| POST | `/{id}/approve` | Duyệt |
| POST | `/{id}/reject` | Không duyệt (bắt buộc lý do) |
| GET | `/{id}/print-data` | Dữ liệu in phiếu (mẫu 465) |
| GET | `/{id}/histories` | Lịch sử thay đổi |
| GET | `/{id}` | Chi tiết |

⚠️ Route **tĩnh khai TRƯỚC** `/{id}` — nếu không sẽ bị route động nuốt.

### FE — `pages/finance/product-import-direct-transfers/`

```
index.vue                 # danh sách
create.vue                # tạo mới
_id/index.vue             # chi tiết (+ khối Lịch sử)
_id/edit.vue              # sửa
_id/print.vue             # in phiếu (mẫu 465)
components/
    ProductImportDirectTransferForm.vue   # form dùng chung create/edit/show
    StockSearchModal.vue                  # popup "Tồn hàng nhập thẳng của nhân viên"
    ProductImportDirectTransferHistoryModal.vue
```

## Chi tiết màn — bám bộ chuẩn V2

Đọc trước khi code: `.claude/skills/list-page`, `button-convention`, `modal-popup`,
`form-validate`, `unsaved-changes`, `print-page`, `entity-history`,
`notification-convention`.

### Màn danh sách

- `V2BaseSmartFilterPanel` + `V2BaseDataTable`, `@import '@/assets/scss/v2-styles.scss'`.
- **Cột mặc định (7)**: `STT` · `Số phiếu` · `Người nhận` · `Người tạo` · `Ngày tạo` ·
  `Trạng thái` · `Hành động`.
  `Người nhận` hiện mặc định theo **ngoại lệ §6 của skill `list-page`** — thiếu nó thì dòng dữ
  liệu không đọc được là phiếu chuyển cho ai.
  Cột ẩn mặc định (bật ở "Cấu hình cột hiển thị"): `Công ty`, `Phòng ban`, `Ghi chú`, `Người duyệt`.
- `STT` + `Số phiếu` khai `sticky: true` + `locked: true`; `Số phiếu` là link `.v2-cell-link`
  vào chi tiết bằng `<nuxt-link>`.
- **Sortable**: `Số phiếu`, `Ngày tạo` (khai đủ trong `SORTABLE_COLUMNS` của service, key FE
  trùng key BE).
- **Bộ lọc**: Công ty → Phòng ban → Bộ phận (cascade, `V2BaseCompanyDepartmentFilter`) +
  Mã phiếu · Trạng thái · Tên/mã hàng hoá · Người nhận · Người lập · Từ ngày / Đến ngày.
  Auto-search bằng deep watcher (`ignoredFields: ['keyword']`), `filterStateMixin` với
  `localStorageKey: 'finance_product_import_direct_transfers'`,
  `pathsToKeep: ['/finance/product-import-direct-transfers']`.
- **Tìm nhanh**: Số phiếu + Người tạo; sắp xếp theo độ khớp ở BE (`applyRelevanceOrder`).
- **Hành động/dòng** (`V2BaseRowActions`): `Sửa` (`ri-edit-line`, có `to`) · `Xóa`
  (`ri-delete-bin-6-line`, danger) + menu `⋮`: `In`, `Lịch sử` (`ri-history-line`).
  Mọi cờ quyền fail-closed.
- **Nút màn**: `Tạo mới` · `In` · `Xuất Excel` (xanh lá) — theo `button-convention`.
- **Thứ tự request** (skill `list-page` §8): `loadData()` chạy đầu tiên trong `created()`,
  không `await` gì; cấu hình cột và quyền chạy song song; options bộ lọc nâng cao hoãn tới
  khi mở panel.

### Màn Tạo / Sửa

| Trường | Quy tắc |
| --- | --- |
| Người nhận (*) | Select nhân viên **cùng công ty với người tạo phiếu**, loại chính mình |
| Phòng ban | Tự điền theo người nhận, **disabled** |
| Ghi chú | Tối đa 255 ký tự |
| Bảng hàng hoá (*) | Chọn từ popup "Tồn hàng nhập thẳng của nhân viên"; mỗi dòng: Tên hàng · Mã hàng · ĐVT · Số lượng · Số lượng theo ĐV cơ bản |

- Quy đổi giữ nguyên ERP: `changed_qty = qty × unit_coefficient`; đổi ĐVT thì tính lại
  `qty = product_qty / unit_coefficient`; **chặn nhập vượt tồn** (`qty ≤ product_qty / hệ số`).
- 2 nút lưu: **Lưu nháp** (status 1) · **Lưu & Gửi duyệt** (status 2). Gửi duyệt thì bắn thông
  báo cho nhóm quyền `Kế toán kho` theo `notification-convention`.
- `unsavedChangesMixin` + `markFormSaved()` sau khi lưu; validate realtime bằng `vee-validate`
  trên component `V2Base*`; select trong popup dùng `V2BaseSelectInModal`.

### Màn Chi tiết

- Tiêu đề: `Chi tiết phiếu chuyển hàng nhập thẳng: <mã>` (set sau khi form `$emit('loaded')`).
- Form readonly (kiểu ô khoá theo `list-page` §10) + khối **Lịch sử** cuối trang, mặc định
  thu gọn, lazy load.
- `V2Footer`: `Sửa` → `In` → `Duyệt` / `Không duyệt` → `Xóa` → `Quay lại`, gate fail-closed
  đúng cờ quyền của màn danh sách.
- Duyệt / Không duyệt mở `components/modal/base-confirm-modal.vue`; **Không duyệt bắt buộc
  nhập lý do** (`approver_comment`).

### In / Xuất Excel

- **In phiếu**: `_id/print.vue`, dữ liệu từ `GET /{id}/print-data` (BE fill template DB id 465
  bằng `fillReport` + `clearNull` như `product-import-requests`).
- **In danh sách**: `GET /print-list-data` (template 471, in ngang, 6 cột: STT · Số phiếu ·
  Ngày lập · Người lập · Người nhận · Trạng thái).
- **Xuất Excel danh sách**: theo convention ExcelJS của FE, nhớ **tự gắn token** vào header.

## Tab Lịch sử — tính năng MỚI

Theo `.claude/skills/entity-history` (biến thể **subset-diff**, đọc `ui-base.md` trước khi
viết markup).

**Bảng mới** `product_import_direct_transfer_history`:
`id` · `product_import_direct_transfer_id` (index) · `company_id` (index) · `action` ·
`old_value` / `new_value` (text, JSON) · `note` · `changed_by` · `changed_at` · `timestamps()`.
Không FK cứng, không SoftDeletes.

| Chốt theo §0 của skill | Giá trị |
| --- | --- |
| Track trường nào | Người nhận · Ghi chú · Trạng thái + **bảng con hàng hoá** |
| Ai được xem | Không quyền riêng — vào được màn thì xem được |
| Action ngoài `update` | `create` · `send_approve` · `approve` · `reject` |
| Bảng con dạng danh sách | Có → dùng **khoá dạng bảng**, `__key = product_id + '|' + unit_id` (vì `syncProducts` xoá hết rồi tạo lại, không upsert theo id) |

- `note` = `approver_comment` — bắt buộc theo §4.1: lý do Không duyệt phải hiện trên lịch sử.
- Snapshot lưu **giá trị hiển thị** (tên nhân viên, tên ĐVT, tên trạng thái), không lưu id.
- Sắp xếp **mới → cũ**; làm **đủ 2 nơi**: popup ở menu `⋮` màn danh sách + khối Lịch sử ở màn chi tiết.

⚠️ **Bảng này chỉ HRM ghi.** Phiếu sửa/duyệt bên cổng ERP sẽ không vào lịch sử → 2 cổng lệch
cho tới khi màn ERP bị tắt. Đã báo user.

## Rủi ro / điểm cần canh

1. **Logic duyệt đụng tồn thật** — trừ FIFO `lockForUpdate` trên `product_import_direct_details`
   + ghi `..._logs` + tạo bản ghi tồn cho người nhận. Sai là lệch tồn nhập thẳng của nhân viên.
   Phải test trên bản sao dữ liệu, không test trên phiếu thật.
2. **`ProductImportDirectDetailLog` bên ERP không được `use`** trong `ProductImportDirectTransfer`
   (cùng namespace `App\Model\Warehouse` nên chạy được). Khi port sang HRM phải khai `use` đầy đủ
   — bẫy "class cùng namespace" của `chuyen-code-phan-he`.
3. **`generateCode()`** dùng `auth()->user()->info->company->code . '_CHNT_' . generateCode(3, id)`
   — phải sinh **giống hệt** ERP để 2 cổng không lệch định dạng mã.
4. **`employees` đã gộp** → `auth()->id()` là id nhân viên duy nhất, không còn lớp map ERP id.
5. **Migration lịch sử** là thay đổi DB duy nhất — đặt ở `database/migrations/` (chỗ chung của cả
   project), chạy bằng `php artisan migrate`.

## Liên quan

- `.plans/gop-db/design.md` — nền tảng gộp DB (đọc trước)
- `.plans/gop-db/finance-product-import-request/` — khuôn mẫu gần nhất
- `.plans/gop-db/finance-product-transfer-request/` — khuôn mẫu về quyền + duyệt
- `.plans/gop-db/chuyen-code-phan-he/` — 10 bẫy khi chuyển code sang phân hệ
