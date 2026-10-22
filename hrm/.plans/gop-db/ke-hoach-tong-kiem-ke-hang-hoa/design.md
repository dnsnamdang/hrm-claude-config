# Kế hoạch tổng kiểm kê hàng hóa — Tóm tắt

> Người phụ trách: @khoipv · Nhánh: `feat/chuyen-doi-hang-hoa` (checkout từ `gop_db`) · Bắt đầu: 20/10/2026
> Nguồn ERP: `selfInventoryRequestAll.*` — `Warehouse\SelfInventoryRequestAllController` (menu Kế toán › Kiểm kê, `?type=all`)
> Màn anh em đã port: `.plans/gop-db/ke-hoach-kiem-ke-theo-hang-hoa/` (`pages/finance/self-inventory-requests`)
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-20-ke-hoach-tong-kiem-ke-hang-hoa-design.md`

- **Mục tiêu:** port màn Kế hoạch tổng kiểm kê hàng hóa (`self_inventory_request_alls`) sang Tài chính › Kiểm kê — danh sách, Thêm/Sửa/Chi tiết,
  Xóa, In (mẫu 290/289), Xuất Excel danh sách, Lịch sử, Lập phiếu → màn HRM Phiếu kiểm kê theo hàng hóa.
- **Form:** Ngày kiểm kê từ–đến, Kho (nhiều), Công ty thuê kho (theo kho), Thành phần tham gia (phòng ban), Nội dung yêu cầu — tất cả bắt buộc.
  2 trạng thái: Đang tạo (xám) → Đã duyệt (xanh lá). Nút Lưu nháp / Lưu và duyệt.
- **Quyết định (20/10):** Nội dung yêu cầu + Thành phần tham gia bắt buộc thật (ERP chỉ gắn *); dùng lại 3 quyền màn anh em (ERP cùng tên);
  bỏ ô lọc chết (Kho / Mã hàng / Tên hàng tra nhầm bảng màn anh em); Xóa chạy được (ERP lỗi); điều kiện Lập phiếu giữ y ERP.
- KHÔNG đổi schema, KHÔNG migration, KHÔNG quyền mới.
