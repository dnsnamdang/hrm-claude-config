# Task 5 — SourceService: nạp SL khả dụng theo hợp đồng (Firm + WrService)

**Repo:** `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api` (nhánh gop_db, Laravel 8, PHP 7.4, DB gộp erp_hrm_check). Query chạy trên MERGED DB qua default connection — CẤM `mysql2`/`DB_CONNECTION_SECOND`.
**ERP source (chỉ ĐỌC để port logic, KHÔNG sửa):** `/Users/nguyentrancu/DEV/code/ERP-HRM/ERP/TanPhatDev`.

Tạo 1 file: `Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestSourceService.php`.

## Interface phải PRODUCE (Task 6 sẽ consume — giữ chữ ký chính xác)
- `loadFirm(int $contractId, array $tabIds, $vatPercent): array` → `['tabs'=>..., 'products'=>..., 'support_accounting'=>...]`
- `loadWrService(int $contractId): array` → `['products'=>..., 'sum_cost'=>...]`
- `borrowedDetails(array $exportRequestIds, int $productId): \Illuminate\Support\Collection`

## FACT đã xác minh (dùng verbatim — KHÔNG tự đổi)
- **Hệ số**: bảng `product_units` cột hệ số là **`unit_coefficient`** (KHÔNG phải `coefficient`). Bảng `firm_contract_tab_products` ĐÃ CÓ sẵn cột `unit_coefficient` (line-level).
- **XUAT_BAN_HD_HANG = 14** (ExportModel).
- 3 bảng in-flight tồn tại: `product_export_request_tab_products`(perd), `warehouse_export_request_tab_products`(werd), `warehouse_export_requests`(wer), `borrow_sell_request_tab_products`(bsrtp), `borrow_sell_requests`(bsr).
- Cột perd: parent_id,product_export_request_id,firm_contract_id,firm_contract_tab_id,product_id,unit_id,need_export,qty,exported_qty. Cột werd: parent_id,warehouse_export_request_id,firm_contract_id,firm_contract_tab_id,product_id,unit_id,qty,need_export.
- Cột firm_contract_tab_products: quantity,exported_qty,returned_qty,warehouse_exported_qty,price,price_extra,price_with_extra,allocated_price,vat_percent,unit_coefficient,brand_id,code,avatar,product_id,product_name,model_name,unit_id,unit_name,firm_contract_id,parent_id.
- Cột wr_service_contract_items: wr_service_contract_id,type,product_id,product_name,unit_id,root_qty,qty,exported_qty,annex_qty,returned_qty,price,price_extra,price_after_extra,sale_percent,allocated_price,vat_percent.
- Cột product_export_request_details: parent_id,product_id,unit_id,base_exported_qty,borrow_returned_qty,returned_qty,unit_coefficient,firm_contract_tab_product_id,wr_service_contract_item_id.

## Bước 1 — loadFirm + 2 hàm in-flight (ĐÃ trace ERP getExportingQty/getBorrowingQty — port verbatim)

**CHỈNH SỬA quan trọng so với plan**: plan chỉ trừ `exportingQty`. ERP trừ CẢ `getBorrowingQty` (SL phiếu mượn chờ duyệt status=2 chiếm cùng quỹ HĐ). Công thức đúng:
`qty_khả_dụng = quantity - exported_qty - firmExportingQty(...) - firmBorrowingQty(...)`.

```php
<?php
namespace Modules\Finance\Services\BorrowSellRequest;

use Illuminate\Support\Facades\DB;

class BorrowSellRequestSourceService
{
    const XUAT_BAN_HD_HANG = 14;

    // Port FirmContractBorrowSellService::getDataForBorrowSell (nhánh HĐ hãng)
    public function loadFirm(int $contractId, array $tabIds, $vatPercent): array
    {
        $products = DB::table('firm_contract_tab_products')
            ->select('parent_id', 'firm_contract_id', 'product_name', 'model_name', 'brand_id',
                'unit_id', 'unit_name', 'unit_coefficient', 'code', 'avatar', 'product_id', 'price',
                'allocated_price', 'price_with_extra', 'vat_percent')
            ->selectRaw('SUM(quantity) as quantity, SUM(exported_qty) as exported_qty')
            ->where('firm_contract_id', $contractId)
            ->when($vatPercent !== null && $vatPercent !== '', function ($q) use ($vatPercent) {
                $q->where('vat_percent', $vatPercent);
            })
            ->whereIn('parent_id', $tabIds)
            ->groupBy('parent_id', 'firm_contract_id', 'product_name', 'model_name', 'brand_id',
                'unit_id', 'unit_name', 'unit_coefficient', 'code', 'avatar', 'product_id', 'price',
                'allocated_price', 'price_with_extra', 'vat_percent')
            ->get();

        foreach ($products as $p) {
            $exportingQty = $this->firmExportingQty($contractId, (int) $p->parent_id, (int) $p->product_id, null);
            $borrowingQty = $this->firmBorrowingQty($contractId, (int) $p->parent_id, (int) $p->product_id, null);
            $p->unit_coefficient = (float) ($p->unit_coefficient ?: 1);
            $p->extra_price = $p->price_with_extra - $p->price;
            $p->qty = $p->quantity - $p->exported_qty - $exportingQty - $borrowingQty;
            $p->contract_qty = $p->quantity;
        }

        $tabs = DB::table('firm_contract_tabs')->whereIn('id', $tabIds)->get();

        return [
            'tabs' => $tabs,
            'products' => $products,
            'support_accounting' => null, // Phase 1 chưa dùng hạch toán; giữ khoá để Task 6/FE không vỡ
        ];
    }

    /**
     * Port FirmContractTabProduct::getExportingQty($except) — SL YCXH/phiếu kho đang in-flight của 1 item.
     * $exceptExportRequestId: product_export_request_id cần loại (khi sửa phiếu YCXH — Phase 1 tạo mới nên null).
     */
    private function firmExportingQty(int $contractId, int $tabId, int $productId, ?int $exceptExportRequestId): float
    {
        $perQty = DB::table('product_export_request_tab_products as perd')
            ->join('product_export_requests as per', 'perd.product_export_request_id', '=', 'per.id')
            ->leftJoin('warehouse_export_requests as wer', 'wer.product_export_request_id', '=', 'per.id')
            ->where('per.firm_contract_id', $contractId)
            ->where('per.type', self::XUAT_BAN_HD_HANG)
            ->where('per.is_completed', false)
            ->when($exceptExportRequestId, function ($q) use ($exceptExportRequestId) {
                $q->where('per.id', '!=', $exceptExportRequestId);
            })
            ->whereIn('per.status', [2, 7, 10, 11])
            ->where(function ($q) {
                $q->whereNull('wer.id')->orWhere('wer.status', 3);
            })
            ->where('perd.firm_contract_tab_id', $tabId)
            ->where('perd.product_id', $productId)
            ->where('perd.need_export', true)
            ->sum('perd.qty');

        $werQty = DB::table('warehouse_export_request_tab_products as werd')
            ->join('warehouse_export_requests as wer', 'werd.warehouse_export_request_id', '=', 'wer.id')
            ->where('wer.firm_contract_id', $contractId)
            ->where('wer.type', self::XUAT_BAN_HD_HANG)
            ->where('wer.is_complete', false)
            ->where('wer.status', '!=', 3)
            ->where('wer.status', '!=', 5)
            ->where('werd.firm_contract_tab_id', $tabId)
            ->where('werd.product_id', $productId)
            ->where('werd.need_export', true)
            ->sum('werd.qty');

        return (float) $perQty + (float) $werQty;
    }

    /**
     * Port FirmContractTabProduct::getBorrowingQty($except) — SL phiếu YC xuất bán hàng mượn CHỜ DUYỆT (status=2).
     * $exceptBorrowSellRequestId: borrow_sell_request_id đang tạo/sửa cần loại (Phase 1 tạo mới → null).
     */
    private function firmBorrowingQty(int $contractId, int $tabId, int $productId, ?int $exceptBorrowSellRequestId): float
    {
        return (float) DB::table('borrow_sell_request_tab_products as bsrtp')
            ->join('borrow_sell_requests as bsr', 'bsr.id', '=', 'bsrtp.borrow_sell_request_id')
            ->where('bsr.status', 2)
            ->when($exceptBorrowSellRequestId, function ($q) use ($exceptBorrowSellRequestId) {
                $q->where('bsrtp.borrow_sell_request_id', '!=', $exceptBorrowSellRequestId);
            })
            ->where('bsrtp.firm_contract_id', $contractId)
            ->where('bsrtp.firm_contract_tab_id', $tabId)
            ->where('bsrtp.product_id', $productId)
            ->sum('bsrtp.qty');
    }
```

## Bước 2 — loadWrService (port WrServiceContract::getDataForBorrowSell)
Đọc ERP `app/Model/Customers/WrServiceContract.php` — tìm `function getDataForBorrowSell` (khoảng dòng 1763-1801). Port sang query builder. Scaffold plan (giữ, chỉ port đúng phần in-flight `wrExportingQty`):

```php
    public function loadWrService(int $contractId): array
    {
        $products = DB::table('wr_service_contract_items')
            ->where('wr_service_contract_id', $contractId)
            ->where('type', 1)
            ->get([
                'id', 'wr_service_contract_id', 'product_name', 'product_id',
                'root_qty as quantity', 'unit_id', 'exported_qty',
                'price', 'price_extra as extra_cost', 'allocated_price',
                'annex_qty', 'type', 'vat_percent',
                DB::raw('(price_extra / NULLIF(root_qty,0)) as extra_price'),
                DB::raw('(price_after_extra * sale_percent / 100) as rebate_price'),
                DB::raw('id as wr_service_contract_item_id'),
            ]);

        foreach ($products as $p) {
            $p->unit_coefficient = $this->unitCoefficient((int) $p->product_id, (int) $p->unit_id);
            $exportingQty = $this->wrExportingQty((int) $p->id);
            $p->quantity = $p->quantity - $exportingQty - $p->annex_qty;
            $p->contract_qty = $p->quantity;
        }

        return ['products' => $products, 'sum_cost' => 0];
    }
```

**wrExportingQty($itemId)**: ĐỌC logic exporting của WrService trong `getDataForBorrowSell` gốc (ERP) và port trung thực. Nếu ERP tính exporting cho WrService qua `product_export_request_details` (cột `wr_service_contract_item_id`) join `product_export_requests` (cột `wr_service_contract_id`, type in-flight) — port đúng điều kiện lọc phiếu chưa hoàn tất. **Nếu source gốc KHÔNG có exporting riêng cho WrService (chỉ dựa exported_qty + annex_qty)** thì để `wrExportingQty` trả 0 và GHI RÕ trong report là "WrService gốc không trừ in-flight, chỉ exported_qty+annex_qty". KHÔNG bịa điều kiện.

## Bước 3 — unitCoefficient + borrowedDetails
```php
    // Port Product unit coefficient — cột đúng là product_units.unit_coefficient (KHÔNG phải coefficient)
    private function unitCoefficient(int $productId, int $unitId): float
    {
        $coef = DB::table('product_units')
            ->where('product_id', $productId)
            ->where('unit_id', $unitId)
            ->value('unit_coefficient');
        return (float) ($coef ?: 1);
    }

    // Chi tiết đã mượn còn lại (dùng ở Task 6 tính returning_qty)
    public function borrowedDetails(array $exportRequestIds, int $productId)
    {
        return DB::table('product_export_request_details')
            ->whereIn('parent_id', $exportRequestIds)
            ->where('product_id', $productId)
            ->get();
    }
```

## Bước 4 — Verify (chạy, dán output report)
```
php -l Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestSourceService.php

# loadFirm trên 1 HĐ Firm thật (có tab)
php artisan tinker --execute="\$id=DB::table('firm_contract_tabs')->value('firm_contract_id'); \$tabs=DB::table('firm_contract_tabs')->where('firm_contract_id',\$id)->pluck('id')->all(); \$d=(new Modules\Finance\Services\BorrowSellRequest\BorrowSellRequestSourceService)->loadFirm(\$id,\$tabs,''); echo 'firm products='.count(\$d['products']).' tabs='.count(\$d['tabs']); \$p=\$d['products']->first(); if(\$p){ echo ' | sample qty='.\$p->qty.' contract_qty='.\$p->contract_qty.' coef='.\$p->unit_coefficient; } echo PHP_EOL;"

# loadWrService trên 1 HĐ DV thật
php artisan tinker --execute="\$id=DB::table('wr_service_contract_items')->value('wr_service_contract_id'); if(\$id){ \$d=(new Modules\Finance\Services\BorrowSellRequest\BorrowSellRequestSourceService)->loadWrService(\$id); echo 'wr products='.count(\$d['products']).PHP_EOL; } else { echo 'no wr item'.PHP_EOL; }"
```
Kỳ vọng: php -l "No syntax errors"; loadFirm in số products/tabs + sample qty (có thể âm nếu HĐ đã xuất nhiều — không sao, miễn không lỗi); loadWrService in số products không lỗi. DÁN output vào report.

## KHÔNG làm
- KHÔNG commit/push, KHÔNG dispatch subagent, KHÔNG sửa file khác (chỉ tạo 1 file SourceService).
- KHÔNG dùng mysql2/DB_CONNECTION_SECOND. KHÔNG đọc vendor/. KHÔNG sửa ERP.
- KHÔNG viết store/duyệt/searchByFilter (Task 6). KHÔNG bịa cột/điều kiện — bám source ERP + schema đã cho.

## Report
Ghi `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-5-report.md`: đường dẫn file, xác nhận công thức Firm (trừ cả exporting+borrowing), cách port wrExportingQty (có/không in-flight + trích dẫn dòng ERP), output 3 lệnh verify. Trả về (ngắn, KHÔNG dán code): STATUS, 1 dòng verify (firm/wr load OK), concerns (đặc biệt: WrService in-flight port thế nào).
