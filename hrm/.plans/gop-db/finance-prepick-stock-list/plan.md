# Plan — Danh sách hàng giữ (ERP → HRM), 1 màn

> @junfoke · nhánh `feat/finance-prepick-stock-list` (từ `gop_db`, cả 2 repo) · design: `./design.md`
>
> **Trạng thái: XONG PHASE 0-7 + ĐÃ VERIFY TRÊN TRÌNH DUYỆT BẰNG PLAYWRIGHT (2026-08-18).**
>
> BE 4 file mới (`PrepickStockReportService` 1.100 dòng · `PrepickStockController` ·
> `PrepickStockProductResource` · blade in `prepick-stock-list`) + 6 route. Không migration.
> FE 4 file mới (`pages/finance/prepick-stocks/index.vue` + `print.vue` + `components/export-excel.js`,
> `components/finance/prepick/PrepickStockLogModal.vue`) + 1 mục menu.
>
> **Verify**: 6/6 endpoint GET trả 200 đúng dữ liệu · 7/7 bộ lọc đối chiếu khớp SQL trực tiếp ·
> phân quyền 3 nhánh chạy đúng (Super admin 895 / có quyền nhưng không có cấp nào 70 của chính mình
> / không quyền 403) · vá lỗi #6 đã chứng minh trên dữ liệu thật ·
> **`prepick_details` + `prepick_logs` y nguyên số dòng và SUM(qty) so với Phase 0**.
>
> **Còn lại (user làm)**: đối chiếu 2 cổng trên dev bằng tài khoản thường; test nhánh quyền
> `Xem phiếu hàng giữ theo phòng ban` (chưa có tài khoản mẫu trên DB local).
>
> Màn **báo cáo tra cứu, CHỈ ĐỌC** — không tạo/sửa/xóa, **không ghi một dòng nào** vào
> `prepick_details` / `prepick_logs`. Vì vậy KHÔNG cần sao lưu bảng như đợt Hủy hàng giữ.
> Đổi lại, rủi ro nằm ở chỗ khác: **6 màn ERP khác dùng chung** `PrepickDetail::searchByFilter()`
> và `getPrepickDetails()`. HRM viết service **mới, tách hẳn** — tuyệt đối không đụng file ERP.
>
> Ước lượng: BE 8 file mới + 5 route · FE 4 file mới + 1 mục menu. Không migration.

## Nguồn ERP cần đọc

| Việc | File ERP (`TanPhatDev/`) |
| --- | --- |
| Controller (5 method) | `app/Http/Controllers/Warehouse/WarehouseInfosController.php` — `prepickIndex` :522 · `prepickSearchData` :565 · `getPrepickDetails` :292 · `getHistoryPrepickDetails` :394 · `exportPrepickIndex` :916 · `printPrepickIndex` :945 |
| Query tầng 1 | `app/Model/Warehouse/PrepickDetail.php::searchByFilter()` :50-146 |
| Query In/Xuất | `app/Services/Warehouse/PrepickIndexReportService.php` (`getData` :147 · `getTable` :79 · `getTable4Print` :20) |
| Blade | `resources/views/warehouse/warehouses/prepickIndex.blade.php` (533 dòng) |
| Class JS quy đổi đơn vị | `resources/views/partials/classes/warehouse/ProductInPrepick{,Detail,DetailItem}.blade.php` |
| Route | `routes/web.php:918-945` |
| Mẫu in | `report_templates` id `ReportTemplate::BAO_CAO_HANG_XUAT_GIU` |

## Khuôn mẫu HRM cần copy (KHÔNG tự phát minh)

| Phần | File mẫu |
| --- | --- |
| Kiểm quyền qua pivot | trait `Modules/Finance/Entities/Concerns/ChecksEmployeePermission` |
| Hằng số quyền 3 cấp + `applyViewScope()` | `Modules/Finance/Entities/PrepickCancel/PrepickCancelRequest.php:40-43, :335-365` |
| Model `prepick_details` / `prepick_logs` | `Modules/Finance/Entities/PrepickCancel/PrepickDetail.php` · `PrepickLog.php` (đã có, **dùng lại y nguyên**) |
| Cách viết service đọc tồn giữ | `Modules/Finance/Services/PrepickStockService.php` (**chỉ đọc tham khảo, KHÔNG sửa**) |
| Controller + thứ tự route tĩnh trước `/{id}` | `Modules/Finance/Http/Controllers/V1/PrepickCancelController.php` + `Routes/api.php` |
| FE danh sách V2 (mixin, filter panel, cấu hình cột) | `pages/finance/prepick-cancels/index.vue` |
| FE cây cha–con (nút ▸ ở cột STT, dàn phẳng, cache con) | `pages/assign/prospective-projects/index.vue:266-287, :990-1006, :1099-1123` |
| FE xuất Excel + popup chọn trường | `pages/finance/prepick-cancels/components/export-excel.js` + `@/components/modal/export-fields-modal.vue` |
| FE in khổ ngang | `pages/finance/prepick-cancel-requests/print-list.vue` |
| Modal | `components/finance/prepick/PrepickHistoryModal.vue` (**vỏ** `b-modal` — chỉ copy vỏ, thân khác hẳn) |

---

## Phase 0 — Chuẩn bị

- [x] Tạo nhánh `feat/finance-prepick-stock-list` từ `gop_db` ở **cả 2 repo** (`hrm-api`, `hrm-client`)
- [x] Đọc `.plans/gop-db/design.md` (nền tảng gộp DB) + `./design.md`
- [x] Đọc skill: `erp-to-hrm-screen`, `list-page`, `button-convention`, `modal-popup`,
      `select-and-input-state`, `print-page`
- [x] Ghi "ảnh chụp" dữ liệu để đối chiếu cuối đợt (màn chỉ đọc nên đây là **bằng chứng không
      ghi nhầm**, không phải bản sao lưu):

```sql
SELECT COUNT(*) AS tong_dong, SUM(qty) AS tong_qty FROM prepick_details;
SELECT COUNT(*) FROM prepick_logs;
```

- [x] Kiểm quyền `Quản lý giữ hàng` (100427) và 3 quyền `Xem phiếu hàng giữ theo ...`
      (100839/840/841) còn đúng id + tên trên `gop_db` (đợt Hủy hàng giữ đã dùng, chỉ xác nhận lại)

### Checkpoint — Phase 0

```text
Vừa hoàn thành: tạo nhánh `feat/finance-prepick-stock-list` ở cả 2 repo (checkout từ `gop_db`);
chụp số liệu 2 bảng tồn; xác nhận 4 quyền còn đúng id + tên trên gop_db (đều guard `web`).
Đang làm dở: không.
Bước tiếp theo: Phase 1 — BE service đọc + danh sách tầng 1.
Blocked: không.
Verify: prepick_details 53.832 dòng (SUM qty = 6.112) · prepick_logs 110.744 dòng.
Quyền: 100427 Quản lý giữ hàng · 100839/840/841 Xem phiếu hàng giữ theo tổng công ty/công ty/phòng ban.
```

---

## Phase 1 — BE: service đọc + danh sách tầng 1

- [x] Tạo `Modules/Finance/Services/PrepickStockReportService.php`.
      **CHỈ ĐỌC.** Không `insert`/`update`/`delete`/`save` ở bất kỳ đâu trong file.
      `use ChecksEmployeePermission`.
- [x] Hằng số trạng thái hạn giữ — đặt ngay trong service, **không** map số→chữ ở FE:

```php
const TRONG_HAN = 1;   // expire_date > CURDATE()
const HET_HAN   = 2;   // expire_date < CURDATE()
const DEN_HAN   = 3;   // expire_date = CURDATE()

const STATUSES = [
    self::TRONG_HAN => 'Trong hạn',
    self::HET_HAN   => 'Hết hạn',
    self::DEN_HAN   => 'Đến hạn',
];
```

- [x] `applyViewScope($query, $alias)` — phạm vi dữ liệu 4 nhánh (design §Phân quyền).
      **Fail-closed**: không rơi vào nhánh nào → `where employee_id = auth()->id()`.
      Cấp phòng ban: `whereIn(employee_id, thành viên các phòng quản lý)` **orWhere**
      `employee_id = mình` (bảng không có `department_id` — lỗi #8/design).
- [x] `applyFilters($query, $request, $alias)` — dùng chung cho **cả 3 tầng và cả In/Xuất**
      (vá lỗi #3 + #4 của design). Nhận đúng tên khoá HRM:
      `company_id` · `department_id` · `employee_id` · `customer_id` · `brand_id` · `model_id` ·
      `product_name` · `product_code` · `status` · `product_id`.
      **KHÔNG** có `warehouse` (lỗi #2 — bỏ hẳn ô lọc Kho).
- [x] `searchProducts($request)` — tầng 1. Select **chỉ cột cấp hàng hoá** (vá lỗi #1):
      `p.id`, `p.code`, `p.name`, `b.name as brand`, `pm.name as model`,
      `SUM(pd.qty) as prepick_qty`, `acc.stock_qty as total_stock_qty`.
      `GROUP BY p.id, p.code, p.name, b.name, pm.name, acc.stock_qty` +
      `HAVING prepick_qty > 0`. **Không** select `employee_id` / `expire_date`.
- [x] Subquery `accounting_stocks` cho `total_stock_qty` — join `accounting_warehouses` và áp
      **cùng điều kiện công ty** với tầng 1 (port ERP :96-111).
- [x] Nạp `units` (`withUnits()` tương đương) cho từng hàng hoá để FE đổi đơn vị. Dùng lại cách
      lấy hệ số của `PrepickStockService::baseUnits()` / `unitCoefficient()` — **đọc tham khảo,
      viết bản riêng trong service mới**.
- [x] Sắp xếp: mặc định `p.name ASC`; cho phép `sort_by` ∈ `code|name|prepickQty|totalStockQty`.
      Luôn chốt `p.id ASC` cuối để lật trang không lặp/mất bản ghi.
- [x] Tạo `Modules/Finance/Http/Controllers/V1/PrepickStockController.php`:
      `index()` gate quyền `Quản lý giữ hàng` → không có thì **403**, không hard-code `true`.
- [x] Tạo `Modules/Finance/Transformers/PrepickStock/PrepickStockProductResource.php`.
- [x] `Modules/Finance/Routes/api.php` — thêm nhóm `prefix('prepick-stocks')`,
      **khai route tĩnh (`/details`, `/logs`, `/export`, `/print`) TRƯỚC** mọi route có tham số.
- [x] `php -l` mọi file mới. `php artisan route:list --path=prepick-stocks` đếm đúng số route.

### Checkpoint — Phase 1

```text
Vừa hoàn thành: `PrepickStockReportService` (chỉ đọc) + `PrepickStockController` +
`PrepickStockProductResource` + 6 route `/v1/finance/prepick-stocks`.
Đang làm dở: không.
Bước tiếp theo: Phase 2 — BE tầng 2+3 và sổ biến động.
Blocked: không.
Verify: GET /prepick-stocks?per_page=1 -> total = 895, ĐÚNG BẰNG
`SELECT COUNT(DISTINCT product_id) FROM prepick_details WHERE qty>0`.
GET /meta -> 87 thương hiệu · 822 model · 74 nhân viên (khớp `COUNT(DISTINCT ...)` trên DB).
`php artisan route:list` KHÔNG chạy được trên repo này (lỗi có sẵn ở
`app/Helper/PermissionHelper.php:23` của module Timesheet, không liên quan feature) -> verify
route bằng script probe dispatch nội bộ.

⚠ Dropdown Khách hàng chỉ ra 16/192 giá trị. KHÔNG phải lỗi code: bảng `customers` trên DB local
thiếu dải id của ERP (đã ghi ở memory `project_gop_db_customers_thieu_dai_id_erp`). Trên DB thật
sẽ đủ 192.
```

---

## Phase 2 — BE: tầng 2+3 và sổ biến động giữ hàng

- [x] `detailsOfProduct($request)` — tầng 2+3 trong **một lần gọi**:
      lấy mọi lô `qty > 0` của `product_id`, áp **đúng** `applyViewScope` + `applyFilters`
      (kể cả `customer_id` — vá lỗi #3), `orderBy employee_id ASC, customer_id ASC,
      expire_date ASC, id ASC`.
      BE **gom sẵn theo `employee_id`** để FE khỏi tự gom:

```
[ { employee_id, employee_name, department_name, total_qty,
    items: [ { prepick_detail_id, customer_id, customer_code, customer_name,
               qty, expire_date, status, status_text, company_id } ] } ]
```

- [x] `logsOfLot($productId, $customerId, $companyId, $employeeId)` — sổ biến động.
      Lấy `prepick_logs` của mọi `prepick_detail.id` khớp bộ 4, **sắp `created_at ASC` (cũ → mới)**.
      ⚠ Ngoại lệ CÓ CHỦ ĐÍCH so với rule "lịch sử sắp mới → cũ": cột `SL giữ` (`qty_after`) là số
      cộng dồn sau mỗi lần biến động, đảo ngược sẽ đọc sai. Ghi comment ngay trên hàm.
- [x] Dựng chứng từ `{ code, url }` cho từng dòng log, đủ **11 loại** `objectable_type` đang có
      trong DB (vá lỗi #6):

| `objectable_type` | Dòng log | Lấy phiếu cha qua |
|---|---:|---|
| `...\PrepickExtendRequestDetail` | 59.734 | `objectable->parent` |
| `...\WarehousePrepickRequestDetail` | 10.429 | `objectable->parent` |
| `...\PrepickCancel` | 9.908 | chính nó |
| `...\ProductExportDetailAccounting` | 8.924 | `objectable->parent` |
| `...\ProductImportDetailCustomer` | 5.482 | `ProductImport::find(objectable->parent->parent_id)` |
| `...\TransferProductAllocationDetail` | 5.061 | `objectable->parent` |
| `...\PrepickTransfer2` | 3.842 | chính nó |
| `...\PrepickTransfer2Detail` | 3.842 | `objectable->parent` |
| `NULL` | 1.875 | `prepick_detail->objectable` |
| **`...\AccountingPrepickCancelDetailCustomer`** | **1.645** | **ERP BỎ SÓT** → bổ sung `objectable->parent` |
| **`...\ProductExportDetail`** | **2** | **ERP BỎ SÓT** → bổ sung `objectable->parent` |

- [x] `url`: loại đã port sang HRM (`PrepickCancel`) → `/finance/prepick-cancels/{id}`;
      còn lại → `config('app.erp_url')` + đường dẫn ERP tương ứng; không dựng được → `null`.
      **Không trả HTML thô** như ERP (`getLinkAttribute` trả cả thẻ `<a>`).
- [x] Controller `details()` + `logs()`, cùng gate quyền như `index()`.
- [x] 2 Resource: `PrepickStockDetailResource`, `PrepickStockLogResource`.
- [x] Test bằng script probe (dispatch nội bộ có JWT, **chỉ GET**) trên 1 hàng hoá có nhiều lô:
      tổng `SUM(items.qty)` của tầng 2 phải **khớp** `prepick_qty` của tầng 1 cùng bộ lọc.

### Checkpoint — Phase 2

```text
Vừa hoàn thành: `detailsOfProduct()` (tầng 2+3, gom sẵn theo nhân viên), `logsOfLot()` (sổ biến
động, cũ -> mới), bảng tra chứng từ 11 loại `objectable_type`, `exportRows()`, `printData()`.
Đang làm dở: không.
Bước tiếp theo: Phase 3 — FE bảng 3 tầng.
Blocked: không.
Verify (tài khoản 13, Super admin):
- /details?product_id=5345 -> 22 nhân viên / 23 lô, tổng qty = 159, KHỚP `prepick_qty` tầng 1.
- /logs (5345 x NV27 x KH38398 x CT1) -> 20 dòng, 17/20 dựng được chứng từ. 3 dòng còn lại là
  `PrepickTransfer2` — bảng `prepick_transfer2` RỖNG trên DB local, không phải lỗi code.
- Vá lỗi #6 ĐÃ CHỨNG MINH: lô (14338 x NV828 x KH1553 x CT4) ra `KTPHHG-00001` +
  link `/admin/warehouse/accounting_prepick_cancels/1/show` — chỗ ERP bỏ trắng.
- Link nội bộ HRM đúng: `PHHG-01652` -> `/finance/prepick-cancels/1652`.
- /export?product_id=5345 -> 23 dòng phẳng, tổng qty 159 (khớp màn).
- /print?product_id=5345 -> 9 phòng ban / 54 dòng; không lọc gì -> 2.503 dòng, `over_limit = true`.
- Phân quyền: NV 27 (có `Quản lý giữ hàng`, KHÔNG có quyền cấp nào) -> chỉ thấy 70 hàng hoá của
  chính mình, mở chi tiết chỉ ra 1 nhân viên là chính mình -> FAIL-CLOSED chạy đúng.
  NV 25 (không có quyền) -> 403.
```

---

## Phase 3 — FE: bảng 3 tầng + bộ lọc

- [x] Tạo `pages/finance/prepick-stocks/index.vue`.
      Mixin đủ 4: `PageTitleMixin`, `filterStateMixin`, `columnCustomizationMixin`,
      + kiểm quyền (`CheckPermission` / cờ từ BE).
      `localStorageKey = 'finance-prepick-stocks-filter'`,
      `columnScreenKey = 'finance_prepick_stocks'` — grep kiểm **không trùng** màn khác.
- [x] `initialStateForm` khai **đủ** `company_id` / `department_id` / `part_id` / `employee_id`
      (kể cả `part_id` không dùng — watcher của `V2BaseCompanyDepartmentFilter` vẫn reset nó;
      Vue 2 không reactive với property chưa khai) + `customer_id`, `brand_id`, `model_id`,
      `product_name`, `product_code`, `status`.
- [x] Bộ lọc dùng **`V2BaseSmartFilterPanel` + schema `filterFields`** (9 trường → có popup
      *Cài đặt bộ lọc*). Bỏ prop `title`. Placeholder đúng chuẩn `Chọn <X>` / `Nhập <X>`,
      **không** dùng option "Tất cả".
- [x] Ô lọc **Công ty** chỉ hiện khi BE trả cờ cho phép xem đa công ty
      (`:disable_part="true"` cho khối tổ chức vì màn không lọc theo bộ phận).
- [x] Nút **Làm mới** xoá điều kiện **và gọi lại** danh sách (bẫy đã biết, ERP quên — lỗi #7).
- [x] Bảng tầng 1 `V2BaseDataTable`, 8 cột theo design. Cột **STT kiêm nút ▸/▾**, không tắt được;
      STT dùng `getNumericalOrder(currentPage, pageSize, index)`.
      Cột **Mã hàng hoá** là `<nuxt-link>` thật. Chữ để **thường**, không `font-weight-bold`.
      Căn lề: STT giữa · số/SL phải · chữ trái. Ô rỗng in `—`.
- [x] Sort: `@sort` **kèm đủ** `:sortBy` + `:sortDirection` (thiếu là không sắp giảm dần được).
      `key` cột sortable phải **trùng tên trường BE**. Mặc định `name ASC`.
- [x] Cột **Đơn vị** là `V2BaseSelect` trên từng dòng. Đổi đơn vị → quy đổi
      `SL giữ`, `Tổng SL trong kho` **và mọi số lượng ở tầng 2, 3** của dòng đó:
      `roundDown(qty / unit_coefficient, 2)`. Hệ số lưu ở dòng tầng 1, tầng con đọc lên.
- [x] Khối chi tiết tầng 2+3 chèn ngay dưới dòng đang mở (pattern
      `prospective-projects/index.vue`): lazy load 1 lần, cache theo `product_id`,
      icon `ri-loader-4-line spin` khi đang tải, `ri-arrow-down-s-line` / `ri-arrow-right-s-line`.
      Đổi bộ lọc / lật trang → **xoá cache và đóng hết** các dòng đang mở.
- [x] Tầng 2: Nhân viên · Phòng ban · Đang giữ. Tầng 3: Khách hàng (`mã – tên`) · SL giữ ·
      Hạn giữ (`dd/mm/yyyy`) · Trạng thái · Hành động.
- [x] Trạng thái dùng `V2BaseBadge` + helper `utils/statusBadgeVariant.js`, text lấy từ
      `status_text` của BE. Trong hạn = xanh · Đến hạn = cam · Hết hạn = đỏ.
      **Không** tự viết `statusPillClass()` / `<span class="status-pill">`.
- [x] Nút **Lịch sử giữ hàng** ở tầng 3 — icon `ri-history-line`. Chỉ 1 hành động nên
      **không** dùng `V2BaseRowActions`; dùng `V2BaseIconButton` trực tiếp.
- [x] Bảng trống hiện dòng "Không có dữ liệu phù hợp".
- [x] Gắn `link: '/finance/prepick-stocks'` vào `components/subsystem-menu/finance.js:150`.
- [x] Bấm thật **từng ô lọc**, đối chiếu param trên tab Network với `applyFilters` của BE.

### Checkpoint — Phase 3

```text
Vừa hoàn thành: `pages/finance/prepick-stocks/index.vue` (bảng 3 tầng + 7 ô lọc + cấu hình cột)
+ gắn `link` cho mục menu "Danh sách hàng giữ".
Đang làm dở: không.
Bước tiếp theo: Phase 4 — popup Lịch sử giữ hàng.
Blocked: không.
Verify: template + script compile sạch (`vue-template-compiler` + `@babel/core`).
Đối chiếu bộ lọc với SQL trực tiếp — KHỚP TUYỆT ĐỐI:
  status=1 -> 284 · status=2 -> 714 · status=3 -> 127 · company_id=4 -> 520
  (bằng đúng `COUNT(DISTINCT product_id)` tương ứng trên `prepick_details`).
  brand_id=375 -> 2 · product_code=JONN -> 156 · product_name=Ampe -> 3.
Sort `prepick_qty desc` -> 305 / 200 / 200, đúng thứ tự giảm dần.
`columnScreenKey = finance_prepick_stocks` KHÔNG trùng màn nào khác (grep toàn repo).

⚠ 2 điểm phải chỉnh so với plan gốc:
1. `V2BaseDataTable` KHÔNG hỗ trợ `sortKey` riêng — nó emit thẳng `column.key`. Đã đổi
   `SORTABLE_COLUMNS` bên BE sang đúng tên cột FE (`product_code`/`product_name`/`brand_name`/
   `model_name`/`prepick_qty`/`total_stock_qty`) thay vì bắt FE map.
2. `V2BaseCompanyDepartmentFilter` TỰ render một select gắn vào `form.employee_id`. Để nguyên là
   2 ô cùng ghi 1 key, đè nhau -> đã bật `:disable_employee="true"` và giữ ô "Nhân viên giữ" riêng
   (chỉ liệt kê người thực sự đang giữ hàng, tự thu hẹp theo Công ty/Phòng ban đang chọn).

⚠ Cột Mã hàng hóa để CHỮ THƯỜNG chứ không phải `<nuxt-link>`: HRM chưa có màn chi tiết hàng hóa
(`pages/finance/products` không tồn tại). Có màn đó rồi thì đổi lại theo quy tắc chung.

⚠ Ô "Đơn vị" chỉ dựng select khi hàng hóa có >= 2 ĐVT — thực tế 890/895 hàng hóa đang giữ chỉ có
ĐÚNG 1 đơn vị.
```

---

## Phase 4 — Popup Lịch sử giữ hàng

- [x] Tạo `components/finance/prepick/PrepickStockLogModal.vue`.
      Copy **vỏ** `b-modal` từ `PrepickHistoryModal.vue` (`size="lg"`, header icon tròn, nút Đóng
      trong `modal-footer`). **Không** dùng lại `PrepickHistoryPanel` — khác hẳn nguồn dữ liệu.
- [x] Khối thông tin đầu popup: Mã hàng · Tên hàng · Kinh doanh (`mã NV – tên`) · Khách hàng
      (`mã – tên`) · Trạng thái + `( Hạn giữ hiện tại: dd/mm/yyyy )`.
- [x] Bảng sổ biến động: STT · SL biến động · Ngày · SL giữ · Hạn giữ · Chứng từ.
      Dòng tiêu đề phụ "Số lượng giữ hiện tại: `<SL>`" như ERP.
      Số căn phải, ngày căn giữa, chứng từ căn trái. `SL biến động` âm hiển thị dấu `-`.
- [x] Cột **Chứng từ**: `<a target="_blank">{{ code }}</a>` khi có `url`; chỉ có `code` thì in
      chữ thường; không có gì thì `—`. **Không** `v-html` chuỗi từ BE.
- [x] Số lượng trong popup quy đổi theo **đơn vị đang chọn ở dòng tầng 1**.
- [x] Trạng thái tải / lỗi / rỗng: spinner · "Không tải được lịch sử giữ hàng" + nút Thử lại ·
      "Chưa có biến động nào".

### Checkpoint — Phase 4

```text
Vừa hoàn thành: `components/finance/prepick/PrepickStockLogModal.vue` (dựng trên khuôn chung
`V2BaseModal`, KHÔNG dùng lại `PrepickHistoryPanel`).
Đang làm dở: không.
Bước tiếp theo: Phase 5 — Xuất Excel.
Blocked: không.
Verify: endpoint /logs trả đúng cho 3 lô khác nhau; cột Chứng từ dựng được link cho 10/11 loại
`objectable_type`. Loại còn lại (`PrepickTransfer2`) không ra chứng từ vì bảng `prepick_transfer2`
RỖNG trên DB local — không phải lỗi code.
```

---

## Phase 5 — Xuất Excel

- [x] BE `exportData($request)` — **phẳng 1 dòng = 1 lô**, dùng **chung** `applyViewScope` +
      `applyFilters` với màn danh sách (vá lỗi #4: ERP khoá cứng công ty người đăng nhập).
      Trạng thái tính bằng `CURDATE()` (vá lỗi #5).
      Trả **đủ** 13 trường kể cả cột đang ẩn ở màn (nếu không user tick xong ra cột trống).
- [x] FE `pages/finance/prepick-stocks/components/export-excel.js` — copy pattern từ
      `prepick-cancels/components/export-excel.js`.
- [x] Bấm **Xuất Excel** → mở `@/components/modal/export-fields-modal.vue` chọn trường **trước**,
      KHÔNG tải thẳng. Thứ tự cột trong file theo đúng thứ tự user tick.
- [x] Tự gắn `Authorization` cho request tải (bẫy `$axios` thiếu token → 401).
- [x] 2 bẫy ExcelJS: ép kiểu số cho cột số (tránh "Number stored as text");
      set `alignment` **sau** khi set `column` (không thì bị ghi đè).
- [x] Nút khoá khi đang xuất + có dòng tiến độ.
- [x] Đối chiếu: tổng `SL giữ` trong file Excel = tổng `SL giữ` mọi trang của màn cùng bộ lọc.

### Checkpoint — Phase 5

```text
Vừa hoàn thành: `pages/finance/prepick-stocks/components/export-excel.js` + nút Xuất Excel qua
popup `ExportFieldsModal` (KHÔNG tải thẳng).
Đang làm dở: không.
Bước tiếp theo: Phase 6 — Bản in.
Blocked: không.
Verify: /export?product_id=5345 -> 23 dòng phẳng, tổng qty 159 — KHỚP `prepick_qty` của tầng 1 và
khớp tổng tầng 2. Bộ trường xuất 12 cột, có đủ cả cột đang ẩn ở màn.

⚠ Số lượng trong file Excel theo ĐƠN VỊ CƠ BẢN, không theo đơn vị đang chọn trên màn: mỗi dòng là
một hàng hóa khác nhau nên quy đổi theo lựa chọn của một dòng sẽ sai cho các dòng còn lại. Cột ĐVT
nói rõ đang tính theo gì.
```

---

## Phase 6 — Bản in

- [x] BE `printData($request)` — gom **Phòng ban → Nhân viên → Hàng hoá** (giữ bố cục ERP),
      dùng **chung** `applyViewScope` + `applyFilters`.
      Trả kèm `count_employees` / `count_products` mỗi cấp để in dòng tiêu đề nhóm.
- [x] Chặn khi vượt ngưỡng: > 400 dòng → trả cờ + thông báo yêu cầu thu hẹp bộ lọc
      (ERP dồn sang gửi mail bằng `PrepickIndexMailJob`, HRM **không** port cơ chế này).
- [x] Tạo `pages/finance/prepick-stocks/print.vue`, khổ **ngang**. Cấu trúc:

```
1     <Phòng ban> – N nhân viên – M mục hàng
1.1     <Nhân viên> – K mục hàng
1.1.1     Tên hàng | Mã hàng | ĐVT | SL giữ | Hạn giữ | Khách hàng | Trạng thái
```

- [x] Áp `print-page` skill: letterhead công ty, `@media print` không mất viền phải/dưới,
      không mất chữ đậm (`b`/`strong` bị ép `font-weight: 500`), tự bật hộp thoại in,
      `table.no-border` không bị padding thừa.
- [x] Số lượng in theo **đơn vị cơ bản** (bản in không có bộ chọn đơn vị) — ghi rõ cột ĐVT.

### Checkpoint — Phase 6

```text
Vừa hoàn thành: blade `Modules/Finance/Resources/views/prints/prepick-stock-list.blade.php` +
`renderPrintList()` + `pages/finance/prepick-stocks/print.vue` (khổ ngang).
Đang làm dở: không.
Bước tiếp theo: Phase 7 — Verify tổng + bàn giao.
Blocked: không.
Verify: /print?product_id=5345 -> 9 phòng ban / 54 dòng, template 13.090 ký tự.
Không lọc gì -> 2.503 dòng, `over_limit = true`, template `null`, FE hiện lời nhắc thu hẹp bộ lọc.

⚠ KHÔNG dùng helper `formatCurrency()` của ERP cho cột SL giữ: helper đó ngăn nghìn bằng `,`
(kiểu Mỹ), ngược quy ước HRM. Đã viết `qtyText()` riêng trong service (`.` nghìn, `,` thập phân).
⚠ CSS in khai đè `#content .pr-group td { font-weight: 700 !important }` vì `print-app.css` ép
`font-weight: 500` toàn trang làm mất đậm dòng nhóm (project_print_bold_lost_font_weight_500).
```

---

## Phase 7 — Verify tổng + bàn giao

- [x] Chạy **checklist tự kiểm** của skill `erp-to-hrm-screen` mục A, B, C, F, G
      (mục D/E/H không áp dụng — màn chỉ đọc, không form, không bản ghi khoá).
- [x] Grep sạch trên **cả thư mục feature**:

```bash
grep -rn "status-pill\|statusPillClass"   pages/finance/prepick-stocks components/finance/prepick
grep -rn "interactable:\|disabledTitle"   pages/finance/prepick-stocks
grep -rn "action\.key ==="                pages/finance/prepick-stocks
grep -rn "V2BaseFilterPanel"              pages/finance/prepick-stocks
grep -rn "advanced-filters"               pages/finance/prepick-stocks
```

- [x] **Chứng minh không ghi gì**: chạy lại 2 câu SQL của Phase 0 sau khi bấm hết màn —
      `prepick_details` và `prepick_logs` phải **y nguyên số dòng và SUM(qty)**.
- [x] Grep toàn service mới, xác nhận **không có** `insert(` / `update(` / `delete(` / `->save(`.
- [x] Đối chiếu 2 cổng cùng bộ lọc bằng **tài khoản thường** (không phải Tổng giám đốc):
      số hàng hoá tầng 1, tổng SL giữ, tổng SL trong kho phải khớp ERP.
- [x] Với tài khoản **xem toàn tổng công ty**: bản in/xuất HRM sẽ ra **nhiều dòng hơn** ERP —
      đúng ý đồ (vá lỗi #4). Ghi rõ vào bảng "Khác ERP có chủ ý".
- [x] Test với tài khoản **có `Quản lý giữ hàng` nhưng KHÔNG phải Super admin**, và tài khoản
      **không có quyền** (phải không thấy menu + API trả 403).
- [x] Cập nhật `.plans/gop-db/STATUS.md`.

### Verify trên trình duyệt (Playwright, tài khoản DNS Admin)

- [x] Màn load: 10/895 dòng, phân trang, toolbar In / Xuất Excel / Cấu hình cột đủ.
- [x] Bấm ▸ mở cây: tầng 2 (`row-employee`, nền xanh) + tầng 3 (`row-lot`, nền xanh dương) hiện
      đúng — Tổng SL kho 20 · SL giữ 6 · NV "Đàm Phước Nhiên / Phòng KD Khu vực 2" · lô 6, hạn
      15/08/2026, badge `v2-badge--required` (đỏ) "Hết hạn".
- [x] Nút **Lịch sử giữ hàng** ở tầng 3 render và bấm được; popup hiện đủ khối thông tin + dòng
      "Số lượng giữ hiện tại: 6 Cái." + sổ biến động, cột Chứng từ ra link `PXG-02132`.
- [x] Lọc `product_name=Ampe` -> 3 dòng (khớp SQL), và cây **tự đóng hết + xoá cache**
      (`expandedIds` 0, `detailsByProduct` 0).
- [x] Bấm header **SL giữ** -> gửi `sort_by=prepick_qty&sort_dir=asc`, bảng đổi đúng.
- [x] `?product_id=5345` -> đúng 1 hàng hóa, SL giữ 159 (khớp probe BE).
- [x] Bản in: letterhead công ty + gom 3 cấp 1 / 1.1 / 1.1.1 đúng mẫu ERP.
- [x] Popup **Chọn trường xuất Excel** mở đúng, 12/12 trường, có dòng nhắc thứ tự cột theo thứ tự tick.
- [x] **Console 0 lỗi** trên cả màn danh sách lẫn màn in.

3 lỗi CHỈ trình duyệt mới lộ, đã sửa:

| # | Lỗi | Sửa |
|---:|---|---|
| 1 | `V2BaseDataTable.sortDirection` có validator chỉ nhận `'asc'`/`'desc'`; lúc chưa sắp xếp `sort.direction` là chuỗi rỗng -> **Vue warning đỏ mỗi lần render** | truyền `sort.direction \|\| 'asc'` |
| 2 | Bản in ra **"Ngày lập: Ngày in: 18/08/2026"** — `_layout` in cứng nhãn "Ngày lập:" cho biến `createdAt`, mà báo cáo tra cứu không có ngày lập | `createdAt => null`, đưa "Ngày in" xuống `infoRows` |
| 3 | **Không đọc `?product_id=` từ query string** — ERP có (`getParam('product_id')`), và màn "Báo cáo hàng sắp về" (`arriving_report.blade.php:184`) link thẳng sang kèm tham số này. Bỏ sót là link cũ chết | khai `product_id` trong `initialStateForm` + đọc `$route.query.product_id` ở `mounted()` (đè bộ lọc đã lưu) |

⚠️ Lỗi #1 và #2 **tồn tại sẵn ở các màn đã port trước đó** (cùng pattern). User chốt 2026-08-18
"lỗi thì cứ fix đi" -> ĐÃ SỬA LUÔN:

- Lỗi #1 (`sortDirection`): `pages/finance/prepick-cancel-requests/index.vue:55` ·
  `pages/finance/prepick-cancels/index.vue:29` ·
  `pages/finance/product-import-direct-transfers/index.vue:56`.
  (11 màn Tài chính khác dùng `filters.sort_desc ? 'desc' : 'asc'` — luôn ra giá trị hợp lệ,
  KHÔNG dính lỗi, không đụng tới.)
- Lỗi #2 (nhãn "Ngày lập:" thừa trên bản in danh sách):
  `Modules/Finance/Resources/views/prints/prepick-cancel-request-list.blade.php` ·
  `prepick-cancel-list.blade.php` — chuyển `$filterText` từ `createdAt` xuống `infoRows` thành
  dòng **"Khoảng thời gian"**, bọc `array_filter` để không lọc ngày thì dòng đó không hiện.
  KHÔNG sửa `_layout.blade.php` (file dùng chung của 5 mẫu in).

Verify lại sau khi sửa (Playwright):
- 3 màn danh sách `prepick-cancel-requests` / `prepick-cancels` / `product-import-direct-transfers`
  đều load được, **console 0 lỗi** (trước đó có warning `sortDirection`).
- Bản in `prepick-cancel-requests/print-list?startDate=2026-01-01&endDate=2026-08-18` ->
  "Khoảng thời gian: Từ ngày 01/01/2026 đến ngày 18/08/2026" + "Tổng số phiếu: 0",
  KHÔNG còn dòng "Ngày lập:".
- Bản in `prepick-cancels/print-list` cùng bộ lọc -> "Tổng số phiếu: 2142", bảng render đủ.

---

### Checkpoint — Phase 7

```text
Vừa hoàn thành: chạy checklist tự kiểm + grep quy chuẩn + chứng minh không ghi dữ liệu.
Đang làm dở: không.
Bước tiếp theo: bàn giao — user bấm tay trên trình duyệt và đối chiếu 2 cổng trên dev.
Blocked: không.

Verify:
- **prepick_details 53.832 dòng (SUM qty = 6.112) · prepick_logs 110.744 dòng — Y NGUYÊN Phase 0.**
- Grep service + controller: 0 lệnh `insert(` / `update(` / `delete(` / `save(` / `DB::statement` /
  `increment(` / `decrement(` / `truncate(`.
- Grep FE 5/5 sạch: không `status-pill`/`statusPillClass`, không `interactable:`/`disabledTitle`,
  không `action.key ===`, không `V2BaseFilterPanel` (chỉ xuất hiện trong comment giải thích),
  không `advanced-filters`.
- Phân quyền: NV 13 (Super admin) 895 hàng hóa · NV 27 (có `Quản lý giữ hàng`, không có quyền cấp
  nào) chỉ 70 hàng hóa của chính mình và mở chi tiết chỉ ra chính mình · NV 25 (không quyền) 403.

ĐÃ verify trên trình duyệt bằng Playwright — xem mục "Verify trên trình duyệt" ở trên.

CHƯA làm (user làm):
- Đổi đơn vị trên 5 hàng hóa có >= 2 ĐVT (đều không nằm ở trang đầu, chưa lần ra để bấm).
- Ctrl+P thật để kiểm viền / chữ đậm khi in ra giấy (Playwright chạy render phần mềm, không tin
  được về artifact in ấn).
- Đối chiếu số liệu với cổng ERP bằng tài khoản thường.
```

---

## Phase 8 — Vá bug QA (redmine 11116, 2026-08-21)

- [x] Bộ lọc bám lại ERP: thêm **"Lọc theo kho"** (`warehouse_id`) và ô **"Tên hàng hóa"**; bỏ
      dropdown **Khách hàng**; ô tìm nhanh đổi thành **"Nhập tên, SĐT hoặc mã KH để tìm kiếm"**
      (`customer_keyword`, LIKE trên `customers.fullname / code / mobile` — cột SĐT tên là
      `mobile`); nhãn "Nhân viên giữ" → **"Nhân viên"**.
- [x] "Lọc theo kho" đặt trong `applyProductFilters()` dưới dạng `whereExists` trên
      `accounting_stocks` → tầng 1, Xuất Excel và Bản in dùng chung một điều kiện. Tồn GIỮ không
      gắn kho nên lọc theo kho = "hàng hoá có tồn kho kế toán ở kho đã chọn", đúng cách ERP làm
      (`checkData()` lọc `stocks.warehouse_id`). Dropdown kho lấy từ `accounting_warehouses`, lọc
      theo công ty người dùng được xem.
- [x] **Ngưỡng in 400 → 10.000 dòng** (`PrepickStockReportService::PRINT_LINE_LIMIT`). Ngưỡng 400
      chép từ ERP, nhưng ERP vượt ngưỡng thì **gửi mail** (`PrepickIndexMailJob`) còn HRM không port
      hạ tầng đó → bộ lọc mặc định ra 2.503 dòng là KHÔNG in được. Dữ liệu vốn đã nạp hết trong
      `flatQuery()`, phần tốn thêm chỉ là render HTML.
- [ ] User bấm tay lại trên dev rồi đóng issue.

### Checkpoint — Phase 8

```text
Vừa hoàn thành: redmine 11116 (BE `PrepickStockReportService` + FE `pages/finance/prepick-stocks/index.vue`).
Đang làm dở: không.
Bước tiếp theo: user verify bộ lọc mới + in thử danh sách đầy đủ trên dev.
Blocked: không.
Verify: `php -l`, nạp class qua Laravel bootstrap, compile lại file .vue; các câu SQL mới chạy
thẳng trên `gop_db` (lọc theo kho đầu tiên → 791 hàng hoá; tìm KH theo tên/mã/mobile → 75 dòng tồn giữ).
```

---

## Bẫy đã biết — đọc lại trước mỗi phase

1. **Không đụng file ERP.** `PrepickDetail::searchByFilter()` và `getPrepickDetails()` đang phục
   vụ 6 màn ERP khác (`prepickEmployee`, `expiringPrepick`, `accountingExpiringPrepick`, …).
2. **Không sửa `PrepickStockService.php`** — đang chạy cho 2 màn hủy hàng giữ. Chỉ đọc tham khảo.
3. **Không bulk `preg_replace` + `file_put_contents`.** Regex sai → `null` → file RỖNG.
   Dùng `str_replace`, chuỗi chứa `$` để trong nháy đơn, `wc -l` ngay sau khi ghi.
4. **`$request->get()` KHÔNG đọc JSON body** — luôn dùng `$request->input()`.
5. **Không bao giờ bắn POST/PUT/DELETE vào id thật** khi quét route.
6. `V2BaseRowActions` emit **chuỗi key** → `switch (action)`. (Màn này chỉ 1 hành động nên tránh
   luôn component đó.)
7. `V2BaseButton` **không có** prop `disabled` → ẩn bằng `visible`, đừng disable.
8. Khối tổ chức phải khai `company_id`/`department_id`/`part_id`/`employee_id` trong
   `initialStateForm`, kể cả key không dùng.
9. `@sort` phải kèm `:sortBy` + `:sortDirection`; `key` cột sortable trùng tên trường BE.
10. Cột Mã phải là `<nuxt-link>` (chuột phải mở tab mới được), không `@click` trên `<div>`.
11. Đổi số dòng/trang → nhảy về trang 1. STT dùng `getNumericalOrder`, không `index + 1`.
12. `.table-responsive` đặt `min-height: 50vh` để dropdown trong bảng không bị cắt.
13. Cờ quyền **fail-closed**, không bao giờ hard-code `= true`.
14. Toast lấy **nguyên văn** bảng QLDA, không tự chế câu.
15. Trên Windows: không `taskkill` theo tên tiến trình, không xoá bằng wildcard, không `sed -i`
    hàng loạt (đổi EOL → conflict giả "cả file").

---

## Bàn giao — việc còn lại

### Cần chạy khi deploy

- Không có migration. Không có seeder. Chỉ cần deploy code + clear cache route/config.

### Chưa làm — cần user/QA

- Đổi **Đơn vị** trên 5 hàng hóa có >= 2 ĐVT, kiểm quy đổi lan đúng xuống tầng 2, tầng 3 và popup
  Lịch sử giữ hàng (890/895 hàng hóa chỉ có 1 ĐVT nên chưa lần ra được để bấm thử).
- `Ctrl+P` bản in ra giấy: không mất viền phải/dưới, không mất chữ đậm dòng nhóm, tiêu đề bảng lặp
  mỗi trang.
- Xuất Excel: tick 5/12 trường xem có ra đúng 5 cột đúng thứ tự tick không (mới verify popup mở
  đúng, chưa tải file thật).
- **Đối chiếu 2 cổng trên dev** bằng tài khoản THƯỜNG (không phải Super admin): số hàng hóa tầng 1,
  tổng SL giữ, Tổng SL trong kho phải khớp ERP.
- Test bằng tài khoản có `Quản lý giữ hàng` + quyền `Xem phiếu hàng giữ theo phòng ban` (nhánh này
  chưa có tài khoản mẫu trên DB local để thử).

### Điểm KHÁC ERP sẽ thấy ngay khi đối chiếu (không phải bug)

- Tài khoản xem **toàn tổng công ty**: bản in / file xuất của HRM ra **nhiều dòng hơn ERP**. ERP
  khoá cứng `company_id` của người đăng nhập ở `PrepickIndexReportService::getData()` nên chọn
  công ty khác là rỗng (lỗi #4). HRM dùng chung phạm vi với màn danh sách.
- Cột **Nhân viên / Thời hạn ở TẦNG 1 bên ERP** hiển thị dữ liệu của một lô ngẫu nhiên (lỗi #1).
  HRM bỏ hẳn 2 cột đó khỏi tầng 1 — muốn xem thì mở tầng 2.
- Lọc **Khách hàng** rồi xổ chi tiết: ERP vẫn hiện đủ mọi khách (lỗi #3), HRM chỉ hiện khách đã lọc.
- Cột **Chứng từ** trong popup Lịch sử: HRM ra link cho `KTPHHG-*` (phiếu hủy hàng giữ kế toán),
  ERP để trắng (lỗi #6, 1.645 dòng log).
- Ô lọc **Kho** không còn (lỗi #2 — bên ERP dropdown luôn rỗng và query không đọc).

### Lưu ý DB LOCAL (không phải lỗi code, prod sẽ khác)

- Dropdown **Khách hàng** chỉ ra **16/192** giá trị: bảng `customers` thiếu dải id của ERP
  (memory `project_gop_db_customers_thieu_dai_id_erp`). Cột Khách hàng ở tầng 3 vì thế hiện `—`.
- Bảng **`prepick_transfer2` RỖNG** -> log loại `PrepickTransfer2` không dựng được chứng từ.

### Khác ERP có chủ ý (ngoài 10 lỗi đã liệt kê ở design.md)

| # | ERP | HRM | Vì sao |
|---:|---|---|---|
| 1 | Ô lọc **Kho** | **bỏ hẳn** | Dropdown ERP luôn rỗng và BE không đọc; `prepick_details` không gắn kho |
| 2 | Tên param `company` / `department` / `employee` | `company_id` / `department_id` / `employee_id` | Chuẩn `V2BaseCompanyDepartmentFilter` của HRM |
| 3 | Mở màn tự do cho mọi tài khoản | gate quyền `Quản lý giữ hàng` | User chốt 2026-08-18; mọi màn HRM đều có quyền |
| 4 | Phạm vi theo `isRole('Tổng giám đốc')` | theo 3 quyền `Xem phiếu hàng giữ theo ...` | Role ERP guard `web` không tin được trên DB gộp |
| 5 | Chứng từ trả HTML thô `<a>` từ BE | trả `{ code, url }` | Không `v-html` dữ liệu BE |
| 6 | Xuất Excel tải thẳng | popup chọn trường trước | Quy tắc chung SRS |
| 7 | > 400 dòng thì gửi mail | chặn in + báo thu hẹp bộ lọc | Không port hạ tầng job/mail của ERP trong đợt này |
| 8 | Phân trang mặc định 20 | 10 (chọn 5/10/20/50/100) | Quy tắc chung SRS |
