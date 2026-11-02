# Khảo sát B — Phiếu nhập kết quả: FORM TẠO / SỬA + LUỒNG LƯU (ERP → HRM) — @khoipv

Ngày 02/11/2026 · chỉ đọc, chưa sửa code. Nguồn ERP `D:\laragon\www\erp` (viết tắt: **C** = `app/Http/Controllers/Customercare/WrImportResultsController.php`, **M** = `app/Model/Customers/WrImportResult.php`, **R** = `app/Http/Requests/WrImportResultRequest.php`, **T** = `app/Http/Traits/SerialValidationTrait.php`, **AT** = `app/Model/Customers/WrAssignTask.php`, **V** = `resources/views/customercare/warranty_repair_import_results/`).
Đã đối chiếu DB chung bằng tinker (chỉ SELECT) — mục 6.

---

## 0. Tóm tắt nhanh

- Form **1 màn dùng chung cho Tạo và Sửa** (`V/form.blade.php`, 1906 dòng), các khối hiện theo **id chứng từ nguồn của phiếu giao việc** (`wr_service_contract_id` / `assembly_request_id` / `assign_other_request_id`), **không theo cột `type`**. Type 1 HĐ / 2 BH / 3 PL đều đi nhánh `wr_service_contract_id` (BH khác HĐ/PL ở chỗ có `product_warrantys` thay cho `product_repairs`/`extend_products`).
- 2 nút submit: **"Lưu"** → `status = 1` (Đang tạo) · **"Lưu & Gửi duyệt"** → `status = 2` (Chờ duyệt kết quả). + "Quay lại".
- Sửa được khi `created_by = mình` **và** `status ∈ {1 Đang tạo, 6 Không duyệt}` (`M:350 canEdit`). ERP **chỉ chặn ở GET edit**, POST update không kiểm.
- Lưu = 1 transaction: insert/fill `wr_import_results` → xoá-ghi ~14 bảng con → cập nhật `wr_assign_tasks.status` (7 / 2) → thông báo quyền **"Duyệt phiếu nhập kết quả"** (khi status 2) → cập nhật `assign_task_progress` + bảng con progress + `assign_task_serial_progress` (lắp đặt) → `wr_service_contracts.is_assign` (BH).
- **Không** đụng bảng `serials` ở bước nhập (syncSerial chỉ gọi ở bước DUYỆT — `WrApproveResultsController:380,1132`).
- Ảnh thi công / bàn giao upload **local disk ERP** `public/uploads/wrImportResult/{construction|handove}/`, lưu **path tương đối** `/uploads/...` vào `wr_import_result_galleries_constructions|handovers.url`.
- Quyền "Duyệt phiếu nhập kết quả" và "Nhập kết quả thực hiện" **chưa có trong bảng `permissions` (guard api) của HRM** → cần chốt.

---

## 1. Cấu trúc form (create + edit)

Vỏ: `V/create.blade.php` (controller `WarrantyRepairInformationRequest`, `new WrImportResult({}, {mode:'create'})` rồi gán `form.wr_assign_task = <getForDataImportResult>`, `form.wr_assign_task_timesheet = wr_assign_task.timesheets`) · `V/edit.blade.php` (`new WrImportResult(<getForEdit>, {mode:'edit'})`, timesheets lấy từ `WrAssignTask::getForShow`). Tiêu đề trang: "Phiếu nhập kết quả" (tạo) / "Phiếu nhập kết quả {code}" (sửa).
Khoá ô: mọi input `ng-disabled="show"` — ở create/edit `show = false` → **sửa được hết**, trừ các ô ghi rõ dưới đây.

### 1.0 Thanh tab đầu (form.blade.php:41-62)
3 tab: **"Thông tin khách hàng"** · **"Chấm công"** · **"File ảnh đính kèm (*)"** (tab tô đỏ + icon `fa-exclamation-circle` khi có lỗi `galleries_construction`/`galleries_handover`). Góc phải: `<người tạo> - <ngày tạo dd/mm/yyyy>` (BaseClass.creator/created_time; tạo mới = user hiện tại + hôm nay).

### 1.1 Tab "Thông tin khách hàng" (form:63-288; khối 147-286 comment chết = file đính kèm cũ)
| Nhãn (nguyên văn) | Hiện khi | Nguồn | Sửa? |
|---|---|---|---|
| Phiếu giao việc (*) | luôn | `wr_assign_task_code`, link `/admin/customer-care/wr_assign_tasks/{id}/show` | khoá (link) |
| Phiếu YCGV khác (*) | `assign_other_request_id` | `assign_other_request_code` → link `assign_other_requests/{id}/show` | khoá |
| Hợp đồng (*) | `assembly_request_id` | `firm_contract_code` (create: `assembly_request.firm_contract_*`, C:181-182) → link `/admin/sale/firm-contracts/{id}` | khoá |
| Khách hàng (*) | luôn | `customer_code - customer_name` | disabled |
| Địa chỉ lắp đặt | assembly hoặc wr_service | `wr_assign_task.delivery_place` | disabled |
| Người liên hệ (*) | 3 nguồn | `customer_contact_name` | disabled |
| SĐT liên hệ | 3 nguồn | `customer_contact_phones` | disabled |
| Người yêu cầu | 3 nguồn | `creator_request` = fullname người tạo chứng từ nguồn (C:184-200) | disabled |
| SĐT Người yêu cầu | 3 nguồn | `phone_creator` = telephone người tạo chứng từ nguồn | disabled |
| Ghi chú | 3 nguồn | `note` (rỗng) | **sửa được** (textarea) |
Ghi chú: Chỉ nhánh wr_service_contract **không** được C:create gán `firm_contract_*`; người yêu cầu lấy từ `wr_service_contract.employee_create`.

### 1.2 Tab "Chấm công" (form:289-338)
Bảng 2 tầng: STT · Ngày làm việc (`day` dd/MM/yyyy) · nhóm **"Chấm công theo HRM"** (Checkin, Checkout, Giờ làm việc = `checkin`,`checkout`,`time`, chỉ đọc) · nhóm **"Điều chỉnh theo thực tế"** (Checkin `checkin_actual`, Checkout `checkout_actual` — ô giờ `hourPicker`, **khoá khi đã có checkin/checkout HRM**; Giờ làm việc `time_actual` = `calculateHourDifference` (`formJS.blade.php:5-31`: chênh giờ, qua nửa đêm +24h, `toFixed(1)`)).
Nguồn `wr_assign_task.timesheets` (bảng `wr_assign_task_timesheets`). **DB hiện có 0 dòng** → tab luôn trống. Lưu: `syncTimesheet` (M:1176) `findOrFail(id)` rồi ghi 3 cột actual. Rule required timesheet đã comment (R:48-50).

### 1.3 Tab "File ảnh đính kèm (*)" (form:339-397, JS `formJS.blade.php:38-100`)
2 ô dropzone: **"Ảnh công trình"** (`galleries_construction`) · **"Ảnh biên bản bàn giao"** (`galleries_handover`); nhãn kèm chữ đỏ "(Định dạng file: png, jpg, jpeg, pdf, doc, docx, xls, xlsx. Dung lượng tối đa: 5MB)"; placeholder "Chọn ảnh hoặc file để upload".
- Dropzone: `uploadMultiple`, `parallelUploads 5`, `maxFilesize 5` (MB), `acceptedFiles .jpeg,.jpg,.png,.pdf,.doc,.docx,.xls,.xlsx`, `dictFileTooBig 'Image is bigger than 5MB'`. Upload ngay khi chọn (autoProcessQueue) tới route `uploadConstructionImg` / `uploadHandoveImg` (`routes/web.php:5948-5949`, `Common\UploadController:58-170`): validate `file required` ("Không được để trống"), lưu **local** `base_path()/public/uploads/wrImportResult/construction/` (handover: `.../handove/`), tên `time() . slug(tên gốc) . ext`; ảnh còn sinh thêm `-large` (800×800) và `-thumbnail` (75×75). Trả `data = ['/uploads/wrImportResult/construction/<file>']`; FE chỉ lấy **phần tử cuối** (`res.data.pop()`) push vào mảng (upload nhiều file 1 lượt sẽ mất bớt — lỗi ERP).
- Hiển thị: ảnh → thumbnail 100×100 + fancybox; file khác → icon theo đuôi + tên; nút × `deleteImg(img)` = **chỉ xoá khỏi mảng FE** (cả 2 mảng), không gọi server, không xoá file vật lý. Kéo thả sắp xếp (`ui-sortable`).
- Lưu: gửi mảng URL; `syncGalleriesConstruction/Handover` (M:1187-1209) **chỉ chạy khi mảng khác rỗng** → xoá hết rồi `insert` (`wr_import_result_id`, `url`; **không set created_at**).
- Edit: C:1857-1874 đổi relation thành mảng URL.
- `deleteFile` (C:3318) **không liên quan ảnh** — xoá file trong cột JSON `attachments` (chức năng đính kèm cũ đã comment ở FE; DB `attachments` toàn NULL).

### 1.4 Card "A - TÍNH CÔNG BẢO HÀNH SỬA CHỮA" (form:402-929) — hiện khi `wr_service_contract_id` (type 1/2/3)
**I - Bảo hành** (form:407-600, hiện khi `product_warrantys.length > 0`, thực tế type 2)
Cột: STT · Nội dung công việc · ĐVT · **Kết quả** [Đã hoàn thành (checkbox chọn hết `changeAllProductWarrantyCompleted`) | Hoàn thành (%)] · SL Bàn giao · Serial · ĐM công · CK đề xuất duyệt · CK được tính dự kiến · Ghi chú.
Mỗi thiết bị `p`:
- Dòng tiêu đề: `{product_name} - Model: {model_name} - Mã hàng: {product_code}` / "Thiết bị: {type_text}" (tp Tân Phát · tpc Tân Phát CC · ncck/new Nhà cung cấp khác) / "Lỗi thiết bị: {device_error_name}".
- **{n}.1 "Công tháo lắp sửa chữa thiết bị"**: checkbox `p.is_completed` · `% finish_percent` (khoá khi đã tick; tick ⇒ 100; nhập ≥100 bị **bỏ qua im lặng**, chỉ nhận <100 — `WrImportResultProduct.blade.php:162-181`) · SL bàn giao = `p.qty` (chỉ đọc) · **Serial** input `p.serial` (sửa được; `ng-change changeSerial` đồng bộ serial sang dòng dịch vụ trả tiền cùng `serial_old`; tooltip "Serial từ hợp đồng: {serial_old}") · ĐM công = `rate_effort` · CK đề xuất duyệt = `rate_effort_approve` · CK được tính dự kiến = `rate_effort_approve × benefit_rate` · Ghi chú `p.note`.
- Mode create: `serial` mặc định **rỗng** nếu không có `serial_id` (`after()` dòng 9-21); có `serial_id` thì giữ serial cũ.
- **{n}.2 "Danh sách dịch vụ"**: mỗi dịch vụ (đã tách 1 dòng / 1 đơn vị, `qty = 1`): `cost_name` · checkbox · % · SL (`service.qty`, đọc) · Ghi chú.
- **{n}.3 "Danh sách vật tư"**: `product_name` · `unit_name` · SL `product_item.qty` (sửa được, setter chặn trần `available_qty`) · Ghi chú. (BH: vật tư không có checkbox/%.)
- Dòng tổng: "Tổng công được tính" = Σ `rate_effort_approve` | Σ `rate_effort_approve × benefit_rate`.

**I - Dịch vụ sửa chữa** (form:607-779, hiện khi `product_repairs` hoặc `extend_products` có dòng — type 1/3)
Giống BH, khác: vật tư {n}.3 **có** checkbox + % (`pr_completed_item…`, form:741-750); checkbox chọn hết `changeAllProductRepairCompleted` tick cả dịch vụ + vật tư. Tổng như trên.
**II. Danh mục thiết bị cần bảo dưỡng** (form:780-928)
Cột: STT · Loại dịch vụ · ĐVT · Kết quả [Đã hoàn thành (chọn hết `changeAllProductExtendCompleted`) | Hoàn thành] · SL Bàn giao · Serial · ĐM công · CK đề xuất duyệt · CK được tính dự kiến · Ghi chú.
- Dòng thiết bị: `{product_name} - {model_name} - {product_code}` / Thiết bị: type_text · Serial input `product.serial` (sửa được, không có changeSerial).
- Dòng dịch vụ `{service_name} ({level_name})` · ĐVT cứng "Gói" · checkbox · % (khoá khi tick, nhận ≤100 làm tròn 2) · SL `service.qty` · ĐM công = `service.qty ? rate_effort : '-'` · CK đề xuất = `rate_effort × finish_percent / 100` · CK được tính = `approve × benefit_coefficient` · Ghi chú.
  Mặc định (`WrImportResultExtendProductService.blade.php` after): `rate_effort = service_level.quota_work || 1`, `benefit_coefficient = service_level.benefit_coefficient || 1` (theo `\App\Model\Sale\Service::getRateEffort()` = toàn bảng `service_levels`), `qty = available_qty` nếu rỗng.
- Dòng vật tư con: tên / Model / Mã hàng · ĐVT · checkbox · (ô % đã comment) · SL `product.qty` (sửa được, chặn ≤ available_qty) · Ghi chú.
- Tổng "Tổng công định mức (II)" = Σ rate_effort (dịch vụ qty≠0) | Σ approve | Σ result.

### 1.5 Card "A - Hạng mục lắp đặt, bàn giao" (form:929-1035) — hiện khi `assembly_request_id` (type 4)
**I - Lắp đặt, bàn giao**. Cột: STT · Hàng hoá (`product_name` + "Mã hàng:") · Model · ĐVT · Kết quả [Đã hoàn thành (chọn hết `changeAllAssemblyCompleted`) | % Hoàn thành] · SL bàn giao · Serial · SL tính công khoán · ĐM công · CK đề xuất duyệt (theo phiếu nhập kết quả) · CK được tính dự kiến · Ghi chú.
- Dữ liệu (`WrImportResult.blade.php:463-501 calculateProductAssembly`): từ `wr_assign_task.assembly` (đã lọc qty>0). Hàng **`is_serial = false` bị tách thành `qty` dòng, mỗi dòng `qty = 1`**; `is_serial = true` giữ 1 dòng. `is_serial = product.product_type ∈ configs.serial_product_types` (AT:1913-1923; DB: `tool_and_device,tool,automotive_parts,supplies,…`) — lưu ý tên biến ngược nghĩa: `is_serial = true` ⇒ chỉ 1 ô serial, **không bắt buộc**.
- Checkbox `p.is_completed` → `changeAssemblyCompleted`: tick ⇒ `delivery_qty = qty` + dựng lại số ô serial; cập nhật checkbox chọn hết.
- % (khoá khi tick). SL bàn giao `p.delivery_qty` (**sửa được**, `only-number`, setter chặn ≤ qty; mặc định 0) → `changeDeliveryQty` dựng số ô serial = delivery_qty (is_serial: luôn 1 ô).
- Serial: mỗi dòng con `d.serial` (rowspan = số serial + 1), lỗi `product_assembly.{i}.serials.{j}.serial`.
- SL tính công khoán `require_worker_qty = ceil(delivery_qty / worker_qty)` (worker_qty mặc định 1). ĐM công `rate_effort`. **CK đề xuất duyệt = min(round(rate_effort × require_worker_qty × finish_percent / 100, 2), rate_effort × require_worker_qty)** (`WrImportResultProduct.blade.php:232-236`). CK được tính = approve × benefit_rate (benefit_rate 0/rỗng ⇒ 1).
- Dòng "Tổng công được tính": Σ delivery_qty · Σ require_worker_qty · Σ approve · Σ approve×benefit.

### 1.6 Card "A - TÍNH CÔNG DỊCH VỤ ĐÍNH KÈM" (form:1036-1087) — hiện khi `assign_other_request_id` (type 5)
**I - Dịch vụ đính kèm**: STT · Dịch vụ đi kèm (`cost_name`) · ĐM công (`rate_effort`, đọc) · Công khoán đề xuất duyệt (input `rate_effort_approve`, mặc định = rate_effort, FE chặn trần ≤ rate_effort — `WrImportResultCost.blade.php`). Cột checkbox hoàn thành đã comment → `is_completed` luôn 0. Tổng "Tổng công được tính" = Σ rate_effort | Σ approve. Nguồn `wr_assign_task.revenue_costs`, lưu vào `wr_import_result_costs` **type 2**.

### 1.7 Card "B - Công phụ tính P3" (form:1088-1240) — luôn hiện
**I - Công việc phụ tính P3**: STT · "Công phụ tính P3" + nút **(+)** `addWorkP3()` · Đã hoàn thành (chọn hết) · ĐM công · Công khoán đề xuất duyệt · Ghi chú.
- Dòng từ phiếu giao việc (`work_p3`, create): tên/ĐM công/CK đề xuất **chỉ đọc**, checkbox `is_completed` mặc định **false** ⇒ CK đề xuất = 0; tick ⇒ CK đề xuất = ĐM công (`syncRateEffortApprove(force)`).
- Dòng thêm mới (`w.new`, không có work_name): tên (input, có nút × xoá đúng index), ĐM công (input), CK đề xuất (input, chặn ≤ ĐM công), **mặc định is_completed = true**. Edit: dòng có `work_name` không nằm trong `work_p3` của phiếu giao việc được gắn `new = true` (C:1844-1849).
- Tổng "Tổng công phụ được tính" = Σ rate_effort / Σ approve **chỉ dòng đã tick**.
**II - Tổng công định mức** (form:1209-1240): 1 "Công khoán chính" = `rate_effort_main` · 2 "Công khoán phụ" = Σ approve P3 · "Tổng công định mức (ngày)" = chính + phụ.
`rate_effort_main` (`WrImportResult.blade.php:780-794`): wr_service → nếu có repairs/extend: Σapprove SC + Σapprove BD (**bỏ qua BH**), ngược lại Σapprove BH · assembly → Σapprove lắp đặt · còn lại → Σapprove dịch vụ đính kèm. (Chỉ hiển thị, **không gửi BE**.)
"VI - Nhân sự tham gia" (form:1241-1270) **đã comment** — nhưng `executors` vẫn gửi & lưu (copy từ `wr_assign_task.executors`: employee_id/code/name/rate_effort).

### 1.8 Card "B - DANH SÁCH GIAO NHẬN VẬT TƯ" (form:1273-1462) — hiện khi `!wr_service_contract_id && (item_warrantys|item_repairs|item_extends)`
I - Cho bảo hành / II - Cho sửa chữa - Bảo dưỡng / III - Hàng bán thêm: STT · Tên vật tư · Model · Mã hàng · ĐVT · Số lượng lấy (`qty`) · Số lượng giao cho khách (input `delivery_qty`).
⚠️ Vật tư chỉ sinh từ phiếu có HĐ dịch vụ (`calculateItemWarrantys/Repairs` gom `items` theo product_id; repairs gom cả vật tư của dịch vụ bảo dưỡng) ⇒ **card này thực tế không bao giờ hiện**, nhưng dữ liệu vẫn gửi và lưu (`wr_import_result_items` type 2 = 1442 dòng).
### 1.9 Card "C - DANH SÁCH VẬT TƯ BÁN THÊM" (form:1463-1505) — hiện khi `wr_service_contract_id && item_extends`
I - Hàng bán thêm: STT · Tên vật tư (tên + Mã hàng + Model) · ĐVT · Số lượng HĐ (`available_qty`) · Số lượng Giao (input `delivery_qty`, mặc định = qty, chặn ≤ available_qty). Nguồn `wr_assign_task.merchandises`.
### 1.10 Card "DANH SÁCH DỊCH VỤ TRẢ TIỀN" (form:1506-1636) — hiện khi `!wr_service_contract_id && (service_warrantys|service_repairs)`
Tiêu đề h4 lại đòi `wr_service_contract_id` ("C - DANH SÁCH DỊCH VỤ TRẢ TIỀN" / "B - DANH SÁCH VỤ TRẢ TIỀN" — sai chính tả nguyên văn) ⇒ mâu thuẫn, **card không bao giờ hiện**. Cột: STT · Tên dịch vụ · Serial thiết bị · Giá làm thực tế (input `price`) · File đính kèm (input file → upload S3 `CmcS3Helper::putFile(..,'wr_import_result_service')` trong `syncService` M:1089). Vẫn gửi & lưu (`wr_import_result_services` 3514 dòng, price 0, attachment NULL).
### 1.11 "III - Các chi phí liên quan" (1 - Chi phí vận chuyển `cost_id = 5` / 2 - Chi phí khác) (form:1638-1773) — **đã comment**. `costs` vẫn gửi & lưu (`wr_import_result_costs` type 1, copy `wr_assign_task.costs` chỉ cost_id/cost_name, price 0) — mỗi phiếu ~5 dòng.
### 1.12 "Ghi chú duyệt" (form:1776-1815)
Ở form Tạo/Sửa luôn rơi vào nhánh `@else` (canApproveResult cần status 2, canEdit cần 1/6): hiện card **chỉ đọc** `approve_comment` nếu có (phiếu "Không duyệt" → lý do không duyệt do `reject()` ghi vào `approve_comment`, C:2783-2785). `approve_comment` vẫn có trong submit_data nhưng `store/update` không fill (không nằm trong `only`).
### 1.13 Popup
- **"Chọn serial cần ngưng"** (`#chooseSerialChange`, form:1848-1875): select "Chọn serial" từ `form.product_current.serials` → `needChangeSerial` gán `serial_id` cho dòng sửa chữa cùng khoá; lưu ý đỏ "Lưu ý: Nếu không chọn serial nào thì mặc định sẽ ngưng serial trên hợp đồng". **Popup chết**: không có code nào mở modal / gán `product_current` (`chooseSerial()` rỗng — `WrImportResultProduct.blade.php:188-190`).
- **"Cảnh báo !"** (`#checkProductExportError`, form:1877-1902): liệt kê `data_errors` (HTML, `trustAsHtml`), nút "Đóng". Mở khi BE trả `type = 'check_product_export'`.

---

## 2. Nút submit, xác nhận, điều kiện Sửa

| Nút (form:1819-1845) | status gửi | Ghi chú |
|---|---|---|
| **Lưu** (`btn-success`, icon `fa-save`) | 1 Đang tạo | |
| **Lưu & Gửi duyệt** (`btn-success`) | 2 Chờ duyệt kết quả | Nếu không có mục nào hoàn thành (`is_completed` của repairs/warrantys/assembly/revenue_costs + extend service) → swal "Xác nhận!" / "Phiếu không hoàn thành công việc, bạn có đồng ý không?" [Xác nhận / Hủy] (`create.blade.php:107`) |
| Quay lại (`btn-danger`) | — | `WrImportResults.index?type=all` |
| (Không duyệt / Duyệt kết quả) | — | chỉ ở màn Xem (`show`), ngoài phạm vi |

`submitData(status)` (`create.blade.php:55-195`): `data = form.submit_data` + `status`; **JSON.stringify** 3 mảng `product_assembly`, `product_repairs`, `product_warrantys` (BE `prepareForValidation` decode lại, R:31-40), còn lại `jsonToFormData` (multipart) + file dịch vụ/chi phí. POST `WrImportResults.store` (`POST /admin/customer-care/wr_import_results`) hoặc `WrImportResults.update` (`POST {id}/update`).
Phản hồi: success → toast **"Tạo phiếu nhập kết quả thành công!"** / **"Chỉnh sửa phiếu nhập kết quả thành công!"** + chuyển `index?type=all` · `type check_product_export` → popup Cảnh báo · `type check_serial` → xoá serial MỚI (dòng không có `serial_id`, cả `serials[]`) của BH/SC/BD + toast warning `message` · khác → `errors` inline + toast `message` · lỗi HTTP → "Đã có lỗi xảy ra". (Nhánh swal xác nhận **không xử lý** `check_product_export`.)

**Điều kiện Sửa**: `canEdit()` (M:350) = `created_by == user.id && status ∈ {1, 6}`; menu danh sách hiện "Sửa"/"Xóa" theo đúng điều kiện này (C:154-157). GET edit: không đạt → view `not_found` (C:1850). **POST update không kiểm canEdit**, không kiểm PCT.
**Điều kiện Tạo**: GET create **không kiểm gì**; POST store chặn (C:216-224): đã có phiếu → "Phiếu giao việc này đã có phiếu nhập kết quả, không thể tạo thêm. Vui lòng mở phiếu kết quả đã có để chỉnh sửa." · `has_assign_business != 1` → "Chỉ được nhập kết quả khi phiếu công tác (PCT) đã được duyệt". Lối vào là nút "Nhập kết quả" ở phiếu giao việc (`canImportResult` AT:391 — HRM đã port).
Route web không gắn middleware quyền (routes/web.php:6158-6171).

---

## 3. Validate

### 3.1 FormRequest `R` (lỗi chung `message = "Thao tác thất bại"`, `errors` theo key — `BaseRequest::failedValidation`)
| Key | Rule | Câu lỗi |
|---|---|---|
| `wr_assign_task_id` | required\|exists:wr_assign_tasks,id | mặc định Laravel |
| `customer_id`, `status` | required | mặc định |
| `product_warrantys.*.serial`, `product_repairs.*.serial`, `extend_products.*.serial` | `required_if:…is_completed,1\|not_in:0` | not_in: **"Không ghi nhận số 0"** (required_if dùng câu mặc định) |
| `works.*.work_name`, `works.*.rate_effort` | required | mặc định |
| `works.{i}.rate_effort_approve`, `revenue_costs.{i}.rate_effort_approve` | approve > rate_effort | **"Công khoán đề xuất duyệt không được lớn hơn định mức công"** |
| `product_assembly.{i}.serials` (dòng `is_completed`) | required\|array | mặc định |
| `product_assembly.{i}.serials.{j}.serial` (dòng hoàn thành) | `required` nếu `is_serial === false`, string, closure | **"Serial không được để trống"** · **"Serial \"{v}\" đã tồn tại cho sản phẩm khác"** (`serials.serial` thuộc product khác) · **"Seri đã hoàn thành nhập kết quả, không được nhập tiếp!"** (ATP lắp đặt của HĐ `firm_contract_id`, `contract_type='firm'`, **phiếu giao việc khác**, serial progress có success_percent 100) · **"Bạn cần phải nhập tối đa bằng {100 − Σ%}"** (finish_percent > % còn lại) · **"Serial \"{v}\" đang bị trùng trong danh sách"** |
| (dòng chưa hoàn thành) | nullable, closure giống trên nhưng xét ATP **cùng** phiếu giao việc, không kiểm "SP khác" | như trên |
| `galleries_construction`, `galleries_handover` | required\|array khi có dòng `finish_percent == 100` ở assembly / warranty / repair, hoặc dịch vụ BD `finish_percent == 100` | **"Ảnh công trình là bắt buộc khi có sản phẩm hoàn thành 100%"** · **"Ảnh biên bản bàn giao là bắt buộc khi có sản phẩm hoàn thành 100%"** (các message `.*.file/mimes` khai nhưng không có rule) |
| `attachments.{pw\|pr\|rc}` | nullable (vô hiệu) | — |
| `product_warrantys.{i}.serial` (dòng hoàn thành có serial) | closure: ATP BH của **HĐ khác phiếu** đã DA_DUYET | **"Seri đã hoàn thành nhập kết quả, không được nhập tiếp!"** · **"Bạn cần phải nhập tối đa bằng {x} %"** |
| `product_repairs.{i}.serial` | closure (mọi dòng) — phần fail đã comment ⇒ **không còn chặn gì** | — |
Rule chết (bị ghi đè cùng key ngay sau): BH "Số serial \"{s}\" đang bị trùng", BH/SC "\"{tên}\" cần nhập cùng serial" (R:401-424, 535-548).

### 3.2 Kiểm trong controller (trước transaction)
1. Trùng phiếu / PCT (mục 2) — chỉ store; update chỉ kiểm trùng: **"Phiếu nhập kết quả đã tồn tại"** (C:1901-1903).
2. `checkValidateSerial` (T): gom dòng BH/SC/BD **không có `serial_id`** mà (dòng tick hoàn thành hoặc có dịch vụ/vật tư tick) → khử trùng theo (product_id, code, name, no_sale_name, type, serial) → với từng thiết bị của khách (`Customer::getListProductOfCustomer`, model Sale/Customer.php:1789-2148, ~360 dòng): đếm serial mới khác rỗng, chưa có trong `serials` đang dùng; `free = qty − count(serials)` (≥0). Trả `type: 'check_serial'`, message:
   - **"Thiết bị \"{tên}\": số serial đang sử dụng đã đủ theo số lượng thiết bị. Vui lòng vào Danh mục serial thiết bị để ngừng sử dụng bớt 1 serial cũ trước khi nhập serial mới."**
   - **"Thiết bị \"{tên}\": số serial nhập thêm ({n}) vượt quá số lượng thiết bị còn có thể gắn serial ({free})."**
3. `hasProductExport` (C:3344-3452, chỉ khi có `product_assembly`): với dòng `is_completed` có `exportable_id`: phiếu YC xuất hàng (`ProductExportRequest`) chưa `DA_HACH_TOAN` → **"Phiếu yêu cầu xuất hàng '<b>{code}</b>' chưa được hạch toán"**; YC xuất bán hàng mượn (`BorrowSellRequest`) chưa có `borrow_sells` → **"Phiếu yêu cầu xuất bán hàng mượn '<b>{code}</b>' chưa được hạch toán"**. Trả `{success:false, type:'check_product_export', data:{exportable_id: message}}`.
### 3.3 JS (không chặn submit, chỉ kẹp giá trị)
`finish_percent` <100 (tick = 100) · `delivery_qty` ≤ qty · `qty` vật tư/dịch vụ BD ≤ `available_qty` · `rate_effort_approve` P3/dịch vụ đính kèm ≤ `rate_effort` · số nhập qua `parseNumberString` + `roundNumber`.

---

## 4. Luồng store / update

### 4.1 store (C:210-794) — `DB::beginTransaction` sau các kiểm 3.2
1. `new WrImportResult` fill `wr_assign_task_id, wr_assign_task_code, customer_id, customer_name, customer_code, sw_note, sr_note, status, note, delivery_place, customer_contact_name, customer_contact_phones, firm_contract_id, firm_contract_code, creator_request, phone_creator` → save (BaseModel gắn `created_by/updated_by`). `sw_note` **không trong $fillable** ⇒ không lưu.
   Event `created` (M:83-99): ghi `company_id`, `department_id` theo **người đăng nhập** (save lần 2).
2. `generateCode()` (M:188): `{company.code}.PNKQ.{YYYY}{id đệm 6}` (vd `TPE.PNKQ.2026007047`) — company **của người đăng nhập** (save lần 3). DB unique `code` + unique `wr_assign_task_id`.
3. Bảng con (thứ tự):
   | Gọi | Bảng | Cách ghi |
   |---|---|---|
   | `syncProductWarranty(…,1)` M:515 | `wr_import_result_products` type 1 + `wr_import_result_product_items` + `wr_import_result_product_services` + `wr_import_result_product_device_errors`; **cập nhật ngược** `wr_assign_task_product_items/services.finish_percent, is_completed` | xoá products type 1 (không xoá items/services/device_errors cũ); `serials` JSON; `serial_id` dò lại theo (product_id, serial) nếu FE gửi key `serial_id`; item: `wr_assign_task_product_item_id = item.id`, `available_qty`, `delivery_customer_qty` lấy từ bản giao việc; service: `qty = 1`, `wr_assign_task_product_service_id = service.id`, `available_qty`, `payed_price`, `cost_price`, `sell_price = revenue_price` từ bản giao việc |
   | `syncProductRepair(…,2)` M:789 | như trên type 2 | xoá products type 2 **và TẤT CẢ product_services/product_items của phiếu** (không lọc type) |
   | `syncExtendProducts` M:1034 | `wr_import_result_extend_products` / `_services` / `_service_items` | xoá-ghi 3 cấp; `model_id/model_name` lấy từ `products.model` (tìm theo product_id) |
   | `syncProduct(…,3)` M:360 | `wr_import_result_products` type 3 + device_errors | `serials` JSON, `serial` = nối các serial bằng `,`; `device_error_*` = phần tử đầu `product_device_errors` |
   | `syncItem(…,1/2/3)` M:1077 | `wr_import_result_items` | xoá-ghi theo type |
   | `syncService(…,1/2)` M:1089 | `wr_import_result_services` | xoá-ghi; file → S3 `wr_import_result_service` |
   | `syncCost` M:1111 / `syncRevenueCost` M:1132 | `wr_import_result_costs` type 1 / 2 | xoá-ghi; file → S3 `wr_import_result_cost` |
   | `syncWork` M:1154 | `wr_import_result_works` | xoá-ghi |
   | `syncExecutor` M:1165 | `wr_import_result_executors` | xoá-ghi |
   | `syncTimesheet` M:1176 | `wr_assign_task_timesheets` (UPDATE) | checkin_actual, checkout_actual, time_actual |
   | `syncGalleries*` M:1187/1199 | `wr_import_result_galleries_constructions/handovers` | xoá-insert (chỉ khi mảng ≠ rỗng) |
   Mỗi nhóm chỉ chạy khi request có mảng khác rỗng.
4. `wr_assign_tasks.status`: status 1 → **7 DANG_NHAP_KET_QUA**; status 2 → **2 DA_NHAP_KET_QUA** + thông báo:
   `NotificationHelper::sendNotifyWithPermission('Duyệt phiếu nhập kết quả', '/admin/customer-care/wr_approve_results/create?wr_import_result_id={id}', 'Bạn có 1 phiếu kết quả giao việc cần duyệt')` — người nhận: mọi NV có quyền đó **cùng công ty với người đăng nhập** (helper :40-69). Gửi **trong transaction**, trước các bước ATP.
5. **ATP lắp đặt** (`product_assembly` ≠ rỗng, C:336-414): với mỗi dòng type 3 vừa lưu, tìm `assign_task_progress` (product_id, assign_task_id, request_type 4). Lần đầu gặp product → **xoá hết `assign_task_serial_progress`** của ATP đó. Cập nhật ATP: `import_result_id, import_result_qty (= tổng luỹ kế mọi dòng — sai, bị ghi đè ở bước sau), serial, import_result_time_update = now, import_result_detail_id, success_percent = finish_percent, current_stage = 4 IMPORT_RESULT, status = 1 DA_DUYET`; INSERT `assign_task_serial_progress (assign_task_progress_id, serial, success_percent, qty = delivery_qty, can_request = finish_percent == 100)`.
   Rồi duyệt lại mọi ATP lắp đặt của phiếu: `can_request_qty = Σ serialProgress.qty`; `import_result_qty = Σ delivery_qty` theo product; ATP không có dòng nào → import_result_qty 0, success 0, stage 4, status 1.
6. **ATP sửa chữa** (C:416-551): ATP (request_type 2, type 1 REPAIR, contract_type `wr_service`) khớp product_id + `serial_contract = serial_old` (+ device_error_id nếu có) → `import_result_*`, `success_percent`, stage 4, `serial`, status 1, `can_request_qty = delivery_qty = delivery_qty dòng`. `itemProgress` (khớp `parent_id = product_id` vật tư): `import_result_qty = qty = item.qty`, không thấy → qty 0. `serviceProgress`: gom dịch vụ cùng **`parent_id = serviceProgress.cost_id`** (store) — update dùng `cost_id = serviceProgress.parent_id` (2 bản lệch nhau): `import_result_qty = Σqty`, `qty = delivery_qty = can_request_qty = Σqty`, `complete_text = JSON[{id,qty,is_completed,finish_percent}]`; không có → 0.
7. **ATP bảo dưỡng** (C:553-611): ATP type 2 EXTEND khớp product_id + serial_contract=serial_old → import_result_*, stage 4, serial, status 1; serviceProgress khớp (`parent_id = service_id`, `type_id = level_id`) → success_percent, can_request = is_completed, import_result_qty = qty = delivery_qty = can_request_qty = service.qty; serviceItemProgress khớp (parent_id = product_id, unit_id) → import_result_qty = qty = item.qty (không null-check).
8. **ATP hàng bán thêm** (C:613-633): ATP type 3 MERCHANDISE khớp product_id → import_result_qty = delivery_qty = can_request_qty = item.delivery_qty, stage 4, status 1.
9. **ATP bảo hành** (C:635-768): ATP request_type 3, type 5 WARRANTY khớp product_id (+device_error_id) → như sửa chữa (item/service progress, service gom theo `cost_id = parent_id`). Sau đó `wr_service_contracts.is_assign = canAssignTaskWarranty() ? 1 : 0`.
10. **ATP dịch vụ đính kèm** (C:770-787): ATP request_type 5, type 6 REVENUE_COST khớp `product_id = cost_id` → import_result_qty 1, success_percent, stage 4, status 1 (không null-check).
11. `attachments` (S3 `wr_import_results`) — chức năng chết.
12. `DB::commit` → `responseSuccess($object)`; catch `\Exception` → rollback + `responseErrors($e->getMessage())` (ValidationException không liên quan vì FormRequest chạy trước).

### 4.2 update (C:1897-2484) — khác store
- Không kiểm PCT, không kiểm canEdit; kiểm trùng "Phiếu nhập kết quả đã tồn tại"; vẫn chạy checkValidateSerial + hasProductExport.
- `only` bỏ `delivery_place, customer_contact_*, firm_contract_*, creator_request, phone_creator` (giữ wr_assign_task_*, customer_*, sw_note, sr_note, status, note). Không sinh lại code.
- BH/SC dùng `syncProductWarrantyEdit` / `syncProductRepairEdit` (M:724, 965): **không cập nhật ngược** bảng giao việc; dịch vụ `wr_assign_task_product_service_id = service.id` (lúc này `id` là id dòng nhập KQ cũ, không phải id dịch vụ giao việc); không copy available/price; BH Edit **không xoá** items/services cũ (nhân bản mỗi lần sửa nếu không có SC).
- attachments xử lý trước khi đổi status; ATP lắp đặt **không gán serial** cho ATP, `import_result_qty` luôn 0 rồi bị ghi đè; SC khớp ATP thêm điều kiện serial_old; BD **không null-check ATP**, service item thêm success_percent/can_request; dịch vụ đính kèm thêm `delivery_qty = can_request_qty = 1`.
- catch **không `return`** ⇒ lỗi trả HTTP 200 rỗng (FE vào nhánh `success: undefined` → toast `undefined`).
- Mỗi lần update status 2 lại bắn thông báo.

### 4.3 Bản app mobile (storeApp C:800, apiStore C:3075, apiUpdate C:3198, apiShow C:2913)
Route `prefix hrm` **không middleware** (routes/web.php:23-31): `POST hrm/wr_import_results` (storeApp), `POST hrm/wr_import_results/{id}` (= `update` web), `hrm/wr_import_results/upload*Img`. storeApp khác store: nhận thêm `created_by, updated_by` từ request; dùng `syncProduct*App` (thêm `delivery_qty = qty` nếu rỗng); company lấy theo `request()->employee_info_id` khi không có auth. HRM web port **không cần** các bản này (app Flutter là chủ đề khác).

---

## 5. Dữ liệu nguồn `WrAssignTask::getForDataImportResult` (AT:1856-2252) + C:create
Trả **mảng** (`toArray`) phiếu giao việc + quan hệ:
```
{ ...cột wr_assign_tasks, customer_code, wr_service_contract_code, assembly_request_code, assign_other_request_code,
  product_export_requests (json decode), places (json decode),
  wr_service_contract{…, employee_create{info}}, assembly_request{…, employee_create{info}}, assign_other_request{…},
  customer{…},
  product_repairs[]: { …wr_assign_task_products (handle_type 1), product{…}, is_serial, delivery_qty = qty, worker_qty (contractRows theo group_id / product_type, mặc định 1),
                       serials[] (serial đang dùng của KH), product_stock_qty (SL thiết bị KH), can_import_result,
                       product_device_errors[] (rỗng → 1 phần tử tạm {device_error_id, device_error_name} của dòng),
                       services[]: tách theo qty → mỗi phần tử qty 1, is_completed 0, finish_percent 0 (giữ id dịch vụ giao việc),
                       items[]: chỉ qty > 0, key available_qty đặt trước qty },
  product_warrantys[]: như trên (handle_type 0; không có is_serial; không có device_error tạm),
  extend_products[]: { …, product{…}, serials, product_stock_qty, services[] (qty>0, nhân bản `qty` lần, mỗi bản giữ nguyên qty!, products[] qty>0) },
  merchandises[]{product}, costs[], assembly[] (qty > 0; is_serial theo serial_product_types; product{}),
  work_p12[], work_p3[], executors[], timesheets[], revenue_costs[] }
```
Chỉ giữ thiết bị `can_import_result` (qty>0 hoặc có dịch vụ/vật tư qty>0). C:create bổ sung `firm_contract_id/code` (lắp đặt), `creator_request`, `phone_creator` (fullname/telephone người tạo chứng từ nguồn).
Edit dùng `WrImportResult::getForEdit` (M:1251-1336) + xử lý C:1654-1876: dựng `items/services` từ bảng nhập KQ, `type_status` từ `wr_assign_task_products` (handle_type 1/0), `rate_effort` lấy lại từ phiếu giao việc (SC có device_error) hoặc từ dịch vụ BD (SC không device_error), lắp đặt lấy lại `rate_effort/exportable_*` từ `wr_assign_task_assembles`, `serials` decode, wr_service gắn lại `serials/product_stock_qty` từ danh sách thiết bị KH.

---

## 6. Đối chiếu DB thật (tinker, chỉ SELECT)

Bảng (tên đúng): `wr_import_results` (6920), `wr_import_result_products` (15255; type 1=3865, 2=2371, 3=9019), `…_product_items` (1483), `…_product_services` (3458), `…_product_device_errors` (2404), `…_extend_products` (1183), `…_extend_product_services` (1348), `…_extend_product_service_items` (55), `…_items` (1713; type 2=1442, 3=271, **type 1 = 0**), `…_services` (3514), `…_costs` (26160; type 1=25470, 2=690), `…_works` (645), `…_executors` (10622), `…_galleries_constructions` (11297), `…_galleries_handovers` (8258), `…_other_services` (0, bảng chết), **`assign_task_serial_progress`** (số ít, 8370), `wr_assign_task_timesheets` (**0**).

Cột NOT NULL không default (phải tự điền khi ghi bằng query builder):
- `wr_import_results`: wr_assign_task_id, **code** (unique — ERP save trước rồi mới sinh code ⇒ HRM phải điền tạm/sinh trước), **created_by, updated_by**, **status**. Unique `wr_assign_task_id`.
- `wr_import_result_products`: wr_import_result_id, **product_name, product_code**, product_id, type.
- `…_product_items` / `…_product_services`: wr_import_result_id, wr_import_result_product_id, **wr_assign_task_product_item_id / wr_assign_task_product_service_id**.
- `…_product_device_errors`: wr_import_result_product_id, wr_import_result_id, **device_error_id, device_error_name**.
- `…_items`: wr_import_result_id, product_name, **product_code**, product_id, type.
- `…_services`: wr_import_result_id, **service_name**, type. `…_costs`: wr_import_result_id, **cost_name**. `…_works`: wr_import_result_id, **work_name**. `…_executors`: wr_import_result_id, employee_id. galleries: wr_import_result_id, **url**. timesheets: wr_assign_task_id, day.
(Bảng extend_* toàn nullable; `qty`, `is_completed` NOT NULL có default.)
`assign_task_serial_progress`: id, assign_task_progress_id, serial, serial_old, success_percent(_old), qty(_old), can_request(_old) NOT NULL default 0, timestamps.

Dữ liệu: status phiếu 3=6661, 2=197, 6=56, 1=4, 5=2 · theo type phiếu giao việc 1=1821, 2=3205, 3=68, 4=1158, 5=668 · mọi phiếu có `has_assign_business = 1` · `sw_note`, `attachments` toàn NULL · không phiếu nào có cả BH lẫn SC · gallery URL dạng `/uploads/wrImportResult/construction/<file>.jpg` (tương đối, host ERP) · code `TPE.PNKQ.2026007047` · bản ghi mới nhất 28/07/2026.
Mẫu: SC/HĐ `id 7041` (4 product type 2 có device_error, `serials` JSON = danh sách serial KH, 5 cost type 1 price 0, 2 executor, 2+2 ảnh) · Lắp đặt `7047` (product type 3, `worker_qty 10`, `is_serial 1`, serials `[{"serial":"FGHFGH1566"}]`, 1 work P3) · GVK `7045` (cost type 2 `rate_effort 0.7` nhưng **`rate_effort_approve 1.00`** > ĐM — có thể do bước duyệt), `7046` (9 ảnh công trình, 0 ảnh bàn giao).
Bất thường dữ liệu do lỗi ERP: **271 nhóm product_services trùng** (cùng product + cùng service giao việc), **14 product_services mồ côi**, **172 device_errors mồ côi** (product đã bị xoá-ghi).

Quyền (bảng `permissions`, guard api): **không có** "Duyệt phiếu nhập kết quả", "Nhập kết quả thực hiện", "Xem phiếu nhập kết quả theo …". Chỉ có "Nhập kết quả công tác/công việc" (khác nghiệp vụ).

---

## 7. Lỗi / bất thường ERP (chỉ ghi, không sửa — theo chốt "y hệt ERP")
1. `update` không kiểm `canEdit` / PCT; route `hrm/wr_import_results/{id}` (= update) và `hrm/wr_import_results` (storeApp) **không có middleware đăng nhập**.
2. `update` catch thiếu `return` → lỗi trả 200 rỗng, FE toast `undefined`.
3. `syncProductRepair(Edit)` xoá **toàn bộ** product_items/services của phiếu (không lọc type) — nếu có cả BH sẽ mất dữ liệu BH (DB chưa gặp).
4. `syncProductWarrantyEdit` không xoá items/services cũ → nhân bản mỗi lần sửa (271 nhóm trùng trong DB); mọi `sync*Product*` không xoá device_errors cũ → mồ côi (172).
5. Edit gán `wr_assign_task_product_service_id = service.id` = id dòng nhập KQ cũ (sai liên kết); edit không cập nhật ngược finish/is_completed bảng giao việc.
6. Service progress: store gom theo `parent_id = serviceProgress.cost_id` (SC) — update theo `cost_id = parent_id` (lệch, store SC có thể không khớp).
7. ATP revenue cost / extend (update) / service item không null-check → 500 "Attempt to assign property on null" khi lệch dữ liệu.
8. `edit` C:1727: `($cur->rate_effort || 0)` trả boolean → ĐM công SC không lỗi thiết bị = số dịch vụ có qty; `$wr_product->type` không null-check → 500 nếu dòng giao việc bị xoá.
9. Rule FormRequest bị ghi đè cùng key → "đang bị trùng" / "cần nhập cùng serial" không bao giờ chạy; closure SC phần chặn đã comment; `product_stock_qty` undefined index nếu FE không gửi (ErrorException). Message `.*.file/.mimes` của ảnh vô dụng.
10. `sw_note` có trong `only` nhưng không có trong `$fillable`. `approve_comment` gửi lên nhưng không lưu.
11. Card "B - DANH SÁCH GIAO NHẬN VẬT TƯ" và "DANH SÁCH DỊCH VỤ TRẢ TIỀN" điều kiện mâu thuẫn ⇒ không bao giờ hiện, nhưng dữ liệu vẫn ghi; h4 "B - DANH SÁCH VỤ TRẢ TIỀN" sai chính tả; điều kiện h4 dùng `||` thay `&&`.
12. Popup "Chọn serial cần ngưng" chết (`chooseSerial()` rỗng); các `ng-change="service.chooseSerial()"`/`product_item.chooseSerial()` gọi hàm không tồn tại (Angular nuốt).
13. Upload ảnh nhiều file 1 lượt chỉ nhận file cuối (`res.data.pop()`); xoá ảnh không xoá file vật lý; xoá **hết** ảnh khi sửa không có tác dụng (sync chỉ chạy khi mảng ≠ rỗng); `insert` không có timestamps.
14. `finish_percent` nhập 100 (không tick) bị bỏ qua im lặng (setter chỉ nhận <100).
15. `rate_effort_main` bỏ công BH khi phiếu có cả SC/BD.
16. Nhánh swal xác nhận "Lưu & Gửi duyệt" không xử lý `check_product_export`.
17. Thông báo bắn trong transaction trước các bước ATP (rollback sau đó vẫn để push realtime đã gửi); update status 2 bắn lại mỗi lần lưu.
18. `getForDataImportResult` extend: nhân bản service `qty` lần nhưng **giữ nguyên qty** mỗi bản (khác SC/BH đặt 1).
19. Code + company/department theo **người đăng nhập** chứ không theo phiếu giao việc.
20. GET create không kiểm quyền / canImportResult (chỉ store kiểm PCT + trùng).
21. ATP lắp đặt store: `import_result_qty` luỹ kế qua mọi sản phẩm (bị ghi đè ở vòng sau nên kết quả cuối đúng).

---

## 8. Tái dùng từ màn Phiếu giao việc (HRM, nhánh `develop` ⊂ gop_db)
BE `hrm-api/Modules/CustomerCare`:
- **Entities/WrAssignTask/** — dùng lại toàn bộ: `WrAssignTask` (hằng status 1/7/2/…, `PCT_DA_DUYET`, type 1-5, quan hệ wr_service_contract/assembly_request/assign_other_request/customer/creator, `product_warrantys/repairs`), 13 bảng con `WrAssignTask*` (để đọc nguồn + cập nhật ngược `wr_assign_task_product_items/services`), `AssignTaskProgress` (đủ hằng `IMPORT_RESULT = 4`, `DA_DUYET = 1`, TYPE_*, quan hệ `itemProgress/serviceProgress/serviceItemProgress`) + `AssignTaskItem/Service/ServiceItemProgress`. **Thiếu**: `AssignTaskSerialProgress` (bảng `assign_task_serial_progress`), `WrAssignTaskTimesheet` (có `Modules/Human/Entities/TpWrAssignTaskTimesheet.php` — kiểm connection trước khi dùng), quan hệ `executors/work_p3/costs/merchandises/revenue_costs/assembles/timesheets` trên WrAssignTask (kiểm lại tên).
- `Services/WrAssignTaskRemainingService::canAssignTaskWarranty(int $contractId)` (:145) — dùng cho bước 4.1-9.
- `Services/WrAssignTaskSourceService` — logic `worker_qty` theo `contractRows`, `is_serial` theo `serial_product_types`, `rate_effort` dịch vụ BD theo `quota_work` (:528) → tách helper dùng chung cho `getForDataImportResult`.
- `Services/WrAssignTaskStoreService` — khuôn transaction + `insert()` query builder (:873) + `writeDeviceProgress` (:771) / `writeAssemblyProgress` (:825) làm mẫu cho bước ghi ATP; `generateCode` format `{company}.PGV.` → đổi `PNKQ`.
- `WrAssignTask::canImportResult` (đã port) — dùng để chặn GET create / lối vào.
- Chưa có: port `Customer::getListProductOfCustomer` (ERP ~360 dòng, dùng ở checkValidateSerial + nguồn serial). Có thể tham khảo `Modules/Assign/Services/CustomerManagerService.php` TAB 5 (equipments_old + external_equipments + serials, :324-780) nhưng không đồng nhất đầu ra (`qty`, `serials`, `type`, `product_no_sale_name`) → cần port riêng hoặc tách hàm chung (hỏi trước vì là hàm dùng chung).
FE `hrm-client/pages/customer-care/wr-assign-tasks/components/`:
- `wrAssignTaskCalc.js` (`num/round2/fmt/deviceTypeText/deviceTitle/requireWorkerQty`) — tái dùng trực tiếp (thêm công thức approve × %).
- `WrAssignTaskNumberCell.vue` (ô số trong bảng, tách component chống lag) — tái dùng.
- `WrAssignTaskDeviceTable.vue` (i.1/i.2/i.3 BH/SC), `WrAssignTaskMaintainTable.vue` (BD), `WrAssignTaskAssemblyTable.vue`, `WrAssignTaskRevenueCostTable.vue`, `WrAssignTaskP3WorkTable.vue`, `WrAssignTaskMerchandiseTable.vue` — **khung bảng + tiêu đề dòng** dùng lại được, nhưng cột khác hẳn (thêm Kết quả: checkbox/%, Serial, CK đề xuất, CK được tính) → nên copy thành bộ `WrImportResult*Table.vue` hơn là thêm prop.
- `wrAssignTaskLinks.js` — đổi `importResultCreateUrl/importResultShowUrl` sang HRM khi port xong; `sourceDocuments(form)` dùng lại cho khối Thông tin khách hàng.
- `WrAssignTaskForm.vue` (khuôn khối Thông tin khách hàng, `CreatorInfoLine`, cảnh báo chưa lưu, nút) — khuôn vỏ form.
- Upload ảnh: dùng khối file đính kèm chung `AttachmentSection.vue` (memory) / S3 HRM — xem điểm chốt C.

---

## 9. Ước lượng & đề xuất chia task (phần B: form tạo/sửa + lưu)

| # | Task | Ước lượng |
|---|---|---|
| BE-1 | Entities `WrImportResult` + 15 bảng con + `AssignTaskSerialProgress` + timesheet (khai `$table`, quan hệ, hằng status 1-6, `canEdit`) | 0,5 ngày |
| BE-2 | Port `Customer::getListProductOfCustomer` (service riêng, chỉ đọc) | 1 ngày |
| BE-3 | `GET /customer-care/wr-import-results/source-data?wr_assign_task_id=` (port getForDataImportResult + C:create) + chặn theo `canImportResult` | 1 ngày |
| BE-4 | `GET /{id}/edit-data` (port getForEdit + C:edit, kể cả lỗi 8) + `canEdit` → 403 | 0,5–1 ngày |
| BE-5 | FormRequest (rule + câu lỗi nguyên văn, kể cả rule chết giữ nguyên hành vi) + `checkValidateSerial` + `hasProductExport` (cần entity/đọc `product_export_requests`, `borrow_sell*`) | 1,5 ngày |
| BE-6 | `StoreService` store/update: insert + sync 14 bảng (y lỗi ERP 3-6) + status phiếu giao việc + ATP 6 nhánh + serial progress + is_assign; transaction, rethrow ValidationException | 2–2,5 ngày |
| BE-7 | Upload ảnh 2 loại + thông báo "Duyệt phiếu nhập kết quả" (NotificationMeta) + quyền seeder (nếu chốt) + lịch sử (catalog_histories, đăng ký bảng) | 1 ngày |
| FE-1 | Trang `create.vue` / `[id]/edit.vue` + vỏ form (3 tab, Thông tin KH, Chấm công, File ảnh) + unsavedChanges | 1 ngày |
| FE-2 | Bảng BH/SC (i.1-i.3), Bảo dưỡng (II), Lắp đặt (serial động theo SL), Dịch vụ đính kèm, P3 + Tổng công định mức, Vật tư bán thêm; công thức computed | 2,5–3 ngày |
| FE-3 | Submit 2 nút + swal xác nhận + xử lý `check_serial` (xoá serial mới) / `check_product_export` (popup Cảnh báo) + lỗi inline (`touched`) | 1 ngày |
| QA | Smoke API bằng HTTP kernel (route:list hỏng) cho 5 type, so count bảng con với phiếu ERP mẫu (memory "ERP sinh sẵn bảng kết quả") | 1 ngày |
**Tổng phần B ≈ 13–15 ngày công** (chưa gồm danh sách/xem/duyệt/không duyệt/xoá — phần khác).
Thứ tự đề xuất: BE-1 → BE-3 → FE-1/FE-2 (đọc nguồn hiển thị được) → BE-2/BE-5 → BE-6 → BE-7 → FE-3 → QA.

---

## 10. Điểm cần user chốt
A. **Quyền**: HRM chưa có "Duyệt phiếu nhập kết quả" (người nhận thông báo + duyệt) — thêm vào seeder với tên nguyên văn ERP? Có gắn middleware cho store/update không (ERP không gắn)?
B. **Lỗ hổng ERP 1/2/20** (update không kiểm canEdit, GET create không kiểm): "y hệt ERP" có giữ luôn lỗ hổng quyền không, hay HRM tối thiểu chặn `canEdit` / `canImportResult` ở BE (defense-in-depth theo CLAUDE.md)?
C. **Ảnh thi công/bàn giao**: ERP lưu local disk ERP + path tương đối `/uploads/...`. HRM upload lên **S3 và lưu URL tuyệt đối** (ERP vẫn hiển thị được vì `<img src>` tuyệt đối) hay upload sang ERP? Ảnh cũ hiển thị ở HRM = ghép `ERP_URL` + path.
D. **Các khối chết** (card Giao nhận vật tư, Dịch vụ trả tiền, Chi phí liên quan, Nhân sự tham gia, popup Chọn serial cần ngưng, tab Chấm công không có dữ liệu): không dựng UI nhưng **vẫn gửi & ghi** dữ liệu ẩn (items/services/costs/executors) như ERP? Đề xuất: ghi y ERP (bước duyệt đọc các bảng này), không dựng UI khối chết.
E. **Lỗi ghi dữ liệu 3-6** (xoá nhầm items/services, nhân bản khi sửa, sai `wr_assign_task_product_service_id` khi sửa): giữ y hệt (dữ liệu bẩn tiếp tục sinh) hay ngoại lệ sửa? Ảnh hưởng trực tiếp bước Duyệt + Đề nghị thanh toán.
F. **Code + company_id** theo người đăng nhập (ERP) hay theo phiếu giao việc?
G. **Câu lỗi bắt buộc**: giữ câu mặc định Laravel/"Thao tác thất bại" như ERP hay đổi sang chuẩn HRM "Bắt buộc phải nhập" (màn Phiếu giao việc đã đổi)?
H. Mở màn Tạo/Sửa HRM từ đâu: đổi `wrAssignTaskLinks.importResultCreateUrl` + nút "Sửa" danh sách sang HRM ngay khi xong phần B, hay đợi port xong cả danh sách/xem/duyệt?
