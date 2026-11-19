# YCXH — Loại "Xuất khuyến mại" HĐ hãng (type 15), trọn chuỗi

**Người phụ trách:** @dangquang
**Nhánh:** `develop` (cả `hrm-api` và `hrm-client`) — nhánh con của `gop_db`
**Ngày:** 2026-10-16
**Spec chi tiết:** `docs/superpowers/specs/gop-db/2026-10-16-ycxh-xuat-khuyen-mai-type15-design.md`

Port loại xuất **15 (XUAT_KM_HD_HANG — Xuất khuyến mại HĐ hãng)** từ ERP sang HRM, **trọn chuỗi**
YCXH → ĐNXK → PXK → PXH + hạch toán. Đây là loại đầu trong 3 loại port đợt này (15 → 4 → 17,
làm **từng loại một**, xong loại này mới sang loại kế).

## Bối cảnh

- Loại 15 hiện mới có **constant + tên + nằm trong DROPDOWN + FILTERABLE** nhưng **CHƯA** nằm trong
  `CREATABLE_TYPE_IDS` → chọn ở dropdown sẽ bị `store()` chặn 422. Chưa có luồng tạo.
- Loại 14 (Xuất bán hàng HĐ hãng) đã port trọn (pattern `createFromFirmContract` + `writeFirmContractTabs`).
  Loại 15 là **anh em của loại 14**: cùng `firm_contract_id`, snapshot KH, cơ chế tab, chuỗi ĐNXK/PXK/PXH.
- `StockService` đã nhận loại 15 ở khâu trừ tồn (một phần plumbing).
- **Mọi cột cần thiết đã có sẵn** trên 3 bảng YCXH (gộp DB dùng bảng ERP) → **không migration**.
- Data test đủ trên local `erp_hrm_check`: 535 HĐ hãng còn combo KM chưa xuất (1.112 dòng).

## Khác biệt loại 15 so với loại 14 (4 điểm)

1. **Nguồn dòng** = combo khuyến mại `firm_contract_combo_group_option_products` (không phải
   `firm_contract_tab_products`), lọc `take_qty - exported_qty - exporting_qty > 0`, **giá = 0**.
2. **Kho khuyến mại** `promo_warehouse_id` (danh sách = `company.promo_warehouse_ids`).
3. **Hạch toán chỉ giá vốn** (hàng KM giá 0 → không doanh thu/giảm trừ/support_accounting).
4. **Điều kiện tạo** = `canProductExportPromotion` (HĐ hiệu lực + đúng người lập + combo còn hàng).

## Hướng giải quyết (user đã duyệt 2026-10-16)

- Bám **đúng ERP**, dựng loại 15 như anh em loại 14.
- Hạch toán loại 15 **chỉ giá vốn** — khớp ERP.
- Phân quyền **tái dùng quyền YCXH sẵn có** (như loại 14/19/20/21), **không** thêm quyền mới riêng loại 15.
- **Không migration** (cột đã đủ).

## Phạm vi theo tầng

- **Tầng 1 — YCXH**: thêm 15 vào `CREATABLE_TYPE_IDS`; method `createFromFirmContractPromotion()`;
  endpoint load dòng combo KM; validate `canProductExportPromotion` + chặn vượt SL combo; lưu nháp nới.
- **Tầng 2 — ĐNXK**: dùng lại `createFromExportRequest`, bảo đảm pass-through
  `firm_contract_tab_combo_product_id` + `promo_warehouse_id`.
- **Tầng 3 — PXK (ERP)**: generic, không sửa riêng.
- **Tầng 4 — PXH + hạch toán**: trừ tồn kho KM + ghi ngược `exported_qty` về combo; thêm nhánh
  hạch toán giá vốn loại 15 vào `getDataProductExportAccounting`.

## Quyết định đã chốt

- Làm từng loại; loại 15 trước, trọn chuỗi.
- Nguồn dòng = combo KM giá 0; kho KM `promo_warehouse_id`.
- Hạch toán chỉ giá vốn.
- Tái dùng quyền YCXH, không thêm quyền mới.
- Không tạo bảng/migration (ghi thẳng bảng ERP sẵn có — gộp DB).
- Mọi thao tác GHI/seed chỉ trên DB local `erp_hrm_check`; `hrm_erp_gop` là PRODUCTION chỉ đọc.

## Verify (dự kiến)

- `php -l` sạch các file BE sửa; test BE (ProductExportRequest) xanh.
- Playwright `http://127.0.0.1:3000`: tạo YCXH loại 15 từ HĐ hãng có combo (vd firm_contract_id=10626),
  load đúng dòng combo giá 0 + chọn kho KM; gửi duyệt chặn đúng khi combo hết / HĐ hết hiệu lực / sai
  người lập; chạy hết chuỗi tới PXH, kiểm trừ tồn kho KM + ghi ngược exported_qty + bút toán giá vốn.
