# Danh sách hàng giữ (ERP → HRM) — design

- **Trạng thái**: CODE DONE + ĐÃ VERIFY HTTP (2026-08-18) — xem `./plan.md`
- **Phạm vi**: **1 màn** — `Danh sách hàng giữ` (báo cáo tra cứu, CHỈ ĐỌC)
- **Phân hệ đích**: Tài chính — nhóm menu **Giữ hàng**, mục placeholder đã có sẵn ở
  `components/subsystem-menu/finance.js:150`, chỉ thiếu `link`
- **Tiền lệ**: dùng lại hạ tầng của
  [Hủy hàng giữ](../finance-prepick-cancel-request/design.md) (`PrepickDetail`, `PrepickLog`,
  trait `ChecksEmployeePermission`)

---

## Mục tiêu

Đưa màn tra cứu **tồn hàng giữ** sang HRM. Đây là màn **báo cáo, không phải phiếu**: không tạo,
không sửa, không xóa, **không ghi một dòng nào** vào `prepick_details` / `prepick_logs`.

### Nghiệp vụ

Nhân viên kinh doanh giữ hàng cho khách — mỗi lô nằm ở `prepick_details`, khóa theo
`employee_id` × `customer_id` × `company_id` × `product_id`, kèm `expire_date` (hạn giữ).
Màn này trả lời 3 câu hỏi:

1. Hàng hoá nào đang bị giữ, giữ bao nhiêu, so với tổng tồn kho là bao nhiêu?
2. Ai đang giữ, giữ cho khách nào, đến khi nào?
3. Lô đó biến động thế nào từ đầu (nhập/giữ/gia hạn/điều chuyển/hủy/xuất) — chứng từ nào gây ra?

---

## Quyết định của user (2026-08-18)

| Điểm | Chốt |
|---|---|
| Bố cục bảng | **Giữ nguyên 3 tầng lồng như ERP** |
| Quyền vào màn | Dùng lại quyền **`Quản lý giữ hàng`** (id 100427) |
| Phạm vi dữ liệu | Theo **3 quyền `Xem phiếu hàng giữ theo tổng công ty / công ty / phòng ban`** (100839/840/841) |
| In & Xuất | **Xuất Excel phẳng** theo cột hiển thị (popup chọn trường); **Bản in giữ nhóm Phòng ban → NV** như ERP |

---

## Bảng dữ liệu (dùng chung ERP — KHÔNG tạo bảng mới, KHÔNG migration)

| Bảng | Số dòng (2026-08-18) | Vai trò |
|---|---:|---|
| `prepick_details` | 53.832 (2.412 lô còn `qty > 0`) | tồn giữ — **chỉ đọc** |
| `prepick_logs` | 110.753 | nhật ký biến động — **chỉ đọc** |
| `accounting_stocks` + `accounting_warehouses` | — | lấy "Tổng SL trong kho" |
| `products` / `brands` / `product_models` / `customers` / `employees` / `employee_infos` / `departments` | — | join hiển thị + lọc |

Quy mô dữ liệu sống: **895 hàng hoá · 74 nhân viên · 192 khách hàng**, phân theo công ty
`company_id` 1 = 1.445 lô · 4 = 937 · 3 = 30.

⚠ `prepick_details` **KHÔNG có `unit_id`** → `qty` luôn là **đơn vị cơ bản**. Ô "Đơn vị" trên màn
là bộ chuyển đổi hiển thị: đổi đơn vị thì mọi số lượng của dòng đó chia cho `unit_coefficient`
(làm tròn xuống 2 chữ số, đúng `roundDown` của ERP).

⚠ Bảng **không có `department_id`** → phạm vi "phòng ban" phải quy về `employee_id IN (thành viên
các phòng đang quản lý)`, không lọc thẳng được như 2 màn phiếu hủy.

---

## Hiện trạng ERP

`WarehouseInfosController` (5 method) + `PrepickDetail::searchByFilter()` + `PrepickIndexReportService`
+ blade `warehouse/warehouses/prepickIndex.blade.php` (533 dòng) + 3 class JS
(`ProductInPrepick`, `ProductInPrepickDetail`, `ProductInPrepickDetailItem`).

| Route ERP | Việc |
|---|---|
| `warehouseInfo.prepickIndex` | render màn |
| `warehouseInfo.prepickSearchData` | tầng 1 — danh sách hàng hoá, phân trang 20 |
| `warehouseInfo.getPrepickDetails` | tầng 2+3 — mọi lô của 1 hàng hoá (không phân trang) |
| `warehouseInfo.getHistoryPrepickDetails` | popup Lịch sử giữ hàng của 1 cặp NV×KH×HH×CT |
| `warehouseInfo.prepickIndex.exportPrepickIndex` | Xuất Excel (gom PB→NV→HH) |
| `warehouseInfo.prepickIndex.printPrepickIndex` | In (mẫu `BAO_CAO_HANG_XUAT_GIU`, gom PB→NV→HH) |

**Không có `checkPermission` trên nhóm route `warehouse_infos`** — ERP mở màn này cho mọi tài
khoản đăng nhập. Menu ERP cũng không `@can`. HRM sẽ gate lại theo quyết định ở trên.

### Trạng thái hạn giữ (tính runtime, không lưu DB)

| Giá trị | Nhãn | Điều kiện | Màu HRM |
|---:|---|---|---|
| `1` | Trong hạn | `expire_date > CURDATE()` | xanh lá (`status-approved`) |
| `3` | Đến hạn | `expire_date = CURDATE()` | cam/vàng (`status-pending`) |
| `2` | Hết hạn | `expire_date < CURDATE()` | đỏ (`status-rejected`) |

### Bộ lọc ERP

Công ty (chỉ hiện với vai trò *Tổng giám đốc*) · Phòng ban · Nhân viên · **Kho** · Thương hiệu ·
Model · Tên hàng · Mã hàng · Trạng thái · Khách hàng. Ngoài ra nhận `product_id` từ query string
(dùng khi màn khác nhảy sang).

---

## 10 lỗi / điểm bất nhất của ERP và cách xử lý

| # | Lỗi ERP | Xử lý bản HRM |
|---:|---|---|
| 1 | `searchByFilter` `GROUP BY pds.product_id` nhưng vẫn `SELECT pds.employee_id, pds.expire_date` → 2 giá trị này là của **một lô bất kỳ** trong nhóm; bật `ONLY_FULL_GROUP_BY` là văng lỗi | Tầng 1 chỉ select cột cấp hàng hoá + `SUM(qty)`. **Bỏ hẳn** `employee_id` / `expire_date` khỏi tầng 1 vì ở mức gộp chúng vô nghĩa |
| 2 | Ô lọc **Kho** có trên giao diện nhưng: biến `$warehouses` không được `compact()` truyền sang view → dropdown **luôn rỗng**; và `searchByFilter` **không đọc** `$request->warehouse` | **Bỏ hẳn ô lọc Kho.** `prepick_details` không gắn kho — hàng giữ là tồn theo nhân viên, không theo kho |
| 3 | Lọc **Khách hàng** áp ở tầng 1 nhưng `getPrepickDetails` **không** lọc `customer_id` → xổ chi tiết ra vẫn thấy đủ mọi khách | Truyền `customer_id` xuống tầng 2. Tầng 1 và tầng 2 dùng **cùng một bộ điều kiện** |
| 4 | Export/print `getData()` khoá cứng `where('company_id', Auth::user()->info->company_id)` **kể cả Tổng giám đốc**, lại lọc `company` bằng `Company::getMembers()` (theo nhân viên) trong khi màn lọc bằng `pds.company_id` → **chọn công ty khác ra rỗng**, và số liệu bản in ≠ số liệu trên màn | In/Xuất dùng **chung đúng một hàm dựng điều kiện** với màn danh sách |
| 5 | `getData()` tính trạng thái bằng `expire_date > NOW()` (so `date` với `datetime`) → lô **hết hạn hôm nay** ra "Hết hạn" trên bản in nhưng "Đến hạn" trên màn | Cả 2 nơi dùng `CURDATE()` |
| 6 | `getHistoryPrepickDetails` không map link cho `AccountingPrepickCancelDetailCustomer` (**1.645 dòng log**) và `ProductExportDetail` (2 dòng) → cột **Chứng từ để trống** | Bổ sung 2 nhánh; loại nào vẫn không dựng được link thì hiện `—` chứ không để trắng |
| 7 | `$scope.onClear()` xoá điều kiện nhưng **không gọi lại** `filter()` → nút Làm mới không nạp lại danh sách | Nút **Làm mới** xoá điều kiện **và** tải lại (bẫy đã biết, đã sửa ở 24 màn khác) |
| 8 | Phạm vi dữ liệu dựa vào `isRole('Tổng giám đốc')` — trên DB gộp role/quyền ERP có `guard_name = web` nên API Eloquent của spatie trả sai | Dùng trait `ChecksEmployeePermission` (query thẳng pivot), theo 3 quyền cấp |
| 9 | `getPrepickDetails` gọi thẳng `PrepickDetail::where('product_id', ...)` **không giới hạn**; hàng hoá nhiều lô thì tải hết một lần | Giữ nguyên (thực tế tối đa vài chục lô/hàng hoá), nhưng thêm `qty > 0` + sắp xếp ổn định |
| 10 | Popup lịch sử `orderBy('created_at')` = **cũ → mới** | **Giữ nguyên cũ → mới.** Đây là sổ biến động tồn, cột `SL giữ` là số cộng dồn sau mỗi lần — đảo ngược sẽ đọc sai. ⚠ Đây là **ngoại lệ có chủ đích** so với rule "lịch sử sắp mới → cũ" |

---

## Thiết kế bản HRM

### Route & menu

| | |
|---|---|
| FE route | `/finance/prepick-stocks` |
| File | `hrm-client/pages/finance/prepick-stocks/index.vue` (+ `print.vue`) |
| Menu | `components/subsystem-menu/finance.js:150` — gắn `link` vào mục **Danh sách hàng giữ** |
| API prefix | `/v1/finance/prepick-stocks` |
| `localStorageKey` | `finance-prepick-stocks-filter` |
| `columnScreenKey` | `finance_prepick_stocks` |

### Phân quyền

- **Vào màn**: quyền `Quản lý giữ hàng`. Không có quyền → không hiện mục menu, gọi API trả **403**.
- **Phạm vi dữ liệu** (fail-closed, xét theo thứ tự):

| Điều kiện | Thấy gì |
|---|---|
| Super admin (role id 18) **hoặc** `Xem phiếu hàng giữ theo tổng công ty` | mọi công ty |
| `Xem phiếu hàng giữ theo công ty` | `prepick_details.company_id = công ty của mình` |
| `Xem phiếu hàng giữ theo phòng ban` | `employee_id IN (thành viên các phòng mình quản lý)` **hoặc** `employee_id = mình` |
| Không quyền nào ở trên | chỉ `employee_id = mình` |

- Ô lọc **Công ty** chỉ hiện với người thuộc nhánh "tổng công ty"; các nhánh khác ẩn ô này
  (ERP cũng chỉ hiện cho Tổng giám đốc).
- **Không** hard-code `true` ở bất kỳ cờ quyền nào.

### Cấu trúc BE

| File | Việc |
|---|---|
| `Modules/Finance/Services/PrepickStockReportService.php` | **mới** — toàn bộ truy vấn của màn. **CHỈ ĐỌC.** |
| `Modules/Finance/Http/Controllers/V1/PrepickStockController.php` | **mới** — 5 endpoint, gate quyền |
| `Modules/Finance/Transformers/PrepickStock/*` | **mới** — 3 resource |
| `Modules/Finance/Routes/api.php` | thêm nhóm route (route tĩnh khai trước) |

⚠ **KHÔNG sửa** `PrepickStockService.php` đang chạy cho 2 màn hủy hàng giữ. Service đó vẫn là nơi
duy nhất **GHI** `prepick_details` / `prepick_logs`; service mới chỉ **đọc**, tách file để không
đụng vào code dùng chung.

| Endpoint | Trả về |
|---|---|
| `GET /v1/finance/prepick-stocks` | tầng 1 — hàng hoá, phân trang; kèm `units[]`, `prepick_qty`, `total_stock_qty` |
| `GET /v1/finance/prepick-stocks/details` | tầng 2+3 — mọi lô `qty > 0` của 1 hàng hoá, đã gom theo nhân viên |
| `GET /v1/finance/prepick-stocks/logs` | sổ biến động của 1 cặp `product × customer × company × employee`, cũ → mới |
| `GET /v1/finance/prepick-stocks/export` | **phẳng** 1 dòng = 1 lô, đủ mọi trường của popup chọn trường |
| `GET /v1/finance/prepick-stocks/print` | gom **Phòng ban → Nhân viên → Hàng hoá** cho bản in |

Tầng 2+3 lấy **một lần** cho cả hai tầng (ERP cũng vậy): API trả danh sách lô, BE gom sẵn theo
`employee_id` để FE khỏi tự gom.

`logs` trả cho mỗi dòng: `change`, `created_at`, `qty_after`, `expire_date`, và chứng từ dạng
`{ code, url }`:

- Loại **đã port sang HRM** (`PrepickCancel`) → link nội bộ `/finance/prepick-cancels/{id}`.
- Loại **chưa port** → link sang cổng ERP bằng `config('app.erp_url')`.
- Không dựng được → `null`, FE hiện `—`.

### Cấu trúc FE

Bố cục 3 tầng, mượn đúng pattern cây cha–con đã có ở
`pages/assign/prospective-projects/index.vue` (nút mở/thu ở cột STT, lazy load con, dàn phẳng
trong computed, cache theo id).

**Tầng 1 — bảng chính** (`V2DataTable`, phân trang 10/5/10/20/50/100):

| Cột | Căn | Ghi chú |
|---|---|---|
| STT | giữa | kiêm nút ▸/▾ mở chi tiết, không tắt được |
| Mã hàng hoá | trái | `<nuxt-link>` sang chi tiết hàng hoá |
| Tên hàng hoá | trái | |
| Đơn vị | trái | `V2BaseSelect` — đổi đơn vị thì quy đổi mọi số lượng của dòng và các tầng con |
| Model | trái | |
| Thương hiệu | trái | |
| Tổng SL trong kho | phải | |
| SL giữ | phải | |

Sắp xếp mặc định **Tên hàng hoá ↑** (giữ đúng ERP — đây là báo cáo tra cứu, không có ngày tạo).
Bật sort cho Mã / Tên / Tổng SL trong kho / SL giữ.

**Tầng 2 + 3 — khối chi tiết** chèn ngay dưới dòng hàng hoá đang mở:

| Tầng 2 (nhân viên) | Tầng 3 (khách hàng) |
|---|---|
| Nhân viên · Phòng ban · Đang giữ | Khách hàng (`mã – tên`) · SL giữ · Hạn giữ · Trạng thái · Hành động |

Hành động duy nhất: **Lịch sử giữ hàng** (icon `ri-history-line`) → mở
`PrepickStockLogModal.vue`.

**Bộ lọc** — `V2BaseSmartFilterPanel` + schema `filterFields` (9 trường → có popup *Cài đặt bộ lọc*):

Công ty (ẩn nếu không thuộc nhánh tổng công ty) · Phòng ban · Nhân viên · Khách hàng ·
Thương hiệu · Model · Tên hàng · Mã hàng · Trạng thái.

Khối tổ chức khai đủ `company_id` / `department_id` / `part_id` / `employee_id` trong
`initialStateForm` (bẫy Vue 2 không reactive). BE đọc **đúng các tên đó** — khác ERP
(`company`/`department`/`employee`), đây là chuẩn HRM.

**Toolbar**: Xuất Excel → In → Cấu hình cột. Không có Thêm mới / Import (màn chỉ đọc).

### Component mới

| File | Việc |
|---|---|
| `components/finance/prepick/PrepickStockLogModal.vue` | popup **Lịch sử giữ hàng**: khối thông tin (Mã hàng · Tên hàng · Kinh doanh · Khách hàng · Trạng thái + hạn giữ hiện tại) + bảng sổ biến động (STT · SL biến động · Ngày · SL giữ · Hạn giữ · Chứng từ), dòng tổng "Số lượng giữ hiện tại" |

⚠ **Không** dùng lại `PrepickHistoryPanel.vue` — component đó là lịch sử **thay đổi bản ghi**
(Loại hành động / Người thực hiện / diff cũ→mới). Cái cần ở đây là **sổ biến động số lượng**,
khác hoàn toàn về cột lẫn nguồn dữ liệu.

### Xuất Excel

Bấm **Xuất Excel** → mở `ExportFieldsModal` chọn trường → dựng file bằng ExcelJS ở FE, **phẳng
1 dòng = 1 lô**:

STT · Mã hàng hoá · Tên hàng hoá · ĐVT · Model · Thương hiệu · Nhân viên · Phòng ban ·
Khách hàng · SL giữ · Tổng SL trong kho · Hạn giữ · Trạng thái.

BE trả **đủ** các trường trên kể cả cột đang ẩn ở màn. Tự gắn `Authorization` cho request tải
(bẫy `$axios` thiếu token). Nút khoá khi đang xuất + có dòng tiến độ.

### Bản in

`pages/finance/prepick-stocks/print.vue`, khổ **ngang**, giữ bố cục phân nhóm của ERP:

```
1     <Phòng ban> – N nhân viên – M mục hàng
1.1     <Nhân viên> – K mục hàng
1.1.1     Tên hàng | Mã hàng | ĐVT | SL giữ | Hạn giữ | Khách hàng | Trạng thái
```

Áp `print-page` skill (letterhead, viền, không mất chữ đậm). ERP dồn sang gửi mail khi > 400
dòng — HRM không port cơ chế gửi mail; thay vào đó chặn in khi vượt ngưỡng và báo user thu hẹp
bộ lọc.

---

## Không làm trong đợt này

- 3 màn anh em dùng chung `PrepickDetail` — **Hàng sắp hết hạn giữ** (`expiringPrepick`),
  **Hàng giữ của tôi** (`prepickEmployee`), **Hàng sắp hết hạn giữ (kế toán)**
  (`accountingExpiringPrepick`). Chúng chỉ là màn này + điều kiện `expire_date` theo
  `config.warning_day`; `PrepickStockReportService` được viết sẵn để nhận `type` nên port sau rất
  nhẹ.
- Cơ chế gửi báo cáo qua mail khi dữ liệu lớn (`PrepickIndexMailJob`).
- Danh sách hàng **mượn** (`borrowIndex`) — khác bảng, khác nghiệp vụ.

---

## Rủi ro

| Rủi ro | Giảm thiểu |
|---|---|
| Sửa lỗi #1 (bỏ `employee_id`/`expire_date` khỏi tầng 1) làm số liệu **khác ERP** | Đó là giá trị rác của ERP; tầng 2 mới là nơi hiển thị đúng. Ghi rõ vào bảng "khác biệt có chủ đích" trong `plan.md` |
| Sửa lỗi #4 làm bản in ra **nhiều dòng hơn** ERP với tài khoản Tổng giám đốc | Đúng ý nghĩa nghiệp vụ. Đối chiếu 2 cổng với tài khoản thường (không đổi) trước, rồi mới báo lệch với tài khoản TGĐ |
| 3 tầng lồng chưa có tiền lệ 3 cấp trong HRM (cây cha–con hiện chỉ 2 cấp) | Tầng 2+3 lấy **một lần** trong cùng response nên không phải lazy load lồng nhau; chỉ có 1 nút mở/thu |
| Đổi đơn vị ở tầng 1 phải quy đổi cả tầng 2, 3 | Hệ số quy đổi lưu trên dòng tầng 1, tầng con đọc lên qua `_parent` (đúng cách 3 class JS của ERP làm) |
| Màn dùng `employee_id IN (...)` cho cấp phòng ban trên 74 nhân viên | Danh sách nhỏ, không cần bảng tạm |
