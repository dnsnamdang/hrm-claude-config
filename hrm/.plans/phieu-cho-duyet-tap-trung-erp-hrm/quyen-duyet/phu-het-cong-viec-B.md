# Phủ hết màn duyệt — Công việc, fork B (Giải pháp / Hạng mục / Vấn đề) — @cuong61n

17/11/2026. Definition: `hrm-api/Modules/ApprovalCenter/Definitions/Assign/{Solution,Issue}Definition.php`; test `hrm-api/tests/Feature/ApprovalCenter/Assign/{Solution,Issue}DefinitionTest.php`. Manifest dữ liệu thử: `wave2-assign-B.json` (đã dọn).

| doc_type | Màn gốc | Cấp | Gate | Pending local thật | Verify | Đột biến | Trạng thái |
|---|---|---|---|---|---|---|---|
| `solution` | `/assign/solutions/{id}/edit?mode=approve` (nút "Giao cho Leader" / "Lưu và duyệt" ở danh sách + chi tiết) | 1 "Chờ PM duyệt" (status 3) · 2 "Chờ Leader duyệt" (status 5) | Cấp 1: `pm_id` = tôi (`canEdit`). Cấp 2: tôi là `leader_id` của hạng mục còn `status != 2` (`has_unapproved_leader_module`). Thành viên bị khoá (middleware `solutionMemberActive`) loại. Không mã quyền / công ty | 2 (status 3) | 32.000 cặp 0 chênh (command); test 1.620 cặp, 30 dương, 0 chênh | 4/4 | xong |
| `issue` | `/assign/issues?open_issue={id}` | 1 "Chờ duyệt" (status `resolved` + có `approver_id`) | `approver_id` = tôi (`getAllowedNextStatuses` chứa completed + rejected). Không mã quyền / công ty | 1 | 28.000 cặp 0 chênh; test 720 cặp, 30 dương, 0 chênh | 3/3 | xong |
| `solution_module` | — | — | — | — | — | — | KHÔNG đăng ký (bằng chứng dưới) |

## Quyết định
- **Gom `solution` 1 doc_type 2 cấp** (step 1 PM, step 2 Leader) vì cùng 1 hàng `solutions`, cùng màn duyệt `edit?mode=approve`, cấp đổi theo status — giống `quotation`.
- **status 9 "Chờ duyệt giải pháp" KHÔNG nằm trong `solution`**: quyết định ở Hồ sơ trình duyệt (`SolutionService::reviewSolutionProfileDecision` `Services/SolutionService.php:2706+`, người tạo giải pháp) — đã có `solution_review_profile`. `Solution::canEdit` ở status 9 (`Entities/Solution.php` ~230) chỉ là quyền SỬA của phòng tiếp nhận.
- **`solution_module` bỏ**: không có trạng thái chờ riêng của hạng mục ngoài 2 thứ đã phủ. (1) Leader duyệt hạng mục = bước 5 của `solution` (`SolutionService::update` khối `approve_modules`, FE `_id/edit.vue:25-33,286`; nút duyệt hết hạng mục của mình 1 lượt). (2) PM thêm hạng mục khi "Đang triển khai" tự duyệt luôn (`auto_approve_new_modules` `SolutionService.php` ~595, FE `_id/edit.vue:43-50,329`) — không có bước chờ người khác. (3) status 6 "Chờ duyệt hồ sơ trình duyệt" (`SolutionModule::STATUS_CHO_DUYET_HO_SO_TRINH_DUYET`) là phản chiếu của hồ sơ pending, quyết ở `reviewModuleProfileDecision` (`SolutionModuleService.php:1397`) = loại `solution_module_review_profile` đã đăng ký.
- Kiểm 2 loại hồ sơ trình duyệt đợt 1: `solution_review_profile` khớp `reviewSolutionProfileDecision` (người tạo giải pháp, khoá thành viên, tự triển khai); `solution_module_review_profile` khớp `reviewModuleProfileDecision` (`pm_id` giải pháp ∨ `pm_id` hồ sơ). Không thiếu cấp, KHÔNG sửa.
- Chữ `issue` hiển thị "Chờ duyệt" #D97706 (BE gọi "Đã xử lý xong" xanh nhưng thông báo cho người duyệt ghi "Chờ duyệt", `IssueService::notifyApproverForReview`).

## Đồng bộ
- Gắn trait `SyncsApprovalInbox` vào `Solution` (doc_type `solution`) và `Issue` (doc_type `issue`).
- Ghi hàng loạt bằng query builder đã xử lý: `ProspectiveProjectService` (đóng dự án) `Solution::whereIn()->update(status=Đóng)` — thêm `ApprovalInboxService::scheduleSync('solution', id)` cho từng giải pháp (sau khối cascade giải pháp). `SolutionService::update` ghi trạng thái hạng mục bằng `$solution->modules()->update(...)` (không phát sự kiện) nhưng ngay trước đó có `$solution->update($payload)` nên trait vẫn sync sau commit; ngoài ra `watchedTables` của `solution` nghe `solution_modules`, `solution_members`, `solution_module_members` (DB::listen).
- `Issue`: mọi đường đổi trạng thái qua `$issue->update()` (IssueService::changeStatus) ⇒ trait tự sync.

## Lỗi / lưu ý code gốc
- Giải pháp ở status 3 / 5 không có nút Từ chối; chỉ có "Yêu cầu chỉnh sửa" từ status 11 đưa về status 3 (vòng mới, `round` tăng).
- `Solution::save()` ngoài `DB::transaction` trên DB local trả `$solution->id = 0` (đã thử `withoutEvents`, vẫn 0 ⇒ không do trait) — `seedTest` bọc trong transaction. Chưa tìm ra nguyên nhân (không có trigger); thường không dính vì controller bọc giao dịch.
- Issue: BE không kiểm gì ngoài `getAllowedNextStatuses` (an toàn); người làm = người duyệt được phép (không chặn).
- Dữ liệu thật: giải pháp 12 và 29 đang chờ PM (status 3) từ tháng 7-9/2026; giải pháp status 5 = 0; issue 6 (người duyệt employee 13) 1 phiếu.

## BE không chốt quyền
Không có: cả 2 loại đều có chốt BE (`SolutionController::update` kiểm `canEdit` + middleware khoá thành viên; `IssueService::changeStatus` kiểm trạng thái kế tiếp theo vai trò). Điểm lỏng: `canEdit` ở status 5 cũng cho PM sửa nhưng chỉ Leader có hạng mục chưa duyệt mới "duyệt" được — Definition theo cờ nút FE.
