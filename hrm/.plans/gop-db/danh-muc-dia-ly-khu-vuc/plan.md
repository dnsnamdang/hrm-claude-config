# Danh mục địa lý — thêm Khu vực / Quốc gia (Redmine #11573)

@cuong61n · nhánh `gop_db` (code thẳng, cả api + client)

Khu vực / Quốc gia KHÔNG lưu ở quận/huyện, phường/xã, đường/phố — lấy qua Tỉnh/TP (`provinces.area_id`, `provinces.nation_id`). Ô chọn trên form chỉ là ô lọc cha để thu hẹp Tỉnh/TP, không có DB mới.

## Phase 1 — Fix #11573

### BE
- [x] Detail resource Quận/Huyện, Phường/Xã, Đường/Phố trả kèm `area_id` (+ `nation_id`) của tỉnh
- [x] Phường/Xã: lọc `area_id`, cột `area_name` (eager load `province.area`) + cột xuất Excel
- [x] Đường/Phố: join `areas`, lọc `area_id`, cột `area_name` + cột xuất Excel

### FE
- [x] Quận/Huyện: form thêm Quốc gia + Khu vực (lọc Tỉnh/TP); cột Khu vực + Quốc gia có trong Tuỳ chỉnh cột (ẩn mặc định, như cũ)
- [x] Phường/Xã: form thêm Quốc gia + Khu vực; bộ lọc thêm Khu vực; Tuỳ chỉnh cột thêm Khu vực (ẩn mặc định)
- [x] Đường/Phố: form thêm Khu vực; bộ lọc thêm Quốc gia + Khu vực; Tuỳ chỉnh cột thêm Khu vực (ẩn mặc định)

### Checkpoint — 2026-10-05
Vừa hoàn thành: code BE + FE Phase 1 (trên nhánh `gop_db`, chưa commit); BE đã chạy thử qua tinker, FE biên dịch SFC OK
Đang làm dở: —
Bước tiếp theo: test trên trình duyệt (chưa chạy Playwright), commit/push khi user cho phép
Blocked:

## Phase 2 — Khu vực: tên không trùng trong phạm vi quốc gia (user bổ sung 05/10)
- [x] BE `CreateAreasRequest`: unique `name` theo `nation_id` (trước unique toàn hệ thống); bỏ message `required` tự khai, dùng lang file
- [x] BE `AreaService` import: khoá chống trùng (nation_id + tên) ở validate + ghi; test `test_khu_vuc_trung_ten_chi_chan_trong_cung_quoc_gia`
