# Plan — Port 6 loại xuất mới + căn dropdown (HRM)

Thứ tự thi công: **P0 dropdown/label → P1 (19) → P2 (4) → P3 (16/17) → P4 (14/15)**.
Mỗi phase test bằng trình duyệt (tạo phiếu thật) trước khi sang phase sau.

## P0 — Nhãn + hằng số + delivery (nền cho mọi phase) — ✅ DONE
- [x] `Assign/Entities/Warehouse/ProductExportRequest.php`:
  - [x] Sửa `TYPE_NAMES`: 14→"Xuất bán hàng", 15→"Xuất khuyến mại", 4→"Xuất trả nhà cung cấp", 17→"Xuất bán SC - BD" (khớp constant.js).
  - [x] Thêm const `XUAT_TRA_NCC=4, XUAT_BAN_HD_HANG=14, XUAT_KM_HD_HANG=15, XUAT_BAO_HANH=16, XUAT_BD_SC=17, XUAT_THUC_HIEN_HD=19`.
  - [x] `HAS_DELIVERY_TYPE_IDS` = khớp ERP getHasDeliveryTypes (mọi creatable trừ 16).
  - [x] Thêm relation `productImportRequest()` (type 4).
- **CHIẾN LƯỢC LỘ DẦN (an toàn, HRM không có git):** `CREATABLE_TYPE_IDS` chỉ khai loại ĐÃ
  dựng xong luồng Tạo (BE+FE). Mở khoá TỪNG loại khi hoàn tất phase của nó → dropdown chỉ giống
  hệt ERP khi cả 6 loại port xong. Hiện giữ nguyên 8 loại đang chạy (3,6,7,12,18,99,20,21).

## P1 — Type 19 (Xuất thực hiện hợp đồng)
- [ ] Verify ERP type 19: loại HĐ attach + có auto-load dòng không (form.blade has_parent / create.blade getParentInfo).
- [ ] BE `rulesForType(19)`: nhập tay (warehouse + products min:1) + `emplement_contract_id nullable|exists`.
- [ ] BE service: nhánh manual + set `emplement_contract_id/type`.
- [ ] FE `ProductExportRequestForm.vue`: thêm 19 vào MANUAL_TYPES-like + đính ContractSearchModal (KH read-only, không load dòng).
- [ ] Test: tạo phiếu 19, kiểm dữ liệu tab_products/details.

## P2 — Type 4 (Xuất trả nhà cung cấp)
- [ ] BE: `ProductImportRequest::canSupplierReturn($id)` + `getDataForSupplierReturn($id)` (port ERP getDataForReturn).
- [ ] BE endpoint Assign: `GET .../product-export-requests/import-request-lines/{id}` (nạp dòng trả NCC) + tái dùng list `finance/product-import-requests` cho modal.
- [ ] BE `rulesForType(4)`: `product_import_request_id required|exists` + re-check canSupplierReturn; service ghi `product_import_request_id` (cha) + dòng (allocated_price/inland_cost/vat).
- [ ] FE: modal chọn phiếu ĐNNK + bảng SL trả / allocated_price / inland_cost / vat.
- [ ] Test: tạo phiếu 4 từ ĐNNK đủ điều kiện; kiểm chặn khi không đủ điều kiện.

## P3 — Types 16/17 (nguồn HĐ SC-BH)
- [ ] BE: port `canProductExport()` cho WrServiceContract (CustomerCare).
- [ ] BE: mở rộng `BorrowSellRequestSourceService::loadWrService()` (hoặc service Assign mới) — nhánh `items.type=0` (loại 16, không rebate/vat) + giữ `type=1` (loại 17).
- [ ] BE endpoint Assign: search HĐ SC-BH + load dòng theo `type` (16→0 / 17→1).
- [ ] BE `rulesForType`: 17 require `wr_service_contract_id` + delivery; 16 không require, không delivery. Store ghi `wr_service_contract_id` cả 2 + snapshot KH + guard canProductExport.
- [ ] FE: modal chọn HĐ SC-BH + bảng (17 có rebate/vat/delivery, 16 không).
- [ ] Test: tạo phiếu 16 và 17 riêng.

## P4 — Types 14/15 (nguồn HĐ hãng)
- [ ] BE endpoint Assign: search HĐ hãng (bê `PrepickExportContractService::searchContracts`).
- [ ] BE endpoint load `getDataForWarehouseExport`: bước 1 vat_options+tabs; bước 2 dòng — 14 dùng `loadFirm`, 15 viết nhánh combo KM (`firm_contract_combo_group_option_products`, giá 0).
- [ ] BE endpoint `getPromoWarehouse` (kho KM, `promo_warehouse_ids`) cho loại 15.
- [ ] BE `rulesForType(14)`: firm_contract_id/firm_tab_vat_percent/tabs.*/need_repair; `rulesForType(15)`: firm_contract_id/promo_warehouse_id.
- [ ] BE store: ghi cha (firm_contract_id/firm_tab_vat_percent/need_repair/promo_warehouse_id) + snapshot KH + guard canProductExport(14)/canProductExportPromotion(15); dòng vào tab_products(firm_contract_tab_id)+details(giá, 15=0).
- [ ] FE: modal HĐ hãng → chọn tab/VAT → bảng giá (14 có/15=0) + "Cần lắp đặt"(14) + kho KM(15).
- [ ] Test: tạo phiếu 14 (theo tab+VAT, need_repair) và 15 (combo KM, kho KM).

## Ghi chú chung
- Không migration (DB đã đủ cột — verify ở design §3).
- Ghi dòng kép tab_products + details theo khuôn `writeContractLines` hiện có.
- Guard nghiệp vụ (canProductExport/canSupplierReturn/canProductExportPromotion) BẮT BUỘC port, không bỏ.
- Tuân skill `erp-to-hrm-screen`: UI theo chuẩn HRM; hàm nghiệp vụ dùng chung grep trước khi viết, ưu tiên tái dùng service Finance đã port.
