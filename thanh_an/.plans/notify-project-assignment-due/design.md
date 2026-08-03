# Thông báo dự toán chờ phân công sắp hết hạn — Tóm tắt

**Người phụ trách:** @khoipv · **Ngày:** 2026-07-06

## Mục tiêu
Màn Dự toán (`sale/project`): tự động thông báo cho người có quyền `'Phân công báo giá'` khi có dự toán ở trạng thái **Chờ phân công** (status 2) mà còn **≤ 2 ngày làm việc** là tới hạn `expected_time`.

## Quyết định lớn
- Người nhận: **tất cả** ai có quyền `'Phân công báo giá'` (không lọc cấp).
- Ngưỡng: **≤ 2 NLV** (nhắc lại mỗi ngày tới khi được phân công).
- Chỉ trừ T7/CN (không dùng ngày lễ). Không gửi vào cuối tuần. Không gửi khi đã quá hạn.
- Không gửi cho người tạo.

## Cách làm
- 1 Console Command `projects:notify-assignment-due` (`app/Console/Commands/NotifyProjectAssignmentDue.php`).
- Đăng ký cron dailyAt 07:00 trong `app/Console/Kernel.php`.
- Tái dùng `EmployeeInfoService::listEmployeeInfoByPermission` + `sendToAllContractNotification`. Dùng `Carbon::diffInWeekdays`.
- **Chỉ BE**, không migration, không đụng FE.

## Spec chi tiết
`docs/superpowers/specs/2026-07-06-notify-project-assignment-due-design.md`
