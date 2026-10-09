# Fix — PLG HĐ mua ngoài: người duyệt đã chọn nhưng báo "không có quyền"

## Bối cảnh
`admin/orders/inland_buy_contract_annex2/{id}/show`. PLG (phụ lục giảm) HĐ mua ngoài đã chọn người duyệt = Đỗ Đăng Hiếu (emp 148), phiếu status=2, nhưng Hiếu vào duyệt → "không có quyền".

## Root cause
`InlandBuyContractAnnex2::canApprove()` (dòng 425) + `canView` (419) check quyền **"Duyệt phụ lục đặt hàng ngoài"** — quyền này **KHÔNG có trong PermissionsTableSeeder** (không tồn tại trong bảng permissions) → `Auth::user()->can(...)` luôn `false` → không ai duyệt được. (Model nhập khẩu `BuyContractAnnex2` dùng đúng quyền tồn tại "Duyệt phụ lục hợp đồng mua hàng" id 376.)

Xác minh prod: PLG id=1 approver_id=148 status=2; Hiếu CÓ quyền 124 "Duyệt hợp đồng đặt hàng ngoài" (qua role); quyền "Duyệt phụ lục đặt hàng ngoài" KHÔNG tồn tại.

## Fix (đã chốt: reuse quyền tồn tại 124)
- [x] Đổi 2 chỗ trong `app/Model/Order/InlandBuyContractAnnex2.php` (canView 419, canApprove 425): "Duyệt phụ lục đặt hàng ngoài" → **"Duyệt hợp đồng đặt hàng ngoài"** (id 124 — quyền route `forApprover` đang dùng, Hiếu đã có). Không cần seed/gán thêm.
- [ ] User test: Hiếu vào duyệt PLG → OK.

Phương án thay thế (không chọn): tạo quyền mới "Duyệt phụ lục đặt hàng ngoài" trong seeder + gán role — tốn công seed + gán trên prod.

## File
- `app/Model/Order/InlandBuyContractAnnex2.php`
