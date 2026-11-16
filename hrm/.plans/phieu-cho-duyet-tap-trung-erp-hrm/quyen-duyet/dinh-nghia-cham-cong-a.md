# Định nghĩa loại phiếu — Chấm công nhóm A (Trung tâm phê duyệt) — @cuong61n

> 16/11/2026, nhánh `hrm-api` = `gop_db-main`. Thư mục Definition: `hrm-api/Modules/ApprovalCenter/Definitions/Timesheet/` (+ `Concerns/ResolvesTimesheetApprovers.php` dùng chung, không phải Definition). Test: `hrm-api/tests/Feature/ApprovalCenter/Timesheet/` (+ `Concerns/GroupAFixtures.php`).

## Bảng tóm tắt

| doc_type | Màn gốc (menu Phê duyệt) | Cấp | Gate | handler_path |
|---|---|---|---|---|
| `attendances_extend_request` | Đơn kết thúc nghỉ phép (`/timesheet/attendance/attendances-extend-request`) | 1 (status 1) | mã `timesheet.don_xin_nghi.approve` + quản lý phòng HIỆN TẠI của người TẠO phiếu + `phiếu.company_id` = công ty đang làm (xem mục 1) | màn danh sách (không có màn chi tiết theo id) |
| `late_early_out` | Đăng ký đi muộn về sớm | 1 (status 1) | mã `timesheet.dang_ky_di_muon_ve_som.approve` + quản lý người đăng ký (`employee_id`); KHÔNG hạn ngày | `/timesheet/late-in-early-out/{id}/approve` |
| `late_early_out_change_end_request` | Đơn kết thúc đăng ký đi muộn về sớm | 1 (status 1) | cùng mã trên + `phiếu.department_id` nằm trong phòng mình quản lý + `phiếu.company_id` = công ty đang làm (xem mục 1) | `/timesheet/late-in-early-out/change-end-request` (danh sách) |
| `overtime_assignment` | Đăng ký làm thêm (gồm Phân công làm thêm) | 1 (status 1) | mã `timesheet.dang_ky_lam_them.approve` + (loại 0: quản lý `employee_id`; loại 1: quản lý `department_id` của phiếu); hạn = hết ngày `overtime_start_at` | `/timesheet/overtime-assignment/{id}/approve` |
| `overtime_requirement` | Phiếu yêu cầu làm thêm | 1 (status 1) | mã `timesheet.phieu_yeu_cau_lam_them.approve` + quản lý `department_id` = Đơn vị thực hiện (không phải `requirement_department_id`); hạn = hết ngày `start_at` | `/timesheet/overtime-requirement/{id}/approve` |
| `request_update_timesheet` | Đề nghị tra soát công | 1 (status 1 "Gửi TP duyệt") / 2 (status 4 "Chờ NSHC duyệt") | cấp 1: `…de_nghi_tra_soat_cong.confirm`; cấp 2: `…approve`; cả hai: `phiếu.company_id` = công ty đang làm + quản lý người đề nghị | `/timesheet/request-update-working/{id}/approve` |

Màu badge: entity các loại này KHÔNG có accessor `status_color` → Definition tự map 9 mã chuẩn (cùng bảng Attendance: 1/4 `#D97706`, 2 `#16A34A`, 3/5 `#DC2626`). Chữ lấy từ accessor BE của phiếu.

## 1. Chỗ phải quyết định: truth() của 2 loại "phẳng"

`AttendancesExtendRequest::can_approve` chỉ xét `status=1 ∧ mã don_xin_nghi.approve`; `LateInEarlyOutChangeEndRequest::can_approve` chỉ xét `status=CHO_DUYET ∧ mã dang_ky_di_muon_ve_som.approve`. Cờ KHÔNG xét công ty / quản lý. Nhưng nút Duyệt chỉ hiện ở màn danh sách (`*Service::index`) vốn lọc: `company_id = công ty đang làm` VÀ phòng (người tạo / `department_id` phiếu) ∈ `listManageDepartmentIds()`. Nếu `truth()` chỉ = cờ thô thì mọi người giữ mã ở MỌI công ty đều "duyệt được" mọi phiếu → bảng gom phình ra vô nghĩa và không khớp màn gốc. Đã chọn: `truth()` = cờ `can_approve` **VÀ** phạm vi màn danh sách (override trong 2 Definition, có docblock). **Cần điều phối viên xác nhận** — nếu muốn bám cờ thô thì phải đổi `approvers()` thành "mọi người giữ mã ở mọi công ty".

## 2. Điểm đáng chú ý từng loại

- **Đi muộn về sớm**: không còn hạn ngày (`&& $isEditStatus` bị comment) — 33 phiếu "Gửi duyệt" cũ vẫn còn người duyệt. Từ chối phiếu Đã duyệt còn hiệu lực là `can_reject`, không phải bước chờ → không vào bảng gom.
- **Làm thêm**: phiếu Phân công (loại 1) thường `employee_id` NULL (một số phiếu cũ vẫn có `employee_id`, bị bỏ qua vì code xét phòng). `requester_id` = người lập (`created_by`) cho loại 1; loại 0 = người đăng ký (`employee_id`→`employees.id`), không có thì người lập. Trần giờ OT/tháng (422 lúc bấm) ghi ở `gate_blocker`, không loại phiếu. Phiếu quá hạn (start < hôm nay): vẫn "Gửi duyệt" nhưng `approvable_until` đã qua nên không ai thấy trong "Chờ tôi duyệt" (local: 178 pending, chỉ 5 phiếu còn người duyệt).
- **Phiếu yêu cầu làm thêm**: quyền xét `department_id` (đơn vị thực hiện), có test dựng 2 chiều lệch với `requirement_department_id`.
- **Tra soát công**: người giữ cả `confirm` + `approve` duyệt phiếu cấp 1 → nhảy thẳng Đã duyệt (`RequestUpdateTimeSheetService::storeApprove:267-279`). Họ vẫn là người duyệt cấp 1 đúng (can_approve); bảng gom ghi phiếu rời chờ thành Đã duyệt không qua cấp 2 (có test `test_nguoi_giu_ca_hai_ma_duyet_nhay_cap_thang_sang_da_duyet`). Trạng thái 5 "TP từ chối" và 3 "Từ chối" đều → REJECTED.
- "Là quản lý" dùng đúng `ApproveScope` (cờ tất cả phòng ban 2 nguồn, phòng HIỆN TẠI, nhân viên đã nghỉ chỉ thấy qua cờ tất cả phòng ban; phòng: cờ → mọi phòng có `departments.company_id` = c, người có cờ thì BỎ QUA dòng theo phòng).

## 3. Ghi bằng query builder / chỗ không qua Eloquent

Đã rà `Modules/` + `app/`: KHÔNG có chỗ nào của 6 bảng ghi trạng thái bằng `DB::table()` / `->update()` trong code nghiệp vụ (mọi đường tạo/duyệt đi qua `->save()` / `::create()` của Service/Controller). Nên chỉ gắn trait `SyncsApprovalInbox` lên 6 model. Còn lại: `CompanyRepairTimesheets` (lệnh sửa dữ liệu) chỉ đọc tên bảng `overtime_assignments`; `Modules/Agent` chỉ đọc/lọc. Lệnh `approval-inbox:backfill` là lưới an toàn cho ERP ghi thẳng DB.

## 4. Lỗi / lệch của code gốc (chỉ ghi nhận, không sửa)

1. **Kết thúc nghỉ phép**: BE KHÔNG chốt endpoint duyệt (`POST /timesheet/attendances-extend-requests/{id}` → `AttendancesExtendRequestService::save` ghi thẳng `attendance_end_at` mới vào đơn nghỉ gốc, không kiểm quyền/trạng thái/quản lý) — ai đăng nhập cũng duyệt/ghi đè được. Nhánh NSHC trong `index` là closure rỗng.
2. **Đăng ký làm thêm**: thông báo "chờ duyệt" gửi cho quản lý phòng của NGƯỜI TẠO (không phải phòng của nhân viên trong phiếu); phiếu Phân công `employee_id` NULL không nằm trong danh sách `/overtime-assignment/approve` (chỉ thấy qua màn Phân công làm thêm) — bảng gom đưa được thẳng tới `/overtime-assignment/{id}/approve`.
3. **Phiếu yêu cầu làm thêm**: thông báo gửi người giữ `dang_ky_lam_them.approve` trong khi người duyệt thật giữ `phieu_yeu_cau_lam_them.approve`.
4. **Tra soát công**: sau khi TP duyệt cấp 1, thông báo NSHC tính theo phòng của TP (người vừa duyệt) chứ không phải phòng người đề nghị.
5. `AttendancesExtendRequest::can_approve`: `$isNotTP` luôn true vì model không có thuộc tính `employee_id` (code chết).
6. Các `isNotTP` ở Đi muộn về sớm cũng thừa (luôn true khi đã có mã).

## 5. Dữ liệu local (DB `local_hrm_erp`, sau khi dọn phiếu thử)

Pending thật: `attendances_extend_request` 1 · `late_early_out` 33 · `late_early_out_change_end_request` 0 (bảng có 1 dòng, đã duyệt) · `overtime_assignment` 178 · `overtime_requirement` 115 · `request_update_timesheet` 76 (57 cấp 1 + 19 cấp 2).

## 6. Kiểm chứng

- `approval-inbox:verify` (kèm phiếu thử, 8/loại): 0 chênh lệch cả 6 loại. Cặp so / cặp được duyệt thật (sample 40): extend 4.689/59 · late 21.361/351 · change-end 4.168/58 · overtime_assignment 96.906/22 · overtime_requirement 64.083/20 · request_update 43.176/539. (Số cặp thật của 2 loại làm thêm thấp vì phần lớn phiếu trong DB đã quá hạn; phép so trong test dựng phiếu còn hạn: 415 / 311 cặp thật.)
- PHPUnit `tests/Feature/ApprovalCenter/Timesheet`: 49 test xanh (chạy 3 lần ổn định). Test ghi cứng mã quyền (không lấy từ Definition) để bắt tra nhầm mã; `GroupAFixtures::revokePermissionInCompany` phải `PermissionChecker::flush()` (đệm tĩnh) — bài học: nếu quên thì verify báo giả "can_approve=true".
- Đột biến (cố ý làm sai Definition/trait → test phải đỏ): extend 8/8, late 7/7, change-end 8/8, assignment 9/9, requirement 9/9, request_update 8/8. Các ca ban đầu SỐNG sót rồi đã bổ sung test: đổi mã quyền sang mã khác (cần test gỡ mã khỏi công ty), `pendingQuery` sai trạng thái, `requirement_department_id` thay `department_id`.
- API thật (JWT mint, người duyệt thật): `GET /approval-center/inbox?doc_type=…` trả đúng hàng, status_text/màu/handler_path đúng cho cả 6 loại; `/inbox/counts` ok. Không chạy Playwright.
