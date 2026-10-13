# Fix: màn "Yêu cầu đặt hàng cần duyệt" rò phiếu chéo công ty

## Vấn đề
Màn `admin/orders/root_order_request/forApprover` ("Chờ tiếp nhận"): user (vd Lê Trung Tiến, cty 4) thấy cả phiếu của công ty khác (cty 1, người mua Bùi Thị Bích Phương), đáng lẽ chỉ thấy phiếu mình được phân công mua.

## Nguyên nhân
`RootOrderRequest::searchByFilter()` tính `$ids` (phiếu user được phân công mua) bằng cách match **brand_id + manufacture_id** của `AssignHistory` (đang mở, buy_employee = user) với phiếu — **KHÔNG lọc công ty**. Cùng 1 brand/hãng được phân công cho người ở nhiều công ty khác nhau → `$ids` kéo luôn phiếu công ty khác.

Cột "Người mua hàng" lại khóa theo `send_company_id` nên hiển thị đúng người của công ty phiếu → lệch với danh sách được thấy.

## Bằng chứng (prod erp_new)
Lê Trung Tiến (id 290, cty 4): `$ids`=1742; phiếu status=3 thấy=75 → 71 thuộc `send_company_id=1`, chỉ 4 thuộc cty 4.

## Fix
`app/Model/Order/RootOrderRequest.php` (~dòng 332) — thêm lọc công ty vào vòng tính `$ids`:
```php
self::where('brand_id', $item->brand_id)
    ->where('manufacture_id', $item->manufactures_id)
    ->where('send_company_id', $item->company_id)   // + lọc đúng công ty phân công
    ->pluck('id')
```
Sửa ở nguồn `$ids` → áp dụng cho cả 3 nhánh (`all` / `for-approved` / else). Kỳ vọng LTT còn 4 phiếu.

## Scope
1 file, 1 dòng. Không đổi data. Không đổi luồng phân công (AssignHistory).
