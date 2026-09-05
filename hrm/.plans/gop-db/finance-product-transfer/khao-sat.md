# Khảo sát: chuyển màn **Phiếu điều chuyển hàng** từ ERP sang HRM

**Người phụ trách:** @junfoke — 2026-09-04
**Nhánh làm việc:** `feat/finance-product-transfer` (hrm-api + hrm-client, tách từ `gop_db`), ERP `master`
**Trạng thái:** MỚI KHẢO SÁT — chưa code, chưa chốt scope với user.

> Nhánh được tạo 2026-09-04 sau khi user nhắc: mỗi màn port một nhánh riêng, không làm ké nhánh
> của màn khác (`feat/finance-prepick-export-request`). Thay đổi menu ở mục 1 đã được mang sang đây.

---

## 1. Xác định đúng màn

ERP menu: **Kho → Điều chuyển → Phiếu điều chuyển hàng** → `route('productTransfer.index')?type=all`.

| Thành phần | Đường dẫn ERP |
|---|---|
| Controller | `app/Http/Controllers/Warehouse/ProductTransfersController.php` (578 dòng) |
| Model | `app/Model/Warehouse/ProductTransfer.php`, `ProductTransferDetail.php` |
| View | `resources/views/warehouse/product_transfers/` (index/create/edit/show/form/formJs — 603 dòng) |
| Class JS | `resources/views/partials/classes/warehouse/ProductTransfer(.Detail).blade.php` |
| Bảng | `product_transfers` (309 dòng trên `gop_db`), `product_transfer_details` (407 dòng) |
| Mã phiếu | `PDCH-xxxxx` |
| Mẫu in | `report_templates` id **388** (Phiếu điều chuyển hàng), **387** (Danh sách phiếu điều chuyển hàng) — đều ĐÃ có trên `gop_db` |
| Quyền | `100682` "Xem phiếu điều chuyển hàng theo - tổng công ty", `100683` "… - công ty", `100080` "Kế toán kho" (guard **web**) |

### ⚠️ Trùng tên với màn đã port — phải chốt trước khi làm

`hrm-client/components/subsystem-menu/finance.js:206` hiện có mục nhãn **"Phiếu điều chuyển hàng"**
nhưng trỏ vào `/finance/product-transfer-requests` — đó là màn ERP **"Phiếu yêu cầu chuyển hàng"**
(`product_transfer_requests`), đã port xong. Comment trong file ghi user chốt đổi nhãn ngày 2026-08-07.

→ Màn đang khảo sát (`product_transfers`) là màn **KHÁC**, chưa port. Nếu port sẽ có 2 mục cùng tên
trong nhóm "Điều chuyển". **Cần user chốt lại nhãn** (gợi ý: giữ "Phiếu yêu cầu chuyển hàng" cho màn cũ,
dùng "Phiếu điều chuyển hàng" cho màn mới — đúng nhãn ERP).

Cũng lưu ý: `AccountingStockService` (docblock đầu file) đang chú thích nhầm là phục vụ
"màn Phiếu điều chuyển hàng" — thực ra là màn yêu cầu chuyển hàng. Sửa comment khi port.

---

## 2. Nghiệp vụ

Phiếu **chuyển hàng giữa 2 kho KẾ TOÁN trong cùng 1 kho VẬT LÝ** (hàng không đi đâu, chỉ đổi kho hạch toán).

**Luồng:** không có duyệt nhiều cấp, chỉ 2 trạng thái:

| Status | Tên | Ý nghĩa |
|---|---|---|
| 1 | Đang tạo (đỏ) | nút **Lưu** — mới ghi phiếu, chưa đụng tồn |
| 2 | Đã hạch toán (xanh) | nút **Duyệt** — trừ/cộng tồn kế toán + ghi sổ ngay |

- Chuyển sang **Đã hạch toán** thì `updateWarehouse()` + `saveAccounting()` chạy, ghi `date_accounting = now()`.
- `canEdit()` = `status == Đang tạo && created_by == mình` → Đã hạch toán là **khoá cứng**, không Sửa/Xóa.
- **KHÔNG có chức năng huỷ/đảo bút toán.** Thực tế trên `gop_db`: 309/309 phiếu đều status = 2.

**Phạm vi xem** (`searchByFilter`, chỉ áp dụng khi `?type=all`):
quyền tổng công ty → tất cả; quyền công ty → cùng `company_id`; không quyền → chỉ phiếu mình lập.
Ngoài ra phiếu **Đang tạo** chỉ người lập thấy.

**Bút toán** (`saveAccounting`): mỗi dòng ghi Nợ 156 / Có 156 với `amount_export_price`.
Hai vế cùng TK 156 — đúng bản chất chuyển kho nội bộ, giữ nguyên khi port.

**Giá vốn** (`updateWarehouse`): `export_price` = chênh lệch `value_before - value_after` của
`AccountingStockLog` bên kho xuất, chia cho số lượng quy đổi (FIFO). Kho nhập cộng vào không tính lại giá.

---

## 3. Giao diện ERP

### Danh sách (9 cột + Hành động)
STT · Số phiếu (link show) · Ngày hạch toán · Kho vật lý · Kho xuất · Kho nhập · Người lập · Ngày lập · Trạng thái.
Hành động: Sửa/Xóa (chỉ khi `canEdit`) · In · Xuất excel. Có nút **Tạo mới**, **In danh sách**, **Xuất Excel danh sách**.

### Bộ lọc khai báo trong `search_columns`
Mã phiếu · Kho · Trạng thái · Người tạo · Người duyệt · Mã hàng hóa · Tên hàng hóa · (khoảng ngày).

### Form Thêm/Sửa/Xem
- Thông tin chung: **Kho vật lý** (bắt buộc) · **Kho xuất** (kho kế toán, bắt buộc) · **Kho nhập** (bắt buộc) · Ghi chú · File đính kèm (PDF, nhiều file, S3).
- Chi tiết: STT · Tên hàng hóa · Model · Mã hàng · **SL tồn** (chỉ khi tạo/sửa) · **SL chuyển** · ĐVT ·
  **Đơn giá vốn / Thành tiền vốn** (chỉ màn Xem) · TK nợ `156` · TK có `156` (hard-code) · nút xoá dòng.
- Thêm hàng bằng popup `partials.modals.searchProduct` (popup dùng chung ~40 màn, HRM đã có bản port).
- Đổi Kho vật lý → xoá sạch kho xuất/nhập + danh sách hàng; dropdown kho kế toán lọc theo `warehouse_id`.

---

## 4. Lỗi / điểm bất thường của ERP phát hiện khi đọc code

Phải chốt với user từng điểm: **giữ nguyên như ERP** hay **sửa theo chuẩn HRM**.

1. **Bộ lọc chết**: `searchByFilter` chỉ xử lý `code`, `status`, `created_by`, `company`, `department`.
   Các bộ lọc **Kho**, **Người duyệt**, **Mã hàng hóa**, **Tên hàng hóa**, **khoảng ngày** khai báo trên
   giao diện nhưng backend **không dùng** → lọc xong không đổi kết quả. (Màn này còn không có khái niệm
   "người duyệt", nên bộ lọc đó vô nghĩa hoàn toàn.)
2. **Rò dữ liệu khi vào không kèm `?type=all`**: nhánh phân quyền trong `searchByFilter` nằm gọn trong
   `if ($request->type == 'all')`. Route `productTransfer.index` không tham số → `type='index'` →
   **không lọc công ty, không lọc người lập** → thấy phiếu của mọi công ty. Menu luôn gắn `?type=all`
   nên thực tế ít lộ, nhưng gõ URL trần là thấy.
3. **`store`/`update` không kiểm quyền**: chỉ `create()` (màn) chặn bằng `can('Kế toán kho')`;
   API lưu thì không → gọi thẳng POST là tạo được phiếu.
4. **`status` nhận thẳng từ request**, không có rule validate → client gửi giá trị nào cũng ghi.
5. **Setter `qty` tự kẹp về `in_stock`** (`ProductTransferDetail.blade.php`) — trái rule team
   "vượt khoảng thì báo đỏ, không tự sửa giá trị người nhập".
6. **`products.*.qty` => `min:1`** — chặn cả số lẻ < 1 dù cột là `decimal(12,2)`.
7. **Dropdown kho kế toán lúc mở màn Sửa/Xem** nạp `AccountingWarehouse::getForSelect()` = **toàn bộ kho
   của mọi công ty, cả kho đã khoá**; chỉ sau khi đổi kho vật lý mới lọc lại theo công ty + status.
8. **`getDataProduct` đọc `$product->data`** — accessor này đã biết là **hỏng trên `gop_db`**
   (xem memory `project_erp_product_data_accessor_hong_tren_gop_db`, bảng `files` đổi schema).
   Port sang HRM phải tự chọn field, không bê accessor.
9. **`getAccountingStockDetail` là bản COPY cục bộ** trong controller, khác `Product::getAccountingStockDetail()`
   mà các màn khác dùng: bản này thêm `in_acc_warehouse` (tồn riêng kho kế toán được chọn) và
   `in_stock = min(khả dụng công ty, in_acc_warehouse, in_warehouse)`.
   → KHÔNG phải sửa `AccountingStockService` vì chuyện này, xem mục 5.
10. **Xoá phiếu không dọn file đính kèm** trên S3, và `delete()` dùng `redirect()->with()` (kiểu web) thay vì JSON.
11. **Link chết**: `warehouse_transfers/show.blade.php` và `WarehouseTransfersController` còn nút
    "Tạo phiếu điều chuyển hàng" truyền `?warehouse_transfer_id=`, nhưng cột đó **đã bị migration
    2023-10-30 xoá** và `create()` không đọc tham số. Màn `warehouseTransfer` cũng không còn trong menu
    → **không port phần này**.
12. **`export_price` chỉ được tính lúc hạch toán**; nếu `$product->qty == 0` thì biến `$export_price`
    dùng lại giá trị của vòng lặp trước (không reset) → gán nhầm giá dòng trước.
13. Mẫu in để cột **TK nợ / TK có** cứng "156", không đọc cấu hình.

---

## 5. Hạ tầng HRM đã có — mức độ tái sử dụng

| Cần gì | HRM đã có | Ghi chú |
|---|---|---|
| Tính tồn kho kế toán | `Modules/Finance/Services/AccountingStockService::detail()` | **Dùng lại NGUYÊN TRẠNG, KHÔNG sửa** — xem ghi chú (a) ngay dưới bảng |
| Trừ/cộng tồn + ghi `accounting_stock_logs` + giá vốn FIFO | `Modules/Assign/Services/WarehouseExportAccountingService` (đã port `calculateValue`/`getValueDetails`, có sẵn hằng `TRANSFER_FQN = App\Model\Warehouse\ProductTransferDetail`) | Cần 2 method private `fifoValue()` + `layerQtyPrice()` — xem ghi chú (b) |
| Ghi sổ `account_details` | `Modules/Finance/Entities/Account/AccountDetail::createDataSaveDept/saveAccountDetail` | Dùng thẳng, đúng chữ ký ERP |
| Entity `AccountingStock`, `AccountingStockLog` | `Modules/Assign/Entities/Warehouse/` | Có sẵn |
| Popup tìm hàng hóa | `GET /v1/customer-care/services/search-products` (màn YC chuyển hàng đang dùng) | Dùng lại, không tạo mới |
| Khuôn màn gần nhất | `Modules/Finance/.../ProductTransferRequestController` + `Services/ProductTransferRequestService` (1.014 dòng) và FE `pages/finance/product-transfer-requests/` | **Khuôn chuẩn để bám theo**: đính kèm PDF multipart, print-data từ mẫu ERP, export Excel, gate bằng `canView/canEdit` trên Entity thay vì middleware |
| Mẫu in ERP | `Modules/Finance/Entities/ErpReportTemplate` | Đọc template 388 / 387 |
| Dropdown kho vật lý / kho kế toán | **CHƯA có** endpoint đúng nhu cầu | `stockOptions()` hiện tại là dropdown **nhóm kho** cho màn YC chuyển hàng, không dùng lại được |

### (a) `AccountingStockService` — dùng lại nguyên trạng, KHÔNG mở rộng

Bản khảo sát đầu (2026-09-04 sáng) ghi phải bổ sung `in_acc_warehouse` vào service dùng chung.
**Sai — đã sửa lại sau khi user chất vấn.** Đọc kỹ ERP (`ProductTransfersController` :395-402 và vòng
lặp pending :430-440): `in_acc_warehouse` chỉ là `SUM(qty)` **thô** của đúng kho kế toán đang chọn,
**không** bị trừ pending (vòng lặp pending chỉ trừ `in_warehouse` và `in_promotion`).

⇒ Nó không dính gì tới phần logic phức tạp mà service đang giữ (pending / prepick / hold / khả dụng
toàn công ty). Service riêng của màn tự lo:

1. gọi `AccountingStockService::detail($productId, $accWhIdsCủaKhoVậtLý, $companyId, $employeeId)`
   để lấy `in_warehouse` + khả dụng toàn công ty (chính là `in_stock` service trả về);
2. tự query 1 dòng `SUM(accounting_stocks.qty)` theo `acc_warehouse_export_id` → `in_acc_warehouse`;
3. tự ghép `in_stock = min(khả dụng, in_acc_warehouse, in_warehouse)` — công thức RIÊNG của màn này
   (nhánh kho khuyến mại: `min(in_acc_warehouse, in_promotion)`).

4 màn đang gọi service (`prepick-cancel-request`, `prepick-extend-request`, `prepick-transfer-request`,
`warehouse-prepick-request`) **không bị ảnh hưởng**.

### (b) FIFO giá vốn — tách 2 method private, KHÔNG phải "đụng hàm dùng chung"

Bản đầu xếp `WarehouseExportAccountingService` vào diện hàm dùng chung phải xin phép. **Nói quá** —
service này chỉ có **đúng 1 nơi gọi**: `ProductExportService.php:245`.

Màn ĐCH cần đúng 2 method private `fifoValue()` + `layerQtyPrice()` (:150-211) — dựng lại giá vốn
theo layer nhập. `layerQtyPrice()` **đã có sẵn nhánh `TRANSFER_FQN` đọc `product_transfer_details`**,
tức bản port trước đã tính đến chuyện phiếu ĐCH là một layer nhập trong chuỗi FIFO; ERP cũng chỉ có
một bản logic này.

⇒ Đề xuất **tách 2 method đó ra service dùng chung** (refactor nhỏ, 1 caller, không đổi hành vi),
thay vì chép bản thứ hai cho màn ĐCH — chép đúng vào cái bẫy mà docblock `AccountingStockService`
đã cảnh báo: "2 bản chắc chắn lệch nhau theo thời gian".

`calculateExportPrice()` thì **KHÔNG dùng lại được**: nó bám bảng `product_export_detail_accounting`
(phân bổ kho của phiếu xuất hàng), màn ĐCH không có bảng đó → tự tính từ log của chính nó như ERP.

### Bẫy phân quyền đã biết (áp dụng nguyên si)
Quyền ERP nằm ở guard **`web`** (`100682/100683/100080`), HRM guard `api`. Middleware `checkPermission`
của HRM resolve qua spatie `getAllPermissions()` nên **bỏ sót quyền gán từ ERP** (`model_type='App\Employee'`).
→ Màn YC chuyển hàng đã cố tình **không gắn `checkPermission`**, chặn bằng `canView()/canEdit()` tự query pivot.
Màn này làm y hệt. (memory `project_erp_permission_guard_web_vs_api`)

---

## 6. Khối lượng ước tính

**Backend** (`Modules/Finance`): 2 Entity (`ProductTransfer`, `ProductTransferDetail`) + Service
(~600–700 dòng: searchByFilter, store/update/destroy, hạch toán, printData, exportData, stockOfProducts,
productUnits, deleteFile) + Controller + FormRequest + 2 Resource + ~13 route.
**Frontend** (`hrm-client/pages/finance/product-transfers/`): `index.vue`, `create.vue`, `_id/index.vue`,
`_id/edit.vue`, `_id/print.vue`, `components/ProductTransferForm.vue` + 1 mục menu.
Không cần migration (bảng đã có sẵn trên `gop_db`, khớp cột).

Ước lượng: **~5–7 ngày công**, tương đương màn `finance-product-transfer-request` đã làm — nhưng
**rủi ro cao hơn** vì màn này GHI TỒN KHO + GHI SỔ KẾ TOÁN thật (màn kia chỉ là yêu cầu, không đụng tồn).

---

## 7. Việc cần user chốt trước khi lập plan

1. **Nhãn menu**: xử lý trùng tên với `/finance/product-transfer-requests` như thế nào?
2. **Nhóm lỗi ERP ở mục 4**: giữ nguyên hành vi ERP hay sửa theo chuẩn HRM? Đặc biệt:
   - bộ lọc chết (Kho / Người duyệt / Mã–Tên hàng hóa / khoảng ngày) — bỏ hẳn khỏi giao diện hay làm cho chạy?
   - setter `qty` tự kẹp — chuyển sang báo đỏ theo rule team?
   - `min:1` cho số lượng — cho phép số lẻ?
3. **Tách 2 method FIFO** (`fifoValue` / `layerQtyPrice`) khỏi `WarehouseExportAccountingService`
   thành service dùng chung, thay vì chép bản thứ hai — xem ghi chú (b) mục 5. Refactor nhỏ, đúng 1
   caller hiện tại, không đổi hành vi. (`AccountingStockService` **không** phải đụng tới.)
4. Có cần **lịch sử thao tác** (bảng history) như các màn Giữ hàng không? ERP màn này **không có**.
5. Có cần bổ sung chức năng **huỷ phiếu / đảo bút toán** không? ERP **không có** — hạch toán rồi là khoá vĩnh viễn.

---

## 8. Kết luận

Màn này **port được**, hạ tầng kế toán kho phía HRM đã đủ (tồn kho, log FIFO, ghi sổ đều có sẵn từ các
màn trước). Rào cản không nằm ở kỹ thuật mà ở **quyết định nghiệp vụ**: trùng tên menu, và một loạt
lỗi/thiếu sót của ERP mà nếu bê nguyên sẽ mang lỗi sang HRM, còn nếu sửa thì lệch hành vi ERP.
Đề nghị chốt mục 7 rồi mới viết `design.md` + `plan.md`.
