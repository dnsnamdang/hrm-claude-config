---
name: feature-scaffolder
description: Scaffold cấu trúc file cho feature mới (BE + FE)
---

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
| Controller | `Http/Controllers/Api/V1/[Entity]Controller.php` | Extends `ApiController` |
| Service | `Services/[Entity]Service.php` | Extends `BaseService` |
| Request | `Http/Requests/[Entity]/[Entity]Request.php` | Validation rules |
| List Resource | `Transformers/[Entity]Resource/[Entity]ListResource.php` | Cho danh sách |
| Detail Resource | `Transformers/[Entity]Resource/Detail[Entity]Resource.php` | Cho chi tiết |
| Routes | `Routes/api.php` | Thêm routes vào file có sẵn |

### Frontend (trong repo hrm-client)

| File | Đường dẫn | Mô tả |
|------|-----------|-------|
| List page | `pages/[module]/[entity]/index.vue` | V2Base components + filter |
| Detail/Form page | `pages/[module]/[entity]/_id.vue` hoặc `add.vue` | Form CRUD |
| Menu item | `components/menu-sidebar.js` | Thêm vào nhóm phù hợp |

## Pattern bắt buộc

### BE — Controller
```php
class EntityController extends ApiController
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
@import '@/assets/scss/v2-styles.scss';
</style>
```
- Dùng `V2BaseFilterPanel` cho bộ lọc
- Cascading filter: Công ty >> Phòng ban >> Bộ phận
- API qua `this.$store.dispatch('apiGetMethod', ...)`

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
