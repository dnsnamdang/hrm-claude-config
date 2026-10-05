# Design — Xác nhận tham dự trước cuộc họp (Redmine #11369)

> Feature: `meeting-attendance-confirm` · Phụ trách: @junfoke · Nhánh `task_11369` (tách từ `tpe`, cả 2 repo)
> Spec chi tiết: `docs/superpowers/specs/2026-09-11-meeting-attendance-confirm-design.md`

## Mục tiêu

Khách mời **nội bộ** của một cuộc họp tự phản hồi trước giờ họp: **[Có mặt]** hoặc **[Vắng có lý do]**.
Phản hồi ghi thẳng vào bảng Điểm danh nên người chủ trì mở biên bản là thấy sẵn, vẫn sửa lại được.

## Scope

| Có làm | Không làm |
| --- | --- |
| Endpoint tự xác nhận cho chính khách mời (không cần quyền `canEdit`) | Không thêm quyền mới vào seeder — đây là thao tác tự phục vụ của chính người trong cuộc họp |
| Cụm nút + badge ở màn Chi tiết meeting (khối Thông tin chung) | Không đụng luồng Điểm danh của người chủ trì (đã có sẵn) |
| Cụm nút ngay trên thông báo chuông (user chốt làm đủ spec) | Không thêm cột DB mới |
| Popup "Báo vắng mặt cuộc họp" bắt buộc nhập lý do | Không lưu lịch sử đổi ý (chỉ giữ lựa chọn cuối) |

## Quyết định lớn

1. **Không thêm cột DB.** Tận dụng `meeting_employees.attendance_status` + `attendance_note` đã có
   (0 chưa điểm danh / 1 Có mặt / 2 Vắng có lý do / 3 Vắng không lý do). Spec gọi đây là "điểm danh
   sơ bộ" và cho người chủ trì ghi đè — cùng một ô dữ liệu, nên đồng bộ là *tự nhiên*, không cần mapping.
2. **Endpoint riêng, không dùng `POST assign/meeting/{id}`.** Luồng update hiện tại gate bằng
   `canEdit()` = người tạo **hoặc** người chủ trì; khách mời thường không lọt qua. Endpoint mới chỉ cho
   sửa **đúng dòng của chính mình** và chỉ 2 cột điểm danh.
3. **Ẩn chứ không disable** khi không đủ điều kiện — theo quy ước project (spec cho phép "Disabled hoặc ẩn").
4. **Component dùng chung `MeetingAttendanceConfirm.vue`** cho CẢ màn chi tiết lẫn chuông, nên
   `BasicSubsystem.vue` (component dùng chung toàn hệ thống) chỉ phải thêm vài dòng gọi component.
   ⚠️ User đã duyệt việc đụng vào `BasicSubsystem.vue` (2026-09-11).
5. **`base-confirm-modal.vue` được bổ sung 2 prop tùy chọn** `required-input` + `input-required-message`,
   mặc định tắt → 70+ màn đang dùng không đổi hành vi. User duyệt 2026-09-11.

## Điểm cần khách xác nhận

- Phản hồi trước họp và điểm danh thật dùng **chung một ô dữ liệu** → sau cuộc họp không phân biệt được
  ai tự báo, ai bị chủ trì sửa. Spec mô tả đúng như vậy; nếu sau này cần tách thì thêm cột riêng.
- Khách mời **không** được tự chọn "Vắng không lý do" (status 3) — spec chỉ cho 2 nút.
