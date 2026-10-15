# Fix: phường "Hạnh Thông" bị id=0 → lỗi market khi lập HĐ

## WHY id=0 (đã xác định)
- Cột `wards.id` là PRIMARY KEY nhưng **KHÔNG AUTO_INCREMENT** (Extra='', Default='0').
- `WardsController::store()` tạo ward `new Ward(); ...->save()` **không set id** → Eloquent insert rơi về default **0**.
- "Hạnh Thông" (crm_id=2651, tạo 2025-08-26 bởi emp 787 Trịnh Thị Lợi) là ward duy nhất tạo qua form này (ward thứ 2 kiểu này sẽ lỗi trùng PK).
- Hệ quả: `delivery_places.ward_id=0`, market check `marketDivisionContract` query `id_ward=0` không match → chặn lập HĐ (báo giá BGBH_TPSG_KV1_26_0812 của Lê Đức Thái).

## Phạm vi ảnh hưởng (erp_new, đã đo)
- 1 row wards id=0 (Hạnh Thông). 8 FK trỏ `wards.id`, **ON UPDATE NO ACTION** → không đổi được PK.
- 12 record trỏ ward 0: 8 delivery_places + 2 customers + 2 hamlets.
  - **Là Hạnh Thông thật (repoint):** delivery_places **38286, 38287, 38303** (địa chỉ có "Hạnh Thông") + 3 phân công `division_market_employee_wards` id_ward=0 (dept 117).
  - **No-ward (giữ 0):** delivery_place 24274 (Gò Vấp p.14), 35594/35623/38397/38400 (không có báo giá), 2 customers, 2 hamlets.
- 4 báo giá mở dính: 0764 (by 553), 0791/0812/0818 (by 547=Thái).

## Fix (đã viết, CHƯA chạy prod — chờ duyệt)
- [x] `UpdateDB::fixWardHanhThong()` — tạo row Hạnh Thông mới ở id hợp lệ (MAX+1), repoint 3 delivery_places + 3 phân công, đổi tên row id=0 → "(Chưa xác định phường)" cho các record no-ward còn lại (giữ FK). Transaction + idempotent. `php -l` sạch.
- [x] Migration `2026_07_15_110000_set_autoincrement_wards_id.php` — bật AUTO_INCREMENT cho `wards.id` (chống tái diễn; form Tạo xã sẽ tự sinh id). `php -l` sạch.
- [x] Chạy `(new \UpdateDB)->fixWardHanhThong()` trên prod → Hạnh Thông = id 13467, dp 38286/38287/38303 + 3 phân công repoint OK, row 0 → "(Chưa xác định phường)". Verify: dp38286 ward=13467; ward 13467 thuộc dept 117 (Phi/Vương/Quyết).
- [ ] Deploy migrate `set_autoincrement_wards_id` trên prod (chống tái diễn).

## Quyết định nghiệp vụ (user xác nhận: Thái CÓ phụ trách Gò Vấp/Hạnh Thông)
- [x] `UpdateDB::assignWardHanhThongToThai()` — chèn phường 13467 vào phân công HCM của Thái
  (province row 5547, dme 2273, dmde 15, in_charge=1). Đã chạy prod.
  Verify: `marketDivisionContract` cho BG 48643 giờ trả TRUE (query khớp 1 dòng, KH thường) → hết chặn.

## Checkpoint — 2026-07-15
Root cause + phạm vi xác định trên prod erp_new. Fix method + migration viết xong, lint sạch, chưa chạy.
Bước tiếp: chờ user (1) duyệt chạy fix catalog, (2) quyết địa bàn Thái.
