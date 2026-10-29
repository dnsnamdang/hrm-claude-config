# Design — Rebuild màn Phiếu xuất hàng HRM cho giống ERP

Spec đầy đủ: `HRM/docs/superpowers/specs/gop-db/2026-10-09-product-export-form-rebuild-design.md`

## Tóm tắt
- Một form `create.vue` thống nhất, 2 đường nạp (deep-link / popup) → cùng state, cho **chọn lại nguồn**.
- Bố cục tab giống ERP: Thông tin chung / Vận chuyển (nếu `has_delivery`) / Bốc xếp; card Hàng hóa + tab Nhóm (14/15).
- Cờ ẩn/hiện khớp verbatim ERP: has_customer[1,2,8,12,14,16,17], is_sale[1,11,13,14,16,17], show_allocated_price[1,4,11,13,14,16,17], has_contract[1,2,8,11,13,14,16,17], has_delivery=transition_type==2.
- Khối tài khoản read-only (hardcode) cho loại 1-4 — "tài khoản chỉ hiển thị".
- Loại 15 = Cách A (bám ERP, render tối giản).

## BE (3 việc)
1. Trả `type` trong `warehouse_export` (2 endpoint form-data).
2. Trả đủ 27 field khối Thông tin chung (bảng đầy đủ ở spec §3.2) — HĐ/NVKD/người nhận/người yêu cầu/phòng ban/ngày hạch toán/thủ kho; loại 4: HĐ mua+NCC; loại 7: hệ số điều chuyển; loại 9/10/18/19: field nhập tay TK (account_debt/has, cost_debt_id, work, documents).
3. Trả `tabs` (Nhóm HĐ hãng 14/15) từ firm_contracts + firm_contract_tabs + firm_contract_tab_products (tái dùng FirmContractExportStockService).

## Quyết định đã chốt
- 2026-10-09: loại 9/10/18/19 → phương án **(a) làm đầy đủ** (dựng đủ field EDIT + danh mục accounts_s/cost_debts/works + upload). Không để TODO.

## Ngoài phạm vi
- Hạch toán (đã port 20/21 + bốc xếp). List + detail page (đã khớp ERP).

## Trạng thái
- Chờ user review spec → lập plan (writing-plans) → implement. CHƯA code.
