# Design (tóm tắt) — Tab "Lịch meeting" trong màn Todo

- **Người phụ trách**: @dnsnamdang
- **Branch**: `meeting-schedule` (api + client)
- **Spec chi tiết**: `docs/superpowers/specs/2026-08-14-lich-meeting-tab-design.md`
- **Mockup**: `.plans/gop-db/ke-hoach-phat-trien-thi-truong/ke-hoach-phat-trien-thi-truong-mockup-meeting.html` (tab "📅 Lịch meeting")

## Mục tiêu
Chia màn `pages/assign/my-todo/index.vue` thành 2 tab:
1. `✅ Công việc của tôi` — **giữ nguyên** tab hiện có.
2. `📅 Lịch meeting` — **mới**, lịch Tháng/Tuần hiển thị meeting của tôi, bám đúng mockup.

Tab thứ 3 "Kết quả meeting theo thị trường" (báo cáo) = **feature khác**.

## Quyết định lớn
- **Data**: chỉ meeting của tôi = đúng scoping `MeetingCriteria` của danh sách meeting hiện tại, lọc theo khoảng ngày kỳ đang xem.
- **BE**: thêm endpoint riêng `GET assign/meeting/calendar?from_date&to_date` — trả danh sách gọn, **không phân trang**. Tái dùng `MeetingCriteria`.
- **FE**: bọc nội dung my-todo trong tab switcher (dùng `v-show` giữ state), thêm cây component `components/calendar/` (Header, FilterToolbar, SummaryBar, MonthGrid, WeekGrid, MeetingCard, MultiDayBar, DetailDrawer, DayPopover).
- **Màu thẻ theo trạng thái**: Đang tạo/Lên lịch→xám, Chốt lịch→xanh dương, Hoàn thành→xanh lá, Huỷ→đỏ (muted).
- **Drawer "Sửa"/"Xem biên bản"**: tái dùng flow meeting sẵn có, không viết mới.

## Quyết định đã chốt — nguồn dữ liệu lấy vào lịch (2026-09-08)

1. **Điều kiện DUY NHẤT: user có tên trong Thành phần — Phía Công ty** (`meeting_employees.type = 1`).
   - KHÔNG dùng phạm vi theo quyền cấp (tổng công ty / công ty / phòng ban / bộ phận) như màn
     danh sách `/assign/meeting`. Đây là lịch làm việc CỦA TÔI, không phải lịch toàn công ty.
   - KHÔNG xét `host_employee_id` — thừa, vì chủ trì đã tự vào Thành phần ở mọi lượt lưu.
   - KHÔNG xét `created_by` — người tạo chỉ là người nhập liệu, thư ký nhập hộ không dự họp.
   → `MeetingCalendarCriteria`, KHÔNG sửa `MeetingCriteria` (màn danh sách giữ nguyên phạm vi quyền).
2. **Người chủ trì LUÔN nằm trong Thành phần**, do `MeetingService::ensureHostIsCompanyMember()`
   bảo đảm ở cả tạo mới lẫn sửa. Thêm vào CUỐI danh sách (giữ thứ tự kéo thả), chỉ thêm khi
   thiếu, đổi chủ trì thì KHÔNG gỡ người cũ.
3. **Trạng thái giữ nguyên**: meeting nháp chỉ người tạo thấy; meeting Hủy vẫn lên lịch (khối
   thống kê có ô "Hủy" riêng nên là cố ý).
4. Dữ liệu cũ vá bằng `hrm-api/database/backfill_meeting_host_as_member.php` (2 bước, idempotent,
   không đội `updated_at`).

## Ngoài scope
Tab báo cáo thị trường; tạo meeting từ ô lịch; sửa logic tab Công việc của tôi; lọc theo nhân viên/phòng ban/thị trường.

## Trạng thái
DESIGN DONE (2026-08-14) — chờ user review spec → writing-plans lên plan chi tiết.
