# Khảo sát A — Phiếu nhập kết quả (ERP → HRM): Danh sách · Phạm vi · Chi tiết · Xóa · Không duyệt · deleteFile · In/Xuất · Thông báo · Menu

Người khảo sát: subagent cho @khoipv · Ngày 02/11/2026 · CHỈ ĐỌC (không sửa code/DB).
Nhánh: hrm-api `develop`, hrm-client `develop` (con của `gop_db`) · ERP `D:\laragon\www\erp` (DB `gop_db`, chung với HRM).

Viết tắt: **C** = `app/Http/Controllers/Customercare/WrImportResultsController.php` · **M** = `app/Model/Customers/WrImportResult.php` ·
**V/** = `resources/views/customercare/warranty_repair_import_results/` · **PGV** = phiếu giao việc (`wr_assign_tasks`) ·
**PNKQ** = phiếu nhập kết quả (`wr_import_results`) · **ATP** = `assign_task_progress`.

---

## 0. Hằng số

`wr_import_results.status` (M:43-81, `STATUSES` — thứ tự mảng = thứ tự option ô lọc):

| id | Hằng | Nhãn nguyên văn | `type` (màu ERP) | Số phiếu DB thật |
|---|---|---|---|---|
| 1 | DANG_TAO | Đang tạo | danger | 4 |
| 2 | CHO_DUYET_KET_QUA | Chờ duyệt kết quả | warning | 197 |
| 5 | DANG_DUYET_KET_QUA | Đang duyệt kết quả | warning | 2 |
| 3 | DA_DUYET_KET_QUA | Đã duyệt kết quả | success | 6 661 |
| 4 | CHO_BKS_DUYET | Chờ BKS duyệt kết quả | warning | **0** (không bao giờ được set) |
| 6 | KHONG_DUYET | Không duyệt kết quả | danger | 56 |

Tổng 6 920 phiếu; công ty 1: 6 537 · 4: 331 · 3: 52. `company_id`/`department_id` không có dòng NULL (gán ở `boot()::created` M:83-99 theo **người tạo**).

PGV liên quan (WrAssignTask.php:31-39): 1 DANG_GIAO "Chờ thực hiện" · 7 DANG_NHAP_KET_QUA · 2 DA_NHAP_KET_QUA · 8 DANG_DUYET_KET_QUA · 3 DA_DUYET_KET_QUA · 9 HUY.
Đối chiếu DB (PNKQ.status × PGV.status): 1↔7 (4) · 2↔2 (197) · 3↔3 (6 661) · 5↔8 (2) · **6↔2 (56)** — "Không duyệt" KHÔNG đổi trạng thái PGV.

ATP (AssignTaskProgress.php:56-79): `request_type` 1 HĐ · 2 SUA_CHUA_BAO_DUONG · 3 BAO_HANH · 4 LAP_DAT · 5 GIAO_VIEC_KHAC; `current_stage` 1 REQUEST_TASK · 2 ASSIGN_TASK · 3 BUSINESS_REQUEST · 4 IMPORT_RESULT · 5 APPROVER_RESULT; `type` 1 REPAIR · 2 EXTEND_PRODUCT · 3 MERCHANDISE · 4 ITEM · 5 WARRANTY · 6 REVENUE_COST; `status` 1 DA_DUYET · 2 KHONG_DUYET (DB: 1 = 18 510, 2 = 127, NULL = 47).

---

## 1. Danh sách

### 1.1 Route / lối vào

- `GET admin/customer-care/wr_import_results/` → `index` (C:77-81): `$type = $request->type ?? 'index'`, truyền vào blade; blade gửi `d.type` khi gọi `searchData` (V/index.blade.php:43).
- `GET .../searchData` → C:89-171 (Yajra Datatables, serverSide).
- Route `/all` (`WrImportResults.all`, routes/web.php:6160) trỏ `WrImportResultsController@all` — **hàm không tồn tại** (route chết).
- Tiêu đề trang: "Danh sách phiếu nhập kết quả" (V/index.blade.php:12).

### 1.2 Phạm vi theo `type` (M:241-283)

Eager load `wr_assign_task`, `wr_approve_result.employee_approved`, `employee_create` (M:243).

| `type` | Điều kiện |
|---|---|
| `all` (menu) | Theo quyền (if/else-if, lấy quyền cao nhất): **tổng công ty** → không bó · **công ty** → `company_id = cty mình OR created_by = mình` · **phòng ban** → `department_id ∈ employee_manage_departments(employee_id = mình, company_id = cty mình) OR created_by = mình` · không quyền → `created_by = mình`. **Sau đó luôn thêm** `status != 1 OR (created_by = mình AND status = 1)` (phiếu "Đang tạo" chỉ người tạo thấy). M:251-275 |
| `index` (mặc định khi không có `type`) | `created_by = mình` (M:276-277) — không lọc trạng thái |
| `wait_approve_result` (dashboard + redirect sau duyệt) | **chỉ khi** có quyền `Duyệt phiếu nhập kết quả`: `status = 2 AND company_id = cty mình` (M:277-279). **Không có quyền → rơi khỏi mọi nhánh, KHÔNG bó phạm vi gì (thấy toàn hệ thống)** — lỗi ERP, xem mục 6 |
| giá trị khác | không bó phạm vi (cùng lỗi trên) |

Người duyệt (canApproveResult) KHÔNG được thêm vào phạm vi `type=all` dù `canView` cho họ xem chi tiết (M:233-236). Người thực hiện PGV cũng không được thêm.

Super Admin bên ERP: `Gate::before` → `can()` luôn true → nhánh tổng công ty.

### 1.3 Cột (V/index.blade.php:46-59 + C:93-145)

| # | Tiêu đề nguyên văn | `data` | Nguồn hiển thị | Link | Sort (Yajra `orderable`) |
|---|---|---|---|---|---|
| 1 | STT | DT_RowIndex | số thứ tự | – | không |
| 2 | Số phiếu nhập kết quả | code | `wr_import_results.code` | `WrImportResults.show` tab mới (C:96-98) | có (cột thật) |
| 3 | Số phiếu giao việc | assign_task_code | `wr_import_results.wr_assign_task_code` (cột lưu sẵn) | `WrAssignTasks.show` tab mới (C:99-101) | khai có — nhưng `assign_task_code` **không phải cột DB** (cột là `wr_assign_task_code`) → sort nhiều khả năng lỗi SQL/không tác dụng |
| 4 | Số hợp đồng | wr_contract_code | PGV có `wr_service_contract_id` → `wr_service_contracts.code`, link theo `wr_service_contract.type`: 1 `WarrantyRepairContracts.show` · 2 `WrWarrantys.show` · 3 `WarrantyRepairContractAdditionAnnex.show` · 4 `WarrantyRepairContractAnnex.show` (cùng tab); PGV có `assembly_request_id` → `wr_import_results.firm_contract_code` link `firmContract.show` tab mới (rỗng nếu `firm_contract_id` null); khác → '' (C:102-117) | như trên | khai có — không phải cột DB → như #3 |
| 5 | Số phiếu Y/C | request_code | PGV `assembly_request.code` → `assemblyRequest.show` · `assign_other_request.code` → `assignOtherRequest.show` (tab mới) (C:118-125) | như trên | khai có — không phải cột DB → như #3 |
| 6 | Khách hàng | customer | `customer_code . '-' . customer_name` (C:129-131) | – | không |
| 7 | Người tạo | created_by | `employee_create->fullname` (chỉ tên, KHÔNG kèm SĐT) (C:132-134) | – | không |
| 8 | Ngày tạo | created_at | `d/m/Y - H:i` (C:93-95 & 135-137 — khai 2 lần) | – | có |
| 9 | Người duyệt | approver | `wr_approve_result.employee_approved.fullname` = PGV con (`wr_assign_tasks.parent_id = wr_assign_task_id`) → `approved_by` (M:107-110, C:138-140) | – | không |
| 10 | Ngày duyệt | approved_time | `wr_approve_result.approved_time` `d/m/Y - H:i` (C:141-145) | – | không |
| 11 | Trạng thái | status | `getStatus(status, STATUSES)` badge theo `type` (C:126-128) | – | có |
| 12 | Hành động | action | dropdown ⚙ (C:147-164) | – | không |

Mặc định: `orderBy created_at desc` khi DataTables không gửi `order` (M:345-347); `order: []` ở Datatable.blade.php:493.
Dữ liệu thật: PGV con (phiếu duyệt) có `approved_by`/`approved_time` ở 4 310/6 664 dòng.

### 1.4 Ô lọc (V/index.blade.php:60-86 + M:285-343)

| Placeholder nguyên văn | key gửi | Kiểu | BE lọc |
|---|---|---|---|
| Số phiếu nhập kết quả | `code` | text | `code like %x%` |
| Số phiếu giao việc | `assign_task_code` | text | `wr_assign_task_id IN (wr_assign_tasks.code like %x%)` |
| Số hợp đồng | `wr_contract_code` | text | PGV có `wr_service_contract.code like` **hoặc** `assembly_request.firm_contract_code like`, **hoặc** `wr_import_results.firm_contract_code like` (M:293-307) |
| Số phiếu y/c | `request_code` | text | `wr_assign_task_id IN` (PGV có `assembly_request.code like` ∪ `assign_other_request.code like`) |
| Khách hàng | `customer_id` | select-ajax `customers.searchCustomerByKeywords` | `customer_id =` |
| Người tạo | `created_by` | select-ajax `employee.searchEmployeeByKeyword?all_status=1` | `created_by =` |
| Người duyệt | `approved_by` | select-ajax như trên | `whereHas wr_approve_result approved_by =` |
| Trạng thái | `status` | select (STATUSES) | `status =` |
| Từ ngày / Đến ngày | `startDate` / `endDate` | date (`search_by_time: true`) | `DATE(created_at) >= start` · `DATE(created_at) < end + 1 ngày` |
| (Công ty) / Phòng ban / (Bộ phận) | `company` / `department` / `part` | select — DATATABLE tự sinh khi `search_by_info` (`type == 'all'`) và có quyền xem theo cấp (Datatable.blade.php:142-176) | **BE KHÔNG đọc 3 key này → ô lọc chết** (mục 6) |

Ô Công ty/Phòng ban/Bộ phận do DATATABLE quyết theo `is_big_boss/is_boss/is_manager` = quyền "Xem phiếu nhập kết quả theo …" (index.blade.php:84-86) **hoặc** quyền chung `Xem tất cả phiếu` / `Xem tất cả phiếu của công ty` / `Xem tất cả phiếu của phòng ban` (Datatable.blade.php:10-12): big_boss → Công ty + Phòng ban; boss → Phòng ban (cty mình); manager → Phòng ban (`Auth::user()->departments`) + Bộ phận.

### 1.5 Hành động dòng (C:147-164)

| Nút (nguyên văn) | Điều kiện | Thực hiện |
|---|---|---|
| Sửa | `canEdit()` = `created_by == mình AND status ∈ {1 Đang tạo, 6 Không duyệt}` (M:350-353) | `WrImportResults.edit` (cùng tab) |
| Xóa | cùng `canEdit()` | `GET {id}/delete`, popup chung `partials.confirm`: tiêu đề "Xác nhận xóa!", nội dung "Bạn chắc chắn muốn xóa bản ghi này?", nút "Xác nhận"/"Hủy" → `window.location = href` (confirm.blade.php:4-25) |
| Duyệt kết quả | `canApproveResult()` = `status == 2 AND can('Duyệt phiếu nhập kết quả') AND company_id người xem == company_id phiếu` (M:355-358) | `WrApproveResults.create?wr_import_result_id={id}` (cùng tab) → HRM: link ERP tab mới (user chốt) |
| Không duyệt kết quả | cùng `canApproveResult()` | popup nhập lý do (mục 3.2) → `GET {id}/reject` |

Không có hành động Xem (xem bằng link Số phiếu). Super Admin KHÔNG có ngoại lệ ở `canEdit` (chỉ người tạo) nhưng có ở `canApproveResult` qua `Gate::before` (vẫn phải cùng công ty).

### 1.6 Toolbar — In / Xuất / Tạo mới

DATATABLE chỉ sinh nút khi truyền option `create_link` / `print_link` / `print_link_with_params` / `export_link` / `export_link_with_params` / `export_pdf_link` (Datatable.blade.php:106-123). Màn này **không truyền option nào** (`create_link` bị comment, index.blade.php:87) → **ERP KHÔNG có In, Xuất Excel, Tạo mới** ở danh sách. Controller cũng không có `printList`/`exportList`. Trên HRM: Xuất Excel + Cấu hình cột + Lịch sử là bộ bắt buộc (skill); In danh sách — cần user chốt (Phiếu giao việc có In vì ERP có).

---

## 2. Chi tiết (show) — C:1389-1652, V/show.blade.php, V/form_show.blade.php

### 2.1 Quyền `canView()` (M:207-239)
Theo thứ tự: Super Admin → true · người tạo → true · nếu `status != 1`: quyền tổng công ty → true; quyền công ty + `company_id` khớp cty người xem → true; quyền phòng ban + `department_id ∈ employee_manage_departments(mình, cty mình)` → true · cuối cùng `canApproveResult()` → true · còn lại false → `view('not_found')` (C:1394-1396).
Không đạt → HRM: 403 → FE `/pages/extras/404` (khuôn PGV).

### 2.2 Dữ liệu nạp
- **Dùng `getForEdit($id)` chứ KHÔNG dùng `getForShow`** (C:1393). `getForShow` (M:1211-1249) không được gọi ở show web (chỉ còn là code thừa; `apiShow` C:2913 cần kiểm riêng).
- `getForEdit` (M:1251-1336): `galleries_construction` (url), `galleries_handover` (id,url), `wr_assign_task.assign_other_request`, `wr_assign_task.customer`, `product_repairs` (type 2) + `product_device_errors`, `product`, `wr_import_result_product_items`, `wr_import_result_product_services`; `extend_products.services.products.product`; `product_warrantys` (type 1) cùng bộ; `product_assembly` (type 3); `item_warrantys/repairs/extends` (type 1/2/3); `service_warrantys/repairs` (type 1/2); `costs` (type 1), `revenue_costs` (type 2), `works`, `executors`, `employee_create.info`; `attachments` json_decode. PGV có `wr_service_contract_id` → gắn `serials`, `product_stock_qty` từ `Customer::getListProductOfCustomer(customer_id)` theo khoá `product_id|type` (`tpc` → `tp`).
- Hậu xử lý ở controller:
  - `product_assembly`: `serials` json_decode; đảo thứ tự thuộc tính `qty`/`delivery_qty` (chỉ thứ tự JSON) (C:1397-1414).
  - `$wr_assign_task = WrAssignTask::getForShow(wr_assign_task_id)` (C:1416) — dùng cho `timesheets` (tab Chấm công) và tra `rate_effort`.
  - `product_repairs`: **`delivery_qty` bị gán = `qty`** (C:1426); items/services: `available_qty ?? 0`, `qty ?? 1`, services `is_completed` → bool; gắn `items`, `services`; `type_status` = `wr_assign_task_products.type` (handle_type 1); `rate_effort`: có `device_error_id` → lấy từ `wr_assign_task_products` (khớp product_id + device_error_id + serial_old + handle_type 1); không có → Σ dịch vụ của `wr_assign_task_extend_products` khớp product_id + serial_old với công thức `$cur->qty ? ($cur->rate_effort || 0) : 0` (C:1418-1491).
  - `product_warrantys`: tương tự, `type_status` = `wr_assign_task_products.type` (handle_type 0) — **không guard null** (C:1559).
  - `assign_other_request_code` nếu có (C:1612-1614); galleries → mảng url (C:1616-1633).
- JS: `new WrImportResult(@json($object), {mode:'show'})`, `$scope.show = true`, `form.wr_assign_task_timesheet = $wr_assign_task.timesheets` (show.blade.php:36-40).

### 2.3 Bố cục form_show (V/form_show.blade.php)
- Thanh tab: **Thông tin khách hàng** · **Chấm công** · **File ảnh đính kèm**; góc phải `form.creator - form.created_time` (:41-58).
- Tab Thông tin khách hàng (:60-145): Phiếu giao việc (link ERP PGV tab mới) · Phiếu YCGV khác (nếu `assign_other_request_id`) · Hợp đồng (nếu `assembly_request_id`, link `/admin/sale/firm-contracts/{firm_contract_id}`) · Khách hàng `mã - tên` · Địa chỉ lắp đặt (lắp đặt/HĐ) · Người liên hệ · SĐT liên hệ · Người yêu cầu · SĐT Người yêu cầu · **Ghi chú (textarea KHÔNG disabled ở màn Xem, không có nút lưu)**.
- Tab Chấm công (:269-310): bảng STT · Ngày làm việc · Chấm công theo HRM (Checkin/Checkout/Giờ làm việc) · Điều chỉnh theo thực tế (Checkin/Checkout/Giờ làm việc) — nguồn `wr_assign_task_timesheets` của PGV, readonly ở show.
- Tab File ảnh đính kèm (:311-381): Ảnh công trình · Ảnh biên bản bàn giao (fancybox xem ảnh, file khác hiện icon + tên).
- Card theo nguồn: `wr_service_contract_id` → "A - TÍNH CÔNG BẢO HÀNH SỬA CHỮA" (I - Bảo hành · I - Dịch vụ sửa chữa · II. Danh mục thiết bị cần bảo dưỡng) (:385) · `assembly_request_id` → "A - Hạng mục lắp đặt, bàn giao" / "I - Lắp đặt, bàn giao" (:898) · `assign_other_request_id` → "A - TÍNH CÔNG DỊCH VỤ ĐÍNH KÈM" / "I - Dịch vụ đính kèm" (:1005) · luôn: "B - Công phụ tính P3" (I - Công việc phụ tính P3 · II - Tổng công định mức · VI - Nhân sự tham gia) (:1059) · không HĐ + có items → "B - DANH SÁCH GIAO NHẬN VẬT TƯ" (I - Cho bảo hành · II - Cho sửa chữa - Bảo dưỡng · III - Hàng bán thêm) (:1243) · HĐ + `item_extends` → "C - DANH SÁCH VẬT TƯ BÁN THÊM" (:1433) · không HĐ + services → "C/B - DANH SÁCH (DỊCH) VỤ TRẢ TIỀN" (:1478, tiêu đề B viết thiếu chữ "DỊCH"; điều kiện card mâu thuẫn với điều kiện tiêu đề — tiêu đề đòi `wr_service_contract_id` mà card đòi `!wr_service_contract_id` → **khối này không bao giờ có tiêu đề**). Khối "III - Các chi phí liên quan" bị comment (:1607-1743). Chi tiết cột từng khối → khảo sát phần form (B).
- **Ghi chú duyệt** (:1745-1784): nếu `canApproveResult()` → textarea sửa được (nhưng **không nối vào nút Không duyệt** — popup dùng ô riêng → ô này chết); ngược lại hiện readonly khi có `approve_comment`.
- Footer (:1786-1815): **Không duyệt** (đỏ, `ng-click reject()`) + **Duyệt kết quả** (link `WrApproveResults.create?wr_import_result_id=`) — cả 2 chỉ khi `canApproveResult()`; **Quay lại** → `WrImportResults.index?type=all`. "Lưu"/"Lưu & Gửi duyệt" có `ng-if="!show"` → ẩn ở show. **Không có Sửa/Xóa/In ở màn chi tiết.**

### 2.4 Khác biệt form_show so với form (diff 2 file)
form_show: bỏ dropzone upload + nút xoá ảnh + text định dạng/dung lượng + lỗi validate galleries; tab "File ảnh đính kèm" không có `(*)`/icon lỗi; SL vật tư (`product_item.qty`, `product.qty` dịch vụ BD) hiện chữ thay vì input; bỏ `ng-change="w.changeCompleted()"` ở ô tích P3; `| number` thay `| my_number` ở tổng SC; xê dịch ô trống/colspan (bảng BH thêm 1 ô trống, SC colspan 5→4 + thêm ô, "Danh sách dịch vụ/vật tư" colspan 10→9) — có thể lệch cột so với tiêu đề. Còn lại giống hệt (cùng nhãn).

---

## 3. Xóa và Không duyệt

### 3.1 Xóa — `GET {id}/delete` (C:2486-2760)

Điều kiện: `canEdit()` (người tạo + status 1/6). **Không đạt → không làm gì, vẫn redirect, không báo lỗi.** 1 transaction.

1. **Lắp đặt** — nếu PNKQ có `product_assembly` (type 3): với mỗi `wr_assign_task_assembles` của PGV, tìm ATP `import_result_id = PNKQ.id AND product_id AND request_type = 4` (first) → xoá `assign_task_serial_progress` của ATP; ATP: `import_result_id/qty/detail_id/time_update = NULL`, `approver_result_id = NULL`, `approver_result_qty = 0`, `approver_result_time_update/detail_id = NULL`, `success_percent = NULL`, `serial = NULL`, `can_request_qty = assign_task_qty`, `current_stage = 2`. (C:2493-2519)
2. **SC** — nếu PGV `product_repairs`: ATP `assign_task_id = PGV, request_type 2, type 1, contract_type 'wr_service'`; với mỗi SP của PGV lấy ATP **đầu tiên theo product_id**: reset như trên + `serial = wr_assign_task_products.serial`, `can_request_qty = delivery_qty = assign_task_qty`, `current_stage = 2`; xoá hết `itemProgress`, `serviceProgress`; tạo lại `assign_task_service_progress` (name = cost_name, parent_id = cost_id, qty/assign_task_qty/can_request_qty/delivery_qty = qty, available_qty) từ `services` của dòng PGV và `assign_task_item_progress` (name, parent_id = product_id, unit_id, qty, assign_task_qty, available_qty) từ `items`. (C:2521-2577)
3. **Bảo dưỡng (extend)** — ATP type 2: reset + `serial = extend_product.serial`, `current_stage = 2` (**không** reset `can_request_qty`/`delivery_qty`); xoá `serviceItemProgress` + `serviceProgress`; tạo lại service progress (name = service_name, parent_id = service_id, type_id = level_id, qty…) + service item progress (C:2579-2639).
4. Hàng bán thêm (merchandise): **comment, không làm** (C:2641-2653).
5. **BH** — ATP request_type 3, type 5: như SC (C:2655-2710). **Không** tính lại `wr_service_contracts.is_assign` (khác reject).
6. **GVK** — ATP request_type 5, type 6: lấy theo `product_id = cost_id`, reset các cột import/approver (**không guard null** → nổ nếu không có) (C:2712-2731).
7. Xoá: `wr_import_result_items`, `wr_import_result_products`, `wr_import_result_services`, `wr_import_result_product_device_errors` (theo `wr_import_result_id`), `costs()` (**chỉ type 1**), `executors`, `works`, rồi `wr_import_results` (hard delete) (C:2733-2740).
   **KHÔNG xoá**: `wr_import_result_costs` type 2 (revenue_costs), `wr_import_result_product_items`, `wr_import_result_product_services`, `wr_import_result_extend_products` (+`_services`, +`_service_items`), `wr_import_result_galleries_constructions/handovers`, `wr_import_result_other_services` → mồ côi. DB thật có mồ côi: galleries_constructions 7, galleries_handovers 7, product_items 1, product_services 3.
8. PGV: `status = 1 (DANG_GIAO "Chờ thực hiện")` (C:2742-2744) → nút "Nhập kết quả" ở PGV hiện lại (`canImportResult` cần status 1).
9. Không đổi ATP.`status` (phiếu đã "Không duyệt" thì ATP.status = 2 vẫn giữ). Không thông báo. Không ghi lịch sử.
10. Kết thúc: `redirect()->route('WrImportResults.index')` (**không kèm `?type=all`** → về danh sách `index` = phiếu mình tạo), **không toast**. Lỗi: `Log::error` + rollback + redirect im lặng (C:2753-2758).

Lưu ý `wr_import_results.wr_assign_task_id` là **UNIQUE** → bắt buộc hard delete thì mới nhập lại được.

### 3.2 Không duyệt kết quả — `GET {id}/reject?approve_comment=` (C:2762-2911)

Popup (index.blade.php:90-145 và show.blade.php:44-99, giống nhau): tiêu đề **"Xác nhận không duyệt!"**, nội dung "Bạn chắc chắn không duyệt kết quả này?", ô **"Lý do không duyệt" (*)**, lỗi trống **"Bạn phải nhập lý do không duyệt"** (show còn chặn chuỗi toàn khoảng trắng — index thì không), nút "Xác nhận" (đỏ) / "Hủy". Thành công: `toastr.success(message)` → về `WrImportResults.index?type=all`; `success=false` → `toastr.warning(message)`; lỗi HTTP → "Đã có lỗi xảy ra".

BE:
1. Validate `approve_comment` required → `{success:false, message:'Thao tác thất bại!', errors}` (C:2765-2777).
2. `canApproveResult()` sai → `'Không có quyền!'` (C:2781-2783).
3. PNKQ: `status = 6`, `approve_comment = lý do` (C:2784-2786). (DB: 5/56 phiếu status 6 có `approve_comment` rỗng — tạo bởi luồng khác, vd unApprove ở WrApproveResults cho phép nullable.)
4. ATP → `status = 2 (KHONG_DUYET)` cho: lắp đặt (`import_result_id = PNKQ, product_id, request_type 4`) · SC (request_type 2 type 1) · extend (type 2) · **merchandise (type 3 — có làm, khác delete)** · BH (request_type 3 type 5 — **không guard null**) · GVK (request_type 5 type 6); khớp ATP đầu tiên theo product_id (C:2790-2899).
5. BH: tính lại `wr_service_contracts.is_assign = canAssignTaskWarranty() ? 1 : 0` (C:2872-2882).
6. **PGV giữ nguyên status (2 "Đã nhập kết quả")**; không xoá/không reset cột import của ATP.
7. Thông báo: `NotificationHelper::sendNotify(created_by của PNKQ, route('WrImportResults.show', id, false), '<fullname người thao tác> vừa không duyệt phiếu nhập kết quả của bạn!')` (C:2902-2903) — thông báo ERP (notifiable `App\Employee`, app HRM không đọc). **Không** gọi cầu nối `notify-result` của HRM (#9816 chỉ gắn ở `WrApproveResultsController::unApprove` :2032 + approve :875/:1592).
8. `responseSuccess('Thao tác thành công!')`. catch `Exception` (không có `use`, không có `\`) → class `App\Http\Controllers\Customercare\Exception` không tồn tại → **không bắt được lỗi, không rollback có kiểm soát** (500).

### 3.3 deleteFile — `POST {id}/deleteFile` {file, position} (C:3318-3342)
- Chỉ màn **Sửa** gọi (edit.blade.php:183-213, popup "Xác nhận!" / "Bạn chắc chắn muốn xóa file này?"); ở form chỉ còn sống 2 vị trí `ir` (vật tư SC) và `ie` (hàng bán thêm), các vị trí khác bị comment; form_show ẩn (`ng-if="!show"`).
- `canEdit()` sai → "Không có quyền"; file không có trong `attachments[position]` → "Không có file"; `unlink(public_path().file)` (file thật lưu **S3** qua `CmcS3Helper::putFile` C:767-783 → unlink vô tác dụng, file S3 không bị xoá); `array_diff` giữ key → JSON có thể thành object; trả "Xóa thành công" + `data.attachments`.
- **DB thật: 0/6 920 phiếu có `attachments`** → chức năng gần như không dùng. Thuộc màn Sửa (phần B), không thuộc show.

### 3.4 Thông báo liên quan màn (tổng hợp)
| Sự kiện | Người nhận | Nội dung nguyên văn | Link | Nơi |
|---|---|---|---|---|
| Lưu & Gửi duyệt (status 2) | mọi NV có quyền `Duyệt phiếu nhập kết quả` **cùng công ty người thao tác** (`sendNotifyWithPermission`, NotificationHelper:40-69) | "Bạn có 1 phiếu kết quả giao việc cần duyệt" | `WrApproveResults.create?wr_import_result_id=` | C:333-334 (store), :925-926 (storeApp), :2024-2025 (update), :3166, :3307 (api) |
| Không duyệt (màn này) | người tạo PNKQ | "{fullname} vừa không duyệt phiếu nhập kết quả của bạn!" | `WrImportResults.show` | C:2902-2903 |
| Xóa | – | không có | – | – |
| Dashboard ERP | NV có quyền `Duyệt phiếu nhập kết quả` | ô "Chờ duyệt phiếu nhập kết quả giao việc" (đếm status 2 cùng công ty) | `WrImportResults.index?type=wait_approve_result` | HomeController.php:1884-1894 |

HRM đã có endpoint `POST v1/assign/wr_import_results/{id}/notify-result` (Modules/Assign/Http/Controllers/Api/V1/WrImportResultController.php:71-118): NotificationMeta `CONG_VIEC`/`PNKQ`/"Từ chối" + "Lý do: …", type `wrImportResult`, url `/assign/assign_import_result/{id}` → nên tái dùng khi port Không duyệt (cần user chốt, mục 8).

---

## 4. Quyền ERP liên quan (database/seeds/PermissionsTableSeeder.php)

| Tên nguyên văn | Seeder | Chỗ dùng |
|---|---|---|
| `Xem phiếu nhập kết quả theo tổng công ty` | :664 (legacy id 100435) | M:217, M:246 (searchByFilter), index.blade.php:84 |
| `Xem phiếu nhập kết quả theo công ty` | :665 (100436) | M:220, M:247, index.blade.php:85 |
| `Xem phiếu nhập kết quả theo phòng ban` | :666 (100437) | M:223, M:248, index.blade.php:86 |
| `Duyệt phiếu nhập kết quả` | :627 (100419) | M:277 (wait_approve_result), M:357 (canApproveResult → nút Duyệt/Không duyệt, xem chi tiết, reject), HomeController:1884, người nhận thông báo C:334… |
| `Nhập kết quả thực hiện` | :626 (100418) | WrAssignTask.php:404 (`canImportResult`), :479 (phạm vi PGV) — không dùng trực tiếp ở màn PNKQ |
| `Xem tất cả phiếu` / `Xem tất cả phiếu của công ty` / `Xem tất cả phiếu của phòng ban` | (quyền chung) | Datatable.blade.php:10-12 — chỉ bật ô lọc Công ty/Phòng ban (chết) |

Không có quyền riêng cho Sửa/Xóa (chỉ người tạo). Không middleware quyền trên route.
**DB gop_db local: bảng `permissions` KHÔNG có 5 quyền ERP trên** (chỉ có quyền guard `api` của HRM: `Nhập kết quả công việc` id 194, `Nhập kết quả công tác` 207… — khác nghĩa). Theo skill: HRM tạo quyền mới `type` CSKH sau bán (24, như PGV), tên nguyên văn ERP.

---

## 5. DB thật (tinker, chỉ SELECT)

### 5.1 Bảng + số dòng
`wr_import_results` 6 920 · `_products` 15 255 (type 1 BH 3 865 · 2 SC 2 371 · 3 lắp đặt 9 019) · `_product_items` 1 483 · `_product_services` 3 458 · `_product_device_errors` 2 404 · `_extend_products` 1 183 · `_extend_product_services` 1 348 · `_extend_product_service_items` 55 · `_items` 1 713 (type 2: 1 442 · 3: 271 · type 1: 0) · `_services` 3 514 (1: 371 · 2: 3 143) · `_costs` 26 160 (type 1: 25 470 · 2: 690) · `_works` 645 · `_executors` 10 622 · `_galleries_constructions` 11 297 · `_galleries_handovers` 8 258 · `_other_services` **0**.
Tên bảng = mặc định Laravel (các model con ERP không khai `$table`).

### 5.2 Cột `wr_import_results` (bẫy)
`id` · `wr_assign_task_id` bigint **NOT NULL UNIQUE** · `code` varchar **NOT NULL UNIQUE không default** (ERP sinh sau insert bằng `generateCode()` M:188-205: `{company.code}.PNKQ.{YYYY}{id đệm 6}` theo công ty **người tạo**, vd `TPE.PNKQ.2026007047`, `TPSG.PNKQ.2026007046`) · `wr_assign_task_code`, `customer_id/name/code` nullable (thực tế đủ) · `created_by`, `updated_by` bigint **NOT NULL không default** · `attachments` text (0 dòng có dữ liệu) · `sw_note`, `sr_note`, `note` varchar(255) · `status` tinyint **NOT NULL không default** · `company_id`, `department_id` nullable (gán sau insert ở `boot`) · `approve_comment`, `bks_approve_comment` text · `delivery_place`, `customer_contact_name/phones` · `firm_contract_id/code` (1 157 dòng có) · `creator_request`, `phone_creator`.
**Không có cột `approved_by`/`approved_time`** — người/ngày duyệt nằm ở PGV con (`wr_assign_tasks.parent_id`).

### 5.3 Cột bảng con (NOT NULL không default — bẫy khi ghi)
- `_costs`: `wr_import_result_id`, `cost_name` NOT NULL; `type` default 1 (1 chi phí · 2 revenue_costs).
- `_executors`: `wr_import_result_id`, `employee_id` NOT NULL.
- `_galleries_*`: `wr_import_result_id`, `url` NOT NULL.
- `_items`: `wr_import_result_id`, `product_name`, `product_code`, `product_id`, `type` NOT NULL (type không default).
- `_other_services`: `wr_import_result_id` **int** (khác bigint các bảng khác), `name`, `price` NOT NULL.
- `_product_device_errors`: `wr_import_result_product_id`, `wr_import_result_id`, `device_error_id`, `device_error_name` NOT NULL.
- `_product_items`: `wr_import_result_id`, `wr_import_result_product_id`, `wr_assign_task_product_item_id` NOT NULL; `is_completed` **int nullable** (các bảng khác tinyint NOT NULL default 0).
- `_product_services`: `wr_import_result_id`, `wr_import_result_product_id`, `wr_assign_task_product_service_id` NOT NULL.
- `_products`: `wr_import_result_id`, `product_name`, `product_code`, `product_id`, `type` NOT NULL; `rate_effort` double(8,2) default 0; `qty`/`delivery_qty`/`worker_qty` double(18,4) nullable; `serials` text (JSON); `is_serial` default 0; `serial_old` varchar(225).
- `_services`: `wr_import_result_id`, `service_name`, `type` NOT NULL.
- `_works`: `wr_import_result_id`, `work_name` NOT NULL.
- `_extend_*`: hầu hết nullable; `qty` NOT NULL default 0.

### 5.4 Dữ liệu đáng chú ý
- 4 phiếu status 1 + 2 phiếu status 5: id 83, 103, 358, 1759, 2088, 3426 (2025-08 → 2026-01).
- PNKQ status 2 có sẵn phiếu duyệt con: 1 phiếu (id 891 → PGV con 2341 status 3) — dữ liệu lệch.
- PNKQ status 3 ↔ PGV con status 2 (3 621) / 1 (3 040).
- Mồ côi do Xóa (mục 3.1): galleries 7 + 7, product_items 1, product_services 3.
- Bảng `notifications` gop_db là schema Laravel (`notifiable_type/id`, `data` JSON); ERP ghi qua adapter `App\Model\Common\Notification` (notifiable `App\Employee`).

### 5.5 Entity HRM đã có cho các bảng này
Chỉ `Modules/Assign/Entities/TpWrImportResult.php` (`$table = 'wr_import_results'`, fillable thiếu `note`, `delivery_place`, `firm_contract_*`, `company_id`…; có `STATUSES` chép ERP, `canEditBy($erpEmployeeId)`). **Không có Entity cho bất kỳ bảng `wr_import_result_*` nào.** Các chỗ khác chỉ tham chiếu tên bảng: `CustomerCare/Entities/Cost/Cost.php:129-131` (chặn xoá dịch vụ đang dùng), `MasterData/Services/Product/ProductUsageGuard.php:119`, `Assign/Services/CustomerManagerService.php:46-47` (serial đang dùng), `CustomerCare/Services/WrAssignTaskService.php:493` (DB::table lấy `MIN(id)` PNKQ theo PGV).

---

## 6. Lỗi / bất thường ERP (chỉ ghi, không sửa — user chốt làm y hệt ERP)

1. `type=wait_approve_result` (hoặc `type` lạ) khi **không** có quyền `Duyệt phiếu nhập kết quả` → không bó phạm vi, thấy mọi PNKQ của mọi công ty kể cả phiếu "Đang tạo" của người khác (M:277). ⚠ lỗ hổng xem chéo — xem mục 8.
2. Ô lọc Công ty/Phòng ban/Bộ phận (DATATABLE `search_by_info`) gửi `company/department/part` nhưng `searchByFilter` không đọc → ô lọc chết.
3. Sort cột Số phiếu giao việc / Số hợp đồng / Số phiếu Y/C khai `orderable` nhưng `data` không phải cột DB (`assign_task_code`, `wr_contract_code`, `request_code`) → sort lỗi/không tác dụng (cần thử trên ERP để biết là lỗi SQL hay bị bỏ qua).
4. Route `WrImportResults.all` trỏ hàm `all()` không tồn tại.
5. Xóa: không đạt `canEdit` hoặc lỗi → redirect im lặng, không báo; thành công không toast; về `index` thay vì `?type=all`.
6. Xóa không xoá `_product_items`, `_product_services`, `_extend_products(+services,+items)`, `_galleries_*`, revenue_costs (`_costs` type 2), `_other_services` → mồ côi (DB đã có).
7. Xóa: ATP extend không reset `can_request_qty`/`delivery_qty`; không reset ATP.`status` (phiếu đã Không duyệt giữ ATP.status = 2); merchandise không xử lý; BH không tính lại `is_assign` (reject thì có).
8. Xóa/Không duyệt khớp ATP bằng `product_id` + `first()` → PGV có 2 dòng cùng SP (khác serial/lỗi) chỉ cập nhật 1 ATP.
9. Xóa nhánh GVK và Không duyệt nhánh BH không guard null ATP → lỗi; ở Không duyệt `catch (Exception)` sai namespace → không bắt được (500, transaction không rollback chủ động).
10. Không duyệt không đổi trạng thái PGV (giữ 2 "Đã nhập kết quả") — có thể là chủ ý (PGV chờ nhập lại), ghi nhận.
11. Không duyệt ở màn này không gọi cầu nối HRM `notify-result` (#9816) → app không nhận thông báo; chỉ có ở `WrApproveResultsController::unApprove`.
12. Popup Không duyệt ở danh sách không chặn lý do toàn khoảng trắng (show thì chặn); BE chỉ `required` (Laravel `TrimStrings` có thể biến "   " thành null → bị chặn ở BE).
13. Show dùng `getForEdit` (nặng, gọi `getListProductOfCustomer`), `getForShow` là code thừa; `ini_set max_execution_time 300 / memory 512M`.
14. Show `product_repairs`/`product_warrantys`: `delivery_qty` bị ghi đè = `qty` (C:1426, :1531); items `is_completed` gán vào biến tạm (`$item[...]`) không vào mảng → không đổi kiểu (C:1432); `($cur->rate_effort || 0)` trả boolean → `rate_effort` sản phẩm bảo dưỡng = **số dịch vụ có qty**, không phải tổng định mức (C:1485); `$wr_product->type` không guard null ở BH (C:1559).
15. form_show: "Ghi chú" (tab Thông tin KH) sửa được ở màn Xem nhưng không lưu; ô "Ghi chú duyệt" sửa được nhưng không nối với nút Không duyệt; card "DANH SÁCH DỊCH VỤ TRẢ TIỀN" điều kiện tiêu đề ngược điều kiện card → không có tiêu đề, tiêu đề B viết "DANH SÁCH VỤ TRẢ TIỀN"; colspan/ô trống lệch so với form.
16. deleteFile: `unlink(public_path())` cho file S3 → không xoá file thật; `array_diff` giữ key.
17. Status 4 "Chờ BKS duyệt kết quả" không có phiếu nào; `canView` cho phép người duyệt xem nhưng danh sách `type=all` không liệt kê phiếu cho họ (chỉ qua `wait_approve_result`).
18. Cột "Người tạo" chỉ tên (PGV HRM dùng `tên - SĐT`) — quy ước HRM cần chốt.

---

## 7. Code HRM hiện có liên quan (chỗ cần nối)

### 7.1 hrm-api
- `Modules/Assign/Entities/TpWrImportResult.php` — model cũ cho app mobile (`STATUSES`, `canEditBy`, accessor `word_stand`).
- `Modules/Assign/Services/TpWrImportResultService.php` (608 dòng): `searchByFilter` (:37-134, đọc DB chung, lọc `code` = số **PGV**, `import_code` = số PNKQ, `approved_by` lọc cột `wr_import_results.approved_by` **không tồn tại** → lỗi SQL nếu app gửi), `show` (:137, proxy `ERP_URL/hrm/wr_import_results/{id}/apiShow`), `store` (:207 → ERP `/hrm/wr_import_results` = `storeApp`), `update` (:364 → ERP `/hrm/wr_import_results/{id}`), upload ảnh (:525, :567 → ERP).
- `Modules/Assign/Http/Controllers/Api/V1/WrImportResultController.php` + routes `Modules/Assign/Routes/api.php:1282-1290` (`/v1/assign/wr_import_results`: index, show, store, uploadConstructionImg, uploadHandoveImg, update, `notify-result`).
- `Modules/Assign/Transformers/WrAssignTaskResource/WrAssignTaskListResource.php:29-66` — `wr_import_result_id` (latest) cho app.
- `Modules/CustomerCare/Services/WrAssignTaskService.php:376-393` (`actionFlags`: `is_can_view_import_result` khi PGV status ∉ {1,9}, `import_result_id` = MIN(id) hoặc 0) và :493-498.
- Seeder quyền: `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php:368-374` — quyền PGV type 24 (khuôn để thêm quyền PNKQ).

### 7.2 hrm-client (đang link sang ERP)
- `pages/customer-care/wr-assign-tasks/components/wrAssignTaskLinks.js:27-47` — `ERP_ASSIGN_PATHS.importResultCreate` (`/admin/customer-care/wr_import_results/create`), `importResultShow(id)` (`…/{id}/show`, id 0 khi chưa có), `approveResultShow`.
- `pages/customer-care/wr-assign-tasks/index.vue:580-607` — hành động dòng "Nhập kết quả" (`openErpOrWarn('/admin/customer-care/wr_import_results/create', {wr_assign_task_id})`) và "Xem phiếu nhập kết quả" (`…/${item.import_result_id || 0}/show`).
- `pages/customer-care/wr-assign-tasks/components/WrAssignTaskForm.vue:243-262` — nút "Nhập kết quả" (`openImportResult`) / "Xem phiếu nhập kết quả" (`importResultShowUrl(form.import_result_id)`) ở màn chi tiết PGV.
- Menu: `components/subsystem-menu/customer-care.js:111-125` nhóm "Giao việc" hiện có 3 mục (Phiếu chờ giao việc · Phiếu giao việc · Phiếu giao việc được giao) — **chưa có "Phiếu nhập kết quả"**. `components/assign-components/assign-slidebar.vue:199,209` có "Phiếu nhập kết quả giao việc"/"Phiếu duyệt kết quả giao việc" — là màn **Giao việc nội bộ** (`pages/assign/assign_job_import_result`), KHÁC màn này, đừng nhầm.
- App/thông báo: url `/assign/assign_import_result/{id}` (notify-result) là màn PNKQ **công tác** của HRM — không phải PNKQ CSKH; khi port xong có thể cần đổi url thông báo sang màn mới (chốt).

### 7.3 Menu ERP
`resources/views/layouts/topmenubar.blade.php:1909` — CSKH › Kiểm tra bảo hành sửa chữa › nhóm **Giao việc** › "**Phiếu nhập kết quả**" → `WrImportResults.index?type=all` (ngay sau "Phiếu giao việc được giao", trước "Phiếu duyệt kết quả"). Chỉ 1 vị trí menu; lối vào phụ `?type=wait_approve_result` từ dashboard (HomeController:1892) và redirect sau khi tạo/sửa phiếu duyệt (wr_approve_results/create.blade.php:224, edit.blade.php:218). Menu không gate quyền.

---

## 8. Điểm cần user chốt

1. **Lỗ xem chéo `wait_approve_result` không quyền** (mục 6.1): "y hệt ERP" nghĩa là để nguyên lỗ? Đề xuất: HRM chỉ nhận `type ∈ {all, index, wait_approve_result}`, nhánh `wait_approve_result` không quyền → rỗng (`1=0`). Cần chốt vì đụng nguyên tắc fail-closed của CLAUDE.md.
2. **Lối vào `?type=wait_approve_result`**: có khai mục menu "Chờ duyệt phiếu nhập kết quả" ở HRM không (ERP chỉ có trên dashboard)? Và đích redirect sau khi duyệt ở ERP vẫn trỏ ERP.
3. **Ô lọc Công ty/Phòng ban/Bộ phận** (ERP hiện nhưng chết): bỏ (y ERP về kết quả) hay làm cho chạy theo chuẩn HRM `meta.is_all_company`?
4. **Sort** 3 cột Số PGV/Số HĐ/Số phiếu Y/C: ERP khai sort nhưng hỏng — HRM cho sort (theo `wr_assign_task_code`…) hay tắt?
5. **In danh sách**: ERP không có In/Xuất. HRM bộ bắt buộc có Xuất Excel + Cấu hình cột + Lịch sử; có thêm In như PGV không?
6. **Xóa**: giữ y ERP các lỗi (không xoá bảng con extend/galleries/revenue_costs/product_items/services, không reset ATP.status, redirect im lặng) hay xoá đủ bảng con? HRM chắc chắn cần toast "Xóa thành công." + 409 khi trạng thái đã đổi (khuôn PGV) — xác nhận.
7. **Không duyệt — thông báo**: dùng NotificationMeta HRM (tái dùng logic `notify-result`, gửi chuông + push app) thay cho câu ERP "{tên} vừa không duyệt phiếu nhập kết quả của bạn!"? Deep-link về màn chi tiết PNKQ mới (`/customer-care/wr-import-results/{id}`) hay giữ `/assign/assign_import_result/{id}` app đang mở?
8. **Không duyệt nhánh BH/GVK không guard null + catch sai** — HRM có guard (không đổi nghiệp vụ, chỉ không nổ 500)?
9. **Cột "Người tạo"/"Người duyệt"**: chỉ tên như ERP hay `tên - SĐT` như PGV HRM? Bổ sung cột chuẩn HRM nào (Ngày tạo đã có)?
10. **Chi tiết**: ô "Ghi chú" và "Ghi chú duyệt" sửa được nhưng không lưu ở ERP — HRM khoá (readonly) như PGV đã làm?
11. **Lỗi hiển thị show** (`rate_effort` bảo dưỡng = số dịch vụ do `|| 0`, `delivery_qty = qty`, tiêu đề khối dịch vụ trả tiền mất): giữ y ERP (con số sai) hay hiển thị đúng?
12. **Sửa** (canEdit: người tạo + status 1/6) có port trong đợt này không (phần form B), hay nút Sửa link ERP tab mới?
13. **Quyền HRM mới**: 4 quyền tên nguyên văn ERP (`Xem phiếu nhập kết quả theo tổng công ty/công ty/phòng ban`, `Duyệt phiếu nhập kết quả`) `type` 24, group "Phiếu nhập kết quả" — xác nhận. `Duyệt phiếu nhập kết quả` gate cả nút Không duyệt (+ middleware `checkPermission` cho route reject).
14. **Mục menu HRM**: thêm "Phiếu nhập kết quả" → `/customer-care/wr-import-results?type=all` vào nhóm Giao việc (`customer-care.js`) sau "Phiếu giao việc được giao"; đồng thời đổi link "Xem phiếu nhập kết quả" ở PGV (index.vue:607, WrAssignTaskForm.vue:251, wrAssignTaskLinks.js:31) sang HRM — xác nhận (khi id = 0 thì HRM 404 như ERP?).
