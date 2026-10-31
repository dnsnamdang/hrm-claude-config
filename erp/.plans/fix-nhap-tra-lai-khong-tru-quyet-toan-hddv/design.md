# Fix: Phiếu nhập trả lại (mượn-bán) KHÔNG trừ ở quyết toán HĐ dịch vụ

## Bối cảnh
- User thắc mắc: HĐ dịch vụ **HDDV_TPE_HN_KD1_26_0283_BD.SC.PS-TC.HP** (settlement_contracts id **17492**, WrServiceContract id **7286**) có phiếu nhập trả lại **PNH-15975** ("Nhập hàng bán(khi mượn) trả lại", kho PNK-11717, trả 1 cái SP 13370) nhưng cột XUẤT HÀNG/QUYẾT TOÁN vẫn = 58,164,000, chênh lệch = 0.
- DB kiểm tra: `hrm_erp_gop` (prod gộp, remote). DB local `erp_hrm_check` KHÔNG có HĐ này.

## Nguyên nhân gốc — LỖI CODE THẬT
`app/Model/Warehouse/ProductImport.php:1741` (nhánh `updateWarehouse()` → `$this->is_return` → `type == NHAP_BAN_MUON_TRA_LAI` (=9)):

```php
$contract_item = WrServiceContractItem::query()->find($req_product->contractable_id);
```

`$req_product` là `BorrowSellRequestProduct` — bảng `borrow_sell_request_products` **KHÔNG có cột `contractable_id`** (chỉ có `objectable_id` / `objectable_type` qua `morphTo('objectable')`). Nên `$req_product->contractable_id` = `null` → `find(null)` = `null` → `if ($contract_item)` false → **khối cập nhật dòng hợp đồng bị bỏ qua trong im lặng**.

Hệ quả: khi hoàn thành phiếu nhập trả loại 9:
- ✅ `borrow_sell_request_products.returned_qty += qty` (dòng 1738, dùng `$req_product` trực tiếp) — CHẠY ĐÚNG.
- ❌ `wr_service_contract_items.returned_qty/exported_qty` + `objectable` (= `wr_service_contract_product_items` / `wr_service_contract_merchandises`) — KHÔNG được cập nhật.

Quyết toán (`WrSettlementContractService::discountReturn()`, chỉ áp cho `type_info='settlement'`) đọc `returned_qty` trên `product_repairs->items` (= `WrServiceContractProductItem`). Vì nó = 0 nên không trừ gì → QUYẾT TOÁN = XUẤT HÀNG, chênh lệch 0.

(Cột XUẤT HÀNG `type_info='export'` dùng `quantity - annex_qty`, **theo thiết kế không bao giờ trừ trả lại** — đúng ý đồ.)

## So sánh nhánh khác (xác nhận chỉ nhánh type 9 + WrServiceContract bị)
- Nhánh `BAN_TRA_LAI` (type 4, dòng 1676-1686): `$req_product` là `ProductExportRequestDetail`, dùng cột đúng `wr_service_contract_item_id` → chạy đúng.
- Nhánh type 9 cho `FirmContract` (dòng 1763-1792): dùng where tường minh trên `FirmContractTabProduct` / `BorrowSellRequestTabProduct`, không dựa `contractable_id` → không dính.
- Chỉ **type 9 + contractable_type == WrServiceContract** (dòng 1740-1751) dính bug.

## Fix
1. **Code** `ProductImport.php:1741`: đổi `$req_product->contractable_id` → `$req_product->objectable_id`, và chỉ nhận khi `objectable_type == WrServiceContractItem::class` cho chắc.
2. **Backfill data** (prod `hrm_erp_gop`): 13 dòng lệch / 9 HĐ (xem plan.md). Mỗi dòng: cộng `returned_qty` và trừ `exported_qty` trên `wr_service_contract_items` + `objectable` của nó, bằng đúng `borrow_sell_request_products.returned_qty` chưa được truyền. Idempotent theo guard `i.returned_qty <> bsp.returned_qty`.

## Phạm vi / rủi ro
- 13 dòng BSP returned_qty>0 trỏ `WrServiceContractItem` (12 → product-item, 1 → merchandise); tổng 55 đơn vị; đều `i.returned_qty=0`, `exported_qty >= returned` (không âm sau trừ).
- ⚠️ **Cần hỏi riêng**: một số HĐ có thể đã quyết toán + hạch toán xong ở số CŨ (chưa trừ trả lại). Backfill làm màn quyết toán tính lại số ĐÚNG, nhưng KHÔNG tự sửa bút toán đã ghi. Việc đối chiếu/điều chỉnh bút toán đã posting là quyết định riêng của user — KHÔNG tự động làm.

## Quyết định đã chốt
- User (30/10/2026): làm CẢ hai — fix code + backfill 13 dòng.
