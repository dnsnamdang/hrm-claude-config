# Khảo sát C — "Duyệt kết quả" (ERP `WrApproveResults`) để gộp vào màn Phiếu nhập kết quả HRM — @khoipv

Ngày: 03/11/2026 · Chỉ đọc code ERP `D:\laragon\www\erp` + SELECT DB `gop_db` (không sửa code, không ghi DB).
Viết tắt: **C** = `app/Http/Controllers/Customercare/WrApproveResultsController.php` · **AT** = `app/Model/Customers/WrAssignTask.php` ·
**R** = `app/Http/Requests/WrApproveResultsStoreRequest.php` · **V/** = `resources/views/customercare/wr_approve_results/` ·
**PDKQ** = Phiếu duyệt kết quả · **PNKQ** = Phiếu nhập kết quả · **PGV** = Phiếu giao việc · **ATP** = `assign_task_progress`.

---

## 0. Phát hiện quan trọng nhất

1. **KHÔNG có bảng `wr_approve_results`.** PDKQ là **một dòng của chính bảng `wr_assign_tasks`** với `parent_id = id PGV`
   (AT:204-207 "có parent là phiếu duyệt kết quả"; C:281-285 `new WrAssignTask(); parent_id = wr_assign_task_id`).
   Bảng con cũng là **bảng con của PGV** (`wr_assign_task_products / _product_services / _product_items / _product_device_errors /
   _extend_products / _extend_product_services / _extend_product_service_items / _assembles / _p3_works / _p12_works /
   _revenue_costs / _merchandises / _costs / _executors`), phân biệt bằng `wr_assign_task_id = id PDKQ`.
   - DB: 6 664 PDKQ, mỗi PGV tối đa 1 PDKQ (`count = count(distinct parent_id)`); mã min `TPE.PDKQ.2025000049`, max `TPV.PDKQ.2026014517`.
   - Cột `status` của PDKQ dùng **bộ hằng riêng** `KQ_*` (AT:48-51, 165-186), trùng cột với trạng thái PGV.
   - HRM đã có entity `Modules/CustomerCare/Entities/WrAssignTask/WrAssignTask.php` + đủ entity bảng con (port từ màn PGV) và
     `WrImportResult::wr_approve_result()` (hasOne `parent_id`). Màn PGV HRM đang `whereNull('parent_id')`.
2. **Chỉ có 1 cấp duyệt thật.** Cấp "BKS duyệt" (KQ 4) là **code chết**: không chỗ nào gán `status = 4` (grep toàn ERP), DB 0 PDKQ status 4,
   `bksUnApprove` không có nút gọi + cột `bks_approve_comment` không tồn tại. "Kế toán kho trả về" (`refuseToAccount`) cũng không có nút (V/form:2430 bị comment).
   Bước sau duyệt là **Hạch toán dịch vụ** (`WrAccountingService.create?wr_approve_result_id=`) — màn kế toán khác, HRM chưa nối đường này.
3. Trường "Ghi chú", "Ghi chú duyệt", "Ghi chú BKS duyệt" trên form **hiển thị cho gõ nhưng KHÔNG lưu** (không nằm trong `$request->only`, bảng không có cột
   `approve_comment`/`bks_approve_comment`; DB 0/6 664 PDKQ có `note`).

---

## 1. Luồng duyệt

### 1.1 Ai được duyệt (vào form tạo PDKQ)
- Điều kiện duy nhất: `WrImportResult::canApproveResult()` = **PNKQ status 2 "Chờ duyệt kết quả"** + quyền **"Duyệt phiếu nhập kết quả"** + **cùng công ty** với PNKQ
  (`app/Model/Customers/WrImportResult.php:355-358`). Áp ở `create` (C:205 → `not_found`) và `store` (C:274-280, "Không có quyền").
- Route store/update có middleware **`checkDueConfigsManager:Duyệt kết quả công việc`** (routes/web.php:6178, 6183) — chặn trưởng phòng có NV quá hạn
  (`app/Http/Middleware/CheckDueConfigsManager.php`; HRM ĐÃ có middleware này `app/Http/Middleware/CheckDueConfigsManager.php`).
- Sửa PDKQ (lưu nháp xong làm tiếp): `WrAssignTask::canEdit()` = PDKQ status 3 "Đang tạo" **và đúng người tạo PDKQ** (AT:422-424). Chỉ check ở `edit` (C:893),
  **`update` KHÔNG check quyền** (C:937-960, đoạn check bị comment).
- Xem PDKQ: `canView()` (AT:344-389): Super Admin / người tạo / executor / 3 quyền "Xem phiếu duyệt kết quả theo tổng công ty|công ty|phòng ban"
  (trừ phiếu Đang tạo) / "Kế toán kho" xem phiếu Chờ hạch toán cùng công ty.

### 1.2 Các nút → trạng thái ghi (đọc `ng-click` thật, V/form:2400-2440 + V/create:54-170)
| Nút (nhãn ERP) | Hiện khi | Gửi `status` PDKQ | Ghi chú |
|---|---|---|---|
| **Lưu** | luôn (create/edit) | `3` KQ_DANG_TAO "Đang tạo" | lưu nháp |
| **Duyệt** | `assembly_request_id \|\| assign_other_request_id` (lắp đặt / GVK) | `2` KQ_DA_HACH_TOAN "Đã hạch toán" | bỏ qua bước hạch toán |
| **Duyệt** | `wr_service_contract_id` (HĐ SC / BH / PL) | `1` KQ_CHO_HACH_TOAN "Chờ hạch toán" | chờ Kế toán kho |
| **Không duyệt** | luôn (create/edit) | — | swal bắt nhập lý do → `POST unApprove` |
| Hạch toán dịch vụ (link) | `canAccountingService()` (chỉ ở màn Xem) | — | sang màn kế toán |
| Quay lại | luôn | — | `WrApproveResults.index?type=all` |

- **Ép trạng thái** (V/create:73-78): nếu KHÔNG có dòng nào "hoàn thành" (SC/BH/BD/dịch vụ đính kèm) **và không có lắp đặt** và nút ≠ Lưu ⇒ `status = 2` (Đã hạch toán) +
  swal xác nhận "Phiếu không hoàn thành công việc, bạn có đồng ý không?".
- Lưu xong → `WrApproveResults.index?type=all` + toast "Thao tác thành công!". Không duyệt xong → `WrImportResults.index?type=wait_approve_result`.

### 1.3 Mỗi bước đổi gì (store C:229-886, update C:937-1603)
| Bảng | Lưu (3) | Duyệt HĐ (1) | Duyệt lắp đặt/GVK hoặc ép (2) |
|---|---|---|---|
| `wr_assign_tasks` (PDKQ) | tạo/sửa, status 3 | status 1, `approved_by/time` (update: chỉ lần đầu) | status 2, `approved_by/time` |
| `wr_assign_tasks` (PGV cha) | status **8** Đang duyệt KQ | status **3** Đã duyệt KQ + copy 4 cột `sum_amount_rate_effort_*` | như cột bên |
| `wr_import_results` | status **5** Đang duyệt KQ | status **3** Đã duyệt KQ | status 3 |
| HĐ dịch vụ (`wr_service_contract_*`) | — | `syncSerial()` (AT:2548) + `updateContract()` (AT:2281): `assign_qty +=` SL đã duyệt hoàn thành ở dòng SC/BH/BD/vật tư/dịch vụ/hàng bán thêm của HĐ; ghi `serial/serial_id/add_serial=0` vào HĐ + `wr_import_result_products` | — |
| `serials` | — | `syncProduct/syncExtendProducts` khi status 1: tạo serial mới (`Serial::insertSerial`), serial cũ đổi sẽ `NGUNG_SU_DUNG` (AT:1071-1165, 1227-1310) | `syncAssembly` khi status 2: `insertSerial` cho serial lắp đặt (AT:1414-1500) |
| `assembly_requests` + `_details` | — | — | `updateAssemblyRequest()` `assign_qty += Σ delivery_qty` (AT:2532) + status Đã/Chờ giao việc |
| `wr_service_contracts.is_assign` | tính lại khi có `product_warrantys` (C:707-716) | như trái | như trái |
| ATP + con | luôn cập nhật (mọi status) — chi tiết mục 3.3 | | |
| Thông báo | — | `sendNotifyWithPermission('Kế toán kho', show PDKQ, 'Bạn có 1 phiếu kết quả giao việc cần hạch toán')` — người có quyền **cùng công ty người duyệt** | — |
| Thông báo app (#9816) | — | PNKQ lần đầu sang 3 → gọi HRM `POST /api/v1/assign/wr_import_results/{id}/notify-result {status:approved}` (C:2389-2406; HRM `Modules/Assign/.../WrImportResultController::notifyResult`) | như trái |

- Sau duyệt: PDKQ 1 → **Kế toán kho** "Hạch toán dịch vụ" (`WrAccountingServicesController:145-215`) đổi PDKQ → **2 Đã hạch toán**.
  Lưu ý BH (type 2) cũng thành "Chờ hạch toán" nhưng danh sách `wait_accounting_service` **loại type 2** → BH kẹt "Chờ hạch toán" vĩnh viễn (DB: 3 025 PDKQ BH status 1).
- DB phân bố PDKQ (type/status): HĐ 1761×2, 13×1, 1×3 · BH 3025×1, 126×2, 1×3 · PL 64×2, 2×1 · Lắp đặt 1058×2 · GVK 612×2, 1×3.
  PNKQ ↔ PDKQ: PNKQ 3 có PDKQ 2 (3 621) hoặc 1 (3 040); PNKQ 2 không PDKQ (196); PNKQ 5 có PDKQ 3 (2); PNKQ 2 có PDKQ 3 (1 — lệch).

### 1.4 Không duyệt từ form duyệt — `unApprove` (C:1642-2040) ≠ `WrImportResults@reject` HRM đã port
- Validate `wr_import_result_id` required, `approve_comment` **nullable** ở BE (FE swal bắt buộc). **Không check quyền** (dòng check bị comment C:1671-1673).
- PNKQ → **6** + `approve_comment`; `sendNotify(người tạo PNKQ, 'X vừa không duyệt phiếu nhập kết quả của bạn!')`; gọi HRM `notify-result {rejected, reason}`.
- Nếu đã có PDKQ (nháp): ATP các dòng của PDKQ → `status = KHONG_DUYET` (không null-guard → lỗi nếu thiếu ATP), tính lại `is_assign` BH, rồi **`deleteAll()` PDKQ**.
  Nếu chưa có: ATP của PGV → KHONG_DUYET (có null-guard).
- **Không đổi trạng thái PGV** (PGV đang 8 sẽ kẹt 8 nếu không duyệt sau khi đã Lưu nháp).
- HRM `WrImportResultService::reject()` (port `WrImportResultsController@reject`) đòi PNKQ status 2 → **phiếu đang nháp duyệt (PNKQ 5) sẽ bị 409** → cần nhánh unApprove riêng nếu cho Không duyệt ở chế độ duyệt nháp.

### 1.5 Các action khác
- `delete($id)` GET (C:2136-2309): `canEdit()` mới xoá; hoàn ATP về IMPORT_RESULT, dựng lại serial progress lắp đặt từ PNKQ, `deleteAll()`. **Không có nút nào gọi** (index chỉ có Sửa/BKS/Hạch toán).
- `refuseToAccount` (C:2042-2087): Kế toán kho trả về → PNKQ **1** + `updateContractWhenUnApprove` + xoá PDKQ. Nút bị comment.
- `bksUnApprove` (C:2089-2131): code chết (status 4 không bao giờ xảy ra, cột không tồn tại).

---

## 2. Form duyệt

### 2.1 Dữ liệu nguồn (create C:189-227)
`WrAssignTask::getForShowImportResult(PGV)` (AT:1668-1802 — PGV + con, đánh `can_assign_task` cho BH) ghép PNKQ, rồi `WrAssignTask::mapImportResult()` (AT:638-1060):
- BH: chỉ dòng PGV `can_assign_task`; ghép dòng PNKQ type 1 cùng `product_id` (+`product_type/serial_old` nếu có serial) → lấy `is_completed, note_import_result, serial, serial_id,
  serial_old, finish_percent, delivery_qty, worker_qty, is_serial`, `items/services` = **của PNKQ**; **xoá `rate_effort_approve/result`** (CK đề xuất tính lại ở FE).
- SC: như BH nhưng khớp thêm `device_error_id`; dòng PGV không có ở PNKQ bị **bỏ**.
- Lắp đặt: lấy **thẳng dòng PNKQ type 3**; `worker_qty`/`rate_effort` bù từ `wr_assign_task_assembles` PGV; `benefit_rate` 0 ⇒ hệ số nhóm hàng;
  `rate_effort_approve = round(rate_effort × ceil(delivery/worker) × finish% / 100, 2)`.
- Hàng bán thêm: `qty/delivery_qty` từ `wr_import_result_items` type 3. P3: ghép theo `work_name` (`is_completed`, `rate_effort_approve`, `note` của PNKQ; dòng PNKQ thêm mới được nối vào).
- Executors: `real_work` từ `wr_import_result_executors`. Costs: `real_price = suggest_price` = giá PNKQ. GVK: `is_completed` từ `wr_import_result_costs` type 2.
- Ảnh thi công/bàn giao: URL từ PNKQ (chỉ hiển thị). Bảo dưỡng (`extend_products`): lấy của **PNKQ** (C:220).
- Edit (C:889-931): `WrAssignTask::getForShow(PDKQ)` — đọc lại bảng con của PDKQ.

### 2.2 Khối hiển thị (V/form.blade.php)
| Khối | Hiện khi | Sửa được (`ng-disabled="show"` = sửa ở create/edit) |
|---|---|---|
| Đầu phiếu: Số PGV, Số PNKQ, Số HĐ/BH/YC lắp đặt/YC GVK, Số HĐ bán, KH, Địa chỉ, Người liên hệ, SĐT | luôn | chỉ đọc |
| Ngày bàn giao `handover_date` | luôn | **sửa, bắt buộc** |
| Người yêu cầu / SĐT | luôn | chỉ đọc |
| Ghi chú `note` | lắp đặt hoặc HĐ | gõ được nhưng **không lưu** |
| Ảnh công trình / bàn giao | luôn | hiển thị từ PNKQ (file đính kèm `attachments` đã comment) |
| A - BẢO HÀNH (V/form:404-579) | `has_warranty` | Đã hoàn thành (+chọn hết), % HT (khoá khi tick), Serial, **CK duyệt `rate_effort_approve_accept`**, Ghi chú; dịch vụ: tick/%/ghi chú; vật tư: **SL**, ghi chú |
| A - DV SỬA CHỮA BẢO DƯỠNG / I SC (581-755) | `has_repair` | như BH |
| II - Thiết bị cần bảo dưỡng (758-908) | (trong khối SC) | Serial, dịch vụ: tick/%/**CK duyệt**/ghi chú; vật tư: tick/%/SL/ghi chú |
| A - Dịch vụ đính kèm (1053-1105) | GVK | CK đề xuất `rate_effort_approve`, **CK duyệt** (cột tick đã comment) |
| A - Hạng mục lắp đặt (1108-1215) | lắp đặt | tick (+chọn hết), %, **SL bàn giao `delivery_qty`**, **CK duyệt**, ghi chú, serial từng dòng `d.serial` |
| B - Công việc phụ P3 (1218-1355) | luôn (2 bản: thường / GVK) | tên việc, tick, (GVK: CK đề xuất), **CK duyệt**, ghi chú; ĐM công chỉ đọc |
| C/D - Tổng công định mức (1360-1397, 1886-1954) | lắp đặt / SC-BH-GVK | chỉ đọc: Công khoán chính + phụ, cột "đề xuất" và "được duyệt" |
| C - Vật tư bán thêm (1841-1885) | HĐ + có hàng | chỉ đọc |
| Tổng hợp dịch vụ trả tiền / vật tư / chi phí IV | — | **comment** (`<!-- -->`, `{{-- --}}`) |
| Ghi chú duyệt / Ghi chú BKS duyệt (1813-1838, 2369-2394) | luôn | gõ được nhưng **không lưu** |
| Popup "Cảnh báo !" `checkProductExportError` (2445-2470) | lỗi `check_product_export` | v-html danh sách lỗi |

### 2.3 Giá trị mặc định + phép tính (JS, đọc cả `after()`)
- `WrApproveResult` extends `WrAssignTaskResult` (V/WrApproveResult.blade.php:14-24): `after()` gán `work_price = company.work_bond`; `no_set` bỏ qua
  `sum_amount_rate_effort, expected_*, work_price, performent_work, work_bond, summary` khi nạp.
- Dòng thiết bị `WrApproveResultProduct` (V/WrApproveResultProduct): tick ⇒ % = 100; % chỉ nhận < 100; `qty == 0` ⇒ không cho tick;
  **CK đề xuất** = `_rate_effort_approve` hoặc `min(round(rate_effort × ceil(delivery/worker) × % / 100, 2), rate_effort × ceil(...))`;
  **CK duyệt** mặc định = CK đề xuất, trần `rate_effort × ceil(delivery/worker)`; `amount_rate_effort_result = CK duyệt × benefit_rate` (benefit 0 ⇒ 1);
  `rate_effort_result` mặc định `rate_effort_approve × benefit_rate`.
- P3 `WrApproveResultP3Work`: CK đề xuất giữ số PNKQ (rỗng ⇒ tick ? ĐM : 0); CK duyệt = 0 nếu chưa tick, tick ⇒ đề xuất (>0) hoặc ĐM; trần ĐM.
- GVK `WrApproveResultRevenueCost`: tick & chưa có ⇒ đề xuất = ĐM. Dịch vụ thiết bị: `_payed_price = outsourcing_price`; status 4 ⇒ `approve_price = payed` (chết).
- `summary.rate_effort` (V/WrApproveResult.blade.php:153-300) — **~45 khoá**, gửi nguyên lên BE và lưu vào cột `summary` (JSON, giá trị là **chuỗi** do FormData):
  `warranty, warranty_approve(Σ CK duyệt BH), repair_approve(Σ CK đề xuất SC), repair_approve_accept(Σ CK duyệt SC), repair_approve_accept_total(+BD),
  assembly_approve / assembly_approve_accept, revenue_cost_approve / _approve_accept, maintain_approve, work_p3_approve / work_p3_approve_accept / work_p3_result(=accept),
  repair_maintain_approve, total_*`…
- BE lấy từ summary: lắp đặt `sum_amount_rate_effort_approve = assembly_approve_accept`, `_result = assembly_result`; còn lại `= repair_maintain_approve`, `_result = repair_maintain_result`;
  `_sub_approve = work_p3_approve`, `_sub_result = work_p3_result` (C:315-327).

---

## 3. Lưu

### 3.1 Validate
- **FormRequest R** (khác `WrImportResultRequest`): `customer_id, customer_contact_name, customer_name, status` required; `handover_date` required `Y-m-d`
  (câu riêng "Bắt buộc phải nhập ngày bàn giao." / "Ngày bàn giao không hợp lệ."); `expected_start_time/end_time` required `Y-m-d`, end ≥ start;
  **`product_export_requests` required**; wildcard bắt buộc cho từng dòng SC/BH/BD/vật tư/dịch vụ/chi phí/hàng bán/P12/P3 (tên, ĐM, CK duyệt…);
  `*.rate_effort_approve` numeric ≥ 0; `assembly.*.rate_effort_approve_accept` required.
- Closure trần: **"Công khoán duyệt không được lớn hơn định mức công"** cho P3 (`rate_effort_approve(_accept)` > ĐM), lắp đặt (accept > `rate_effort × ceil(delivery/worker)`),
  BH/SC/BD/GVK (accept > ĐM).
- Serial SC/BH (closure trên ATP khác PGV cùng HĐ, status DA_DUYET): "Seri đã hoàn thành nhập kết quả, không được nhập tiếp!" / "Bạn cần phải nhập tối đa bằng {x} %";
  tick hoàn thành ⇒ `rate_effort_approve` required. (Như PNKQ: rule `required` serial bị **ghi đè** bằng `nullable` ⇒ serial không thật sự bắt buộc.)
- Serial lắp đặt: trùng SP khác, đã hoàn thành ở PGV khác, vượt % còn lại (câu thiếu "%"), trùng trong danh sách.
- `prepareForValidation` decode 4 mảng chuỗi JSON (`assembly, product_repairs, product_warrantys, extend_products`).
- Trong controller: `checkValidateSerial` (trait chung `app/Http/Traits/SerialValidationTrait.php` — **cùng hàm** HRM đã port ở `WrImportResultValidationService`);
  `hasProductExport` **bản riêng của màn duyệt** (C:2318-2383): ngoài check phiếu xuất/mượn chưa hạch toán còn **check SL bàn giao ≤ SL đã xuất kho HĐ bán − SL đã duyệt ở PNKQ khác**
  ("Số lượng sản phẩm '<b>X</b>' không đủ số lượng để bàn giao") ⇒ trả `{success:false, type:'check_product_export', data:[...]}` → popup Cảnh báo.
  Bỏ qua cứng PGV 1941 / PNKQ 5598 (C:237-239, 943).
- Quyền check SAU 2 bước trên (C:274).

### 3.2 Bảng ghi (store / update)
- `wr_assign_tasks` (PDKQ): fill `wr_service_contract_id, assembly_request_id, assign_other_request_id, customer_*, delivery_place, status, shift_from/to,
  expected_start/end_time, product_export_requests, work_price, performent_work, summary, handover_date`; `parent_id`; `type` = type HĐ | 4 lắp đặt | 5 GVK;
  4 cột `sum_amount_rate_effort_*`; `company_id/department_id` từ người tạo (boot `created`); `approved_by/time`.
  **Mã**: tạm `randomString(20)` → `generateCode('PDKQ')` = `{company.code}.PDKQ.{YYYY}{id 6 số}` (AT:307-312) — VD `TPE.PDKQ.2026014540` (id chung dãy với PGV).
- Bảng con (xoá hết rồi chèn lại — `sync*` AT:1062-1530):
  `wr_assign_task_products` (handle_type 1 BH / 2 SC; cột duyệt `rate_effort_approve, rate_effort_approve_accept, rate_effort_result, benefit_rate, is_completed,
  finish_percent, delivery_qty, worker_qty, serial, serial_id, serial_old, is_serial, note, note_import_result`) + `_product_device_errors` + `_product_items`
  (`model_*` lấy từ products, `delivery_customer_qty` mặc định = qty) + `_product_services` (`approve_price = payed_price`, upload `attachment` S3);
  `wr_assign_task_extend_products` + `_extend_product_services` (CK duyệt) + `_extend_product_service_items`; `wr_assign_task_costs` (`approve_price = suggest_price`);
  `wr_assign_task_revenue_costs`; `wr_assign_task_p3_works` (`rate_effort_approve(_accept)`, `is_completed`); `wr_assign_task_p12_works`;
  `wr_assign_task_assembles` (`serials` JSON + `serial` nối phẩy, CK duyệt); `wr_assign_task_executors`; `wr_assign_task_merchandises` (`unit_name` từ unit).
  Mỗi bảng chỉ sync **khi FE gửi mảng khác rỗng**.
- DB mẫu: HĐ `14578` (3 products, 2 services, 5 costs, 4 executors), BH `14491`, PL `14579`, lắp đặt `14542` (1 assemble, 1 P3), GVK `14582` (1 revenue_cost).
- ATP (C:405-860): lắp đặt — xoá + tạo lại `assign_task_serial_progress`, cập nhật `approver_result_id/qty/detail_id/time_update`, `current_stage = APPROVER_RESULT`,
  tính lại `can_request_qty/delivery_qty`; SC/BH — cập nhật ATP + `itemProgress.qty/approver_result_qty` + `serviceProgress` (`complete_text` JSON);
  BD — ATP + serviceProgress + serviceItemProgress; hàng bán thêm; GVK (`approver_result_qty = 1`, `can_request_qty = 1`).
- Sửa PDKQ: chỉ khi status 3 + người tạo (vào form); xoá: route có nhưng không có nút.

### 3.3 Thông báo
| Sự kiện | Người nhận | Nội dung ERP |
|---|---|---|
| Duyệt HĐ (status 1) | quyền "Kế toán kho" cùng công ty người duyệt | "Bạn có 1 phiếu kết quả giao việc cần hạch toán" → show PDKQ |
| PNKQ lần đầu sang Đã duyệt | người tạo PNKQ (qua HRM `notify-result`, `[PNKQ] Đã duyệt`) | NotificationMeta CONG_VIEC |
| Không duyệt (unApprove) | người tạo PNKQ | ERP: "X vừa không duyệt phiếu nhập kết quả của bạn!" + HRM `notify-result rejected` |

---

## 4. Các nút — xem mục 1.2 (đã đọc `ng-click`: `submitData(3)` / `submitData(2)` / `submitData(1)` / `reject()` → `unApprove`).

## 5. Danh sách `WrApproveResults.index` (chỉ ghi lại — user không muốn màn riêng)
- Nguồn: `WrAssignTask::searchByFilter($r, 'approve_result')` (AT:427-636) `whereNotNull('parent_id')`, loại status 9.
- Lối vào: `?type=all` (menu CSKH › Giao việc "Phiếu duyệt kết quả", topmenubar:1912) — phạm vi theo 3 quyền "Xem phiếu duyệt kết quả theo…" / Kế toán kho (chờ hạch toán cùng cty) /
  mặc định phiếu mình tạo, ẩn phiếu Đang tạo của người khác; `?type=wait_accounting_service` (menu Kế toán "Danh sách kết quả giao việc chờ hạch toán", topmenubar:2322,
  gate "Kế toán kho"): status 1 cùng công ty, **type ≠ 2**; `?type=bks_approve_result` (trang chủ, chết); mặc định = phiếu mình tạo. Trang chủ đếm chờ hạch toán (HomeController:1380).
- 15 cột: STT · Số phiếu duyệt KQ (→ show) · Số PGV · Số HĐ (link theo type) · Số phiếu y/c · KH · Người yêu cầu · Người thực hiện (executor đầu) · Thời gian dự kiến ·
  Tổng công định mức (`summary.rate_effort.total`) · CK duyệt (`approve + sub_approve`) · Người lập · Ngày lập · Ngày duyệt KQ · Trạng thái (APPROVE_STATUSES).
- 9 lọc: số phiếu, số PGV, số HĐ (cả HĐ bán), số phiếu y/c, KH, người yêu cầu, người lập, trạng thái, tên/mã hàng (`product_keyword` qua PNKQ).
- Hành động: Sửa duyệt KQ (canEdit) · BKS duyệt (chết) · Hạch toán dịch vụ (canAccountingService).
- PGV ERP có hành động "Xem phiếu duyệt kết quả" khi PDKQ ≠ Đang tạo (WrAssignTasksController:184-187); HRM PGV hiện trỏ link ERP `wrAssignTaskLinks.js:31`.

## 6. Downstream đọc PDKQ / bảng con
| Nơi đọc | Đọc gì |
|---|---|
| ERP `WrAccountingServicesController` create/store (+ HRM `Modules/Finance/Services/WrAccountingServiceService.php` — đường `wr_approve_result_id` **chưa port**) | PDKQ status 1 → hạch toán → status 2 |
| ERP `WarrantyRepairContractsController::apiGetDataForSettlement` (1144-1390, quyết toán HĐ) | `wr_assign_task_products / extend_product_services / assembles / revenue_costs` của PDKQ + `summary.rate_effort.repair_approve_accept / work_p3_approve / assembly_approve_accept / revenue_cost_approve_accept` |
| **HRM** `Modules/Assign/Services/AssignBusinessService.php:656-860`, `Repositories/PaymentProfileRepository.php:58-81` (đề nghị thanh toán công tác / hồ sơ thanh toán) | `sum_amount_rate_effort_approve` + `summary.rate_effort.work_p3_approve / work_p3_approve_accept / repair_approve_accept_total` của PDKQ (`parent_id`) |
| ERP `ReportInstallDeliveryRepair*` (báo cáo lắp đặt / bàn giao / sửa chữa) | ATP `approver_result_id/qty`, join `wr_assign_tasks` lấy mã/ngày/người PDKQ, link show PDKQ |
| ERP `WrImportResultsController` danh sách PNKQ + **HRM `WrImportResultService` (đã port)** | Người duyệt / Ngày duyệt = `approved_by/approved_time` của PDKQ |
| ERP `HomeController` | đếm chờ hạch toán |
| `HandoverAcceptanceRecord::createFromApproveResult` | gọi đã comment |
| Bước nhập/duyệt PGV sau (validate serial, `can_request_qty`) | ATP / `assign_task_serial_progress` do bước duyệt ghi |

## 7. Lỗi / quirk ERP thấy khi đọc code (hỏi giữ hay sửa)
1. `dd($e)` trong catch store/update/unApprove (C:879, 1596, 2035) → lỗi trả HTML dump, FE chỉ báo "Đã có lỗi xảy ra".
2. Ghi chú / Ghi chú duyệt / Ghi chú BKS **gõ được nhưng không lưu** (mục 0.3).
3. **`update` không check quyền** (bất kỳ ai POST được), chỉ `edit` check.
4. **`update` không cập nhật cột `summary`, `work_price`, `performent_work`** (thiếu trong `only`) → Lưu nháp rồi Duyệt: `summary` JSON giữ số lúc nháp,
   trong khi 4 cột `sum_amount_*` lấy số mới → quyết toán HĐ / thanh toán công tác HRM đọc `summary` có thể lệch.
5. `update` nhánh BH dùng nhầm `$product_repair->services` (C:1405) thay cho `$product_warranty->services` → sai số / lỗi khi PDKQ BH có dịch vụ.
6. store ≠ update ở nhiều chỗ: lắp đặt tính "còn giao" bằng `delivery_qty` (store) vs `qty` (update); store reset ATP sản phẩm không có trong duyệt, update không;
   `can_request_qty` chỉ guard `is_success` ở update; BD store ghi `approver_result_qty/qty` của service, update không; hàng bán thêm store **thiếu `save()`**;
   GVK store không null-guard ATP (crash), update có.
7. `sum_amount_rate_effort_approve` (không lắp đặt) = Σ **CK đề xuất** của SC/BD/GVK nhưng Σ **CK duyệt** của BH → lệch nghĩa giữa các loại.
8. "Duyệt" không có dòng nào hoàn thành ⇒ ép **Đã hạch toán** (bỏ qua kế toán), kể cả HĐ dịch vụ.
9. BH: thông báo Kế toán kho "cần hạch toán" nhưng danh sách chờ hạch toán loại BH → 3 025 phiếu kẹt "Chờ hạch toán".
10. `unApprove` không check quyền, không đổi trạng thái PGV (kẹt 8 nếu đã nháp), không null-guard ATP; `deleteAll()` sót `wr_assign_task_revenue_costs` (mồ côi).
11. Bypass cứng PGV 1941 / PNKQ 5598 ở check phiếu xuất.
12. Không khoá dòng: 2 người cùng bấm Duyệt có thể tạo 2 PDKQ (DB hiện chưa có ca nào).
13. Cấp BKS + refuseToAccount + delete: code có, UI không có / chết.
14. syncProduct sinh serial mới & ngừng serial cũ khi status 1 — side-effect lên danh mục serial KH.

## 8. Đề xuất gộp vào màn PNKQ HRM

### 8.1 Hướng
- **Không tạo menu/danh sách riêng.** Thêm trang con của PNKQ: `pages/customer-care/wr-import-results/_id/approve.vue`
  - Vào từ nút "Duyệt kết quả" (danh sách + chi tiết PNKQ, thay `openApproveResult` mở ERP) khi PNKQ status 2 + `is_can_approve`.
  - Nếu PNKQ status 5 (đã Lưu nháp duyệt) và người xem là người tạo PDKQ → nút "Tiếp tục duyệt" mở cùng trang ở chế độ sửa PDKQ.
  - Chi tiết PNKQ đã duyệt (3): thêm khối/tab "Kết quả duyệt" chỉ đọc (đọc PDKQ) thay link ERP show — tuỳ user chốt.
- **Form:** dựng `WrApproveResultForm.vue` dùng lại khung `WrImportResultForm.vue` (vỏ, khối KH, gallery, `V2Footer`, tab) và các bảng `WrImportResult*Table.vue`
  thêm prop `mode='approve'` để mở cột **CK đề xuất (đọc) + CK duyệt (sửa) + Ghi chú** — vì cột khác ít (khảo sát B §1.4-1.7 đã có cột CK đề xuất). Logic thuần
  `wrApproveResultBuild.js` port `WrApproveResult*` (đặc biệt `summary` 45 khoá — downstream HRM thanh toán công tác + quyết toán ERP đọc).
- **Dữ liệu** ghi y ERP vào `wr_assign_tasks` (`parent_id`) + bảng con PGV → ERP & báo cáo đọc tiếp không cần sửa.

### 8.2 HRM đã có, dùng lại
- Entity `WrAssignTask` + 23 entity con + ATP/serial progress (`Entities/WrAssignTask/*`); `WrImportResult::wr_approve_result()`.
- `WrImportResultService::canApproveResult()` + cờ `is_can_approve`; danh sách đã hiện người duyệt/ngày duyệt; `wait_approve_result`.
- `WrImportResultValidationService::checkValidateSerial()` (cùng trait ERP); `CustomerDeviceListService`.
- `WrImportResultNotifier` (thêm `notifyApproved` thay vì HTTP `notify-result`); `NotificationMeta`.
- FE: `WrImportResultForm.vue`, 9 bảng con, `wrImportResultBuild.js` (đã port `rate_effort_approve` + clamp), `wrImportResultActions.js`, popup `check_product_export`.
- Middleware `checkDueConfigsManager`; quyền "Duyệt phiếu nhập kết quả" (seeder dòng 381), "Kế toán kho" (1257).

### 8.3 Phải làm mới
**BE (`Modules/CustomerCare`)**
1. `WrApproveResultSourceService`: `GET /wr-import-results/{id}/approve-data` (port `getForShowImportResult` + `mapImportResult`) và `GET /wr-approve-results/{pdkqId}/edit-data` (port `getForShow` PDKQ) — ~1 ngày.
2. `WrApproveResultRequest` (port R, giữ câu ERP) + `hasProductExport` bản duyệt — ~0,5 ngày.
3. `WrApproveResultStoreService` store/update: 14 bảng con sync, mã PDKQ, 3 nhánh status (PDKQ/PGV/PNKQ), `syncSerial`, `updateContract`, sinh/ngừng serial (`syncProduct`/`syncAssembly`),
   `updateAssemblyRequest`, ATP 5 nhánh + serial progress, `is_assign`, thông báo Kế toán kho + người tạo PNKQ, lịch sử — **phần nặng nhất ~2,5-3 ngày**.
4. `unApprove` (Không duyệt khi đang nháp duyệt: ATP KHONG_DUYET + xoá PDKQ) — dùng chung nút "Không duyệt" — ~0,5 ngày.
5. Route + middleware + quyền; smoke 5 loại (HĐ SC, BH, PL, lắp đặt, GVK) trong transaction/rollback, so số dòng với PDKQ ERP mẫu — ~1 ngày.

**FE**
1. `_id/approve.vue` (+ chế độ sửa nháp) + `WrApproveResultForm.vue` + bật cột duyệt ở 6 bảng — ~2,5 ngày.
2. `wrApproveResultBuild.js` (CK đề xuất/CK duyệt/trần, chọn hết, summary 45 khoá, ép status, payload) + test node trên dữ liệu thật — ~1,5 ngày.
3. Nút Lưu / Duyệt / Không duyệt + popup xác nhận "Phiếu không hoàn thành công việc…", popup Cảnh báo, cảnh báo chưa lưu; nối danh sách/chi tiết PNKQ; khối "Kết quả duyệt" ở chi tiết — ~1 ngày.

**Tổng ước lượng: BE ~5,5-6 ngày, FE ~5 ngày, verify ~1-1,5 ngày ⇒ ~11-12 ngày công.**

## 9. Câu hỏi cần user chốt
1. **Lỗi ERP giữ hay sửa?** (A) giữ y hệt như PNKQ đã chốt · (B) sửa nhóm "chắc chắn sai": update không check quyền (#3), `summary` không cập nhật khi sửa (#4),
   biến nhầm BH (#5), `dd($e)` (#1), unApprove không check quyền (#10). → **Khuyến nghị B** (sai dữ liệu ảnh hưởng quyết toán + thanh toán công tác), còn lại giữ.
2. **Ghi chú duyệt / Ghi chú / Ghi chú BKS** (không lưu ở ERP): (A) bỏ khỏi form · (B) hiện như ERP nhưng không lưu · (C) lưu `approve_comment` vào PNKQ.
   → **Khuyến nghị A** (không thêm cột; "Ghi chú duyệt" đã có ở PNKQ khi Không duyệt).
3. **Lưu nháp duyệt** (status 3): (A) giữ nút Lưu + "Tiếp tục duyệt" (chỉ người lưu) · (B) bỏ, chỉ Duyệt/Không duyệt một lần. → **A** (giữ nghiệp vụ; DB có ca thật).
4. **Không duyệt trong form duyệt**: (A) dùng `unApprove` y ERP (xoá PDKQ nháp, không check quyền) · (B) dùng `reject` HRM đã có + bổ sung xoá PDKQ nháp khi PNKQ status 5. → **B**.
5. **Cấp BKS + Kế toán kho trả về + Xoá PDKQ** (chết ở ERP): bỏ không port? → **Khuyến nghị bỏ**.
6. **Xem PDKQ sau khi duyệt**: (A) khối/tab "Kết quả duyệt" chỉ đọc trong chi tiết PNKQ · (B) link ERP show. → **A** (chỉ đọc, dùng lại form ở mode show).
7. **Danh sách "Phiếu duyệt kết quả" (`type=all`) + "Kết quả giao việc chờ hạch toán" (Kế toán kho)**: không màn riêng thì Kế toán kho tìm phiếu chờ hạch toán ở đâu?
   (A) để ERP · (B) thêm lọc "Trạng thái duyệt" vào danh sách PNKQ · (C) làm khi port Hạch toán dịch vụ. → **A + C** (đường hạch toán `wr_approve_result_id` HRM đang hoãn).
8. **Ép "Đã hạch toán" khi không có dòng hoàn thành** + BH kẹt "Chờ hạch toán": giữ y ERP? → **Giữ** (đổi là đổi luồng kế toán).
9. **Sinh/ngừng serial khi Duyệt HĐ** (side-effect danh mục serial): giữ y ERP? → **Giữ** (ERP + màn serial đọc).
10. **Thông báo**: Kế toán kho dùng `[PDKQ]`/`[PNKQ] Chờ hạch toán` theo skill notification-convention, người tạo PNKQ `[PNKQ] Đã duyệt` gọi thẳng notifier (không qua HTTP)? → **Đồng ý**.
11. Nhãn nút: "Lưu" / "Duyệt" / "Không duyệt" như ERP (button-convention) — đồng ý?
