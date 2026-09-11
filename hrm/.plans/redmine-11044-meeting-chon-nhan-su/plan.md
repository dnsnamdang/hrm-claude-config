# Redmine #11044 — Tối ưu UI/UX chọn nhân sự (Người đề xuất / Người thực hiện)

Màn: Meetings → Lịch meeting → Chi tiết → Tab Biên bản cuộc họp (`pages/assign/meeting/components/MeetingReport.vue`)
Nhánh: `tpe-develop-assign_fix` (cả API và Client)

## Phase 1 — Người thực hiện chọn nhiều

### BE
- [x] Migration tạo bảng `meeting_report_executors` (meeting_report_id, executor_id, executor_name, executor_type, created_by, updated_by)
- [x] Entity `MeetingReportExecutor` + quan hệ `executors()` trên `MeetingReport` (`$with`)
- [x] `MeetingService::syncReports()` ghi danh sách người thực hiện; vẫn ghi `executor_name` (chuỗi gộp) để in/xuất Excel/báo cáo cũ không vỡ
- [x] `getListEmployee`: thêm filter `working_position_id` (Chức vụ), `employee_role_id` (Chức danh), tham số `only_ids=1` trả toàn bộ id theo bộ lọc (phục vụ Chọn tất cả nhiều trang)

### FE
- [x] Component dùng chung `components/V2BasePickerField.vue` — ô click cả khối mở popup, hiển thị text (đơn) hoặc tag có nút x (nhiều)
- [x] `PopupStaff.vue`: chế độ đơn click dòng là chọn + tự đóng; thêm filter Chức vụ / Chức danh; checkbox "Chọn tất cả" theo toàn bộ bộ lọc (mọi trang); nút "Thêm thành viên"; nhận `initialSelected` để tick sẵn người đã chọn
- [x] `MeetingReport.vue`: ô Người đề xuất dùng picker đơn, Người thực hiện dùng picker nhiều (`r.executors`), đồng bộ `executor_name`

### Checkpoint — 2026-08-26
Vừa hoàn thành: toàn bộ Phase 1 (BE + FE), đã test BE bằng tinker (sync/filter/get_all trả đúng)
Đang làm dở: chưa test UI thật trên trình duyệt
Bước tiếp theo: chạy thử màn Biên bản cuộc họp trên :3000 theo 4 AC của task
Blocked:

## Kiểm thử (2026-08-26)

- [x] BE 33 case (tinker): bộ lọc Chức vụ/Chức danh + kết hợp + giá trị không tồn tại · `get_all` khớp tổng phân trang và chứa hết id mọi trang · lưu nhiều/0/tên rỗng người thực hiện · lưu lại lần 2 không nhân đôi · nhân sự khách hàng type=2 · tương thích ngược `executor_name` · xoá meeting không để mồ côi
- [x] UI vòng 1 — 32 case (Playwright): AC1 chọn đơn tự đóng · AC2 tag + nút x · AC3 bộ lọc Chức vụ/Chức danh/Phòng ban · AC4 Chọn tất cả mọi trang · click lại bỏ tick · bỏ tick tất cả · đóng popup không mất tag · không lỗi JS
- [x] UI vòng 2 — 18 case: lưu → tải lại còn đủ tag, đúng thứ tự · bỏ hết người thực hiện bị BE chặn (400, lỗi đúng `reports.0.executor_name`) · màn Xem khoá ô + không mở popup · tài khoản ngoài cuộc họp bị 403 và bị đá khỏi màn Sửa · chưa đăng nhập thì `get_all` bị chặn
- [x] UI vòng 3 — 4 case: màn In hiện đủ 3 người thực hiện; `executor_name` (báo cáo cũ) đủ 3 tên
- [x] Dọn dữ liệu thử: xoá dòng biên bản thử + meeting thử, trả lại ngày meeting 26, trả lại mật khẩu tài khoản test

**Lỗi phát hiện khi test và đã sửa:** `MeetingController::destroy()` xoá meeting nhưng không dọn `meeting_report_executors` → dữ liệu mồ côi.

**Ngoài phạm vi task:** DB `hrm_prod_local` thiếu 12 migration nhánh meeting (mọi API chi tiết meeting trả 500) — đã chạy `php artisan migrate` theo xác nhận của user.

### Checkpoint — 2026-08-26
Vừa hoàn thành: code + test đầy đủ (87 case, 0 FAIL), Redmine #11044 chuyển "Đang tiến hành"
Đang làm dở:
Bước tiếp theo: chờ review / chuyển "Code xong chờ test" khi bàn giao
Blocked:

## Bổ sung — Bộ lọc dạng "Tìm kiếm nâng cao" (yêu cầu user 2026-08-26)

- [x] `PopupStaff.vue` bỏ khối `.pick-filter` tự dựng, chuyển sang `components/V2BaseFilterPanel.vue` — copy pattern từ `pages/assign/quotations/components/QuotationProductSearchModal.vue:34` (popup "Thêm hàng hoá")
  - Ô tìm nhanh "Tìm theo tên, mã nhân viên" + nút Tìm kiếm / Làm mới luôn hiện cùng hàng (`inlineSearchButtons`)
  - Công ty · Phòng ban · Bộ phận · Chức vụ · Chức danh nằm trong panel ẩn/hiện, **mặc định thu gọn** để dồn chỗ cho bảng nhân sự
  - Gõ chữ chỉ cập nhật keyword (Enter/nút mới tìm), bấm X xoá trắng thì tìm lại ngay — đúng khuôn `onQuickSearchChange` của popup Báo giá
- [x] Chạy lại bộ UI test: 35/35 PASS (thêm 3 case: mặc định thu gọn · ô tìm nhanh luôn hiện · bấm "Tìm kiếm nâng cao" mở panel)
- [x] Sửa lệch lề bộ lọc: 3 ô Công ty/Phòng ban/Bộ phận do `V2BaseCompanyDepartmentFilter` render (component con, bọc `.d-contents`) nên rule padding scoped không chạm tới → dòng 1 lệch 8px so với dòng 2 và ô tìm nhanh. Đổi sang `.pick-filter-row ::v-deep [class*='col-']`. Đo lại bằng Playwright: mọi hàng đều `left=271`, ô lọc `x=275` = mép ô tìm nhanh. Thêm 2 case chống tái phát (37/37 PASS)
