# Phiếu nhập kho (nhập mua hàng từ Phiếu giao hàng) — Design (tóm tắt)

> Người phụ trách: @khoipv · Bắt đầu: 07/11/2026
> Demo gốc: `c:\Users\Admin\Desktop\demo nhập kho\demo-phieu-nhap-kho.html`
> Spec chi tiết: [docs/superpowers/specs/2026-11-07-phieu-nhap-kho-design.md](../../docs/superpowers/specs/2026-11-07-phieu-nhap-kho-design.md)

## Mục tiêu
Sau khi phiếu giao hàng hoàn thành và kho đã nhận hàng, thủ kho của kho nhận lập **phiếu nhập kho**: kiểm đếm SL, nhập lô / HSD / seri, lưu nháp, duyệt → ghi sổ tồn + thẻ kho + thông báo.

## Scope
- Màn **PGH chờ nhập kho** `/warehouse/receipt_queue`
- Màn **Phiếu nhập kho** `/warehouse/receipts` (danh sách) + `/create` + `/:id` (sửa / xem), in 01-VT
- BE `Modules/Warehouse`: 4 bảng PNK + 3 bảng tồn (`stock_balances`, `stock_serials`, `stock_ledgers`), API `/v1/warehouse/receipt-queue`, `/v1/warehouse/receipts`
- Thông báo thủ kho khi PGH hoàn thành có điểm về kho; thông báo khi duyệt PNK

## Quyết định lớn
- Kiểu quản lý lô/seri của hàng hóa (chốt 09/11/2026): cột `products.stock_manage_type`, chọn bắt buộc ở màn Quản lý hàng hóa (mặc định Không quản lý, chỉ hàng hóa thường), khóa đổi khi đã có PNK đã duyệt; danh sách hàng hóa có cột + lọc + Excel. `StockManageType::forProduct()` đọc cột này; dòng PNK snapshot `manage_type`.
- Quyền tạm mở (09/11/2026): config `warehouse.receipt_open_permission` = true → ai cũng làm được mọi thao tác PNK.
- Quyền mới `Xem phiếu nhập kho` (id 526) xem tất cả; thủ kho xem kho mình; Tạo / Sửa / Duyệt / Xóa nháp chỉ thủ kho của kho nhập. Không phân quyền theo cấp.
- Xóa: chỉ phiếu nháp (status 2), thủ kho kho nhập; PGH quay về hàng chờ.
- Duyệt: ghi sổ tồn theo kho / hàng / lô / HSD / mục đích giữ hàng; seri trong kho; thẻ kho. Không hủy duyệt.
- Trạng thái PGH (Phase 3, phương án A + C): Hoàn thành giao hàng có điểm về kho → PGH **Chờ nhập kho** (7); mọi điểm về kho có PNK **đã duyệt** → PGH tự **Hoàn thành** (5). Chi tiết PGH hiện trạng thái nhập kho của từng điểm (Chờ / Đang / Đã nhập kho, suy ra từ PNK) + link PNK. Dữ liệu cũ: migration `Supply/2026_11_07_000003`.
