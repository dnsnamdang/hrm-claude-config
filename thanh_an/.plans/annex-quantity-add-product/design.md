# Thêm hàng hóa mới vào phụ lục thay đổi số lượng

> Người phụ trách: @khoipv | Ngày: 2026-05-08

## Mục tiêu

Cho phép thêm sản phẩm mới từ danh mục hệ thống vào phụ lục thay đổi số lượng (tạo nhóm mới hoặc chọn nhóm cũ, hỗ trợ nhân bản). Khi duyệt, sản phẩm mới được thêm vào `contract_products` và snapshot phiên bản mới.

## Scope

- Tái sử dụng modal `ProductModalWithDuplicate` (đã có sẵn, đang bị comment)
- Sản phẩm mới đánh dấu bằng `contract_product_id = null` + `product_id`
- BE tạo `contract_products` mới khi approve

## Quyết định

1. Không tạo modal mới — dùng lại `ProductModalWithDuplicate`
2. Sản phẩm mới có `contract_qty = 0`, `price = 0`
3. Cho phép 1 phụ lục vừa điều chỉnh qty cũ vừa thêm sản phẩm mới

## Spec chi tiết

→ `docs/superpowers/specs/2026-05-08-annex-quantity-add-product-design.md`
