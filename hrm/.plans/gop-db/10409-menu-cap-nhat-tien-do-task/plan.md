# #10409 — [App] Đổi tên + di chuyển menu "Báo cáo tiến độ task" — @cuong61n

TPE_APP `develop`. CHƯA commit.

- [x] Menu trái: đổi tên "Cập nhật tiến độ task", lên menu cấp 1 ngay dưới "Công việc của tôi" (icon edit, giữ badge), bỏ khỏi nhóm "Giao việc/Công tác" — `ui/dashboard_nhan_vien/dashboard_nhan_vien_page.dart`
- [x] Tiêu đề màn đổi "Báo cáo tiến độ" → "Cập nhật tiến độ task" cho khớp menu
- [x] `dart analyze` không lỗi mới
- [x] Test iOS simulator: menu cấp 1 đúng vị trí + tên + icon; nhóm Giao việc/Công tác không còn mục cũ; số đỏ "1" hiện ở menu cấp 1 (TK namdangit, khớp 1 task chờ báo cáo); bấm mở đúng màn, tiêu đề mới
