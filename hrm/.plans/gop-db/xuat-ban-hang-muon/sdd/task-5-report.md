# Task 5 report — BorrowSellRequestSourceService

**File tạo:** `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api/Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestSourceService.php`

## Công thức Firm (loadFirm)
Xác nhận theo brief: `qty = quantity - exported_qty - firmExportingQty(...) - firmBorrowingQty(...)`, trừ CẢ exporting (YCXH/phiếu kho in-flight, `product_export_request_tab_products` + `warehouse_export_request_tab_products`) VÀ borrowing (SL trong `borrow_sell_request_tab_products` của các YC mượn đang `status=2` chờ duyệt). Port verbatim từ brief (đã trace ERP `FirmContractTabProduct::getExportingQty`/`getBorrowingQty`).

## Port wrExportingQty — CÓ in-flight (không phải chỉ exported_qty + annex_qty)
Đọc `ERP/TanPhatDev/app/Model/Customers/WrServiceContractItem.php` dòng 54-80, hàm `getExportingQtyAttribute()` — đây là accessor được gọi ngầm khi `getDataForBorrowSell` (WrServiceContract.php dòng 1788-1797) chạy `$p->exporting_qty = $p->exporting_qty;` trên Eloquent model item (không phải no-op — nó trigger accessor, giá trị này KHÔNG được dùng tiếp ở dòng 1791 vì code gốc gọi lại `$p->exporting_qty` lần 2 trong phép trừ, cùng giá trị).

Logic gốc:
```php
public function getExportingQtyAttribute() {
    $type = $this->type == 0 ? ExportModel::XUAT_BAO_HANH : ExportModel::XUAT_BD_SC; // 16 : 17
    $product_request_qty = ProductExportRequestDetail::from('product_export_request_details as perd')
        ->join('product_export_requests as per', 'perd.parent_id', '=', 'per.id')
        ->leftJoin('warehouse_export_requests as wer', 'wer.product_export_request_id', '=', 'per.id')
        ->where('per.wr_service_contract_id', $this->wr_service_contract_id)
        ->where('per.type',  $type)
        ->where('per.is_completed', false)
        ->whereIn('per.status', [7, 2])
        ->where(function($q) { $q->where('wer.id', null)->orWhere('wer.status', 3); })
        ->where('perd.need_export', true)
        ->where('perd.wr_service_contract_item_id', $this->id)
        ->sum('perd.qty');
    $warehouse_request_qty = WarehouseExportRequestDetail::from('warehouse_export_request_details as werd')
        ->leftJoin('warehouse_export_requests as wer', 'werd.parent_id', '=', 'wer.id')
        ->where('wer.wr_service_contract_id', $this->wr_service_contract_id)
        ->where('wer.type',  $type)
        ->where('wer.is_complete', false)
        ->where('wer.status', '!=', 3)
        ->where('wer.status', '!=', 5)
        ->where('werd.wr_service_contract_item_id', $this->id)
        ->where('werd.need_export', true)
        ->sum('werd.qty');
    return $product_request_qty + $warehouse_request_qty;
}
```
(ERP `app/Model/Customers/WrServiceContractItem.php` dòng 54-80.)

Port sang `wrExportingQty($itemId, $contractId, $itemType)` trong file mới, dùng đúng 2 bảng gốc **`product_export_request_details`** và **`warehouse_export_request_details`** (KHÁC bảng `*_tab_products` dùng ở nhánh Firm — đã verify tồn tại + có cột `wr_service_contract_item_id`, `need_export`, `qty`, `parent_id` qua `Schema::getColumnListing`). `type` xuất được chọn động theo `item.type` (`XUAT_BAO_HANH=16` nếu `type==0`, ngược lại `XUAT_BD_SC=17`) — verify hằng số qua `ERP/TanPhatDev/app/Model/Warehouse/ExportModel.php` dòng 26-27. Dữ liệu thực tế trong DB gộp: `wr_service_contract_items.type` chỉ có giá trị `1` → luôn map ra `XUAT_BD_SC=17` cho tập dữ liệu hiện có, nhưng code giữ nhánh điều kiện đầy đủ để đúng tổng quát.

`annex_qty` vẫn trừ thêm sau exportingQty đúng theo dòng 1791 gốc: `$p->quantity = $p->quantity - $p->exporting_qty - $p->annex_qty;`.

## Output verify (Bước 4)

```
=== php -l ===
No syntax errors detected in Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestSourceService.php

=== loadFirm ===
firm products=16 tabs=1 | sample qty=10 contract_qty=10.00 coef=1

=== loadWrService ===
wr products=1
```

## Ghi chú khác
- Chỉ tạo đúng 1 file như yêu cầu. Không sửa file khác, không commit/push, không dùng mysql2/DB_CONNECTION_SECOND.
- Cột `unit_coefficient` (không phải `coefficient`) dùng đúng theo fact đã cho.
- `borrowedDetails` port nguyên theo brief (query trên `product_export_request_details`).
