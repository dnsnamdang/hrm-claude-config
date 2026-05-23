# Design: Elearning Auth (v2 — 2026-05-20)

> **Lưu ý:** Spec này thay thế phiên bản 2026-05-12. Code đã viết trước đó sẽ bị xóa/ghi đè (migration cũ chưa chạy → an toàn). Chi tiết cleanup ở mục 12 của spec.

## 1. Mục đích

Auth cho ứng dụng Elearning (Vue 3 + Vite). 2 nhóm user:

- **Employee (nhân viên HRM)** — auto-login qua SSO từ `hrm-client` (cùng pattern team đã làm cho CRM, xem `sso.csv`). KHÔNG có form login cho employee ở elearning.
- **Learner (người ngoài)** — đăng ký + đăng nhập bằng email/password ngay tại elearning. Không bắt buộc verify email.

## 2. Quyết định chính

- **Chung 1 BE `hrm-api`, 1 JWT_SECRET**. Employee dùng nguyên JWT của HRM; Learner dùng guard mới `elearning` (cùng secret, claim `user_type=learner`).
- **Bảng mới `elearning_learners`** + `elearning_password_resets` (tách khỏi `employees`).
- **Flow SSO**: elearning chưa auth → redirect `hrm-client/sso/elearning?redirect_page=...` → trang này check trạng thái login HRM:
  - Đã login → redirect về elearning kèm `?token=<jwt>`
  - Chưa login → redirect về elearning kèm `?sso=failed` (hiện màn login learner)
- **Logout**: employee → gọi `hrm-api/users/auth/logout` để invalidate JWT toàn hệ thống. Learner → chỉ logout local.
- **Không verify email**. Có forgot/reset password.

## 3. Scope

- BE: migration mới (2 bảng), Entity, Routes, Middleware, Controller, Service, Request, Resource, Mail reset-password, config guard.
- FE elearning: chỉnh router, store, api util, 5 views (loại bỏ VerifyEmail).
- FE hrm-client: thêm 1 page mới `pages/sso/elearning.vue`.

## 4. Spec chi tiết

→ `docs/superpowers/specs/2026-05-20-elearning-auth-design.md`

## 5. Phụ trách

@manhcuong
