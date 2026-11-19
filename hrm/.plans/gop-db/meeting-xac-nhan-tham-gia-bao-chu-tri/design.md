# Meeting — xác nhận tham gia báo chủ trì + cập nhật tab Điểm danh ngay (tóm tắt)

Người phụ trách: @namdangit · 01/11/2026 · Plan: `plan.md` cùng thư mục.

## Yêu cầu
Người tham gia bấm **Xác nhận tham gia / Không tham gia** ⇒ (1) gửi thông báo cho người chủ trì; (2) tab Điểm danh cập nhật
ngay lúc đó — trước đây chỉ hiện khi meeting đã Chốt lịch.

## Quyết định đã chốt (user 01/11)
| # | Quyết định |
|---|---|
| Q1 | Ở **Lên lịch** cột điểm danh **chỉ xem** (nhãn "Xác nhận tham gia", "Chưa phản hồi"); chủ trì chỉ sửa điểm danh từ Chốt lịch |
| Q2 | Chỉ báo khi trạng thái **thực sự đổi**; người bấm là chủ trì thì không báo |
| Q3 | Tự cập nhật **realtime** trên cả web và app (không cần tải lại) |

## Cách làm
- BE `MeetingService::confirmAttendance` ⇒ `notifyHostAttendanceConfirmed()`: `[MET] Cập nhật: <tên>. X xác nhận Có mặt` /
  `X báo Vắng có lý do. Lý do: …`, deep-link `/assign/meeting/{id}/show?active_tab=participants`, gửi chuông + push + DB.
  `MeetingMineResource.attendance_open` gồm cả Lên lịch.
- Web: 4 component menu phát `$root.$emit('realtime-notification')` khi socket báo; `MeetingForm` nghe → `reloadAttendance()`
  (merge trạng thái, không đè dòng chủ trì đã sửa tay ở Chốt lịch). `MeetingParticipants` + `AttendanceStatusCell` chế độ RSVP.
- App: `meetingPushed` (StreamController) trong `meeting_create.dart`, `app_bloc` onMessage đẩy id ⇒ Hub + màn Nhân sự tham gia tự tải lại.
