# Fix ERP "Unknown column receiver_id" sau gộp DB notifications

## Bối cảnh
Commit gộp hôm nay làm bảng `notifications` mang cấu trúc HRM (Laravel:
notifiable_type/read_at). ERP dùng cấu trúc riêng (receiver_id/url/content/
seen/status/expired_date) ở ~140 file → mọi màn ERP gọi thông báo bị 500.
`hrm_notifications` đã bị drop, `notifications` rỗng.

## Quyết định (user chốt) — KHÔNG LÀM
User không thao tác ERP nữa → chấp nhận để bảng `notifications` nguyên cấu trúc
HRM. Hệ quả: mọi luồng ERP gọi `sendNotify` sẽ 500 + rollback, nhưng vì không
dùng ERP nên bỏ qua. Sẽ làm lại cơ chế thông báo khi chuyển chức năng sang HRM.

→ Các task dưới đây DEFERRED (không thực hiện). Giữ lại để tham chiếu nếu sau
này cần ERP chạy tạm trên DB gộp.

## Phương án đã khảo sát (nếu cần dùng lại)
Tách bảng: hoặc ERP giữ `notifications` + HRM → `hrm_notifications`, hoặc HRM
giữ `notifications` + ERP → `notifications_erp` (cấu trúc ERP: id, url, content,
status, receiver_id, created_by, timestamps, expired_date, details, seen).

## Tasks
- [ ] Migration ERP tạo bảng `notifications_erp` (id, url, content, status, receiver_id, created_by, timestamps, expired_date, details, seen)
- [ ] `Notification` model: thêm `protected $table = 'notifications_erp'`
- [ ] `ClearNotification.php:46` raw `DB::table('notifications')` → `notifications_erp`
- [ ] Chạy migration trên DB local (erp_hrm_check)
- [ ] Verify: query NotificationsController::index không còn lỗi
- [ ] (Hỏi) Kiểm tra bảng `files` — cùng commit gộp, có thể lỗi tương tự
