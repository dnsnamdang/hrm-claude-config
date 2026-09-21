# Plan — Ẩn công ty đã khoá khỏi ô chọn công ty (header)

Nhánh `tpe`. Phụ trách: @cuong61n. QA báo 17/09/2026 tại `/timesheet/request-update-working/create`
(thực ra là ô chọn công ty của component `BasicSubsystem`, hiện ở mọi màn).

- [x] `AuthNewController@userProfile`: `company_roles` lọc `companies.status = 1` (trước đây không lọc — dòng có từ 16/10/2024)
- [x] Chốt với user: **ẩn hẳn**, không ngoại lệ cho công ty đang làm việc
- [x] Test `test_company_locked.php`: 17/17 PASS (khoá → biến mất, mở khoá → hiện lại, công ty đang làm việc bị khoá vẫn vào được hệ thống, khoá hết → danh sách rỗng không lỗi, tự trả lại trạng thái công ty)
- [x] Đối chứng code cũ: 4 FAIL (trả cả 8 công ty kể cả đã khoá)
- [x] UI thật với `ceo@tanphat.com` (role gắn 8 công ty, 3 công ty đang khoá): header chỉ còn 5 công ty hoạt động
