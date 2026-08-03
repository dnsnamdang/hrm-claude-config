# Gộp nhóm hàng hóa trùng tên ở bộ lọc — Danh mục hàng hóa (@namdangit)

**Màn:** `category/product` · **Ngày:** 2026-07-27 · **Loại:** cải tiến filter (FE + 1 chỉnh nhỏ BE, không migration)

## Vấn đề
1 nhóm hàng hóa thuộc nhiều mảng, nhưng DB không có bảng nối — quan hệ là cột đơn `product_groups.array_product_id`. Để "1 nhóm thuộc nhiều mảng", dữ liệu tạo nhiều bản ghi `product_groups` trùng `name` khác `array_product_id`. Nên khi CHƯA chọn mảng, dropdown Nhóm hàng hóa hiện trùng (vd "nước tiểu" 2 lần).

## Mục tiêu
- Chưa chọn mảng → dropdown nhóm gộp trùng theo tên, mỗi tên 1 dòng.
- Chọn nhóm đã gộp → sản phẩm ra ĐỦ của tất cả mảng có nhóm tên đó (không mất dữ liệu).
- Đã chọn mảng → giữ nguyên như cũ. Backward compatible với caller `product_group_id` đơn.

## Quyết định (đã chốt user)
- Không sửa mô hình DL, không bảng nối, không migration.
- **Gộp hiển thị FE + lọc theo nhiều id**: dropdown 1 dòng, khi lọc gửi tất cả id cùng tên dạng `product_group_id[]=...` → backend `whereIn`.

## Thay đổi
- **FE** `pages/category/product/index.vue`:
  - Computed `listProductGroupFilter` (:823-825): thêm nhánh chưa-chọn-mảng → gộp theo `text`.
  - `getData()` (:834-848): nếu chưa chọn mảng + có chọn nhóm → gom mọi id cùng tên, nối tay `product_group_id[]=` vào query (vì `buildQueryString` không tạo `[]`). v-model Select2 vẫn 1 id.
- **BE** `Modules/Category/Services/ProductService.php` (:61-63): nhận `product_group_id` cả mảng lẫn đơn (pattern giống `array_product_id` :53-59).

## Không đụng
DB/migration/dữ liệu; create/update product; các màn khác (backward compatible).

## Spec chi tiết
`docs/superpowers/specs/2026-07-27-product-group-dedup-filter-design.md`
