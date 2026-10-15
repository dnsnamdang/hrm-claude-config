# Plan — Fix cột "SL bạn đang giữ / NV khác giữ" popup Công thức lắp ráp

## Bối cảnh
Popup "Công thức lắp ráp của hàng hóa" ở màn tạo báo giá bán hàng firm-quotation
(`/admin/sale/firm-quotations/create?quotation_type=1`). Admin (emp 13, giữ 0) lại
thấy "SL bạn đang giữ = 17". 17 = tổng NV khác giữ combo 45121 (NV30:7 + NV31:6 + NV44:4).

## Root cause (đã xác nhận code + dữ liệu)
- **Lỗi 1 — Hoán đổi cột ở view** `resources/views/sale/firm/quotations/partials/StockAssemblyModal.blade.php`:
  header dòng 21 "SL NV khác giữ" / dòng 22 "SL bạn đang giữ", nhưng body dòng 36 bind
  `prepick_qty` (thực chất = BẠN giữ) và dòng 37 bind `other_prepick_qty` (= NV khác giữ) → ngược nhãn.
- **Lỗi 2 — Query sai product_id** `app/Http/Controllers/Warehouse/WarehouseInfosController.php@stockAssembly`
  dòng 256 & 263 query `where('product_id', $request->product_id)` (mã COMBO) trong vòng lặp
  từng linh kiện → mọi dòng ra cùng giá trị = giữ của combo, không phải giữ của từng linh kiện.
  (Cột "SL tồn có thể bán" thì đã tính đúng theo từng linh kiện → không nhất quán.)

## Tasks
- [x] Lỗi 1: đổi bind 2 cột trong `StockAssemblyModal.blade.php` (dòng 36/37) cho khớp nhãn header
- [x] Lỗi 2: thêm `rp.product_id as product_id` vào SELECT (dòng 219) + đổi `$request->product_id`
      → `$recipe_product->product_id` (dòng 256 & 263) trong `WarehouseInfosController@stockAssembly`
- [x] `php -l` 2 file — sạch
- [ ] User test browser: admin thấy "SL bạn đang giữ = 0"; mỗi linh kiện hiện giữ riêng
      (Súng 4740: NV khác giữ **8** cty1; Đầu nối 6662: **20** cty1 — đã verify query trên erp_new)

## Checkpoint — 2026-08-20
Vừa hoàn thành: sửa cả 2 lỗi (view swap + query product_id), php -l sạch, verify số kỳ vọng trên erp_new.
Đang làm dở: (không)
Bước tiếp theo: user reload popup Công thức lắp ráp xác nhận admin thấy bạn đang giữ=0; sau đó quyết định commit.
Blocked:

## Không đụng
- `Product::stockCompanies()` / cột "SL tồn có thể bán" (đúng, per-linh-kiện, tách theo công ty)
- Endpoint "SL có thể LR" (`SearchController@searchProductStockBuyer`) — không liên quan
