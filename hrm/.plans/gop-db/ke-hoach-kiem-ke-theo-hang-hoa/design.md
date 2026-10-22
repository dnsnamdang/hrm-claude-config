# Kế hoạch kiểm kê theo hàng hóa — Tóm tắt

> Người phụ trách: @khoipv · Nhánh: `feat/chuyen-doi-hang-hoa` (checkout từ `gop_db`) · Bắt đầu: 20/10/2026
> Nguồn ERP: `selfInventoryRequest.*` — `Warehouse\SelfInventoryRequestController` (menu Kế toán › Kiểm kê, `?type=all`)
> Màn anh em đã port: `.plans/gop-db/ke-hoach-kiem-ke-theo-vi-tri/` (`pages/finance/position-inventories`)
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-20-ke-hoach-kiem-ke-theo-hang-hoa-design.md`

- **Mục tiêu:** port màn Kế hoạch kiểm kê theo hàng hóa (`self_inventory_requests`) sang Tài chính › Kiểm kê — danh sách, Thêm/Sửa/Chi tiết,
  Xóa, In, Xuất Excel (phiếu + danh sách), Lịch sử. Phiếu kiểm kê theo hàng hóa vẫn ở ERP (nút Lập phiếu mở ERP).
- **Quyết định (user 20/10):** 3 quyền tên y ERP; Xóa = Đang tạo + người tạo; popup chọn hàng dùng chung thêm lọc nhiều kho;
  lỗi ERP giữ y (bỏ nút Làm mới số liệu + ô lọc chết), chỉ sửa lỗi làm thao tác không chạy.
- KHÔNG đổi schema, KHÔNG migration. Khuôn UI = màn Kế hoạch kiểm kê theo vị trí.
