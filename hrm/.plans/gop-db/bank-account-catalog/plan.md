# Plan — Danh mục tài khoản ngân hàng (ERP → HRM)

> **For agentic workers:** REQUIRED SUB-SKILL: dùng superpowers:subagent-driven-development (khuyến nghị) hoặc superpowers:executing-plans để thực thi từng task. Step dùng checkbox (`- [ ]`) để theo dõi.

- Người phụ trách: @khoipv
- Nhánh: `gop_db` (cả 2 repo — KHÔNG tạo branch riêng, user đã chốt làm thẳng trên `gop_db`)
- Spec: `docs/superpowers/specs/gop-db/2026-08-03-bank-account-catalog-design.md` (ĐÃ DUYỆT 2026-08-04)

**Goal:** Port màn ERP "Danh mục tài khoản ngân hàng" (`admin/accounting/account-banks`, bảng `company_accounts`) sang HRM tại `Modules/Finance` + `pages/finance/account-banks`, tối giản như ERP (danh sách + lọc + Thêm/Sửa + khóa qua Trạng thái, KHÔNG xóa/export/lịch sử).

**Architecture:** BE theo chuẩn base Finance/Assign có sẵn (ApiController + Service + FormRequest + ListResource meta `total/lastPage/currentPage/perPage`) — mẫu là bộ `SourceCapital*`/`CostDebt*` trong `Modules/Finance`. FE V2Base — mẫu là `pages/finance/cost-debts/index.vue` + `CostDebtModal.vue`. Scope cứng theo `company_id` user login, 1 quyền duy nhất `Quản lý danh mục tài khoản ngân hàng`.

**Tech Stack:** PHP 7.4 / Laravel 8 / MySQL (DB gộp `gop_db`, connection default) · Nuxt 2 / Vue 2 / Bootstrap-Vue.

## Global Constraints

- Nhánh git phải là `gop_db` ở CẢ `hrm-api` và `hrm-client` — kiểm tra `git branch --show-current` trước khi sửa file; sai nhánh thì DỪNG, báo lại.
- KHÔNG đổi schema bảng `company_accounts` (59 file ERP tham chiếu). KHÔNG migration.
- KHÔNG dùng `mysql2` / model `TpXxx` / `ErpPermissionHelper` — bảng nằm ngay trên connection default.
- KHÔNG kế thừa `App\Models\BaseModel` cho entity (hook của nó ghi `created_by/updated_by` — bảng không có 2 cột này).
- KHÔNG git commit/push.
- ValidationException KHÔNG được catch — để bay lên cho FE nhận 422 chuẩn Laravel.
- Mọi text hiển thị tiếng Việt; message validate required = "Bắt buộc phải nhập".
- FE: trước khi code phải đọc skill `.claude/skills/list-page/SKILL.md`, `.claude/skills/modal-popup/SKILL.md`, `.claude/skills/button-convention/SKILL.md`. Icon phải đối chiếu font local: `grep "^\.ri-xxx:before" hrm-client/assets/scss/custom/plugins/icons/_remixicon.scss`.
- DB local: KHÔNG chạy `PermissionsTableSeeder` (`run()` truncate `hrm_permissions`); KHÔNG xóa file bằng wildcard.
- Dữ liệu test tạo ra phải dọn sạch (bảng `company_accounts` phải về đúng 40 dòng gốc — đếm trước khi test để xác nhận baseline).

---

### Task 1: Entity `CompanyAccount`

**Files:**
- Create: `hrm-api/Modules/Finance/Entities/CompanyAccount/CompanyAccount.php`

**Interfaces:**
- Produces: class `Modules\Finance\Entities\CompanyAccount\CompanyAccount` — hằng `STATUS_ACTIVE = 1`, `STATUS_LOCKED = 0`; `$fillable` 9 cột; hook saving tự uppercase `account_name`/`bank_name`. Task 3/4/5 dùng class này.

- [x] **Step 1: Kiểm tra branch cả 2 repo**

Chạy: `git -C D:/laragon/www/hrm/hrm-api branch --show-current` và `git -C D:/laragon/www/hrm/hrm-client branch --show-current`
Kỳ vọng: cả 2 in ra `gop_db`. Nếu khác → DỪNG, báo user.

- [x] **Step 2: Viết entity**

```php
<?php

namespace Modules\Finance\Entities\CompanyAccount;

use Illuminate\Database\Eloquent\Model;
use Modules\Finance\Entities\Currency\Currency;
use Modules\Human\Entities\Bank;
use Modules\Human\Entities\BankBranch;

/**
 * Tài khoản ngân hàng của công ty — bảng ERP `company_accounts` trên DB gộp (59 file ERP
 * tham chiếu, cấm đổi schema). Bảng KHÔNG có created_by/updated_by nên KHÔNG kế thừa
 * App\Models\BaseModel (hook của nó ghi 2 cột đó bằng HRM user id).
 */
class CompanyAccount extends Model
{
    const STATUS_ACTIVE = 1;
    const STATUS_LOCKED = 0;

    protected $table = 'company_accounts';

    protected $fillable = [
        'bank_id', 'bank_branch_id', 'account_name', 'account_number',
        'company_id', 'bank_name', 'bank_branch', 'status', 'currency_id',
    ];

    protected static function booted()
    {
        // Mirror hook saving của ERP CompanyAccount — 2 màn chạy song song ghi dữ liệu đồng nhất.
        static::saving(function (CompanyAccount $model) {
            $model->account_name = mb_strtoupper((string) $model->account_name, 'UTF-8');
            $model->bank_name = mb_strtoupper((string) $model->bank_name, 'UTF-8');
        });
    }

    public function bank()
    {
        return $this->belongsTo(Bank::class, 'bank_id');
    }

    public function bankBranch()
    {
        return $this->belongsTo(BankBranch::class, 'bank_branch_id');
    }

    public function currency()
    {
        return $this->belongsTo(Currency::class, 'currency_id');
    }
}
```

- [x] **Step 3: Verify**

Chạy: `php -l hrm-api/Modules/Finance/Entities/CompanyAccount/CompanyAccount.php`
Kỳ vọng: `No syntax errors`.

Chạy (trong thư mục `hrm-api`):
`php artisan tinker --execute="echo Modules\Finance\Entities\CompanyAccount\CompanyAccount::count();"`
Kỳ vọng: in ra `40` (số dòng gốc — ghi lại số này làm baseline dọn dẹp).

---

### Task 2: FormRequest `CompanyAccountRequest`

**Files:**
- Create: `hrm-api/Modules/Finance/Http/Requests/CompanyAccount/CompanyAccountRequest.php`

**Interfaces:**
- Produces: class `Modules\Finance\Http\Requests\CompanyAccount\CompanyAccountRequest` — dùng chung store/update, phân biệt qua route param `id`. Task 5 type-hint class này.

- [x] **Step 1: Viết request**

```php
<?php

namespace Modules\Finance\Http\Requests\CompanyAccount;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class CompanyAccountRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        $id = $this->route('id'); // null khi tạo mới, id khi cập nhật

        return [
            'account_number' => [
                'required',
                // Bảng không có unique index DB — race 2 màn ERP/HRM chấp nhận (hiện trạng ERP).
                Rule::unique('company_accounts', 'account_number')->ignore($id),
            ],
            'account_name' => 'required',
            'bank_id' => 'required|exists:banks,id',
            'bank_branch_id' => [
                'required',
                // ERP chỉ lọc chi nhánh theo ngân hàng ở FE — HRM check luôn ở BE (sửa chủ động).
                Rule::exists('bank_branches', 'id')->where('bank_id', (int) $this->input('bank_id')),
            ],
            // ERP update THIẾU required currency_id — HRM áp cả create lẫn update (sửa chủ động).
            'currency_id' => 'required|exists:currencies,id',
            'status' => 'required|in:0,1',
        ];
    }

    public function messages(): array
    {
        return [
            'account_number.required' => 'Bắt buộc phải nhập',
            // ERP ghi nhầm "Tên tài khoản đã tồn tại" — HRM sửa lại cho đúng.
            'account_number.unique' => 'Số tài khoản đã tồn tại',
            'account_name.required' => 'Bắt buộc phải nhập',
            'bank_id.required' => 'Bắt buộc phải nhập',
            'bank_id.exists' => 'Ngân hàng không tồn tại',
            'bank_branch_id.required' => 'Bắt buộc phải nhập',
            'bank_branch_id.exists' => 'Chi nhánh không thuộc ngân hàng đã chọn',
            'currency_id.required' => 'Bắt buộc phải nhập',
            'currency_id.exists' => 'Loại tiền tệ không tồn tại',
            'status.required' => 'Bắt buộc phải nhập',
            'status.in' => 'Trạng thái không hợp lệ',
        ];
    }
}
```

- [x] **Step 2: Verify**

Chạy: `php -l hrm-api/Modules/Finance/Http/Requests/CompanyAccount/CompanyAccountRequest.php`
Kỳ vọng: `No syntax errors`.

---

### Task 3: Service `CompanyAccountService`

**Files:**
- Create: `hrm-api/Modules/Finance/Services/CompanyAccountService.php`

**Interfaces:**
- Consumes: `CompanyAccount` (Task 1).
- Produces (Task 5 gọi đúng các chữ ký này):
  - `currentCompanyId(): ?int`
  - `searchByFilter(\Illuminate\Http\Request $request)` → LengthAwarePaginator
  - `options(): array` — `['banks' => [...], 'bank_branches' => [...]]`
  - `findForCompany(int $id): ?CompanyAccount`
  - `createOrUpdate(array $attrs, ?CompanyAccount $obj = null): CompanyAccount`

- [x] **Step 1: Viết service**

```php
<?php

namespace Modules\Finance\Services;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Modules\Finance\Entities\CompanyAccount\CompanyAccount;

class CompanyAccountService
{
    /**
     * Công ty của user đang login — scope cứng của toàn màn (mirror ERP).
     * KHÔNG dùng ErpPermissionHelper: helper đọc qua mysql2 → DB ERP cũ, trả sai id trên DB gộp.
     */
    public function currentCompanyId(): ?int
    {
        $companyId = auth()->user()->info->company_id ?? null;

        return $companyId ? (int) $companyId : null;
    }

    public function searchByFilter(Request $request)
    {
        $limit = (int) $request->get('per_page', 10);

        $query = CompanyAccount::query()
            ->leftJoin('currencies', 'currencies.id', '=', 'company_accounts.currency_id')
            ->select('company_accounts.*', 'currencies.code as currency_code')
            // company_id null (user không gắn employee_info) → danh sách rỗng, không lộ công ty khác.
            ->where('company_accounts.company_id', $this->currentCompanyId());

        if ($request->filled('keyword')) {
            $keyword = $request->get('keyword');
            $query->where(function ($q) use ($keyword) {
                $q->where('company_accounts.account_number', 'like', "%{$keyword}%")
                    ->orWhere('company_accounts.account_name', 'like', "%{$keyword}%")
                    ->orWhere('company_accounts.bank_name', 'like', "%{$keyword}%");
            });
        }
        // ERP so khớp account_number CHÍNH XÁC — HRM đổi thành like cho nhất quán 4 ô text (sửa chủ động).
        foreach (['account_number', 'account_name', 'bank_name', 'bank_branch'] as $field) {
            if ($request->filled($field)) {
                $query->where('company_accounts.' . $field, 'like', '%' . $request->get($field) . '%');
            }
        }
        // filled() nhận cả chuỗi '0' → lọc Khóa hoạt động đúng.
        if ($request->filled('status')) {
            $query->where('company_accounts.status', (int) $request->get('status'));
        }

        return $query->orderBy('company_accounts.created_at', 'desc')->paginate($limit);
    }

    /**
     * Data dropdown cho form: load 1 lần, FE tự lọc chi nhánh theo ngân hàng (như ERP).
     * Không lọc theo status khóa của ngân hàng — mirror ERP.
     */
    public function options(): array
    {
        return [
            'banks' => DB::table('banks')->select('id', 'name')->orderBy('name')->get(),
            'bank_branches' => DB::table('bank_branches')->select('id', 'name', 'bank_id')->orderBy('name')->get(),
        ];
    }

    public function findForCompany(int $id): ?CompanyAccount
    {
        return CompanyAccount::query()
            ->where('id', $id)
            ->where('company_id', $this->currentCompanyId())
            ->first();
    }

    public function createOrUpdate(array $attrs, ?CompanyAccount $obj = null): CompanyAccount
    {
        return DB::transaction(function () use ($attrs, $obj) {
            $data = [
                'account_number' => trim((string) $attrs['account_number']),
                'account_name' => trim((string) $attrs['account_name']),
                'bank_id' => (int) $attrs['bank_id'],
                'bank_branch_id' => (int) $attrs['bank_branch_id'],
                'currency_id' => (int) $attrs['currency_id'],
                'status' => (int) $attrs['status'],
                // Denormalized như ERP: fill tên từ id; mở Sửa + lưu lại sẽ refresh tên mới.
                'bank_name' => (string) DB::table('banks')->where('id', $attrs['bank_id'])->value('name'),
                'bank_branch' => (string) DB::table('bank_branches')->where('id', $attrs['bank_branch_id'])->value('name'),
                // Gán cả create lẫn update — như ERP.
                'company_id' => $this->currentCompanyId(),
            ];

            if ($obj) {
                $obj->update($data);

                return $obj->refresh();
            }

            return CompanyAccount::create($data);
        });
    }
}
```

- [x] **Step 2: Verify syntax**

Chạy: `php -l hrm-api/Modules/Finance/Services/CompanyAccountService.php`
Kỳ vọng: `No syntax errors`.

- [x] **Step 3: Smoke tinker có rollback (DB nguyên trạng)**

Chạy trong `hrm-api` (1 lệnh tinker duy nhất, transaction + throw để rollback):

```php
php artisan tinker --execute="
DB::beginTransaction();
try {
    \$svc = app(Modules\Finance\Services\CompanyAccountService::class);
    \$bank = DB::table('banks')->first();
    \$branch = DB::table('bank_branches')->where('bank_id', \$bank->id)->first();
    \$currency = DB::table('currencies')->first();
    // Không có auth trong tinker → currentCompanyId() null; test createOrUpdate qua attrs trực tiếp
    \$obj = Modules\Finance\Entities\CompanyAccount\CompanyAccount::create([
        'account_number' => 'TEST-SMOKE-001', 'account_name' => 'nguyễn văn test',
        'bank_id' => \$bank->id, 'bank_branch_id' => \$branch->id,
        'bank_name' => \$bank->name, 'bank_branch' => \$branch->name,
        'currency_id' => \$currency->id, 'status' => 1, 'company_id' => 1,
    ]);
    echo 'uppercase: ' . \$obj->account_name . PHP_EOL; // kỳ vọng NGUYỄN VĂN TEST
    echo 'count-in-tx: ' . Modules\Finance\Entities\CompanyAccount\CompanyAccount::count() . PHP_EOL;
} finally {
    DB::rollBack();
}
echo 'count-after: ' . Modules\Finance\Entities\CompanyAccount\CompanyAccount::count() . PHP_EOL;
"
```

Kỳ vọng: `uppercase: NGUYỄN VĂN TEST` (hook saving chạy), `count-in-tx: 41`, `count-after: 40`.

---

### Task 4: Resources (List + Detail)

**Files:**
- Create: `hrm-api/Modules/Finance/Transformers/CompanyAccountResource/CompanyAccountListResource.php`
- Create: `hrm-api/Modules/Finance/Transformers/CompanyAccountResource/CompanyAccountDetailResource.php`

**Interfaces:**
- Consumes: paginator từ `CompanyAccountService::searchByFilter` (mỗi item có thêm cột join `currency_code`).
- Produces: 2 class Task 5 dùng. List item: `{id, account_number, account_name, bank_name, bank_branch, currency_text, status: '1'|'0', status_text}`. Detail: `{id, account_number, account_name, bank_id, bank_branch_id, currency_id, status: '1'|'0'}`.

- [x] **Step 1: Viết ListResource**

```php
<?php

namespace Modules\Finance\Transformers\CompanyAccountResource;

use Illuminate\Http\Resources\Json\ResourceCollection;
use Modules\Finance\Entities\CompanyAccount\CompanyAccount;

class CompanyAccountListResource extends ResourceCollection
{
    public function toArray($request): array
    {
        $result = [];
        foreach ($this->collection as $item) {
            $result[] = [
                'id' => $item->id,
                'account_number' => $item->account_number,
                'account_name' => $item->account_name,
                'bank_name' => $item->bank_name,
                'bank_branch' => $item->bank_branch,
                // Bản ghi cũ currency_id null (schema nullable) → hiện gạch ngang.
                'currency_text' => $item->currency_code ?: '—',
                'status' => (string) $item->status,
                'status_text' => (int) $item->status === CompanyAccount::STATUS_ACTIVE ? 'Hoạt động' : 'Khóa',
            ];
        }

        return $result;
    }
}
```

- [x] **Step 2: Viết DetailResource**

```php
<?php

namespace Modules\Finance\Transformers\CompanyAccountResource;

use Illuminate\Http\Resources\Json\JsonResource;

class CompanyAccountDetailResource extends JsonResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'account_number' => $this->account_number,
            'account_name' => $this->account_name,
            'bank_id' => $this->bank_id,
            'bank_branch_id' => $this->bank_branch_id,
            'currency_id' => $this->currency_id,
            'status' => (string) $this->status,
        ];
    }
}
```

- [x] **Step 3: Verify**

Chạy: `php -l` cả 2 file.
Kỳ vọng: `No syntax errors`.

---

### Task 5: Controller + Routes

**Files:**
- Create: `hrm-api/Modules/Finance/Http/Controllers/V1/CompanyAccountController.php`
- Modify: `hrm-api/Modules/Finance/Routes/api.php` (thêm group `/account-banks` vào cuối group `/v1/finance`, sau group `source-capitals`; thêm `use` ở đầu file)

**Interfaces:**
- Consumes: `CompanyAccountService` (Task 3), `CompanyAccountRequest` (Task 2), 2 resource (Task 4), `ApiController::responseJson($message, $code, $data)` có sẵn.
- Produces: API `GET|POST /api/v1/finance/account-banks`, `GET /options`, `GET|PUT /{id}` — FE (Task 8/9) gọi các URL này.

- [x] **Step 1: Viết controller**

```php
<?php

namespace Modules\Finance\Http\Controllers\V1;

use Illuminate\Http\Request;
use Modules\Finance\Http\Requests\CompanyAccount\CompanyAccountRequest;
use Modules\Finance\Services\CompanyAccountService;
use Modules\Finance\Transformers\CompanyAccountResource\CompanyAccountDetailResource;
use Modules\Finance\Transformers\CompanyAccountResource\CompanyAccountListResource;

class CompanyAccountController extends ApiController
{
    private $companyAccountService;

    public function __construct(CompanyAccountService $companyAccountService)
    {
        $this->companyAccountService = $companyAccountService;
    }

    public function index(Request $request)
    {
        $items = $this->companyAccountService->searchByFilter($request);

        return (new CompanyAccountListResource($items))->additional([
            'total' => $items->total(),
            'lastPage' => $items->lastPage(),
            'currentPage' => $items->currentPage(),
            'perPage' => (int) $items->perPage(),
        ]);
    }

    public function options()
    {
        return $this->responseJson('success', 200, $this->companyAccountService->options());
    }

    public function show($id)
    {
        $obj = $this->companyAccountService->findForCompany((int) $id);
        if (!$obj) {
            // Bản ghi công ty khác cũng trả 404 — không lộ sự tồn tại (edge case #3 spec).
            return $this->responseJson('Không tìm thấy tài khoản ngân hàng', 404);
        }

        return new CompanyAccountDetailResource($obj);
    }

    public function store(CompanyAccountRequest $request)
    {
        if (!$this->companyAccountService->currentCompanyId()) {
            // Edge case #2 spec: user không gắn công ty → chặn tạo, báo rõ.
            return $this->responseJson('Tài khoản đăng nhập chưa gắn công ty, không thể thao tác', 422);
        }
        $obj = $this->companyAccountService->createOrUpdate($request->only([
            'account_number', 'account_name', 'bank_id', 'bank_branch_id', 'currency_id', 'status',
        ]));

        return new CompanyAccountDetailResource($obj);
    }

    public function update(CompanyAccountRequest $request, $id)
    {
        $obj = $this->companyAccountService->findForCompany((int) $id);
        if (!$obj) {
            return $this->responseJson('Không tìm thấy tài khoản ngân hàng', 404);
        }
        $obj = $this->companyAccountService->createOrUpdate($request->only([
            'account_number', 'account_name', 'bank_id', 'bank_branch_id', 'currency_id', 'status',
        ]), $obj);

        return new CompanyAccountDetailResource($obj);
    }
}
```

- [x] **Step 2: Thêm routes**

Đầu file `Routes/api.php` thêm import:

```php
use Modules\Finance\Http\Controllers\V1\CompanyAccountController;
```

Cuối group `/v1/finance` (sau group `source-capitals`, trước `});` đóng group) thêm:

```php
    // Danh muc tai khoan ngan hang cua cong ty (bang ERP `company_accounts` tren DB gop)
    // 1 quyen duy nhat nhu ERP — index cung gan vi ERP chan index bang quyen nay.
    Route::group(['prefix' => '/account-banks'], function () {
        // Route tinh phai dat TRUOC /{id} de khong bi nuot
        Route::get('/', [CompanyAccountController::class, 'index'])
            ->middleware('checkPermission:Quản lý danh mục tài khoản ngân hàng');
        Route::get('/options', [CompanyAccountController::class, 'options'])
            ->middleware('checkPermission:Quản lý danh mục tài khoản ngân hàng');
        Route::post('/', [CompanyAccountController::class, 'store'])
            ->middleware('checkPermission:Quản lý danh mục tài khoản ngân hàng');
        Route::put('/{id}', [CompanyAccountController::class, 'update'])
            ->middleware('checkPermission:Quản lý danh mục tài khoản ngân hàng');
        Route::get('/{id}', [CompanyAccountController::class, 'show'])
            ->middleware('checkPermission:Quản lý danh mục tài khoản ngân hàng');
    });
```

- [x] **Step 3: Verify route đăng ký**

`php -l` 2 file sửa/tạo. Sau đó (KHÔNG dùng `route:list` — crash sẵn trong repo):

```
php artisan tinker --execute="collect(Route::getRoutes())->filter(function(\$r){ return strpos(\$r->uri(), 'account-banks') !== false; })->each(function(\$r){ echo implode('|', \$r->methods()) . ' ' . \$r->uri() . PHP_EOL; });"
```

Kỳ vọng: 5 dòng — GET `/`, GET `options`, POST `/`, PUT `{id}`, GET `{id}` (prefix `api/v1/finance/account-banks`).

---

### Task 6: Permission (seeder + DB local)

**Files:**
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (sau dòng 1099 — cuối khối "Danh mục tiền tệ", trước khối CSKH type 24)

**Interfaces:**
- Produces: quyền `Quản lý danh mục tài khoản ngân hàng` (id 1123, type 8, group `Danh mục tài chính`) — routes Task 5 và FE Task 8 check theo TÊN quyền này (khớp từng ký tự).

- [x] **Step 1: Thêm dòng seeder**

Id kế tiếp còn trống là **1123** (seeder hiện kết thúc ở 1122 — xác nhận lại bằng grep `'id' => 112` trước khi thêm). Group `Danh mục tài chính` ĐÃ tồn tại (không dính gotcha "group duy nhất toàn hệ thống"). Thêm sau dòng 1099:

```php
        // Danh mục tài khoản ngân hàng (chuyển từ ERP admin/accounting/account-banks) —
        // chỉ 1 quyền "Quản lý" như ERP (gate cả xem lẫn thao tác).
        Permission::create(['id' => 1123, 'guard_name' => 'api', 'name' => 'Quản lý danh mục tài khoản ngân hàng', 'display_name' => 'Quản lý danh mục tài khoản ngân hàng', 'group' => 'Danh mục tài chính', 'type' => 8]);
```

- [x] **Step 2: Insert DB local + cấp cho Super admin (KHÔNG chạy seeder)**

Mirror cách đã cấp quyền 1107-1110: tìm các role đang giữ quyền 1107 rồi cấp 1123 cho đúng các role đó. Chạy trong `hrm-api`:

```php
php artisan tinker --execute="
\$model = get_class(app(Spatie\Permission\PermissionRegistrar::class)->getPermissionClass());
\$p = \$model::query()->find(1123);
if (!\$p) { \$p = \$model::create(['id' => 1123, 'guard_name' => 'api', 'name' => 'Quản lý danh mục tài khoản ngân hàng', 'display_name' => 'Quản lý danh mục tài khoản ngân hàng', 'group' => 'Danh mục tài chính', 'type' => 8]); }
\$roleIds = DB::table('hrm_role_has_permissions')->where('permission_id', 1107)->pluck('role_id');
foreach (\$roleIds as \$rid) { DB::table('hrm_role_has_permissions')->insertOrIgnore(['permission_id' => 1123, 'role_id' => \$rid]); }
app(Spatie\Permission\PermissionRegistrar::class)->forgetCachedPermissions();
echo 'roles granted: ' . \$roleIds->implode(',');
"
```

Lưu ý: nếu bảng role-permission của HRM không tên `hrm_role_has_permissions` thì lấy tên thật từ `config('permission.table_names.role_has_permissions')` và thay vào. Nếu `display_name`/`group`/`type` không nằm trong `$fillable` của model Permission thì insert bằng `DB::table(config('permission.table_names.permissions'))->insert([...])` kèm `created_at/updated_at = now()`.

- [x] **Step 3: Verify**

```php
php artisan tinker --execute="
echo DB::table(config('permission.table_names.permissions'))->where('id', 1123)->value('name') . PHP_EOL;
echo 'grants: ' . DB::table(config('permission.table_names.role_has_permissions'))->where('permission_id', 1123)->count();
"
```

Kỳ vọng: in đúng tên quyền + `grants:` ≥ 1. `php -l` file seeder sạch.

---

### Task 7: Verify BE bằng HTTP thật

**Files:** không sửa code — chỉ test. Nếu test lòi bug thì fix ngay tại file liên quan (Task 1-6) rồi chạy lại.

**Interfaces:**
- Consumes: toàn bộ API Task 5 + quyền Task 6.

- [x] **Step 1: Dựng server + lấy JWT**

Chạy `php -S 127.0.0.1:8000 -t public` (background) trong `hrm-api`. Login lấy token:
`POST http://127.0.0.1:8000/api/auth/login` với tài khoản Super admin local (xem `.env` hoặc hỏi user nếu không có sẵn). Ghi `Authorization: Bearer <token>` cho các call sau. Ghi lại `company_id` của user (qua `auth()->user()->info->company_id` bằng tinker) để đối chiếu scope.

- [x] **Step 2: Bộ case validate (kỳ vọng 422 + đúng key trong `errors`)**

1. POST `{}` → 422, errors đủ 6 key: account_number, account_name, bank_id, bank_branch_id, currency_id, status.
2. POST với account_number TRÙNG số TK có sẵn trong 40 dòng → 422, `errors.account_number[0] = "Số tài khoản đã tồn tại"`.
3. POST với bank_branch_id KHÔNG thuộc bank_id đã chọn → 422, `errors.bank_branch_id[0] = "Chi nhánh không thuộc ngân hàng đã chọn"`.
4. Tạo 1 bản ghi hợp lệ (account_number `TEST-HTTP-001`) → 200/201, response data có id. GHI LẠI id để dọn.
5. PUT bản ghi vừa tạo, BỎ currency_id → 422 (xác nhận sửa lỗi ERP update thiếu required).
6. PUT bản ghi vừa tạo với status '0' + đổi account_name → 200; GET /{id} thấy status '0', account_name UPPERCASE.

- [x] **Step 3: Bộ case scope + quyền**

7. GET danh sách → mọi dòng thuộc company user login (đối chiếu bằng tinker: `CompanyAccount::where('company_id','!=',X)->count()` so với tổng). Lọc `?status=0` chỉ trả dòng khóa; `?status=1` chỉ trả hoạt động ('0' không bị nuốt).
8. Tinker: tạo tạm 1 bản ghi company_id KHÁC (nhớ id) → GET /{id} bằng token hiện tại → 404; PUT /{id} → 404. Xóa bản ghi tạm ngay.
9. Gọi GET danh sách bằng token của user KHÔNG có quyền `Quản lý danh mục tài khoản ngân hàng` (hoặc tạm thu quyền của 1 user test) → 403.
10. GET `/options` → JSON có `banks` + `bank_branches`, branch có trường `bank_id`. GET `/api/v1/finance/currencies/getAll` → danh sách tiền tệ (endpoint có sẵn, chỉ xác nhận còn chạy).

- [x] **Step 4: Dọn dẹp**

Xóa bản ghi `TEST-HTTP-001` + mọi bản ghi test bằng tinker theo ĐÍCH DANH id đã ghi (không xóa theo pattern). Verify: `CompanyAccount::count()` = 40 (baseline Task 1). Check `storage/logs/laravel.log` không có lỗi mới ngoài các call 4xx chủ đích. Tắt server test.

---

### Task 8: FE — menu + trang danh sách

**Files:**
- Modify: `hrm-client/components/subsystem-menu/finance.js` (dòng 42: slot xám `{ label: 'Danh mục tài khoản ngân hàng' }`)
- Create: `hrm-client/pages/finance/account-banks/index.vue`

**Interfaces:**
- Consumes: API `finance/account-banks` (Task 5), quyền `Quản lý danh mục tài khoản ngân hàng` (Task 6), modal `AccountBankModal` (Task 9 — ref `accountBankModal`, method `open(id|null)`, emit `saved`).
- Produces: route FE `/finance/account-banks`.

- [x] **Step 0: Đọc skill**

Đọc `.claude/skills/list-page/SKILL.md` + `.claude/skills/button-convention/SKILL.md` trước khi code.

- [x] **Step 1: Sửa menu**

Thay dòng 42 `{ label: 'Danh mục tài khoản ngân hàng' },` bằng:

```js
            {
                label: 'Danh mục tài khoản ngân hàng',
                link: '/finance/account-banks',
                isShow: ['Quản lý danh mục tài khoản ngân hàng'],
            },
```

- [x] **Step 2: Viết trang danh sách**

Mirror `pages/finance/cost-debts/index.vue` (đã áp các bài học phân trang), KHÁC BIỆT: thêm `DedupeLoadMixin` + `buildParams()` (spec yêu cầu đủ 4 bài học Phase 8); status dùng `'1'/'0'` (KHÔNG phải '1'/'2' như cost-debts); không có nút Xóa.

```vue
<template>
  <div class="v2-styles min-vh-100 d-flex justify-content-center pt-2">
    <div class="container-fluid">
      <V2BaseFilterPanel
        title="Bộ lọc danh mục tài khoản ngân hàng"
        :collapsed="filterCollapsed"
        :quickSearchValue="filters.keyword"
        quickSearchPlaceholder="Tìm theo số tài khoản, chủ tài khoản, ngân hàng"
        :filters="filters"
        @toggle-panel="filterCollapsed = !filterCollapsed"
        @quick-search-change="(v) => (filters.keyword = v)"
        @search="handleSearch"
        @reset="handleReset"
      >
        <template #advanced-filters="{ collapsed }">
          <div v-show="!collapsed" class="row">
            <div class="col-md-3">
              <V2BaseLabel text="Số tài khoản" />
              <V2BaseInput v-model="filters.account_number" size="sm" />
            </div>
            <div class="col-md-3">
              <V2BaseLabel text="Chủ tài khoản" />
              <V2BaseInput v-model="filters.account_name" size="sm" />
            </div>
            <div class="col-md-3">
              <V2BaseLabel text="Ngân hàng" />
              <V2BaseInput v-model="filters.bank_name" size="sm" />
            </div>
            <div class="col-md-3">
              <V2BaseLabel text="Chi nhánh" />
              <V2BaseInput v-model="filters.bank_branch" size="sm" />
            </div>
            <div class="col-md-3 mt-2">
              <V2BaseLabel text="Trạng thái" />
              <V2BaseSelect v-model="filters.status" :options="statusFilterOptions" size="sm" />
            </div>
          </div>
        </template>
      </V2BaseFilterPanel>

      <V2BaseDataTable
        :data="tableData"
        :columns="tableColumns"
        :pagination="pagination"
        :loading="loading"
        title="Danh sách tài khoản ngân hàng"
        rowKey="id"
        itemLabel="tài khoản"
        emptyText="Không có dữ liệu phù hợp bộ lọc."
        @page-change="handlePageChange"
        @page-size-change="handlePageSizeChange"
      >
        <template #actions-bottom>
          <V2BaseButton v-if="canManage" primary size="sm" class="btn-compact" @click="openCreate">
            <template #prefix>
              <i class="ri-add-line" style="font-size: 13px"></i>
            </template>
            Thêm tài khoản
          </V2BaseButton>
        </template>
        <template #cell-index="{ index }">
          {{ (pagination.currentPage - 1) * pagination.pageSize + index + 1 }}
        </template>
        <template #cell-status="{ item }">
          <V2BaseBadge :variant="item.status === '1' ? 'brand' : 'required'">
            {{ item.status_text }}
          </V2BaseBadge>
        </template>
        <template #cell-actions="{ item }">
          <V2BaseIconButton v-if="canManage" title="Sửa" @click="openEdit(item)">
            <i class="ri-pencil-line"></i>
          </V2BaseIconButton>
        </template>
      </V2BaseDataTable>

      <AccountBankModal ref="accountBankModal" @saved="handleSaved" />
    </div>
  </div>
</template>

<script>
import V2BaseFilterPanel from '@/components/V2BaseFilterPanel.vue'
import V2BaseDataTable from '@/components/V2BaseDataTable.vue'
import V2BaseSelect from '@/components/V2BaseSelect.vue'
import V2BaseInput from '@/components/V2BaseInput.vue'
import V2BaseLabel from '@/components/V2BaseLabel.vue'
import V2BaseButton from '@/components/V2BaseButton.vue'
import V2BaseBadge from '@/components/V2BaseBadge.vue'
import V2BaseIconButton from '@/components/V2BaseIconButton.vue'
import PageTitleMixin from '@/utils/mixins/PageTitleMixin'
import CheckPermission from '@/utils/mixins/CheckPermission'
import filterStateMixin from '@/utils/mixins/filterStateMixin.js'
import DedupeLoadMixin from '@/utils/mixins/DedupeLoadMixin.js'
import { buildQueryString } from '@/utils/url-action'
import AccountBankModal from './AccountBankModal.vue'

const initialStateForm = {
  keyword: undefined,
  account_number: undefined,
  account_name: undefined,
  bank_name: undefined,
  bank_branch: undefined,
  status: undefined,
}

export default {
  layout: 'default-sidebar',
  mixins: [PageTitleMixin, CheckPermission, filterStateMixin, DedupeLoadMixin],
  components: {
    V2BaseFilterPanel,
    V2BaseDataTable,
    V2BaseSelect,
    V2BaseInput,
    V2BaseLabel,
    V2BaseButton,
    V2BaseBadge,
    V2BaseIconButton,
    AccountBankModal,
  },
  data() {
    return {
      loading: false,
      tableData: [],
      // page/per_page tách khỏi filters (bài học Phase 8: deep watcher coi đổi trang là đổi bộ lọc)
      pagination: { currentPage: 1, pageSize: 10, total: 0, totalPages: 1, from: 0, to: 0 },
      filterCollapsed: true,
      filters: { ...initialStateForm },
      ignoredFields: ['keyword'],
      oldFilters: {},
      statusFilterOptions: [
        { id: undefined, name: 'Tất cả' },
        { id: '1', name: 'Hoạt động' },
        { id: '0', name: 'Khóa' },
      ],
      // filterStateMixin
      filterFieldName: 'filters',
      localStorageKey: 'finance_account_banks',
      pathsToKeep: ['/finance/account-banks'],
      expirationTime: 10 * 60 * 1000,
    }
  },
  computed: {
    pageTitle() {
      return 'Danh mục tài khoản ngân hàng'
    },
    canManage() {
      return this.hasAPermission('Quản lý danh mục tài khoản ngân hàng')
    },
    tableColumns() {
      return [
        { key: 'index', title: 'STT', sticky: true, align: 'left' },
        { key: 'account_number', title: 'Số tài khoản', sticky: true, align: 'left' },
        { key: 'currency_text', title: 'Loại tiền tệ', align: 'left' },
        { key: 'account_name', title: 'Chủ tài khoản', align: 'left', cellClass: 'text-wrap' },
        { key: 'bank_name', title: 'Ngân hàng', align: 'left', cellClass: 'text-wrap' },
        { key: 'bank_branch', title: 'Chi nhánh', align: 'left', cellClass: 'text-wrap' },
        { key: 'status', title: 'Trạng thái', align: 'left' },
        { key: 'actions', title: 'Thao tác', align: 'center' },
      ]
    },
  },
  created() {
    this.oldFilters = JSON.parse(JSON.stringify(this.filters))
  },
  watch: {
    filters: {
      handler(newVal) {
        const shouldCallApi = !this.ignoredFields.some((f) => newVal[f] !== this.oldFilters[f])
        if (shouldCallApi) {
          this.pagination.currentPage = 1
          this.loadData()
        }
        this.oldFilters = JSON.parse(JSON.stringify(this.filters))
      },
      deep: true,
    },
  },
  mounted() {
    const savedState = this.loadFilterState()
    if (savedState) {
      this.filters = { ...initialStateForm, ...savedState.filter }
      if (savedState.filterCollapsed !== undefined) this.filterCollapsed = savedState.filterCollapsed
    }
    this.oldFilters = JSON.parse(JSON.stringify(this.filters))
    this.loadData()
  },
  methods: {
    buildParams() {
      return {
        page: this.pagination.currentPage,
        per_page: this.pagination.pageSize,
        keyword: this.filters.keyword || undefined,
        account_number: this.filters.account_number || undefined,
        account_name: this.filters.account_name || undefined,
        bank_name: this.filters.bank_name || undefined,
        bank_branch: this.filters.bank_branch || undefined,
        status: this.filters.status,
      }
    },
    async loadData() {
      const params = this.buildParams()
      if (this.isDuplicateLoad(params)) return
      this.loading = true
      try {
        const res = await this.$store.dispatch('apiGetMethod', `finance/account-banks${buildQueryString(params)}`)
        this.tableData = res.data || []
        // Ép Number() toàn bộ meta — Laravel trả per_page dạng CHUỖI (bài học Phase 8)
        Object.assign(this.pagination, {
          currentPage: Number(res.currentPage) || 1,
          pageSize: Number(res.perPage) || 10,
          total: Number(res.total) || 0,
          totalPages: Number(res.lastPage) || 1,
        })
      } catch (error) {
        if (error?.response?.status !== 403) {
          this.$toasted?.global?.error?.({ message: 'Lỗi khi tải dữ liệu' })
        }
      } finally {
        this.loading = false
      }
    },
    handleSearch() {
      this.pagination.currentPage = 1
      this.loadData()
    },
    // Chỉ đổi filters — deep watcher tự load (bài học Phase 8: không gọi loadData ở đây)
    handleReset() {
      this.filters = { ...initialStateForm }
    },
    handlePageChange(page) {
      this.pagination.currentPage = page
      this.loadData()
    },
    handlePageSizeChange(size) {
      this.pagination.pageSize = size
      this.pagination.currentPage = 1
      this.loadData()
    },
    openCreate() {
      this.$refs.accountBankModal.open(null)
    },
    openEdit(row) {
      this.$refs.accountBankModal.open(row.id)
    },
    handleSaved() {
      this.resetLoadDedupe()
      this.loadData()
    },
  },
}
</script>

<style lang="scss">
@import '@/assets/scss/v2-styles.scss';
</style>
```

- [x] **Step 3: Verify parse**

hrm-client KHÔNG có ESLint (Node 14) — verify bằng vue-template-compiler + @babel/parser như các màn trước (script parse template + script của `index.vue`, kỳ vọng không lỗi). Kiểm icon: `ri-add-line`, `ri-pencil-line` có trong `_remixicon.scss` (grep `^\.ri-add-line:before` và `^\.ri-pencil-line:before`).

---

### Task 9: FE — modal Thêm/Sửa `AccountBankModal`

**Files:**
- Create: `hrm-client/pages/finance/account-banks/AccountBankModal.vue`

**Interfaces:**
- Consumes: API `finance/account-banks` (POST/PUT/GET /{id}/options — Task 5), `finance/currencies/getAll` (có sẵn, response `responseJson` → lấy `res.data`).
- Produces: component `AccountBankModal` — method `open(id|null)`, emit `saved` (Task 8 đã gọi đúng tên này).

- [x] **Step 0: Đọc skill**

Đọc `.claude/skills/modal-popup/SKILL.md` trước khi code. Select trong modal BẮT BUỘC `V2BaseSelectInModal`.

- [x] **Step 1: Viết modal**

Mirror `pages/finance/cost-debts/CostDebtModal.vue`, thêm: 3 select (tiền tệ / ngân hàng / chi nhánh cascade), loading `$nuxt.$loading` cho submit, options load khi mở.

```vue
<template>
  <b-modal id="finance-account-bank-modal" ref="modal" hide-footer size="lg" content-class="shadow" @hide="reset">
    <template #modal-header>
      <h5 class="modal-title mb-0">{{ id ? 'Sửa tài khoản ngân hàng' : 'Thêm tài khoản ngân hàng' }}</h5>
      <button type="button" class="close" @click="$refs.modal.hide()">
        <span aria-hidden="true">&times;</span>
      </button>
    </template>

    <div class="modal-body">
      <div class="form-row">
        <div class="col-md-6 mb-2">
          <V2BaseLabel>Số tài khoản <span class="text-danger">*</span></V2BaseLabel>
          <V2BaseInput
            v-model="form.account_number"
            size="sm"
            :class="{ 'is-invalid': touched && formError.account_number }"
          />
          <div v-if="touched && formError.account_number" class="text-small-error mt-1">
            <i class="ri-error-warning-line mr-1"></i>{{ formError.account_number }}
          </div>
        </div>

        <div class="col-md-6 mb-2">
          <V2BaseLabel>Loại tiền tệ <span class="text-danger">*</span></V2BaseLabel>
          <V2BaseSelectInModal
            v-model="form.currency_id"
            :options="currencyOptions"
            size="sm"
            :class="{ 'is-invalid': touched && formError.currency_id }"
          />
          <div v-if="touched && formError.currency_id" class="text-small-error mt-1">
            <i class="ri-error-warning-line mr-1"></i>{{ formError.currency_id }}
          </div>
        </div>
      </div>

      <div class="form-row">
        <div class="col-md-12 mb-2">
          <V2BaseLabel>Chủ tài khoản <span class="text-danger">*</span></V2BaseLabel>
          <V2BaseInput
            v-model="form.account_name"
            size="sm"
            placeholder="Hệ thống tự chuyển thành CHỮ IN HOA khi lưu"
            :class="{ 'is-invalid': touched && formError.account_name }"
          />
          <div v-if="touched && formError.account_name" class="text-small-error mt-1">
            <i class="ri-error-warning-line mr-1"></i>{{ formError.account_name }}
          </div>
        </div>
      </div>

      <div class="form-row">
        <div class="col-md-6 mb-2">
          <V2BaseLabel>Ngân hàng <span class="text-danger">*</span></V2BaseLabel>
          <V2BaseSelectInModal
            v-model="form.bank_id"
            :options="bankOptions"
            size="sm"
            :class="{ 'is-invalid': touched && formError.bank_id }"
          />
          <div v-if="touched && formError.bank_id" class="text-small-error mt-1">
            <i class="ri-error-warning-line mr-1"></i>{{ formError.bank_id }}
          </div>
        </div>

        <div class="col-md-6 mb-2">
          <V2BaseLabel>Chi nhánh <span class="text-danger">*</span></V2BaseLabel>
          <V2BaseSelectInModal
            v-model="form.bank_branch_id"
            :options="branchOptionsForBank"
            size="sm"
            :disabled="!form.bank_id"
            :class="{ 'is-invalid': touched && formError.bank_branch_id }"
          />
          <div v-if="touched && formError.bank_branch_id" class="text-small-error mt-1">
            <i class="ri-error-warning-line mr-1"></i>{{ formError.bank_branch_id }}
          </div>
        </div>
      </div>

      <div class="form-row">
        <div class="col-md-6 mb-2">
          <V2BaseLabel>Trạng thái <span class="text-danger">*</span></V2BaseLabel>
          <V2BaseSelectInModal
            v-model="form.status"
            :options="statusOptions"
            size="sm"
            :allowClear="false"
          />
          <div v-if="touched && formError.status" class="text-small-error mt-1">
            <i class="ri-error-warning-line mr-1"></i>{{ formError.status }}
          </div>
        </div>
      </div>
    </div>

    <div class="modal-footer">
      <V2BaseButton primary :disabled="submitting" @click="submit">
        <template #prefix><i class="ri-save-3-line mr-1"></i></template>
        Lưu
      </V2BaseButton>
      <V2BaseButton light :disabled="submitting" @click="$refs.modal.hide()">Đóng</V2BaseButton>
    </div>
  </b-modal>
</template>

<script>
import V2BaseLabel from '@/components/V2BaseLabel.vue'
import V2BaseInput from '@/components/V2BaseInput.vue'
import V2BaseSelectInModal from '@/components/V2BaseSelectInModal.vue'
import V2BaseButton from '@/components/V2BaseButton.vue'

export default {
  name: 'AccountBankModal',
  components: { V2BaseLabel, V2BaseInput, V2BaseSelectInModal, V2BaseButton },
  data() {
    return {
      id: null,
      form: {
        account_number: '',
        account_name: '',
        currency_id: undefined,
        bank_id: undefined,
        bank_branch_id: undefined,
        status: '1',
      },
      formError: {},
      touched: false,
      submitting: false,
      bankOptions: [],
      branchOptions: [],
      currencyOptions: [],
      optionsLoaded: false,
      statusOptions: [
        { id: '1', name: 'Hoạt động' },
        { id: '0', name: 'Khóa' },
      ],
    }
  },
  computed: {
    // Lọc chi nhánh theo ngân hàng đã chọn ở client — như ERP (options load 1 lần)
    branchOptionsForBank() {
      if (!this.form.bank_id) return []
      return this.branchOptions.filter((b) => String(b.bank_id) === String(this.form.bank_id))
    },
  },
  watch: {
    // Đổi ngân hàng → reset chi nhánh nếu chi nhánh đang chọn không thuộc ngân hàng mới.
    // So sánh trước khi reset để KHÔNG clobber giá trị vừa nạp từ loadDetail.
    'form.bank_id'(newVal) {
      const branch = this.branchOptions.find((b) => String(b.id) === String(this.form.bank_branch_id))
      if (!branch || String(branch.bank_id) !== String(newVal)) {
        this.form.bank_branch_id = undefined
      }
    },
  },
  methods: {
    async open(id) {
      this.reset()
      this.id = id
      this.$refs.modal.show()
      await this.loadOptions()
      if (id) await this.loadDetail(id)
    },
    reset() {
      this.id = null
      this.form = {
        account_number: '',
        account_name: '',
        currency_id: undefined,
        bank_id: undefined,
        bank_branch_id: undefined,
        status: '1',
      }
      this.formError = {}
      this.touched = false
    },
    async loadOptions() {
      if (this.optionsLoaded) return
      try {
        const [banksRes, currenciesRes] = await Promise.all([
          this.$store.dispatch('apiGetMethod', 'finance/account-banks/options'),
          this.$store.dispatch('apiGetMethod', 'finance/currencies/getAll'),
        ])
        const opts = banksRes.data || {}
        this.bankOptions = opts.banks || []
        this.branchOptions = opts.bank_branches || []
        this.currencyOptions = (currenciesRes.data || []).map((c) => ({
          id: c.id,
          name: `${c.code} — ${c.name}`,
        }))
        this.optionsLoaded = true
      } catch (error) {
        if (error?.response?.status !== 403) {
          this.$toasted?.global?.error?.({ message: 'Lỗi khi tải danh mục ngân hàng/tiền tệ' })
        }
      }
    },
    async loadDetail(id) {
      try {
        const res = await this.$store.dispatch('apiGetMethod', `finance/account-banks/${id}`)
        const d = res.data || res
        this.form = {
          account_number: d.account_number || '',
          account_name: d.account_name || '',
          currency_id: d.currency_id || undefined, // bản ghi cũ null → bắt chọn mới cho lưu (edge case #5 spec)
          bank_id: d.bank_id || undefined,
          bank_branch_id: d.bank_branch_id || undefined,
          status: String(d.status),
        }
      } catch (error) {
        const status = Number(error?.response?.status)
        if (status !== 403) {
          this.$toasted?.global?.error?.({ message: error?.response?.data?.message || 'Lỗi khi tải dữ liệu' })
        }
        this.$refs.modal.hide()
      }
    },
    validateLocal() {
      const e = {}
      if (!this.form.account_number || !this.form.account_number.trim()) e.account_number = 'Bắt buộc phải nhập'
      if (!this.form.account_name || !this.form.account_name.trim()) e.account_name = 'Bắt buộc phải nhập'
      if (!this.form.currency_id) e.currency_id = 'Bắt buộc phải nhập'
      if (!this.form.bank_id) e.bank_id = 'Bắt buộc phải nhập'
      if (!this.form.bank_branch_id) e.bank_branch_id = 'Bắt buộc phải nhập'
      this.formError = e
      return Object.keys(e).length === 0
    },
    async submit() {
      this.touched = true
      if (!this.validateLocal()) return
      this.submitting = true
      this.$nuxt.$loading.start()
      try {
        const payload = {
          account_number: this.form.account_number.trim(),
          account_name: this.form.account_name.trim(),
          currency_id: this.form.currency_id,
          bank_id: this.form.bank_id,
          bank_branch_id: this.form.bank_branch_id,
          status: this.form.status,
        }
        if (this.id) {
          await this.$store.dispatch('apiPutMethod', { url: `finance/account-banks/${this.id}`, payload })
        } else {
          await this.$store.dispatch('apiPostMethod', { url: 'finance/account-banks', payload })
        }
        this.$toasted?.global?.success?.({ message: this.id ? 'Cập nhật thành công' : 'Thêm mới thành công' })
        this.$emit('saved')
        this.$refs.modal.hide()
      } catch (error) {
        const status = Number(error?.response?.status)
        if (status === 422) {
          const errs = error.response.data.errors || {}
          // Laravel 422: errors.field = [msg,...] → lấy msg đầu, map vào đúng input
          this.formError = Object.keys(errs).reduce((a, k) => {
            a[k] = Array.isArray(errs[k]) ? errs[k][0] : errs[k]
            return a
          }, {})
          // 422 không có errors (vd: chưa gắn công ty) → toast message
          if (!Object.keys(errs).length) {
            this.$toasted?.global?.error?.({ message: error?.response?.data?.message || 'Thao tác thất bại' })
          }
        } else if (status !== 403) {
          this.$toasted?.global?.error?.({ message: error?.response?.data?.message || 'Thao tác thất bại' })
        }
      } finally {
        this.submitting = false
        this.$nuxt.$loading.finish()
      }
    },
  },
}
</script>

<style scoped>
.text-small-error {
  font-size: 12px;
  color: #dc3545;
  display: flex;
  align-items: center;
}
</style>
```

- [x] **Step 2: Verify parse**

Parse template + script bằng vue-template-compiler + @babel/parser — kỳ vọng không lỗi. Icon `ri-save-3-line`, `ri-error-warning-line` đối chiếu `_remixicon.scss`.

---

### Task 10: Verify browser Playwright + dọn dẹp

**Files:** không sửa code (trừ khi lòi bug — fix tại file liên quan rồi test lại).

- [x] **Step 1: Dựng môi trường**

FE localhost:3000 (Laragon/`npm run dev` sẵn của user — hỏi user nếu chưa chạy), BE `php -S 127.0.0.1:8000 -t public`. Login bằng tài khoản Super admin (đã có quyền 1123 từ Task 6).

- [x] **Step 2: Kịch bản E2E (Playwright MCP)**

1. Menu Tài chính → Danh mục → "Danh mục tài khoản ngân hàng" hết xám, click vào `/finance/account-banks`, bảng render dữ liệu thật (đối chiếu số dòng với DB theo company user).
2. Bấm "Thêm tài khoản" → submit rỗng → 5 lỗi inline "Bắt buộc phải nhập" (số TK, tiền tệ, chủ TK, ngân hàng, chi nhánh), KHÔNG toast lỗi validate.
3. Chọn ngân hàng → dropdown chi nhánh chỉ hiện chi nhánh của ngân hàng đó; đổi sang ngân hàng khác → chi nhánh đã chọn bị reset.
4. Nhập đủ (số TK `TEST-E2E-001`, chủ TK chữ thường) → Lưu → toast thành công, dòng mới đầu danh sách, chủ TK hiển thị IN HOA, tiền tệ đúng code.
5. Nhập số TK trùng dòng có sẵn → Lưu → lỗi inline "Số tài khoản đã tồn tại" tại đúng ô số TK.
6. Sửa `TEST-E2E-001`: modal nạp đúng 6 giá trị; đổi trạng thái → Khóa → Lưu → badge danh sách đổi đỏ "Khóa"; lọc Trạng thái = Khóa → dòng xuất hiện; lọc = Hoạt động → biến mất.
7. Bộ lọc nâng cao: từng ô (số TK / chủ TK / ngân hàng / chi nhánh) lọc đúng; quick search keyword; Đặt lại → về mặc định, KHÔNG request đúp (check số request qua `browser_network_requests` — mỗi thao tác đúng 1 request).
8. Đổi trang / đổi số dòng trên trang → mỗi thao tác đúng 1 request (DedupeLoadMixin hoạt động).
9. Mở màn ERP `admin/accounting/account-banks` cùng công ty (nếu ERP local đang chạy — nếu không, đối chiếu trực tiếp DB bằng tinker) → thấy `TEST-E2E-001` (2 màn cùng bảng).

- [x] **Step 3: Dọn dẹp**

Xóa `TEST-E2E-001` bằng tinker theo đích danh id (màn không có nút xóa — xóa qua DB là chủ đích). Verify `CompanyAccount::count()` = 40. Xóa screenshot test theo ĐÍCH DANH tên file (không wildcard). Check `laravel.log` sạch lỗi mới. Tắt server test.

- [ ] **Step 4: Checkpoint**

Cập nhật checkpoint vào cuối file này theo format bắt buộc + báo user test lại bằng mắt.

---

### Task 11: Fix F1 review tổng — scope company_id NULL (BE)

**Files:**
- Modify: `hrm-api/Modules/Finance/Services/CompanyAccountService.php`

Finding F1 (Important): `where('company_id', null)` compile thành `IS NULL` — user không gắn công ty sẽ thấy/sửa được dòng `company_id NULL` nếu tồn tại (ERP song song có thể sinh). Vi phạm spec §5 edge #2.

- [x] **Step 1: Early-return trong `searchByFilter`** — khi `currentCompanyId() === null` trả paginator rỗng (`CompanyAccount::query()->whereRaw('1 = 0')->paginate($limit)` hoặc tương đương), kèm sửa comment sai cơ chế ở dòng ~34.
- [x] **Step 2: Early-return trong `findForCompany`** — company null → `return null` ngay (show/update tự 404).
- [x] **Step 3: Tiện tay sửa comment nhầm nhánh dedupe** ở `hrm-client/pages/finance/account-banks/index.vue` (~dòng 232-234): dedupe chặn call của watcher (call trực tiếp chạy trước), không phải ngược lại.
- [x] **Step 4: Verify** — php -l; tinker mô phỏng company null (mock service hoặc query whereRaw) xác nhận 0 dòng; parse lại index.vue.

### Task 12: UI danh sách — gộp thao tác vào cột Số tài khoản + chức năng Xem (yêu cầu user 2026-08-04)

**Files:**
- Modify: `hrm-client/pages/finance/account-banks/index.vue`
- Modify: `hrm-client/pages/finance/account-banks/AccountBankModal.vue`

Mirror pattern màn `/human/banks` (`pages/human/banks/index.vue` cột `bankInfo` + Phase 5 Xem chi tiết).

- [x] **Step 1: index.vue — bỏ cột `actions`**, cột `account_number` render `V2BaseTitleSubInfo` (title = số TK bold; sub = chủ TK nếu cần thì thôi — chỉ số TK) + slot `#actions` chứa 2 nút theo thứ tự button-convention **Xem → Sửa**:

```vue
<template #cell-account_number="{ item }">
    <V2BaseTitleSubInfo
        :title="[{ text: item.account_number, isLightColor: false }]"
        titleClass="field-line font-weight-bold text-dark"
    >
        <template #actions>
            <button type="button" class="btn btn-light border btn-sm mr-1" title="Xem" @click="viewItem(item)">
                <i class="ri-eye-line"></i>
            </button>
            <button v-if="canManage" type="button" class="btn btn-light border btn-sm mr-1" title="Sửa" @click="openEdit(item)">
                <i class="ri-pencil-line"></i>
            </button>
        </template>
    </V2BaseTitleSubInfo>
</template>
```

Import `V2BaseTitleSubInfo`, bỏ `V2BaseIconButton` nếu không còn dùng; bỏ cột `{ key: 'actions', ... }` khỏi `tableColumns`; thêm method `viewItem(row) { this.$refs.accountBankModal.open(row.id, true) }`.

- [x] **Step 2: AccountBankModal.vue — chế độ Xem** (mirror BankModel.vue Phase 5, nhưng theo pattern open() nội bộ — không prop, không dính bug $nextTick):
  - `open(id, isView = false)` → set `this.isView = isView`; `reset()` đặt lại `isView = false`.
  - Title: Xem → "Xem chi tiết tài khoản ngân hàng"; các input/select thêm `:disabled="isView"` (giữ nguyên disabled cascade chi nhánh khi chưa chọn bank).
  - Footer: khi `isView` chỉ còn nút Đóng (ẩn nút Lưu); `submit()` guard `if (this.isView) return`.
  - Icon `ri-eye-line` đã có trong font local (banks đang dùng).
- [x] **Step 3: Verify** — parse 2 file; Playwright nhanh: mở Xem (6 field disabled, đúng dữ liệu, footer chỉ Đóng) → đóng → mở Sửa cùng dòng (input enable lại, footer có Lưu — isView reset đúng); nút Xem/Sửa nằm trong ô Số tài khoản, cột Thao tác biến mất; xoá data/screenshot test.

### Task 13: Khóa/mở khóa nhanh trên cột Trạng thái (yêu cầu user 2026-08-04, mirror assign/solution-groups)

**Files:**
- Modify: `hrm-api/Modules/Finance/Services/CompanyAccountService.php` (thêm `setStatus`)
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/CompanyAccountController.php` (thêm `lock`/`unlock`)
- Modify: `hrm-api/Modules/Finance/Routes/api.php` (thêm 2 route)
- Modify: `hrm-client/pages/finance/account-banks/index.vue` (cell status + confirm modal + CSS)

Mẫu: `pages/assign/solution-groups/index.vue` (cell-status `status-wrap` + `toggle-status-btn` + BaseConfirmModal + endpoint `/{id}/lock|unlock`). KHÁC BIỆT: status màn này `'1'/'0'` (không phải 1/2); KHÔNG có điều kiện cha-con (`is_can_lock_update`) — chỉ ẩn nút khi thiếu `canManage`.

- [x] **Step 1: Service** — thêm method:

```php
    public function setStatus(CompanyAccount $obj, int $status): CompanyAccount
    {
        $obj->status = $status;
        $obj->save();

        return $obj;
    }
```

- [x] **Step 2: Controller** — thêm 2 method (sau `update`), dùng `findForCompany` → 404 như show/update:

```php
    public function lock($id)
    {
        $obj = $this->companyAccountService->findForCompany((int) $id);
        if (!$obj) {
            return $this->responseJson('Không tìm thấy tài khoản ngân hàng', 404);
        }
        $this->companyAccountService->setStatus($obj, CompanyAccount::STATUS_LOCKED);

        return $this->responseJson('Khóa tài khoản ngân hàng thành công', 200);
    }

    public function unlock($id)
    {
        $obj = $this->companyAccountService->findForCompany((int) $id);
        if (!$obj) {
            return $this->responseJson('Không tìm thấy tài khoản ngân hàng', 404);
        }
        $this->companyAccountService->setStatus($obj, CompanyAccount::STATUS_ACTIVE);

        return $this->responseJson('Mở khóa tài khoản ngân hàng thành công', 200);
    }
```

(import `use Modules\Finance\Entities\CompanyAccount\CompanyAccount;` nếu chưa có.)

- [x] **Step 3: Routes** — thêm TRƯỚC `GET /{id}` (mirror thứ tự các group khác):

```php
        Route::get('/{id}/lock', [CompanyAccountController::class, 'lock'])
            ->middleware('checkPermission:Quản lý danh mục tài khoản ngân hàng');
        Route::get('/{id}/unlock', [CompanyAccountController::class, 'unlock'])
            ->middleware('checkPermission:Quản lý danh mục tài khoản ngân hàng');
```

- [x] **Step 4: FE cell status** — thay template `#cell-status` hiện tại:

```vue
        <template #cell-status="{ item }">
          <div class="status-wrap">
            <V2BaseBadge :variant="item.status === '1' ? 'brand' : 'required'">
              {{ item.status_text }}
            </V2BaseBadge>
            <button
              v-if="canManage"
              class="toggle-status-btn"
              :title="item.status === '0' ? 'Mở khóa tài khoản' : 'Khóa tài khoản'"
              @click="confirmToggleLock(item)"
            >
              <i :class="item.status === '0' ? 'ri-lock-unlock-line' : 'ri-lock-line'"></i>
            </button>
          </div>
        </template>
```

Thêm `BaseConfirmModal` (id `confirm-toggle-lock-account-bank`, title/message/action computed theo `itemToToggle.status`), state `itemToToggle`, method `confirmToggleLock(item)` + `handleConfirmToggleLock()` gọi `apiGetMethod` `finance/account-banks/${id}/lock|unlock`, toast thành công, `resetLoadDedupe()` + `loadData()`; lỗi: 403 im lặng, 404 "Dữ liệu đã thay đổi, vui lòng tải lại", khác → message BE. CSS copy `.status-wrap` + `.toggle-status-btn` (kể cả `:hover`, `:disabled`, `i`) từ solution-groups vào block style của màn. Icon `ri-lock-line`/`ri-lock-unlock-line` phải grep `_remixicon.scss`.

- [x] **Step 5: Verify** — php -l 3 file BE + tinker liệt kê 7 route account-banks; parse index.vue; HTTP nhanh: lock rồi unlock 1 bản ghi thật company 1 (ghi lại status gốc, trả về nguyên trạng), 404 với id company khác; Playwright: pill + nút khóa hiện, confirm modal đúng chữ, khóa → badge đỏ → mở khóa → badge xanh (dùng 1 bản ghi thật, trả về trạng thái ban đầu, verify DB nguyên trạng).

## Ghi chú cho người thực thi

- Mẫu code chuẩn đã đối chiếu trong codebase: BE bộ `SourceCapital*` (controller/service/request/resource), FE `pages/finance/cost-debts/` (list + modal). Khi phân vân style → mở các file đó.
- `php artisan route:list` crash SẴN trong repo — dùng tinker liệt kê route (xem Task 5 Step 3).
- Log BE tại `hrm-api/storage/logs/laravel.log` (LOG_CHANNEL=single — không phải laravel-[ngày].log).
- Seeder hiện có 2 dòng TRÙNG quyền tiền tệ (id 1117/1118 lặp lại name của 1115/1116) — lỗi CÓ SẴN, KHÔNG thuộc feature này, KHÔNG tự sửa (đã báo user).

### Checkpoint — 2026-08-04
Vừa hoàn thành: TOÀN BỘ 12 task (BE + FE + verify HTTP 10/10 + E2E 9/9 + final review + fix F1 + Task 12 gộp cột thao tác vào Số tài khoản + chức năng Xem read-only). Review từng task + final review đều Approved.
Đang làm dở: không.
Bước tiếp theo: user test lại toàn màn /finance/account-banks trên browser (F5 để nạp lại quyền; BE đang chạy `php artisan serve` port 8000). Báo team vụ seeder trùng id 1117/1118 (pre-existing).
Blocked: không.

### Task 14: Placeholder input bộ lọc (yêu cầu user 2026-08-04, micro — làm inline)

- [x] 4 input bộ lọc nâng cao thêm placeholder "Nhập số tài khoản / Nhập tên chủ tài khoản / Nhập tên ngân hàng / Nhập tên chi nhánh" (convention màn banks); select Trạng thái: placeholder "Chọn trạng thái" + allowClear, bỏ option "Tất cả" (mirror banks — bổ sung theo yêu cầu user). Parse OK.
