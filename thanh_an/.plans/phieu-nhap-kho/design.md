# Phiếu nhập kho (nhập mua hàng từ Phiếu giao hàng) — Design (tóm tắt)

> Người phụ trách: @khoipv · Bắt đầu: 07/11/2026
> Demo gốc: `c:\Users\Admin\Desktop\demo nhập kho\demo-phieu-nhap-kho.html`
> Spec chi tiết: [docs/superpowers/specs/2026-11-07-phieu-nhap-kho-design.md](../../docs/superpowers/specs/2026-11-07-phieu-nhap-kho-design.md)

## Mục tiêu
Sau khi phiếu giao hàng hoàn thành và kho đã nhận hàng, thủ kho của kho nhận lập **phiếu nhập kho**: kiểm đếm SL, tự nhập chi tiết (Số lô · NSX · HSD · SL · Mục đích · Seri), lưu nháp, duyệt → ghi sổ tồn + thẻ kho + thông báo.

## Scope
- Màn **PGH chờ nhập kho** `/warehouse/receipt_queue`
- Màn **Phiếu nhập kho** `/warehouse/receipts` (danh sách) + `/create` + `/:id` (sửa / xem), in 01-VT
- BE `Modules/Warehouse`: 4 bảng PNK + 3 bảng tồn (`stock_balances`, `stock_serials`, `stock_ledgers`), API `/v1/warehouse/receipt-queue`, `/v1/warehouse/receipts`
- Thông báo thủ kho khi PGH hoàn thành có điểm về kho; thông báo khi duyệt PNK

## Quyết định lớn
- **Bỏ kiểu quản lý lô / seri (chốt 19/11/2026)**: hàng hóa không phân Lô+HSD / Lô+HSD+Seri / Seri nữa (không cột `stock_manage_type`, không snapshot `manage_type`). Mọi dòng cùng 1 khối chi tiết, người dùng tự nhập.
- **Validate tự do + vài quy tắc (19/11/2026)**: Lô / NSX / HSD / Seri không bắt buộc; Σ SL chi tiết = SL nhập; HSD ≥ NSX; số seri ≤ SL dòng; seri không trùng trong phiếu / không đã có trong kho; SL nhập < SL thực nhận cần lý do (Khác cần mô tả); > 1 mục đích thì mỗi dòng chọn mục đích, Σ theo mục đích giữ KH ≤ SL còn được nhập; SL nguyên; ≥ 1 dòng SL > 0; ngày nhập ≤ hôm nay. HSD đã qua / cận date (90 ngày) chỉ cảnh báo ở popup Duyệt.
- Quyền tạm mở (chốt lại 19/11/2026): config `warehouse.receipt_open_permission` = true → ai cũng làm được mọi thao tác PNK.
- Quyền mới `Xem phiếu nhập kho` (id 527 trên DB dev) xem tất cả; thủ kho xem kho mình; Tạo / Sửa / Duyệt / Xóa nháp chỉ thủ kho của kho nhập. Không phân quyền theo cấp.
- Xóa: chỉ phiếu nháp (status 2), thủ kho kho nhập; PGH quay về hàng chờ.
- Duyệt: ghi sổ tồn theo kho / hàng / lô / HSD / mục đích giữ hàng; seri trong kho; thẻ kho. Không hủy duyệt.
- Trạng thái PGH (Phase 3, phương án A + C): Hoàn thành giao hàng có điểm về kho → PGH **Chờ nhập kho** (7); mọi điểm về kho có PNK **đã duyệt** → PGH tự **Hoàn thành** (5). Chi tiết PGH hiện trạng thái nhập kho của từng điểm (Chờ / Đang / Đã nhập kho, suy ra từ PNK) + link PNK. Dữ liệu cũ: migration `Supply/2026_11_07_000003`.
