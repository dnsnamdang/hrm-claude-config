# Fix — Màn Phân công làm thêm không thấy phiếu yêu cầu phòng khác gửi tới

## Bối cảnh
- Prod: phiếu `PYCLT-212` (đã duyệt, Phòng Dự án gửi tới Phòng Kỹ thuật công nghệ) không hiện ở modal chọn phiếu của `/timesheet/overtime-allocation/add` — anh Hà Mạnh Cường (12510560, phòng KTCN) không phân công được.
- Gốc rễ: modal `AddOvertimeRequirement.vue` gửi `department_id=<phòng user>`, nhưng BE `OvertimeRequirementService::filter()` map param này sang cột `requirement_department_id` (= **đơn vị yêu cầu**), trong khi phòng nhận phiếu nằm ở cột `department_id` (= **đơn vị thực hiện**).
- Hệ quả: modal chỉ ra phiếu do chính phòng mình phát ra → mọi phiếu phòng khác gửi tới đều không phân công được (không riêng phiếu 212).
- Verify trên prod (chạy đúng service với account anh Cường): `department_id=51` → 0 kết quả; bỏ param → 85 phiếu, có id 212 ⇒ không phải lỗi quyền/trạng thái.

## Task
- [x] BE `Modules/Timesheet/Services/OvertimeRequirementService.php::filter()`: thêm param mới `execute_department_id` → `where('department_id', ...)`. Giữ nguyên `department_id` (màn danh sách + export đang dùng theo nghĩa đơn vị yêu cầu).
- [x] FE `components/modals/AddOvertimeRequirement.vue`: đổi `department_id=` → `execute_department_id=`; bỏ `console.log` và block comment chết `if (this.isAllocation)`.
- [x] Test local (BE :8005 / FE :3005 — worktree tpe, DB `hrm_prod_6_6`):
  - API, account anh Cường (phòng 51): `department_id=51` → total 0 · `execute_department_id=51` → total 83. Khớp DB (83 phiếu status=2, dept 51).
  - Regression param cũ (account quyền tổng công ty): `department_id=55` → 12 phiếu (đơn vị yêu cầu) — hành vi cũ không đổi.
  - UI `/timesheet/overtime-allocation/add`, login Hà Mạnh Cường: modal "Thêm phiếu yêu cầu làm thêm" hiện **83 bản ghi**, cột Đơn vị thực hiện đều = PHÒNG KỸ THUẬT CÔNG NGHỆ; chọn PYCLT-208 → form tự điền Phiếu yêu cầu / Phòng ban yêu cầu / ngày giờ / loại công việc.
  - Tái hiện bug (tạm đổi lại param cũ, reload): modal "Chưa có dữ liệu — Tổng số bản ghi: 0" ✔ đúng triệu chứng prod. Đã khôi phục bản fix.
  - Màn dùng chung modal `/timesheet/overtime-assignment/add`: cũng ra 83 bản ghi.
  - Test nghịch quyền: login Nguyễn Đức Tuân (phòng 42) → modal 0 bản ghi, không rò 83 phiếu phòng KTCN. API `execute_department_id=51` với account này chỉ ra 14 phiếu, tất cả `created_by = chính user` (quyền xem phiếu mình tạo) — scope quyền không đổi.

## Còn treo (chờ chốt nghiệp vụ)
- Param `min_date` FE gửi lên BE **không dùng đến**. Nếu bổ sung thì phiếu quá khứ (212 có `start_at = 10/09/2026`) sẽ bị ẩn → cần chốt có cho phân công phiếu đã qua ngày không.

## Nhánh
- Sửa thẳng trên `tpe`. Đã commit + push lên GitHub (12/09/2026):
  - hrm-api `191ce8b78`
  - hrm-client `5760f8b0a`
- Push bằng worktree tạm dựng từ `origin/tpe` để không đụng các thay đổi dở khác đang có trong `worktrees/tpe-*`; sau đó 2 worktree chính đã fast-forward lên bản mới.
