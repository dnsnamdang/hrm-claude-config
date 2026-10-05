# Plan — App báo "Route Not Found!" khi chọn khách hàng (26/09/2026) @namdangit

- [x] BE: khôi phục `GET /api/v1/customers` (bị gỡ ở 931a192d6) — `Modules/Timesheet/Http/Controllers/Api/V1/CustomerController@index` + `CustomerListResource` (lấy từ nhánh tpe), giữ hợp đồng cũ, eager load, trần limit 100 — nhánh `fix/app-customers-route` (worktree `worktrees/app-customers-api`)
- [x] Commit `3ef7509c2` → push `gop_db` → `git pull` prod + `php artisan route:cache` (prod bật route cache từ 25/09 18:30, thiếu bước này route mới vẫn 404) → API 200, total 44.326, tìm "vinfast" 80 KH; app thật gọi 200 từ 08:59
