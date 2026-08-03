# Fix — Hàng gửi không cần bảng giá khi duyệt chuyến xe

## Bug
Màn Duyệt chuyến xe (`admin/warehouse/delivery_trips/{id}/approveForm`) với chuyến **hàng gửi** (`is_sent=1`, ischeck=3, cước nhập tay) → bấm Duyệt báo nhầm **"Chưa có bảng giá hiệu lực vận chuyển"** dù hàng gửi không liên quan bảng giá.

## Root cause (đã xác minh DB erp_new + code)
- Message là **toastr FE** ở `resources/views/warehouse/delivery_trips/approveForm.blade.php:217-223`, chặn submit khi `delivery_recipe == 0`.
- `delivery_recipe` nạp qua `getRoadCost()` chỉ chạy khi `ischeck != 3` (dòng 142). Hàng gửi ischeck=3 → không nạp → `delivery_recipe=0` → dính guard.
- BE đã đúng: `approve()` dòng 581 dùng `total_cost_shipping` (cước nhập tay) cho ischeck=3; validate ischeck=3 không đòi bảng giá.
- Trip 4000: is_sent=1, vehicle_category_id=0, vehicle_payload_id=0; công ty 1 thực ra CÓ bảng giá hiệu lực (BGHLVC-00002).

## Fix
- [x] Bọc guard `delivery_recipe` bằng `@if ($status != 3) ... @endif` trong `approveForm.blade.php` (status=3 = hàng gửi). Hàng thường giữ nguyên.
- [ ] User test browser: duyệt chuyến hàng gửi (cước nhập tay) → không còn báo "Chưa có bảng giá hiệu lực", duyệt thành công. Chuyến hàng thường vẫn check như cũ.

## Phạm vi
- FE thuần: `resources/views/warehouse/delivery_trips/approveForm.blade.php` (~217-223). Không đụng BE.
- File này độc lập với các thay đổi bill-adjust đang dở trên nhánh `bill-adjust-dept-them-hd-khach-phong-ban` → commit tách riêng được.
