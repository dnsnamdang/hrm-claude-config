# Phiếu xuất kho điều chỉnh kiểm kê (ERP → HRM) — Design

**Người phụ trách:** @khoipv — 2026-10-27 · Nhánh `develop` (cả 2 repo, nhánh con của `gop_db`)
Plan: `.plans/gop-db/phieu-xuat-kho-dieu-chinh-kiem-ke/plan.md` ·
Spec: `docs/superpowers/specs/gop-db/2026-10-27-phieu-xuat-kho-dieu-chinh-kiem-ke-design.md`

## Mục tiêu

Port màn ERP `Kho › Xuất kho › Phiếu xuất kho điều chỉnh kiểm kê` (`warehouseInventoryExport`, bảng `warehouse_inventory_exports`,
mã `PXKĐCKK-xxxxx`) sang HRM `/warehouse/inventory-exports`, phân hệ Kho. Đối xứng màn đã port Phiếu nhập kho điều chỉnh kiểm kê.

## Luồng nghiệp vụ (giữ y ERP)

Phiếu kiểm kê hàng hóa có hàng THIẾU (`diff_qty < 0`) → người xử lý bấm "Tạo phiếu xuất kho điều chuyển" → chọn kho → Lưu (3 Đang
tạo) / Gửi duyệt (1 Chờ duyệt: **trừ tồn vật lý ngay theo lô + vị trí**, báo Kế toán kho) → Kế toán kho "Tạo phiếu xuất hàng"
(màn ERP `inventory_exports`, chưa port — mở ERP) → 2 Đang hạch toán / 4 Đã hạch toán. Phiếu kiểm kê nguồn → Đang xử lý.

## Quyết định (user chốt 27/10/2026)

1. **Quyền y ERP**: 2 quyền xem tên y ERP (tổng công ty / công ty; không quyền ⇒ phiếu mình tạo) + "Kế toán kho". Không thêm quyền
   Tạo, không thêm cấp phòng ban. Kiểm bằng trait `ChecksEmployeePermission`, không middleware (khuôn màn nhập ĐCKK).
2. **Ghi tồn giống ERP**: log tồn theo công ty LÔ, log chi tiết lô type 3 (NHAP_DIEU_CHINH) — mở rộng `PhysicalStockWriter::exportLot()`.
3. **Giá cơ sở dùng hàm chung** `ProductPriceReader::retailPrices()` (đã có sẵn); màn Kiểm kê hàng hóa chuyển sang gọi hàm này.

## Phạm vi màn

- Danh sách: STT · Số phiếu · Phiếu kiểm kê · Ngày kiểm kê · Kho · Người tạo · Ngày tạo · Người duyệt · Ngày duyệt · Trạng thái ·
  Hành động. Lọc y ERP: Mã phiếu · Kho · Trạng thái · Người tạo · Mã hàng · Tên hàng · Ngày tạo · Công ty–Phòng ban. Tạo mới
  (màn Thêm có ô chọn Phiếu kiểm kê — HRM thêm 27/10, ERP lỗi 500 ở luồng này) · Xuất Excel · In danh sách · Cấu hình cột.
- Hành động: Sửa (Đang tạo, người tạo) · Tạo phiếu xuất hàng (Chờ duyệt + Kế toán kho → ERP) · In · Lịch sử. Không có Xóa (y ERP).
- Form/Chi tiết: khuôn K1 nhóm kho; bảng chi tiết y ERP (Lô, SL xuất, Đơn giá bán, Thành tiền bán); trạng thái trên tiêu đề trang.
- Menu: Kho › Xuất kho. Lối "chờ duyệt" của ERP (Hàng hóa › Xuất hàng) không khai riêng — Kế toán kho thấy phiếu Chờ duyệt ngay
  trong danh sách (như màn nhập ĐCKK).

## Khác ERP (sửa lỗi)

Dòng hàng lấy lại ở server; khoá phiếu kiểm kê chống lập trùng; Gửi duyệt từ màn Sửa cũng trừ tồn (ERP quên); kiểm tồn vật lý
trước khi trừ (ERP `firstOrFail` → 500 / trừ âm); `canView` chặn 404 (ERP `true`). Chi tiết: spec.
