# [Chấm công] Thông báo: check lại quyền nhận thông báo trên app và lỗi text (#12096) — @cuong61n

Redmine #12096 (Nguyễn Huyền giao 10/11/2026, nền tảng Mobile App). Hai việc: (1) quyền nhận thông báo, (2) sửa text lý do phiếu đi muộn về sớm.

## Task 1 — Quyền nhận thông báo (ví dụ Hoàng Trung Hậu nhận quá nhiều)
- [x] 10/11 Điều tra: Hậu (employee_infos.id 246) có 590 thông báo chưa đọc trong 30 ngày trên prod, 100% là `App\Notifications\SystemNotification` loại "đang tổng hợp yêu cầu đặt hàng cho thương hiệu …" (4–47 cái/ngày). Các loại khác (cơm, lịch lãnh đạo, chấm công) số lượng bình thường.
- [x] 10/11 Nguyên nhân: ERP (TanPhatDev) gửi cho TOÀN BỘ nhân viên đang hoạt động trừ người tạo (`Employee::where('status','!=',0)`), không lọc quyền/vai trò — 4 controller Order: InlandOrderNotificationNew, InlandOrderNotification2, OrderNotification2, OrderNotifications (mỗi file 2 chỗ).
- [ ] Chờ chốt đối tượng nhận (đề xuất: người được phân công phụ trách thương hiệu trong `AssignHistory`, hoặc người có quyền xem màn đặt hàng) rồi sửa ERP. Đổi nghiệp vụ → cần user duyệt trước.

## Task 2 — Sửa text lý do phiếu đi muộn về sớm
- [x] 10/11 Web (hrm-client) đã đúng "Chế độ phụ nữ/Thai sản nữ" (add.vue, _id/index.vue, _id/approve.vue) — không phải sửa.
- [x] 10/11 App (TPE_APP, nhánh `tpe`): đổi "Thai sản nữ" → "Chế độ phụ nữ/Thai sản nữ" ở `ui/dang_ky_di_muon_ve_som/dang_ky_di_muon_ve_som_page.dart` (danh sách chọn) và `bloc/dang_ky_di_muon_ve_som_bloc.dart` (gán ô lý do). Chuỗi chỉ là nhãn hiển thị, payload dùng cờ `truLuongChecked` nên không đổi dữ liệu gửi BE.
- [x] 10/11 `fvm dart analyze` thư mục màn: 0 lỗi.
- [ ] Chưa bấm thử trên simulator; chưa commit/push (TPE_APP còn thay đổi `makefile`, `scripts/build/*` không phải của việc này).
