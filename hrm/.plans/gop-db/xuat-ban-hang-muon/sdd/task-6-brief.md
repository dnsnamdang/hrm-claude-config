# Task 6 — BorrowSellRequestService (store + duyệt + notify + searchByFilter)

**Repo:** `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api` (nhánh gop_db, Laravel 8, PHP 7.4). Mọi lệnh chạy trong thư mục này. DB gộp `erp_hrm_check` (bảng ERP + HRM chung 1 DB). **KHÔNG dùng `DB_CONNECTION_SECOND`/`mysql2`.** KHÔNG đọc `vendor/`. KHÔNG commit/push. KHÔNG dispatch subagent.

Đây là task LỚN nhất (port ~450 dòng ERP). Đọc kỹ toàn bộ brief này TRƯỚC KHI code — brief chứa TẤT CẢ code ERP đã trace sẵn + các bản vá bắt buộc. KHÔNG cần đọc plan file gốc.

Bối cảnh: feature "yêu cầu xuất bán hàng mượn" port ERP→HRM. Task 1-5 đã xong: permissions seeder, 5 entity con, entity cha `BorrowSellRequest`, `BorrowSellRequestCalculator`, `BorrowSellRequestSourceService`. Task 6 viết Service điều phối: tạo phiếu (store), duyệt (TP/BGD), từ chối, thông báo, và (trên ENTITY) searchByFilter + meta.

---

## 0. RULINGS BẮT BUỘC ÁP DỤNG (đọc trước — đã quyết, KHÔNG tự đổi)

1. **`searchByFilter()` và `meta()` đặt TRÊN ENTITY `BorrowSellRequest` (public static), KHÔNG trong Service.** Lý do: chúng cần các helper quyền của trait `ChecksEmployeePermission` (`currentEmployeeHasPermission`, `currentEmployeeIsSuperAdmin`, `currentCompanyId`, `currentManagedDepartmentIds`) — các method này là `protected static`, chỉ gọi được TỪ TRONG class dùng trait. Service là class riêng → KHÔNG gọi được. Cách này cũng khớp ERP (`BorrowSellRequest::searchByFilter`). → Task 6 THÊM 2 method này vào file entity `Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequest.php`.

2. **FIX cột hạn mức: dùng `limit_debt_export` (KHÔNG phải `limit_export_debt`).** ERP controller:611 đọc `->limit_export_debt` là BUG CHẾT NGẦM (đọc attr không tồn tại → null → over-limit không bao giờ kích). Cột thật (model ERP DeclareLimitDebt $fillable + merged DB) = `limit_debt_export`. Dùng `->value('limit_debt_export')`. Đây là điểm HRM SỬA đúng bug ERP — trọng tâm luồng escalation TP→BGD Phase 1.

3. **FIX morph OpeningContract: dùng `'App\\Model\\Accounting\\OpeningContract'` (KHÔNG phải `App\\Model\\Sale\\OpeningContract`).** Merged DB `account_details.contractable_type` thực tế = `App\Model\Accounting\OpeningContract`.

4. **`returningQty` KHÔNG có sẵn trong SourceService** (Task 5 chỉ có `borrowedDetails`). Port `getReturningQty()` thành private helper TRONG Service (code đầy đủ ở Mục 4). Calculator::availableSellQty đã nhận `returningQty` làm tham số.

5. **Mọi lỗi validate → `throw \Illuminate\Validation\ValidationException::withMessages([...])`** (CLAUDE.md: BE phải rethrow ValidationException, KHÔNG catch chung Exception, KHÔNG `abort(422)` cho lỗi nghiệp vụ). Controller (Task 8) sẽ bắt và format. Trong `DB::transaction`, ValidationException tự rollback (không cần rollback thủ công) — nhưng ĐẶT các check nặng (over-limit, diff-price) TRƯỚC khi mở transaction như ERP.

6. **Over-limit KHÔNG phải lỗi.** Nó quyết `status`: over-limit → `CHO_TP_DUYET(10)`; ngược lại → `CHO_KE_TOAN_KHO(2)`. Service TỰ quyết status, KHÔNG tin `status` từ FE.

7. **unit_coefficient trong store**: dùng private helper query `product_units` (giống Task 5 nhưng SourceService::unitCoefficient là private → Service tự có helper riêng, chấp nhận trùng 3 dòng để giữ ranh giới task).

8. **Entity boot() (Task 3) đã tự set `created_by`, `company_id`, `department_id`** khi save → store() KHÔNG set thủ công 3 cột này.

---

## 1. File tạo/sửa
- **Create:** `Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestService.php`
- **Modify:** `Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequest.php` — THÊM `public static function searchByFilter($request)` + `public static function meta(): array` (Mục 7). Chỉ THÊM, không sửa method sẵn có.

## Interfaces
- Consumes: `BorrowSellRequest` (entity Task 3, các const + relations + syncTabs), `BorrowSellRequestProduct`, `BorrowSellRequestProductDetail` (entity Task 2), `BorrowSellRequestCalculator` (Task 4: `availableSellQty`, `isQtyExceeded`, `isOverLimitDebt`), `BorrowSellRequestSourceService` (Task 5: `firmExportingQty`, `firmBorrowingQty` — public? xem chú ý), `Modules\Timesheet\Services\EmployeeInfoService::sendNotification`.
- **Chú ý visibility SourceService**: `firmExportingQty`/`firmBorrowingQty` trong Task 5 là `private`. Service Task 6 cần gọi `firmBorrowingQty` (guard quỹ HĐ, Mục 3 store). → THÊM 2 method này (hoặc dùng lại) bằng cách: Task 5 SourceService cần đổi `firmExportingQty` + `firmBorrowingQty` sang `public` (chỉ đổi visibility, KHÔNG đổi logic). ĐÂY LÀ THAY ĐỔI DUY NHẤT được phép trên file Task 5. Nếu không muốn đụng Task 5, tự viết `firmInflightQty()` private trong Service port lại 2 method — nhưng ưu tiên đổi visibility (DRY). Ghi rõ lựa chọn vào report.
- Produces (Service): `store(Request): BorrowSellRequest`, `deny(BorrowSellRequest,string): void`, `managerApprove(BorrowSellRequest): void`, `switchBoardOfManager(BorrowSellRequest): void`, `boardOfManagerApprove(BorrowSellRequest): void`, `getDebtCustomerByEmployee(int): float`.
- Produces (Entity): `BorrowSellRequest::searchByFilter($request)` (trả query builder, controller `.paginate()`), `BorrowSellRequest::meta(): array`.

---

## 2. Khung Service + store() — port ERP store() (controller dòng 179-451)

Header:
```php
<?php
namespace Modules\Finance\Services\BorrowSellRequest;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Illuminate\Validation\ValidationException;
use Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest;
use Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequestProduct;
use Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequestProductDetail;
use Modules\Timesheet\Services\EmployeeInfoService;

class BorrowSellRequestService
{
    // morph objectable của dòng SP (khớp chuỗi class ERP lưu trong borrow_sell_request_products.objectable_type)
    const OBJECTABLE_FIRM = 'App\Model\Sale\Firm\Contract\FirmContractTabProduct';
    const OBJECTABLE_WR_SERVICE = 'App\Model\Customers\WrServiceContractItem';
    const XUAT_MUON = 3;         // ProductExportRequest type "Xuất mượn" (ExportModel::XUAT_MUON)
    const DA_MUON = 2;           // ProductExportRequest borrow_status "Đã mượn"
    const DON_HANG_NGUYEN_TAC = 8; // FirmContract::DON_HANG_NGUYEN_TAC (check diff-price)

    protected $source;
    public function __construct(BorrowSellRequestSourceService $source) { $this->source = $source; }
```

### store() — logic tuần tự (port ERP 179-451, thay Response::json → throw/return Model)

**Bước tiền-kiểm (NGOÀI transaction, đúng thứ tự ERP):**
1. `$isFirm = $request->contractable_type === BorrowSellRequest::CONTRACT_FIRM;`
2. Load hợp đồng + check `canProductExport`. ERP 230-244: nếu Firm → `FirmContract::find`; nếu WrService → `WrServiceContract::find`; gọi `$contract->canProductExport()`. **HRM**: dùng query builder đọc bảng `firm_contracts` / `wr_service_contracts` lấy hàng (`id, customer_id, customer_type, customer_name, customer_address, customer_mobile, customer_contact_name, customer_contact_phone, contact_address, type, price_type, support_accounting_id, need_check_exported`). `canProductExport()` là accessor nghiệp vụ ERP — Phase 1 KHÔNG port đầy đủ trạng thái HĐ; **RULING: coi hợp đồng hợp lệ nếu tồn tại + có `support_accounting_id`** (check support_accounting ở bước 4 đã bao). Nếu tìm không thấy HĐ → `ValidationException::withMessages(['contractable_id'=>['Không thể chọn hợp đồng này!']])`.
   - Lưu ý: đọc cột thực tế của `firm_contracts`/`wr_service_contracts` bằng `Schema::getColumnListing` trước khi select (tên cột support_accounting có thể là `support_accounting_id`); nếu cột khác → sửa. Report ghi cột đã dùng.
3. Với mỗi `$id` trong `$request->product_export_request_ids`: check "can_borrow_sell". Port accessor ERP (ProductExportRequest.php:1482):
   `can_borrow_sell = (created_by == auth()->id()) && (status == 5 || borrow_status == 2)`.
   Query builder: `DB::table('product_export_requests')->where('id',$id)->first(['created_by','status','borrow_status'])`. Nếu KHÔNG can_borrow_sell → `ValidationException::withMessages(['product_export_request_ids'=>['Có yêu cầu xuất mượn không hợp lệ!']])`.
4. `support_accounting`: nếu HĐ không có `support_accounting_id` → `ValidationException::withMessages(['contractable_id'=>['Hợp đồng không có hỗ trợ hạch toán']])`.
5. **over-limit** (Mục 5): `$overLimit = $request->boolean('check_over_limit_export') && $this->isOverLimit($request,(int)$contract->customer_id);` → `$status = $overLimit ? BorrowSellRequest::CHO_TP_DUYET : BorrowSellRequest::CHO_KE_TOAN_KHO;`
6. **diff-price** (Mục 6): `$this->assertDiffPrice($request, $contract, $isFirm, $status);` (throw nếu lệch giá).

**Trong `DB::transaction(function() {...})`:**
7. Tạo `$object = new BorrowSellRequest();` set: `code='TMP-'.uniqid()` (tạm, generateCode() ghi đè sau khi có id), `type=(int)$request->type`, `status=$status`, `contractable_id=$contract->id`, `contractable_type=$request->contractable_type`, snapshot khách (`customer_id,customer_type,customer_name,customer_address,customer_mobile,customer_contact_name,customer_contact_phone,contact_address` từ `$contract`), `note=$request->note`, `firm_tab_vat_percent=$request->firm_tab_vat_percent`, `need_repair=$request->need_repair ?? 0`, các cột tiền (`vat_percent, vat_cost_allocated, sum_amount_allocated, sum_amount_allocated_after_vat, sum_amount_after_extra, sum_amount_after_extra_vat, sum_amount_after_extra_after_vat` từ `$request` nếu có gửi — dùng `$request->input(...)`, nullable). KHÔNG set created_by/company_id/department_id (boot lo). `$object->save();` rồi `$object->generateCode();` (entity method sinh `PYCXBHM-xxxxx`, tự save code).
8. `$object->product_export_requests()->sync((array)$request->product_export_request_ids);`
9. `$hasChange = $this->syncProducts($object, $request, $contract, $isFirm);` (Mục 3).
10. Nếu `$isFirm && $request->tabs`: `$object->syncTabs($request->tabs);` (entity method Task 3).
11. Nếu `!$hasChange` → `throw ValidationException::withMessages(['products'=>['Không có thay đổi']]);`
12. `$this->notifyAfterStore($object);` (Mục 6-notify).
13. `return $object;`

Ví dụ khung (điền chi tiết từ các bước trên):
```php
public function store(Request $request): BorrowSellRequest
{
    $isFirm = $request->contractable_type === BorrowSellRequest::CONTRACT_FIRM;
    $contract = $this->loadContract($request->contractable_type, (int)$request->contractable_id, $isFirm);
    if (!$contract) {
        throw ValidationException::withMessages(['contractable_id' => ['Không thể chọn hợp đồng này!']]);
    }
    foreach ((array)$request->product_export_request_ids as $id) {
        if (!$this->canBorrowSell((int)$id)) {
            throw ValidationException::withMessages(['product_export_request_ids' => ['Có yêu cầu xuất mượn không hợp lệ!']]);
        }
    }
    if (empty($contract->support_accounting_id)) {
        throw ValidationException::withMessages(['contractable_id' => ['Hợp đồng không có hỗ trợ hạch toán']]);
    }
    $overLimit = $request->boolean('check_over_limit_export')
        && $this->isOverLimit($request, (int)$contract->customer_id);
    $status = $overLimit ? BorrowSellRequest::CHO_TP_DUYET : BorrowSellRequest::CHO_KE_TOAN_KHO;
    $this->assertDiffPrice($request, $contract, $isFirm, $status);

    return DB::transaction(function () use ($request, $contract, $isFirm, $status) {
        $object = new BorrowSellRequest();
        // ... set fields (bước 7) ...
        $object->save();
        $object->generateCode();
        $object->product_export_requests()->sync((array)$request->product_export_request_ids);
        $hasChange = $this->syncProducts($object, $request, $contract, $isFirm);
        if ($isFirm && $request->tabs) { $object->syncTabs($request->tabs); }
        if (!$hasChange) { throw ValidationException::withMessages(['products' => ['Không có thay đổi']]); }
        $this->notifyAfterStore($object);
        return $object;
    });
}
```

---

## 3. syncProducts() — port loop SP ERP (controller 315-419)

Trả `bool $hasChange`. Với mỗi `$product` trong `$request->products` (bỏ qua nếu thiếu `details`):
- Tạo `$p = new BorrowSellRequestProduct();`
- Lấy `$contract_product` + `$contract_qty` + `objectable_type`:
  - **Firm** (`$request->contractable_type === FirmContract`): query `firm_contract_tab_products` where `firm_contract_id=$object->contractable_id, product_id=$product['product_id'], unit_id=$product['unit_id']` và `whereIn('parent_id', $request->firm_tab_ids)`; `$contract_qty = sum(quantity)`; `$contract_product = hàng đầu tiên`; `$p->objectable_type = self::OBJECTABLE_FIRM;`
  - **WrService**: query `wr_service_contract_items` where `id=$product['wr_service_contract_item_id']` (firstOrFail → nếu null throw ValidationException); `$contract_qty = $contract_product->qty`; `$p->objectable_type = self::OBJECTABLE_WR_SERVICE;`
  - `$p->objectable_id = $contract_product->id;`
- Metadata SP (port ERP 341-360) qua query builder (gotcha gop_db: `products` KHÔNG có brand_name/unit_id → join): 
  - `products` where id=`$contract_product->product_id` → `model_id, brand_id, code`
  - `units` where id=`$contract_product->unit_id` → `name` (unit_name)
  - `product_models` where id=`products.model_id` → `name` (model_name)
  - `brands` where id=`products.brand_id` → `name` (brand_name)
  - `$unitCoef = $this->unitCoefficient($contract_product->product_id, $contract_product->unit_id);` (Mục 7 helper)
- Set `$p`: `parent_id=$object->id, product_id, product_name (=$contract_product->product_name), unit_id, unit_name, model_id, model_name, brand_id, brand_name, code, contract_qty=$contract_qty, unit_coefficient=$unitCoef, price=$product['price']??0, extra_price=$product['extra_price']??0, allocated_price=$product['allocated_price']??0, rebate_price=$product['rebate_price']??0, net_price=$product['net_price']??0, vat_percent=$product['vat_percent']??0, qty=0, approved_qty=0, returned_qty=0`. `$p->save();`
- `$qty = 0;` Loop `$product['details']`:
  - Nếu `$detail['product_export_request_id']` KHÔNG nằm trong `$request->product_export_request_ids` → `throw ValidationException::withMessages(['products'=>['Dữ liệu không hợp lệ']]);`
  - `$request_product = DB::table('product_export_request_details')->where('parent_id',$detail['product_export_request_id'])->where('product_id',$p->product_id)->first();` (null → ValidationException 'Dữ liệu không hợp lệ').
  - **check SL đã mượn** (port ERP 377-378 qua Calculator):
    ```php
    $returning = $this->returningQty((int)$detail['product_export_request_id'], (int)$p->product_id);
    $available = BorrowSellRequestCalculator::availableSellQty(
        (float)$request_product->base_exported_qty,
        (float)$request_product->borrow_returned_qty,
        (float)$returning,
        (float)$unitCoef
    );
    if (BorrowSellRequestCalculator::isQtyExceeded($available, (float)$unitCoef, (float)$detail['qty'])) {
        throw ValidationException::withMessages(['products' => ['Số lượng không hợp lệ']]);
    }
    ```
  - `$qty += $detail['qty']; if ($detail['qty'] > 0) $hasChange = true;`
  - Tạo `$d = new BorrowSellRequestProductDetail();` set: `parent_id=$p->id, request_id=$object->id, product_export_request_id=$detail['product_export_request_id'], product_export_request_detail_id=$request_product->id, unit_id=$request_product->unit_id, product_id=$p->product_id, qty=$detail['qty'], approved_qty=0`. `$d->save();`
- Sau details: `$p->qty = $qty; $p->save();`
- **check quỹ HĐ in-flight** (port ERP 403-418):
  ```php
  $inflight = 0;
  if ($isFirm) {
      $inflight = $this->source->firmExportingQty($object->contractable_id, (int)$contract_product->parent_id, (int)$p->product_id, null)
                + $this->source->firmBorrowingQty($object->contractable_id, (int)$contract_product->parent_id, (int)$p->product_id, $object->id);
  }
  $needCheck = $isFirm ? true : (bool)($contract->need_check_exported ?? true);
  if ($needCheck && ($contract_qty - $contract_product->exported_qty - $inflight) < $qty) {
      throw ValidationException::withMessages(['products' => ['Số lượng không hợp lệ']]);
  }
  ```
  (`$contract_product->parent_id` = firm_contract_tab_id. WrService không có in-flight quỹ ở đây → inflight=0, needCheck theo `need_check_exported`.)

Trả `$hasChange`.

> **Chú ý firmBorrowingQty ở đây TRUYỀN `$object->id`** để loại chính phiếu đang tạo (except). Ở LOAD (Task 5) KHÔNG trừ borrowingQty — nhưng ở STORE thì CÓ (đúng ERP:407). Đừng nhầm.

---

## 4. returningQty() — port ProductExportRequestDetail::getReturningQty() (ERP Model/Warehouse/ProductExportRequestDetail.php:65)

Private helper. Guard: phiếu cha (`product_export_requests.type`) phải == XUAT_MUON(3), nếu không trả 0. Tổng 3 nguồn SL "đang trả về" (in-flight), mỗi nguồn `SUM(qty * unit_coefficient)` theo `product_export_request_id = $exportRequestId` + `product_id`:
```php
private function returningQty(int $exportRequestId, int $productId): float
{
    $parentType = DB::table('product_export_requests')->where('id', $exportRequestId)->value('type');
    if ((int)$parentType !== self::XUAT_MUON) return 0;

    // 1) YC nhập lại (product_import_requests chưa hoàn thành)
    $import = (float) DB::table('product_import_request_details as pird')
        ->join('product_import_requests as pir', 'pird.parent_id', '=', 'pir.id')
        ->where('pird.product_id', $productId)
        ->where('pir.is_complete', false)
        ->where('pir.product_export_request_id', $exportRequestId)
        ->sum(DB::raw('pird.qty * pird.unit_coefficient'));

    // 2) YC xuất bán hàng mượn khác đang chờ duyệt (status=2)
    $sell = (float) DB::table('borrow_sell_request_product_details as bsrpd')
        ->join('borrow_sell_request_products as bsrp', 'bsrpd.parent_id', '=', 'bsrp.id')
        ->join('borrow_sell_requests as bsr', 'bsrp.parent_id', '=', 'bsr.id')
        ->where('bsrp.product_id', $productId)
        ->where('bsr.status', 2)
        ->where('bsrpd.product_export_request_id', $exportRequestId)
        ->sum(DB::raw('bsrpd.qty * bsrp.unit_coefficient'));

    // 3) YC xuất trả khác đang chờ (borrow_export_requests status=2)
    $other = (float) DB::table('borrow_export_request_product_details as berpd')
        ->join('borrow_export_request_products as berp', 'berpd.parent_id', '=', 'berp.id')
        ->join('borrow_export_requests as ber', 'berp.parent_id', '=', 'ber.id')
        ->where('berp.product_id', $productId)
        ->where('ber.status', 2)
        ->where('berpd.product_export_request_id', $exportRequestId)
        ->sum(DB::raw('berp.qty * berp.unit_coefficient'));  // LƯU Ý: ERP dùng berpd.qty * berp.unit_coefficient — dùng berpd.qty

    return $import + $sell + $other;
}
```
**SỬA lại nguồn 3 cho đúng ERP: `SUM(berpd.qty * berp.unit_coefficient)`** (qty ở detail berpd, coefficient ở product berp). Ba bảng đã verify tồn tại + `unit_coefficient` nằm ở pird/bsrp/berp. Phiếu đang tạo chưa có bản ghi nên không cần except.

---

## 5. isOverLimit() + getDebtCustomerByEmployee() (port controller 599-639 + 713-730, ÁP FIX #2 #3)

```php
private function isOverLimit(Request $request, int $customerId): bool
{
    $companyId = auth()->user()->info->company_id ?? null;
    $limit = DB::table('declare_limit_debts')
        ->where('customer_id', $customerId)
        ->where('company_id', $companyId)
        ->value('limit_debt_export');          // FIX #2: limit_debt_export (KHÔNG limit_export_debt)
    $currentDebt = $this->getDebtCustomerByEmployee($customerId);
    return BorrowSellRequestCalculator::isOverLimitDebt(
        $limit === null ? null : (float)$limit,
        (float)$currentDebt,
        (float)$request->input('sum_amount_after_extra_after_vat', 0)
    );
}

public function getDebtCustomerByEmployee(int $customerId): float
{
    $accountIds = DB::table('accounts')->where('identify_number_parent', 131)->pluck('id')->all();
    if (empty($accountIds)) return 0;
    $row = DB::table('account_details')
        ->selectRaw('SUM(CASE WHEN type = 1 THEN money_value_exchange ELSE 0 END) as total_debt')
        ->selectRaw('SUM(CASE WHEN type = 2 THEN money_value_exchange ELSE 0 END) as total_has')
        ->where('customer_id', $customerId)
        ->whereIn('account_id', $accountIds)
        ->whereIn('contractable_type', [
            BorrowSellRequest::CONTRACT_FIRM,             // App\Model\Sale\Firm\Contract\FirmContract
            BorrowSellRequest::CONTRACT_WR_SERVICE,       // App\Model\Customers\WrServiceContract
            'App\\Model\\Accounting\\OpeningContract',    // FIX #3 (KHÔNG App\Model\Sale\OpeningContract)
        ])
        ->where('created_by', auth()->id())
        ->first();
    return (float)(($row->total_debt ?? 0) - ($row->total_has ?? 0));
}
```

---

## 6. assertDiffPrice() + notify

### assertDiffPrice() — port checkDiffPrice (controller 641-711)
Chỉ áp khi `$isFirm && (int)$contract->type === self::DON_HANG_NGUYEN_TAC(8) && !in_array($status, [3,4])`. Gom products (từ `$request->tabs[].products` nếu có tabs, ngược lại `$request->products`). Với mỗi product so giá catalog hiện tại vs giá trên đơn nguyên tắc:
- Giá đơn nguyên tắc: `firm_contract_tab_products` where firm_contract_id=$contract->id → map `product_id.'_'.unit_id => price`.
- Giá catalog: port `Product::getPriceByUnitAndType($product_id,$unit_id,$contract->price_type)->price` → query builder trên bảng giá SP (tìm bảng qua grep ERP `getPriceByUnitAndType`; Phase 1 nếu quá phức tạp, đọc method ERP và port tối giản). Nhân hệ số công ty: `product_company_coefficients` where product_id + company_id → `coefficient`; nếu `!=1`: `$price = round($price * $coef / 1000) * 1000`.
- So `floatValue($catalog) != floatValue($contractPrice)` (chuẩn hoá bỏ dấu phẩy) → thêm `{product_id,unit_id}` vào danh sách lệch. Bỏ qua SP không có trên đơn (contractPrice null).
- Nếu có lệch → `throw ValidationException::withMessages(['products' => ['Sản phẩm có sự thay đổi về giá. Không thể xuất!']]);` **và** đính danh sách lệch: đặt thêm key `change_price` = mảng `[{product_id,unit_id}]` dạng JSON để FE/Task 8 đọc (ví dụ `withMessages(['products'=>[...], 'change_price'=>[json_encode($ids)]])`). RULING: giữ message + danh sách; `type='change-price'` là việc Task 8 controller gắn khi bắt exception.

> Nếu `getPriceByUnitAndType`/bảng giá quá rối để port trong Phase 1 → KHÔNG bỏ check âm thầm. Ghi rõ vào report phần "cần chốt" và port khung so-giá dựa trên cột `price` của `firm_contract_tab_products` so với chính nó (no-op an toàn = luôn pass) CHỈ KHI thực sự bế tắc; ưu tiên port đúng. Đọc ERP `Product::getPriceByUnitAndType` trước khi quyết.

### notifyAfterStore() + notifyInfoIds() + notifyCreator()
```php
private function notifyAfterStore(BorrowSellRequest $m): void
{
    if ($m->status == BorrowSellRequest::CHO_KE_TOAN_KHO) {
        $ids = BorrowSellRequest::employeeInfoIdsHavingPermission(BorrowSellRequest::PERMISSION_KE_TOAN_KHO, $m->company_id);
        $this->notifyInfoIds($ids, $m, '[XBHM] Gửi duyệt: ' . $m->code . '. Vừa tạo yêu cầu xuất bán hàng mượn');
    } elseif ($m->status == BorrowSellRequest::CHO_TP_DUYET) {
        $ids = BorrowSellRequest::employeeInfoIdsHavingPermission(BorrowSellRequest::PERMISSION_TP_APPROVE, $m->company_id);
        $this->notifyInfoIds($ids, $m, '[XBHM] Chờ TP duyệt: ' . $m->code . '. Yêu cầu vượt hạn mức công nợ cần trưởng phòng duyệt');
    }
}

private function notifyInfoIds(array $employeeInfoIds, BorrowSellRequest $m, string $title): void
{
    $data = ['url' => '/finance/borrow-sell-requests/' . $m->id, 'title' => $title, 'type' => 'borrowSellRequest', 'id' => $m->id];
    foreach (array_unique($employeeInfoIds) as $infoId) {
        try { EmployeeInfoService::sendNotification($infoId, $data); }
        catch (\Throwable $e) { Log::error('[BorrowSellRequest] notify fail phiếu ' . $m->id . ': ' . $e->getMessage()); }
    }
}

private function notifyCreator(BorrowSellRequest $m, string $title): void
{
    $infoId = (int) DB::table('employees')->where('id', $m->created_by)->value('employee_info_id');
    if ($infoId) { $this->notifyInfoIds([$infoId], $m, $title); }
}
```
(Template thông báo `[PREFIX] {Nhóm}: {Tên}. {Ghi chú}` + deep-link kèm id — đã có url+id. Prefix `[XBHM]` theo plan; nếu skill notification-convention có prefix chuẩn khác cho Finance thì đọc `.claude/skills/notification-convention/SKILL.md` và chỉnh cho khớp, ghi vào report.)

---

## 7. deny / managerApprove / switchBoardOfManager / boardOfManagerApprove (port controller 491-597)

Các method này CHỈ đổi status + notify. **Quyền duyệt (canApprove/canManagerApprove/...) do CONTROLLER Task 8 gate qua entity trước khi gọi** — Service KHÔNG tự check quyền.
```php
public function deny(BorrowSellRequest $m, string $comment): void
{
    DB::transaction(function () use ($m, $comment) {
        $m->comment = $comment;
        $m->approver_id = auth()->id();
        $m->approved_time = now();
        $m->status = BorrowSellRequest::KHONG_DUYET;   // 4
        $m->save();
    });
    $this->notifyCreator($m, '[XBHM] Từ chối: ' . $m->code . '. Yêu cầu xuất bán hàng mượn bị từ chối');
}

public function managerApprove(BorrowSellRequest $m): void   // TP duyệt: 10 -> 2
{
    $m->status = BorrowSellRequest::CHO_KE_TOAN_KHO;
    $m->save();
    $this->notifyInfoIds(BorrowSellRequest::employeeInfoIdsHavingPermission(BorrowSellRequest::PERMISSION_KE_TOAN_KHO, $m->company_id), $m, '[XBHM] Gửi duyệt: ' . $m->code . '. TP đã duyệt yêu cầu xuất bán hàng mượn');
}

public function switchBoardOfManager(BorrowSellRequest $m): void   // TP chuyển BGD: 10 -> 11
{
    $m->status = BorrowSellRequest::CHO_BGD_DUYET;
    $m->save();
    $this->notifyInfoIds(BorrowSellRequest::employeeInfoIdsHavingPermission(BorrowSellRequest::PERMISSION_BGD_APPROVE, $m->company_id), $m, '[XBHM] Chờ BGD duyệt: ' . $m->code . '. Yêu cầu cần ban giám đốc duyệt');
}

public function boardOfManagerApprove(BorrowSellRequest $m): void   // BGD duyệt: 11 -> 2
{
    $m->status = BorrowSellRequest::CHO_KE_TOAN_KHO;
    $m->save();
    $this->notifyInfoIds(BorrowSellRequest::employeeInfoIdsHavingPermission(BorrowSellRequest::PERMISSION_KE_TOAN_KHO, $m->company_id), $m, '[XBHM] Gửi duyệt: ' . $m->code . '. BGD đã duyệt yêu cầu xuất bán hàng mượn');
}
```
(ERP switchBoardOfManager notify quyền `'Ban giám đốc duyệt xuất hàng vượt hạn mức công nợ'` = PERMISSION_BGD_APPROVE. ERP boardOfManagerApprove không có sẵn hàm riêng — HRM chuẩn hoá 11→2 như trên.)

### unitCoefficient() private (helper Mục 3)
```php
private function unitCoefficient(int $productId, int $unitId): float
{
    $coef = DB::table('product_units')->where('product_id',$productId)->where('unit_id',$unitId)->value('unit_coefficient');
    return (float)($coef ?: 1);
}
```

### loadContract() / canBorrowSell() private
Port bước tiền-kiểm 2-3 ở Mục 2. `loadContract` trả object (stdClass) từ query builder với các cột cần; `canBorrowSell(int $id): bool` như bước 3.

---

## 8. Entity: THÊM searchByFilter() + meta() vào BorrowSellRequest.php (RULING #1)

Port ERP `BorrowSellRequest::searchByFilter` (Model/Warehouse/BorrowSellRequest.php:607-752). Thay `auth()->user()->can('X')` → `self::currentEmployeeHasPermission('X')`; `EmployeeManageDepartment::...pluck` → `self::currentManagedDepartmentIds()`; `auth()->user()->info->company_id` → `self::currentCompanyId()`; `Auth::user()->id` → `auth()->id()`. Trả về query builder (KHÔNG paginate — controller Task 8 gọi `->paginate()`).

Cấu trúc scope (port nguyên):
- `type=='all'`: super-cty (PERMISSION_VIEW_ALL_COMPANY) không lọc / công ty (PERMISSION_VIEW_COMPANY) `where company_id=self::currentCompanyId()` / phòng ban (PERMISSION_VIEW_DEPARTMENT) `whereIn department_id, self::currentManagedDepartmentIds()` / fallback `where created_by=auth()->id()`. Sau đó `where(status!=3 OR (status=3 AND created_by=self))`.
- `type=='accounting'` && `self::currentEmployeeHasPermission(PERMISSION_KE_TOAN_KHO)`: `where status!=0 && company_id=current && status!=3`.
- `type=='waiting_approve'`: `where(closure)`: nếu có PERMISSION_TP_APPROVE → `orWhere(status=CHO_TP_DUYET & whereIn department_id managed)`; nếu có PERMISSION_BGD_APPROVE → `orWhere(status=CHO_BGD_DUYET)`; luôn `orWhere(company_id=current & status=2)`.
- else: `where created_by=auth()->id()`.
- Filter phụ (áp sau, giống ERP 673-740): contract_id→contractable_id, contract_type→contractable_type, created_by, export_type→type, approver→approver_id, code (like), status, startDate/endDate (created_at), company→company_id, department→department_id, productName/productCode (subquery BorrowSellRequestProduct.parent_id). contract_code/customer: ERP dùng whereHasMorph — HRM Phase 1 có thể bỏ 2 filter này nếu morph relation chưa cấu hình (ghi vào report), hoặc port bằng subquery trên firm_contracts/wr_service_contracts.
- Order mặc định `created_at DESC` nếu không có `order`.
- Cuối: `where(created_by=auth()->id() OR status!=3)`.
- Eager load: `employee_create`, `approver` (relations entity Task 3), + contractable/customer nếu có relation (nếu chưa có, bỏ, ghi report).

`meta(): array` — cờ quyền cho FE (fail-closed, mặc định false):
```php
public static function meta(): array
{
    return [
        'canViewAllCompany' => self::currentEmployeeHasPermission(self::PERMISSION_VIEW_ALL_COMPANY),
        'canViewCompany'    => self::currentEmployeeHasPermission(self::PERMISSION_VIEW_COMPANY),
        'canViewDepartment' => self::currentEmployeeHasPermission(self::PERMISSION_VIEW_DEPARTMENT),
        'isKeToanKho'       => self::currentEmployeeHasPermission(self::PERMISSION_KE_TOAN_KHO),
        'isTP'              => self::currentEmployeeHasPermission(self::PERMISSION_TP_APPROVE),
        'isBGD'             => self::currentEmployeeHasPermission(self::PERMISSION_BGD_APPROVE),
    ];
}
```

---

## 9. Verify (chạy, DÁN output vào report)
1. `php -l` cả 2 file (Service + entity).
2. `composer dump-autoload -o` (class mới).
3. Tinker khói (giả lập auth) — CHỈ nếu tìm được dữ liệu hợp lệ; nếu không dựng được dữ liệu, tối thiểu chứng minh class load + method tồn tại:
   ```
   php artisan tinker --execute="
   \$s = app(\Modules\Finance\Services\BorrowSellRequest\BorrowSellRequestService::class);
   echo get_class(\$s).PHP_EOL;
   echo 'searchByFilter exists: '.(int)method_exists(\Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest::class,'searchByFilter').PHP_EOL;
   echo 'meta exists: '.(int)method_exists(\Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest::class,'meta').PHP_EOL;
   "
   ```
4. Nếu dựng được 1 HĐ Firm + 1 phiếu XUAT_MUON DA_MUON hợp lệ: `Auth::loginUsingId(<emp có quyền>)`, dựng `$request`, gọi `store($request)`, in `->code`,`->status`; kiểm `borrow_sell_requests`/`_products`/`_product_details`/pivot có bản ghi; **`account_details` count KHÔNG đổi** (Phase 1 chưa hạch toán). Nếu không dựng được, ghi rõ "chưa smoke-test store do thiếu dữ liệu" — KHÔNG bịa kết quả.

## KHÔNG làm
- KHÔNG commit/push/dispatch subagent. KHÔNG đọc vendor/. KHÔNG dùng mysql2/DB_CONNECTION_SECOND.
- KHÔNG hard-code cờ quyền = true. KHÔNG catch nuốt Exception (rethrow ValidationException).
- KHÔNG sửa file Task 1-5 TRỪ đổi visibility `firmExportingQty`/`firmBorrowingQty` private→public trong SourceService (nếu chọn cách đó — ghi report).
- KHÔNG tự bỏ check diff-price/over-limit âm thầm. Bế tắc thì ghi "cần chốt" vào report, KHÔNG che.

## Report
Ghi `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-6-report.md`: danh sách file tạo/sửa, output verify (php -l, tinker), lựa chọn visibility SourceService, cột HĐ đã dùng (firm_contracts/wr_service_contracts), cách xử lý diff-price (port đủ hay khung), các filter searchByFilter đã bỏ (nếu có) + lý do, bất kỳ "cần chốt" nào.
Trả về (NGẮN, KHÔNG dán code dài): STATUS (DONE/DONE_WITH_CONCERNS/BLOCKED/NEEDS_CONTEXT), 1 dòng verify, concerns.
