# #10668 — [App] Đơn xin nghỉ: màn duyệt không hiện loại nghỉ — @cuong61n

Nguyên nhân: app lấy tên loại nghỉ bằng cách tìm `leave_type_id` của đơn trong `GET leave-type/get-list-leave-type-by-employee?employee_id=<người nộp>`. BE `LeaveTypeService::getListLeaveTypeByEmployee` lọc theo `current_company_role` của NGƯỜI ĐĂNG NHẬP (người duyệt) → người duyệt khác công ty với người nộp (vd đơn 13337 NV công ty 9, loại nghỉ id 60) thì danh sách không chứa loại nghỉ của đơn → ô trống. Web màn duyệt + chi tiết đơn gọi cùng API nhưng hiện tên bằng `leave_type_name` của chi tiết đơn → web KHÔNG trống (danh sách chỉ dùng khi đổi loại nghỉ).

## Phase 1 — BE (user duyệt sửa hàm dùng chung 19/10/2026)
- [x] `getListLeaveTypeByEmployee($employee_info_id, $companyId = null)`; controller: có `employee_id` → lấy `employee_infos.company_id` của NV đó; không truyền (form tạo đơn của chính mình) → giữ như cũ
- [x] Test API: employee 1695/1712 (công ty 9) → 7 loại nghỉ công ty 9 có id 60, 62 ✓; không truyền employee_id → 14 loại công ty 1 như cũ ✓
- [x] Test app: đơn cùng công ty hiện "Nghỉ phép" ✓; dựng tạm đơn 12997 thành NV công ty 9 + loại nghỉ 60 → hiện "Nghỉ phép" ✓ (đã trả dữ liệu gốc)
- [x] Test web (Playwright, đơn 12997 dựng tạm khác công ty): màn duyệt + màn chi tiết hiện "Nghỉ phép", API trả loại nghỉ công ty 9 (58–64) ✓; đã trả dữ liệu gốc
