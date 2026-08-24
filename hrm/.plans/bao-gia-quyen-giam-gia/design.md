# Báo giá — Quyền áp dụng giảm giá (Redmine #10789)

@dnsnamdang · nhánh `tpe-develop-assign` · 2026-08-17

## Mục tiêu

Thêm quyền `Cho phép thêm giảm giá trong báo giá` (nhóm **Báo giá**, phân hệ Giao việc). Chỉ user có
quyền mới được chọn phương thức GG và nhập số liệu giảm giá ở màn Tạo mới / Cập nhật báo giá.

## Quyết định đã chốt

1. **Không có quyền → ô GG bị disable, mặc định "Không GG"** (spec yêu cầu disable chứ không ẩn —
   khác quy ước "nút không dùng được thì ẩn", vì đây là **ô nhập** chứ không phải nút).
   Nút "Thêm khoản GG" / xoá khoản GG vẫn **ẩn hẳn** theo quy ước chung.
2. **Dữ liệu giảm giá cũ được giữ nguyên, chỉ xem.** BE chỉ chặn khi payload làm **THAY ĐỔI**
   phương thức GG hoặc số tiền giảm giá — nếu chặn cứng theo "payload có giảm giá > 0" thì user
   không quyền sẽ không lưu nổi báo giá cũ của chính mình (mất dữ liệu / kẹt màn).
3. BE là chốt chặn thật, trả **403** kèm message `Bạn không có quyền áp dụng giảm giá trong báo giá`.

## Thay đổi

| Lớp | File | Nội dung |
| --- | --- | --- |
| Quyền | `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` | Permission id **1107**, group `Báo giá`, type 4, sort_order 10 |
| BE | `Modules/Assign/Services/QuotationService.php` | `assertCanChangeDiscount()` + `discountFingerprint()` / `payloadDiscountFingerprint()` / `sumRowDiscount()`; gọi ở `create()` và `update()` |
| BE | `Modules/Assign/Http/Controllers/Api/V1/QuotationController.php` | `update()` map `Exception(code 403)` → HTTP 403 (đồng bộ `store()` / `copy()`) |
| FE | `pages/assign/quotations/_id/edit.vue` | computed `canApplyDiscount` (đọc `$store.state.permissions`, mặc định false) + `canEditDiscount`; disable ô GG + icon khoá tooltip; mọi ô nhập GG dòng hàng/dịch vụ và section "Giảm giá tổng đơn hàng" theo `canEditDiscount` |

## Cách nhận diện "có thay đổi giảm giá"

So "vân tay" giảm giá giữa payload và bản đang lưu, theo 6 phần rời nhau:
`method` · `products` · `services` · `ship_item` · `ship_alloc` · `order`.
Key nào **không gửi lên** thì lấy giá trị đang lưu (payload PUT là partial). Lệch > 0.009 ở bất kỳ
phần nào → 403. Vân tay cộng gộp cả `%` lẫn tiền vì chỉ dùng để phát hiện thay đổi, không phải số
liệu nghiệp vụ.

## Điều kiện nghiệm thu (theo Redmine)

- AC1 — màn phân quyền có quyền mới ✅ (seeder)
- AC2/AC3 — user có quyền: nhập GG bình thường ✅
- AC4 — user không quyền: ô GG disable, ô nhập GG readonly/ẩn ✅
- AC5 — gọi API lưu với giảm giá > 0 (khác dữ liệu đang lưu) → **403** ✅
