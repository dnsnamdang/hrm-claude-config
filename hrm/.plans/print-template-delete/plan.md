# Xóa mềm mẫu in (chưa dùng & không phải mẫu hệ thống) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Cho phép xóa mềm mẫu in tại màn `decision/category/print_templates`, chỉ với mẫu chưa được dùng ở 9 bảng dữ liệu và không nằm trong danh sách mẫu hệ thống (`PROTECTED_CODES`); nút Xóa chỉ hiện khi mẫu được phép xóa.

**Architecture:** Backend (Laravel, module Human) thêm cột `status` cho soft-delete, tính sẵn cờ `can_delete` cho từng dòng ở API list (check 9 bảng theo lô để tránh N+1), và validate lại khi xóa. Frontend (Nuxt/Vue + BootstrapVue) hiện nút Xóa theo `item.can_delete`, gọi `DELETE` và hiển thị thông báo lỗi theo message backend.

**Tech Stack:** PHP 8 / Laravel (nwidart modules), MySQL, Vue 2 / Nuxt / BootstrapVue, Vuex (`apiGet`/`apiDelete`).

**Spec:** `docs/superpowers/specs/2026-06-02-print-template-delete-design.md`

---

## Quy ước thực thi (đọc trước)

- **Không có hạ tầng test tự động** trong dự án (chỉ `tests/*/ExampleTest.php`, không factory, không `RefreshDatabase`). Verify theo cách dự án dùng: `php artisan tinker` cho logic backend, và thao tác UI/Network cho frontend. Mỗi snippet tinker dưới đây là một kiểm chứng cụ thể, không phải placeholder.
- **Lệnh chạy ở thư mục** `D:\laragon\www\hrm\hrm-api` (backend) hoặc `D:\laragon\www\hrm\hrm-client` (frontend). Dùng PowerShell.
- Trước khi bắt đầu, đảm bảo có ít nhất vài bản ghi `print_templates` trong DB dev để thử (màn Tạo mới đã có sẵn).

---

## File Structure

**Backend (`hrm-api`):**
- Create: `database/migrations/2026_06_02_000000_add_status_to_print_templates_table.php` — thêm cột `status`.
- Modify: `Modules/Human/Entities/PrintTemplate.php` — `$fillable` + hằng `PROTECTED_CODES`.
- Modify: `Modules/Human/Services/PrintTemplateService.php` — lọc status, tính `can_delete`, `getUsedTemplateIds`, `isPrintTemplateInUse`, `deletePrintTemplate`.
- Modify: `Modules/Human/Http/Controllers/Api/V1/PrintTemplateController.php` — method `delete($id)`.
- Modify: `Modules/Human/Transformers/PrintTemplateVariable/PrintTemplateResource.php` — trả `status` + `can_delete`.
- (Route `Modules/Human/Routes/api.php:377` đã trỏ `delete` — **không sửa**.)

**Frontend (`hrm-client`):**
- Modify: `pages/decision/category/print_templates/index.vue` — nút Xóa `v-if="item.can_delete"`, đọc message lỗi, dọn code chết.

---

## Task 1: Migration thêm cột `status` vào `print_templates`

**Files:**
- Create: `hrm-api/database/migrations/2026_06_02_000000_add_status_to_print_templates_table.php`

- [x] **Step 1: Tạo file migration**

Tạo `hrm-api/database/migrations/2026_06_02_000000_add_status_to_print_templates_table.php`:

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddStatusToPrintTemplatesTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::table('print_templates', function (Blueprint $table) {
            $table->unsignedTinyInteger('status')->default(1)->after('type')
                ->comment('1: hoạt động, 0: đã xóa mềm');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::table('print_templates', function (Blueprint $table) {
            $table->dropColumn('status');
        });
    }
}
```

- [x] **Step 2: Chạy migration**

Run (trong `D:\laragon\www\hrm\hrm-api`):
```
php artisan migrate
```
Expected: dòng `Migrating: 2026_06_02_000000_add_status_to_print_templates_table` rồi `Migrated:`.

- [x] **Step 3: Checkpoint — xác minh cột tồn tại và giá trị mặc định**

Run:
```
php artisan tinker --execute="echo Schema::hasColumn('print_templates','status') ? 'HAS' : 'NO'; echo PHP_EOL; echo \Modules\Human\Entities\PrintTemplate::query()->whereNull('status')->count();"
```
Expected: in ra `HAS` và `0` (mọi bản ghi cũ đã có `status = 1` theo default, không null).

---

## Task 2: Entity — `$fillable` + hằng `PROTECTED_CODES`

**Files:**
- Modify: `hrm-api/Modules/Human/Entities/PrintTemplate.php`

- [x] **Step 1: Thêm hằng `PROTECTED_CODES` và `status` vào `$fillable`**

Trong `PrintTemplate.php`, thay khối hằng + `$fillable` hiện tại:

```php
    public const TYPES = [
        [
            'id' => 1,
            'name' => 'Hợp đồng lao động',
        ],
    ];

    protected $table = 'print_templates';

    protected $fillable = [
        'code',
        'name',
        'type',
        'template',
    ];
```

thành:

```php
    public const TYPES = [
        [
            'id' => 1,
            'name' => 'Hợp đồng lao động',
        ],
    ];

    /**
     * Các mã mẫu in được code tra cứu theo `code` (hardcode) — là mẫu hệ thống,
     * KHÔNG được phép xóa. Bổ sung danh sách này khi thêm chỗ dùng PrintTemplate::where('code', ...).
     */
    public const PROTECTED_CODES = [
        'BIEN_BAN_CUOC_HOP',                            // Modules/Assign/.../MeetingController — in biên bản họp
        'HOP_DONG_DAO_TAO',                             // Modules/Decision/Jobs/CreateTrainingContractJob
        'PHU_LUC_HOP_DONG_LAO_DONG',                    // IncreaseSeniorityService, AppendixLaborContractService
        'QUYET_DINH_DIEU_CHINH_LUONG',                  // Seeder
        'HOP_DONG_LAO_DONG_CHINH_THUC_KHONG_THOI_HAN',  // Seeder
    ];

    protected $table = 'print_templates';

    protected $fillable = [
        'code',
        'name',
        'type',
        'status',
        'template',
    ];
```

- [x] **Step 2: Checkpoint — hằng đọc được, fillable nhận `status`**

Run:
```
php artisan tinker --execute="echo implode(',', \Modules\Human\Entities\PrintTemplate::PROTECTED_CODES); echo PHP_EOL; echo in_array('status', (new \Modules\Human\Entities\PrintTemplate)->getFillable()) ? 'FILLABLE_OK' : 'MISSING';"
```
Expected: in 5 code, xuống dòng, rồi `FILLABLE_OK`.

---

## Task 3: Service — lọc status, tính `can_delete`, và logic xóa

**Files:**
- Modify: `hrm-api/Modules/Human/Services/PrintTemplateService.php`

- [x] **Step 1: Lọc list theo `status = 1` và bọc nhóm điều kiện keyword**

Trong `getPrintTemplates()`, thay khối build query (từ `$query = $this->_model;` đến hết phần `paginate`) bằng:

```php
        $query = $this->_model->newQuery()->where('status', 1);
        if (!empty($request->get('keyword'))) {
            $keyword = $request->get('keyword');
            $query->where(function ($q) use ($keyword) {
                $q->where('code', 'like', '%' . $keyword . '%')
                    ->orWhere('name', 'like', '%' . $keyword . '%');
            });
        }
        if (!empty($request->get('type'))) {
            $query->where('type', $request->get('type'));
        }
        if (!empty($request->get('created_by'))) {
            $query->where('created_by', $request->get('created_by'));
        }
        if (!empty($request->get('updated_by'))) {
            $query->where('updated_by', $request->get('updated_by'));
        }

        $printTemplates = $query->select(['print_templates.*'])
            ->orderBy($sortBy, $sortDesc)
            ->paginate($limit);

        $this->attachCanDelete($printTemplates);

        return $printTemplates;
```

> Lý do bọc closure cho keyword: trước đây `where(code)->orWhere(name)` đứng cạnh `where(status)` sẽ thành `status AND (code) OR (name)` sai logic. Bọc nhóm đảm bảo `status = 1 AND (code LIKE OR name LIKE)`.

- [x] **Step 2: Thêm 3 method mới vào cuối class (trước dấu `}` đóng class, thay luôn khối comment `deleteCompanyAccountBank` đã bị comment)**

Thêm vào `PrintTemplateService` (đặt sau `getPrintTemplateById()`):

```php
    /**
     * Gán cờ can_delete cho từng dòng trong trang hiện tại (tránh N+1).
     *
     * @param \Illuminate\Pagination\LengthAwarePaginator $printTemplates
     * @return void
     */
    private function attachCanDelete($printTemplates): void
    {
        $ids = $printTemplates->getCollection()->pluck('id')->all();
        $usedIds = $this->getUsedTemplateIds($ids);

        $printTemplates->getCollection()->transform(function ($item) use ($usedIds) {
            $item->can_delete = !in_array($item->code, PrintTemplate::PROTECTED_CODES, true)
                && !in_array($item->id, $usedIds, true);
            return $item;
        });
    }

    /**
     * Map các bảng tham chiếu mẫu in => cột khóa.
     *
     * @return array
     */
    private function referencingTables(): array
    {
        return [
            'decisions' => 'print_template_id',
            'department_establishments' => 'print_template_id',
            'department_dissolutions' => 'print_template_id',
            'trouble_shooting_reports' => 'print_template_id',
            'decision_labor_contracts' => 'print_template_id',
            'appendix_labor_contracts' => 'print_template_id',
            'training_contracts' => 'print_template_id',
            'self_notifications' => 'print_template_id',
            'suspend_labor_contracts' => 'print_template_agreement_id',
        ];
    }

    /**
     * Lấy tập id mẫu in đang được tham chiếu trong các id truyền vào (check theo lô).
     *
     * @param array $ids
     * @return array
     */
    public function getUsedTemplateIds(array $ids): array
    {
        if (empty($ids)) {
            return [];
        }

        $used = [];
        foreach ($this->referencingTables() as $table => $column) {
            $found = DB::table($table)
                ->whereIn($column, $ids)
                ->whereNotNull($column)
                ->distinct()
                ->pluck($column)
                ->all();
            $used = array_merge($used, $found);
        }

        return array_values(array_unique(array_map('intval', $used)));
    }

    /**
     * Kiểm tra một mẫu in có đang được sử dụng ở bất kỳ bảng nào không.
     *
     * @param int $id
     * @return bool
     */
    public function isPrintTemplateInUse(int $id): bool
    {
        foreach ($this->referencingTables() as $table => $column) {
            if (DB::table($table)->where($column, $id)->exists()) {
                return true;
            }
        }
        return false;
    }

    /**
     * Xóa mềm mẫu in nếu hợp lệ.
     * Trả về mảng: ['status' => 'ok'|'not_found'|'protected'|'in_use'].
     *
     * @param int $id
     * @return array
     */
    public function deletePrintTemplate(int $id): array
    {
        $printTemplate = $this->_model->where('status', 1)->find($id);
        if (!$printTemplate) {
            return ['status' => 'not_found'];
        }
        if (in_array($printTemplate->code, PrintTemplate::PROTECTED_CODES, true)) {
            return ['status' => 'protected'];
        }
        if ($this->isPrintTemplateInUse($id)) {
            return ['status' => 'in_use'];
        }

        $printTemplate->fill(['status' => 0])->save();

        return ['status' => 'ok'];
    }
```

> `DB` và `PrintTemplate` đã được `use` sẵn ở đầu file (`use Illuminate\Support\Facades\DB;`, `use Modules\Human\Entities\PrintTemplate;`). Nếu khối comment `deleteCompanyAccountBank` còn đó thì xóa luôn cho sạch.

- [x] **Step 3: Checkpoint — can_delete & isPrintTemplateInUse đúng**

Lấy 1 id mẫu hệ thống (theo code) và 1 id mẫu thường chưa dùng để kiểm chứng:

```
php artisan tinker --execute="$s=app(\Modules\Human\Services\PrintTemplateService::class); $p=\Modules\Human\Entities\PrintTemplate::where('code','BIEN_BAN_CUOC_HOP')->first(); echo $p ? ('protected_in_use='.var_export($s->isPrintTemplateInUse($p->id),true).' will_block(by code)') : 'no BIEN_BAN_CUOC_HOP row'; echo PHP_EOL; echo 'usedIds_sample='.json_encode($s->getUsedTemplateIds(\Modules\Human\Entities\PrintTemplate::query()->limit(20)->pluck('id')->all()));"
```
Expected: chạy không lỗi; in ra trạng thái và một mảng `usedIds_sample` (có thể rỗng `[]` nếu DB dev chưa có quyết định nào dùng mẫu — vẫn hợp lệ).

---

## Task 4: Controller — method `delete($id)`

**Files:**
- Modify: `hrm-api/Modules/Human/Http/Controllers/Api/V1/PrintTemplateController.php`

- [x] **Step 1: Thay method `destroy()` rỗng bằng `delete($id)`**

Thay khối:

```php
    /**
     * Remove the specified resource from storage.
     * @param int $id
     * @return Renderable
     */
    public function destroy($id)
    {
        //
    }
```

bằng:

```php
    /**
     * Xóa mềm mẫu in (chỉ khi chưa được sử dụng và không phải mẫu hệ thống).
     * @param int $id
     * @return Renderable
     */
    public function delete($id)
    {
        $result = $this->printTemplateService->deletePrintTemplate((int) $id);

        switch ($result['status']) {
            case 'not_found':
                return $this->responseJson('Không tìm thấy mẫu in', Response::HTTP_NOT_FOUND);
            case 'protected':
                return $this->responseJson('Mẫu in hệ thống, không thể xóa', Response::HTTP_BAD_REQUEST);
            case 'in_use':
                return $this->responseJson('Mẫu in đang được sử dụng, không thể xóa', Response::HTTP_BAD_REQUEST);
            default:
                return $this->responseJson('success', Response::HTTP_OK);
        }
    }
```

> `Response` đã được `use Illuminate\Http\Response;` ở đầu file. Route `Modules/Human/Routes/api.php:377` đã trỏ `[PrintTemplateController::class, 'delete']` — không cần sửa.

- [x] **Step 2: Checkpoint — gọi thử endpoint logic qua service đã ở Task 3.** Xác minh route map đúng:

Run:
```
php artisan route:list --path=human/print-templates
```
Expected: có dòng `DELETE  human/print-templates/{id}` trỏ tới `PrintTemplateController@delete`.

---

## Task 5: Resource — trả `status` + `can_delete`

**Files:**
- Modify: `hrm-api/Modules/Human/Transformers/PrintTemplateVariable/PrintTemplateResource.php`

- [x] **Step 1: Thêm 2 field vào mỗi dòng**

Trong `toArray()`, thay khối `$printTemplateData[] = [ ... ];` bằng:

```php
            $printTemplateData[] = [
                'stt' => ($page - 1) * $limit + 1 + $index,
                'id' => $data->id,
                'code' => $data->code,
                'name' => $data->name,
                'type' => PrintTemplateVariable::TYPES[$data->type],
                'status' => (int) $data->status,
                'can_delete' => (bool) ($data->can_delete ?? false),
                'created_at' => Helper::formatDate($data->created_at),
                'updated_at' => Helper::formatDate($data->updated_at),
                'created_by' => $data->employee_create ? $data->employee_create->info->fullname : null,
                'updated_by' => $data->employee_update ? $data->employee_update->info->fullname : null,
            ];
```

- [x] **Step 2: Checkpoint — API list trả `can_delete`**

Đảm bảo backend đang chạy (Laragon). Gọi list bằng tinker để khỏi cần token:

```
php artisan tinker --execute="$svc=app(\Modules\Human\Services\PrintTemplateService::class); $req=new \Illuminate\Http\Request(['page'=>1,'limit'=>5]); $res=$svc->getPrintTemplates($req); foreach($res->getCollection() as $r){ echo $r->id.' code='.$r->code.' can_delete='.var_export($r->can_delete,true).PHP_EOL; }"
```
Expected: in mỗi dòng kèm `can_delete=true/false`; dòng có `code` thuộc `PROTECTED_CODES` phải là `false`.

---

## Task 6: Frontend — nút Xóa theo `can_delete` + thông báo lỗi

**Files:**
- Modify: `hrm-client/pages/decision/category/print_templates/index.vue`

- [x] **Step 1: Đổi điều kiện hiển thị nút Xóa**

Thay khối dropdown item Xóa:

```vue
                                            <b-dropdown-item
                                                v-if="item.status"
                                                @click="delete_id = item.id"
                                                v-b-modal.modal-delete-selected
                                            >
                                                <i class="fa fa-angle-right"></i> Xóa
                                            </b-dropdown-item>
```

bằng:

```vue
                                            <b-dropdown-item
                                                v-if="item.can_delete"
                                                @click="delete_id = item.id"
                                                v-b-modal.modal-delete-selected
                                            >
                                                <i class="fa fa-angle-right"></i> Xóa
                                            </b-dropdown-item>
```

- [x] **Step 2: Đọc message lỗi từ backend trong `deleteReportTemplate`**

Thay method `deleteReportTemplate()` bằng:

```js
        async deleteReportTemplate() {
            this.$bvModal.hide('modal-delete-selected')
            await this.$store
                .dispatch('apiDelete', `human/print-templates/${this.delete_id}`)
                .then((response) => {
                    this.getReportTemplates()
                    this.$toasted.global.success({
                        message: 'Xoá mẫu in thành công',
                    })
                })
                .catch((error) => {
                    this.$toasted.global.error({
                        message: error.response?.data?.message || 'Xoá mẫu in thất bại',
                    })
                })
        },
```

- [x] **Step 3: Dọn code chết liên quan `status`**

Trong cùng file, xóa 2 dòng tham chiếu method không tồn tại (trong template, cell `status`):

```vue
                                <template v-slot:cell(status)="{ item }">
                                    <span :class="getStatusClass(item)"> {{ getStatusText(item) }} </span>
                                </template>
```
→ Xóa hẳn khối `<template v-slot:cell(status)>` này (cột `status` không nằm trong `fields` nên không hiển thị; khối này chỉ gọi `getStatusClass`/`getStatusText` không tồn tại).

> Không cần sửa `data().filter`/`fields`. Cột `status` không có trong `fields` nên không render. Giữ nguyên phần còn lại.

- [x] **Step 4: Checkpoint — kiểm thử UI**

Khởi động frontend nếu chưa chạy (trong `D:\laragon\www\hrm\hrm-client`): `npm run dev` (hoặc môi trường dev sẵn có của dự án).

Mở màn `Quản lý mẫu in` (`/decision/category/print_templates`) và xác minh:
1. Mẫu thường chưa dùng → có nút **Xóa** trong dropdown ⚙.
2. Mẫu hệ thống (vd `BIEN_BAN_CUOC_HOP`) hoặc mẫu đã dùng → **không** có nút Xóa.
3. Bấm Xóa một mẫu hợp lệ → modal xác nhận → toast "Xoá mẫu in thành công", mẫu biến mất khỏi list (đã set `status=0`).
4. (Tùy chọn) Mô phỏng chặn: tạm gọi DELETE tới id mẫu hệ thống bằng DevTools/Network và xác nhận nhận message "Mẫu in hệ thống, không thể xóa".

---

## Self-Review (đã rà khi viết plan)

- **Spec coverage:** Migration `status` (Task 1) ✓; `PROTECTED_CODES` + fillable (Task 2) ✓; lọc status + `getUsedTemplateIds` (lô) + `isPrintTemplateInUse` + `deletePrintTemplate` (Task 3) ✓; controller `delete` 4 nhánh trạng thái (Task 4) ✓; Resource `status` + `can_delete` (Task 5) ✓; frontend `v-if="item.can_delete"` + message lỗi + dọn code chết (Task 6) ✓. Lớp 1 (9 bảng) + Lớp 2 (PROTECTED_CODES) đều phủ.
- **Type consistency:** `deletePrintTemplate` trả `['status' => ...]` với các giá trị `not_found|protected|in_use|ok` — controller switch khớp đúng 4 nhánh. `getUsedTemplateIds(array): array`, `isPrintTemplateInUse(int): bool`, `attachCanDelete` private — tên dùng nhất quán giữa các task. Field `can_delete` (snake_case) nhất quán backend↔frontend.
- **Placeholder scan:** không có TBD/TODO; mọi step có code/lệnh cụ thể.
- **Caveat đã ghi trong spec** (unique `code` khi tạo lại; phải bảo trì `PROTECTED_CODES`) — nằm ngoài phạm vi code task, không cần task riêng.
