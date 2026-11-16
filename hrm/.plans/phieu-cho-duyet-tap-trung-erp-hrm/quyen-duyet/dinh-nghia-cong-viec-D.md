# Định nghĩa loại phiếu — nhóm Công việc, phần D — @cuong61n

Ngày 16/11/2026. 6 loại, tất cả XONG (verify 0 chênh lệch, đột biến bị test bắt). Đường dẫn tính từ `hrm-api/`.
Definition: `Modules/ApprovalCenter/Definitions/Assign/*Definition.php`; test: `tests/Feature/ApprovalCenter/Assign/*DefinitionTest.php`
(dùng chung `Concerns/DiverseTestData`, và `Concerns/VerifiesByEmployeeSet` cho loại người duyệt đích danh — do phần D thêm).

| doc_type | Màn gốc (FE) | Cấp | Gate | Pending local thật |
|---|---|---|---|---|
| payment_business_request | `/assign/payment_business_request/{id}/show` | 2 "Chờ TP duyệt" → 3 "Chờ KT duyệt" | mã `assign.de_nghi_thanh_toan_truong_phong.approve` / `..._ke_toan.approve`, không xét phòng/công ty | 808 (610 + 198) |
| settlement_contract | `/assign/settlement_contract/{id}/show` | 2 TP → 3 KT | mã `assign.quyet_toan_hop_dong_truong_phong.approve` / `..._ke_toan.approve`, không xét phòng/công ty | 0 |
| payment_profile | `/assign/payment_profile/{id}/show` | 1 cấp "Chờ duyệt" | mã `assign.ho_so_thanh_toan.approve`; KHÔNG có từ chối | 303 |
| task_extension_request | `/assign/tasks?open_task={task_id}` | 1 cấp "Chờ duyệt" | người giao `tasks.created_by` + `TaskAccess::assertWritable` (nhóm chưa đóng, trừ nhóm KH); mọi công ty | 0 |
| solution_review_profile | `/assign/solutions/{id}/manager?active_tab=review-profiles` | 1 cấp 'pending' | người tạo giải pháp `solutions.created_by`; dự án "Tự triển khai" ⇒ không ai duyệt; thành viên bị khoá bị middleware chặn | 0 |
| solution_module_review_profile | `/assign/solution-modules/{id}/manager?active_tab=review-profiles` | 1 cấp 'pending' | `solutions.pm_id` (giải pháp chứa hạng mục) HOẶC `pm_id` ghi trên hồ sơ | 0 |

## Điểm đáng nhớ
- BE không trả chữ/màu trạng thái cho 3 loại thanh toán/quyết toán (FE tự map) ⇒ Definition khai theo đúng chữ FE ("Chờ TP duyệt", "Chờ KT duyệt", "Chờ duyệt") + màu `#D97706`.
- `PaymentProfile` không có `created_by` trong `$fillable` ⇒ seed/test gán thuộc tính trực tiếp.
- Route duyệt cấp TP của 3 luồng thanh toán có middleware ERP `checkDueConfigsManager` (fail-open) — không phải gate nghiệp vụ, không đưa vào Definition (ghi trong `gate_blocker`).
- Loại đích danh không dựa vào quyền/công ty ⇒ gán người duyệt cho MỌI công ty (khớp truth: endpoint không kiểm công ty).
- Hàm duyệt giải pháp / hạng mục có tác dụng phụ (đổi trạng thái, thông báo, đồng bộ BOM) nên `truth()` viết lại đúng thứ tự điều kiện chặn; phần khoá thành viên gọi thẳng `CheckSolutionMemberActive::isLockedMember` qua reflection.
- Gia hạn nhiệm vụ: `truth()` gọi `TaskAccess::assertWritable` + `TaskExtensionService::canDecide` (reflection).
- Chưa kiểm được trên DB local: nhánh "nhóm (workspace) đã đóng" của gia hạn nhiệm vụ (cột `tasks.workspace_id` thuộc migration 2026_11_14 chưa chạy ở local) — test đó `skipped`.

## Lỗi / lưu ý code gốc
- `SettlementContractController::approve/ktApprove/tpReject/ktReject` và `PaymentProfileController::approve` trả `responseErrors('Không có quyền!')` — truyền chuỗi vào tham số mã lỗi (HTTP code), có thể ra mã lạ.
- FE chỉ hiện nút duyệt hồ sơ trình duyệt hạng mục cho `solutions.pm_id`, BE cho cả `pm_id` ghi trên hồ sơ ⇒ PM-hồ sơ (khác PM giải pháp) thấy phiếu trong Chờ duyệt nhưng màn không có nút (Definition theo BE).
- Thông báo quyết toán dùng tên quyền `Duyệt quyết toán hợp đồng` không có trong Catalog (đã ghi ở 02-cong-viec.md mục 10) — không đụng.

## Chỗ ghi bằng query builder
Không có chỗ nào ghi trạng thái chờ duyệt bằng `->update()`/`DB::table()` cho 6 bảng này trong code chạy thật. Các `->update(['status' => 'expired'])` ở `SolutionService:2925` và `SolutionModuleService:1232` chỉ đổi hồ sơ 'approved' → 'expired' (không phải đang chờ) nên không cần `scheduleSync`.

## Việc cho điều phối
- `task_extension_request.watchedTables()` chỉ nghe `workspaces`; đổi `tasks.created_by` (người giao) của việc đang có đề nghị chờ không tự sync (lệnh backfill vớt). Nếu muốn chặt hơn cần nghe `tasks` (ghi rất thường xuyên).
