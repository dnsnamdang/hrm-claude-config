# Phiếu điều chuyển vị trí — Tóm tắt

> Người phụ trách: @khoipv · Nhánh: `feat/chuyen-doi-hang-hoa` (từ `gop_db`) · Bắt đầu: 19/10/2026
> Nguồn ERP: `positionTransfer.*` — `Warehouse\PositionTransfersController` (menu Kho › Điều chuyển, `?type=all`)
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-19-phieu-dieu-chuyen-vi-tri-design.md`

## Mục tiêu
Port màn Phiếu điều chuyển vị trí (chuyển hàng giữa 2 vị trí trong cùng kho, theo lô) sang HRM, phân hệ Kho.

## Scope
- Danh sách (lọc, Cấu hình cột, Xuất Excel, Lịch sử) · Tạo / Sửa nháp / Chi tiết · Lưu nháp · Điều chuyển (ghi tồn vật lý) · In phiếu · In dự kiến · File đính kèm.
- Nối nút "Tạo phiếu điều chuyển vị trí" của Phiếu kiểm kê theo vị trí (HRM) sang màn mới.
- Ngoài scope (vẫn ERP): 4 form phụ từ Kiểm kho theo hàng hoá / Tự kiểm kê.

## Quyết định lớn
- 4 quyền tên y ERP, guard api, type 21, kiểm qua `ChecksEmployeePermission`.
- Ghi tồn qua hàm mới `PhysicalStockWriter::transferLot()` (dùng chung).
- Giữ lỗi ERP: phiếu Đang tạo ai xem được cũng sửa/xóa được (user chốt).
- Không migration; Đang tạo = xám, Đã chuyển = xanh.
