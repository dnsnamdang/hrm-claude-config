# Design — Redmine #11292: In biên bản meeting, cấu hình chỉ hiện người CÓ MẶT

**Phụ trách:** @khoipv · **Nhánh:** `fix-bug-11092026` (hrm-api + hrm-client)
**Spec chi tiết:** `docs/superpowers/specs/2026-09-11-redmine-11292-in-bien-ban-thanh-phan-co-mat-design.md`

## Mục tiêu
Popup cấu hình in biên bản cuộc họp có thêm checkbox **"Thành phần tham dự có mặt"** (mặc định tắt):
- **Tắt (mặc định)** — in đủ mọi người được mời, kèm **trạng thái tham dự** và **lý do vắng**.
- **Bật** — chỉ in người điểm danh **"Có mặt"**, ẩn "Vắng mặt" và "Chưa điểm danh".

## Hiện trạng
- Luồng in: nút **In** → `MeetingPartsConfigModal` (chọn phần) → `MeetingPrintPreview.vue` (render Vue, tự mở cửa sổ in). Dùng ở `pages/assign/meeting/index.vue` và `MeetingReport.vue`.
- Bảng "III/ Thành phần tham gia" chỉ có 4 cột: TT / Họ và tên / Chức vụ / Chữ ký — **chưa có trạng thái điểm danh**.
- Dữ liệu điểm danh có sẵn: `meeting_employees.attendance_status` (0 Dự kiến tham gia · 1 Có mặt · 2 Vắng có lý do · 3 Vắng không lý do) + `attendance_note` (ghi chú/lý do). `MeetingResource` trả nguyên model nên FE đã có.
- **Bản in có 2 nguồn** dựng cùng nội dung I–V: blade `hrm-api/resources/views/exports/meeting_record.blade.php` (route `GET assign/meeting/{id}/print`) và `MeetingPrintPreview.vue`. File blade ghi rõ nợ kỹ thuật: sửa 1 bên quên bên kia là lệch.

## Quyết định
1. **1 cột duy nhất** "Trạng thái tham dự (Attendance)", lý do để trong ngoặc: `Vắng có lý do (Đi công tác)` — không tách cột lý do, tránh bóp cột Họ tên/Chức vụ trên khổ A4 dọc.
2. Khi checkbox **bật** thì **ẩn** cột trạng thái (mọi dòng đều "Có mặt" nên cột thừa).
3. Nhãn trạng thái **dùng đúng nhãn của tab Điểm danh**, kể cả trạng thái 0 là "Dự kiến tham gia" (issue gọi là "Chưa điểm danh").
4. **Không đụng Xuất Excel** — issue chỉ nói bản in. `MeetingPartsConfigModal` dùng chung cho cả Excel nên checkbox bật/tắt qua prop `showOnlyPresentOption`, mặc định `false`.
5. **Có cập nhật blade BE** để 2 nguồn in không lệch; blade nhận thêm `$onlyPresent` từ query `only_present` của `MeetingController@print`.
6. Checkbox chỉ hiện khi phần **"Thành phần tham dự"** có trong danh sách phần khả dụng (meeting không có thành viên nào thì checkbox vô nghĩa).
