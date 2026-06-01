# Force Change Password — Design (tóm tắt)

**Mục tiêu:** Buộc đổi mật khẩu mặc định. Lần login đầu cho vào; từ lần 2 trở đi nếu chưa từng đổi → **chặn cứng**, ép sang màn `/change_password` đến khi đổi xong.

**Phạm vi:** Chỉ tài khoản tạo mới sau deploy (tài khoản cũ miễn — backfill khi migrate).

## Quyết định chốt (brainstorming 2026-06-01)
- Điều kiện bắt: `login_count >= 2 && password_changed_at IS NULL`.
- Chặn cứng: enforce cả **FE** (route guard) **lẫn BE** (middleware chặn mọi API trừ updatePass/logout/profile).
- Tái dùng màn `/change_password` có sẵn (không làm popup mới); thêm chế độ "bắt buộc" (banner + nút Đóng = logout).
- Rule mật khẩu mới áp cho **mọi lần đổi**: 7–20 ký tự, đủ 4 yếu tố (số/hoa/thường/đặc biệt), khác `123456@`.
- Dữ liệu cũ: backfill `password_changed_at = now()` → miễn bắt.

## Thay đổi chính
- **DB:** thêm `login_count`, `password_changed_at` vào `employees` + backfill.
- **BE:** `login` (++count + flag `require_change_password`), middleware `MustChangePassword`, refactor `updatePass` sang FormRequest + rule mới + set `password_changed_at`.
- **FE:** login redirect theo flag, route guard, axios 403 interceptor, màn `/change_password` 2 chế độ + validate inline.

**Spec chi tiết:** `docs/superpowers/specs/2026-06-01-force-change-password-design.md`
