# Design: Elearning Auth

## 1. Mục đích
Xây dựng hệ thống auth cho ứng dụng Elearning (Vue 3 + Vite), hỗ trợ 2 loại user:
- **Employee**: nhân viên HRM, đăng nhập bằng email/password có sẵn
- **Learner**: người ngoài, đăng ký mới + xác thực email

Hai app chạy trên domain khác nhau, không share cookie.

## 2. Quyết định chính
- **Phương án A**: tạo bảng `elearning_users` riêng (không ô nhiễm `employees`)
- **1 form login chung**: BE tự nhận biết loại user qua email
- **Multi-guard JWT**: guard `elearning` cho Learner, guard `api` cho Employee
- **Email verification**: bắt buộc cho Learner trước khi login
- **Token chung bảng**: `elearning_verifications` dùng cho cả verify email + reset password (cột `type`)

## 3. Scope
- BE: migration, model, guard, middleware, controller, service, mail
- FE: auth store, router guard, 5 trang auth (login, register, verify, forgot, reset), cập nhật header

## 4. Spec chi tiết
→ `docs/superpowers/specs/2026-05-12-elearning-auth-design.md`

## 5. Người phụ trách
@manhcuong
