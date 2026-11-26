# Feature Scaffolder — ERP TPE

## Mục đích
Tạo bộ khung (scaffold) cho feature mới theo đúng pattern và cấu trúc module của project.

## Khi nào dùng
- Bắt đầu feature mới cần tạo nhiều file (CRUD, list screen, API...)
- Thêm entity/model mới vào module có sẵn

## Input cần thiết
Trước khi scaffold, cần xác nhận:
1. **Module**: Assign / Human / Timesheet / Payroll / ...
2. **Tên entity**: VD: `HandoverItem`, `BomList`
3. **Loại feature**: CRUD đầy đủ / List screen / API only
4. **Có phân quyền theo cấp không?** (Hỏi user nếu chưa rõ)
5. **Điều kiện xóa** (`is_can_delete`): Hỏi user trước khi viết

## Danh sách file cần tạo

### Backend (trong `Modules/[Module]/`)

| File | Đường dẫn | Mô tả |
|------|-----------|-------|
| Migration | `database/migrations/YYYY_MM_DD_HHMMSS_create_[table]_table.php` | Hoặc đặt ở `database/migrations/` gốc |
| Entity/Model | `Entities/[Entity].php` | Extends `BaseModel` |
| Controller | `Http/Controllers/Api/V1/[Entity]Controller.php` | Extends `BaseApiController` |
| Service | `Services/[Entity]Service.php` | Extends `BaseService` |
| Request | `Http/Requests/[Entity]/[Entity]Request.php` | Validation rules |
| List Resource | `Transformers/[Entity]Resource/[Entity]ListResource.php` | Cho danh sách |
| Detail Resource | `Transformers/[Entity]Resource/Detail[Entity]Resource.php` | Cho chi tiết |
| Routes | `Routes/api.php` | Thêm routes vào file có sẵn |

### Frontend (trong repo hrm-thanhan-client)

| File | Đường dẫn | Mô tả |
|------|-----------|-------|
| List page | `pages/[module]/[entity]/index.vue` | Base* components + filter |
| Detail/Form page | `pages/[module]/[entity]/_id.vue` hoặc `add.vue` | Form CRUD |
| Menu item | `components/menu-sidebar.js` | Thêm vào nhóm phù hợp |

## Pattern bắt buộc

### BE — Thêm quyền (permission) mới — CHỈ sửa seeder, KHÔNG viết migration

Mọi quyền khai tập trung ở **một file duy nhất**:
`hrm-thanhan-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`

- Thêm 1 dòng `Permission::create([...])` **cuối hàm `run()`**, **id cố định = id lớn nhất hiện có + 1**
  (grep `'id' => 5` trong file để lấy id cuối). Không để auto-increment.
- Model là `App\Models\Permission` (không phải `Spatie\Permission\Models\Permission`).
- Đủ 6 trường, `name` = `display_name`:
  ```php
  // 26/11/2026 — Phân hệ Kho (type 16) - Nhập kho: <quyền dùng để làm gì> (<Class::HANG_SO dùng nó>)
  Permission::create(['id' => 533, 'guard_name' => 'api', 'name' => 'Nhập thông tin phiếu nhập kho', 'display_name' => 'Nhập thông tin phiếu nhập kho', 'group' => 'Nhập kho', 'type' => 16]);
  ```
- `group` = nhóm hiển thị trên màn phân quyền; `type` = phân hệ — lấy theo các dòng cùng phân hệ đã có
  (vd Chấm công 1 · Cung ứng 7 · Hợp đồng 8 · Kho 16). Không rõ thì hỏi user.
- Comment phía trên: ngày + phân hệ + quyền dùng để làm gì.
- Đổi tên quyền → sửa thẳng dòng trong seeder (giữ nguyên `id`), đồng thời sửa hằng tên quyền trong code BE.

**KHÔNG làm:**
- ❌ Migration `DB::table('permissions')->insert(...)` / `Permission::create` / đổi tên quyền trong migration
  (đã từng phải xoá ở `de-xuat-cung-ung-khach-le`, `duyet-ket-xuat-hop-dong-cung-ung`, `phieu-nhap-kho`).
- ❌ Seeder riêng cho từng module (`XxxPermissionSeeder`) — chỉ một nguồn là `PermissionsTableSeeder`.
- ❌ Tự gán quyền cho vai trò trong code — user tự gán trên màn phân quyền.

**Áp dụng lên DB** (seeder `truncate` bảng `permissions` rồi tạo lại theo id cố định, nên quyền đã gán cho vai trò vẫn giữ):
```bash
php artisan db:seed --class="Modules\Timesheet\Database\Seeders\PermissionsTableSeeder"
```
→ Ghi lệnh này vào checkpoint `plan.md` ("Bước tiếp theo") + nhắc user gán quyền mới cho vai trò.

### BE — Controller
```php
class EntityController extends BaseApiController
{
    protected $entityService;

    public function __construct(EntityService $service)
    {
        $this->entityService = $service;
    }

    public function index(Request $request)
    {
        $data = $this->entityService->index($request);
        return EntityListResource::collection($data);
    }

    public function store(EntityRequest $request)
    {
        $entity = $this->entityService->store($request);
        return $this->responseJson('success', Response::HTTP_OK, new DetailEntityResource($entity));
    }
}
```

### BE — Service
```php
class EntityService extends BaseService
{
    public function index(Request $request)
    {
        $query = Entity::query();
        // Filter, sort, paginate
        return $query->paginate($request->per_page ?? 20);
    }
}
```

### FE — List page
```vue
<style lang="scss">
@import '@/assets/scss/custom.scss';
</style>
```
- Dùng `<b-button v-b-toggle>` + `<b-collapse>` cho bộ lọc
- Cascading filter: Công ty >> Phòng ban >> Bộ phận
- API qua `this.$store.dispatch('apiGetMethod', ...)`

### FE — Quy tắc input/dropdown (bắt buộc mọi màn)
- **KHÔNG dùng `<input>` / `<select>` native.** Luôn dùng base component tương ứng:
  - Dropdown/select (form, bộ lọc, popup/modal) → `base-select2`; options `{ id, text }`, placeholder qua prop, cho xóa chọn bằng `:settings="{ allowClear: true }"`
  - Ô nhập / tìm kiếm → `b-form-input` (Bootstrap-Vue); field form có label/đơn vị → `base-input-field`
- Khi `allowClear` clear giá trị, v-model trả về `null` → guard filter phải dùng truthy, không so sánh `''`
- Label field bắt buộc dùng component `<Required />` (sao đỏ), không viết `*` trần

## Tham khảo chi tiết
- Pattern CRUD đầy đủ: `docs/conventions.md`
- Base classes & components: `docs/shared.md`
- Màn danh sách: `.skills/list-page/SKILL.md`
- Import Excel: `.skills/import-excel/SKILL.md`

## Quy tắc
- Hỏi user trước khi thêm phân quyền theo cấp
- Hỏi user điều kiện `is_can_delete` cụ thể
- Không sửa hàm dùng chung khi chưa confirm
- Tạo plan.md trước khi code
