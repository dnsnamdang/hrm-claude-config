# Plan — Phân quyền hiển thị lộ trình elearning theo loại user

Phụ trách: @khoipv

## Bối cảnh
Màn `/lo-trinh-hoc-tap` (elearning 3001) gọi `GET /api/v1/elearning/public/learning-paths`.
Trước đây luôn lọc `status=ACTIVE AND is_public=1` → chỉ hiện 2/7 lộ trình.
Yêu cầu: nhân viên đăng nhập từ HRM (SSO) thấy tất cả lộ trình ngoài nháp;
guest + học viên elearning độc lập chỉ thấy lộ trình công khai.

## Quyết định
- Employee (user_type=`employee`): `status=ACTIVE(2)` — bỏ điều kiện `is_public`.
- Guest + Learner: `status=ACTIVE(2)` AND `is_public=1`.
- "Ngoài nháp" = chỉ trạng thái Đang dùng (2); KHÔNG bao gồm Khoá (3).

## Task
- [x] BE: gắn middleware `elearning.auth.optional` cho route `public/learning-paths`
      (`Modules/Elearning/Routes/api.php`)
- [x] BE: trong `PublicBrowseController@learningPaths`, chỉ áp `where('is_public',1)`
      khi `user_type !== 'employee'`
- [x] Verify: guest=2 lộ trình, employee=5 lộ trình (status=2); Nháp(1) luôn bị ẩn
- [ ] FE: không cần sửa — `services/api.js` đã đính kèm Bearer token cho mọi request

## Ghi chú
- Endpoint `public/subjects` (khóa học) hiện cũng lọc tương tự — chưa đụng tới,
  chờ xác nhận nếu cần áp dụng cùng quy tắc.

### Checkpoint — 2026-06-04
Vừa hoàn thành: sửa BE route + controller, verify count đúng (guest 2 / employee 5)
Đang làm dở: không
Bước tiếp theo: test thực tế trên trình duyệt với tài khoản HRM SSO
Blocked:
