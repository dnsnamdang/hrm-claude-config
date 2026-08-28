# Hàng sắp hết hạn giữ (ERP → HRM) — KHẢO SÁT

- **Trạng thái**: KHẢO SÁT XONG + ĐÃ CHỐT HƯỚNG (2026-08-27) — chưa code, chưa có `plan.md`
- **Phạm vi**: màn `Hàng sắp hết hạn giữ` — báo cáo tra cứu, CHỈ ĐỌC
- **Phân hệ đích**: Tài chính, nhóm menu **Giữ hàng** — placeholder đã có sẵn ở
  `hrm-client/components/subsystem-menu/finance.js:178` (mục `{ label: 'Hàng sắp hết hạn giữ' }`, thiếu `link`)
- **Tiền lệ dùng lại**: [Danh sách hàng giữ](../finance-prepick-stock-list/design.md) —
  **CÙNG một query, cùng một bảng, cùng một bộ lọc**; màn này chỉ khác ở 1 điều kiện ngày

---

## 1. ERP có 2 màn cùng tên "Hàng sắp hết hạn giữ"

| | Bản **cá nhân** | Bản **kế toán** |
|---|---|---|
| Route | `warehouseInfo.expiringPrepick` | `warehouseInfo.accountingExpiringPrepick` |
| Controller | `WarehouseInfosController@expiringPrepick` (dòng 603) | `@accountingExpiringPrepick` (dòng 610) |
| Blade | `warehouse/warehouses/expiringPrepick.blade.php` (283 dòng) | `.../accountingExpiringPrepick.blade.php` (303 dòng) |
| Vào từ menu | Thông báo → `topmenubar.blade.php:851` | Kế toán kho → Giữ hàng → `topmenubar.blade.php:1077` |
| `search.type` gửi lên | `expiring` | `accounting_expiring` |
| Dữ liệu thấy | **CHỈ lô của chính mình** (`employee_id = Auth::user()->id`) | Mọi lô trong phạm vi công ty |
| Bộ lọc | Thương hiệu · Model · Tên hàng · Mã hàng | + **Kho** · **Phòng ban** · **Nhân viên** |
| Cột bảng | 7 cột | + cột **Kho** |

`diff` 2 file: bản kế toán là **tập cha** của bản cá nhân, khác đúng 5 chỗ (3 ô lọc, 1 cột, 1 giá trị `type`).

> Menu HRM `finance.js:178` nằm trong nhóm **Giữ hàng** — đúng vị trí của bản **kế toán**.
> Bản cá nhân là đích của thông báo cron `PrepickWarning` ("Bạn có hàng sắp hết hạn giữ").

---

## 2. Bảng nghiệp vụ (Bước 1 của skill `erp-to-hrm-screen`)

### Nguồn dữ liệu

`prepick_details` (tồn giữ) ⋈ `products` ⋈ `brands` ⋈ `product_models`,
`accounting_stocks` ⋈ `accounting_warehouses` (cột "Tổng SL trong kho").
**Không tạo bảng mới, không migration.**

### Tầng 1 — bảng chính (`PrepickDetail::searchByFilter`, phân trang 20)

| Cột | Nguồn | Ghi chú |
|---|---|---|
| Tên hàng hóa | `p.name` | |
| Đơn vị | `product.units` | select đổi đơn vị → chia `unit_coefficient`, `roundDown` 2 số |
| Kho | `acw.code - acw.name` | **chỉ bản kế toán** |
| Model | `pm.name` | |
| Mã hàng hóa | `p.code` | |
| Thương hiệu | `b.name` | |
| Tổng SL trong kho | `SUM(acs.qty)` | |
| SL giữ | `SUM(pds.qty)` | kèm icon ⓘ mở tầng 2+3 |

### Tầng 2 + 3 — bung chi tiết (`getPrepickDetails`, không phân trang)

- Tầng 2 (gom theo nhân viên): Nhân viên · Phòng ban · Đang giữ
- Tầng 3 (từng lô): Khách hàng (`mã - tên`) · SL giữ · Thời hạn

### Hành động / Xuất / In / Import

**KHÔNG có gì cả.** Không nút thêm/sửa/xóa, không Xuất Excel, không In, không Import.
Toàn màn chỉ có: bộ lọc, bảng, phân trang, và link ⓘ bung chi tiết.

### Quyền

Nhóm route `warehouse_infos` **không có `checkPermission`**; menu cũng không `@can`.
→ ERP mở màn này cho **mọi tài khoản đăng nhập**. Phạm vi dữ liệu chỉ chặn bằng
`Auth::user()->isRole('Tổng giám đốc')` (không phải TGĐ thì ép `company_id` của mình).

### Trạng thái

Màn này **KHÔNG hiển thị cột Trạng thái** (khác màn Danh sách hàng giữ). BE có tính
`status` 1/2/3 trong `getPrepickDetails` nhưng blade không dùng.

---

## 3. Điều kiện "sắp hết hạn" — điểm nghi vấn LỚN NHẤT

`PrepickDetail::searchByFilter()` dòng 63-69 và `getPrepickDetails()` dòng 372-377 dùng **cùng một** điều kiện:

    ? BETWEEN pds.expire_date AND DATE_ADD(pds.expire_date, INTERVAL ? DAY)   -- [hôm nay, warning_day]

Bung ra: `expire_date <= hôm nay` **AND** `expire_date >= hôm nay - warning_day`
→ tức là **hàng ĐÃ hết hạn trong vòng N ngày vừa qua**, KHÔNG phải "sắp hết hạn".

Mọi chỗ khác trong hệ thống dùng chiều **ngược lại**:

| Nơi | Điều kiện |
|---|---|
| `app/Console/Commands/PrepickWarning.php:52` | `expire_date = hôm nay + warning_day` |
| `HomeController.php:2341` | `return_date <= hôm nay + warning_day` |
| HRM `PrepickExtendRequestService::warningDate()` (đã port, user đã chốt) | `expire_date <= hôm nay + warning_day` |

→ **Đề xuất**: bản HRM dùng `expire_date <= CURDATE() + configs.warning_day AND qty > 0`
(đúng nghĩa "sắp hết hạn", đúng với màn Gia hạn hàng giữ đã port). **Cần user xác nhận** vì
số dòng trên màn HRM sẽ khác hẳn ERP — QA đối chiếu 2 cổng sẽ thấy lệch.

---

## 4. Lỗi ERP phát hiện được khi khảo sát

| # | Lỗi | Bằng chứng | Xử lý đề xuất |
|---:|---|---|---|
| E1 | **Bung chi tiết luôn RỖNG.** Blade gửi `stock_id: product.stock_id` nhưng controller đọc `$request->product_id`; mà tầng 1 select `p.id`, **không có** cột `stock_id` → gửi lên `undefined` | `expiringPrepick.blade.php:257` vs `WarehouseInfosController.php:350`. Màn anh em `prepickIndex.blade.php:460` gửi đúng `product_id: product.id` | Gửi đúng `product_id` |
| E2 | Điều kiện ngày ngược nghĩa (mục 3) | | Đảo lại theo `warning_day` xuôi |
| E3 | Ô lọc **Kho** (bản kế toán) không có tác dụng — `searchByFilter` không đọc `$request->warehouse` | `PrepickDetail.php:50-145` | Bỏ ô lọc, hoặc lọc thật qua `accounting_stocks` (chờ chốt) |
| E4 | `GROUP BY pds.product_id` mà vẫn `SELECT pds.employee_id, pds.expire_date` → 2 cột là của **một lô bất kỳ**; bật `ONLY_FULL_GROUP_BY` là văng lỗi | `PrepickDetail.php:54-56` | Đã có cách vá ở `PrepickStockReportService` (lỗi #1) — dùng lại |
| E5 | Tầng 1 lọc theo bộ lọc, tầng 2 lọc bằng bộ khác (không nhận `customer_id`, không nhận `brand/model/name/code`) → bung ra thấy lô không khớp bộ lọc | `getPrepickDetails` chỉ nhận company/department/employee/status | Dùng CHUNG `applyPrepickFilters()` cho cả 2 tầng |
| E6 | Phạm vi dữ liệu dựa `isRole('Tổng giám đốc')` — trên DB gộp role ERP có `guard_name = web`, API spatie trả sai | `PrepickDetail.php:57` | Dùng trait `ChecksEmployeePermission` |
| E7 | Bộ lọc **không nhớ** khi quay lại; không có nút Làm mới | blade không có `onClear` | Áp `filterStateMixin` như mọi màn HRM |

---

## 5. Bên HRM đã có sẵn những gì (mức tái sử dụng rất cao)

| Đã có | File | Dùng được cho màn này |
|---|---|---|
| Toàn bộ truy vấn 3 tầng + phân quyền + đơn vị + tồn kho | `Modules/Finance/Services/PrepickStockReportService.php` (1.190 dòng) | **~90%** — chỉ cần thêm 1 điều kiện ngày |
| `applyViewScope()` / `applyPrepickFilters()` / `applyProductFilters()` / `stockSubQuery()` / `unitsOfProducts()` / `detailsOfProduct()` | cùng file, đều `public` | gọi lại nguyên vẹn |
| Đọc `configs.warning_day` + mốc "sắp hết hạn" | `PrepickExtendRequestService::config()` / `warningDate()` (đang `private`) | **cần tách ra dùng chung** — xem mục 6 |
| Controller + Transformer + route mẫu | `PrepickStockController.php`, `Routes/api.php:590-599` | copy khuôn |
| Màn danh sách 3 tầng (mở/thu ở cột STT, lazy load, đổi đơn vị) | `hrm-client/pages/finance/prepick-stocks/index.vue` (879 dòng) | copy khuôn |
| Quyền vào màn | `Quản lý giữ hàng` (id 100427) | dùng lại |
| Quyền phạm vi dữ liệu | `Xem phiếu hàng giữ theo tổng công ty / công ty / phòng ban` (100839/840/841) | dùng lại |
| Mục menu | `finance.js:178` | chỉ thêm `link` |

**Chốt kỹ thuật đề xuất**: KHÔNG viết service mới. Thêm vào `PrepickStockReportService` một cờ
`expiring_only` mà `applyPrepickFilters()` đọc — một dòng điều kiện, dùng chung cho cả tầng 1,
tầng 2 và bản xuất. Đúng tinh thần Bước 3b của skill (không chép bản thứ hai).

---

## 6. Hàm dùng chung cần tách (Bước 3b — PHẢI hỏi user trước khi sửa)

`PrepickExtendRequestService::config()` và `warningDate()` đang **`private`**, mà màn mới cũng cần
đúng mốc đó. Chép sang bản thứ hai là dính đúng cái bẫy skill cảnh báo.
→ Đề xuất tách thành `Modules/Finance/Services/PrepickConfigService.php` (hoặc đổi 2 hàm thành
`public`), rồi **test lại màn Yêu cầu gia hạn hàng giữ** ngay sau khi tách.

---

## 7. Chênh lệch UI phải xử theo chuẩn HRM (không bê nguyên ERP)

- ERP không có: Cấu hình cột · nhớ bộ lọc · nút Làm mới · placeholder đúng chuẩn · dòng "Không có
  dữ liệu phù hợp" · `V2BaseSmartFilterPanel` → **màn HRM phải có đủ**.
- ERP phân trang 20 → HRM mặc định **10**, chọn 5/10/20/50/100.
- ERP không có cột Trạng thái → HRM **thêm** cột Trạng thái hạn giữ + Hạn giữ bằng `V2BaseBadge` +
  `utils/statusBadgeVariant.js` như màn Danh sách hàng giữ (đã chốt — xem mục 8).
- ERP không có Xuất Excel / In → HRM **bổ sung cả 2** theo khuôn `prepick-stocks` (đã chốt).
- Ô rỗng để **TRỐNG** (rule mới 22/08/2026), số theo chuẩn quốc tế `1,234,567.89`.

---

## 8. Quyết định đã chốt (user, 2026-08-27)

| Điểm | Chốt |
|---|---|
| Màn port | **CHỈ bản kế toán** — `http://erp-crm.eteksofts.com/admin/warehouse/warehouse_infos/accountingExpiringPrepick`. Bản cá nhân KHÔNG port thành màn riêng; ai không có quyền cấp nào thì `applyViewScope()` tự cho thấy đúng lô của mình |
| Điều kiện ngày | **GIỮ NGUYÊN hành vi ERP** — `hôm nay BETWEEN expire_date AND expire_date + warning_day`, tức lô đã quá hạn trong `warning_day` ngày gần đây. KHÔNG sửa cho xuôi (để QA đối chiếu 2 cổng ra cùng số) |
| Cột Trạng thái + Hạn giữ | **CÓ** — `V2BaseBadge` + `utils/statusBadgeVariant.js` |
| Xuất Excel | **CÓ** — popup chọn trường, xuất phẳng, dùng lại khuôn `prepick-stocks/components/export-excel.js` |
| In danh sách | **CÓ** — gom Phòng ban → Nhân viên → Hàng hoá, dùng lại khuôn `prepick-stocks/print.vue` |
| Ô lọc Kho | **BỎ HẲN** (giống màn Danh sách hàng giữ) → cột **Kho** ở tầng 1 cũng bỏ theo, vì `prepick_details` không gắn kho |
| `config()` / `warningDate()` | **TÁCH ra dùng chung**, rồi test lại màn Yêu cầu gia hạn hàng giữ ngay sau khi tách |

### Hệ quả cần biết của quyết định "giữ nguyên hành vi ERP"

Vì bộ lọc gốc chỉ trả lô có `expire_date <= hôm nay`, cột **Trạng thái** trên màn này sẽ **không bao
giờ** ra giá trị *Trong hạn* — chỉ có *Hết hạn* (đa số) và *Đến hạn* (lô hết hạn đúng hôm nay).
Đây là hệ quả đúng của quyết định, không phải bug; ghi lại để lần sau không ai "sửa nhầm".

Ô lọc **Trạng thái** vì thế cũng chỉ nên cho 2 lựa chọn *Hết hạn* / *Đến hạn*, hoặc bỏ luôn — **chốt
khi làm `plan.md`**.

---

## 9. Việc dự kiến (chi tiết hoá khi viết `plan.md`)

**BE** — không tạo service mới:

- `PrepickStockReportService`: thêm cờ `expiring_only` đọc trong `applyPrepickFilters()`
  (1 điều kiện `whereRaw`), áp cho cả tầng 1 / tầng 2 / export / print.
- Tách `config()` + `warningDate()` của `PrepickExtendRequestService` sang service dùng chung
  → **test lại màn Yêu cầu gia hạn hàng giữ**.
- `PrepickExpiringController` (hoặc thêm nhánh vào `PrepickStockController`): 6 endpoint
  `index / meta / details / export / print` — copy khuôn `Routes/api.php:590-599`.
- Vá lỗi E1 (truyền đúng `product_id` xuống tầng 2) và E5 (dùng chung bộ lọc) — **không** vá E2.

**FE**:

- `pages/finance/prepick-expiring/index.vue` + `print.vue` + `components/export-excel.js`,
  copy khuôn `pages/finance/prepick-stocks/`.
- `localStorageKey` / `columnScreenKey` mới: `finance_prepick_expiring` (grep kiểm trùng).
- Gắn `link` vào `components/subsystem-menu/finance.js:178`.

**Migration**: **không có** — dùng lại quyền `Quản lý giữ hàng` (100427) và 3 quyền phạm vi
(100839/840/841).
