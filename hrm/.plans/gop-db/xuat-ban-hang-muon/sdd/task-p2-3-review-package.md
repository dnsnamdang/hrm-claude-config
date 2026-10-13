# Review package — Task P2-3 (BASE 1c103ca → HEAD 2d4bbfe)

## git log --oneline
```
2d4bbfe74 refactor(assign): tách SupportAccountingTrait dùng chung cho hạch toán xuất hàng + bán hàng mượn
```
## git diff --stat
```
 .../Services/Accounting/SupportAccountingTrait.php | 296 +++++++++++++++++++++
 .../Services/ProductExportPostingService.php       | 282 +-------------------
 .../Feature/ProductExportPostingRegressionTest.php |  57 ++++
 3 files changed, 356 insertions(+), 279 deletions(-)
```
## git diff -U6
```diff
diff --git a/Modules/Assign/Services/Accounting/SupportAccountingTrait.php b/Modules/Assign/Services/Accounting/SupportAccountingTrait.php
new file mode 100644
index 000000000..c4191a4d1
--- /dev/null
+++ b/Modules/Assign/Services/Accounting/SupportAccountingTrait.php
@@ -0,0 +1,296 @@
+<?php
+
+namespace Modules\Assign\Services\Accounting;
+
+use Illuminate\Support\Facades\DB;
+use Modules\Assign\Entities\Contract\Contract;
+use Modules\Finance\Entities\Account\AccountDetail;
+
+/**
+ * 8 cụm bút toán bán hàng (doanh thu, thưởng, hoa hồng, TNCN, quỹ rủi ro...) + helper tra tổ chức
+ * (phòng/bộ phận). Cắt nguyên văn từ Modules\Assign\Services\ProductExportPostingService (Task P2-3)
+ * để dùng chung giữa ProductExportPostingService (xuất hàng thường) và BorrowSellPostingService
+ * (xuất bán hàng mượn). KHÔNG sửa logic khi di chuyển.
+ */
+trait SupportAccountingTrait
+{
+    /** cache tra tổ chức trong 1 lần chạy */
+    private $deptCache = [];
+    private $partCache = [];
+
+    // ----------------------------------------------------------------------------------
+    // 8 CỤM BÚT TOÁN — port FirmContractExportService (dịch ::class → key cột thô HRM)
+    // ----------------------------------------------------------------------------------
+
+    /** 1. Doanh thu: Nợ 1311 / Có 5111 + 33311 (giá trị gộp, trước giảm trừ). */
+    private function revenueAccounting($total_price, $vat_cost, Contract $contract, array &$accounts, int &$group): void
+    {
+        $group += 1;
+        AccountDetail::createDataSaveDept($accounts, 1311, $total_price + $vat_cost, AccountDetail::TYPE_DEPT,
+            [5111, 33311], ['customer_id' => $contract->customer_id, 'group' => $group]);
+        AccountDetail::createDataSaveDept($accounts, 5111, $total_price, AccountDetail::TYPE_HAS, [1311],
+            ['employee_id' => $contract->created_by, 'work_id' => self::WORK_DOANH_THU, 'group' => $group]);
+        AccountDetail::createDataSaveDept($accounts, 33311, $vat_cost, AccountDetail::TYPE_HAS, [1311],
+            ['group' => $group]);
+    }
+
+    /** 2. Giảm trừ doanh thu: Nợ 5213 + 33311 / Có 1311. */
+    private function revenueDeductionAccounting($sale_invoice, $sale_invoice_vat, Contract $contract, array &$accounts, int &$group): void
+    {
+        $group += 1;
+        AccountDetail::createDataSaveDept($accounts, 5213, $sale_invoice, AccountDetail::TYPE_DEPT, [1311],
+            ['employee_id' => $contract->created_by, 'work_id' => self::WORK_GIAM_TRU_DT, 'group' => $group]);
+        AccountDetail::createDataSaveDept($accounts, 33311, $sale_invoice_vat, AccountDetail::TYPE_DEPT, [1311],
+            ['group' => $group]);
+        AccountDetail::createDataSaveDept($accounts, 1311, $sale_invoice + $sale_invoice_vat, AccountDetail::TYPE_HAS,
+            [5213, 33311], ['customer_id' => $contract->customer_id, 'group' => $group]);
+    }
+
+    /** 4. Thưởng thực hiện HĐ: Nợ 5211 / Có 35241 — chia NV / trưởng BP / trưởng phòng. */
+    private function bonusContractAccounting($percent, $sa, Contract $contract, array &$accounts, int &$group): ?string
+    {
+        $amount = round($percent * (float) $sa->bonus_contract_before_vat);
+        $dm = $sa->department_main;
+        if (!$dm) {
+            return 'HĐ ' . $contract->code . ' chưa cấu hình phòng chính (HTHT)!';
+        }
+        $created_by = $contract->created_by;
+        $rootDeptId = (int) $dm->department_id;
+        $manager_parts = [];
+
+        foreach ($dm->employees as $emp) {
+            $partLead = $this->partLeadId($emp->part_id);
+            if ($partLead && !in_array($partLead, $manager_parts)) {
+                $manager_parts[] = $partLead;
+            }
+            $group += 1;
+            $bonus = round($amount * ((float) $emp->commission_sale_percent / 100) * ((float) $dm->diff_employee_percent / 100));
+            AccountDetail::createDataSaveDept($accounts, 5211, $bonus, AccountDetail::TYPE_DEPT, [35241],
+                ['employee_id' => $created_by, 'employee_department_id' => $contract->department_id, 'group' => $group, 'work_id' => self::WORK_THUONG_HH]);
+            AccountDetail::createDataSaveDept($accounts, 35241, $bonus, AccountDetail::TYPE_HAS, [5211],
+                ['employee_id' => $emp->employee_id, 'employee_department_id' => $rootDeptId, 'work_id' => self::WORK_THUONG_HH, 'group' => $group]);
+        }
+        foreach ($manager_parts as $partLead) {
+            $group += 1;
+            $bonus = round($amount * ((float) $dm->diff_part_lead_percent / 100));
+            AccountDetail::createDataSaveDept($accounts, 5211, $bonus, AccountDetail::TYPE_DEPT, [35241],
+                ['employee_id' => $created_by, 'employee_department_id' => $contract->department_id, 'group' => $group, 'work_id' => self::WORK_THUONG_HH]);
+            AccountDetail::createDataSaveDept($accounts, 35241, $bonus, AccountDetail::TYPE_HAS, [5211],
+                ['employee_id' => $partLead, 'employee_department_id' => $rootDeptId, 'work_id' => self::WORK_THUONG_HH, 'group' => $group]);
+        }
+
+        $deptLead = $this->deptLeadId($rootDeptId);
+        if (!$deptLead) {
+            return 'Chưa cấu hình trưởng phòng ' . $this->deptName($rootDeptId) . '!';
+        }
+        $group += 1;
+        $bonus = round($amount * ((float) $dm->diff_department_lead_percent / 100));
+        AccountDetail::createDataSaveDept($accounts, 5211, $bonus, AccountDetail::TYPE_DEPT, [35241],
+            ['employee_id' => $created_by, 'employee_department_id' => $contract->department_id, 'group' => $group, 'work_id' => self::WORK_THUONG_HH]);
+        AccountDetail::createDataSaveDept($accounts, 35241, $bonus, AccountDetail::TYPE_HAS, [5211],
+            ['employee_id' => $deptLead, 'employee_department_id' => $rootDeptId, 'work_id' => self::WORK_THUONG_HH, 'group' => $group]);
+
+        return null;
+    }
+
+    /** 5. TNCN tạm tính: Nợ 35241 / Có 3335 — chia NV / trưởng BP / trưởng phòng. */
+    private function vatExtraCostAccounting($percent, $sa, Contract $contract, array &$accounts, int &$group): ?string
+    {
+        $amount = round($percent * (float) $sa->tndn_vat);
+        $group += 1;
+        $dm = $sa->department_main;
+        if (!$dm) {
+            return 'HĐ ' . $contract->code . ' chưa cấu hình phòng chính (HTHT)!';
+        }
+        $deptId = (int) $dm->department_id;
+        $manager_parts = [];
+
+        foreach ($dm->employees as $emp) {
+            $partLead = $this->partLeadId($emp->part_id);
+            if ($partLead && !in_array($partLead, $manager_parts)) {
+                $manager_parts[] = $partLead;
+            }
+            $group += 1;
+            $vat = round($amount * ((float) $emp->commission_sale_percent / 100) * ((float) $dm->diff_employee_percent / 100));
+            AccountDetail::createDataSaveDept($accounts, 35241, $vat, AccountDetail::TYPE_DEPT, [3335],
+                ['employee_id' => $emp->employee_id, 'employee_department_id' => $deptId, 'work_id' => self::WORK_THUONG_HH, 'group' => $group]);
+            AccountDetail::createDataSaveDept($accounts, 3335, $vat, AccountDetail::TYPE_HAS, [35241],
+                ['employee_id' => $emp->employee_id, 'employee_department_id' => $deptId, 'work_id' => self::WORK_THUONG_HH, 'group' => $group]);
+        }
+        foreach ($manager_parts as $partLead) {
+            $group += 1;
+            $vat = round($amount * ((float) $dm->diff_part_lead_percent / 100));
+            AccountDetail::createDataSaveDept($accounts, 35241, $vat, AccountDetail::TYPE_DEPT, [3335],
+                ['employee_id' => $partLead, 'employee_department_id' => $deptId, 'work_id' => self::WORK_THUONG_HH, 'group' => $group]);
+            AccountDetail::createDataSaveDept($accounts, 3335, $vat, AccountDetail::TYPE_HAS, [35241],
+                ['employee_id' => $partLead, 'employee_department_id' => $deptId, 'work_id' => self::WORK_THUONG_HH, 'group' => $group]);
+        }
+
+        $deptLead = $this->deptLeadId($deptId);
+        if (!$deptLead) {
+            return 'Chưa cấu hình trưởng phòng ' . $this->deptName($deptId) . '!';
+        }
+        $group += 1;
+        $vat = round($amount * ((float) $dm->diff_department_lead_percent / 100));
+        AccountDetail::createDataSaveDept($accounts, 35241, $vat, AccountDetail::TYPE_DEPT, [3335],
+            ['employee_id' => $deptLead, 'employee_department_id' => $deptId, 'work_id' => self::WORK_THUONG_HH, 'group' => $group]);
+        AccountDetail::createDataSaveDept($accounts, 3335, $vat, AccountDetail::TYPE_HAS, [35241],
+            ['employee_id' => $deptLead, 'employee_department_id' => $deptId, 'work_id' => self::WORK_THUONG_HH, 'group' => $group]);
+
+        return null;
+    }
+
+    /** 6 + 7. Hoa hồng tháng + quý: Nợ 6411 / Có 35241 — mỗi phòng cùng công ty HĐ. */
+    private function monthlyAndQuarterlyCommissionAccounting($percent, $sa, $contractCompanyId, array &$accounts, int &$group): ?string
+    {
+        foreach ($sa->departments as $department) {
+            if ((int) $this->deptCompany((int) $department->department_id) !== (int) $contractCompanyId) {
+                continue;
+            }
+            $deptId = (int) $department->department_id;
+            $manager_parts = [];
+
+            foreach ($department->employees as $emp) {
+                $partLead = $this->partLeadId($emp->part_id);
+                if ($partLead && !in_array($partLead, $manager_parts)) {
+                    $manager_parts[] = $partLead;
+                }
+                // Hoa hồng tháng
+                $group += 1;
+                $monthEmp = round($percent * (float) $department->month_employee_amount * (float) $emp->commission_sale_percent / 100);
+                AccountDetail::createDataSaveDept($accounts, 6411, $monthEmp, AccountDetail::TYPE_DEPT, [35241], ['group' => $group]);
+                AccountDetail::createDataSaveDept($accounts, 35241, $monthEmp, AccountDetail::TYPE_HAS, [6411],
+                    ['employee_id' => $emp->employee_id, 'employee_department_id' => $deptId, 'work_id' => self::WORK_HH_THANG, 'group' => $group]);
+                // Hoa hồng quý
+                $group += 1;
+                $qtrEmp = round($percent * (float) $department->after_settlement_employee_amount * (float) $emp->commission_sale_percent / 100);
+                AccountDetail::createDataSaveDept($accounts, 6411, $qtrEmp, AccountDetail::TYPE_DEPT, [35241], ['group' => $group]);
+                AccountDetail::createDataSaveDept($accounts, 35241, $qtrEmp, AccountDetail::TYPE_HAS, [6411],
+                    ['employee_id' => $emp->employee_id, 'employee_department_id' => $deptId, 'work_id' => self::WORK_HH_QUY, 'group' => $group]);
+            }
+            foreach ($manager_parts as $partLead) {
+                $group += 1;
+                $monthPL = round($percent * (float) $department->month_part_lead_amount);
+                AccountDetail::createDataSaveDept($accounts, 6411, $monthPL, AccountDetail::TYPE_DEPT, [35241], ['group' => $group]);
+                AccountDetail::createDataSaveDept($accounts, 35241, $monthPL, AccountDetail::TYPE_HAS, [6411],
+                    ['employee_id' => $partLead, 'employee_department_id' => $deptId, 'work_id' => self::WORK_HH_THANG, 'group' => $group]);
+                $group += 1;
+                $qtrPL = round($percent * (float) $department->after_settlement_part_lead_amount);
+                AccountDetail::createDataSaveDept($accounts, 6411, $qtrPL, AccountDetail::TYPE_DEPT, [35241], ['group' => $group]);
+                AccountDetail::createDataSaveDept($accounts, 35241, $qtrPL, AccountDetail::TYPE_HAS, [6411],
+                    ['employee_id' => $partLead, 'employee_department_id' => $deptId, 'work_id' => self::WORK_HH_QUY, 'group' => $group]);
+            }
+
+            // Trưởng phòng (is_main → chính phòng; ngược lại → phòng objectable)
+            $rootDeptId = $department->is_main ? $deptId : $this->objectableDeptId($department);
+            $deptLead = $rootDeptId ? $this->deptLeadId($rootDeptId) : null;
+            if (!$deptLead) {
+                return 'Chưa cấu hình trưởng phòng ' . $this->deptName($rootDeptId) . '!';
+            }
+            $group += 1;
+            $monthDL = round($percent * (float) $department->month_department_lead_amount);
+            AccountDetail::createDataSaveDept($accounts, 6411, $monthDL, AccountDetail::TYPE_DEPT, [35241], ['group' => $group]);
+            AccountDetail::createDataSaveDept($accounts, 35241, $monthDL, AccountDetail::TYPE_HAS, [6411],
+                ['employee_id' => $deptLead, 'employee_department_id' => $rootDeptId, 'work_id' => self::WORK_HH_THANG, 'group' => $group]);
+            $group += 1;
+            $qtrDL = round($percent * (float) $department->after_settlement_department_lead_amount);
+            AccountDetail::createDataSaveDept($accounts, 6411, $qtrDL, AccountDetail::TYPE_DEPT, [35241], ['group' => $group]);
+            AccountDetail::createDataSaveDept($accounts, 35241, $qtrDL, AccountDetail::TYPE_HAS, [6411],
+                ['employee_id' => $deptLead, 'employee_department_id' => $rootDeptId, 'work_id' => self::WORK_HH_QUY, 'group' => $group]);
+        }
+
+        return null;
+    }
+
+    /** 8. Quỹ quản lý rủi ro phòng: Nợ 6411 / Có 35241 (đối tượng = phòng/bộ phận objectable). */
+    private function riskFundAccounting($percent, $sa, $contractCompanyId, array &$accounts, int &$group): void
+    {
+        foreach ($sa->departments as $department) {
+            if ((int) $this->deptCompany((int) $department->department_id) !== (int) $contractCompanyId) {
+                continue;
+            }
+            $risk = round($percent * (float) $department->risk_fund_amount);
+            $group += 1;
+            AccountDetail::createDataSaveDept($accounts, 6411, $risk, AccountDetail::TYPE_DEPT, [35241], ['group' => $group]);
+            $objKey = $this->objColumnFor($department->objectable_type);
+            AccountDetail::createDataSaveDept($accounts, 35241, $risk, AccountDetail::TYPE_HAS, [6411],
+                [$objKey => $department->objectable_id, 'work_id' => self::WORK_QUY_RUI_RO, 'group' => $group]);
+        }
+    }
+
+    // ----------------------------------------------------------------------------------
+    // Tra tổ chức qua DB::table (merged-DB-safe, thay morphTo cross-DB)
+    // ----------------------------------------------------------------------------------
+
+    private function dept(int $id)
+    {
+        if ($id <= 0) return null;
+        if (!array_key_exists($id, $this->deptCache)) {
+            $this->deptCache[$id] = DB::table('departments')
+                ->select('id', 'name', 'company_id', 'department_lead_id')
+                ->where('id', $id)->first();
+        }
+        return $this->deptCache[$id];
+    }
+
+    private function deptLeadId(int $id): ?int
+    {
+        $d = $this->dept($id);
+        return $d && $d->department_lead_id ? (int) $d->department_lead_id : null;
+    }
+
+    private function deptCompany(int $id): ?int
+    {
+        $d = $this->dept($id);
+        return $d ? (int) $d->company_id : null;
+    }
+
+    private function deptName(int $id): string
+    {
+        $d = $this->dept($id);
+        return $d ? $d->name : ('#' . $id);
+    }
+
+    private function partLeadId($partId): ?int
+    {
+        $partId = (int) $partId;
+        if ($partId <= 0) return null;
+        if (!array_key_exists($partId, $this->partCache)) {
+            $this->partCache[$partId] = DB::table('parts')
+                ->select('id', 'department_id', 'part_lead_id')
+                ->where('id', $partId)->first();
+        }
+        $p = $this->partCache[$partId];
+        return $p && $p->part_lead_id ? (int) $p->part_lead_id : null;
+    }
+
+    /** objectable → id phòng (Department: chính id; Part: phòng cha của bộ phận). */
+    private function objectableDeptId($department): ?int
+    {
+        $type = (string) $department->objectable_type;
+        $oid = (int) $department->objectable_id;
+        if ($oid <= 0) return null;
+        if (substr($type, -strlen('\\Part')) === '\\Part') {
+            if (!array_key_exists($oid, $this->partCache)) {
+                $this->partCache[$oid] = DB::table('parts')
+                    ->select('id', 'department_id', 'part_lead_id')->where('id', $oid)->first();
+            }
+            $p = $this->partCache[$oid];
+            return $p ? (int) $p->department_id : null;
+        }
+        return $oid; // Department
+    }
+
+    /** objectable_type (FQN ERP) → cột obj_* trong bút toán. */
+    private function objColumnFor($type): string
+    {
+        $type = (string) $type;
+        if (substr($type, -strlen('\\Part')) === '\\Part') {
+            return 'obj_part_id';
+        }
+        if (substr($type, -strlen('\\Company')) === '\\Company') {
+            return 'obj_company_id';
+        }
+        return 'obj_department_id';
+    }
+}
diff --git a/Modules/Assign/Services/ProductExportPostingService.php b/Modules/Assign/Services/ProductExportPostingService.php
index 70f70df58..b57626924 100644
--- a/Modules/Assign/Services/ProductExportPostingService.php
+++ b/Modules/Assign/Services/ProductExportPostingService.php
@@ -8,12 +8,13 @@ use Modules\Assign\Entities\Warehouse\ProductExport;
 use Modules\Assign\Entities\Warehouse\ProductExportRequest;
 use Modules\Assign\Entities\Warehouse\ContractProductImport;
 use Modules\Assign\Entities\Warehouse\WarehouseExport;
 use Modules\Assign\Entities\Warehouse\ProductImportExportArrangeDelivery;
 use Modules\Assign\Entities\Contract\Contract;
 use Modules\Finance\Entities\Account\AccountDetail;
+use Modules\Assign\Services\Accounting\SupportAccountingTrait;
 
 /**
  * Hạch toán (ghi sổ account_details) cho Phiếu xuất hàng HĐ HRM loại 20/21.
  *
  * PORT 1-1 "hạch toán bán hàng theo hãng" của ERP:
  *   - App\Services\Sale\Firm\Contract\FirmContractProductExportService::getDataProductExportAccounting
@@ -34,24 +35,22 @@ use Modules\Finance\Entities\Account\AccountDetail;
  *   - Tra tổ chức (phòng/bộ phận: lead, company) bằng DB::table (merged-DB-safe), KHÔNG morphTo cross-DB.
  *   - gross/gross_vat tính THẲNG từ chi tiết (product_exports.sum_amount_after_extra có thể chưa được
  *     điền ở luồng HRM) — bằng đúng định nghĩa Σ(price+extra)×qty của ERP.
  */
 class ProductExportPostingService
 {
+    use SupportAccountingTrait;
+
     /** Số hiệu công việc (Work) — bám sát ERP (accounting_works.id). */
     const WORK_DOANH_THU = 15;
     const WORK_GIAM_TRU_DT = 16;
     const WORK_THUONG_HH = 12;      // thưởng thực hiện HĐ + TNCN
     const WORK_HH_THANG = 13;
     const WORK_HH_QUY = 14;
     const WORK_QUY_RUI_RO = 6;
 
-    /** cache tra tổ chức trong 1 lần chạy */
-    private $deptCache = [];
-    private $partCache = [];
-
     /**
      * Sinh bút toán + ghi sổ cho 1 phiếu xuất hàng. Idempotent, chỉ chạy khi status=1.
      *
      * @return array [bool ok, string err]
      */
     public function postAccounting(ProductExport $pxh): array
@@ -343,40 +342,12 @@ class ProductExportPostingService
         $summation = (float) $sa->before_vat_product + (float) $sa->before_vat_repair_service;
         $pct_wo_cost = $summation > 0 ? ($amount / $summation) : 0;
 
         return [true, $sale_invoice, $sale_invoice_vat, $gross, $gross_vat, $sa, $pct_wo_delivery, $pct_wo_cost];
     }
 
-    // ----------------------------------------------------------------------------------
-    // 8 CỤM BÚT TOÁN — port FirmContractExportService (dịch ::class → key cột thô HRM)
-    // ----------------------------------------------------------------------------------
-
-    /** 1. Doanh thu: Nợ 1311 / Có 5111 + 33311 (giá trị gộp, trước giảm trừ). */
-    private function revenueAccounting($total_price, $vat_cost, Contract $contract, array &$accounts, int &$group): void
-    {
-        $group += 1;
-        AccountDetail::createDataSaveDept($accounts, 1311, $total_price + $vat_cost, AccountDetail::TYPE_DEPT,
-            [5111, 33311], ['customer_id' => $contract->customer_id, 'group' => $group]);
-        AccountDetail::createDataSaveDept($accounts, 5111, $total_price, AccountDetail::TYPE_HAS, [1311],
-            ['employee_id' => $contract->created_by, 'work_id' => self::WORK_DOANH_THU, 'group' => $group]);
-        AccountDetail::createDataSaveDept($accounts, 33311, $vat_cost, AccountDetail::TYPE_HAS, [1311],
-            ['group' => $group]);
-    }
-
-    /** 2. Giảm trừ doanh thu: Nợ 5213 + 33311 / Có 1311. */
-    private function revenueDeductionAccounting($sale_invoice, $sale_invoice_vat, Contract $contract, array &$accounts, int &$group): void
-    {
-        $group += 1;
-        AccountDetail::createDataSaveDept($accounts, 5213, $sale_invoice, AccountDetail::TYPE_DEPT, [1311],
-            ['employee_id' => $contract->created_by, 'work_id' => self::WORK_GIAM_TRU_DT, 'group' => $group]);
-        AccountDetail::createDataSaveDept($accounts, 33311, $sale_invoice_vat, AccountDetail::TYPE_DEPT, [1311],
-            ['group' => $group]);
-        AccountDetail::createDataSaveDept($accounts, 1311, $sale_invoice + $sale_invoice_vat, AccountDetail::TYPE_HAS,
-            [5213, 33311], ['customer_id' => $contract->customer_id, 'group' => $group]);
-    }
-
     /**
      * 3. Giá vốn (loại 21): mỗi SP dư Có $creditAcc (155) ref 632; tổng dư Nợ 632 ref $creditAcc.
      * export_price đã do WarehouseExportAccountingService::calculateExportPrice tính = (Σvb−Σva)/(qty×coef)
      * → total = export_price × qty × coef = Σvb−Σva (khớp tới đồng).
      */
     private function costAccounting(ProductExport $pxh, array &$accounts, int &$group, int $creditAcc): void
@@ -407,254 +378,7 @@ class ProductExportPostingService
                 ['product_id' => $p->product_id, 'group' => $group]);
         }
         AccountDetail::createDataSaveDept($accounts, 1541, $sum, AccountDetail::TYPE_DEPT, [1561],
             ['group' => $group]);
     }
 
-    /** 4. Thưởng thực hiện HĐ: Nợ 5211 / Có 35241 — chia NV / trưởng BP / trưởng phòng. */
-    private function bonusContractAccounting($percent, $sa, Contract $contract, array &$accounts, int &$group): ?string
-    {
-        $amount = round($percent * (float) $sa->bonus_contract_before_vat);
-        $dm = $sa->department_main;
-        if (!$dm) {
-            return 'HĐ ' . $contract->code . ' chưa cấu hình phòng chính (HTHT)!';
-        }
-        $created_by = $contract->created_by;
-        $rootDeptId = (int) $dm->department_id;
-        $manager_parts = [];
-
-        foreach ($dm->employees as $emp) {
-            $partLead = $this->partLeadId($emp->part_id);
-            if ($partLead && !in_array($partLead, $manager_parts)) {
-                $manager_parts[] = $partLead;
-            }
-            $group += 1;
-            $bonus = round($amount * ((float) $emp->commission_sale_percent / 100) * ((float) $dm->diff_employee_percent / 100));
-            AccountDetail::createDataSaveDept($accounts, 5211, $bonus, AccountDetail::TYPE_DEPT, [35241],
-                ['employee_id' => $created_by, 'employee_department_id' => $contract->department_id, 'group' => $group, 'work_id' => self::WORK_THUONG_HH]);
-            AccountDetail::createDataSaveDept($accounts, 35241, $bonus, AccountDetail::TYPE_HAS, [5211],
-                ['employee_id' => $emp->employee_id, 'employee_department_id' => $rootDeptId, 'work_id' => self::WORK_THUONG_HH, 'group' => $group]);
-        }
-        foreach ($manager_parts as $partLead) {
-            $group += 1;
-            $bonus = round($amount * ((float) $dm->diff_part_lead_percent / 100));
-            AccountDetail::createDataSaveDept($accounts, 5211, $bonus, AccountDetail::TYPE_DEPT, [35241],
-                ['employee_id' => $created_by, 'employee_department_id' => $contract->department_id, 'group' => $group, 'work_id' => self::WORK_THUONG_HH]);
-            AccountDetail::createDataSaveDept($accounts, 35241, $bonus, AccountDetail::TYPE_HAS, [5211],
-                ['employee_id' => $partLead, 'employee_department_id' => $rootDeptId, 'work_id' => self::WORK_THUONG_HH, 'group' => $group]);
-        }
-
-        $deptLead = $this->deptLeadId($rootDeptId);
-        if (!$deptLead) {
-            return 'Chưa cấu hình trưởng phòng ' . $this->deptName($rootDeptId) . '!';
-        }
-        $group += 1;
-        $bonus = round($amount * ((float) $dm->diff_department_lead_percent / 100));
-        AccountDetail::createDataSaveDept($accounts, 5211, $bonus, AccountDetail::TYPE_DEPT, [35241],
-            ['employee_id' => $created_by, 'employee_department_id' => $contract->department_id, 'group' => $group, 'work_id' => self::WORK_THUONG_HH]);
-        AccountDetail::createDataSaveDept($accounts, 35241, $bonus, AccountDetail::TYPE_HAS, [5211],
-            ['employee_id' => $deptLead, 'employee_department_id' => $rootDeptId, 'work_id' => self::WORK_THUONG_HH, 'group' => $group]);
-
-        return null;
-    }
-
-    /** 5. TNCN tạm tính: Nợ 35241 / Có 3335 — chia NV / trưởng BP / trưởng phòng. */
-    private function vatExtraCostAccounting($percent, $sa, Contract $contract, array &$accounts, int &$group): ?string
-    {
-        $amount = round($percent * (float) $sa->tndn_vat);
-        $group += 1;
-        $dm = $sa->department_main;
-        if (!$dm) {
-            return 'HĐ ' . $contract->code . ' chưa cấu hình phòng chính (HTHT)!';
-        }
-        $deptId = (int) $dm->department_id;
-        $manager_parts = [];
-
-        foreach ($dm->employees as $emp) {
-            $partLead = $this->partLeadId($emp->part_id);
-            if ($partLead && !in_array($partLead, $manager_parts)) {
-                $manager_parts[] = $partLead;
-            }
-            $group += 1;
-            $vat = round($amount * ((float) $emp->commission_sale_percent / 100) * ((float) $dm->diff_employee_percent / 100));
-            AccountDetail::createDataSaveDept($accounts, 35241, $vat, AccountDetail::TYPE_DEPT, [3335],
-                ['employee_id' => $emp->employee_id, 'employee_department_id' => $deptId, 'work_id' => self::WORK_THUONG_HH, 'group' => $group]);
-            AccountDetail::createDataSaveDept($accounts, 3335, $vat, AccountDetail::TYPE_HAS, [35241],
-                ['employee_id' => $emp->employee_id, 'employee_department_id' => $deptId, 'work_id' => self::WORK_THUONG_HH, 'group' => $group]);
-        }
-        foreach ($manager_parts as $partLead) {
-            $group += 1;
-            $vat = round($amount * ((float) $dm->diff_part_lead_percent / 100));
-            AccountDetail::createDataSaveDept($accounts, 35241, $vat, AccountDetail::TYPE_DEPT, [3335],
-                ['employee_id' => $partLead, 'employee_department_id' => $deptId, 'work_id' => self::WORK_THUONG_HH, 'group' => $group]);
-            AccountDetail::createDataSaveDept($accounts, 3335, $vat, AccountDetail::TYPE_HAS, [35241],
-                ['employee_id' => $partLead, 'employee_department_id' => $deptId, 'work_id' => self::WORK_THUONG_HH, 'group' => $group]);
-        }
-
-        $deptLead = $this->deptLeadId($deptId);
-        if (!$deptLead) {
-            return 'Chưa cấu hình trưởng phòng ' . $this->deptName($deptId) . '!';
-        }
-        $group += 1;
-        $vat = round($amount * ((float) $dm->diff_department_lead_percent / 100));
-        AccountDetail::createDataSaveDept($accounts, 35241, $vat, AccountDetail::TYPE_DEPT, [3335],
-            ['employee_id' => $deptLead, 'employee_department_id' => $deptId, 'work_id' => self::WORK_THUONG_HH, 'group' => $group]);
-        AccountDetail::createDataSaveDept($accounts, 3335, $vat, AccountDetail::TYPE_HAS, [35241],
-            ['employee_id' => $deptLead, 'employee_department_id' => $deptId, 'work_id' => self::WORK_THUONG_HH, 'group' => $group]);
-
-        return null;
-    }
-
-    /** 6 + 7. Hoa hồng tháng + quý: Nợ 6411 / Có 35241 — mỗi phòng cùng công ty HĐ. */
-    private function monthlyAndQuarterlyCommissionAccounting($percent, $sa, $contractCompanyId, array &$accounts, int &$group): ?string
-    {
-        foreach ($sa->departments as $department) {
-            if ((int) $this->deptCompany((int) $department->department_id) !== (int) $contractCompanyId) {
-                continue;
-            }
-            $deptId = (int) $department->department_id;
-            $manager_parts = [];
-
-            foreach ($department->employees as $emp) {
-                $partLead = $this->partLeadId($emp->part_id);
-                if ($partLead && !in_array($partLead, $manager_parts)) {
-                    $manager_parts[] = $partLead;
-                }
-                // Hoa hồng tháng
-                $group += 1;
-                $monthEmp = round($percent * (float) $department->month_employee_amount * (float) $emp->commission_sale_percent / 100);
-                AccountDetail::createDataSaveDept($accounts, 6411, $monthEmp, AccountDetail::TYPE_DEPT, [35241], ['group' => $group]);
-                AccountDetail::createDataSaveDept($accounts, 35241, $monthEmp, AccountDetail::TYPE_HAS, [6411],
-                    ['employee_id' => $emp->employee_id, 'employee_department_id' => $deptId, 'work_id' => self::WORK_HH_THANG, 'group' => $group]);
-                // Hoa hồng quý
-                $group += 1;
-                $qtrEmp = round($percent * (float) $department->after_settlement_employee_amount * (float) $emp->commission_sale_percent / 100);
-                AccountDetail::createDataSaveDept($accounts, 6411, $qtrEmp, AccountDetail::TYPE_DEPT, [35241], ['group' => $group]);
-                AccountDetail::createDataSaveDept($accounts, 35241, $qtrEmp, AccountDetail::TYPE_HAS, [6411],
-                    ['employee_id' => $emp->employee_id, 'employee_department_id' => $deptId, 'work_id' => self::WORK_HH_QUY, 'group' => $group]);
-            }
-            foreach ($manager_parts as $partLead) {
-                $group += 1;
-                $monthPL = round($percent * (float) $department->month_part_lead_amount);
-                AccountDetail::createDataSaveDept($accounts, 6411, $monthPL, AccountDetail::TYPE_DEPT, [35241], ['group' => $group]);
-                AccountDetail::createDataSaveDept($accounts, 35241, $monthPL, AccountDetail::TYPE_HAS, [6411],
-                    ['employee_id' => $partLead, 'employee_department_id' => $deptId, 'work_id' => self::WORK_HH_THANG, 'group' => $group]);
-                $group += 1;
-                $qtrPL = round($percent * (float) $department->after_settlement_part_lead_amount);
-                AccountDetail::createDataSaveDept($accounts, 6411, $qtrPL, AccountDetail::TYPE_DEPT, [35241], ['group' => $group]);
-                AccountDetail::createDataSaveDept($accounts, 35241, $qtrPL, AccountDetail::TYPE_HAS, [6411],
-                    ['employee_id' => $partLead, 'employee_department_id' => $deptId, 'work_id' => self::WORK_HH_QUY, 'group' => $group]);
-            }
-
-            // Trưởng phòng (is_main → chính phòng; ngược lại → phòng objectable)
-            $rootDeptId = $department->is_main ? $deptId : $this->objectableDeptId($department);
-            $deptLead = $rootDeptId ? $this->deptLeadId($rootDeptId) : null;
-            if (!$deptLead) {
-                return 'Chưa cấu hình trưởng phòng ' . $this->deptName($rootDeptId) . '!';
-            }
-            $group += 1;
-            $monthDL = round($percent * (float) $department->month_department_lead_amount);
-            AccountDetail::createDataSaveDept($accounts, 6411, $monthDL, AccountDetail::TYPE_DEPT, [35241], ['group' => $group]);
-            AccountDetail::createDataSaveDept($accounts, 35241, $monthDL, AccountDetail::TYPE_HAS, [6411],
-                ['employee_id' => $deptLead, 'employee_department_id' => $rootDeptId, 'work_id' => self::WORK_HH_THANG, 'group' => $group]);
-            $group += 1;
-            $qtrDL = round($percent * (float) $department->after_settlement_department_lead_amount);
-            AccountDetail::createDataSaveDept($accounts, 6411, $qtrDL, AccountDetail::TYPE_DEPT, [35241], ['group' => $group]);
-            AccountDetail::createDataSaveDept($accounts, 35241, $qtrDL, AccountDetail::TYPE_HAS, [6411],
-                ['employee_id' => $deptLead, 'employee_department_id' => $rootDeptId, 'work_id' => self::WORK_HH_QUY, 'group' => $group]);
-        }
-
-        return null;
-    }
-
-    /** 8. Quỹ quản lý rủi ro phòng: Nợ 6411 / Có 35241 (đối tượng = phòng/bộ phận objectable). */
-    private function riskFundAccounting($percent, $sa, $contractCompanyId, array &$accounts, int &$group): void
-    {
-        foreach ($sa->departments as $department) {
-            if ((int) $this->deptCompany((int) $department->department_id) !== (int) $contractCompanyId) {
-                continue;
-            }
-            $risk = round($percent * (float) $department->risk_fund_amount);
-            $group += 1;
-            AccountDetail::createDataSaveDept($accounts, 6411, $risk, AccountDetail::TYPE_DEPT, [35241], ['group' => $group]);
-            $objKey = $this->objColumnFor($department->objectable_type);
-            AccountDetail::createDataSaveDept($accounts, 35241, $risk, AccountDetail::TYPE_HAS, [6411],
-                [$objKey => $department->objectable_id, 'work_id' => self::WORK_QUY_RUI_RO, 'group' => $group]);
-        }
-    }
-
-    // ----------------------------------------------------------------------------------
-    // Tra tổ chức qua DB::table (merged-DB-safe, thay morphTo cross-DB)
-    // ----------------------------------------------------------------------------------
-
-    private function dept(int $id)
-    {
-        if ($id <= 0) return null;
-        if (!array_key_exists($id, $this->deptCache)) {
-            $this->deptCache[$id] = DB::table('departments')
-                ->select('id', 'name', 'company_id', 'department_lead_id')
-                ->where('id', $id)->first();
-        }
-        return $this->deptCache[$id];
-    }
-
-    private function deptLeadId(int $id): ?int
-    {
-        $d = $this->dept($id);
-        return $d && $d->department_lead_id ? (int) $d->department_lead_id : null;
-    }
-
-    private function deptCompany(int $id): ?int
-    {
-        $d = $this->dept($id);
-        return $d ? (int) $d->company_id : null;
-    }
-
-    private function deptName(int $id): string
-    {
-        $d = $this->dept($id);
-        return $d ? $d->name : ('#' . $id);
-    }
-
-    private function partLeadId($partId): ?int
-    {
-        $partId = (int) $partId;
-        if ($partId <= 0) return null;
-        if (!array_key_exists($partId, $this->partCache)) {
-            $this->partCache[$partId] = DB::table('parts')
-                ->select('id', 'department_id', 'part_lead_id')
-                ->where('id', $partId)->first();
-        }
-        $p = $this->partCache[$partId];
-        return $p && $p->part_lead_id ? (int) $p->part_lead_id : null;
-    }
-
-    /** objectable → id phòng (Department: chính id; Part: phòng cha của bộ phận). */
-    private function objectableDeptId($department): ?int
-    {
-        $type = (string) $department->objectable_type;
-        $oid = (int) $department->objectable_id;
-        if ($oid <= 0) return null;
-        if (substr($type, -strlen('\\Part')) === '\\Part') {
-            if (!array_key_exists($oid, $this->partCache)) {
-                $this->partCache[$oid] = DB::table('parts')
-                    ->select('id', 'department_id', 'part_lead_id')->where('id', $oid)->first();
-            }
-            $p = $this->partCache[$oid];
-            return $p ? (int) $p->department_id : null;
-        }
-        return $oid; // Department
-    }
-
-    /** objectable_type (FQN ERP) → cột obj_* trong bút toán. */
-    private function objColumnFor($type): string
-    {
-        $type = (string) $type;
-        if (substr($type, -strlen('\\Part')) === '\\Part') {
-            return 'obj_part_id';
-        }
-        if (substr($type, -strlen('\\Company')) === '\\Company') {
-            return 'obj_company_id';
-        }
-        return 'obj_department_id';
-    }
 }
diff --git a/Modules/Assign/Tests/Feature/ProductExportPostingRegressionTest.php b/Modules/Assign/Tests/Feature/ProductExportPostingRegressionTest.php
new file mode 100644
index 000000000..e06b8d6e3
--- /dev/null
+++ b/Modules/Assign/Tests/Feature/ProductExportPostingRegressionTest.php
@@ -0,0 +1,57 @@
+<?php
+
+namespace Modules\Assign\Tests\Feature;
+
+use Tests\TestCase;
+use Illuminate\Foundation\Testing\DatabaseTransactions;
+use Modules\Assign\Services\ProductExportPostingService;
+use Modules\Assign\Entities\Warehouse\ProductExport;
+use Modules\Assign\Entities\Warehouse\ProductExportRequest;
+
+class ProductExportPostingRegressionTest extends TestCase
+{
+    use DatabaseTransactions;
+
+    public function test_post_accounting_snapshot_stable()
+    {
+        // Fallback (theo brief): PXH mới nhất (id=34590) là type=3, không hỗ trợ hạch toán
+        // (getDataProductExportAccounting trả ok=false, không throw). Chọn PXH loại 20/21
+        // gắn HĐ hợp lệ (ok=true, có accounts) để snapshot cho khớp trước/sau refactor.
+        // Ưu tiên type=21 (XUAT_BAN_HOP_DONG, đủ 8 cụm — bao phủ 13 method di chuyển sang trait),
+        // fallback type=20 (chỉ costAccountingProduction, method KHÔNG di chuyển) nếu không có.
+        $svc = app(ProductExportPostingService::class);
+        $candidates = ProductExport::whereIn('type', [
+            ProductExportRequest::XUAT_BAN_HOP_DONG,
+            ProductExportRequest::XUAT_SAN_XUAT_HOP_DONG,
+        ])->orderByDesc('id')->get()
+            ->sortBy(function ($c) {
+                return (int) $c->type === ProductExportRequest::XUAT_BAN_HOP_DONG ? 0 : 1;
+            });
+
+        $pxh = null;
+        $data = null;
+        foreach ($candidates as $c) {
+            $res = $svc->getDataProductExportAccounting($c);
+            if ($res[0] && !empty($res[1])) {
+                $pxh = $c;
+                $data = $res[1]; // mảng $accounts thực tế (KHÔNG ghi DB)
+                break;
+            }
+        }
+
+        if (!$pxh) {
+            $this->markTestSkipped('Không có ProductExport loại 20/21 gắn HĐ hợp lệ để snapshot.');
+        }
+
+        $sumDept = collect($data)->where('type', 1)->sum('value');
+        $sumHas  = collect($data)->where('type', 2)->sum('value');
+        $this->assertEqualsWithDelta($sumDept, $sumHas, 1.0, 'Nợ phải cân Có');
+        $this->assertNotEmpty($data);
+
+        // Ghi snapshot ra output để so khớp trước/sau refactor (baseline).
+        fwrite(STDERR, sprintf(
+            "\n[SNAPSHOT] pxh_id=%d type=%d rows=%d sumDept=%s sumHas=%s\n",
+            $pxh->id, $pxh->type, count($data), $sumDept, $sumHas
+        ));
+    }
+}
```
