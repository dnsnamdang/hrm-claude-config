# Sửa lỗi không đăng xuất được (logout SSO) — 12/11/2026

Nhánh `gop_db-fix-logout-sso` (hrm-api, worktree `websites/wt-fix-logout/hrm-api`, tách từ origin/gop_db `e674367d1`).
User cho làm phương án 1 (sửa gốc BE). Merge khi user báo.

## Nguyên nhân (đã tái hiện)
- FE `BasicSubsystem.vue::logoutUser()` gửi `is_tpe: true` (commit `4b0c32aa9`, 07/06/2025).
- BE `AuthNewController::logout()` dòng 269 `explode(',', config('common.logout_urls'))`; `config/common.php`
  `'logout_urls' => env('LOGOUT_URLS') ?? []` (commit `81a0908a3`, 18/04/2025) ⇒ thiếu env là MẢNG.
- PHP 8.1: `explode(',', [])` ném `TypeError` (không phải Exception) ⇒ lọt `catch (\Exception)` ⇒ HTTP 500 ⇒ FE catch chỉ
  console.error, không xoá phiên ⇒ kẹt. PHP 7.4: chỉ Warning ⇒ ErrorException bị bắt ⇒ HTTP 200 "Đăng xuất thất bại" ⇒ FE vẫn
  xoá phiên (nhìn như bình thường, token chưa huỷ, không gọi SSO).
- Bằng chứng: log 12/11 5 lần (NV 13, 09:47–11:00); curl :8070 `is_tpe:true` ⇒ 500, không cờ ⇒ 200.

## Task
- [x] `config/common.php`: `logout_urls` luôn là mảng (tách chuỗi env theo dấu phẩy, bỏ phần tử rỗng).
- [x] `AuthNewController::logout()`: dùng thẳng mảng; lỗi gọi từng URL SSO chỉ ghi log, không chặn đăng xuất; catch `\Throwable`.
- [x] Test `tests/Feature/Auth/LogoutSsoTest.php`: không env ⇒ 200 + token bị huỷ; có env 2 URL ⇒ gọi đủ 2; 1 URL lỗi ⇒ vẫn đăng xuất.
- [x] Kiểm: PHPUnit; chạy API của worktree ở cổng tạm, gọi logout `is_tpe:true` ⇒ 200.

### Checkpoint — 12/11/2026
Vừa hoàn thành: sửa 2 file + test (CHƯA commit). Test trên code CŨ (app wt-tpe-agent) 2/3 trượt đúng 500 TypeError; code MỚI 3/3
(PHP 8.1 và 7.4). API worktree ở :8075: logout is_tpe ⇒ 200, token sau đó ⇒ 401.
Bẫy: worktree mới dùng `vendor` symlink ⇒ Composer resolve realpath ⇒ nạp App\ của worktree khác (test chạy code cũ). Dùng
`cp -Rc` (clone APFS) thay symlink.
Bước tiếp theo: user báo commit / merge vào gop_db. :3070/:8070 (nhánh Agent) vẫn còn lỗi tới khi merge hoặc cherry-pick.
Chưa kiểm: prod có khai LOGOUT_URLS không, prod chuyển PHP 8.1 từ khi nào.

### Checkpoint — 12/11/2026 (user chọn 2)
Commit `46e230411` (nhánh gop_db-fix-logout-sso, chưa push, chưa merge gop_db) + cherry-pick sang gop_db-tpe-smart-agent = `a8e903877`.
Kiểm :8070: test 3/3; logout is_tpe ⇒ 200, token sau ⇒ 401. Playwright :3070 (phiên riêng, JWT mới): bấm "Đăng xuất" ở menu
người dùng ⇒ API 200 ⇒ về /login, localStorage token = null.
Khi merge 2 nhánh vào gop_db: cùng nội dung, git nhận cherry-pick ⇒ không xung đột.
