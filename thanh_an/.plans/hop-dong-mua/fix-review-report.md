# Fix review report — Hợp đồng mua (module Supply)

Ngày: 2026-07-20 · Người thực hiện: @khoipv (fix implementer)

## STATUS: DONE (6/6 fix, php -l pass toàn bộ)

## Tóm tắt từng fix

### C1 (Critical) — Sai định dạng ngày trong DetailPurchaseContractResource
File: `Modules/Supply/Transformers/PurchaseContract/DetailPurchaseContractResource.php`
- `sign_time` và `end_time` chuyển từ `Helper::formatDate` (d/m/Y) sang RAW `Y-m-d` bằng `Carbon::parse(...)->format('Y-m-d')` (null-safe).
- GIỮ nguyên `approved_at`, `sent_at`, `created_at` qua `Helper::formatDate` (chỉ hiển thị).

### I1 (Important) — goods-pool thiếu specification/producer_country/product_trade_name
File: `Modules/Supply/Http/Controllers/Api/V1/PurchaseContractController.php` (method `goodsPool`)
- Sau khi có `$demand` + `$catalog`, gom tất cả `product_id` không rỗng (unique).
- Gọi `SupplyHandlingService::productInfoMap(array_map(fn($id)=>['product_id'=>$id], $ids))`.
- Enrich cả 2 mảng bằng closure `&$item` (unset sau mỗi loop): set `specification`, `producer_country`, `product_trade_name` (map dùng key `trade_name`), fallback về giá trị sẵn có nếu map rỗng.
- Enrich TRƯỚC bước lọc exclude → item còn/không còn đều đúng.

### I2 (Important) — reject không reset sent_at
File: `Modules/Supply/Services/PurchaseContractService.php` (method `rejectApprove`)
- Thêm `'sent_at' => null` vào mảng update. Khi user sửa & Lưu-và-gửi lại (status=2), guard `!alreadySent` trong `update()` đúng → gửi lại thông báo.

### M1 (Minor) — getList bỏ qua sort_by/sort_desc
File: `Modules/Supply/Services/PurchaseContractService.php` (method `getList`)
- Whitelist cột: `code, number, name, sign_time, total_amount, status, created_at`.
- Nếu `sort_by` nằm trong whitelist → `orderBy($sortBy, sort_desc ? 'desc':'asc')`; ngược lại (kể cả cột ngoài whitelist) → mặc định `id desc`. Tránh SQL injection cột.

### M4 (Minor) — HĐ Nguyên tắc vẫn tạo 4 payment_terms mặc định
File: `Modules/Supply/Services/PurchaseContractService.php` (method `syncPaymentTerms`)
- Nhánh tạo default bọc điều kiện: `type === TYPE_THUONG_MAI && payment_mode === 'don' && count()===0`.
- Đã xác nhận `payment_mode` giá trị `'don'` (theo đơn) qua comment migration `create_purchase_contracts_table`.
- HĐ Nguyên tắc → KHÔNG tạo default terms.

### M5 (Minor) — approve/rejectApprove không guard status ở BE
File: `Modules/Supply/Services/PurchaseContractService.php`
- Cả 2 method thêm guard đầu: chỉ chạy khi `status === STATUS_PENDING`, ngược lại `throw new \Exception('Hợp đồng không ở trạng thái chờ duyệt')`. Controller đã bọc try/catch → trả HTTP_BAD_REQUEST.

## Kết quả php -l
- DetailPurchaseContractResource.php — No syntax errors detected
- PurchaseContractController.php — No syntax errors detected
- PurchaseContractService.php — No syntax errors detected

## Concern / lưu ý
- M4: điều kiện `payment_mode === 'don'` chặt hơn yêu cầu tối thiểu. Nếu FE có trường hợp HĐ Thương mại theo đợt (`dot`) cũng cần default terms thì cần nới lại — nhưng theo spec điều khoản TT theo đơn chỉ áp dụng cho mode `don` nên hợp lý.
- I1: `productInfoMap` chỉ set 3 field trade_name/specification/producer_country; các field ghi chú khác (note_quotation...) không được enrich vì ngoài phạm vi review. Nếu popup chọn hàng cần thêm → mở review riêng.
- I1: chưa truyền `contract_id` vào item nên `productInfoMap` chỉ lấy từ bảng `products` (đủ cho 3 field cần), không đụng nhánh contract_products/bid_package_products — đúng ý.
