# Plan — Fix nhập trả lại (mượn-bán) không trừ quyết toán HĐ dịch vụ

## Task
- [x] T1. Sửa code `app/Model/Warehouse/ProductImport.php:1741` — `contractable_id` → `objectable_id` (guard `objectable_type == WrServiceContractItem::class`).
- [x] T2. Viết method backfill idempotent trong `database/seeds/UpdateDB.php`: `fixServiceContractReturnedQtyFromBorrowSell_20261030()`.
- [x] T3. Chạy backfill trên prod `hrm_erp_gop` trong transaction (SQL tương đương, vì .env local ≠ prod) — affected 12 product_items + 1 merchandise + 13 items; verify before/after khớp.
- [x] T4. Verify cơ chế + HĐ 7286 (settlement 17492): status=4 chưa duyệt, KHÔNG có snapshot → show recompute LIVE. XUẤT HÀNG=min(exported+returned,quantity)=3 giữ nguyên; QUYẾT TOÁN=exported_qty=2 (trước 3) → trừ 1 cái SP 13370. Chênh lệch ≠ 0 khi mở lại màn.
- [x] T5. Caveat đã xác định (xem dưới) — chờ user quyết.

## Kết quả / caveat đã nêu (chờ user)
5/9 HĐ có phiếu quyết toán:
- 7286 (settlement 17492, status 4 chờ KT duyệt, no snapshot) → FIXED, hiện ngay khi refresh.
- 2246 (4122, status 6 từ chối, no snapshot) → recompute live, không ảnh hưởng (đã từ chối).
- **1944 (3939), 4860 (13632), 5322 (13557) — status 5 ĐÃ DUYỆT, CÓ snapshot (wr_settlement_contract_details).** Màn show đọc snapshot (`getDataForShow`) → KHÔNG tự đổi; và nếu đã sinh bút toán thì bút toán tính theo số CŨ (chưa trừ trả lại). Backfill KHÔNG tự regenerate snapshot / không sửa bút toán đã posting. → Cần user quyết: có lập lại quyết toán / điều chỉnh bút toán 3 HĐ này không.
- 4 HĐ còn lại (1487, 1490, 5913, 7152) chưa có quyết toán → sẽ đúng khi lập.

## Dữ liệu backfill (13 dòng BSP returned_qty>0, item.returned_qty=0)
9 HĐ: 1487, 1490, 1944, 2246, 4860, 5322, 5913, 7152, 7286.
- 12 dòng objectable = WrServiceContractProductItem
- 1 dòng objectable = WrServiceContractMerchandise (ct 1490, wr_service_contract_items.id=945, objectable_id=208)
Delta mỗi dòng = bsp.returned_qty − item.returned_qty. Cập nhật objectable TRƯỚC rồi tới item.

## Checkpoint — 2026-10-30
Vừa hoàn thành: T1 (sửa code ProductImport.php), T2 (method backfill UpdateDB.php), T3 (backfill prod 13 dòng — committed, verify khớp), T4 (xác nhận cơ chế + HĐ 7286 recompute live), T5 (caveat 3 HĐ đã duyệt). **COMMIT + PUSH gop_db: `c3a3013379`** (rebase sạch lên origin, 2 file).
Đang làm dở: (không).
Bước tiếp theo: user chốt có regenerate/điều chỉnh bút toán 3 HĐ đã duyệt (1944/3939, 4860/13632, 5322/13557) không.
Blocked: (không)
