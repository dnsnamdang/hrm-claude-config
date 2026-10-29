# Design — Đồng bộ màn CHI TIẾT YCXH với màn Tạo/Sửa (read-only)

Người phụ trách: @dangquang.tom · Nhánh: `gop_db` · Ngày: 2026-10-14

## Mục tiêu

Màn **Chi tiết Yêu cầu xuất hàng** (nhánh `readonly` của `ProductExportRequestForm.vue`) phải trông
**giống màn Tạo/Sửa** cả về bố cục "Thông tin chung" lẫn box "Chi tiết hàng hoá", nhưng **chỉ đọc** —
không có công cụ nhập (checkbox / ô SL / nút Thêm), không có cột-sống tồn kho (Tồn / Đang giữ / Còn lại).

Mục tiêu CHÍNH = **mirror màn create/edit HRM read-only** (KHÔNG copy ERP 1-1). Ảnh ERP user gửi chỉ là
tham chiếu bổ sung về bố cục (1 card Thông tin chung + card Chi tiết dạng tab cho loại bán HĐ hãng).

## Hướng đã chọn: **B** (tái hiện đúng từng biến thể theo loại, BE trả data gom nhóm)

- BE enrich `show()` (1 endpoint) trả thêm field per-type + `product_groups` (gom theo nhóm hàng hóa cho loại 14).
- FE dựng lại nhánh readonly theo loại, tái dùng SCSS `er-table` / `pay-box` / `pnh-tabs` sẵn có.

## Quyết định đã chốt (user "ok" 14/10)

1. **Bỏ cột-sống** Tồn / Đang giữ / Còn lại + mọi công cụ nhập ở màn xem (chỉ hiển thị cột LƯU ĐƯỢC).
2. **Loại 20/21** bảng **phẳng** — KHÔNG dựng cây cha-con (DB detail không lưu quan hệ cha-con).
3. DB `product_export_request_details` chỉ lưu snapshot (qty / exported_qty / returned_qty / prices),
   KHÔNG lưu live stock và KHÔNG lưu approved_qty → readonly chỉ hiện cột lưu được.
   Map nhãn: **Số lượng = qty · Đã xuất = exported_qty · Đã trả = returned_qty**. BỎ "Được duyệt".
4. Loại 14 (Xuất bán HĐ hãng) dựng **b-tabs theo nhóm hàng hóa** (giống ERP tab theo nhóm + giống box create/edit).
5. Field per-type mới gate bằng **check loại tường minh** (như create/edit), KHÔNG qua `showField`
   (field-relevance.js không khai các field này).

## BE — enrich `show()`

File: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php`

- `$products` select thêm `firm_contract_tab_product_id` (để group loại 14).
- Thêm field hiển thị mirror create/edit:
  - Loại 3: `expected_borrow_date` / `return_date` (format dd/mm/yyyy).
  - Loại 6: `import_warehouse_name` (code - name).
  - Loại 14: `firm_contract_id` / `firm_contract_code` / `firm_tab_vat_percent` / `customer_unit` /
    `delivery_place` (tái dùng `firmContractDisplaySnapshot`) + `product_groups`.
- `product_groups` (loại 14): group `$products` theo nhóm hàng hóa.
  Join details.firm_contract_tab_product_id → firm_contract_tab_products.id → .parent_id (= firm_contract_tabs.id)
  → firm_contract_tabs.name. Dạng `[{tab_id, tab_name, lines[]}]`; dòng không khớp tab → tab_id 0, tên 'Hàng hóa'.
- KHÔNG đụng `editData()` / helper dùng chung (chỉ đọc tham chiếu).

## FE — nhánh readonly `ProductExportRequestForm.vue`

- **Thông tin chung:** thêm `.fld` vào các col; đổi nhãn khớp create/sửa ("Loại phiếu"→"Loại yêu cầu",
  "Số hợp đồng"→"Hợp đồng"/"Hợp đồng hãng"/"Hợp đồng / đơn hàng" theo loại); bổ sung per-type read-only:
  loại 14 Nhóm VAT + Chọn nhóm hàng hóa + Tên viết tắt + Địa chỉ giao hàng; loại 7 Gửi đến công ty +
  Chọn kiểu nhập kho + Phiếu yêu cầu chuyển hàng (chips); loại 3 Ngày cần mượn / Ngày trả; loại 6 Kho nhập.
- **Chi tiết hàng hoá:** đổi title "Danh sách hàng hoá" → "Chi tiết hàng hoá"; `detailIsSale` gồm [21, 14];
  loại 14 dựng b-tabs theo `product_groups` (mỗi group 1 bảng cột sale, reuse pay-box tổng); loại 21 bảng phẳng sale;
  loại 20/7/manual bảng phẳng non-sale (có Tổng cộng). BỎ cột-sống + công cụ nhập.

## Verify

Playwright mở ≥1 phiếu mỗi loại (14 / 20-21 / 7 / manual) tại
`http://127.0.0.1:3000/finance/product-export-requests/{id}`.
