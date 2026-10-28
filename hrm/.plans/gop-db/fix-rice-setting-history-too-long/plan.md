# Fix: Lưu "Thiết lập khi không ăn cơm" lỗi 500 (prod 22/10/2026)

- [x] BE: migration `2026_10_22_000002` đổi `rice_setting_histories.old_value/new_value` varchar(255) → TEXT (chuỗi lịch sử công ty + chức vụ ~700 ký tự)
- [x] Deploy prod (`php artisan migrate`) → nhờ user lưu lại thiết lập
