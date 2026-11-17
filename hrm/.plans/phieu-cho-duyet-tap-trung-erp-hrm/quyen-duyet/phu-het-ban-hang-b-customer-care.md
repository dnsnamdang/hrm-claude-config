# Phủ hết màn duyệt — CSKH sau bán (Modules/CustomerCare) — @cuong61n

Ngày 17/11/2026, fork B của nhóm Bán hàng / CSKH / Vận chuyển / Danh mục. Đối chiếu code `hrm-api` nhánh `gop_db-main`, DB local `local_hrm_erp`. Manifest dọn dữ liệu thử: `wave2-sale-b.json`. Không migrate (không cần: nhóm này không phụ thuộc `form_version`). Không Playwright.

## 1. Bảng kiểm kê luồng CSKH

| Luồng | Màn FE | doc_type | Trạng thái |
|---|---|---|---|
| HĐ dịch vụ — Chờ duyệt (cấp 1) | `/customer-care/wr-service-contracts/{id}` | `wr_service_contract` (đợt 1) | Giữ nguyên |
| HĐ dịch vụ — **Chờ tiếp nhận xử lý** (cấp 2: Từ chối tiếp nhận) | chi tiết HĐ + `/customer-care/waiting-assign-tasks` tab Hợp đồng | `wr_service_contract` **version 2** | MỚI |
| Phụ lục BỔ SUNG HĐ (type 3) — Từ chối tiếp nhận | `/customer-care/waiting-assign-tasks?tab=addition_annex` | `wr_service_annex` | MỚI |
| Phiếu nhập kết quả CSKH (cấp 1, 2) | `/customer-care/wr-import-results/{id}/approve` | `wr_import_result` (đợt 1) | Đã kiểm lại: reject và approve cùng cổng (`WrImportResultService.php:574-630`), không thiếu cấp |
| Yêu cầu đi kiểm tra SC-BH (Từ chối / Chuyển phòng của phòng tiếp nhận) | `/customer-care/warranty-repair-requests/{id}` | `warranty_repair_request` | MỚI |
| Phiếu xử lý yêu cầu "Chờ CCTT" (Không duyệt) | `/customer-care/warranty-repair-handle-requests/{id}` | `warranty_repair_handle_request` | MỚI |
| Phiếu cung cấp thông tin "Chờ làm báo giá" (Từ chối tiếp nhận) | `/customer-care/wr-information-requests/{id}` | `wr_service_quotation` | MỚI |
| Yêu cầu giao việc khác "Chờ giao việc" (Từ chối) | `/customer-care/assign-other-requests/{id}` | `assign_other_request` | MỚI |
| Biên bản bàn giao sơ bộ | `/customer-care/handover-records/{id}` | — | **DỪNG, cần user chốt** (mục 4) |
| Phụ lục (type 3/4) — cấp "Chờ duyệt" / duyệt phụ lục | (không có) | — | BỎ: `WrServiceContractController.php:472-475` (`contractOrFail` ép `type = 1`), được `approve`/`reject`/`unApprove`/`changeReception`/`rejectReception` dùng (:333, :348, :372, :419, :447); `show` cũng ép type 1 (:316) ⇒ duyệt phụ lục chỉ trên ERP |
| Phụ lục GIẢM (type 4) | — | — | BỎ: không có route nào của HRM tác động; tab `addition_annex` chỉ `type = 3` (`WaitingAssignTaskService.php:248`) |
| Báo giá dịch vụ (`wr_service_quotations` type 1) | `/customer-care/wr-quotations` | — | BỎ: chỉ có "Lưu và duyệt" của chính người lập (`WrServiceQuotation.php:84-86` `STATUS_QT_APPROVED` tự duyệt); `Routes/api.php` nhóm `/wr-quotations` không có route duyệt / từ chối |
| Phiếu bảo hành (`wr_service_contracts` type 2) | `/customer-care/wr-warranties` | — | BỎ: màn CHỈ ĐỌC (`Routes/api.php:347-355`); tab "Phiếu bảo hành" của Phiếu chờ giao việc chỉ có "Tạo phiếu giao việc" (`WaitingAssignTaskService.php:522`) |
| Tab Lắp đặt bàn giao / Giao việc khác của Phiếu chờ giao việc | `/customer-care/waiting-assign-tasks` | — | BỎ riêng tab (hàng đợi tạo PGV, nút chỉ `assign` — `WaitingAssignTaskList.vue:552-553` `default: return [assign]`); Từ chối của phiếu giao việc khác nằm ở màn riêng ⇒ `assign_other_request` |
| Phiếu giao việc CSKH (`wr_assign_tasks`) | `/customer-care/wr-assign-tasks` | — | BỎ: không có route duyệt / từ chối (`Routes/api.php:389-403` chỉ đọc / tạo / xoá) |
| Biên bản bàn giao nghiệm thu | `/assign/handover-acceptance-records` | — | BỎ: "Lưu và duyệt" của chính người lập (`HandoverAcceptanceRecordForm.vue:538-549`, `HandoverAcceptanceRecordService.php:341-349` canEdit = người tạo), không có route duyệt (`Routes/api.php:441-456`) |

## 2. Cách tính người duyệt từng loại mới

Cổng chung trong code gốc: mã quyền tính ở **công ty đang làm**; phòng ngồi = `employee_infos.department_id`; công ty "gốc" = `employee_infos.company_id`. Mọi loại dưới không xét công ty phiếu để cho phép duyệt ⇒ người duyệt gắn với MỌI công ty (hoặc đúng công ty đang làm có mã).

- **`warranty_repair_request`** — status 2 "Chờ xử lý" + chưa có phiếu xử lý. Người duyệt: giữ `customer_care.yeu_cau_di_kiem_tra_sua_chua_bao_hanh.confirm` ở công ty đang làm + phòng ngồi = `department_reception_id`. `truth` = `canReject()` (= `canTransferDepartmentReception()` = `canHandleRequest()`). "Chuyển phòng" giữ nguyên trạng thái (chỉ đổi danh sách người duyệt, không mở vòng mới). Model `WarrantyRepairHandleRequest` thêm hook đồng bộ lại phiếu gốc khi thêm / xoá phiếu xử lý.
- **`warranty_repair_handle_request`** — status 2 "Chờ CCTT". Người duyệt: giữ `customer_care.phieu_cung_cap_thong_tin.create` + MỞ ĐƯỢC chi tiết (canView: người lập · mã xem phạm vi Tổng công ty · Công ty = công ty GỐC · Phòng ban ∈ phòng quản lý ∪ phòng ngồi). `truth` = `canView() && canReject()`. BE endpoint reject KHÔNG kiểm canView (xem mục 5).
- **`wr_service_quotation`** (type 0, status 2) — người duyệt = người lập PHIẾU YÊU CẦU GỐC (`warranty_repair_requests.created_by`), mọi công ty; chỉ khi phiếu có phần sửa chữa và mỗi thiết bị ≤ 1 lỗi, ngược lại `approvable = false` kèm lý do. `truth` = `canReject()` (nạp bản ghi mới mỗi lần vì entity đệm kết quả theo người đầu tiên).
- **`assign_other_request`** — status 1 "Chờ giao việc". Người duyệt: người NGỒI đúng `department_reception_id` (không mã quyền, mọi công ty). `truth` = `AssignOtherRequestService::canAssignTask`. Các chỗ ghi bằng query builder đã gọi `scheduleSync`.
- **`wr_service_contract` cấp 2** — status 3 + `department_reception_id` + chưa có phiếu giao việc (không tính Hủy). Người duyệt: mã `customer_care.phieu_giao_viec.create` + phòng ngồi = phòng tiếp nhận + vào được nút qua ≥ 1 cửa: (a) canView hợp đồng; (b) có dòng trong "Phiếu chờ giao việc" tab Hợp đồng (còn số lượng để giao + quyền xem tổng công ty hoặc quản lý phòng tiếp nhận). `truth` = `(is_can_reject_reception && canView()) || cờ của dòng trong query thật của màn Phiếu chờ giao việc`.
- **`wr_service_annex`** (type 3) — như cấp 2 của hợp đồng nhưng chỉ cửa (b) (HRM không có màn chi tiết phụ lục). `truth` = cờ `is_can_reject_reception` của dòng trong query thật `WaitingAssignTaskService` tab `addition_annex`.

## 3. Kết quả kiểm chứng

(Xem bảng trong báo cáo cuối của fork; số liệu phpunit nằm ở `tests/Feature/ApprovalCenter/CustomerCare/*`.)

## 4. Biên bản bàn giao sơ bộ — vì sao dừng

`HandoverRecordController::approve` (`:191`) → `HandoverRecordService::approve` (`:489`) KHÔNG kiểm người duyệt; `canApprove` chỉ xét `status = 2` (`HandoverRecordService.php:185-188`). Phạm vi danh sách = TẤT CẢ biên bản (`filteredQuery` `:102-128`, comment "ai cũng thấy mọi biên bản"). Route không có `checkPermission` (`Routes/api.php:481-496`). Menu không `isShow` / `codes` (`customer-care.js:146`). Cờ `is_can_approve` chỉ theo trạng thái ⇒ MÀN KHÔNG CÓ BẤT KỲ GATE NÀO (phụ lục: dừng và báo). Bảng `handover_records` hiện rỗng (0 phiếu) trên DB local. Cột `approver_id` (NOT NULL, bắt buộc chọn ở form, nhận thông báo "Chờ duyệt" — `HandoverRecordNotifier.php:29`) chỉ để gửi thông báo.

Đề xuất để user chốt: (A) coi `approver_id` là người duyệt đích danh và siết BE (mặc định đề xuất — khớp ý định "Người duyệt" trên form, hiện BE cho mọi người duyệt); (B) giữ y ERP, đăng ký người duyệt = mọi nhân viên có hồ sơ × mọi công ty (~1.3k × 10 dòng / phiếu — nặng và vô nghĩa); (C) không đưa vào Trung tâm phê duyệt. Chưa viết Definition cho loại này.

## 5. Lỗi / điều cần người phụ trách module biết (không sửa)

- **BE không chốt quyền — người duyệt lấy theo điều kiện giao diện**: `warranty_repair_handle_request` (reject không kiểm canView), `wr_service_contract` cấp 2 và `wr_service_annex` (reject-reception không kiểm phạm vi xem; phạm vi nằm ở danh sách), `assign_other_request` (gate bằng phòng ngồi chứ không có mã quyền), `wr_service_quotation` (gate bằng người lập phiếu yêu cầu, không mã quyền), biên bản bàn giao sơ bộ (không gate).
- `WrServiceQuotation::canCreateQuotation()` nhớ kết quả trong chính bản ghi (`$canCreateQuotationCache`): dùng lại cùng 1 object cho nhiều người đăng nhập ra kết quả sai — Definition phải nạp bản mới.
- `WaitingAssignTaskService::applyReceptionScope` / `viewer()` lấy phòng quản lý ở MỌI công ty (ERP không lọc công ty), còn `WrServiceContract::canView` lấy phòng quản lý ở công ty gốc ⇒ hai cửa của cùng 1 nút khác phạm vi.
- Phụ lục bổ sung: nút "Từ chối tiếp nhận" không kiểm "chưa có phiếu giao việc" (khác hợp đồng) — đúng ERP.
- `WrAssignTaskStoreService.php:765` / `WrAssignTaskService.php:896`, `WaitingAssignTaskService.php:180` ghi trạng thái bằng query builder (đã gọi `scheduleSync`).
- Hiệu năng: `assign_other_request` — 798 phiếu × ~1.250 dòng người duyệt = ~1 triệu dòng `approval_inbox_assignees` (phòng 51 có 134 người × 10 công ty). Nạp 34 giây. Đề xuất nếu cần giảm: chỉ gắn công ty mà nhân viên thực sự làm việc được (`company_employees` ∪ công ty gốc) — nhưng lệnh `approval-inbox:verify` quét mọi cặp (nhân viên × công ty) sẽ báo chênh lệch giả ở cặp không có thật.
- Hiệu năng: `wr_service_quotation` 3.760 phiếu (3.599 `approvable = false` vì không có phần sửa chữa / thiết bị nhiều lỗi); nạp 14 giây.
