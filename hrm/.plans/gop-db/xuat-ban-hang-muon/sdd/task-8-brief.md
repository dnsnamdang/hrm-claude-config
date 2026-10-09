# Task 8 — Controller + 3 Resource + Routes (BorrowSellRequest)

**Repo:** `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api` (nhánh gop_db, Laravel 8, **PHP 7.4**). KHÔNG commit/push, KHÔNG dispatch subagent, KHÔNG đọc vendor/, KHÔNG dùng mysql2/DB_CONNECTION_SECOND. Tài liệu (nếu có) ghi vào `HRM/.plans/gop-db/`.

Tầng HTTP MỎNG cho luồng "Yêu cầu xuất bán hàng mượn" (mã `PYCXBHM`). Service (Task 6) + FormRequest (Task 7) + Entity (Task 3) ĐÃ XONG. Task này: (1) thêm 4 method phụ vào Service, (2) Controller, (3) 3 Resource, (4) routes. KHÔNG viết business logic mới ngoài 4 method Service dưới đây.

---

## ⚠️ 4 SỬA LỖI PLAN (đã reconcile — plan `2026-09-03-...-phase1.md`:1015-1169 có defect, KHÔNG copy verbatim)

Plan Task 8 viết cho PHP 8 + giả định Service có sẵn method không tồn tại. Dùng CODE TRONG BRIEF NÀY, không phải code plan.

- **DEFECT#1 — searchByFilter/meta nằm trên ENTITY, không phải Service.** Plan gọi `$this->service->searchByFilter()`/`->meta()`. T6 đặt 2 method này là `public static` TRÊN ENTITY `BorrowSellRequest` (vì trait `ChecksEmployeePermission` helper là `protected static`, chỉ gọi được từ trong entity). Controller PHẢI gọi `BorrowSellRequest::searchByFilter($request)` + `BorrowSellRequest::meta()`. **`searchByFilter` TRẢ VỀ query builder (CHƯA paginate)** → controller phải `->paginate(...)`.
- **DEFECT#2 — KHÔNG dùng constructor property promotion (PHP 8).** Plan viết `__construct(private BorrowSellRequestService $service, ...)` → **VỠ trên PHP 7.4**. Khai property tường minh + gán trong body (xem precedent ProductImportController dưới).
- **DEFECT#3 — 4 method Service chưa tồn tại, phải THÊM.** Service hiện chỉ có `store/getDebtCustomerByEmployee/deny/managerApprove/switchBoardOfManager/boardOfManagerApprove`. Thêm `findOrFail/findForShow/searchContracts/histories` (code đầy đủ dưới).
- **DEFECT#4 — Detail/Print đọc SNAPSHOT, contract_code = DB lookup nhẹ (KHÔNG morphTo).** Bảng `borrow_sell_requests` đã snapshot `customer_name/customer_address/customer_mobile/customer_contact_name/customer_contact_phone/contact_address/delivery_place` → Detail/Print đọc trực tiếp cột. `contract_code` KHÔNG có cột snapshot → tra `firm_contracts`/`wr_service_contracts` theo `contractable_id`. KHÔNG thêm relation `contractable()` morphTo vào entity (né rủi ро ERP-model connection/prefix — cùng lý do T6 loadContract dùng exists()-query thay vì relation).

---

## RULING (đã chốt, ĐỪNG flag lại):

- **R1 (visibility trait ở Resource):** List/Detail/Print Resource `use ChecksEmployeePermission` TRỰC TIẾP nếu cần cờ quyền — GIỐNG precedent `ProductImportListResource`. Nhưng cờ hành động (`is_can_*`) gọi thẳng `canX()` trên từng model item (canX là `public` trên entity), KHÔNG cần trait. Chỉ cần trait nếu muốn gate field nhạy cảm — Phase 1 phiếu này KHÔNG có giá vốn/lương nên KHÔNG cần gate field, KHÔNG cần `use ChecksEmployeePermission` ở Resource.
- **R2 (searchContracts đơn giản hoá — có chủ đích):** ERP KHÔNG có endpoint search contract cho màn này (`create()` chỉ `return view`). Endpoint `contracts` là MỚI cho FE Vue picker. Phase 1: search `firm_contracts` + `wr_service_contracts` theo keyword (code/customer_name LIKE) + scope `company_id` hiện tại, KHÔNG gate `canProductExport` nặng ở bước picker. Eligibility thật (quỹ/canBorrowSell) ĐÃ enforce downstream ở `contractBorrowSellData` (loadFirm/loadWrService trả SL mượn được) + `store()` (canBorrowSell + quỹ per product). **Cost nếu sai:** picker có thể hiện HĐ không còn SL mượn → user chọn xong bước sau rỗng → cấn UX nhẹ, KHÔNG phải lỗi data/bảo mật.
- **R3 (histories = []):** Phase 1 CHƯA có bảng lịch sử duyệt → `histories()` trả `[]`. Endpoint vẫn expose để FE Task 12 gọi không vỡ.
- **R4 (KHÔNG middleware checkPermission):** routes gate qua `canX()` trong controller (fail-closed thật) — GIỐNG `ProductImportController` (role gán từ ERP `model_type='App\Employee'` nên spatie middleware bỏ sót). ĐÃ ruling ở ledger, surface user ở Finish. KHÔNG thêm `->middleware('checkPermission:...')`.
- **R5 (index gate phạm vi):** `searchByFilter` (entity) đã tự gate phạm vi theo cấp tổ chức + chỉ chủ phiếu thấy DANG_TAO (T6 dòng 316-318). Controller index KHÔNG cần gate thêm.

---

## FACT đã trace (dùng verbatim, KHÔNG query lại):

- **ApiController:** `Modules\Finance\Http\Controllers\V1\ApiController` (cùng namespace controller) → chỉ `extends ApiController`, KHÔNG cần `use`. Có `protected function responseJson($message, $code = 200, $data = null)`.
- **Precedent constructor (ProductImportController, PHP 7.4 đúng):**
  ```php
  private $service;
  public function __construct(ProductImportService $service) { $this->service = $service; }
  ```
- **Precedent index (ProductImportController):**
  ```php
  $items = $this->service->searchByFilter($request);
  return (new ProductImportListResource($items))->additional([
      'total' => $items->total(), 'lastPage' => $items->lastPage(),
      'currentPage' => $items->currentPage(), 'perPage' => (int) $items->perPage(),
  ]);
  ```
- **Entity relations:** `products()` hasMany BorrowSellRequestProduct (parent_id), `tabs()` hasMany BorrowSellRequestTab (parent_id), `details()` hasMany BorrowSellRequestProductDetail (request_id). `BorrowSellRequestProduct::details()` hasMany (parent_id). Creator relation = **`employee_create()`** belongsTo Employee (created_by). Employee có `->info->fullname` (như ProductImport dùng `->info->fullname`).
- **Entity gates (public):** canView(), canEdit(), canApprove(), canManagerApprove(), canBoardOfManagerApprove(), canDeny().
- **Constants entity:** CONTRACT_FIRM='App\Model\Sale\Firm\Contract\FirmContract', CONTRACT_WR_SERVICE='App\Model\Customers\WrServiceContract'; DA_DUYET=1, CHO_KE_TOAN_KHO=2, DANG_TAO=3, KHONG_DUYET=4, CHO_TP_DUYET=10, CHO_BGD_DUYET=11.
- **Cột `borrow_sell_requests`:** id, status, type, code, contractable_id, contractable_type, firm_contract_tab_id, project_tab_id, created_by, updated_by, approver_id, approved_time, note, comment, created_at, updated_at, vat_percent, sum_amount_after_extra, sum_amount_after_extra_vat, sum_amount_after_extra_after_vat, customer_id, customer_type, customer_name, customer_address, customer_mobile, customer_contact_name, customer_contact_phone, contact_address, delivery_place, company_id, department_id, need_repair.
- **Cột `borrow_sell_request_products`:** id, parent_id, objectable_id, objectable_type, product_id, product_name, unit_id, unit_name, brand_id, brand_name, model_id, model_name, code, price, extra_price, contract_qty, qty, unit_coefficient, approved_qty, returned_qty, allocated_price, export_price, net_price, rebate_price, usage_status, vat_percent.
- **Cột `borrow_sell_request_product_details`:** id, parent_id, request_id, product_export_request_id, product_export_request_detail_id, product_id, unit_id, qty, approved_qty.
- **Cột `borrow_sell_request_tabs`:** id, parent_id, firm_contract_id, firm_contract_tab_id, name.
- **`firm_contracts` & `wr_service_contracts`:** đều có `code`, `customer_name`, `company_id`, `status`.
- **Status name map (dùng chung mọi Resource):** `[1=>'Đã duyệt',2=>'Chờ duyệt',3=>'Đang tạo',4=>'Không duyệt',10=>'Chờ TP duyệt',11=>'Chờ BGD duyệt']`.
- **Type name map:** `[1=>'HĐ hãng', 2=>'HĐ dịch vụ']` (type: 1=Firm, 2=WrService — khớp FormRequest `type in:1,2`).

---

## File 1: THÊM 4 method vào Service (KHÔNG sửa method cũ)

File: `Modules/Finance/Services/BorrowSellRequest/BorrowSellRequestService.php`. Thêm 4 public method (đặt sau các method duyệt, trước phần private helper). `use Illuminate\Support\Facades\DB;` ĐÃ có sẵn đầu file.

```php
    // =====================================================================
    // Tra cứu cho Controller (Task 8)
    // =====================================================================

    /** Lấy phiếu theo id, 404 nếu không có (dùng cho deny/approve/histories). */
    public function findOrFail(int $id): BorrowSellRequest
    {
        return BorrowSellRequest::findOrFail($id);
    }

    /** Lấy phiếu + eager load cho màn chi tiết/in. */
    public function findForShow(int $id): BorrowSellRequest
    {
        return BorrowSellRequest::with(['products.details', 'tabs'])->findOrFail($id);
    }

    /**
     * Lịch sử duyệt — Phase 1 CHƯA có bảng log riêng → trả []. (R3)
     * Endpoint vẫn expose để FE không vỡ; Phase 2 sẽ đọc bảng lịch sử thật.
     */
    public function histories(BorrowSellRequest $request): array
    {
        return [];
    }

    /**
     * Tìm HĐ hãng + HĐ dịch vụ cho popup chọn hợp đồng ở màn tạo (R2).
     * Keyword LIKE code/customer_name, scope company_id hiện tại. Eligibility quỹ thật
     * enforce downstream (contractBorrowSellData + store).
     */
    public function searchContracts(Request $request): array
    {
        $keyword = trim((string) $request->get('keyword', ''));
        $type = $request->get('type'); // 1=Firm, 2=WrService, rỗng=cả 2
        $companyId = optional(optional(auth()->user())->info)->company_id;
        $limit = 20;

        $result = [];

        if (!$type || (int) $type === 1) {
            $q = DB::table('firm_contracts')->select('id', 'code', 'customer_id', 'customer_name');
            if ($companyId) {
                $q->where('company_id', $companyId);
            }
            if ($keyword !== '') {
                $q->where(function ($w) use ($keyword) {
                    $w->where('code', 'like', '%' . $keyword . '%')
                      ->orWhere('customer_name', 'like', '%' . $keyword . '%');
                });
            }
            foreach ($q->orderBy('id', 'DESC')->limit($limit)->get() as $r) {
                $result[] = [
                    'id' => $r->id,
                    'code' => $r->code,
                    'customer_id' => $r->customer_id,
                    'customer_name' => $r->customer_name,
                    'contractable_type' => BorrowSellRequest::CONTRACT_FIRM,
                    'type' => 1,
                    'type_name' => 'HĐ hãng',
                ];
            }
        }

        if (!$type || (int) $type === 2) {
            $q = DB::table('wr_service_contracts')->select('id', 'code', 'customer_id', 'customer_name');
            if ($companyId) {
                $q->where('company_id', $companyId);
            }
            if ($keyword !== '') {
                $q->where(function ($w) use ($keyword) {
                    $w->where('code', 'like', '%' . $keyword . '%')
                      ->orWhere('customer_name', 'like', '%' . $keyword . '%');
                });
            }
            foreach ($q->orderBy('id', 'DESC')->limit($limit)->get() as $r) {
                $result[] = [
                    'id' => $r->id,
                    'code' => $r->code,
                    'customer_id' => $r->customer_id,
                    'customer_name' => $r->customer_name,
                    'contractable_type' => BorrowSellRequest::CONTRACT_WR_SERVICE,
                    'type' => 2,
                    'type_name' => 'HĐ dịch vụ',
                ];
            }
        }

        return $result;
    }
```

---

## File 2: Controller (PHP 7.4 — property tường minh)

File: `Modules/Finance/Http/Controllers/V1/BorrowSellRequestController.php`

```php
<?php

namespace Modules\Finance\Http\Controllers\V1;

use Illuminate\Http\Request;
use Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest;
use Modules\Finance\Services\BorrowSellRequest\BorrowSellRequestService;
use Modules\Finance\Services\BorrowSellRequest\BorrowSellRequestSourceService;
use Modules\Finance\Http\Requests\BorrowSellRequest\StoreBorrowSellRequestRequest;
use Modules\Finance\Http\Requests\BorrowSellRequest\DenyBorrowSellRequestRequest;
use Modules\Finance\Transformers\BorrowSellRequestResource\BorrowSellRequestListResource;
use Modules\Finance\Transformers\BorrowSellRequestResource\BorrowSellRequestDetailResource;
use Modules\Finance\Transformers\BorrowSellRequestResource\BorrowSellRequestPrintResource;

/**
 * Yêu cầu xuất bán hàng mượn (PYCXBHM) — tầng HTTP MỎNG.
 * Quyền: KHÔNG middleware checkPermission (role ERP model_type='App\Employee' → spatie bỏ sót);
 * gate qua canX() trên entity + searchByFilter tự gate phạm vi. searchByFilter/meta là static TRÊN
 * ENTITY (trait ChecksEmployeePermission helper protected-static).
 */
class BorrowSellRequestController extends ApiController
{
    private $service;
    private $source;

    public function __construct(BorrowSellRequestService $service, BorrowSellRequestSourceService $source)
    {
        $this->service = $service;
        $this->source = $source;
    }

    /** Danh sách — searchByFilter TRÊN ENTITY (trả builder) → paginate ở đây. meta() cờ quyền màn. */
    public function index(Request $request)
    {
        $items = BorrowSellRequest::searchByFilter($request)->paginate((int) $request->get('per_page', 20));

        return (new BorrowSellRequestListResource($items))->additional(array_merge([
            'total' => $items->total(),
            'lastPage' => $items->lastPage(),
            'currentPage' => $items->currentPage(),
            'perPage' => (int) $items->perPage(),
        ], BorrowSellRequest::meta()));
    }

    /** Popup chọn hợp đồng (Firm/WrService). */
    public function contracts(Request $request)
    {
        return $this->responseJson('OK', 200, $this->service->searchContracts($request));
    }

    /** Load SL mượn được theo hợp đồng đã chọn (Firm dùng tab_ids+vat, WrService không). */
    public function contractBorrowSellData(Request $request, $id)
    {
        $type = $request->get('contractable_type');
        $data = $type === BorrowSellRequest::CONTRACT_FIRM
            ? $this->source->loadFirm((int) $id, (array) $request->get('tab_ids', []), $request->get('vat_percent'))
            : $this->source->loadWrService((int) $id);

        return $this->responseJson('OK', 200, $data);
    }

    public function store(StoreBorrowSellRequestRequest $request)
    {
        $m = $this->service->store($request);

        return $this->responseJson('Yêu cầu của bạn đã được gửi', 200, [
            'id' => $m->id, 'code' => $m->code, 'status' => $m->status,
        ]);
    }

    public function show($id)
    {
        $m = $this->service->findForShow((int) $id);
        if (!$m->canView()) {
            return $this->responseJson('Không đủ quyền!', 403);
        }

        return new BorrowSellRequestDetailResource($m);
    }

    public function printData($id)
    {
        $m = $this->service->findForShow((int) $id);
        if (!$m->canView()) {
            return $this->responseJson('Không đủ quyền!', 403);
        }

        return new BorrowSellRequestPrintResource($m);
    }

    public function deny(DenyBorrowSellRequestRequest $request, $id)
    {
        $m = $this->service->findOrFail((int) $id);
        if (!$m->canDeny()) {
            return $this->responseJson('Không đủ quyền!', 403);
        }
        $this->service->deny($m, $request->input('comment'));

        return $this->responseJson('Thao tác thành công!', 200);
    }

    public function managerApprove($id)
    {
        $m = $this->service->findOrFail((int) $id);
        if (!$m->canManagerApprove()) {
            return $this->responseJson('Không đủ quyền!', 403);
        }
        $this->service->managerApprove($m);

        return $this->responseJson('Phiếu đã được duyệt thành công', 200);
    }

    public function switchBoardOfManager($id)
    {
        $m = $this->service->findOrFail((int) $id);
        if (!$m->canManagerApprove()) {
            return $this->responseJson('Không đủ quyền!', 403);
        }
        $this->service->switchBoardOfManager($m);

        return $this->responseJson('Chuyển BGD duyệt thành công!', 200);
    }

    public function boardOfManagerApprove($id)
    {
        $m = $this->service->findOrFail((int) $id);
        if (!$m->canBoardOfManagerApprove()) {
            return $this->responseJson('Không đủ quyền!', 403);
        }
        $this->service->boardOfManagerApprove($m);

        return $this->responseJson('Phiếu đã được duyệt thành công', 200);
    }

    public function histories($id)
    {
        $m = $this->service->findOrFail((int) $id);
        if (!$m->canView()) {
            return $this->responseJson('Không đủ quyền!', 403);
        }

        return $this->responseJson('OK', 200, $this->service->histories($m));
    }
}
```

---

## File 3: BorrowSellRequestListResource

File: `Modules/Finance/Transformers/BorrowSellRequestResource/BorrowSellRequestListResource.php`

- `extends ResourceCollection`. `contract_code` tra batch theo type (né N+1) từ `firm_contracts`/`wr_service_contracts`. `creator_name` = `optional(optional($item->employee_create)->info)->fullname`. 6 cờ hành động gọi canX().

```php
<?php

namespace Modules\Finance\Transformers\BorrowSellRequestResource;

use Carbon\Carbon;
use Illuminate\Http\Resources\Json\ResourceCollection;
use Illuminate\Support\Facades\DB;
use Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest;

class BorrowSellRequestListResource extends ResourceCollection
{
    private static $statusNames = [
        1 => 'Đã duyệt', 2 => 'Chờ duyệt', 3 => 'Đang tạo',
        4 => 'Không duyệt', 10 => 'Chờ TP duyệt', 11 => 'Chờ BGD duyệt',
    ];
    private static $typeNames = [1 => 'HĐ hãng', 2 => 'HĐ dịch vụ'];

    public function toArray($request): array
    {
        // Batch tra mã hợp đồng theo type (tránh N+1)
        $firmIds = [];
        $wrIds = [];
        foreach ($this->collection as $it) {
            if ($it->contractable_type === BorrowSellRequest::CONTRACT_FIRM) {
                $firmIds[] = $it->contractable_id;
            } elseif ($it->contractable_type === BorrowSellRequest::CONTRACT_WR_SERVICE) {
                $wrIds[] = $it->contractable_id;
            }
        }
        $firmCodes = $firmIds ? DB::table('firm_contracts')->whereIn('id', array_unique($firmIds))->pluck('code', 'id') : collect();
        $wrCodes = $wrIds ? DB::table('wr_service_contracts')->whereIn('id', array_unique($wrIds))->pluck('code', 'id') : collect();

        $result = [];
        foreach ($this->collection as $item) {
            $contractCode = $item->contractable_type === BorrowSellRequest::CONTRACT_FIRM
                ? ($firmCodes[$item->contractable_id] ?? null)
                : ($wrCodes[$item->contractable_id] ?? null);

            $result[] = [
                'id' => $item->id,
                'code' => $item->code,
                'type' => $item->type,
                'type_name' => self::$typeNames[$item->type] ?? null,
                'contract_code' => $contractCode,
                'customer_name' => $item->customer_name,
                'creator_name' => optional(optional($item->employee_create)->info)->fullname,
                'status' => $item->status,
                'status_name' => self::$statusNames[$item->status] ?? null,
                'created_at' => self::formatDateTime($item->created_at),

                // Cờ hành động — FE disable nút chứ không ẩn (quy ước dự án). Gọi thẳng canX() (public).
                'is_can_view' => $item->canView(),
                'is_can_edit' => $item->canEdit(),
                'is_can_approve' => $item->canApprove(),
                'is_can_deny' => $item->canDeny(),
                'is_can_manager_approve' => $item->canManagerApprove(),
                'is_can_board_approve' => $item->canBoardOfManagerApprove(),
            ];
        }

        return $result;
    }

    private static function formatDateTime($value): ?string
    {
        if (empty($value)) {
            return null;
        }

        return $value instanceof Carbon
            ? $value->format('d/m/Y H:i')
            : Carbon::parse($value)->format('d/m/Y H:i');
    }
}
```

---

## File 4: BorrowSellRequestDetailResource

File: `Modules/Finance/Transformers/BorrowSellRequestResource/BorrowSellRequestDetailResource.php`

- `extends JsonResource`. Full đầu phiếu (snapshot customer đọc thẳng cột) + products (+details) + tabs. `contract_code` = 1 DB lookup. Cờ hành động cho màn chi tiết.

```php
<?php

namespace Modules\Finance\Transformers\BorrowSellRequestResource;

use Carbon\Carbon;
use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\Facades\DB;
use Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest;

class BorrowSellRequestDetailResource extends JsonResource
{
    private static $statusNames = [
        1 => 'Đã duyệt', 2 => 'Chờ duyệt', 3 => 'Đang tạo',
        4 => 'Không duyệt', 10 => 'Chờ TP duyệt', 11 => 'Chờ BGD duyệt',
    ];
    private static $typeNames = [1 => 'HĐ hãng', 2 => 'HĐ dịch vụ'];

    public function toArray($request): array
    {
        $table = $this->contractable_type === BorrowSellRequest::CONTRACT_FIRM ? 'firm_contracts' : 'wr_service_contracts';
        $contractCode = $this->contractable_id
            ? optional(DB::table($table)->where('id', $this->contractable_id)->first(['code']))->code
            : null;

        return [
            'id' => $this->id,
            'code' => $this->code,
            'type' => $this->type,
            'type_name' => self::$typeNames[$this->type] ?? null,
            'status' => $this->status,
            'status_name' => self::$statusNames[$this->status] ?? null,
            'note' => $this->note,
            'comment' => $this->comment,

            'contractable_id' => $this->contractable_id,
            'contractable_type' => $this->contractable_type,
            'contract_code' => $contractCode,
            'firm_contract_tab_id' => $this->firm_contract_tab_id,
            'vat_percent' => $this->vat_percent,

            // Snapshot khách hàng (đọc thẳng cột borrow_sell_requests)
            'customer_id' => $this->customer_id,
            'customer_name' => $this->customer_name,
            'customer_address' => $this->customer_address,
            'customer_mobile' => $this->customer_mobile,
            'customer_contact_name' => $this->customer_contact_name,
            'customer_contact_phone' => $this->customer_contact_phone,
            'contact_address' => $this->contact_address,
            'delivery_place' => $this->delivery_place,

            'created_by' => $this->created_by,
            'creator_name' => optional(optional($this->employee_create)->info)->fullname,
            'created_at' => self::formatDateTime($this->created_at),
            'approved_time' => self::formatDateTime($this->approved_time),

            'products' => $this->products->map(function ($p) {
                return [
                    'id' => $p->id,
                    'product_id' => $p->product_id,
                    'code' => $p->code,
                    'product_name' => $p->product_name,
                    'unit_id' => $p->unit_id,
                    'unit_name' => $p->unit_name,
                    'brand_name' => $p->brand_name,
                    'model_name' => $p->model_name,
                    'contract_qty' => $p->contract_qty,
                    'qty' => $p->qty,
                    'approved_qty' => $p->approved_qty,
                    'unit_coefficient' => $p->unit_coefficient,
                    'vat_percent' => $p->vat_percent,
                    'details' => $p->details->map(function ($d) {
                        return [
                            'id' => $d->id,
                            'product_export_request_id' => $d->product_export_request_id,
                            'product_export_request_detail_id' => $d->product_export_request_detail_id,
                            'product_id' => $d->product_id,
                            'unit_id' => $d->unit_id,
                            'qty' => $d->qty,
                            'approved_qty' => $d->approved_qty,
                        ];
                    })->values(),
                ];
            })->values(),

            'tabs' => $this->tabs->map(function ($t) {
                return [
                    'id' => $t->id,
                    'firm_contract_id' => $t->firm_contract_id,
                    'firm_contract_tab_id' => $t->firm_contract_tab_id,
                    'name' => $t->name,
                ];
            })->values(),

            'is_can_view' => $this->canView(),
            'is_can_edit' => $this->canEdit(),
            'is_can_approve' => $this->canApprove(),
            'is_can_deny' => $this->canDeny(),
            'is_can_manager_approve' => $this->canManagerApprove(),
            'is_can_board_approve' => $this->canBoardOfManagerApprove(),
        ];
    }

    private static function formatDateTime($value): ?string
    {
        if (empty($value)) {
            return null;
        }

        return $value instanceof Carbon
            ? $value->format('d/m/Y H:i')
            : Carbon::parse($value)->format('d/m/Y H:i');
    }
}
```

---

## File 5: BorrowSellRequestPrintResource

File: `Modules/Finance/Transformers/BorrowSellRequestResource/BorrowSellRequestPrintResource.php`

- `extends JsonResource`. Dữ liệu mẫu in PYCXBHM: đầu phiếu + snapshot khách + dòng SP phẳng. Tối giản, phục vụ FE render mẫu in.

```php
<?php

namespace Modules\Finance\Transformers\BorrowSellRequestResource;

use Carbon\Carbon;
use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\Facades\DB;
use Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest;

class BorrowSellRequestPrintResource extends JsonResource
{
    private static $typeNames = [1 => 'HĐ hãng', 2 => 'HĐ dịch vụ'];

    public function toArray($request): array
    {
        $table = $this->contractable_type === BorrowSellRequest::CONTRACT_FIRM ? 'firm_contracts' : 'wr_service_contracts';
        $contractCode = $this->contractable_id
            ? optional(DB::table($table)->where('id', $this->contractable_id)->first(['code']))->code
            : null;

        return [
            'code' => $this->code,
            'type_name' => self::$typeNames[$this->type] ?? null,
            'contract_code' => $contractCode,
            'note' => $this->note,
            'created_at' => self::formatDateTime($this->created_at),
            'creator_name' => optional(optional($this->employee_create)->info)->fullname,

            'customer_name' => $this->customer_name,
            'customer_address' => $this->customer_address,
            'customer_mobile' => $this->customer_mobile,
            'customer_contact_name' => $this->customer_contact_name,
            'customer_contact_phone' => $this->customer_contact_phone,
            'contact_address' => $this->contact_address,
            'delivery_place' => $this->delivery_place,

            'products' => $this->products->map(function ($p, $i) {
                return [
                    'stt' => $i + 1,
                    'code' => $p->code,
                    'product_name' => $p->product_name,
                    'model_name' => $p->model_name,
                    'unit_name' => $p->unit_name,
                    'qty' => $p->qty,
                ];
            })->values(),
        ];
    }

    private static function formatDateTime($value): ?string
    {
        if (empty($value)) {
            return null;
        }

        return $value instanceof Carbon
            ? $value->format('d/m/Y H:i')
            : Carbon::parse($value)->format('d/m/Y H:i');
    }
}
```

---

## File 6: Routes (static TRƯỚC /{id})

File: `Modules/Finance/Routes/api.php`. Thêm `use Modules\Finance\Http\Controllers\V1\BorrowSellRequestController;` đầu file (khớp cách khai controller khác trong file — KIỂM TRA cú pháp `use` các controller hiện có, có thể file dùng string action thay vì `[Class::class,'m']`; **theo đúng style file hiện tại**). Đặt group vào ĐÚNG nhóm prefix cha hiện có (đọc file để biết prefix `/api/finance` hay khác — KHÔNG đoán).

```php
Route::group(['prefix' => '/borrow-sell-requests'], function () {
    Route::get('/', [BorrowSellRequestController::class, 'index']);
    Route::get('/contracts', [BorrowSellRequestController::class, 'contracts']);
    Route::get('/contracts/{id}/borrow-sell-data', [BorrowSellRequestController::class, 'contractBorrowSellData']);
    Route::post('/', [BorrowSellRequestController::class, 'store']);
    Route::post('/{id}/deny', [BorrowSellRequestController::class, 'deny']);
    Route::post('/{id}/manager-approve', [BorrowSellRequestController::class, 'managerApprove']);
    Route::post('/{id}/switch-board-of-manager', [BorrowSellRequestController::class, 'switchBoardOfManager']);
    Route::post('/{id}/board-of-manager-approve', [BorrowSellRequestController::class, 'boardOfManagerApprove']);
    Route::get('/{id}/histories', [BorrowSellRequestController::class, 'histories']);
    Route::get('/{id}/print-data', [BorrowSellRequestController::class, 'printData']);
    Route::get('/{id}', [BorrowSellRequestController::class, 'show']); // CUỐI CÙNG
});
```

**QUAN TRỌNG:** Nếu file `api.php` hiện dùng string-style action (`'BorrowSellRequestController@index'`) cho các controller khác thì DÙNG string-style cho khớp; nếu dùng `[Class::class,'method']` thì giữ như trên. Đọc 20 dòng đầu + 1 group mẫu trong file trước khi thêm.

---

## Verify (chạy, DÁN output vào report)

1. `php -l` cả 6 file (Controller + 3 Resource + Service sau khi thêm method; api.php).
2. `composer dump-autoload -o`.
3. Tinker: `class_exists('\Modules\Finance\Http\Controllers\V1\BorrowSellRequestController')` + 3 Resource → `true`; `method_exists('\Modules\Finance\Services\BorrowSellRequest\BorrowSellRequestService', 'searchContracts')` + findOrFail/findForShow/histories → `true`.
4. `php artisan route:list --path=borrow-sell-requests` → đủ 11 route, `GET /{id}` (show) nằm DƯỚI các route tĩnh (contracts, contracts/{id}/borrow-sell-data, {id}/histories, {id}/print-data).
5. **Smoke test THẬT (KHÔNG tạo data rác — chỉ đọc):**
   - Tinker: `$req = new \Illuminate\Http\Request(); (new \Modules\Finance\Services\BorrowSellRequest\BorrowSellRequestService(app(\Modules\Finance\Services\BorrowSellRequest\BorrowSellRequestSourceService::class)))->searchContracts($req);` → trả mảng (có thể rỗng nếu chưa auth company — không lỗi).
   - Nếu có phiếu sẵn trong DB: `$m = \Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest::with(['products.details','tabs'])->first(); if($m){ (new \Modules\Finance\Transformers\BorrowSellRequestResource\BorrowSellRequestDetailResource($m))->toArray(request()); echo "detail OK\n"; }` → KHÔNG throw.
   - `BorrowSellRequest::searchByFilter(new \Illuminate\Http\Request())->paginate(5)` → trả paginator (total ≥ 0), KHÔNG lỗi.

## Report
Ghi `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.plans/gop-db/xuat-ban-hang-muon/sdd/task-8-report.md`: 6 file tạo/sửa, output từng bước verify (php -l, route:list, smoke). Ghi RÕ bất kỳ điểm lệch brief nào (vd style route khác, cột thiếu) + cách resolve. TRẢ VỀ ngắn: STATUS (DONE/BLOCKED/DONE_WITH_CONCERNS), commit (KHÔNG commit), 1 dòng verify tổng, concerns nếu có.
