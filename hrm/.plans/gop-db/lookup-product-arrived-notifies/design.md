# Tổng hợp phiếu báo hàng về — Design (tóm tắt)

> @khoipv · nhánh `develop` (con `gop_db`) · bắt đầu 14/10/2026
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-10-14-lookup-product-arrived-notifies-design.md`

## Mục tiêu
Port màn ERP "Tổng hợp phiếu báo hàng về" (`warehouseInfo.arrivedNotifies`) sang HRM, phân hệ
**Tra cứu - thông báo → Thông báo → Phiếu báo hàng về** (`/lookup/product-arrived-notifies`).

## Quyết định user chốt (14/10/2026)
1. **Chỉ màn tổng hợp 3 tab** (Nhập khẩu / Trong nước / Mua ngoài). Màn chi tiết phiếu, invoice, hợp đồng chưa port → link ERP tab mới.
2. **Phạm vi như ERP, quyền HRM mới**: tab Nhập khẩu 3 quyền 1709–1711 (tổng công ty / công ty / phòng ban), không quyền = phiếu mình tạo + phiếu thuộc thương hiệu mình phụ trách mua. Tab Trong nước / Mua ngoài không bó (ERP `type=all`).
3. **Hành động giữ đủ như ERP**: tab Nhập khẩu In / Xuất Excel (mở ERP) + Xóa (API HRM). 2 tab còn lại ERP không hiện cột hành động → HRM cũng không.

## Sửa so với ERP (lỗi ERP, có ghi chú)
- Lọc NCC tab Nhập khẩu: ERP lấy nhầm danh sách Kho → dùng NCC.
- Lọc NCC + Tên/mã hàng tab Mua ngoài: ERP đọc cột/bảng rỗng → đọc qua hợp đồng / `product_arrived_notify_products`.
- Xóa: BE kiểm lại điều kiện (ERP chỉ ẩn nút).
- "Người lập" → "Người tạo"; "Đã gửi" màu vàng thay vì đỏ.
