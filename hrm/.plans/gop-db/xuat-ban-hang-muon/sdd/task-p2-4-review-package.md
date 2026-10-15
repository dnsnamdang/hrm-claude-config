# Task P2-4 review package — BorrowSellPostingService nhánh Firm

BASE=2d4bbfe (sau T3) → HEAD=34fd294 (impl fe9c48f + fix giá vốn 34fd294)

## Commits
34fd29452 fix(finance): giá vốn nhánh Firm bỏ nhân unit_coefficient (port đúng ERP)
fe9c48f25 feat(finance): BorrowSellPostingService nhánh FirmContract (giá vốn TK157 + doanh thu + cụm hỗ trợ)

## Diff stat
 .../BorrowSell/BorrowSellPostingService.php        | 235 +++++++++++++++++++++
 .../Tests/Feature/BorrowSellPostingFirmTest.php    | 101 +++++++++
 2 files changed, 336 insertions(+)

## Full diff (-U15)
```diff
diff --git a/Modules/Finance/Services/BorrowSell/BorrowSellPostingService.php b/Modules/Finance/Services/BorrowSell/BorrowSellPostingService.php
new file mode 100644
index 000000000..a4d3344f6
--- /dev/null
+++ b/Modules/Finance/Services/BorrowSell/BorrowSellPostingService.php
@@ -0,0 +1,235 @@
+<?php
+
+namespace Modules\Finance\Services\BorrowSell;
+
+use Carbon\Carbon;
+use Illuminate\Support\Facades\DB;
+use Modules\Assign\Entities\Contract\Contract;
+use Modules\Assign\Entities\Contract\SupportAccounting;
+use Modules\Assign\Services\Accounting\SupportAccountingTrait;
+use Modules\Finance\Entities\Account\AccountDetail;
+use Modules\Finance\Entities\BorrowSell\BorrowSell;
+use Modules\Finance\Entities\Contract\FirmContract;
+
+/**
+ * Hạch toán (ghi sổ account_details) cho Phiếu XUẤT BÁN HÀNG MƯỢN (`borrow_sells`) — Phase 2.
+ *
+ * PORT 1-1 ERP `App\Services\Sale\Firm\Contract\FirmContractBorrowSellService`
+ * (`getDataBorrowSellAccounting` + `prepareData` + `costAccounting`), nhái cấu trúc
+ * `Modules\Assign\Services\ProductExportPostingService::getDataProductExportAccounting`.
+ *
+ * TASK P2-4: CHỈ nhánh FirmContract (`contractable_type = BorrowSell::CONTRACT_FIRM`).
+ * Nhánh WrService để Task 5 (`getDataAccounting` trả lỗi tạm thời cho nhánh này).
+ *
+ * KHÁC xuất hàng thường: giá vốn dư CÓ TK **157** (hàng gửi bán) thay vì 155/156/1561 —
+ * đúng nghiệp vụ "hàng mượn của hãng đang gửi tại kho mình, giờ xuất bán".
+ *
+ * GOTCHA resolveContract (đã điều tra, xem report task-p2-4-report.md):
+ *   `borrow_sells.contractable_id` trỏ THẲNG `firm_contracts.id` (ERP HĐ hãng thật, ~24.9k dòng),
+ *   KHÔNG PHẢI `hrm_contracts.id` (Contract entity Assign module, chỉ có 2 dòng — miền dữ liệu
+ *   hoàn toàn khác, HĐ "Giao việc" theo báo giá). NHƯNG 6 method cụm của SupportAccountingTrait
+ *   type-hint cứng `Contract $contract` (namespace Assign). Giải pháp: dựng 1 `Contract` SHIM
+ *   trong bộ nhớ (KHÔNG lưu DB) từ đúng các cột `firm_contracts` cần (`customer_id`, `created_by`,
+ *   `code`, `company_id`, `department_id`, `part_id` — tên cột trùng khớp `hrm_contracts`), rồi gắn
+ *   thẳng quan hệ `support_accounting` bằng dòng `firm_support_accounting` tra theo
+ *   (`contractable_id` = firm_contracts.id, `contractable_type` = BorrowSell::CONTRACT_FIRM) — bảng
+ *   này vốn đã polymorphic dùng chung giữa FirmContract (ERP, ~21k dòng) và Contract (Assign, 2 dòng).
+ *   Verify bằng SQL thật (report ghi chi tiết) — không phải đoán.
+ */
+class BorrowSellPostingService
+{
+    use SupportAccountingTrait;
+
+    /**
+     * ⚠️ GOTCHA: trait SupportAccountingTrait gọi `self::WORK_*` nhưng các const này KHÔNG
+     * nằm trong trait (chúng thuộc ProductExportPostingService). Vì self:: phân giải theo class
+     * ĐANG DÙNG trait, BorrowSellPostingService PHẢI tự khai đủ 6 const này, nếu không PHP fatal.
+     */
+    const WORK_DOANH_THU = 15;    // DTHH
+    const WORK_GIAM_TRU_DT = 16;  // GGHH
+    const WORK_THUONG_HH = 12;    // TTHHD (thưởng HĐ + TNCN)
+    const WORK_HH_THANG = 13;     // TNST
+    const WORK_HH_QUY = 14;       // TNSQ
+    const WORK_QUY_RUI_RO = 6;    // RRP
+
+    /** FQN model ERP để lưu cột polymorphic invoiceable_type (ERP đọc lại được). */
+    const INVOICEABLE_BORROW_SELL = 'App\\Model\\Warehouse\\BorrowSell';
+
+    /**
+     * Sinh bút toán + ghi sổ cho 1 phiếu xuất bán hàng mượn.
+     * @return array [bool ok, string err]
+     */
+    public function postAccounting(BorrowSell $bs): array
+    {
+        [$ok, $accounts, $err] = $this->getDataAccounting($bs);
+        if (!$ok) {
+            return [false, $err];
+        }
+        if (empty($accounts)) {
+            return [true, ''];
+        }
+
+        $contract = $bs->contractable_type === BorrowSell::CONTRACT_FIRM
+            ? $this->resolveContract($bs)
+            : null;
+
+        $meta = [
+            'invoiceable_date_accounting' => $bs->created_at ? Carbon::parse($bs->created_at)->format('Y-m-d') : null,
+            'contractable_id' => $bs->contractable_id,
+            'contractable_type' => $bs->contractable_type,
+            'contractable_code' => $contract->code ?? null,
+            'contract_created_by' => $contract->created_by ?? null,
+            'contract_customer_id' => $contract->customer_id ?? null,
+            'company_id' => $contract->company_id ?? null,
+            'department_id' => $contract->department_id ?? null,
+            'part_id' => $contract->part_id ?? null,
+            'created_by' => $bs->created_by,
+        ];
+
+        try {
+            return DB::transaction(function () use ($accounts, $bs, $meta) {
+                return AccountDetail::saveAccountDetail(
+                    $accounts,
+                    $bs->id,
+                    self::INVOICEABLE_BORROW_SELL,
+                    $bs->code,
+                    $meta
+                );
+            });
+        } catch (\Throwable $e) {
+            return [false, 'Lỗi hạch toán phiếu xuất bán hàng mượn ' . $bs->code . ': ' . $e->getMessage()];
+        }
+    }
+
+    /**
+     * Orchestrator — bám sát ERP getDataBorrowSellAccounting. KHÔNG ghi DB.
+     * @return array [bool ok, array accounts, string err]
+     */
+    public function getDataAccounting(BorrowSell $bs): array
+    {
+        $accounts = [];
+        $group = 1;
+
+        if ($bs->contractable_type === BorrowSell::CONTRACT_FIRM) {
+            $contract = $this->resolveContract($bs);
+            if (!$contract) {
+                return [false, [], 'Phiếu ' . $bs->code . ' không tra được hợp đồng hãng (contractable_id='
+                    . $bs->contractable_id . ')!'];
+            }
+            try {
+                $this->firmBranch($bs, $contract, $accounts, $group);
+            } catch (\RuntimeException $e) {
+                return [false, [], $e->getMessage()];
+            }
+            return [true, $accounts, ''];
+        }
+
+        // Task 5 sẽ bổ sung nhánh WrService — KHÔNG tự làm ở task này.
+        return [false, [], 'Nhánh WrService chưa hỗ trợ (Task 5)'];
+    }
+
+    /**
+     * Nạp HĐ hãng thật (`firm_contracts`) từ `borrow_sells.contractable_id`, dựng SHIM
+     * `Modules\Assign\Entities\Contract\Contract` (KHÔNG lưu DB) để dùng chung 6 method cụm
+     * của trait (type-hint cứng Contract). Gắn thẳng quan hệ support_accounting bằng dòng
+     * firm_support_accounting polymorphic đúng (contractable_id/contractable_type = FirmContract).
+     */
+    private function resolveContract(BorrowSell $bs): ?Contract
+    {
+        $firm = FirmContract::find($bs->contractable_id);
+        if (!$firm) {
+            return null;
+        }
+
+        $contract = new Contract($firm->getAttributes());
+
+        $sa = SupportAccounting::where('contractable_id', $firm->id)
+            ->where('contractable_type', BorrowSell::CONTRACT_FIRM)
+            ->first();
+        $contract->setRelation('support_accounting', $sa);
+
+        return $contract;
+    }
+
+    /**
+     * Nhánh HĐ hãng — 8 cụm bút toán (port ERP FirmContractBorrowSellService::getDataBorrowSellAccounting
+     * + prepareData). Ném RuntimeException khi thiếu cấu hình (HTHT/trưởng phòng) — getDataAccounting bắt lại.
+     */
+    private function firmBranch(BorrowSell $bs, Contract $contract, array &$accounts, int &$group): void
+    {
+        $sa = $contract->support_accounting;
+        if (!$sa) {
+            throw new \RuntimeException('HĐ ' . $contract->code . ' chưa có bảng Hỗ trợ hạch toán (HTHT)!');
+        }
+
+        // prepareData — port ERP FirmContractBorrowSellService::prepareData.
+        $sale_invoice = 0;
+        $sale_invoice_vat = 0;
+        foreach ($bs->products as $p) {
+            $discount_price = ((float) $p->price + (float) $p->extra_price) - (float) $p->allocated_price - (float) $p->rebate_price;
+            $qty = (float) $p->qty;
+            $sale_invoice += $discount_price * $qty;
+            $sale_invoice_vat += ($discount_price * $qty) * (float) $p->vat_percent / 100;
+        }
+
+        // gross/gross_vat: HRM dùng thẳng cột header sum_amount_after_extra(_vat) — đúng ERP
+        // borrow_sell->sum_amount_after_extra(_vat), KHÔNG cần cộng dồn lại từ chi tiết.
+        $gross = (float) ($bs->sum_amount_after_extra ?? 0);
+        $gross_vat = (float) ($bs->sum_amount_after_extra_vat ?? 0);
+
+        $amount = $gross - $sale_invoice;
+        $before_vat_not_include_delivery = (float) $sa->before_vat_total - (float) $sa->before_vat_delivery_cost;
+        $pct_wo_delivery = intval($before_vat_not_include_delivery) ? $amount / $before_vat_not_include_delivery : 0;
+        $before_vat = (float) $sa->before_vat_product + (float) $sa->before_vat_repair_service;
+        $pct_wo_cost = intval($before_vat) ? $amount / $before_vat : 0;
+
+        // 1. Doanh thu
+        $this->revenueAccounting($gross, $gross_vat, $contract, $accounts, $group);
+        // 2. Giảm trừ doanh thu
+        $this->revenueDeductionAccounting($sale_invoice, $sale_invoice_vat, $contract, $accounts, $group);
+        // 3. Giá vốn: Nợ 632 / Có 157
+        $this->costAccounting($bs, $accounts, $group);
+        // 4. Thưởng thực hiện hợp đồng
+        $e1 = $this->bonusContractAccounting($pct_wo_delivery, $sa, $contract, $accounts, $group);
+        if ($e1) {
+            throw new \RuntimeException($e1);
+        }
+        // 5. Thuế TNCN tạm tính
+        $e2 = $this->vatExtraCostAccounting($pct_wo_delivery, $sa, $contract, $accounts, $group);
+        if ($e2) {
+            throw new \RuntimeException($e2);
+        }
+        // 6 + 7. Hoa hồng tháng + quý
+        $e3 = $this->monthlyAndQuarterlyCommissionAccounting($pct_wo_cost, $sa, $contract->company_id, $accounts, $group);
+        if ($e3) {
+            throw new \RuntimeException($e3);
+        }
+        // 8. Quỹ quản lý rủi ro phòng
+        $this->riskFundAccounting($pct_wo_cost, $sa, $contract->company_id, $accounts, $group);
+    }
+
+    /**
+     * 3. Giá vốn: mỗi SP dư Có 157 (hàng gửi bán) ref 632; tổng dư Nợ 632 ref 157.
+     * $cost = Σ export_price × qty — port ĐÚNG ERP FirmContractBorrowSellService::costAccounting
+     * (dòng 203: `$product->export_price * $product->qty`, KHÔNG nhân unit_coefficient). Ở nhánh Firm,
+     * export_price của borrow_sell_products lưu theo ĐƠN VỊ BÁN (cùng đơn vị `qty`) — verify bằng data:
+     * SP `Chì dán` unit_coefficient=100, export_price≈330.187/Hộp, giá bán≈664.300/Hộp (price/ep≈2 = biên
+     * lãi thường); nếu nhân coefficient → 33.018.700/Hộp = sai gấp 100 lần. Brief P2-4 ghi nhân coefficient
+     * là LỖI của brief (test cũ pass do fixture coef=1). LƯU Ý: nhánh WrService (Task 5) NGƯỢC LẠI có nhân
+     * unit_coefficient — ERP BorrowSell::getDataCreateDept dòng 600 `export_price*qty*unit_coefficient`.
+     */
+    private function costAccounting(BorrowSell $bs, array &$accounts, int &$group): void
+    {
+        $sum = 0;
+        $group += 1;
+        foreach ($bs->products as $p) {
+            $qty = (float) $p->qty;
+            $total = round((float) $p->export_price * $qty);
+            $sum += $total;
+            AccountDetail::createDataSaveDept($accounts, 157, $total, AccountDetail::TYPE_HAS, [632],
+                ['product_id' => $p->product_id, 'group' => $group]);
+        }
+        AccountDetail::createDataSaveDept($accounts, 632, $sum, AccountDetail::TYPE_DEPT, [157],
+            ['group' => $group]);
+    }
+}
diff --git a/Modules/Finance/Tests/Feature/BorrowSellPostingFirmTest.php b/Modules/Finance/Tests/Feature/BorrowSellPostingFirmTest.php
new file mode 100644
index 000000000..d03f96cbd
--- /dev/null
+++ b/Modules/Finance/Tests/Feature/BorrowSellPostingFirmTest.php
@@ -0,0 +1,101 @@
+<?php
+
+namespace Modules\Finance\Tests\Feature;
+
+use Tests\TestCase;
+use Illuminate\Foundation\Testing\DatabaseTransactions;
+use Illuminate\Support\Facades\DB;
+use Modules\Finance\Services\BorrowSell\BorrowSellPostingService;
+use Modules\Finance\Entities\BorrowSell\BorrowSell;
+use Modules\Finance\Entities\BorrowSell\BorrowSellProduct;
+
+class BorrowSellPostingFirmTest extends TestCase
+{
+    use DatabaseTransactions;
+
+    /**
+     * HĐ hãng thật trong DB gộp (firm_contracts.id=9) có đủ:
+     *  - firm_support_accounting (id=62), before_vat_* > 0
+     *  - firm_support_accounting_departments (dept 77, is_main=1, dept lead=1056)
+     *  - firm_support_accounting_employees (1 NV, part_id NULL)
+     * Verify bằng SQL thật lúc điều tra task-p2-4 (xem report). Nếu dữ liệu này đã bị xoá/đổi
+     * ở môi trường chạy test → skip thay vì để đỏ vì thiếu data.
+     */
+    private const FIRM_CONTRACT_ID = 9;
+
+    public function test_firm_branch_credits_157_for_cost()
+    {
+        $bs = $this->makeFirmBorrowSellFixture();
+        if ($bs === null) {
+            $this->markTestSkipped('Không tìm thấy HĐ Firm fixture (firm_contracts.id=' . self::FIRM_CONTRACT_ID . ') đủ điều kiện HTHT trong DB test.');
+        }
+
+        [$ok, $accounts, $msg] = app(BorrowSellPostingService::class)->getDataAccounting($bs);
+        $this->assertTrue($ok, $msg);
+
+        $cost157 = collect($accounts)->first(fn($a) => $a['number'] == '157' && $a['type'] == 2);
+        $cost632 = collect($accounts)->first(fn($a) => $a['number'] == '632' && $a['type'] == 1);
+        $this->assertNotNull($cost157, 'Phải có Có 157 (giá vốn hàng gửi bán)');
+        $this->assertNotNull($cost632, 'Phải có Nợ 632');
+        $this->assertEqualsWithDelta($cost157['value'], $cost632['value'], 0.01);
+
+        // Giá vốn nhánh Firm = export_price × qty, KHÔNG nhân unit_coefficient (port ERP
+        // FirmContractBorrowSellService::costAccounting dòng 203). Fixture cố tình dùng
+        // unit_coefficient=5 để bắt lỗi nhân nhầm coefficient: đúng = 900.000×10 = 9.000.000;
+        // nếu nhân coefficient sẽ ra 45.000.000.
+        $this->assertEqualsWithDelta(9000000, $cost157['value'], 0.01,
+            'Giá vốn Firm phải = export_price×qty (KHÔNG nhân unit_coefficient)');
+
+        $this->assertEqualsWithDelta(
+            collect($accounts)->where('type', 1)->sum('value'),
+            collect($accounts)->where('type', 2)->sum('value'),
+            1.0,
+            'Nợ phải cân Có'
+        );
+    }
+
+    private function makeFirmBorrowSellFixture(): ?BorrowSell
+    {
+        $firmExists = DB::table('firm_contracts')->where('id', self::FIRM_CONTRACT_ID)->exists();
+        $saExists = DB::table('firm_support_accounting')
+            ->where('contractable_id', self::FIRM_CONTRACT_ID)
+            ->where('contractable_type', BorrowSell::CONTRACT_FIRM)
+            ->exists();
+        if (!$firmExists || !$saExists) {
+            return null;
+        }
+
+        $bs = new BorrowSell([
+            'id' => 999999001,
+            'code' => 'PXBHM-TEST-P2-4',
+            'status' => 1,
+            'type' => 1,
+            'contractable_type' => BorrowSell::CONTRACT_FIRM,
+            'contractable_id' => self::FIRM_CONTRACT_ID,
+            'created_by' => 1,
+            'sum_amount_after_extra' => 11000000,
+            'sum_amount_after_extra_vat' => 1100000,
+        ]);
+
+        $product = new BorrowSellProduct([
+            'id' => 999999001,
+            'parent_id' => 999999001,
+            'product_id' => 1,
+            'product_name' => 'SP test P2-4',
+            'unit_id' => 1,
+            'price' => 1000000,
+            'extra_price' => 0,
+            'contract_qty' => 10,
+            'qty' => 10,
+            'unit_coefficient' => 5,
+            'export_price' => 900000,
+            'allocated_price' => 0,
+            'rebate_price' => 0,
+            'vat_percent' => 10,
+        ]);
+
+        $bs->setRelation('products', collect([$product]));
+
+        return $bs;
+    }
+}
```
