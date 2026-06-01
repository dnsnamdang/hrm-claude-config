# Forgot Password — Design (tóm tắt)

**Mục tiêu:** Nhân viên tự đặt lại mật khẩu từ màn login khi quên, qua link reset gửi email (token 30 phút).

## Luồng
login → "Quên mật khẩu?" → `/forgot_password` (email + captcha ảnh) → BE check tài khoản:
- TH1 (tồn tại + status=1): gửi mail link reset → "Hướng dẫn đặt lại mật khẩu đã được gửi tới email nội bộ."
- TH2 (không / status=0): "Không tìm thấy tài khoản".

Mail → `/reset_password?token&email` (mật khẩu mới + nhập lại, rule 7–20 + 4 yếu tố) → BE verify token (đúng + ≤30p + chưa dùng) → đổi mật khẩu + set `password_changed_at=now()` + xóa token → về `/login`.

## Quyết định chốt (brainstorming 2026-06-01)
- Cơ chế: **link reset token 30p** (không phải mật khẩu random).
- Captcha: **ảnh tự sinh BE** — package `mews/captcha` (API mode, stateless).
- Giữ **2 thông báo TH1/TH2** phân biệt theo mô tả (chấp nhận lộ email tồn tại).
- Tái dùng bảng `password_resets` (không migration mới). Token lưu hash, dùng 1 lần.
- Gửi mail **đồng bộ** (không phụ thuộc queue worker).
- Reset set `password_changed_at` → tích hợp với force-change-password (không bị bắt đổi lại).

## Thay đổi chính
- **Dependency:** `composer require mews/captcha` (cần PHP GD).
- **BE:** 3 route public (captcha, forgot-password, reset-password) + 2 FormRequest + `ResetPasswordMail` + blade mail.
- **FE:** link trên login + 2 màn mới (`forgot_password`, `reset_password`) + 3 store action (getCaptcha/forgotPassword/resetPassword).

**Spec chi tiết:** `docs/superpowers/specs/2026-06-01-forgot-password-design.md`
