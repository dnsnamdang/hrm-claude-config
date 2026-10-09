# Fix N+1 load tồn được xuất — màn tạo Phiếu xuất hàng (product_exports)

## Bối cảnh
Màn `admin/warehouse/product_exports/create`. Sau khi chọn kho kế toán cho từng dòng hàng,
class `ProductExportLotAccounting.updateStock()` bắn **1 POST riêng cho MỖI (sản phẩm × kho kế toán)**
tới `warehouseInfo.accountingStockOfProduct`. Phiếu nhiều hàng → bùng nổ request đồng thời
(mỗi request còn phủ overlay loading toàn trang) → lỗi khi quá nhiều hàng hoá.

Điểm bùng nổ:
- Edit mode: constructor mỗi acc gọi `updateStock()` khi load phiếu cũ.
- `autoFillAccWarehouse`: auto-fill kho đầu cho tất cả sản phẩm → loop `acc.updateStock()`.

## Giải pháp
Gộp tất cả `updateStock()` phát sinh trong cùng 1 tick thành **1 request batch** (debounce hàng đợi tĩnh),
không đổi công thức tính tồn (giữ nguyên hành vi, kể cả biểu thức `Math.min` cũ).

## Tasks
- [x] BE: thêm `WarehouseInfosController@accountingStockOfProducts` (số nhiều) — nhận `items[]`, lặp đúng logic bản đơn (nhánh firm_contract is_zt / getAccountingStockDetail), trả `data[]` theo đúng thứ tự item. Cache FirmContract theo id.
- [x] Route: `POST warehouse_infos/accountingStockOfProducts` → `warehouseInfo.accountingStockOfProducts`.
- [x] FE `ProductExportLotAccounting.blade.php`: `updateStock()` → enqueue vào hàng đợi tĩnh + `setTimeout(30ms)` flush 1 lần; tách `applyStockResponse(data)` giữ NGUYÊN công thức; static `enqueueStock`/`flushStock`; khởi tạo `_stockQueue/_stockTimer` ngoài class.
- [x] Giữ nguyên các call site (`accountingWarehouseChange`, `autoFillAccWarehouse`, constructor edit) — không sửa.
- [x] `php -l` BE + routes sạch; tinker smoke test: batch 1 item KHỚP 100% bản đơn; batch 3 item đúng thứ tự + item thiếu product_id trả null.

### Checkpoint — 2026-08-18
Vừa hoàn thành: gộp N+1 load tồn được xuất thành 1 request batch (BE endpoint mới + route + FE debounce queue). Verified qua tinker trên erp_new.
Đang làm dở: (không).
Bước tiếp theo: user test thật trên trình duyệt màn tạo phiếu nhiều hàng (vd warehouse_export_id=28532) — chọn/auto-fill kho kế toán, xác nhận chỉ còn 1 request `accountingStockOfProducts` và tồn hiển thị đúng.
Blocked:
