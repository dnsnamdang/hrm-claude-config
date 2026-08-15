# Hủy hàng giữ (ERP → HRM) — design

- **Trạng thái**: CODE DONE + ĐÃ VERIFY HTTP END-TO-END (2026-08-15) — xem `./plan.md`
- **Phạm vi**: **2 màn** — `Yêu cầu hủy hàng giữ` + `Phiếu hủy hàng giữ` (user chốt 2026-08-15)
- **Phân hệ đích**: Tài chính — nhóm menu **Giữ hàng**. Cả 2 mục đã có sẵn dạng placeholder trong
  `components/subsystem-menu/finance.js:149-150`, chỉ thiếu `link`
- **Tiền lệ**: làm y hệt quy trình đã dùng cho
  [Phiếu chuyển hàng nhập thẳng](../finance-product-import-direct-transfer/design.md)

---

## Mục tiêu

Đưa trọn luồng **hủy hàng giữ** sang HRM theo bộ chuẩn V2 (list-page skill + entity-history
skill), dùng chung dữ liệu với ERP trên `gop_db` để 2 cổng chạy song song trong giai đoạn
chuyển đổi.

### Nghiệp vụ

Nhân viên kinh doanh đang **giữ hàng** cho một khách hàng — tồn giữ nằm ở `prepick_details`, khóa
theo `employee_id` + `customer_id` + `company_id` + `product_id`, mỗi lô có `expire_date`. Khi
không cần giữ nữa, NV lập **Phiếu yêu cầu hủy hàng giữ** (PYCHHG) liệt kê hàng hóa + số lượng muốn
trả về kho. Kế toán kho (quyền `Quản lý giữ hàng`) xem xét rồi:

- **Không duyệt** → phiếu quay về Đang tạo kèm lý do, hoặc
- **Duyệt** → lập **Phiếu hủy hàng giữ** (PHHG), có thể **cắt bớt số lượng** so với đề nghị. Lúc
  lưu phiếu này tồn giữ mới thực sự bị trừ.

---

## Bảng dữ liệu (dùng chung ERP — không tạo bảng nghiệp vụ mới)

| Bảng | Số dòng (2026-08-15) | Vai trò |
|---|---:|---|
| `prepick_cancel_requests` | 3.521 | phiếu yêu cầu |
| `prepick_cancel_request_details` | 9.956 | dòng hàng của yêu cầu |
| `prepick_cancels` | 3.478 | phiếu hủy |
| `prepick_cancel_details` | 9.752 | dòng hàng của phiếu hủy |
| `prepick_details` | 53.832 | **tồn giữ thật** — bị GHI khi duyệt |
| `prepick_logs` | 110.744 | nhật ký biến động tồn giữ — bị GHI khi duyệt |

3.478 / 3.521 phiếu yêu cầu đã có phiếu hủy tương ứng (quan hệ 1–1).

⚠ **`prepick_details` KHÔNG có `unit_id`** — số lượng tồn giữ luôn tính theo **đơn vị cơ bản**. Trên
form ERP ô "Đơn vị tính" đã bị `disabled` đúng với thực tế này. Bảng chi tiết phiếu vẫn lưu
`unit_id` + `unit_coefficient`, và `cancel_qty = qty × unit_coefficient` là số quy về ĐV cơ bản để
trừ tồn.

⚠ Khi ghi `prepick_logs`, HRM **phải ghi đúng chuỗi lớp của ERP**
`App\Model\Warehouse\PrepickCancel` vào `objectable_type` (đang có 9.908 dòng như vậy) để modal
"Lịch sử giữ hàng" bên ERP vẫn đọc được. Cùng thủ thuật đã dùng ở
`ProductImportDirectDetail::ERP_TRANSFER_PRODUCT_TYPE`.

---

## Hiện trạng ERP

### Màn 1 — Yêu cầu hủy hàng giữ

`PrepickCancelRequestsController` (569 dòng) + `PrepickCancelRequest` (321 dòng) + 7 blade.

Trạng thái đánh số **không theo thứ tự tự nhiên**, phải giữ nguyên vì chung DB:

| Giá trị | Tên | Ghi chú |
|---:|---|---|
| `3` | Đang tạo | bản nháp, chỉ người lập thấy. **Cũng là** trạng thái sau khi bị từ chối (kèm `comment`) |
| `2` | Chờ duyệt | đã gửi |
| `1` | Đã duyệt | do phiếu hủy sinh ra |

Không dùng giá trị `0`. Dữ liệu thực: status `1` = 3.478, status `3` = 43, **không có phiếu nào ở
status `2`**.

2 lối vào menu ERP:

| Route | Nội dung |
|---|---|
| `prepickCancelRequest.index` (`?type=index` / `?type=all`) | `index` = chỉ phiếu của tôi; `all` = áp phạm vi quyền theo cấp |
| `prepickCancelRequest.forAccounting` (middleware `checkPermission:Quản lý giữ hàng`) | `type=accounting` — chỉ phiếu **status 2** cùng công ty |

### Màn 2 — Phiếu hủy hàng giữ

`PrepickCancelsController` (243 dòng) + `PrepickCancel` (286 dòng) + 5 blade.
Chỉ có `index` / `create` / `store` / `show` / `exportList` — **không sửa, không xóa**. Tạo xong là
chốt vĩnh viễn (vì đã trừ tồn). `status` luôn = `1`, không có vòng đời.

Mã phiếu: `PHHG-<5 số>` (yêu cầu là `PYCHHG-<5 số>`).

`store()` chạy 3 việc trong **1 transaction**:

1. Tạo `prepick_cancels` + `syncProducts()` → `prepick_cancel_details`
   (`cancel_qty = qty × unit_coefficient`, `request_qty` chép từ dòng yêu cầu)
2. `updateWarehouse()` — trừ tồn **FIFO theo `expire_date` tăng dần**:

```php
foreach ($this->products as $product) {
    $prepick_details = PrepickDetail::where(product_id, employee_id = <người lập YÊU CẦU>,
                                            customer_id, company_id)
        ->where('qty', '>', 0)->orderBy('expire_date', 'ASC')->get();
    $tmp_qty = $product->cancel_qty;
    foreach ($prepick_details as $prepick) {
        // ghi prepick_logs {qty_before, change (âm), qty_after, objectable = PrepickCancel}
        // trừ dần cho tới khi $tmp_qty == 0
    }
}
```

3. `$parent->approve()` — set yêu cầu về status `1`, `approver_id`, `approved_time`, + thông báo
   cho người lập yêu cầu

⚠ `employee_id` dùng để tìm lô tồn là **người lập YÊU CẦU**, không phải người lập phiếu hủy.

### Nguồn chọn hàng của màn yêu cầu

Popup "Tìm kiếm hàng hóa" đọc thẳng:

```sql
FROM products p
LEFT JOIN prepick_details pd ON pd.product_id = p.id
WHERE p.status != 0 AND pd.qty > 0
  AND pd.employee_id = <người lập>   AND pd.customer_id = <KH đã chọn>
  AND pd.company_id  = <công ty>
GROUP BY p.id ...  -> SUM(pd.qty) AS prepick_qty
```

Sau khi thêm hàng, form gọi `warehouseInfo.stockOfProducts` →
`Product::getAccountingStockDetail()` để lấy:

- **Có thể giữ** (`in_stock`) — tồn kho có thể giữ thêm; chỉ tham khảo trên màn này
- **Có thể hủy** (`prepick_qty`) — `SUM(prepick_details.qty)` **trừ** phần đã nằm trong đề nghị xuất
  kho chưa hoàn thành (`warehouse_export_request_details.export_prepick_qty`)

---

## Phân quyền

Toàn bộ đã có sẵn trên `gop_db`, **guard `web`** (quyền ERP) → phải đọc qua trait
`Modules\Finance\Entities\Concerns\ChecksEmployeePermission`, **KHÔNG** dùng `hasPermissionTo()`.

| ID | Tên quyền | Dùng ở đâu |
|---:|---|---|
| 100427 | `Quản lý giữ hàng` | xem mọi phiếu ≠ nháp, duyệt / không duyệt, lập phiếu hủy, preset "Chờ tôi duyệt" |
| 100839 | `Xem phiếu hàng giữ theo tổng công ty` | phạm vi danh sách — thấy tất cả |
| 100840 | `Xem phiếu hàng giữ theo công ty` | lọc `company_id` |
| 100841 | `Xem phiếu hàng giữ theo phòng ban` | lọc `department_id` theo `employee_manage_departments` |

⚠ Khác màn nhập thẳng: **chỉ 3 cấp**, KHÔNG có cấp "bộ phận" (`part_id`).
Không có quyền riêng cho Thêm/Sửa/Xóa — ai cũng tạo được phiếu yêu cầu của mình.

| Hàm | Điều kiện |
|---|---|
| `canEdit()` (yêu cầu) | `status == 3 && created_by == me` |
| `canDelete()` (yêu cầu) | như `canEdit()` |
| `canApprove()` (yêu cầu) | `status == 2 && can('Quản lý giữ hàng')` |
| `canView()` (phiếu hủy) | quyền `Quản lý giữ hàng`, hoặc là người lập phiếu hủy, hoặc là người lập yêu cầu gốc |

---

## Lỗi ERP phát hiện khi khảo sát

### Màn Yêu cầu

| # | Lỗi | Bằng chứng | Xử lý ở HRM |
|---:|---|---|---|
| 1 | **`print()` chết hẳn** — hằng số `ReportTemplate::YEU_CAU_HUY_HANG_GIU` KHÔNG tồn tại (476 hằng số trong model, không có cái này) → fatal error. Link "In yêu cầu" đã bị comment sẵn | grep `app/` ra 3 chỗ **dùng**, 0 chỗ **định nghĩa**; `report_templates` cũng không có mẫu nào | **Tự dựng mẫu in mới** (user chốt) — xem mục "Mẫu in" |
| 2 | `getPrintDataAttribute()` + `getProductTableAttribute()` là code chết: gọi `$this->parent->code` (không có quan hệ `parent`), lớp `ProductPrepickRequestDetail` (không tồn tại), các trường `customer_name`/`delivery_place`/`customer_type`/`employee_phone`… không có trên bảng | model dòng 91–156 | Bỏ, không port |
| 3 | **`update()` bỏ quên kiểm tra validate** — tạo `$validate` rồi đi thẳng vào `DB::beginTransaction()`, thiếu `if ($validate->fails())`. `store()` thì có → **sửa phiếu bỏ qua toàn bộ validate** | controller dòng 256–262 | FormRequest → validate luôn chạy ở cả tạo và sửa |
| 4 | **Thông báo gửi vào hư không** — gọi `Warehouse::getAccountantIds($object->warehouse_id)` nhưng bảng `prepick_cancel_requests` **không có cột `warehouse_id`** → luôn `null` → trả mảng rỗng. Redis publish vào kênh `"ke_toan_kho"` (thiếu id) | schema bảng + `Warehouse.php:500` | Gửi cho **người có quyền `Quản lý giữ hàng` cùng công ty** qua `EmployeeInfoService::sendNotification` |
| 5 | **`canView()` bỏ qua hoàn toàn 3 quyền theo cấp** — người có `Xem phiếu hàng giữ theo công ty` **thấy** phiếu trong danh sách nhưng bấm vào bị `not_found` | model dòng 294–298 vs 158–184 | `canView()` khớp đúng phạm vi `searchByFilter` (giống FIX #1 màn nhập thẳng) |
| 6 | `searchByFilter` áp trùng điều kiện `created_by = me OR status != 3` hai lần | dòng 179 và 238 | Gộp còn 1 |
| 7 | Số "Đang giữ" trong popup chọn hàng là `SUM(pd.qty)` **thô**, còn cột "Có thể hủy" trên form đã **trừ** phần đang nằm trong ĐN xuất kho chưa xong → 2 số lệch nhau | popup dùng query riêng, form dùng `getAccountingStockDetail` | Popup và form dùng **chung một hàm** → 2 số luôn khớp |

### Màn Phiếu hủy

| # | Lỗi | Bằng chứng | Xử lý ở HRM |
|---:|---|---|---|
| 8 | **`canView()` luôn trả `true`** — nhánh cuối là `return true` thay vì `return false` → ai cũng xem được mọi phiếu hủy | `PrepickCancel.php:240-244` | Cài đúng: quyền `Quản lý giữ hàng` / người lập phiếu / người lập yêu cầu |
| 9 | **Nút "Thêm" trỏ nhầm màn** — `create_link` của danh sách phiếu hủy dùng `route('productImportRequest.create')` (màn Tạo yêu cầu nhập hàng) | `index.blade.php` | HRM không có nút Thêm rời — phiếu hủy chỉ lập từ 1 phiếu yêu cầu |
| 10 | Bộ lọc **Trạng thái** có 3 lựa chọn nhưng 100% dữ liệu là status `1`; bộ lọc **Người duyệt** không được `searchByFilter` xử lý và bảng cũng không có cột `approver_id` → 2 bộ lọc chết | `index.blade.php` vs `searchByFilter` | Bỏ cả 2 bộ lọc chết |
| 11 | Màn xem hiển thị `form.warehouse.name` nhưng không có quan hệ/cột `warehouse` → luôn trống | `show.blade.php` | Bỏ |
| 12 | `searchByFilter` **không áp quyền theo cấp**, chỉ lọc `company_id` của người đăng nhập (dù blade vẫn truyền 3 cờ `is_big_boss`/`is_boss`/`is_manager`) | `PrepickCancel.php:130` | Áp đúng 3 cấp như màn yêu cầu |
| 13 | `updateWarehouse()` **không kiểm tra đủ tồn** — nếu tổng lô còn ít hơn `cancel_qty` thì trừ hết rồi im lặng bỏ qua phần thiếu; và nếu `cancel_qty = 0` vẫn ghi 1 dòng log `change = 0` | model dòng 246–280 | Kiểm tra đủ tồn **trước** khi trừ (khóa `lockForUpdate`), thiếu thì báo lỗi + rollback; bỏ qua dòng `cancel_qty = 0` |

---

## Mẫu in — tự dựng mới (user chốt)

ERP không có mẫu nào trong `report_templates` cho 2 phiếu này. **Không ghi thêm dòng vào
`report_templates`** (bảng dùng chung với ERP — tránh đụng dữ liệu ERP). Thay vào đó dựng mẫu HTML
ngay trong HRM, đặt tại `Modules/Finance/Resources/views/prints/`, bám bố cục 2 mẫu cùng nhóm
(423/424 gia hạn giữ, 425/426 điều chuyển hàng giữ).

4 mẫu:

| Mẫu | Nội dung | Khổ |
|---|---|---|
| `prepick-cancel-request.blade.php` | Phiếu yêu cầu hủy hàng giữ — header công ty, số phiếu, ngày, KH, người/phòng ban yêu cầu, ghi chú, bảng hàng (STT · Tên · Model · Mã · Thương hiệu · ĐVT · SL yêu cầu hủy), khối ký | A4 dọc |
| `prepick-cancel-request-list.blade.php` | Danh sách yêu cầu — 7 cột như file Excel ERP | A4 ngang |
| `prepick-cancel.blade.php` | Phiếu hủy hàng giữ — thêm số phiếu yêu cầu gốc + cột SL yêu cầu / SL duyệt hủy | A4 dọc |
| `prepick-cancel-list.blade.php` | Danh sách phiếu hủy — 6 cột như file Excel ERP | A4 ngang |

Bản in ngang phải khai đè `@page { size: A4 landscape }` trong khối `styles` truyền cho
`$printContent` (plugin không có option landscape — bẫy đã gặp ở màn nhập thẳng).

---

## Cấu trúc code

### BE — `Modules/Finance`

```
Entities/PrepickCancel/
    PrepickCancelRequest.php          # entity yêu cầu: hằng số trạng thái/quyền, can*(), searchByFilter
    PrepickCancelRequestDetail.php
    PrepickCancelRequestHistory.php   # bảng lịch sử MỚI
    PrepickCancel.php                 # entity phiếu hủy
    PrepickCancelDetail.php
    PrepickCancelHistory.php          # bảng lịch sử MỚI
    PrepickDetail.php                 # tồn giữ (bảng ERP `prepick_details`)
    PrepickLog.php                    # nhật ký tồn giữ (bảng ERP `prepick_logs`)
Services/
    PrepickStockService.php                   # DÙNG CHUNG: truy vấn tồn giữ + trừ tồn FIFO
    PrepickCancelRequestService.php
    PrepickCancelRequestHistoryService.php
    PrepickCancelService.php
    PrepickCancelHistoryService.php
Http/Controllers/V1/
    PrepickCancelRequestController.php
    PrepickCancelController.php
Http/Requests/PrepickCancel/
    PrepickCancelRequestRequest.php
    PrepickCancelRequest_StoreRequest.php     # cho phiếu hủy
Resources/views/prints/                       # 4 mẫu in
```

`PrepickStockService` là chỗ duy nhất chạm `prepick_details` / `prepick_logs` — cả popup chọn hàng,
cột "Có thể hủy" và bước trừ tồn FIFO đều gọi vào đây, nên 3 con số luôn nhất quán (sửa lỗi #7).

### API

**Prefix `/v1/finance/prepick-cancel-requests`**

| Method | Path | Việc |
|---|---|---|
| GET | `/` | danh sách (preset `mine` / `all` / `waiting_approve`) |
| GET | `/stock` | ⚑ tĩnh — popup chọn hàng đang giữ |
| GET | `/customers` | ⚑ tĩnh — dropdown KH đang có hàng giữ của người lập |
| GET | `/export` | ⚑ tĩnh — dữ liệu thô xuất Excel |
| GET | `/print-list-data` | ⚑ tĩnh — HTML in danh sách |
| POST | `/` | tạo (status 3 hoặc 2) |
| PUT | `/{id}` | sửa |
| DELETE | `/{id}` | xóa |
| POST | `/{id}/reject` | Không duyệt (bắt buộc `comment`) |
| GET | `/{id}/print-data` | HTML in phiếu |
| GET | `/{id}/histories` | lịch sử thay đổi |
| GET | `/{id}` | chi tiết |

**Prefix `/v1/finance/prepick-cancels`**

| Method | Path | Việc |
|---|---|---|
| GET | `/` | danh sách |
| GET | `/export` | ⚑ tĩnh |
| GET | `/print-list-data` | ⚑ tĩnh |
| GET | `/from-request/{requestId}` | ⚑ tĩnh — nạp dữ liệu lập phiếu hủy từ 1 yêu cầu (gate `canApprove()`) |
| POST | `/` | **lập phiếu hủy = duyệt yêu cầu + trừ tồn FIFO** |
| GET | `/{id}/print-data` | HTML in phiếu |
| GET | `/{id}/histories` | lịch sử |
| GET | `/{id}` | chi tiết |

> Route tĩnh phải khai **TRƯỚC** `/{id}` — bẫy đã dính ở màn nhập thẳng.
> **Không** gắn middleware `checkPermission`/`erpPermission`: trên `gop_db` middleware dùng chung
> resolve qua spatie `getAllPermissions()` nên mismatch `model_type`, người có quyền thật vẫn 403.
> Chặn quyền trong Entity.

### FE

```
pages/finance/prepick-cancel-requests/
    index.vue                                  # danh sách V2
    create.vue   _id/edit.vue   _id/index.vue  # trang vỏ (beforeRouteLeave)
    _id/print.vue   print-list.vue
    components/PrepickCancelRequestForm.vue
    components/PrepickStockSearchModal.vue     # popup chọn hàng đang giữ
    components/HistoryPanel.vue  components/HistoryModal.vue
    components/export-excel.js
pages/finance/prepick-cancels/
    index.vue   create.vue   _id/index.vue   _id/print.vue   print-list.vue
    components/PrepickCancelForm.vue
    components/RequestSearchModal.vue          # popup chọn phiếu yêu cầu chờ duyệt
    components/HistoryPanel.vue  components/HistoryModal.vue
    components/export-excel.js
```

---

## Chi tiết màn — bám bộ chuẩn V2

### Màn 1a — Danh sách Yêu cầu hủy hàng giữ

- **Preset tab**: `Của tôi` · `Tất cả` · `Chờ tôi duyệt` (tab 3 chỉ hiện khi có `Quản lý giữ hàng`)
- **7 cột mặc định**: STT · Mã phiếu (sticky, `.v2-cell-link`) · Người lập · Ngày lập · Trạng thái ·
  Người duyệt · Ngày duyệt — đúng 7 cột danh sách ERP
- **Cột ẩn** (bật qua Cấu hình cột): Khách hàng · Ghi chú · Lý do không duyệt · Phòng ban
- **Bộ lọc** (`V2BaseFilterPanel` + `filterStateMixin`): Mã phiếu · Người lập · Trạng thái ·
  Người duyệt · Tên hàng hóa · Mã hàng hóa · Khoảng ngày lập
- **Sắp xếp**: Mã phiếu, Ngày lập (key cột phải trùng tên trường BE)
- **Hành động**: Sửa · Xóa + menu 3 chấm (`V2BaseRowActions`): Duyệt (→ trang lập phiếu hủy) ·
  Không duyệt · In phiếu · Lịch sử — **disable** chứ không ẩn khi không đủ điều kiện

### Màn 1b — Tạo / Sửa Yêu cầu

Hai khối `form-card`:

1. **Thông tin chung** — Khách hàng (`select2`, bắt buộc, **khóa sau khi đã lưu**) · Ghi chú (≤255)
2. **Chi tiết** — bảng hàng hóa + nút thêm mở popup chọn hàng đang giữ

Cột bảng: STT · Cần hủy (checkbox) · Tên hàng hóa · Model · Mã hàng hóa · Thương hiệu · Có thể giữ ·
Có thể hủy · Yêu cầu hủy (nhập) · ĐVT (khóa, luôn ĐV cơ bản) · Xóa dòng.

Ràng buộc: `Yêu cầu hủy` ≤ `Có thể hủy`; phải có ≥ 1 dòng tick `Cần hủy` và `qty > 0` mới gửi được;
đổi Khách hàng ⇒ nạp lại toàn bộ số tồn giữ.

Footer `V2Footer`: **Lưu nháp** (status 3) · **Gửi duyệt** (status 2) · **Quay lại**.
Dùng `unsavedChangesMixin` + `formValidateMixin`.

### Màn 1c — Chi tiết Yêu cầu

Chỉ đọc, thêm cột **Duyệt hủy** (số lượng thực tế đã hủy, đọc từ `prepick_cancel_details`). Có khối
**Lý do không duyệt** khi có `comment`, link sang phiếu hủy tương ứng, và section **Lịch sử thay đổi**
ở cuối trang. Nút **Duyệt** / **Không duyệt** khi `canApprove()`.

### Màn 2a — Danh sách Phiếu hủy hàng giữ

- **6 cột**: STT · Mã phiếu (sticky, `.v2-cell-link`) · Phiếu yêu cầu (link) · Người yêu cầu ·
  Người lập · Ngày lập
- **Cột ẩn**: Khách hàng · Ghi chú
- **Bộ lọc**: Mã phiếu · Tên/mã hàng hóa · Người yêu cầu · Người lập · Khoảng ngày lập
  (bỏ 2 bộ lọc chết — lỗi #10)
- **Không có nút Thêm** (lỗi #9) — phiếu hủy chỉ lập từ 1 phiếu yêu cầu chờ duyệt
- **Hành động**: In phiếu · Lịch sử (không Sửa / Xóa — ERP cũng không có)

### Màn 2b — Lập Phiếu hủy (= duyệt yêu cầu)

Vào từ nút **Duyệt** ở màn yêu cầu (`?request_id=...`), hoặc mở trống rồi chọn phiếu yêu cầu qua
popup (lọc sẵn status = 2, cùng công ty).

1. **Thông tin chung** (chỉ đọc trừ Ghi chú) — Phiếu yêu cầu · Người yêu cầu · Phòng ban yêu cầu ·
   Khách hàng · Ghi chú
2. **Chi tiết** — STT · Cần hủy (checkbox) · Tên hàng hóa · Model · Mã hàng hóa · Thương hiệu ·
   Có thể hủy · Yêu cầu hủy · **Duyệt hủy (nhập)** · ĐVT

Ràng buộc: `Duyệt hủy` ≤ `Có thể hủy` (tồn giữ hiện tại, tính lại tại thời điểm mở form) **và**
≤ `Yêu cầu hủy`; ≥ 1 dòng tick + `qty > 0`.

Footer: **Duyệt** · **Quay lại**. Nút Duyệt kèm hộp xác nhận nêu rõ "sẽ trừ tồn giữ, không hoàn tác
được".

Xử lý phía BE trong 1 transaction: `lockForUpdate` các lô `prepick_details` → kiểm tra đủ tồn (sửa
lỗi #13) → tạo phiếu hủy + chi tiết → trừ FIFO + ghi `prepick_logs` → set yêu cầu về Đã duyệt →
ghi 2 bản ghi lịch sử → thông báo người lập yêu cầu.

### Màn 2c — Chi tiết Phiếu hủy

Chỉ đọc: thông tin chung + bảng (Yêu cầu hủy / Duyệt hủy) + link về phiếu yêu cầu + section Lịch sử.

### Xuất Excel

| Màn | Cột |
|---|---|
| Yêu cầu | STT · Mã phiếu · Người lập · Ngày lập · Trạng thái · Người duyệt · Ngày duyệt |
| Phiếu hủy | STT · Mã phiếu · Phiếu yêu cầu · Người yêu cầu · Người lập · Ngày lập |

Đúng như 2 file Excel ERP. Dựng bằng ExcelJS ở FE theo convention; BE chỉ trả dữ liệu thô +
`filter_text`. Nhớ 2 bẫy ExcelJS: mã phiếu/ngày ghi dạng chuỗi; căn lề đặt trên **từng ô**.

---

## Lịch sử thay đổi — tính năng MỚI (ERP không có)

2 bảng mới, cùng khuôn 9 cột với `product_import_direct_transfer_history`:

- `prepick_cancel_request_history` — hành động: `create` · `update` · `send_approve` · `reject` ·
  `approve`
- `prepick_cancel_history` — hành động: `create` (kèm snapshot số lượng đã trừ mỗi dòng)

Migration đặt ở **`hrm-api/database/migrations/`** (không đặt trong `Modules/*`), đặt tên index thủ
công để không vượt 64 ký tự của MySQL.

Ghi diff dạng subset, snapshot lưu **giá trị hiển thị**, sắp xếp **mới → cũ**, xuất hiện ở **cả 2
nơi**: popup ⋮ ở màn danh sách và section ở màn chi tiết.

Dòng hàng hóa dùng khóa `product_id` (không cần `unit_id` vì luôn ĐV cơ bản) do `syncProducts`
**xóa rồi tạo lại** toàn bộ chi tiết mỗi lần lưu.

---

## Rủi ro / điểm cần canh

1. **Ghi vào tồn thật** — đây là khác biệt lớn nhất so với màn nhập thẳng. `prepick_details` 53.832
   dòng, `prepick_logs` 110.744 dòng. Bắt buộc backup 4 bảng này trước khi test, và **chỉ thao tác
   trên phiếu tự tạo**.
2. **Không được bắn POST/PUT/DELETE vào id thật** khi quét route — bài học đã trả giá ở màn nhập
   thẳng (lỡ duyệt thật 1 phiếu, phải khôi phục từ backup).
3. **Không có phiếu status 2 nào trên DB local** → phải tự tạo phiếu test cho luồng
   Chờ duyệt / Không duyệt / Duyệt.
4. **Chạy song song 2 cổng** — phiếu tạo ở HRM phải hiện đúng ở ERP và ngược lại; `prepick_logs` do
   HRM ghi phải hiện đúng trong modal "Lịch sử giữ hàng" của ERP. Bắt buộc đối chiếu tay trên dev.
5. Sinh mã `PYCHHG-` / `PHHG-` từ `id` — 2 cổng chung bảng nên không đụng nhau.
6. `BaseModel` của HRM ghi đè `created_by` — đã có bẫy ở màn trước, phải kiểm lại khi tạo phiếu.
7. `prepick_cancels.company_id` lấy từ **người lập phiếu hủy** (kế toán), còn lô tồn tìm theo
   `company_id` đó + `employee_id` của **người lập yêu cầu**. Nếu 2 người khác công ty thì ERP tìm
   không ra lô nào và trừ hụt im lặng → HRM phải chặn (thuộc lỗi #13).

---

## Liên quan

- Màn tiền lệ: [`finance-product-import-direct-transfer`](../finance-product-import-direct-transfer/design.md)
- 2 màn cùng nhóm sẽ làm tiếp: Yêu cầu gia hạn giữ hàng, Phiếu điều chuyển hàng giữ — dùng lại
  `PrepickStockService` + popup chọn hàng giữ + bộ quyền của đợt này
- Còn 1 màn cùng họ chưa tính: **Phiếu hủy hàng giữ kế toán** (`accounting_prepick_cancels`) —
  ngoài phạm vi đợt này
- Skill: `list-page`, `entity-history`
