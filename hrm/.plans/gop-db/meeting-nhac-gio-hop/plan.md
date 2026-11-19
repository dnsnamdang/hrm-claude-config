# Vá nhắc giờ họp (meeting có phòng / người báo vắng)

Người phụ trách: @namdangit · 01/11/2026 · user cho "làm" — hrm-api nhánh gop_db, chỉ BE, không migration, không commit.

## Hiện trạng (kiểm 01/11 trên code develop = gop_db + DB local, collect() chỉ đọc)
- Nhắc giờ họp = `assign:send-work-reminders` (5 phút/lần, `WorkReminderService`, cấu hình `/assign/work-reminder-settings`, mặc định 15').
- Họp có phiếu Chờ duyệt / Đã duyệt bị LOẠI ("đã có Nhắc nhận phòng"), nhưng `meeting:send-booking-reminders` chỉ nhắc phiếu ĐÃ DUYỆT và khi công ty bật (≠ 0)
  ⇒ phiếu chờ duyệt (2618, 2624 ngày 28–29/10) / công ty tắt nhắc nhận phòng: không ai được nhắc. Bản tin sáng cũng bỏ sót họp có phòng.
- Người đã báo vắng vẫn bị nhắc (cả 2 đường). Họp có phòng: người tham gia nhận câu "Nhắc nhận phòng" thay vì nhắc giờ họp.

## Chốt (user 01/11/2026)
1+2+3: mọi thành viên nội bộ luôn nhận nhắc giờ họp (kể cả có phòng); "Nhắc nhận phòng" của phiếu cuộc họp chỉ gửi người đặt + chủ trì; bỏ người đã báo vắng (attendance_status 2/3).

## Task
- [x] `WorkReminderService::baseQuery('meeting')`: bỏ whereNotExists phiếu, lọc vắng, địa điểm = tên phòng đang giữ → location/online
- [x] `MeetingRoomBookingService::notifyCheckinReminder`: phiếu có meeting_id → `meetingCheckinRecipients()` (đặt + chủ trì − vắng); phiếu tự đặt giữ nguyên
- [x] Kiểm local (chỉ đọc + transaction rollback): 28–29/10 từ 10 → 14 cuộc họp được nhắc (có 2618/2624 chờ duyệt), địa điểm = tên phòng; chủ trì báo vắng → rớt khỏi cả 2 đường nhắc
- [x] Kiểm thật trên dev (code CŨ): họp 23:30 01/11, namdangit + thuydt. 23:15:15 M1 (không phòng) → "[MET] Sắp đến hạn … Bắt đầu 23:30, tại Phòng thử" cả 2 người · 23:15:19 M3 (đã duyệt) → "[DPH] … Nhắc nhận phòng, còn 15 phút" cả 2 người · M2 (VIP1 chờ duyệt) → KHÔNG ai nhận gì ⇒ hở 1 xác nhận bằng push thật. Đã huỷ 2320–2322
- [ ] Không thêm PHPUnit (test chạy trên DB .env để lại rác + DB local thiếu bảng rbac) — kiểm lại sau deploy dev

### Checkpoint — 01/11/2026 23:25
Vừa hoàn thành: vá BE (2 file) + kiểm local; bằng chứng hở trên dev
Bước tiếp theo: user cho deploy hrm-api lên dev → kiểm lại M1/M2/M3 (kỳ vọng M2 có nhắc họp, M3: thuydt nhận nhắc họp chứ không nhận "nhắc nhận phòng")
Blocked: —

### Checkpoint — 01/11/2026 23:45
Vừa hoàn thành: commit 5106ee0d0 (gop_db local) → cherry-pick be2f961be push origin/develop. Kiểm lại dev lần 2 (họp 23:50, id 2323–2325): KẾT QUẢ Y HỆT CODE CŨ (M2 chờ duyệt không ai nhận; M3 thuydt vẫn nhận "Nhắc nhận phòng") ⇒ dev-hrm KHÔNG tự deploy khi push develop. Đã huỷ 2323–2325.
Đang làm dở: —
Bước tiếp theo: deploy tay hrm-api develop lên dev-hrm (124.158.4.24) → chạy lại 3 ca. Bản vá ĐÃ lên origin/gop_db (2c480f319, cherry-pick từ worktree tách origin/gop_db, không kèm rbac) — 01/11 23:50.
Blocked: cách deploy dev-hrm chưa có ghi chép
