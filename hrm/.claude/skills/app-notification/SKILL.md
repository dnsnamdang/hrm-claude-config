---
name: app-notification
description: Thông báo trên TPE_APP — nội dung do hrm-api dựng (NotificationMeta, skill notification-convention), app hiển thị ở màn Thông báo + đẩy về điện thoại (FCM), bấm vào mở đúng màn theo data.type / data.id (ui/notification/notification_router.dart — dùng chung cho bấm push và bấm dòng ở màn Thông báo), nhắc hạn Việc của tôi (work_reminder.<loại>), thử thông báo đẩy trên simulator (simctl push). Dùng khi BE thêm loại thông báo mới, bấm thông báo không mở / mở nhầm màn, thông báo hiện "xem trên web", cần xem thông báo trên màn hình khoá.
---

# Thông báo — TPE_APP

## 1. Ai làm gì

| Phần | Ở đâu |
|---|---|
| Nội dung `[PREFIX] Nhóm hành động: <b>Tên</b>. Ghi chú` (≤ 180 ký tự, `note_full`) | hrm-api — `NotificationMeta::build()`, theo skill HRM `notification-convention` |
| Gửi: lưu DB (chuông web + màn Thông báo app) + socket (web realtime) + push FCM | `EmployeeInfoService::sendNotification($infoId, $data + ['url','type','id'], $command)` |
| Tiêu đề / nội dung push | `NotificationMeta::push()` → tiêu đề là CÂU tự nhiên (vd "Nhiệm vụ sắp đến hạn", "Đơn xin nghỉ bị từ chối", "Bình luận mới về nhiệm vụ" — `PUSH_TITLE_PHRASES`, chốt 30/10/2026), nội dung phần còn lại; data có `push_title` / `push_body` thì dùng nguyên (bản tin sáng liệt kê việc theo giờ) |
| Bấm mở màn | app `ui/notification/notification_router.dart` → `openNotificationTarget()` theo `data.type`, `data.id` — **1 bảng duy nhất** cho cả bấm push (AppBloc, `fromPush: true`) lẫn bấm dòng ở màn Thông báo. Trước 30/10/2026 có 2 bảng riêng, bảng của push thiếu 18 loại (bấm push chỉ mở app) — KHÔNG thêm `switch` thứ 2 |

App KHÔNG tự ghép câu thông báo. Tiền tố có dấu sẽ bị `strtoupper` của `NotificationMeta::build` làm hỏng → tiền tố
chỉ dùng chữ không dấu (`VIEC`, `TASK`, `PGV`, `PCT`, `MET`).

## 2. Loại thông báo ↔ màn mở (BẮT BUỘC khi BE thêm loại mới)

- BE thêm `type` mới → **phải thêm `case` trong `openNotificationTarget()`**, nếu không bấm vào chỉ hiện "Vui lòng xem chi
  tiết trên web". Kiểm cả 2 nơi trước khi báo xong.
- `type` phải nói đúng đối tượng. KHÔNG mượn type của luồng khác (bẫy thật: thông báo Phiếu giao việc / Phiếu
  giao công tác dùng `lateInEarlyOutApprove` → app mở màn duyệt Đi muộn về sớm; phần "Tạo mới" đã đổi sang
  `assign_job` / `assign_business` 29/10/2026, các thông báo Chờ duyệt / Đã duyệt cũ của 2 phiếu này vẫn còn sai).
- `data.id` = id đối tượng cần mở (không phải id người nhận).
- Nhắc hạn Việc của tôi: `type = work_reminder.<loại>` (task, issue, assign_job, assign_business, ts_job,
  ts_business, meeting, personal, digest) → `openWorkItemById(loại, id)` (`ui/my_todo/my_todo_actions.dart`).
  Loại chưa có màn trên app (issue) → snackbar "chưa có trên app"; personal / digest → mở Việc của tôi.

## 3. Nhắc hạn (BE `WorkReminderService`, chốt 29/10/2026)

- Nhắc trước hạn theo cấu hình công ty từng loại (màn web `/assign/work-reminder-settings`, quyền "Cấu hình nhắc
  hạn công việc"); quá hạn báo ĐÚNG 1 lần; bản tin sáng 07:30 T2–T7; tổng quá hạn sáng thứ Hai.
- Chạy `assign:send-work-reminders` (5 phút) + `assign:send-work-digest`; thử bằng `--at="Y-m-d H:i"`.
- Chi tiết + bảng từng loại: `HRM/.plans/mytodo-nhac-han/design.md`.

## 4. Thử trên simulator

- Simulator local không nhận FCM → dựng đúng tiêu đề / nội dung BE sẽ gửi rồi đẩy thẳng:
  ```bash
  # payload: {"aps":{"alert":{"title":"…","body":"…"},"sound":"default"},"gcm.message_id":"x","type":"…","id":"…"}
  xcrun simctl push <device> com.tanphat.app payload.json
  ```
  Lấy title/body bằng tinker `NotificationMeta::push(NotificationMeta::stripSender($data))` từ dòng `notifications`.
- Xem màn hình khoá: Simulator → Cmd+L rồi push; kéo lên xem nhóm.
- Bấm thử từng loại trong màn Thông báo của app → mở đúng màn (chi tiết đúng bản ghi).

## Checklist

- [ ] Nội dung dựng ở BE theo `notification-convention`, tiền tố không dấu
- [ ] `type` riêng đúng đối tượng + `case` trong `openNotificationTarget()` (thử bấm cả push lẫn dòng ở màn Thông báo); `id` là id đối tượng
- [ ] Bấm thử trên app mở đúng màn; push hiện đúng trên màn hình khoá
