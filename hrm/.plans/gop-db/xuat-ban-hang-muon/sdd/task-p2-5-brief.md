# Task P2-5 Brief — BorrowSellPostingService: nhánh WrServiceContract (HĐ dịch vụ)

> Đây LÀ yêu cầu của bạn (nguồn sự thật). Các con số/tên cột/chữ ký hàm dùng **nguyên văn** như dưới.
> KHÔNG đọc cả file plan. KHÔNG dùng `git` mạng (chỉ `git add <path>` + `git commit`). KHÔNG spawn subagent.
> Repo: `HRM/hrm-api`, nhánh `gop_db`. DB gộp `erp_hrm_check`. PHP 7.4 / Laravel 8.

## 0. Bối cảnh 1 dòng
Phase 2 phiếu Xuất bán hàng mượn (`BorrowSell`, mã `PXBHM-`). Task 4 đã xong nhánh **FirmContract**
trong `BorrowSellPostingService`. Task 5 bổ sung nhánh còn lại: **WrServiceContract** (HĐ dịch vụ) —
port 1-1 từ ERP `app/Model/Warehouse/BorrowSell.php::getDataCreateDept()` (nhánh
`get_class($contract) == WrServiceContract::class`, dòng 561-720).

## 1. Files
- **Sửa:** `Modules/Finance/Services/BorrowSell/BorrowSellPostingService.php`
  - `getDataAccounting()`: thay nhánh trả lỗi tạm `'Nhánh WrService chưa hỗ trợ (Task 5)'` bằng resolve HĐ dịch vụ + gọi `wrServiceBranch`.
  - `resolveContract()`: rẽ nhánh theo `contractable_type` (thêm nhánh WrService).
  - `postAccounting()`: bỏ điều kiện chỉ resolve cho FIRM (dòng 72-74) → resolve cả 2 loại để lấy meta HĐ.
  - Thêm method `private wrServiceBranch(BorrowSell $bs, Contract $contract, array &$accounts, int &$group): void`.
  - Thêm method `private costAccountingWrService(BorrowSell $bs, array &$accounts, int &$group): void` (giá vốn 1561, ×coef).
  - Thêm const `WORK_CHIET_KHAU = 20;  // CKHH`.
- **Tạo mới (4 entity mirror)** trong `Modules/Finance/Entities/Contract/`:
  - `WrSupportAccounting.php`
  - `WrSupportAccountingDepartment.php`
  - `WrSupportAccountingEmployee.php`
  - `WrSupportAccountingDepartmentDetail.php`
- **Sửa (trait dùng chung — đã được duyệt sửa theo Hướng A):** `Modules/Assign/Services/Accounting/SupportAccountingTrait.php`
  - `monthlyAndQuarterlyCommissionAccounting` + `riskFundAccounting`: khi `$contractCompanyId === null` thì BỎ lọc company.
- **Test:** `Modules/Finance/Tests/Feature/BorrowSellPostingWrServiceTest.php` (tạo mới).

## 2. Sự thật đã verify (dùng làm chân lý, đã kiểm bằng information_schema + đọc nguồn ERP)
1. `borrow_sells.contractable_id` (khi WrService) trỏ THẲNG `wr_service_contracts.id`. Const:
   `BorrowSell::CONTRACT_WR_SERVICE = 'App\\Model\\Customers\\WrServiceContract'` (đã có trong entity `Modules\Finance\Entities\BorrowSell\BorrowSell`).
2. `wr_support_accounting.contractable_type = 'App\\Model\\Customers\\WrServiceContract'` (2471 dòng) = khớp `CONTRACT_WR_SERVICE`.
3. Entity `Modules\Finance\Entities\Contract\WrServiceContract` (ĐÃ CÓ, chỉ đọc, `$table='wr_service_contracts'`) đủ cột shim: `id, code, company_id, department_id, part_id, customer_id, created_by`.
4. **BẪY tên cột (Ruling T5-1):** `wr_support_accounting` KHÔNG có `bonus_contract_before_vat`/`tndn_vat`. Cột tương đương: `contract_performance_bonus_before_vat` + `personal_income_tax`. (firm dùng tên kia — 2 bảng khác nhau.)
5. WR header CÓ: `before_vat_total`, `before_vat_other_cost`, `before_vat_delivery_cost`, `before_vat_product`, `before_vat_repair` (KHÔNG `before_vat_repair_service`), `contract_performance_bonus_before_vat`, `personal_income_tax`.
6. WR dept (`wr_support_accounting_departments`, FK header `wr_support_accounting_id`) — 46 cột parity với firm — đủ: `is_main, department_id, objectable_type, objectable_id, diff_employee_percent, diff_part_lead_percent, diff_department_lead_percent, month_employee_amount, after_settlement_employee_amount, month_part_lead_amount, after_settlement_part_lead_amount, month_department_lead_amount, after_settlement_department_lead_amount, risk_fund_amount`.
7. WR emp (`wr_support_accounting_employees`, FK dept `wr_support_accounting_department_id`) đủ: `employee_id, part_id, commission_sale_percent`.
8. Work `CKHH` id = **20** (bảng `works`, cột `code`). Các work khác (đã khai trong service): DTHH=15, GGHH=16, TTHHD=12, TNST=13, TNSQ=14, RRP=6.
9. **getDataAccounting trả TUPLE** `[bool ok, array accounts, string err]` — test phải destructure, KHÔNG `$accounts = getDataAccounting($bs)`.
10. Cột chi tiết SP là `qty` (KHÔNG `borrow_sell_qty`).
11. Chạy test bằng `php vendor/bin/phpunit --filter=...` (KHÔNG `php artisan test` — fail TTY).

## 3. 4 entity mirror — copy y bộ Assign `SupportAccounting*`, đổi table + FK + thêm 2 accessor

### 3.1 `WrSupportAccounting.php`
```php
<?php

namespace Modules\Finance\Entities\Contract;

use App\Models\BaseModel;

/**
 * HTHT (Hỗ trợ hạch toán) của HĐ DỊCH VỤ — bảng `wr_support_accounting`.
 * Mirror Modules\Assign\Entities\Contract\SupportAccounting (bản HĐ hãng) để dùng lại
 * SupportAccountingTrait. Bảng WR có tên cột thưởng/TNCN KHÁC bảng firm → khai 2 accessor
 * alias để trait (đọc $sa->bonus_contract_before_vat / $sa->tndn_vat) lấy đúng giá trị.
 */
class WrSupportAccounting extends BaseModel
{
    protected $table = 'wr_support_accounting';
    protected $guarded = [];
    public $timestamps = true;

    public function departments()
    {
        return $this->hasMany(WrSupportAccountingDepartment::class, 'wr_support_accounting_id', 'id');
    }

    public function department_main()
    {
        return $this->hasOne(WrSupportAccountingDepartment::class, 'wr_support_accounting_id', 'id')
            ->where('is_main', true);
    }

    /** Alias: trait đọc bonus_contract_before_vat, bảng WR lưu ở contract_performance_bonus_before_vat. */
    public function getBonusContractBeforeVatAttribute()
    {
        return $this->attributes['contract_performance_bonus_before_vat'] ?? 0;
    }

    /** Alias: trait đọc tndn_vat, bảng WR lưu ở personal_income_tax. */
    public function getTndnVatAttribute()
    {
        return $this->attributes['personal_income_tax'] ?? 0;
    }
}
```

### 3.2 `WrSupportAccountingDepartment.php`
```php
<?php

namespace Modules\Finance\Entities\Contract;

use App\Models\BaseModel;

class WrSupportAccountingDepartment extends BaseModel
{
    protected $table = 'wr_support_accounting_departments';
    protected $guarded = [];
    public $timestamps = true;

    public function employees()
    {
        return $this->hasMany(WrSupportAccountingEmployee::class, 'wr_support_accounting_department_id', 'id');
    }

    public function details()
    {
        return $this->hasMany(WrSupportAccountingDepartmentDetail::class, 'wr_support_accounting_department_id', 'id');
    }
}
```

### 3.3 `WrSupportAccountingEmployee.php`
```php
<?php

namespace Modules\Finance\Entities\Contract;

use App\Models\BaseModel;

class WrSupportAccountingEmployee extends BaseModel
{
    protected $table = 'wr_support_accounting_employees';
    protected $guarded = [];
    public $timestamps = true;
}
```

### 3.4 `WrSupportAccountingDepartmentDetail.php`
```php
<?php

namespace Modules\Finance\Entities\Contract;

use App\Models\BaseModel;

class WrSupportAccountingDepartmentDetail extends BaseModel
{
    protected $table = 'wr_support_accounting_department_details';
    protected $guarded = [];
    public $timestamps = true;

    const TYPE_REGULATION = 1;
    const TYPE_PROPOSE = 2;
    const TYPE_APPROVED = 3;
}
```

> ⚠️ Trait dùng `$sa->department_main` (property, không phải `->department_main()`). Eloquent tự
> lazy-load quan hệ qua property. OK.

## 4. Sửa trait — bỏ lọc company khi `$contractCompanyId === null` (Ruling T5-2)

Trong `SupportAccountingTrait.php`, ở CẢ HAI method, đổi điều kiện `continue` để null = không lọc:

`monthlyAndQuarterlyCommissionAccounting` — dòng hiện tại:
```php
        foreach ($sa->departments as $department) {
            if ((int) $this->deptCompany((int) $department->department_id) !== (int) $contractCompanyId) {
                continue;
            }
```
→ sửa thành:
```php
        foreach ($sa->departments as $department) {
            if ($contractCompanyId !== null
                && (int) $this->deptCompany((int) $department->department_id) !== (int) $contractCompanyId) {
                continue;
            }
```

`riskFundAccounting` — y hệt, cùng cách sửa (thêm `$contractCompanyId !== null &&` trước điều kiện so công ty).

> Backward-compatible: `ProductExportPostingService` + Firm branch vẫn truyền company_id thật → hành vi cũ giữ nguyên.
> KHÔNG sửa gì khác trong trait.

## 5. Sửa `BorrowSellPostingService.php`

### 5.1 Imports + const
Thêm imports:
```php
use Modules\Finance\Entities\Contract\WrServiceContract;
use Modules\Finance\Entities\Contract\WrSupportAccounting;
```
Thêm const (cạnh 6 WORK_* hiện có):
```php
    const WORK_CHIET_KHAU = 20;   // CKHH
```

### 5.2 `getDataAccounting()` — thay nhánh WrService
Nhánh `contractable_type === BorrowSell::CONTRACT_FIRM` GIỮ NGUYÊN. Thay đoạn cuối
(`return [false, [], 'Nhánh WrService chưa hỗ trợ (Task 5)'];`) bằng:
```php
        if ($bs->contractable_type === BorrowSell::CONTRACT_WR_SERVICE) {
            $contract = $this->resolveContract($bs);
            if (!$contract) {
                return [false, [], 'Phiếu ' . $bs->code . ' không tra được hợp đồng dịch vụ (contractable_id='
                    . $bs->contractable_id . ')!'];
            }
            try {
                $this->wrServiceBranch($bs, $contract, $accounts, $group);
            } catch (\RuntimeException $e) {
                return [false, [], $e->getMessage()];
            }
            return [true, $accounts, ''];
        }

        return [false, [], 'Phiếu ' . $bs->code . ' có loại hợp đồng không hỗ trợ hạch toán: ' . $bs->contractable_type];
```

### 5.3 `resolveContract()` — rẽ nhánh theo contractable_type
Thay thân method bằng bản rẽ nhánh (giữ logic Firm cũ + thêm WrService):
```php
    private function resolveContract(BorrowSell $bs): ?Contract
    {
        if ($bs->contractable_type === BorrowSell::CONTRACT_FIRM) {
            $firm = FirmContract::find($bs->contractable_id);
            if (!$firm) {
                return null;
            }
            $contract = new Contract($firm->getAttributes());
            $sa = SupportAccounting::where('contractable_id', $firm->id)
                ->where('contractable_type', BorrowSell::CONTRACT_FIRM)
                ->first();
            $contract->setRelation('support_accounting', $sa);
            return $contract;
        }

        if ($bs->contractable_type === BorrowSell::CONTRACT_WR_SERVICE) {
            $wr = WrServiceContract::find($bs->contractable_id);
            if (!$wr) {
                return null;
            }
            $contract = new Contract($wr->getAttributes());
            $sa = WrSupportAccounting::where('contractable_id', $wr->id)
                ->where('contractable_type', BorrowSell::CONTRACT_WR_SERVICE)
                ->first();
            $contract->setRelation('support_accounting', $sa);
            return $contract;
        }

        return null;
    }
```

### 5.4 `postAccounting()` — resolve meta cho cả 2 loại
Đổi dòng 72-74 hiện tại:
```php
        $contract = $bs->contractable_type === BorrowSell::CONTRACT_FIRM
            ? $this->resolveContract($bs)
            : null;
```
→
```php
        $contract = $this->resolveContract($bs);
```
(Phần `$meta` phía dưới giữ nguyên — đã dùng `$contract->... ?? null`.)

### 5.5 Thêm `wrServiceBranch()` — port ERP getDataCreateDept dòng 561-716
```php
    /**
     * Nhánh HĐ DỊCH VỤ — port 1-1 ERP BorrowSell::getDataCreateDept() (nhánh WrServiceContract).
     * KHÁC nhánh Firm: có thêm bút toán CHIẾT KHẤU (5211/CKHH); giá vốn dư Có TK 1561 (KHÔNG 157)
     * và CÓ nhân unit_coefficient; dùng MỘT tỷ lệ percent cho toàn bộ cụm hỗ trợ.
     */
    private function wrServiceBranch(BorrowSell $bs, Contract $contract, array &$accounts, int &$group): void
    {
        $sa = $contract->support_accounting;
        if (!$sa) {
            throw new \RuntimeException('HĐ dịch vụ ' . $contract->code . ' chưa có bảng Hỗ trợ hạch toán (HTHT)!');
        }

        // ---- Block 1: Doanh thu (Nợ 1311 / Có 5111 + 33311) ----
        $gross = (float) ($bs->sum_amount_after_extra ?? 0);
        $gross_vat = (float) ($bs->sum_amount_after_extra_vat ?? 0);
        $group += 1;
        AccountDetail::createDataSaveDept($accounts, 1311, $gross + $gross_vat, AccountDetail::TYPE_DEPT,
            [5111, 33311], ['customer_id' => $contract->customer_id, 'group' => $group]);
        AccountDetail::createDataSaveDept($accounts, 5111, $gross, AccountDetail::TYPE_HAS, [1311],
            ['employee_id' => $contract->created_by, 'employee_department_id' => $contract->department_id,
             'work_id' => self::WORK_DOANH_THU, 'group' => $group]);
        AccountDetail::createDataSaveDept($accounts, 33311, $gross_vat, AccountDetail::TYPE_HAS, [1311],
            ['group' => $group]);

        // ---- Block 2: Chiết khấu (Nợ 5211 + 33311 / Có 1311), work CKHH ----
        $discount = 0;
        $discount_vat = 0;
        foreach ($bs->products as $p) {
            $tmp = (float) $p->rebate_price * (float) $p->qty;
            $discount += $tmp;
            $discount_vat += $tmp * (float) $p->vat_percent / 100;
        }
        $group += 1;
        AccountDetail::createDataSaveDept($accounts, 5211, $discount, AccountDetail::TYPE_DEPT, [1311],
            ['employee_id' => $contract->created_by, 'employee_department_id' => $contract->department_id,
             'work_id' => self::WORK_CHIET_KHAU, 'group' => $group]);
        AccountDetail::createDataSaveDept($accounts, 33311, $discount_vat, AccountDetail::TYPE_DEPT, [1311],
            ['group' => $group]);
        AccountDetail::createDataSaveDept($accounts, 1311, $discount + $discount_vat, AccountDetail::TYPE_HAS,
            [5211, 33311], ['customer_id' => $contract->customer_id, 'group' => $group]);

        // ---- Block 3: Giảm trừ doanh thu (Nợ 5213 + 33311 / Có 1311), work GGHH ----
        $sale_invoice = 0;
        $sale_invoice_vat = 0;
        foreach ($bs->products as $p) {
            $tmp = ((float) $p->price + (float) $p->extra_price - (float) $p->allocated_price - (float) $p->rebate_price) * (float) $p->qty;
            $sale_invoice += $tmp;
            $sale_invoice_vat += (float) $p->vat_percent * $tmp / 100;
        }
        $group += 1;
        AccountDetail::createDataSaveDept($accounts, 5213, $sale_invoice, AccountDetail::TYPE_DEPT, [1311],
            ['employee_id' => $contract->created_by, 'employee_department_id' => $contract->department_id,
             'work_id' => self::WORK_GIAM_TRU_DT, 'group' => $group]);
        AccountDetail::createDataSaveDept($accounts, 33311, $sale_invoice_vat, AccountDetail::TYPE_DEPT, [1311],
            ['group' => $group]);
        AccountDetail::createDataSaveDept($accounts, 1311, $sale_invoice + $sale_invoice_vat, AccountDetail::TYPE_HAS,
            [5213, 33311], ['customer_id' => $contract->customer_id, 'group' => $group]);

        // ---- Block 4: Giá vốn (Nợ 632 / Có 1561), CÓ nhân unit_coefficient ----
        $this->costAccountingWrService($bs, $accounts, $group);

        // ---- Block 5: Cụm hỗ trợ (thưởng HĐ / TNCN / hoa hồng tháng-quý / quỹ rủi ro) ----
        // MỘT tỷ lệ percent cho toàn bộ (khác Firm dùng 2). Port ERP dòng 610-611.
        $before = (float) $sa->before_vat_total - (float) $sa->before_vat_other_cost - (float) $sa->before_vat_delivery_cost;
        $percent = intval($before) ? ($gross - $sale_invoice - $discount) / $before : 0;

        // Thưởng thực hiện HĐ (đọc contract_performance_bonus_before_vat qua accessor alias bonus_contract_before_vat)
        $e1 = $this->bonusContractAccounting($percent, $sa, $contract, $accounts, $group);
        if ($e1) {
            throw new \RuntimeException($e1);
        }
        // TNCN tạm tính (đọc personal_income_tax qua accessor alias tndn_vat)
        $e2 = $this->vatExtraCostAccounting($percent, $sa, $contract, $accounts, $group);
        if ($e2) {
            throw new \RuntimeException($e2);
        }
        // Hoa hồng tháng + quý — truyền null để KHÔNG lọc company (Ruling T5-2)
        $e3 = $this->monthlyAndQuarterlyCommissionAccounting($percent, $sa, null, $accounts, $group);
        if ($e3) {
            throw new \RuntimeException($e3);
        }
        // Quỹ quản lý rủi ro phòng — truyền null để KHÔNG lọc company
        $this->riskFundAccounting($percent, $sa, null, $accounts, $group);
    }
```

### 5.6 Thêm `costAccountingWrService()` — 1561, ×coef
```php
    /**
     * Giá vốn HĐ dịch vụ: mỗi SP dư Có 1561 ref 632; tổng dư Nợ 632 ref 1561.
     * $total = export_price × qty × unit_coefficient — port ERP getDataCreateDept dòng 600
     * (CÓ nhân unit_coefficient, NGƯỢC với nhánh Firm dùng 157 không nhân coefficient).
     */
    private function costAccountingWrService(BorrowSell $bs, array &$accounts, int &$group): void
    {
        $sum = 0;
        $group += 1;
        foreach ($bs->products as $p) {
            $total = round((float) $p->export_price * (float) $p->qty * (float) $p->unit_coefficient);
            $sum += $total;
            AccountDetail::createDataSaveDept($accounts, 1561, $total, AccountDetail::TYPE_HAS, [632],
                ['product_id' => $p->product_id, 'group' => $group]);
        }
        AccountDetail::createDataSaveDept($accounts, 632, $sum, AccountDetail::TYPE_DEPT, [1561],
            ['group' => $group]);
    }
```

## 6. Test — `BorrowSellPostingWrServiceTest.php`

Bám mẫu `BorrowSellPostingFirmTest.php` (in-memory fixture, `DatabaseTransactions`, markTestSkipped nếu thiếu HTHT).

Yêu cầu:
1. Chọn 1 `wr_service_contracts.id` THẬT có `wr_support_accounting` (contractable_type=WrServiceContract) VÀ HTHT cấu hình đủ trưởng phòng (phòng is_main có `departments.department_lead_id` khác NULL) → nếu không thoả thì `markTestSkipped`. Tự tìm id hợp lệ bằng SQL trước khi hard-code (gợi ý điểm khởi đầu: id 139 — có wr_support_accounting id=64; nếu id này thiếu trưởng phòng thì tìm id khác qua query join `departments`).
2. Build in-memory `BorrowSell` (`contractable_type = BorrowSell::CONTRACT_WR_SERVICE`, `contractable_id` = id đã chọn, `sum_amount_after_extra` / `sum_amount_after_extra_vat` khớp SP) + 1 `BorrowSellProduct` với: `price=1000000, extra_price=0, allocated_price=0, rebate_price=100000, qty=10, unit_coefficient=5, export_price=900000, vat_percent=10`. `setRelation('products', collect([...]))`.
   - `sum_amount_after_extra` = tổng thành tiền sau extra trước giảm trừ. Với 1 SP: dùng `(price+extra_price)*qty = 10.000.000`. `sum_amount_after_extra_vat = 1.000.000`.
3. Gọi `[$ok, $accounts, $msg] = app(BorrowSellPostingService::class)->getDataAccounting($bs);` — assert `$ok` (message `$msg` khi fail).
4. **Assert giá vốn CÓ nhân coefficient (regression chính, ngược Firm):**
   ```php
   $cost1561 = collect($accounts)->first(fn($a) => $a['number'] == '1561' && $a['type'] == 2);
   $cost632  = collect($accounts)->first(fn($a) => $a['number'] == '632'  && $a['type'] == 1);
   $this->assertNotNull($cost1561, 'Phải có Có 1561 (giá vốn HĐ dịch vụ)');
   $this->assertEqualsWithDelta($cost1561['value'], $cost632['value'], 0.01);
   $this->assertEqualsWithDelta(45000000, $cost1561['value'], 0.01,
       'Giá vốn WrService = export_price×qty×unit_coefficient = 900000×10×5');
   ```
5. **Assert có block chiết khấu (work CKHH):**
   ```php
   $ck = collect($accounts)->first(fn($a) => $a['number'] == '5211' && ($a['work_id'] ?? null) == BorrowSellPostingService::WORK_CHIET_KHAU);
   $this->assertNotNull($ck, 'Phải có Nợ 5211 chiết khấu (work CKHH)');
   $this->assertEqualsWithDelta(1000000, $ck['value'], 0.01, 'Chiết khấu = rebate_price×qty = 100000×10');
   ```
6. **Assert cân Nợ = Có:**
   ```php
   $this->assertEqualsWithDelta(
       collect($accounts)->where('type', 1)->sum('value'),
       collect($accounts)->where('type', 2)->sum('value'),
       1.0, 'Nợ phải cân Có'
   );
   ```
7. (Khuyến khích) assert cụm thưởng HĐ có phát sinh nếu HTHT có `contract_performance_bonus_before_vat > 0`: tồn tại ít nhất 1 bút toán `5211` với work TTHHD (=12) — bắt lỗi accessor alias thiếu (Ruling T5-1). Nếu HTHT của contract có bonus=0 thì bỏ assert này, KHÔNG ép.

> ⚠️ Chú ý cột kết quả `AccountDetail::createDataSaveDept`: khóa `number`/`value`/`type`/`work_id` như test Firm. Nếu `$a['work_id']` không tồn tại trên vài dòng thì dùng `($a['work_id'] ?? null)`.

Chạy:
```bash
php vendor/bin/phpunit --filter=BorrowSellPostingWrServiceTest Modules/Finance/Tests/Feature/BorrowSellPostingWrServiceTest.php
```

## 7. Ràng buộc chung (Global Constraints — luôn áp dụng)
- gop_db: KHÔNG dùng `DB_CONNECTION_SECOND`/`mysql2`; bảng trùng tên ưu tiên bản ERP.
- KHÔNG đọc `vendor/`, `node_modules/`.
- Cờ phân quyền fail-closed (không liên quan task này nhưng giữ nguyên tắc).
- Commit: chỉ `git add <path cụ thể>` + `git commit` (KHÔNG push/fetch/pull). Message tiếng Việt, prefix `feat(finance):`.
- KHÔNG spawn subagent. KHÔNG sửa Phase 1. KHÔNG đụng nhánh Firm đã xong (chỉ THÊM, không sửa logic Firm trong `firmBranch`/`costAccounting`).

## 8. Report
Ghi report đầy đủ vào `HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-p2-5-report.md`, trả về chat CHỈ:
status (DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED), danh sách commit, 1 dòng tóm tắt kết quả test, và concerns (nếu có).
Report gồm: files đổi, cách chọn contract fixture (+id), giá trị bút toán thực tế (tổng Nợ/Có, giá vốn, chiết khấu, thưởng/TNCN nếu có), và bất kỳ điểm lệch nào so với brief kèm lý do.
