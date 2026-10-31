# Phiếu xuất hàng điều chỉnh kiểm kê (ERP → HRM) — Design

**Người phụ trách:** @khoipv — 2026-10-30 · Nhánh `develop` (cả 2 repo, nhánh con của `gop_db`)
Plan: `.plans/gop-db/phieu-xuat-hang-dieu-chinh-kiem-ke/plan.md` ·
Spec: `docs/superpowers/specs/gop-db/2026-10-30-phieu-xuat-hang-dieu-chinh-kiem-ke-design.md`

## Mục tiêu

Port màn ERP `Hàng hoá - Dịch vụ - Vận chuyển › Xuất hàng › Phiếu xuất hàng điều chỉnh kiểm kê` (`inventoryExport?type=all`,
`InventoryExportsController`, bảng `inventory_exports` + `inventory_export_details` + `inventory_export_detail_acc_warehouses`,
mã `PXHĐCKK-xxxxx`) sang HRM `/finance/inventory-exports`, phân hệ Tài chính › Xuất hàng (mục menu đã khai sẵn).
Bước **Kế toán kho** sau màn đã port "Phiếu xuất kho điều chỉnh kiểm kê" (`/warehouse/inventory-exports`). Bản đối xứng của
màn "Phiếu nhập hàng điều chỉnh kiểm kê" (`/finance/inventory-imports`, port cùng ngày) — code chép khuôn màn đó.

## Luồng nghiệp vụ (giữ y ERP)

Phiếu xuất kho ĐCKK **Chờ duyệt** → Kế toán kho bấm "Tạo phiếu xuất hàng" (hoặc Tạo mới + chọn phiếu) → form nạp dòng hàng của
phiếu xuất kho (đơn giá = đơn giá bán của phiếu xuất kho, sửa được) → chọn Nhân viên, phân bổ từng dòng vào kho kế toán (tổng SL =
SL xuất, mỗi kho không vượt "SL được xuất" = `in_stock` của `AccountingStockService::detail`) →
- **Lưu** (3 Đang tạo): phiếu xuất kho → 2 Đang hạch toán.
- **Lưu và duyệt** (1 Đã hạch toán): TRỪ tồn kế toán (`accounting_stocks` + log FIFO + `stocks.accounting_qty`) rồi tính
  **đơn giá vốn** từng dòng theo FIFO; **KHÔNG bút toán** (y ERP — xem Quyết định 1); phiếu xuất kho → 4 Đã hạch toán.
Cả 2 nút: cộng `handled_qty` vào kết quả phiếu kiểm kê, ghi người duyệt / ngày duyệt cho phiếu xuất kho, phiếu kiểm kê →
Hoàn thành (hết việc xử lý) hoặc Đang xử lý.

## Quyết định (user chốt 30/10/2026)

1. **Không hạch toán — giống ERP.** Code ERP `saveAccounting` nhân `import_price` (cột KHÔNG có ở `inventory_export_details`)
   ⇒ 0 ⇒ `saveAccountDetail` bỏ vế ≤ 0; phiếu thật PXHĐCKK-00001 không có `account_details`. HRM không gọi ghi bút toán.
2. **Còn lại y màn nhập**: 2 quyền xem tên y ERP (`- theo tổng công ty` / `- theo công ty`, type 8); không quyền ⇒ phiếu mình
   tạo; ẩn phiếu Đang tạo của người khác. Lập phiếu = `canCreateProductExport` của phiếu xuất kho (Chờ duyệt + "Kế toán kho").
   Menu gắn link mục có sẵn; nút "Tạo phiếu xuất hàng" ở Phiếu xuất kho ĐCKK chuyển sang màn Thêm HRM. Màn Thêm có ô chọn phiếu.
   Giữ lỗi ERP: sửa phiếu Đang tạo cộng `handled_qty` lần nữa; không chặn lập trùng; nhận dòng hàng FE gửi.

## Phạm vi màn

- Danh sách: STT · Số phiếu · Phiếu xuất kho · Phiếu kiểm kê · Kho · Người tạo · Ngày tạo · Trạng thái · Hành động.
  Lọc: Mã phiếu · Kho · Trạng thái · Người tạo · Mã hàng · Tên hàng · Ngày tạo · Công ty–Phòng ban. Tạo mới · In · Xuất Excel ·
  Cấu hình cột. Hành động: Sửa (Đang tạo + người tạo) · In · Lịch sử. Không Xóa (ERP đã comment).
- Form: Phiếu xuất kho · Phiếu kiểm kê · Kho · Thủ kho · Nhân viên (*) · Ghi chú · File đính kèm; bảng y ERP (Tên hàng, Model,
  Mã hàng, ĐVT, SL xuất, Đơn giá, Thành tiền, [Chi tiết: Đơn giá vốn, Thành tiền vốn], Kho kế toán, Số lượng, [Form: SL được xuất]).
- Trạng thái: Đang tạo (xám) · Đã hạch toán (xanh lá) — ERP để Đang tạo đỏ.
