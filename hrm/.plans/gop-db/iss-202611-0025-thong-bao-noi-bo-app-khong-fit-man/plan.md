# Thông báo nội bộ trên app: nội dung mẫu in không vừa màn điện thoại (ISS-202611-0025) — @cuong61n

Báo lỗi: chat nội bộ (Thu Huyền) 25/11/2026 — thông báo "Nghỉ ngày Văn hóa Việt Nam 24/11" mở trên app bị gãy chữ từng ký tự ở bảng Quốc hiệu / tên công ty, bảng Nơi nhận / Người ký. Chưa có số Redmine (mã ISS của tool chat).

Nguyên nhân (đã lần tới code): nội dung thông báo là MẪU IN A4 (`print_template_id`) do BE điền biến và trả ở field `template` (`DetailSelfNotificationResource.php:102-137`). App đưa nguyên HTML đó vào `HtmlWidget` trong card rộng bằng màn → bảng 2 cột bị bóp còn ~170px/cột. Web không lỗi vì render trong khung 794px.

Cách xử lý đã chốt (user 25/11/2026: "cách đơn giản nhất tối ưu nhất"): copy khuôn màn "Xem biên bản" họp của app (`meeting_minutes_preview_page.dart::_buildPaper`) — dựng tờ giấy đúng khổ A4 794px, lề 57px, `FittedBox` thu nhỏ vừa bề ngang, `InteractiveViewer` zoom 2 ngón tối đa 4x. KHÔNG sửa mẫu in (dùng chung bản in web, user tự sửa), KHÔNG thêm BE / PDF.

## Phase 1 — App (TPE_APP nhánh develop)
- FE app
  - [x] (25/11) `internal_notification_detail_page.dart`: HTML có `<table` → `_buildPaper()` (A4 794px + FittedBox), bọc `InteractiveViewer(minScale 1, maxScale 4)` quanh scroll; nội dung soạn tay không có bảng vẫn `HtmlWidget` như cũ, tắt zoom/pan
  - [x] (25/11) `internal_notification_detail_controller.dart`: cache `paper` dựng 1 lần (HtmlWidget dựng lại khi Obx rebuild làm cột co — bài học từ màn biên bản họp)
  - [x] (25/11) Widget chung mới `lib/common_view/scaled_to_width.dart` (`ScaledToWidth`): dựng child ở bề rộng cố định rồi co CẢ chiều cao theo tỉ lệ. Lý do: `FittedBox(fit: fitWidth)` trong scroll (chiều cao vô hạn) giữ nguyên chiều cao gốc 738px → khoảng trắng lớn dưới giấy (đo thật lần chạy đầu). Màn biên bản họp đang dùng FittedBox cũng dính, chưa sửa (ngoài phạm vi)
  - [x] (25/11) Test iPhone 15 simulator (tpeLocal, TK namdangit), dữ liệu test local `self_notifications.id=405` "[TEST-ISS-0025]…" (HTML giống thông báo thật: bảng Quốc hiệu 2 cột + bảng Nơi nhận/Người ký + 2 file đính kèm, gửi employee_info 6): bảng giữ đúng 2 cột, không gãy chữ; card bó sát giấy (đo pixel: card kết thúc ~541pt, dưới là nền F4F6F9); phần "Thông tin đính kèm" hiện dưới giấy; thông báo soạn tay (DEMO/01) vẫn hiện như cũ; `step.sh` không lỗi Flutter
  - [ ] CHƯA thử: zoom 2 ngón (mobile-mcp không giả lập pinch), Android, bản release. Bản ghi test 405 để nguyên ở DB local
- Trạng thái: đã sửa local + test iOS simulator, chưa commit / chưa build.
