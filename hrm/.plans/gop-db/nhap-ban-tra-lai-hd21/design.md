# Nhập hàng bán trả lại cho HĐ loại 21 — Design (tóm tắt)

> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-08-25-nhap-ban-tra-lai-hd21-design.md`
> Nhánh: `gop_db` · Phụ trách: @namdangit

## Mục tiêu
Mở luồng **Nhập hàng bán trả lại** (import type 4 `BAN_TRA_LAI`) cho hàng đã bán theo **HĐ HRM loại 21** (`XUAT_BAN_HOP_DONG`). **Bắt chước nguyên quy tắc trả lại của loại xuất bán hãng 14 (ERP)**, chỉ đổi nguồn HĐ ERP → HĐ HRM (`Contract` polymorphic).

## Phạm vi
- **Phase 1 (làm ngay)** — nửa trước: lập + validate + duyệt giá phiếu nhập trả lại nguồn loại 21. Tận dụng code type-4 đã port sẵn cho HĐ ERP.
- **Phase 2 (tách sau)** — nửa sau: nhập kho thực + cộng dồn `returned_qty` + hạch toán (gap chung cả tính năng).
- **PENDING** — import type 9 (bán mượn trả) cho loại 21: chờ "phiếu xuất bán hàng mượn" loại 21.

## Quyết định chính
1. Thêm 2 cột `emplement_contract_id/type` vào `product_import_requests` để gắn HĐ HRM.
2. Mở filter chọn nguồn cho loại 21: `type=21 + status=5 (Đã hạch toán) + created_by=self + không phiếu trả treo`. (HRM PER không có status 13.)
3. Validate mirror type 14: `Contract.support_accounting` (dùng chung bảng `firm_support_accountings`), chặn đã quyết toán qua `Contract.status ∈ [11,12]`, SL trả ≤ `exported_qty-returned_qty` (tab_products).
4. Lưu: nguồn loại 21 → chép `emplement_contract_id/type` thay `firm_contract_id`.
5. Duyệt giá tái dùng luồng HRM sẵn có (TP 12 / BKS 10→BGĐ 11, `price_buy_approve`).
6. **Không** đụng nhánh HĐ ERP — mọi thay đổi rẽ theo `type == 21`.

## Hiện trạng đã xác nhận
HĐ HRM loại 21 đã có đủ dữ liệu tương đương type 14: `support_accounting`, khái niệm quyết toán (`Contract.status`/`settlement_contracts.contract_id`), dòng hàng `product_export_request_tab_products` có `qty/exported_qty/returned_qty`. Chỉ khác: không có status 13, cơ chế query quyết toán (khóa thường thay polymorphic).
