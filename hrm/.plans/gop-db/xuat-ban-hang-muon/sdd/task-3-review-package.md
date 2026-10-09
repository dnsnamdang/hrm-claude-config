# Task 3 review package (working-tree diff, uncommitted — no-commit ruling)

## Files in scope for Task 3 (T1 seeder + T2 5 child entities excluded — reviewed prior)
- NEW parent entity: Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequest.php
- MODIFIED trait: Modules/Finance/Entities/Concerns/ChecksEmployeePermission.php
- MODIFIED: Modules/Finance/Services/ProductImportRequestService.php
- DELETED old type-9 entity: Modules/Finance/Entities/ProductImportRequest/BorrowSellRequest.php

## git diff (trait + service + deletion), -U12
```diff
diff --git a/Modules/Finance/Entities/Concerns/ChecksEmployeePermission.php b/Modules/Finance/Entities/Concerns/ChecksEmployeePermission.php
index 2b8dd7d07..62d1d7f25 100644
--- a/Modules/Finance/Entities/Concerns/ChecksEmployeePermission.php
+++ b/Modules/Finance/Entities/Concerns/ChecksEmployeePermission.php
@@ -155,13 +155,33 @@ trait ChecksEmployeePermission
 
     /**
      * company_id của nhân viên đăng nhập, hoặc null nếu không xác định được (không gắn
      * employee_info). Trả null tường minh để mọi nơi dùng đều PHẢI tự xử lý case null —
      * tránh bug "cả 2 vế cùng null coi như cùng công ty".
      */
     protected static function currentCompanyId(): ?int
     {
         $companyId = auth()->user()->info->company_id ?? null;
 
         return $companyId !== null ? (int) $companyId : null;
     }
+
+    /**
+     * department_id mà nhân viên hiện tại quản lý (theo company hiện tại).
+     * Lưu ý: chưa xử lý cờ all_department (quản tất cả) — Phase 1 chỉ pluck theo bản ghi cụ thể.
+     */
+    protected static function currentManagedDepartmentIds(): array
+    {
+        $employeeId = auth()->id();
+        if (!$employeeId) {
+            return [];
+        }
+        $companyId = self::currentCompanyId();
+        return DB::table('employee_manage_departments')
+            ->where('employee_id', $employeeId)
+            ->when($companyId, function ($q) use ($companyId) {
+                $q->where('company_id', $companyId);
+            })
+            ->pluck('department_id')
+            ->all();
+    }
 }
diff --git a/Modules/Finance/Entities/ProductImportRequest/BorrowSellRequest.php b/Modules/Finance/Entities/ProductImportRequest/BorrowSellRequest.php
deleted file mode 100644
index fbf0af308..000000000
--- a/Modules/Finance/Entities/ProductImportRequest/BorrowSellRequest.php
+++ /dev/null
@@ -1,122 +0,0 @@
-<?php
-
-namespace Modules\Finance\Entities\ProductImportRequest;
-
-use Illuminate\Database\Eloquent\Model;
-use Illuminate\Support\Facades\DB;
-use Modules\Human\Entities\Employee;
-
-/**
- * Phiếu YÊU CẦU XUẤT BÁN HÀNG MƯỢN — bảng ERP `borrow_sell_requests` trên DB gộp.
- *
- * ⚠️ Chứng từ NGUỒN (chỉ đọc) của loại phiếu nhập **9 — Nhập hàng bán(khi mượn) trả lại**.
- * HRM chưa port màn này (thuộc phân hệ Kho) nên chỉ đọc để dựng form; mọi thay đổi trên phiếu
- * bán hàng mượn vẫn do cổng ERP làm.
- */
-class BorrowSellRequest extends Model
-{
-    protected $table = 'borrow_sell_requests';
-
-    /** Hợp đồng gắn với phiếu — ERP lưu quan hệ đa hình `contractable`. */
-    const CONTRACT_FIRM = 'App\Model\Sale\Firm\Contract\FirmContract';
-    const CONTRACT_WR_SERVICE = 'App\Model\Customers\WrServiceContract';
-
-    public function employee_create()
-    {
-        return $this->belongsTo(Employee::class, 'created_by', 'id');
-    }
-
-    /**
-     * Danh sách phiếu hợp lệ cho popup — port ERP `borrowSellRequest.searchData` + điều kiện
-     * `canReturn()` (:822-839): chỉ phiếu status 1/13, chưa có phiếu nhập trả nào đang dở, và
-     * còn ít nhất 1 dòng chưa trả hết.
-     *
-     * @param  \Illuminate\Http\Request $request
-     * @return \Illuminate\Database\Eloquent\Builder
-     */
-    public static function searchForPicker($request)
-    {
-        $query = self::query()
-            ->with(['employee_create.info'])
-            ->whereIn('status', [1, 13])
-            // canReturn(): đang có phiếu nhập trả chưa hoàn thành -> không cho lập tiếp
-            ->whereNotExists(function ($q) {
-                $q->select(DB::raw(1))
-                    ->from('product_import_requests as pir')
-                    ->whereColumn('pir.borrow_sell_request_id', 'borrow_sell_requests.id')
-                    ->where('pir.is_complete', false);
-            })
-            // canReturn(): còn ít nhất 1 dòng approved_qty > returned_qty
-            ->whereExists(function ($q) {
-                $q->select(DB::raw(1))
-                    ->from('borrow_sell_request_products as bsrp')
-                    ->whereColumn('bsrp.parent_id', 'borrow_sell_requests.id')
-                    ->whereRaw('bsrp.approved_qty > bsrp.returned_qty');
-            });
-
-        if ($request->filled('code')) {
-            $query->where('code', 'like', '%' . $request->get('code') . '%');
-        }
-
-        return $query->orderBy('created_at', 'DESC');
-    }
-
-    /**
-     * Dữ liệu nguồn cho loại 9 — port ERP `BorrowSellRequest::getDataForReturn()` (:246-300).
-     * Chỉ lấy dòng còn nợ trả (`approved_qty > returned_qty`), SL đề xuất = phần chênh.
-     */
-    public static function dataForImport(int $id): array
-    {
-        $request = self::query()->findOrFail($id);
-
-        $products = DB::table('borrow_sell_request_products')
-            ->where('parent_id', $id)
-            ->whereRaw('approved_qty > returned_qty')
-            ->select([
-                'id',
-                'id as borrow_sell_request_product_id',
-                'parent_id',
-                'product_id',
-                'product_name',
-                'code',
-                'model_name',
-                'brand_name',
-                'unit_name',
-                'unit_id',
-                'allocated_price',
-                'price',
-                'extra_price',
-                'rebate_price',
-                'vat_percent',
-                'approved_qty as exported_qty',
-                'returned_qty',
-                DB::raw('1 as detail_type'),
-                DB::raw('approved_qty - returned_qty as qty'),
-            ])
-            ->get();
-
-        // ERP hiện ô "Hợp đồng" + "Ngày xuất" chỉ-đọc khi hợp đồng ĐÃ QUYẾT TOÁN
-        // (form.blade :265-296, cùng khối với loại 4).
-        $contract = ($request->contractable_type ?? null) === self::CONTRACT_FIRM
-            ? DB::table('firm_contracts')->where('id', $request->contractable_id)->first()
-            : null;
-        $isSettlement = $contract && (int) $contract->status === ProductExportRequest::FIRM_CONTRACT_DA_QUYET_TOAN;
-
-        return [
-            'id' => $request->id,
-            'code' => $request->code,
-            // Phiếu bán hàng mượn không gắn kho nhập -> để FE tự hỏi Kho nhập như bình thường.
-            'warehouse_id' => null,
-            'is_export_direct' => false,
-            'is_settlement' => $isSettlement,
-            'contract_code' => $contract->code ?? null,
-            'date_accounting' => null,
-            'customer_id' => $request->customer_id ?? null,
-            'contractable_id' => $request->contractable_id ?? null,
-            'contractable_type' => $request->contractable_type ?? null,
-            'products' => array_map(function ($row) {
-                return (array) $row;
-            }, $products->all()),
-        ];
-    }
-}
diff --git a/Modules/Finance/Services/ProductImportRequestService.php b/Modules/Finance/Services/ProductImportRequestService.php
index f81e5ea9d..39fd7be36 100644
--- a/Modules/Finance/Services/ProductImportRequestService.php
+++ b/Modules/Finance/Services/ProductImportRequestService.php
@@ -1,23 +1,23 @@
 <?php
 
 namespace Modules\Finance\Services;
 
 use App\Helper\CmcS3Helper;
 use Carbon\Carbon;
 use Illuminate\Http\Request;
 use Illuminate\Support\Facades\DB;
 use Illuminate\Support\Facades\Log;
 use Illuminate\Validation\ValidationException;
-use Modules\Finance\Entities\ProductImportRequest\BorrowSellRequest;
+use Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest;
 use Modules\Finance\Entities\ProductImportRequest\InlandProductArrivedNew;
 use Modules\Finance\Entities\ProductImportRequest\ProductArrivedNotify;
 use Modules\Finance\Entities\ProductImportRequest\ProductExportRequest;
 use Modules\Finance\Entities\ProductImportRequest\ProductImportRequest;
 use Modules\Finance\Entities\ProductImportRequest\ProductImportRequestDetail;
 use Modules\Finance\Entities\ProductImportRequest\ProductImportRequestDetailCustomer;
 use Modules\Timesheet\Services\EmployeeInfoService;
 
 /**
  * Phiếu Yêu cầu nhập hàng — Phase 1: danh sách (4 preset) + chi tiết + dữ liệu cho bộ lọc.
  *
  * Phạm vi quyền và toàn bộ filter đã xử lý trong ProductImportRequest::searchByFilter();
```

## NEW FILE (untracked): Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequest.php
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
}
```
