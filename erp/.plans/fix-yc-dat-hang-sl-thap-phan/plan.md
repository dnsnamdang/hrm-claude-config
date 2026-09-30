# Fix: YC đặt hàng mua ngoài không cho nhập SL thập phân < 1 (vd 0,07 KG)

@junfoke — Repo `TanPhatDev`, nhánh `master`.

## Bối cảnh
- Màn: Yêu cầu đặt hàng mua ngoài (`/admin/orders/inland_order_requests/forBuyer` → Tạo mới / Sửa),
  bảng **Chi tiết** → cột **Số Lượng**.
- Hiện tượng: nhập `0.07` KG → dưới ô SL báo đỏ **"Không hợp lệ"**, không lưu được.
  Nhập `6.2` thì bình thường.

## Root cause
1. **BE (chính)** — `InlandOrderRequestsController`: rule `products.*.details.*.qty` là
   `required|numeric|min:1`, message của `min` được dịch là **"Không hợp lệ"**
   ⇒ mọi SL < 1 (0,07 / 0,5 / 0,9…) đều bị chặn, dù DB `inland_order_request_product_details.qty`
   là `decimal(12,2)` — hoàn toàn chứa được 0,07.
2. **FE (phụ)** — `form.blade.php`: ô SL `<input type="number" step="0.1">`
   ⇒ 0,07 không phải bội của 0,1, trình duyệt/AngularJS coi là invalid.
3. **Kéo theo** — khi phiếu có SL lẻ < 1 thì bước **duyệt giá / trả duyệt** cũng chặn tiếp vì
   `products.*.buyers.*.qty` cũng đang `min:1` (SL người mua mặc định = SL phiếu).

## Tasks
- [x] BE: `products.*.details.*.qty` `min:1` → `min:0.01` ở `store()` (dòng 559) và `update()` (dòng 697)
- [x] BE: `products.*.buyers.*.qty` `min:1` → `min:0.01` ở `approve()` (dòng 997) và `backApproveSm()` (dòng 1132)
- [x] FE: `form.blade.php:213` `step="0.1"` → `step="0.01"` (khớp `decimal(12,2)` của DB)
- [x] `php -l` sạch, diff gọn 5 dòng, CRLF giữ nguyên
- [ ] User test browser: tạo YC với SL 0,07 KG → lưu nháp / gửi duyệt / duyệt giá đều qua
- [ ] Commit + deploy (user tự làm)

## Ngoài scope (chưa đụng, nêu để user quyết)
- `products.*.suggest_price` và `products.*.supplier_price` vẫn `min:1` — là **giá tiền**, không phải SL,
  chưa có ca lỗi nên giữ nguyên.
- Các màn khác trong hệ thống cũng còn `step="0.1"` / `min:1` cho SL (28 chỗ `step="0.1"`),
  chỉ sửa đúng màn user báo, không sửa đại trà.

### Checkpoint — 2026-09-10
Vừa hoàn thành: sửa 4 rule BE + 1 attribute FE, lint sạch.
Đang làm dở: không.
Bước tiếp theo: user test trên browser rồi commit.
Blocked: không.
