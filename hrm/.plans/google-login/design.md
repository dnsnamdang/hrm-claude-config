# Google Login cho Elearning — Tóm tắt Design

> Owner: @junfoke | Ngày: 2026-05-26
> Spec chi tiết: `docs/superpowers/specs/2026-05-26-google-login-design.md`

## Mục tiêu

Thêm chức năng đăng nhập bằng tài khoản Google vào màn login/register elearning.

## Approach

**Google Identity Services (GIS)** — nhẹ nhất, không dependency ngoài:
- FE dùng Google GIS SDK → popup chọn tài khoản → nhận `id_token`
- BE verify token với Google API → tìm/tạo learner → trả JWT

## Quyết định chính

1. **Không dùng Firebase** — overkill, thêm dependency nặng chỉ cho Google login
2. **Không dùng Socialite** — redirect flow không phù hợp SPA
3. **Tự tạo learner mới** nếu email Google chưa tồn tại (email_verified_at = now(), password = null)
4. **`google_id`** (sub) dùng làm key chính, match email chỉ lần đầu
5. **`avatar_url`** riêng biệt với `avatar` (S3) — Google URL là fallback
6. **Nút Google đặt dưới form login**, trước "Chưa có tài khoản?"

## Scope

- 1 migration (2 cột mới)
- BE: 1 request + 1 service method + 1 controller method + 1 route + update resource
- FE: 1 composable mới + 1 store action + update LoginView + RegisterView
