# Hỗ trợ: popup Thông tin thu nhập không hiện Cấp bậc (chưa có số Redmine) — @cuong61n

## Phase 1 — Điều tra (30/10/2026)

- [x] 30/10/2026 — Khách (PROD hrm.eteksofts.com, hồ sơ 1486, phòng "Ban giám đốc CN Vinh", chức vụ TPV_Giám đốc CN Vinh) báo: mở Thông tin thu nhập thì ô Cấp bậc trống + khoá dù đã cấu hình cấp bậc trong Chức vụ, đã tắt Quyết định.
  - Nghiệp vụ: công ty 3 bật "Sử dụng định biên" (general_regulations.using_manpower = 1) → Cấp bậc/Năng lực lấy từ **Định biên nhân sự** của Phòng ban + Chức vụ, KHÔNG lấy từ cấu hình Cấp bậc của Chức vụ; ô bị khoá vì đang dùng định biên (không phải vì Quyết định).
  - Dữ liệu PROD (chỉ đọc): công ty 3 có **0 dòng** department_manpowers → API `human/department-manpowers/getData` trả ranks rỗng → ô trống. Chức vụ 532/618 có cấp bậc trong working_position_ranks nhưng popup không đọc bảng này.
  - Code: `hrm-client/components/modal/add-salary-history-modal.vue` (getManpowerAllocation, `:disabled="isUseDecision || using_manpower"`) · `hrm-api/Modules/Human/Services/DepartmentManpowerService.php::showDetail`.
- [ ] Chờ user chốt hướng: (1) khai Định biên cho phòng ban công ty 3, (2) tắt "Sử dụng định biên" công ty 3, hoặc (3) sửa code fallback lấy cấp bậc theo Chức vụ khi chưa có định biên (đổi hành vi — phải hỏi).
