# Ca làm việc — bỏ bắt buộc "Địa điểm chấm công hợp lệ" khi chọn hình thức App — @cuong61n

Màn: Chấm công › Ca làm việc › Thêm/Sửa ca (`/timesheet/timeworking/add-working-shift/{id}`). Nhánh `gop_db` (hrm-api).

## Phase 1 — BE
- [x] (29/10/2026) Chọn hình thức chấm công "App điện thoại" không còn bắt buộc nhập địa điểm chấm công hợp lệ. Ca không khai địa điểm ⇒ nhân viên chấm App ở mọi nơi (`checkCheckin()` trả true khi không có địa điểm; dòng bỏ trống bị `placeToCheckInOut()` bỏ qua). Kỹ thuật: `Modules/Timesheet/Http/Requests/CreateWorkShiftRequest.php` — `place` từ `required|array|min:1` → `nullable|array`, bỏ `place.*.place required`; chế độ nhập tay toạ độ (`not_goong_working_shift = 1`) chỉ buộc vĩ độ/kinh độ khi ĐÃ nhập địa chỉ (`required_with:place.*.place`).
  - Đã kiểm (tinker Validator): dòng trống → qua; không gửi place → qua; có địa chỉ thiếu toạ độ → 422 "Bắt buộc phải nhập" ở vĩ độ/kinh độ; đủ → qua.
  - Trạng thái: sửa trong worktree `gop_db-api`, chưa commit/push, chưa deploy. FE không đổi (FE vốn không chặn).
