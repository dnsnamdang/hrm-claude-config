# Trang chủ: cảnh báo "Phân công nhân viên phụ trách hãng" đếm theo nhầm phòng (ERP) — @junfoke

Phản ánh 06/11/2026: EG – Phòng KD2 (chị Trần Thị Lan, NV 1238) thấy cảnh báo 3 hãng, bấm vào không xem được.

## Ngày 06/11/2026 (@junfoke)
- [x] 06/11/2026 — Hỗ trợ check: ô cảnh báo hiện cho người có quyền "Tạo phiếu phân công nhân viên phụ trách hãng" HOẶC người quản lý chính phòng mình; trang đích bắt buộc quyền ⇒ trưởng phòng không có quyền bấm vào ra "không tìm thấy". Chị Lan được khai "Quản lý các phòng" = KD2 (id 133) nên thấy cảnh báo dù chỉ là NV KD.
- [x] 06/11/2026 — Lỗi thật (user yêu cầu đọc code, không đoán): `HomeController` join `employee_manage_departments` + `departments` rồi `->get()` (SELECT *) ⇒ cột `departments.department_id` ghi đè `employee_manage_departments.department_id` ⇒ cảnh báo đếm theo phòng 130 (Hành chính Nhân sự) thay vì 133; 3 dòng thiếu NV phụ trách là HP / HP Inc. / MIDORI của phòng HCNS. Sửa select tường minh `departments.id as department_id, departments.name`. Commit `79aea9119c` (gop_db, đã push).
- [x] 06/11/2026 — Sửa lỗi tương tự ở `Division/DivisionMarketEmployeeController` (2 chỗ dropdown phòng của Phiếu phân chia thị trường theo NV ra sai phòng; thêm `departments.status`). Commit `9908e677b4` (gop_db, đã push).
- Bẫy: bảng `notifications` DB gộp đã theo kiểu Laravel (nội dung trong JSON `data`, người nhận `notifiable_id`) — SQL tra thông báo phải dùng `JSON_EXTRACT`.
