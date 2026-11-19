# Ghi lịch sử company cho hàng hoá khi đổi công ty Hãng sản xuất

## Bối cảnh
Màn sửa Hãng sản xuất (`admin/manufactures/{id}/edit`) khi đổi công ty sẽ cascade
`company_id` mới xuống **tất cả hàng hoá** cùng hãng (`manufacture_id`, `status=1`).
Trước đây vòng lặp chỉ gọi `$p->save()` trần → KHÔNG tạo version, KHÔNG ghi lịch sử,
nên thay đổi company_id hàng loạt này biến mất khỏi lịch sử sản phẩm.

## Hiện trạng code
- `app/Http/Controllers/Sale/ManufacturesController.php@update` dòng 270-275: loop cascade.
- Cơ chế lịch sử sẵn có per-product:
  - `ProductVersion` (bảng `product_versions`) — snapshot JSON mỗi lần sửa.
  - `ProductHistory` (bảng `product_histories`) — diff từng cột, gắn `product_version_id`.
  - `Product::createHistoryRecord($versionId, $column, $old, $new)` đã có case `company_id`
    (Product.php:2192-2194) tự dịch id → tên công ty để hiển thị.
  - `created_by` do model `ProductHistory` tự gán (update luôn có `Auth::user()`).

## Quyết định
- Phương án **A (per-product)**: với MỖI hàng hoá **thực sự đổi** company (cũ ≠ mới),
  tạo 1 `ProductVersion` + ghi `createHistoryRecord('company_id', cũ, mới)`.
- Hàng hoá KHÔNG đổi company → save trần, KHÔNG sinh version rỗng.
- KHÔNG thêm dòng chú thích nguồn "do đổi từ Hãng SX" — hiển thị giống hệt sửa tay
  (user chốt 2026-10-14).
- KHÔNG tạo bảng/màn FE mới — lịch sử hiện ngay ở màn lịch sử từng hàng hoá sẵn có.

## Thay đổi
Chỉ sửa vòng lặp cascade trong `ManufacturesController@update` (dòng 270-275), theo khuôn
tạo version của `ProductsController@update` (dòng 1419-1424).

## Test
Đổi company 1 hãng có vài hàng hoá → kiểm tra `product_histories` sinh đúng N dòng
`company_id` (N = số hàng thực đổi), hàng không đổi không sinh version rỗng.
