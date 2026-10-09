# Task 3 — Entity cha `BorrowSellRequest` + hợp nhất & repoint type-9

**Repo:** `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api` (nhánh gop_db). Laravel 8, PHP 7.4, DB gộp erp_hrm_check.

Task 2 đã tạo 5 child entity trong `Modules\Finance\Entities\BorrowSellRequest`. Nay tạo entity CHA + gộp 2 helper của entity read-only cũ vào entity mới rồi xoá entity cũ và repoint chỗ dùng.

## FACT đã chốt (dùng verbatim, KHÔNG tự đổi)
- Bảng `borrow_sell_requests` KHÔNG có cột `part_id` → boot() CHỈ set `created_by`, `company_id`, `department_id`.
- Employee relation dùng `Modules\Human\Entities\Employee` (khớp entity cũ), KHÔNG dùng Timesheet.
- `product_export_requests()` belongsToMany trỏ `Modules\Finance\Entities\ProductImportRequest\ProductExportRequest` (đã tồn tại).
- Trait `Modules\Finance\Entities\Concerns\ChecksEmployeePermission` đã có: currentEmployeeHasPermission, currentEmployeeIsSuperAdmin, employeeInfoIdsHavingPermission, currentCompanyId. CHƯA có currentManagedDepartmentIds → task này thêm.
- Bảng `employee_manage_departments`: id,employee_id,department_id,company_id,all_department,part_ids,timestamps.
- KHÔNG viết `searchByFilter` trong entity (Task 6 làm trong Service).
- Chỉ 1 file dùng entity cũ: `Modules/Finance/Services/ProductImportRequestService.php` dòng 11 (use). Call site 1022/1574/1597 GIỮ NGUYÊN (cùng tên class + method).

## Bước 1 — Tạo `Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequest.php`

```php
<?php
namespace Modules\Finance\Entities\BorrowSellRequest;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\DB;
use Modules\Human\Entities\Employee;
use Modules\Finance\Entities\Concerns\ChecksEmployeePermission;
use Modules\Finance\Entities\ProductImportRequest\ProductExportRequest;

/**
 * Phiếu YÊU CẦU XUẤT BÁN HÀNG MƯỢN — bảng `borrow_sell_requests` (DB gộp).
 * Phase 1 (HRM): list + tạo + duyệt (KT kho / vượt hạn mức TP→BGD) + từ chối. KHÔNG hạch toán, KHÔNG kho.
 * Đồng thời là chứng từ NGUỒN (chỉ đọc) cho loại phiếu nhập 9 — Nhập bán mượn trả lại
 * (2 helper searchForPicker / dataForImport ở cuối class).
 */
class BorrowSellRequest extends Model
{
    use ChecksEmployeePermission;

    protected $table = 'borrow_sell_requests';
    public $timestamps = true;
    protected $guarded = ['id'];

    // Loại hàng
    const HANG_THUONG = 1;
    const HANG_KM = 2;
    // Trạng thái
    const DA_DUYET = 1;          // Phase 2 mới set
    const CHO_KE_TOAN_KHO = 2;
    const DANG_TAO = 3;
    const KHONG_DUYET = 4;
    const CHO_TP_DUYET = 10;
    const CHO_BGD_DUYET = 11;
    // Loại hợp đồng — lưu chuỗi class ERP để tương thích dữ liệu cũ + ERP đọc chung
    const CONTRACT_FIRM = 'App\Model\Sale\Firm\Contract\FirmContract';
    const CONTRACT_WR_SERVICE = 'App\Model\Customers\WrServiceContract';
    // Tên quyền (verbatim guard web ERP)
    const PERMISSION_KE_TOAN_KHO = 'Kế toán kho';
    const PERMISSION_VIEW_ALL_COMPANY = 'Xem tất cả phiếu yêu cầu xuất bán hàng mượn của tổng công ty';
    const PERMISSION_VIEW_COMPANY = 'Xem tất cả phiếu yêu cầu xuất bán hàng mượn của công ty';
    const PERMISSION_VIEW_DEPARTMENT = 'Xem tất cả phiếu yêu cầu xuất bán hàng mượn của phòng ban';
    const PERMISSION_TP_APPROVE = 'Trưởng phòng duyệt xuất hàng vượt hạn mức công nợ';
    const PERMISSION_BGD_APPROVE = 'Ban giám đốc duyệt xuất hàng vượt hạn mức công nợ';

    protected static function boot()
    {
        parent::boot();
        static::creating(function (self $m) {
            $employeeId = auth()->id();
            if (!$employeeId) {
                return;
            }
            if (empty($m->created_by)) {
                $m->created_by = $employeeId;
            }
            $info = optional(auth()->user())->info;
            if ($info) {
                if (empty($m->company_id)) {
                    $m->company_id = $info->company_id ?? null;
                }
                if (empty($m->department_id)) {
                    $m->department_id = $info->department_id ?? null;
                }
            }
        });
        static::updating(function (self $m) {
            if (auth()->id() && empty($m->updated_by)) {
                $m->updated_by = auth()->id();
            }
        });
    }

    // ===== Relations =====
    public function products()
    {
        return $this->hasMany(BorrowSellRequestProduct::class, 'parent_id', 'id');
    }

    public function details()
    {
        return $this->hasMany(BorrowSellRequestProductDetail::class, 'request_id', 'id');
    }

    public function tabs()
    {
        return $this->hasMany(BorrowSellRequestTab::class, 'parent_id');
    }

    public function product_export_requests()
    {
        return $this->belongsToMany(
            ProductExportRequest::class,
            'borrow_sell_request_has_export_requests',
            'borrow_sell_request_id',
            'product_export_request_id'
        );
    }

    public function employee_create()
    {
        return $this->belongsTo(Employee::class, 'created_by', 'id');
    }

    public function approver()
    {
        return $this->belongsTo(Employee::class, 'approver_id', 'id');
    }

    // ===== Mã phiếu =====
    public function generateCode(): void
    {
        $this->code = 'PYCXBHM-' . str_pad((string) $this->id, 5, '0', STR_PAD_LEFT);
        $this->save();
    }

    // ===== Gate quyền =====
    public function canEdit(): bool
    {
        return $this->status == self::DANG_TAO && $this->created_by == auth()->id();
    }

    public function canView(): bool
    {
        if (self::currentEmployeeIsSuperAdmin()) {
            return true;
        }
        if ($this->status != self::DANG_TAO && self::currentEmployeeHasPermission(self::PERMISSION_KE_TOAN_KHO)) {
            return true;
        }
        if (self::currentEmployeeHasPermission(self::PERMISSION_VIEW_ALL_COMPANY)
            || self::currentEmployeeHasPermission(self::PERMISSION_VIEW_COMPANY)
            || self::currentEmployeeHasPermission(self::PERMISSION_VIEW_DEPARTMENT)) {
            return true;
        }
        return $this->created_by == auth()->id();
    }

    public function canApprove(): bool
    {
        return $this->status == self::CHO_KE_TOAN_KHO
            && self::currentEmployeeHasPermission(self::PERMISSION_KE_TOAN_KHO);
    }

    public function canManagerApprove(): bool
    {
        if ($this->status != self::CHO_TP_DUYET) {
            return false;
        }
        if (!self::currentEmployeeHasPermission(self::PERMISSION_TP_APPROVE)) {
            return false;
        }
        return in_array($this->department_id, self::currentManagedDepartmentIds());
    }

    public function canBoardOfManagerApprove(): bool
    {
        return $this->status == self::CHO_BGD_DUYET
            && self::currentEmployeeHasPermission(self::PERMISSION_BGD_APPROVE);
    }

    public function canDeny(): bool
    {
        return $this->canApprove() || $this->canManagerApprove() || $this->canBoardOfManagerApprove();
    }

    // ===== Tạo lại tabs (Firm) =====
    public function syncTabs(array $tabs): void
    {
        $tabIds = $this->tabs()->pluck('id')->all();
        if (!empty($tabIds)) {
            $tabProductIds = BorrowSellRequestTabProduct::whereIn('parent_id', $tabIds)->pluck('id')->all();
            if (!empty($tabProductIds)) {
                BorrowSellRequestTabProductDetail::whereIn('parent_id', $tabProductIds)->delete();
            }
            BorrowSellRequestTabProduct::whereIn('parent_id', $tabIds)->delete();
            BorrowSellRequestTab::whereIn('id', $tabIds)->delete();
        }
        foreach ($tabs as $tab) {
            $t = new BorrowSellRequestTab();
            $t->parent_id = $this->id;
            $t->firm_contract_id = $this->contractable_id;
            $t->firm_contract_tab_id = $tab['firm_contract_tab_id'];
            $t->name = $tab['name'] ?? null;
            $t->save();
            $t->syncTabProducts($tab['products'] ?? []);
        }
    }

    // ===== 2 helper cho loại phiếu nhập 9 (di chuyển NGUYÊN VĂN từ entity read-only cũ) =====
    // >>> DÁN nguyên văn searchForPicker() và dataForImport() ở Bước 2 vào đây <<<
}
```

## Bước 2 — 2 method type-9 dán vào cuối class (thay dòng comment `>>> DÁN ...`)

Dán CHÍNH XÁC 2 method sau (đã lấy nguyên văn từ entity cũ; chỉ giữ nguyên nội dung, KHÔNG đổi logic):

```php
    /**
     * Danh sách phiếu hợp lệ cho popup loại 9 — port ERP borrowSellRequest.searchData + canReturn().
     */
    public static function searchForPicker($request)
    {
        $query = self::query()
            ->with(['employee_create.info'])
            ->whereIn('status', [1, 13])
            ->whereNotExists(function ($q) {
                $q->select(DB::raw(1))
                    ->from('product_import_requests as pir')
                    ->whereColumn('pir.borrow_sell_request_id', 'borrow_sell_requests.id')
                    ->where('pir.is_complete', false);
            })
            ->whereExists(function ($q) {
                $q->select(DB::raw(1))
                    ->from('borrow_sell_request_products as bsrp')
                    ->whereColumn('bsrp.parent_id', 'borrow_sell_requests.id')
                    ->whereRaw('bsrp.approved_qty > bsrp.returned_qty');
            });

        if ($request->filled('code')) {
            $query->where('code', 'like', '%' . $request->get('code') . '%');
        }

        return $query->orderBy('created_at', 'DESC');
    }

    /**
     * Dữ liệu nguồn cho loại 9 — port ERP BorrowSellRequest::getDataForReturn().
     */
    public static function dataForImport(int $id): array
    {
        $request = self::query()->findOrFail($id);

        $products = DB::table('borrow_sell_request_products')
            ->where('parent_id', $id)
            ->whereRaw('approved_qty > returned_qty')
            ->select([
                'id',
                'id as borrow_sell_request_product_id',
                'parent_id',
                'product_id',
                'product_name',
                'code',
                'model_name',
                'brand_name',
                'unit_name',
                'unit_id',
                'allocated_price',
                'price',
                'extra_price',
                'rebate_price',
                'vat_percent',
                'approved_qty as exported_qty',
                'returned_qty',
                DB::raw('1 as detail_type'),
                DB::raw('approved_qty - returned_qty as qty'),
            ])
            ->get();

        $contract = ($request->contractable_type ?? null) === self::CONTRACT_FIRM
            ? DB::table('firm_contracts')->where('id', $request->contractable_id)->first()
            : null;
        $isSettlement = $contract && (int) $contract->status === ProductExportRequest::FIRM_CONTRACT_DA_QUYET_TOAN;

        return [
            'id' => $request->id,
            'code' => $request->code,
            'warehouse_id' => null,
            'is_export_direct' => false,
            'is_settlement' => $isSettlement,
            'contract_code' => $contract->code ?? null,
            'date_accounting' => null,
            'customer_id' => $request->customer_id ?? null,
            'contractable_id' => $request->contractable_id ?? null,
            'contractable_type' => $request->contractable_type ?? null,
            'products' => array_map(function ($row) {
                return (array) $row;
            }, $products->all()),
        ];
    }
```

## Bước 3 — Thêm `currentManagedDepartmentIds()` vào trait

Sửa file `Modules/Finance/Entities/Concerns/ChecksEmployeePermission.php`, thêm method (đặt cạnh currentCompanyId, dùng `use Illuminate\Support\Facades\DB;` nếu file chưa import — kiểm tra đầu file trước):

```php
    /**
     * department_id mà nhân viên hiện tại quản lý (theo company hiện tại).
     * Lưu ý: chưa xử lý cờ all_department (quản tất cả) — Phase 1 chỉ pluck theo bản ghi cụ thể.
     */
    protected static function currentManagedDepartmentIds(): array
    {
        $employeeId = auth()->id();
        if (!$employeeId) {
            return [];
        }
        $companyId = self::currentCompanyId();
        return DB::table('employee_manage_departments')
            ->where('employee_id', $employeeId)
            ->when($companyId, function ($q) use ($companyId) {
                $q->where('company_id', $companyId);
            })
            ->pluck('department_id')
            ->all();
    }
```

## Bước 4 — Repoint type-9 rồi xoá entity cũ
1. Sửa `Modules/Finance/Services/ProductImportRequestService.php` dòng 11:
   - TỪ: `use Modules\Finance\Entities\ProductImportRequest\BorrowSellRequest;`
   - THÀNH: `use Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest;`
   - Các dòng 1022/1574/1597 (gọi `BorrowSellRequest::dataForImport/searchForPicker`) GIỮ NGUYÊN.
2. Xoá file cũ: `rm Modules/Finance/Entities/ProductImportRequest/BorrowSellRequest.php`
3. `composer dump-autoload -o`

## Bước 5 — Verify (bắt buộc, dán output vào report)
```
# a) Không còn tham chiếu ns cũ
grep -rn --include='*.php' "Entities\\\\ProductImportRequest\\\\BorrowSellRequest" Modules/ || echo "OK: no old refs"

# b) php lint 3 file đụng tới
php -l Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequest.php
php -l Modules/Finance/Entities/Concerns/ChecksEmployeePermission.php
php -l Modules/Finance/Services/ProductImportRequestService.php

# c) Entity mới load + generateCode format đúng (không auth → canView có thể false, miễn không exception)
php artisan tinker --execute="\$m=Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest::query()->first(); echo \$m? ('code='.\$m->code.' status='.\$m->status.' dept='.\$m->department_id) : 'no-row'; echo PHP_EOL;"

# d) Hồi quy type-9: 2 helper vẫn chạy qua class mới
php artisan tinker --execute="\$id=Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest::query()->value('id'); \$d=Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest::dataForImport(\$id); echo 'dataForImport products='.count(\$d['products']).' is_settlement='.var_export(\$d['is_settlement'],true).PHP_EOL; echo 'picker count='.Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest::searchForPicker(request())->limit(1)->count().PHP_EOL;"
```
Kỳ vọng: (a) "OK: no old refs"; (b) 3 file "No syntax errors"; (c) in code `PYCXBHM-...`; (d) dataForImport trả mảng products + searchForPicker chạy không lỗi.

## KHÔNG làm
- KHÔNG viết `searchByFilter` (Task 6). KHÔNG tạo Service/Controller/Resource/Request/Route.
- KHÔNG commit. KHÔNG dispatch subagent.
- KHÔNG sửa file ngoài: entity mới + trait + ProductImportRequestService.php (dòng 11) + xoá entity cũ.
- KHÔNG đổi call site 1022/1574/1597.

## Report
Ghi `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-3-report.md`: nội dung boot(), xác nhận Employee=Human, output 4 lệnh verify (a-d), xác nhận repoint 1 dòng + đã xoá file cũ. Trả về: STATUS, 1 dòng tóm tắt verify c+d, concerns.
