# Danh mục hàng hoá (Product Catalog) — Tóm tắt

**Ngày:** 2026-06-03
**Phụ trách:** @manhcuong
**Spec chi tiết:** `docs/superpowers/specs/2026-06-03-product-catalog-design.md`

## Scope

Danh mục hàng hoá thuộc module Category. Mỗi sản phẩm có:
- Mã hàng (nhập tự do), tên, hãng SX, nước SX, loại hàng, thông số kỹ thuật, VAT
- Nhiều đơn vị tính, mỗi ĐVT có bảng giá 5 mức (P0/P3/P5/P7/P10), bắt buộc 1 ĐVT cơ bản
- Nhiều hình ảnh (eager upload + preview)

## Quyết định chính

- DB: 2 bảng mới (`products`, `product_units`) + dùng `files` chung cho ảnh
- FE: Form tạo/sửa là router riêng (không popup) do nhiều thông tin
- Upload ảnh: eager upload (chọn file → upload ngay), khi save chỉ gửi file_path
- Permission: Quản lý / Xem danh mục hàng hoá (không phân quyền theo cấp)
- Giá: 5 mức cố định (P0, P3, P5, P7, P10)
- Mã hàng: tự do, không prefix
