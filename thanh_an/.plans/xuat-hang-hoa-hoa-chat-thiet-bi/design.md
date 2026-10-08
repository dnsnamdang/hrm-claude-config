# Xuất DS hàng hóa kèm Hóa chất sử dụng — Design (tóm tắt)

> Người phụ trách: @khoipv · Bắt đầu: 06/10/2026
> Spec chi tiết: [docs/superpowers/specs/2026-10-06-xuat-hang-hoa-hoa-chat-thiet-bi-design.md](../../docs/superpowers/specs/2026-10-06-xuat-hang-hoa-hoa-chat-thiet-bi-design.md)
> Chức năng xuất kèm **Thiết bị sử dụng** đã bỏ theo yêu cầu user (06/10/2026).

## Mục tiêu
Màn Danh mục › Hàng hóa thêm chức năng xuất Excel DS hàng hóa kèm **Hóa chất sử dụng**.

## Quyết định lớn
- Nút "Xuất excel" → dropdown 2 mục (mục cũ giữ nguyên + mục mới).
- Theo **bộ lọc hiện tại** + phân quyền sẵn có của list.
- **Chỉ xuất hàng có ≥ 1 hóa chất.**
- Bố cục **xếp dọc**: dòng cha STT `1` (đậm, nền xanh nhạt), dòng con `1.1`, `1.2` cùng bộ cột: STT · Tên · Mã hàng hóa · Chủng loại · Quy cách · Mã nội bộ · Hãng, nước sản xuất.
- Dòng con lấy thông tin từ hàng hóa liên kết (`object_id`), mất liên kết thì dùng bản sao trong `product_chemicals`.
- BE: API `GET category/products/export-chemicals` dùng lại `ProductService::index()` (không sửa hàm dùng chung), trả JSON; FE dựng file ExcelJS qua helper `utils/exportProductChemicals.js`.
- Không migration, không thêm quyền, không cho chọn cột.
