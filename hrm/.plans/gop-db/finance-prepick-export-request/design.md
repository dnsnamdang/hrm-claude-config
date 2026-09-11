# Thiết kế — Port cặp màn "Yêu cầu xuất giữ" + "Phiếu xuất giữ" ERP → HRM

Nguồn ERP:
- `warehouse/product_prepick_requests` — Controller 759 dòng, Model 925 dòng, 8 blade.
- `warehouse/warehouse_prepick_requests` — Controller 493 dòng, Model 445 dòng, 8 blade.

Đích HRM: phân hệ **Tài chính** → nhóm **Giữ hàng** (2 mục placeholder đã khai sẵn ở
`components/subsystem-menu/finance.js:179-180`).
- `/finance/product-prepick-requests` — Yêu cầu xuất giữ (PYCXG)
- `/finance/warehouse-prepick-requests` — Phiếu xuất giữ (PXG)

Bảng trên `gop_db` (**giữ nguyên schema ERP**, chỉ thêm bảng lịch sử của HRM):
`product_prepick_requests` (2.174 phiếu) + `product_prepick_request_details` (26.185) ·
`warehouse_prepick_requests` (2.062) + `warehouse_prepick_request_details` (10.692).

---

## 0. Vì sao phải port CẢ HAI cùng đợt

PYCXG là **yêu cầu**, PXG là **phiếu thực hiện**. Chỉ PXG mới ghi tồn:

```
PXG lưu với status = 1 ("Duyệt giữ hàng")
   → updateWarehouse()  : ghi prepick_details + prepick_logs   ← SINH RA LÔ HÀNG GIỮ
   → $parent->approve() : PYCXG chuyển sang 1 (Đã duyệt)
```

Đây chính là nguồn của `prepick_details.objectable_type = App\Model\Warehouse\WarehousePrepickRequest`
mà 4 màn HRM đã port đang tiêu thụ (Danh sách hàng giữ, Gia hạn, Hủy, Điều chuyển) — xem
`PrepickLotContractService::SOURCE_WAREHOUSE_PREPICK`. Port riêng PYCXG thì duyệt xong **không có
màn nào lập được lô hàng giữ**, cả nhóm đứng.

⇒ **Dùng lại `PrepickStockService`** cho bước ghi tồn (skill `erp-to-hrm-screen` Bước 3b) —
hiện service này mới có `moveToExpireDate()` / `moveToOwner()`, cần thêm **`addLot()`** (cộng lô mới).

---

## 1. Nghiệp vụ (Bước 1 của skill)

### 1.1 Trạng thái PYCXG (giữ nguyên số của ERP)

| Số | Tên ERP | Màu HRM (SRS) | Ghi chú |
|---|---|---|---|
| 3 | Đang tạo | **XÁM** | ERP gán `danger` (đỏ) — **bê nguyên là sai** |
| 6 | Chờ TP duyệt | cam | |
| 4 | Chờ BGĐ duyệt | cam | ERP gán `danger` |
| 2 | Chờ KT duyệt | cam | ERP gán `danger` |
| 5 | Đang xuất giữ | cam | KT đã lưu **nháp** PXG; ERP gán `danger` |
| 1 | Đã duyệt | xanh | |

Không duyệt ở bất kỳ cấp nào → quay về **3 (Đang tạo)** kèm `comment`. ERP **không có trạng thái
"Từ chối" riêng** — người lập sửa lại rồi gửi tiếp.

### 1.2 Trạng thái PXG

| Số | Tên | Màu | Ghi chú |
|---|---|---|---|
| 3 | Đang tạo | XÁM | nháp của kế toán; PYCXG cha bị kéo về 5 |
| 4 | Chờ duyệt | cam | nhánh **BKS duyệt — ERP đã comment toàn bộ**, không dùng |
| 1 | Đã duyệt | xanh | ghi tồn giữ |

### 1.3 Luồng duyệt đầy đủ

```
Người lập (KD)   3 Đang tạo ──gửi──▶ 6 Chờ TP duyệt
TP duyệt         6 ──▶ checkSwitchApprove() ? 4 Chờ BGĐ duyệt : 2 Chờ KT duyệt
BGĐ duyệt        4 ──(nhập lại "Giữ đến ngày")──▶ 2 Chờ KT duyệt
Kế toán          2 ──"Tạo phiếu xuất giữ"──▶ PXG
                     PXG lưu nháp (3) → PYCXG = 5 Đang xuất giữ
                     PXG duyệt   (1)  → ghi tồn giữ + PYCXG = 1 Đã duyệt
                     PXG bị xóa       → PYCXG quay lại 2
Không duyệt (mọi cấp) ──▶ 3 Đang tạo + ghi chú
```

`checkSwitchApprove()` — quyết định TP duyệt xong đi BGĐ hay thẳng KT:
- Có hợp đồng: `SUM(account_details.money_value_exchange)` với `account_id = 22`, `type = 2`,
  `invoiceable_type ∈ {BillIncome, BillAdjustDept, BillIncomeReport}` chia `total_after_vat`, so
  với `%` cấu hình ở `companies.prepick_contract_types` theo mã loại HĐ
  (`ban_hang` / `du_an` / `nguyen_tac` / `dich_vu`). Dưới ngưỡng → **phải qua BGĐ**.
- Không có hợp đồng (loại 99): tổng `total_amount` các dòng so với `companies.prepick_other_value`.
  Vượt → **phải qua BGĐ**.

*(Công thức giống hệt `PrepickExtendRequestService` / `PrepickTransferRequestService` đã port —
dùng lại, không viết bản thứ ba.)*

### 1.4 Sáu loại yêu cầu — hai kiểu form khác hẳn nhau

| id | Tên | Nguồn hàng | `contractable_type` |
|---|---|---|---|
| 1 | Xuất giữ thường | Hợp đồng bán (`contracts`) | `App\Contract` |
| 2 | Xuất giữ khuyến mại | `contract_promotions` | `App\Contract` |
| 3 | Xuất giữ HĐDV | `WrServiceContract` | `App\Model\Customers\WrServiceContract` |
| 4 | Xuất giữ HĐDA | `ProjectContract` | `App\Model\Sale\ProjectContract` |
| 5 | Xuất giữ HĐ hãng | `FirmContract` | `App\Model\Sale\Firm\Contract\FirmContract` |
| 99 | Xuất giữ khác | **thêm tay** | NULL |

- Loại 1–5: chọn HĐ qua popup → hàng tự nạp; user chỉ **tick "Cần xuất"** + nhập **SL đề nghị**.
  Không thêm/xóa dòng được. Bắt buộc `contractable_id` + `contractable_type`.
- Loại 99: chọn **Khách hàng** qua popup, **thêm/xóa hàng bằng tay** + chọn ĐVT (`updateStock` gọi
  lại khi đổi ĐVT). Bắt buộc **Khách hàng + Ghi chú + File đính kèm** (≥ 1 file).
- Chung: **Giữ đến ngày** bắt buộc, phải là ngày tương lai, và không vượt
  `now + config.max_prepick_date` (loại 4 dùng `max_prepick_date_project_contract`).

⚠️ **Dữ liệu thật trên `gop_db` chỉ có 2 loại**: 5 (501 phiếu) và 99 (1.673 phiếu). Loại 1–4 = 0
phiếu từ 08/2025 đến nay. User đã chốt **vẫn port đủ 6 loại** (mục 4) → phải dựng đủ 5 popup chọn
hợp đồng và xin dump dữ liệu loại 1–4 từ dev để nghiệm thu.

### 1.5 Bảng chi tiết

**PYCXG loại 1–5** (14 cột): STT · ☑ Cần xuất · Tên hàng hóa · Model · Mã hàng hóa · Thương hiệu ·
**SL Có thể giữ** (`in_stock`) · SL Hợp đồng · SL Đã xuất kho · **SL Đề nghị** (nhập) · Đơn giá ·
Thành tiền · ĐVT · Ảnh. *(loại 3 ẩn 2 cột Hợp đồng / Đã xuất kho)* + dòng **Tổng cộng**.

**PYCXG loại 99** (11 cột): STT · Tên hàng · Model · Mã hàng · Thương hiệu · **Có thể giữ** ·
**Đề nghị** · **ĐVT (select)** · Đơn giá · Thành tiền · nút xóa dòng + nút **+** thêm hàng.

**PXG** (10 cột): STT · ☑ Cần xuất · Tên hàng · Model · Mã hàng · Thương hiệu · **SL có thể giữ** ·
**SL đề nghị** (kế toán sửa được) · ĐVT · Ảnh.

Cột "Có thể giữ" = **tồn KHO**, ERP lấy qua `warehouseInfo.stockOfProducts` →
`Product::getAccountingStockDetail()`. Bên HRM đã có `AccountingStockService::detail()`.

### 1.6 Validate số lượng

| Nơi | Quy tắc |
|---|---|
| PYCXG `validateProducts()` | SL đề nghị ≤ (SL hợp đồng − đã xuất) theo từng loại. HĐ **nguyên tắc** (`Contract::HOP_DONG_NGUYEN_TAC`) thì bỏ qua. Loại 99 không kiểm |
| PYCXG store/update | mọi dòng SL = 0 → chặn ("SL đề nghị tất cả = 0. Không hợp lệ!") |
| PXG `validateProducts()` | `in_stock − in_promotion_stock ≥ qty × unit_coefficient` (tồn kho trừ hàng khuyến mại). Chỉ kiểm khi status ≠ 3 (nháp bỏ qua) |

⚠️ `AccountingStockService::detail()` của HRM **chưa trả `in_promotion`** → phải bổ sung (xem mục 4).

### 1.7 Ghi tồn giữ (`updateWarehouse`) — phần quan trọng nhất

Với mỗi dòng `need_export = 1` và `qty > 0`:
1. `qty_base = qty × product_units.unit_coefficient`, ghi ngược vào `detail.prepick_qty`.
2. Tìm dòng `prepick_details` khớp **product_id + employee_id + customer_id + expire_date +
   company_id**; chưa có thì tạo mới với `objectable_id = PXG.id`,
   `objectable_type = WarehousePrepickRequest`, `start_date = now`, `qty = 0`.
3. Ghi `prepick_logs` (`qty_before` / `change` / `qty_after`, `objectable` = chính dòng detail PXG).
4. `prepick_detail.qty += qty_base`.
5. Đóng dấu `approver_id` / `approved_time` lên PXG.

`employee_id` của lô = **người lập PYCXG** (`$this->parent->created_by`), KHÔNG phải kế toán lập PXG.
Tương tự `boot::created` của PXG copy `company_id` / `department_id` / `part_id` từ **người lập
PYCXG** — port sai chỗ này thì phiếu lọt sang công ty khác.

### 1.8 Danh sách — ERP 3 biến thể, HRM gộp còn 1

ERP PYCXG: `index` (của tôi) · `all` (theo quyền) · `forAccounting` (chờ duyệt).
ERP PXG: `index` · `all` · `forWarehouse`.
Theo rule đã chốt cho màn Tài chính (1 màn = bản `all`, nút hiện theo quyền) → **mỗi nghiệp vụ
1 màn danh sách duy nhất**.

**Cột PYCXG** (bản `all`): STT · Mã phiếu · Loại yêu cầu · Người lập · Ngày lập · Hợp đồng ·
Trạng thái · Người duyệt · Ngày duyệt · Hành động.
HRM bổ sung, mặc định **ẩn** ở Cấu hình cột: Khách hàng · Giữ đến ngày · Ghi chú · Lý do không duyệt ·
Người/Ngày sửa · Phòng ban · TP duyệt · BGĐ duyệt.

**Lọc PYCXG**: Mã phiếu (text) · Người lập (select NV) · Hợp đồng (text) · Trạng thái · Loại yêu cầu ·
Người duyệt (select NV) · Tên/mã hàng hóa (text) · khoảng ngày lập · khối Công ty/Phòng ban.

**Cột PXG**: STT · Mã phiếu · **YCXG** (link phiếu cha) · Người yêu cầu · Phòng yêu cầu · Người lập ·
Ngày lập · Trạng thái · Hành động. Bổ sung ẩn: Khách hàng · Giữ đến ngày · Người duyệt · Ngày duyệt ·
Ghi chú.

**Lọc PXG**: Mã phiếu · YCXG · Người yêu cầu · Người lập · Trạng thái · Tên/mã hàng hóa · ngày ·
khối Công ty/Phòng ban.

### 1.9 Phạm vi xem

Cả hai màn phân cấp theo 3 quyền: `Xem phiếu hàng giữ theo tổng công ty` → toàn bộ ·
`... theo công ty` → `company_id` · `... theo phòng ban` → `EmployeeManageDepartment` ·
còn lại → `created_by = mình`. Phiếu **Đang tạo (3)** chỉ người lập thấy.

Bản `forAccounting` của PYCXG cộng thêm: KT thấy status 2 · BGĐ thấy status 4 · TP thấy status 6
**và** thuộc phòng mình quản lý → HRM gộp bằng `orWhereApprovable` như màn Gia hạn / Điều chuyển.

### 1.10 Hành động & điều kiện ẩn/hiện

**PYCXG**

| Nút | Điều kiện |
|---|---|
| Sửa · Xóa | `canEdit()` = status 3 **và** (người lập là mình **hoặc** Super Admin) |
| TP duyệt / Không duyệt | `canManagerApprove()` = quyền `Trưởng phòng duyệt hàng giữ` + cùng công ty + status 6 + `department_id` ∈ phòng mình quản lý |
| BGĐ duyệt / Không duyệt | `canBoardOfManagerApprove()` = quyền `Ban giám đốc duyệt hàng giữ` + cùng công ty + status 4. **Có nhập lại "Giữ đến ngày"** |
| Tạo phiếu xuất giữ | `canApprove()` = quyền `Kế toán duyệt hàng giữ` + cùng công ty + status 2 |
| In yêu cầu | không điều kiện |
| Xem chi tiết | `canView()` = (`Quản lý giữ hàng` \| 3 quyền duyệt) và status ≠ 3, hoặc là người lập |

**PXG**

| Nút | Điều kiện |
|---|---|
| Sửa · Xóa | `canEdit()` = status 3 **và** là người lập |
| In đề nghị | không điều kiện |
| Duyệt / Không duyệt | `canApprove()` — **nhánh BKS, ERP đã tắt** (xem mục 2 lỗi #2) |

Nút trên **màn chi tiết phải khớp hệt** màn danh sách (checklist B của skill).

### 1.11 Quyền

`Quản lý giữ hàng` (427) · `Trưởng phòng duyệt hàng giữ` (836) · `Ban giám đốc duyệt hàng giữ` (837) ·
`Kế toán duyệt hàng giữ` (838) · `Xem phiếu hàng giữ theo tổng công ty / công ty / phòng ban`
(839 / 840 / 841) · `Ban kiểm soát duyệt giữ hàng` (638, nhánh chết) · `Trưởng phòng kế toán`.

⚠️ Màn PXG bản `all` của ERP bọc thêm `Auth::user()->can("Trưởng phòng kế toán")` — **không có quyền
đó thì chỉ thấy phiếu do chính mình lập**, kể cả khi có 839/840/841. Rất dễ port sót.

### 1.12 Chặn quá hạn (`checkDueConfigs`)

Route `create` / `store` / `update` của PYCXG có middleware `checkDueConfigs`; route `approve` có
`checkDueConfigsManager:Duyệt yêu cầu xuất giữ`. Middleware chặn người **đang còn hàng giữ quá hạn**
(`prepick_details.qty > 0 AND expire_date < today`), hàng mượn quá hạn, hàng nhập thẳng quá hạn — theo
`company_due_configs`. **HRM chưa port middleware này** → xem mục 4.

### 1.13 In & Xuất

| | Mẫu in phiếu | In danh sách | Xuất Excel |
|---|---|---|---|
| PYCXG | `ReportTemplate::YEU_CAU_XUAT_GIU` | `DANH_SACH_YEU_CAU_XUAT_GIU` (ngang, 9 cột) | `danh_sach_yeu_cau_xuat_giu.xlsx` |
| PXG | `ReportTemplate::DE_NGHI_XUAT_GIU` | `DANH_SACH_PHIEU_XUAT_GIU` (ngang, 8 cột) | `danh_sach_phieu_xuat_giu.xlsx` |

HRM: nút Xuất mở `ExportFieldsModal` chọn trường trước (rule SRS), In dùng trang `print-list.vue`
khổ ngang như 3 màn giữ hàng đã port.

### 1.14 File đính kèm

Cả 2 màn upload lên S3 (`CmcS3Helper::putFiles`), thư mục `product_prepick_requests` /
`warehouse_prepick_requests`; mimes `pdf,png,jpg,jpeg,doc,docx,xls,xlsx`, ≤ 13 MB; có API xóa từng file.
HRM dùng lại `BillPaymentAttachmentService` như các màn Tài chính khác.

---

## 2. Lỗi ERP phát hiện khi khảo sát — HRM sẽ vá

| # | Lỗi | Xử lý ở HRM |
|---|---|---|
| 1 | `WarehousePrepickRequestsController::exportList()` gọi `ProductPrepickRequestExcel` mà **thiếu `use`** → nút Xuất Excel màn PXG chết (Class not found) | HRM tự dựng export riêng, không dính |
| 2 | `WarehousePrepickRequest::canApprove()` viết `auth()->user()->info->company_id = $this->company_id` (**gán `=`** thay vì `==`) → điều kiện luôn truthy | Dùng `==`; nhưng nhánh BKS đang tắt (mục 4) |
| 3 | `ProductPrepickRequest::printListData()` gọi `Carbon::parse($item->approved_time)` **không guard null** → phiếu chưa duyệt in ra **ngày hôm nay** | Để trống khi chưa duyệt |
| 4 | `store()` gán `code = randomString(20)` rồi mới `generateCode()` — 2 lần ghi, mã rác nếu transaction gãy | Sinh mã 1 lần theo id |
| 5 | `store()` dùng **bitwise `\|`** trong `if ($request->type == 1 \| $request->type == 2)` → điều kiện luôn đúng với type ≠ 0, `$parent` bị nạp sai kiểu | So sánh đúng bằng `in_array` |
| 6 | `update()` của PYCXG **không reset** `manager_approver_id` / `board_of_manager_approver_id` khi phiếu bị trả về sửa lại → chi tiết vẫn hiện người duyệt cũ | Reset đủ cả 3 cấp |
| 7 | `update()` luôn dùng `config.max_prepick_date`, **quên** `max_prepick_date_project_contract` cho loại 4 (store thì có) | Dùng cùng một hàm tính hạn cho cả store/update |
| 8 | PXG `validateProducts()` / `syncProducts()` so `$p['need_export'] != 'true'` — **so chuỗi**. Chỉ chạy đúng vì AngularJS gửi form-encoded. Gọi bằng JSON (boolean) là `need_export` về 0 → **phiếu lưu ra 0 dòng cần xuất mà không báo lỗi** | HRM ép kiểu bool ở FormRequest; đây là **bẫy chết người** khi chuyển sang API JSON |
| 9 | PXG `store()` khi `validateProducts` fail chỉ `return` mà **không `DB::rollBack()`** (update thì có) → phiếu rác còn lại trong DB | Rollback đủ |
| 10 | `deny()` cho phép **KT (canApprove, status 2)** từ chối, nút "Không duyệt" ở chi tiết vẫn hiện dù KT đã sang bước lập PXG | Giữ nút cho cả 3 cấp như ERP nhưng ghi rõ ở spec |
| 11 | PXG `exportList()` đặt `COLSPAN = 9` trong khi bảng in chỉ có **8 cột** | Đếm đúng cột |
| 12 | Cả 2 màn **không có bảng lịch sử thao tác** | Thêm `product_prepick_request_histories` + `warehouse_prepick_request_histories` như 3 màn giữ hàng đã port |
| 13 | `delete()` xóa cứng cả bảng chi tiết | Giữ lịch sử (đã chốt ở các màn trước) |
| 14 | Màu trạng thái: "Đang tạo" gán `danger` (đỏ), "Chờ KT/BGĐ duyệt" cũng `danger` | Theo bảng màu SRS: nháp = xám, chờ duyệt = cam |
| 15 | `checkSwitchApprove()` chia `total_after_vat` **không chặn 0** → lỗi chia 0 | Chặn mẫu số 0 (đã vá ở màn Điều chuyển) |

---

## 3. Cấu trúc file dự kiến (HRM)

**BE `Modules/Finance/`**

```
Entities/PrepickExport/
    ProductPrepickRequest.php            ProductPrepickRequestDetail.php
    ProductPrepickRequestHistory.php
    WarehousePrepickRequest.php          WarehousePrepickRequestDetail.php
    WarehousePrepickRequestHistory.php
Services/
    ProductPrepickRequestService.php     ProductPrepickRequestHistoryService.php
    WarehousePrepickRequestService.php   WarehousePrepickRequestHistoryService.php
Http/Controllers/V1/
    ProductPrepickRequestController.php  WarehousePrepickRequestController.php
Http/Requests/PrepickExport/*            Transformers/PrepickExportResource/*
Resources/views/prints/                  (2 mẫu in phiếu + 2 mẫu in danh sách, khổ ngang)
database/migrations/                     (2 bảng lịch sử)
```

**FE**

```
pages/finance/product-prepick-requests/    index · create · _id/index · _id/edit · _id/print
                                           print-list · components/{Form, RejectModal, export-excel}
pages/finance/warehouse-prepick-requests/  index · create · _id/index · _id/edit · _id/print
                                           print-list · components/{Form, export-excel}
```

**Dùng lại, KHÔNG viết mới**
- `PrepickStockService` — ghi tồn giữ (**thêm `addLot()`**, là hàm mới duy nhất cần bổ sung).
- `AccountingStockService::detail()` — cột "Có thể giữ" (**cần thêm `in_promotion`**, xem mục 4).
- `PrepickLotContractService` — nếu cần suy hợp đồng của lô.
- Ngưỡng % đã thu: tách hàm chung từ `PrepickExtendRequestService` / `PrepickTransferRequestService`
  (2 màn đó đang có bản riêng) thay vì viết bản thứ ba.
- Popup chọn hàng: dùng popup tìm hàng hóa dùng chung `type=has_stock` (đây là tồn **KHO**),
  KHÔNG dùng `PrepickStockSearchModal` (popup tồn **hàng giữ**).
- `BillPaymentAttachmentService` · `ChecksEmployeePermission` · helper `statusBadgeVariant` ·
  `apiErrorMessage` · `sanitizeNumberEvent`.

---

## 4. Quyết định đã chốt (user chốt 2026-09-03)

| # | Vấn đề | **Chốt** |
|---|---|---|
| 1 | **Loại 1–4 có port không?** `gop_db` chỉ có phiếu loại 5 (501) và 99 (1.673); loại 1–4 = 0 phiếu suốt 08/2025→07/2026. Bảng nguồn: `contracts` (loại 1–2) **1 dòng** — chết · `project_contracts` (loại 4) **0 dòng** — chết · `wr_service_contracts` (loại 3) **6.676 dòng** · `firm_contracts` (loại 5) 23.277 dòng | ✅ **Port ĐỦ 6 LOẠI**, cả BE lẫn form Thêm mới. ⇒ phải dựng **5 popup chọn hợp đồng** (HĐ bán, HĐ khuyến mại dùng chung popup HĐ bán, HĐDV, HĐDA, HĐ hãng) và **xin dump dữ liệu loại 1–4 từ dev** mới test được |
| 2 | **Nhánh BKS duyệt PXG (status 4)** — ERP comment toàn bộ nút + luồng | ✅ **Bỏ hẳn** ở HRM (vẫn đọc được status 4 của dữ liệu cũ; `gop_db` có 0 dòng). Khớp memory `project_prepick_bks_approval_disabled` |
| 3 | **Sửa `AccountingStockService::detail()`** thêm `in_promotion` — file dùng chung của 2 màn đã chạy | ✅ **Được sửa**. Chỉ **THÊM** field, không đổi field cũ → 2 màn kia giữ nguyên hành vi, nhưng **bắt buộc test lại** màn Chuyển hàng + Gia hạn sau khi sửa |
| 4 | **Tách hàm ngưỡng % đã thu** ra service dùng chung (hiện có 2 bản ở màn Gia hạn + Điều chuyển) | ✅ **Được tách** sang `PrepickApprovalRouteService`; sửa 2 màn cũ gọi lại và **test lại cả 2** |
| 5 | **Middleware `checkDueConfigs`** (chặn người còn hàng giữ / hàng mượn quá hạn lập phiếu mới) chưa có ở HRM | ✅ **Port cùng đợt này** (thêm 1 phase riêng) |
| 6 | Nhãn nút trả phiếu: ERP ghi "Không duyệt", skill `button-convention` quy định **"Từ chối"** | Theo **skill** → nút ghi **"Từ chối"**. Trạng thái phiếu vẫn hiển thị theo dữ liệu ERP |
| 7 | Phân quyền theo cấp: giữ 3 cấp ERP hay thêm **bộ phận** | Giữ **đúng 3 cấp ERP** (tổng công ty / công ty / phòng ban), không tự thêm cấp |

---

## 5. Chặn trước khi code

1. Hai repo đang đứng ở nhánh `feat/finance-prepick-transfer-request`, **working tree sạch** →
   tách nhánh mới `feat/finance-prepick-export-request` từ `gop_db`.
2. ⛔ **Cần xin dump dữ liệu phiếu loại 1–4 từ dev** — đã chốt port đủ 6 loại nhưng local `gop_db`
   có 0 phiếu loại 1–4, không đối chiếu được. Trong lúc chờ vẫn code được (nghiệp vụ đọc từ ERP),
   nhưng **không được báo xong** khi chưa bấm thật 4 loại đó.
3. ✅ Đã kiểm bảng nguồn hợp đồng trên `gop_db`: `contracts` 1 dòng, `project_contracts` 0 dòng
   (2 bảng gần như chết — popup chọn HĐ của loại 1, 2, 4 sẽ rỗng trên local) ·
   `wr_service_contracts` 6.676 · `firm_contracts` 23.277.
