# Conventions — Pattern CRUD đầy đủ

## Backend

### Routes

```php
Route::group(['prefix' => '/some-feature'], function () {
    Route::get('/', [SomeController::class, 'index']);
    Route::get('/getAll', [SomeController::class, 'getAll']);
    // Route static PHẢI đặt TRƯỚC route wildcard
    Route::get('/import-template', [SomeController::class, 'importTemplate']);
    Route::post('/', [SomeController::class, 'store'])->middleware('checkPermission:Tên quyền');
    Route::get('/{someModel}', [SomeController::class, 'show']);
    Route::put('/{someModel}', [SomeController::class, 'update'])->middleware('checkPermission:Tên quyền');
    Route::delete('/{someModel}', [SomeController::class, 'destroy'])->middleware('checkPermission:Tên quyền');
});
```

**Quy tắc route:**
- Implicit model binding — `{someModel}` tự resolve sang Model
- `checkPermission` chỉ áp cho store/update/destroy — KHÔNG áp cho index/show
- Route static (`/import-template`) PHẢI đặt TRƯỚC route wildcard (`/{someModel}`)

---

### Controller

```php
use App\Http\Controllers\ApiController;
use Illuminate\Support\Facades\DB;
use Illuminate\Http\Response;
use Exception;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

class SomeController extends ApiController
{
    protected $someService;

    public function __construct(SomeService $someService)
    {
        $this->someService = $someService;
    }

    public function index(Request $request)
    {
        try {
            $result = $this->someService->index($request);
            return $this->apiGetList(SomeResource::apiPaginate($result, $request));
        } catch (Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    // store/update/destroy — PHẢI wrap DB::transaction
    // Connection khác default: DB::connection('mysql_tpe')->transaction(...)
    public function store(SomeStoreRequest $request)
    {
        try {
            return DB::transaction(function () use ($request) {
                $result = $this->someService->store($request);
                return $this->responseJson('success', Response::HTTP_OK, $result);
            });
        } catch (Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function show(SomeModel $someModel)
    {
        try {
            return $this->responseJson('success', Response::HTTP_OK, new DetailSomeResource($someModel));
        } catch (Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function destroy(SomeModel $someModel)
    {
        try {
            return DB::transaction(function () use ($someModel) {
                $result = $this->someService->destroy($someModel);
                return $this->responseJson('success', Response::HTTP_OK, $result);
            });
        } catch (Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }
}
```

---

### Service

```php
use Modules\Training\Services\BaseService;

class SomeService extends BaseService
{
    public function index($request)
    {
        return SomeModel::query()
            ->when($request->keyword, function ($query) use ($request) {
                $query->where('name', 'LIKE', '%' . $request->keyword . '%');
            })
            ->when($request->status, function ($query) use ($request) {
                $query->where('status', $request->status);
            })
            ->when($request->created_at_start, function ($query) use ($request) {
                $query->where('created_at', '>=', $request->created_at_start);
            })
            ->when($request->created_at_end, function ($query) use ($request) {
                $query->where('created_at', '<=', $request->created_at_end);
            })
            ->when($request->employee_id, function ($query) use ($request) {
                $query->whereHas('someRelation', function ($q) use ($request) {
                    $q->where('employee_id', $request->employee_id);
                });
            })
            ->orderBy($request->sort_by ?? 'id', toBoolean($request->sort_desc) ? 'desc' : 'asc');
        // KHÔNG paginate() ở đây — Resource::apiPaginate xử lý
    }

    public function store($request)
    {
        // 1. Tạo bản ghi chính
        $result = SomeModel::create([
            'status' => 1,
            'code' => SomeModel::getNextCode(),
        ]);

        // 2. Bulk insert bản ghi con — KHÔNG dùng create() trong vòng lặp
        $dataInsert = [];
        foreach ($request->items as $item) {
            $dataInsert[] = [
                'parent_id' => $result->id,
                'field' => $item['field'],
                'created_at' => now()->format('Y-m-d H:i:s'),  // insert() không tự thêm
                'updated_at' => now()->format('Y-m-d H:i:s'),
            ];
        }
        collect($dataInsert)->chunk(1000)->map(function ($chunk) {
            ChildModel::insert($chunk->toArray());
        });

        // 3. Dispatch job bất đồng bộ nếu cần
        SomeJob::dispatch($param1, $param2);

        return $result;
    }

    public function destroy(SomeModel $model)
    {
        // Xóa con trước — rồi mới xóa cha
        $model->childRelation()->delete();
        $model->delete();
        return true;
    }

    // Logic phụ → tách thành private method
    private function saveHistory($model) { ... }
    private function sendNotification($model) { ... }
}
```

---

### Request

```php
use Modules\Training\Http\Requests\BaseRequest;
use Illuminate\Validation\Validator;

class SomeRequest extends BaseRequest
{
    public function rules()
    {
        return [
            'field_required' => ['required', 'string'],
            // Validation có điều kiện — dùng ternary
            'conditional_field' => request()->type == 1 ? ['required', 'array', 'min:1'] : [],
            'conditional_field.*.id' => request()->type == 1 ? ['required', 'integer'] : [],
        ];
    }

    // Custom validation phức tạp → dùng withValidator
    public function withValidator(Validator $validator)
    {
        $validator->after(function ($validator) {
            if (request()->type == 2 && !request()->sub_type) {
                $validator->errors()->add('sub_type', 'Bắt buộc phải chọn');
            }
        });
    }
}
```

---

### Model

```php
use App\Models\BaseModel;
use Illuminate\Database\Eloquent\SoftDeletes;

class SomeModel extends BaseModel
{
    use SoftDeletes;

    protected $guarded = [];

    // Constants trạng thái — luôn định nghĩa đủ const + STATUSES (id, name, color)
    const STATUS_TAO_NHAP  = 1;
    const STATUS_CHO_DUYET = 3;
    const STATUS_DA_DUYET  = 5;

    public const STATUSES = [
        ['id' => self::STATUS_TAO_NHAP,  'name' => 'Nháp',      'color' => '#64748B'],
        ['id' => self::STATUS_CHO_DUYET, 'name' => 'Chờ duyệt', 'color' => '#D97706'],
        ['id' => self::STATUS_DA_DUYET,  'name' => 'Đã duyệt',  'color' => '#16A34A'],
    ];

    public function children()
    {
        return $this->hasMany(ChildModel::class);
    }

    // PHẢI hỏi user điều kiện cụ thể trước khi viết accessor này
    public function getIsCanDeleteAttribute()
    {
        // Điều kiện tuỳ nghiệp vụ từng màn — không tự quyết định
    }
}
```

---

### Resource / Transformer

```php
use Modules\Human\Helper\Helper;
use Modules\Human\Transformers\ApiResource;

// List Resource (cho index)
class SomeResource extends ApiResource
{
    public function toArray($request): array
    {
        return [
            'id'              => $this->id,
            'code'            => $this->code,
            'created_at'      => Helper::formatDate($this->created_at),
            'created_by_name' => $this->employee_create_name,
            'is_can_delete'   => $this->is_can_delete,
        ];
    }
}

// Detail Resource (cho show) — LUÔN tách file riêng
class DetailSomeResource extends ApiResource
{
    public function toArray($request): array
    {
        return [
            'id'    => $this->id,
            'items' => $this->children->map(function ($item) {
                return [
                    'id'          => $item->id,
                    'name'        => $item->name,
                    'parent_name' => $item->parentRelation->name,
                ];
            }),
        ];
    }
}
```

---

### Migration

```php
// Luôn viết comment cho mỗi trường
$table->unsignedBigInteger('employee_id')->comment('ID nhân viên phụ trách');
$table->tinyInteger('status')->default(1)->comment('1: nháp, 3: chờ duyệt, 5: đã duyệt');

// KHÔNG khai báo foreign key constraint — chỉ dùng integer column
// FK ngầm định qua tên field
```

---

### Quy tắc tổng hợp Backend

- `store/update/destroy` — luôn wrap `DB::transaction()`
- Bulk insert — dùng `Model::insert()` + `chunk(1000)`, set `created_at/updated_at` thủ công
- Constants trạng thái — đủ `const` riêng lẻ + mảng `STATUSES` với `id`, `name`, `color`
- Xóa dữ liệu — xóa con trước, xóa cha sau
- External API — dùng `GuzzleHttp\Client`, tác vụ nặng → dispatch Job
- `$guarded = []` cho mọi Model
- Resource — luôn tách 2 file: list và detail
- Không dùng `$request->validate()` cho import — dùng check thủ công

---

## Frontend

### Pattern trang danh sách

```vue
<template>
  <div class="v2-styles">
    <V2BaseFilterPanel
      :collapsed="filterCollapsed"
      :quickSearchValue="filters.keyword"
      @search="handleSearch"
      @reset="handleReset"
    >
      <template #advanced-filters>
        <!-- V2BaseSelect, V2BaseDatePicker -->
      </template>
    </V2BaseFilterPanel>

    <V2BaseDataTable
      :data="tableData"
      :columns="tableColumns"
      :pagination="pagination"
      :loading="loading"
      @sort="handleSort"
      @page-change="handlePageChange"
    >
      <template #cell-columnKey="{ item }">
        <!-- Custom cell render -->
      </template>
    </V2BaseDataTable>
  </div>
</template>

<script>
import { buildQuery } from '@/utils/url-action'

export default {
  data() {
    return {
      filters: {
        keyword: undefined,
        status: undefined,
        sort_field: 'created_at',
        sort_dir: 'desc',
      },
      tableData: [],
      loading: false,
      // snake_case để gán trực tiếp this.pagination = meta
      pagination: {
        current_page: 1,
        per_page: 20,
        total: 0,
        last_page: 1,
        from: 0,
        to: 0,
      },
    }
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        const apiFilters = {
          ...this.filters,
          page: this.pagination.current_page,
          per_page: this.pagination.per_page,
        }
        const { data, meta } = await this.$store.dispatch(
          'apiGetMethod',
          `assign/endpoint${buildQuery(apiFilters)}`
        )
        this.tableData = data || []
        this.pagination = meta // gán trực tiếp, không map từng field
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
```

---

### Quy tắc Frontend

- Mỗi page tạo `constants.js` riêng — dùng const thay vì số trực tiếp (1, 2, 3...)
- Luôn dùng `dayjs` từ `@/utils/plugins/dayjs.js` — không tự viết date util
- Pagination khai báo snake_case để gán trực tiếp `this.pagination = meta`
- Option V2BaseSelect — kiểm tra file cùng thư mục: `{ id, text }` hay `{ id, name }`
- Import `@/assets/scss/v2-styles.scss` cho các trang v2
- Tuân thủ style list của module đang triển khai
- Dùng `async/await` cho mọi API dispatch
