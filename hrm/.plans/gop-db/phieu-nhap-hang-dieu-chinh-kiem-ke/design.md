# Phiếu nhập hàng điều chỉnh kiểm kê (ERP → HRM) — Design

**Người phụ trách:** @khoipv — 2026-10-30 · Nhánh `develop` (cả 2 repo, nhánh con của `gop_db`)
Plan: `.plans/gop-db/phieu-nhap-hang-dieu-chinh-kiem-ke/plan.md` ·
Spec: `docs/superpowers/specs/gop-db/2026-10-30-phieu-nhap-hang-dieu-chinh-kiem-ke-design.md`

## Mục tiêu

Port màn ERP `Hàng hoá - Dịch vụ - Vận chuyển › Nhập hàng › Phiếu nhập hàng điều chỉnh kiểm kê` (`inventoryImport`,
`InventoryImportsController`, bảng `inventory_imports` + `inventory_import_details` + `inventory_import_detail_acc_warehouses`,
mã `PNHĐCKK-xxxxx`) sang HRM `/finance/inventory-imports`, phân hệ Tài chính › Nhập hàng (mục menu đã khai sẵn).
Đây là bước **Kế toán kho** sau màn đã port "Phiếu nhập kho điều chỉnh kiểm kê" (`/warehouse/inventory-imports`).

## Luồng nghiệp vụ (giữ y ERP)

Phiếu nhập kho ĐCKK **Chờ duyệt** → Kế toán kho bấm "Tạo phiếu nhập hàng" (hoặc Tạo mới + chọn phiếu) → form nạp dòng hàng của
phiếu nhập kho + đơn giá nhập gần nhất → chọn Nhân viên, phân bổ từng dòng vào kho kế toán (tổng SL = SL nhập) →
- **Lưu** (3 Đang tạo): phiếu nhập kho → 2 Đang hạch toán.
- **Lưu và duyệt** (1 Đã hạch toán): cộng tồn kế toán (`accounting_stocks` + log FIFO + `stocks.accounting_qty`) + bút toán
  Nợ 1561 (từng hàng) / Có 3381 (tổng, theo Nhân viên); phiếu nhập kho → 4 Đã hạch toán.
Cả 2 nút: cộng `handled_qty` vào kết quả phiếu kiểm kê, ghi người duyệt / ngày duyệt cho phiếu nhập kho, phiếu kiểm kê →
Hoàn thành (hết việc xử lý) hoặc Đang xử lý.

## Quyết định (user chốt 30/10/2026)

1. **Quyền y ERP** (như 2 màn anh em): 2 quyền xem tên y ERP (`- theo tổng công ty` / `- theo công ty`, type 8 Tài chính);
   không quyền ⇒ chỉ phiếu mình tạo; ẩn phiếu Đang tạo của người khác. Lập phiếu = điều kiện ERP của phiếu nhập kho
   (`canApprove`: Chờ duyệt + "Kế toán kho"). Kiểm bằng trait `ChecksEmployeePermission`, không middleware.
2. **Menu + đường vào**: gắn link mục có sẵn ở Tài chính › Nhập hàng; nút "Tạo phiếu nhập hàng" ở Phiếu nhập kho ĐCKK
   chuyển từ mở ERP sang màn Thêm HRM (`?warehouse_inventory_import_id=`).
3. **Màn Thêm có ô chọn Phiếu nhập kho ĐCKK** (Chờ duyệt) — ERP mở form trống không chọn được.
4. **Các lỗi ERP giữ nguyên ("làm giống ERP")**: Sửa phiếu Đang tạo cộng `handled_qty` lần nữa; không chặn lập trùng; nhận dòng
   hàng FE gửi lên; API lập phiếu không kiểm quyền riêng.

## Phạm vi màn

- Danh sách: STT · Số phiếu · Phiếu nhập kho · Phiếu kiểm kê · Kho · Người tạo · Ngày tạo · Trạng thái · Hành động (y ERP).
  Lọc: Mã phiếu · Kho · Trạng thái · Người tạo · Mã hàng · Tên hàng · Ngày tạo · Công ty–Phòng ban. Tạo mới · Xuất Excel ·
  In danh sách · Cấu hình cột.
- Hành động: Sửa (Đang tạo + người tạo) · In · Lịch sử. Không Xóa (ERP đã comment).
- Form: Phiếu nhập kho · Phiếu kiểm kê · Kho · Thủ kho (người lập phiếu nhập kho) · Nhân viên (*) · Ghi chú · File đính kèm;
  bảng chi tiết y ERP 2 tầng (Tên hàng, Model, Mã hàng, ĐVT, SL nhập, Đơn giá nhập, Thành tiền nhập, Kho kế toán, Số lượng).
- Trạng thái: Đang tạo (xám) · Đã hạch toán (xanh lá) — ERP để Đang tạo đỏ.
