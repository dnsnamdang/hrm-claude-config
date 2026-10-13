# Danh sách loại phiếu hạch toán — chuyển ERP → HRM

> Người phụ trách: @khoipv · Nhánh: `develop` (checkout từ `gop_db`) · Spec đầy đủ:
> `docs/superpowers/specs/gop-db/2026-10-13-list-bill-accounting-design.md`

## Mục tiêu
Port màn ERP **QTTT › Cấu hình ERP › "Danh sách loại phiếu hạch toán"** (`/systems/list-bill-accounting`,
`SystemController@listBillAccounting`) sang HRM.

## Scope (bám ERP — chỉ XEM)
- ERP chỉ có danh sách, KHÔNG thêm/sửa/xoá/khoá (nút Thêm mới + Xuất excel bị comment trong blade).
- Bảng `list_bill_accountings` (105 dòng cố định, không có `created_by`, `created_at` NULL) — đã có trên DB gộp.
- Cột: STT · Loại phiếu · Phân loại · Hạch toán riêng (dấu ✓).
- Lọc: ô tìm nhanh theo Loại phiếu (thay ô text `name` của ERP) + ô chọn Phân loại (9 giá trị `TYPES`).
- Bổ sung bắt buộc của HRM: Xuất Excel (popup chọn trường), Cấu hình cột.
- KHÔNG có cột Người tạo/Ngày tạo, Hành động, Lịch sử — bảng không có dữ liệu đó, không có thao tác ghi.

## Quyết định (user chốt 13/10/2026)
- Menu: phân hệ **Quản trị hệ thống**, mục cấp 1 ngay dưới "Danh mục mẫu in". Route FE `/admin/list-bill-accountings`.
- **Không gate quyền** (giống ERP — ai đăng nhập cũng xem được).
- BE đặt ở `Modules/Finance` (dữ liệu kế toán), API `GET v1/finance/list-bill-accountings` + `/export`.
