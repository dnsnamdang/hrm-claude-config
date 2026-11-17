# Phủ hết màn duyệt — Công việc, phần C (bàn giao, loại giảm giá, điều chỉnh giải pháp + kiểm kê phần còn lại) — @cuong61n

17/11/2026. Đường dẫn tính từ `hrm-api/`. Definition: `Modules/ApprovalCenter/Definitions/Assign/`; test: `tests/Feature/ApprovalCenter/Assign/`. Manifest dọn thử: `wave2-assign-C.json` (đã `clean-test`, sạch).

## 1. Loại MỚI đăng ký (3)

| doc_type | Màn gốc (FE) | Cấp | Gate | Pending local thật | verify (cặp / chênh) | Đột biến bị bắt | Trạng thái |
|---|---|---|---|---|---|---|---|
| `solution_adjustment_request` | `/assign/prospective-projects/{id}/manager` › Giải pháp › Yêu cầu điều chỉnh GP (màn không đọc query để mở sẵn tab) | 1 (status 1 "Đã gửi" → Tiếp nhận / Từ chối) | **BE không chốt quyền** — giao diện: `solution.pm_id`==tôi ∨ `receive_dept` của YC làm GP ∈ `listManageDepartmentIdsWithOwn()` (quản lý chặt ở công ty đang làm ∪ phòng mình), KHÔNG mã quyền | 0 | 2400 / 0 (test 8400 cặp, 716 dương) | 5/5 | xong |
| `handover_item` | `/assign/handover/receiving` → `/assign/handover/{handover_id}/receive` | 1 (mục `receive_status`=0, phiếu cha `status`=3) | `receiver_id`==tôi (BE CÓ kiểm: `HandoverService::acceptItem/rejectItem`), không quyền/công ty | 2 (mục 6, 7 của phiếu BG.2026.0001) | 5600 / 0 (test 1680 cặp, 70 dương) | 5/5 | xong |
| `discount_type` | `/assign/discount-types` (menu "…" dòng › Duyệt) | 1 (status 3 "Chờ duyệt"; chỉ có Duyệt, không có Từ chối) | mã `assign.danh_muc_loai_giam_gia.manage` (route + nút) ∧ `isCanApprove()`; không công ty/phòng | 1 | 3290 / 0 (test 810 cặp, 210 dương) | 5/5 (thêm test gỡ mã danh mục khác để đột biến "nhầm mã" lộ ra) | xong |

Đơn vị phiếu của `handover_item` là MỘT MỤC (1 phiếu bàn giao nhiều mục, mỗi mục 1 người nhận, nhận/từ chối từng mục); người duyệt gán cho mọi công ty (code không kiểm công ty).

## 2. File đã tạo / sửa
- Mới: `SolutionAdjustmentRequestDefinition.php`, `HandoverItemDefinition.php`, `DiscountTypeDefinition.php` + 3 test cùng tên `*Test.php`.
- Model: `SolutionAdjustmentRequest`, `HandoverItem`, `DiscountType` (thêm trait `SyncsApprovalInbox` + `approvalInboxDocType()`); `Handover` (thêm `boot()`: khi phiếu cha đổi trạng thái/mới tạo thì `scheduleSync('handover_item', từng mục)` — mục chỉ vào hàng chờ khi phiếu cha = Đã duyệt; đã chạy thật ngoài giao dịch: phiếu chờ → null, duyệt → state 1, tiếp nhận → 2, phiếu cha từ chối → 5).
- Chỗ ghi bằng query builder: không có làm đổi trạng thái chờ (`HandoverService.php:804,1304` `items()->delete()` chỉ ở phiếu nháp/chưa duyệt, không có mục nào trong hàng chờ; `scheduleSync` tường minh không cần).
- Không chạy migration. Không đụng `AssignApprovalSupport.php`.

## 3. Kiểm kê phần còn lại của module Assign (mục 5 của giao việc)

| Luồng | Màn FE | Kết luận | Bằng chứng |
|---|---|---|---|
| Biên bản bàn giao nghiệm thu | `/assign/handover-acceptance-records` | BỎ | Không có route/nút duyệt: `Modules/CustomerCare/Routes/api.php:441-458` chỉ index/store/update/destroy; "Đã duyệt" (status 2) là trạng thái người lập tự chọn khi lưu (`handoverActions.js:15-16`, `handoverBuild.js:214` — cần quyền Tạo, kiểm ở `store/update`) ⇒ tự duyệt, không có bước chờ người khác |
| Biên bản bàn giao sơ bộ `handover-records` (`HandoverRecordController::approve`) | `/customer-care/handover-records` | Thuộc nhóm CSKH (FE pages/customer-care); plan.md ghi đã bỏ vì BE không kiểm người duyệt — **cần điều phối xác nhận lại theo phụ lục mới** (route `CustomerCare/Routes/api.php:495`; chưa có Definition ở `Definitions/CustomerCare`) |
| Phiếu YC giao việc khác `AssignOtherRequestController::reject` | `/customer-care/assign-other-requests` | Thuộc nhóm CSKH (`CustomerCare/Routes/api.php:475`), chưa có Definition — chuyển điều phối |
| BOM list `STATUS_CHO_DUYET=3` | `/assign/bom-list` | BỎ | Không có route duyệt trong `Routes/api.php:564+` (nhóm `/assign/bom-lists`); trạng thái chỉ do `BomListService::syncStatusFromSubmission` (`:427-489`) đổi theo kết quả Hồ sơ trình duyệt (đã đăng ký `solution_review_profile`) |
| Yêu cầu XD giá `pricing-requests` | `/assign/pricing-requests` | BỎ | `Routes/api.php:587-596` chỉ có `send`; FE `_id/index.vue` không có nút Duyệt/Từ chối |
| Báo giá tổng hợp | `/assign/summary-quotations` | Đã đăng ký (`summary_quotation`) | — |
| `my-todo` / `my-job` | tổng hợp | BỎ | Chỉ gom cờ `can_approve` của các luồng đã đăng ký, không là luồng riêng (`work-item-types.js`) |
| Meeting — xác nhận tham dự | `/assign/meeting` | BỎ (xin user chốt) | Phản hồi lời mời tự phục vụ của chính người được mời: `Modules/Assign/Routes/Meeting/api.php` route `attendance-confirm`, chú thích "thao tác tự phục vụ của chính người trong cuộc họp"; không có bước Duyệt/Từ chối của người khác phiếu họp |
| Duyệt bình luận task | — | BỎ | `Routes/api.php:1216` route `comments/{id}/approve`, không có nơi nào trong `hrm-client` gọi; mặc định comment `approved=1` |
| `waiting-assign-tasks` reject-reception (PL bổ sung) | `/customer-care/waiting-assign-tasks` | Thuộc nhóm CSKH (C5) — FE `pages/customer-care/...WaitingAssignTaskList.vue:636-637`; plan.md 22/10 đã loại nhóm "chờ giao việc" |
| `job_request` status 3 "Chờ giao việc" | `/assign/job_requests` | GIỮ NGUYÊN `JobRequestDefinition` | `deny` chỉ cho `canApprove()` (status 2) `JobRequestController.php:299-309`; status 3 chỉ có "Giao đi công tác / Giao việc" = lập chứng từ kế tiếp (`job_requests/index.vue:189-206`), không có Duyệt/Từ chối |
| Yêu cầu lắp đặt bàn giao | menu "Phiếu yêu cầu lắp đặt, bàn giao chờ duyệt" không có link (`components/menu-sidebar.js` nhóm "Bàn giao - Lắp đặt") | BỎ | HRM chỉ có tab hàng đợi + in: `Routes/api.php:1320-1327`; `TpAssemblyRequest` không có hàm/route duyệt; duyệt chỉ ở ERP |
| YC xuất hàng `ProductExportRequest`: reject / switch-board-of-manager / manager-approve | `/finance/product-export-requests` | **THIẾU — thuộc nhóm Tài chính/Kho** | `Routes/api.php:794-801`; `Definitions/Finance` chưa có `product_export_request` |
| Đề nghị xuất kho `WarehouseExportRequest` (cancel) / Phiếu xuất `WarehouseExport::deny` | `/finance/...` | **THIẾU — Tài chính/Kho** | `Routes/api.php:846,886-887` (`checkPermission:accounting.ke_toan_kho.manage`; status `CHO_DUYET=2`) — chưa có Definition |
| Biên bản hạch toán / các mục còn lại | — | Không có | Không route duyệt nào khác trong `Modules/Assign/Routes/**` |

## 4. Loại "BE không chốt quyền" cần chuyển người phụ trách module
- `solution_adjustment_request`: `SolutionAdjustmentRequestController::accept/reject` + service (`SolutionAdjustmentRequestService.php:52-79`) không kiểm quyền, không kiểm trạng thái (duyệt lại phiếu đã xử lý được); route `Routes/api.php:438-439` không middleware. Definition bám cờ Entity `is_can_accept/is_can_reject` (`SolutionAdjustmentRequest.php`, `isCurrentUserTPOrPM`) — không kiểm mã quyền.

## 5. Lưu ý / quyết định cần user
- `handover_item`: người bàn giao tự đặt mình làm người nhận vẫn tiếp nhận được (code không chặn) — giữ `excludeOwn()=false`.
- `solution_adjustment_request`: `watchedTables()` chỉ nghe bảng quản lý phòng / hồ sơ nhân viên / phòng; đổi `solutions.pm_id` hoặc `request_solutions.receive_dept` của phiếu đang chờ không tự sync (không nghe 2 bảng ghi thường xuyên) — lưới an toàn backfill 15 phút vớt.
- `handler_path` của điều chỉnh giải pháp chỉ mở màn dự án; user phải bấm tab Giải pháp › Yêu cầu điều chỉnh GP (màn chưa đọc query tab).
- Meeting xác nhận tham dự đang tính là BỎ — nếu user coi là "Xác nhận" thì cần giao thêm.
