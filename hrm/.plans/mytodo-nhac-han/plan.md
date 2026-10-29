# Nhắc hạn "Việc của tôi" (Mytodo) — @cuong61n

## Phase 1 — Chốt nghiệp vụ
- [x] (29/10/2026) Rà nhắc hạn hiện có, đề xuất, chốt hạn từng loại phiếu, quá hạn cách A, chống nhắc lặp, bản tin 07:30 (design.md)

- [x] (29/10/2026) Rà thông báo hiện có của Nhiệm vụ (TaskService, TaskCommentController, NotifyTaskReport), Vấn đề (IssueService, IssueCommentController), Meeting (MeetingService, MeetingReportDeadlineCommand, nhắc nhận phòng MeetingRoomBookingService), Nhắc việc cá nhân (không có): chỉ có thông báo theo sự kiện, chưa có nhắc hạn/quá hạn nào

- [x] (29/10/2026) Đề xuất cấu hình nhắc theo giờ (theo công ty, từng loại việc; Meeting tính phút) + khung giờ yên lặng 21:00–07:00 dồn vào bản tin; khuôn màn theo /meeting/settings (hub + Lịch sử). Chờ chốt

## Phase 2 — BE (chờ user cho làm)
- [ ] Sửa hạn danh sách theo design (deadline / to_time / giờ kết thúc) + sửa lọc phiếu giao công tác status 3
- [ ] Bảng ghi lượt đã nhắc (chống gửi trùng) + command nhắc từng mốc + bản tin 07:30 + tổng quá hạn thứ Hai, đăng ký Kernel
- [ ] Nhãn "Đang diễn ra · còn n ngày" trả từ BE

## Phase 3 — Web + App
- [ ] Hiển thị nhãn Đang diễn ra / Đi → về trên thẻ (web + app); thông báo bấm mở đúng việc
