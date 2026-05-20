# Từ chối phân công dự toán — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thêm chức năng "Từ chối phân công" trên màn dự toán — khi status = DA_DUYET (2), người có quyền phân công có thể từ chối → nhập lý do → dự toán chuyển sang HUY_DU_TOAN (17), trạng thái cuối cùng.

**Architecture:** Tạo API endpoint riêng `reject-assignment`, thêm 3 cột DB mới (lý do, người, thời gian), thêm nút + modal trên cả trang danh sách và chi tiết. Follow pattern `approve-transfer-contract` đã có.

**Tech Stack:** Laravel 8 (PHP 7.4), Nuxt 2 (Vue 2), Bootstrap-Vue, MySQL

**Spec:** `docs/superpowers/specs/2026-05-20-reject-assignment-design.md`

---

### Task 1: Migration — Thêm 3 cột vào bảng `projects`

**Files:**
- Create: `hrm-thanhan-api/database/migrations/2026_05_20_100000_add_reject_assignment_to_projects_table.php`

- [x] **Step 1: Tạo migration file**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddRejectAssignmentToProjectsTable extends Migration
{
    public function up()
    {
        Schema::table('projects', function (Blueprint $table) {
            $table->text('reason_reject_assignment')->nullable()->after('contract_manager_id');
            $table->unsignedBigInteger('rejected_by')->nullable()->after('reason_reject_assignment');
            $table->timestamp('rejected_at')->nullable()->after('rejected_by');
        });
    }

    public function down()
    {
        Schema::table('projects', function (Blueprint $table) {
            $table->dropColumn(['reason_reject_assignment', 'rejected_by', 'rejected_at']);
        });
    }
}
```

- [x] **Step 2: Chạy migration**

Run: `php artisan migrate`

Expected: Migration chạy thành công, 3 cột mới xuất hiện trong bảng `projects`.

---

### Task 2: Model — Thêm constant, fillable, method vào `Project.php`

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Entities/Project/Project.php:83-84` (thêm constant), `:65-66` (thêm fillable), `:138` (thêm method)

- [x] **Step 1: Thêm constant `HUY_DU_TOAN = 17`**

Tại dòng 83, sau `const DANG_LAP_HOP_DONG = 16;`, thêm:

```php
    const HUY_DU_TOAN = 17;
```

- [x] **Step 2: Thêm 3 cột vào `$fillable`**

Tại dòng 65, sau `'contract_manager_id',`, thêm:

```php
        'reason_reject_assignment',
        'rejected_by',
        'rejected_at',
```

- [x] **Step 3: Thêm method `canRejectAssignment()`**

Tại dòng 138 (sau method `canAssign()`), thêm:

```php
    public function canRejectAssignment()
    {
        return $this->status == self::DA_DUYET
            && isCurrentEmployeeHasPermission('Phân công báo giá');
    }
```

---

### Task 3: Route — Thêm endpoint reject-assignment

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Routes/api.php:244`

- [x] **Step 1: Thêm route**

Tại dòng 244, sau `Route::put('/{project}/assign-employee-create-contract', ...);`, thêm:

```php
        Route::put('/{project}/reject-assignment', [ProjectController::class, 'rejectAssignment']);
```

---

### Task 4: Controller — Thêm method `rejectAssignment`

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/ProjectController.php:255` (trước method `detailReport`)

- [x] **Step 1: Thêm method `rejectAssignment()`**

Tại dòng 255 (sau method `assignEmployeeCreateContract`, trước method `detailReport`), thêm:

```php
    public function rejectAssignment(Request $request, Project $project)
    {
        $request->validate([
            'reason' => 'required|string|max:1000',
        ]);

        if (!$project->canRejectAssignment()) {
            return $this->responseJson('Không có quyền!', Response::HTTP_FORBIDDEN);
        }

        DB::beginTransaction();
        try {
            $project->status = Project::HUY_DU_TOAN;
            $project->reason_reject_assignment = $request->reason;
            $project->rejected_by = auth()->user()->id;
            $project->rejected_at = Carbon::now();
            $project->save();

            DB::commit();
            return $this->responseJson('success', Response::HTTP_OK);
        } catch (Exception $e) {
            DB::rollBack();
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }
```

---

### Task 5: Resource — Cập nhật ProjectResource + DetailProjectResource

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Transformers/ProjectResource/ProjectResource.php:101`
- Modify: `hrm-thanhan-api/Modules/Category/Transformers/ProjectResource/DetailProjectResource.php:115-117`

- [x] **Step 1: Cập nhật `ProjectResource.php` (danh sách)**

Tại dòng 101, sau `'can_assign' => $this->canAssign(),`, thêm:

```php
            'can_reject_assignment' => $this->canRejectAssignment(),
```

- [x] **Step 2: Cập nhật `DetailProjectResource.php` (chi tiết)**

Tại dòng 115, sau `'can_assign' => $this->canAssign(),`, thêm:

```php
            'can_reject_assignment' => $this->canRejectAssignment(),
            'reason_reject_assignment' => $this->reason_reject_assignment,
            'rejected_by_name' => $this->rejected_by
                ? (\Modules\Human\Entities\Employee::find($this->rejected_by)->info->fullname ?? '')
                : '',
            'rejected_at' => $this->rejected_at
                ? Carbon::parse($this->rejected_at)->format('d/m/Y H:i')
                : null,
```

---

### Task 6: StatusMap — Cập nhật detailReport + getProjectsByField

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/ProjectController.php:353-354`

- [x] **Step 1: Cập nhật statusMap trong `detailReport()`**

Tại dòng 353, thay:

```php
            16 => 'Đang lập hợp đồng',
        ];
```

Thành:

```php
            16 => 'Đang lập hợp đồng',
            17 => 'Hủy dự toán',
        ];
```

- [x] **Step 2: Kiểm tra `getProjectsByField()` có statusMap không**

Method `getProjectsByField()` (dòng 166) không có statusMap riêng — nó trả trực tiếp `'status' => $data->status` (dòng 204) dưới dạng số. FE đã tự format bằng `getStatusText()`. Không cần sửa BE ở đây.

---

### Task 7: Verify Backend — Test API bằng tay

- [x] **Step 1: Kiểm tra API hoạt động**

Dùng Postman hoặc curl test:

```
PUT /api/v1/category/projects/{id}/reject-assignment
Authorization: Bearer {token}
Content-Type: application/json
Body: { "reason": "Test từ chối phân công" }
```

Với `{id}` là một project có status = 2 (DA_DUYET).

Expected: Response 200, project status chuyển thành 17.

- [x] **Step 2: Test validation — reason trống**

```
PUT /api/v1/category/projects/{id}/reject-assignment
Body: {}
```

Expected: Response 422, error "The reason field is required."

- [x] **Step 3: Test quyền — project status != 2**

Dùng project có status != 2.

Expected: Response 403, "Không có quyền!"

---

### Task 8: Frontend danh sách — Thêm status mới

**Files:**
- Modify: `hrm-thanhan-client/pages/sale/project/index.vue`

- [x] **Step 1: Thêm vào `statusOptions` (dòng 578)**

Tại dòng 578, sau `{ id: 15, text: 'Chờ BGĐ duyệt chuyển HĐ' },`, thêm:

```js
                {
                    id: 17,
                    text: 'Hủy dự toán',
                },
```

- [x] **Step 2: Thêm vào `statusColorMap` (dòng 651)**

Tại dòng 651, sau `16: 'status-pill pj-status-cyan', // Đang lập hợp đồng`, thêm:

```js
                17: 'status-pill pj-status-red', // Hủy dự toán
```

- [x] **Step 3: Thêm vào `getStatusText()` (dòng 905)**

Tại dòng 905, sau `} else if (item.status == 16) { return 'Đang lập hợp đồng' }`, thêm:

```js
            } else if (item.status == 17) {
                return 'Hủy dự toán'
            }
```

---

### Task 9: Frontend danh sách — Nút + Modal từ chối

**Files:**
- Modify: `hrm-thanhan-client/pages/sale/project/index.vue`

- [x] **Step 1: Thêm nút trong cột actions (dòng 220)**

Tại dòng 220, sau nút Phân công (sau `</b-button>` kết thúc nút assign), thêm:

```html
                                        <b-button
                                            v-if="item.can_reject_assignment"
                                            @click="showRejectModal(item.id)"
                                            variant="secondary"
                                            class="btn-small"
                                            v-b-tooltip.hover.top="'Từ chối phân công'"
                                        >
                                            <i class="fas fa-times text-danger"></i>
                                        </b-button>
```

- [x] **Step 2: Thêm modal (dòng 315)**

Tại dòng 315, trước `<confirm-delete-selected`, thêm:

```html
        <b-modal id="modal-reject-assignment" title="Từ chối phân công" @ok="handleRejectAssignment">
            <b-form-group label="Lý do từ chối *">
                <b-form-textarea v-model="rejectReason" rows="3" />
            </b-form-group>
            <div v-if="rejectError" class="text-danger">{{ rejectError }}</div>
        </b-modal>
```

- [x] **Step 3: Thêm data (dòng 584)**

Tại dòng 584, sau `debounceDelay: 400,`, thêm:

```js
            rejectReason: '',
            rejectError: '',
            rejectId: undefined,
```

- [x] **Step 4: Thêm methods (dòng 907)**

Tại dòng 907, sau method `getStatusText()`, thêm:

```js
        showRejectModal(id) {
            this.rejectId = id
            this.rejectReason = ''
            this.rejectError = ''
            this.$bvModal.show('modal-reject-assignment')
        },

        async handleRejectAssignment(bvModalEvent) {
            if (!this.rejectReason) {
                bvModalEvent.preventDefault()
                this.rejectError = 'Vui lòng nhập lý do từ chối'
                return
            }
            try {
                this.$nuxt.$loading.start()
                await this.$store.dispatch('apiPutMethod', {
                    url: `category/projects/${this.rejectId}/reject-assignment`,
                    payload: { reason: this.rejectReason },
                })
                this.$nuxt.$loading.finish()
                this.$toasted.global.success({ message: 'Đã từ chối phân công' })
                this.getData()
            } catch (e) {
                this.$nuxt.$loading.finish()
                this.$toasted.global.error({
                    message: e?.response?.data?.message || 'Thao tác thất bại',
                })
            }
        },
```

---

### Task 10: Frontend chi tiết — Nút + Modal + Hiển thị lý do

**Files:**
- Modify: `hrm-thanhan-client/pages/sale/project/_id/index.vue`

- [x] **Step 1: Thêm modal từ chối (dòng 17)**

Tại dòng 17, sau `</b-modal>` (kết thúc modal-reject-transfer), thêm:

```html
            <b-modal id="modal-reject-assignment" title="Từ chối phân công" @ok="handleRejectAssignment">
                <b-form-group label="Lý do từ chối *">
                    <b-form-textarea v-model="rejectAssignmentReason" rows="3" />
                </b-form-group>
                <div v-if="rejectAssignmentError" class="text-danger">{{ rejectAssignmentError }}</div>
            </b-modal>
```

- [x] **Step 2: Thêm alert hiển thị thông tin từ chối (dòng 10)**

Tại dòng 10, sau `</div>` (kết thúc div row mt-1), trước `<b-modal id="modal-reject-transfer"`, thêm:

```html
            <div v-if="formSubmit.status == 17" class="alert alert-danger mt-2 mx-3">
                <strong>Dự toán đã bị hủy</strong><br />
                <span>Lý do: {{ formSubmit.reason_reject_assignment }}</span><br />
                <span>Người từ chối: {{ formSubmit.rejected_by_name }}</span><br />
                <span>Thời gian: {{ formSubmit.rejected_at }}</span>
            </div>
```

- [x] **Step 3: Thêm nút Từ chối phân công trong footer (dòng 29)**

Tại dòng 29, sau nút "Phân công" (sau `</button>` kết thúc nút Phân công), thêm:

```html
                            <button
                                class="btn btn-danger equal-width"
                                v-if="formSubmit.can_reject_assignment"
                                @click="$bvModal.show('modal-reject-assignment')"
                            >
                                Từ chối phân công
                            </button>
```

- [x] **Step 4: Thêm data (dòng 86)**

Tại dòng 86, sau `rejectError: '',`, thêm:

```js
            rejectAssignmentReason: '',
            rejectAssignmentError: '',
```

- [x] **Step 5: Thêm method (dòng 162)**

Tại dòng 162, sau method `handleRejectTransfer()`, thêm:

```js
        async handleRejectAssignment(bvModalEvent) {
            if (!this.rejectAssignmentReason) {
                bvModalEvent.preventDefault()
                this.rejectAssignmentError = 'Vui lòng nhập lý do từ chối'
                return
            }
            try {
                this.$nuxt.$loading.start()
                await this.$store.dispatch('apiPutMethod', {
                    url: `category/projects/${this.$route.params.id}/reject-assignment`,
                    payload: { reason: this.rejectAssignmentReason },
                })
                this.$nuxt.$loading.finish()
                this.$toasted.global.success({ message: 'Đã từ chối phân công' })
                this.$router.push('/sale/project')
            } catch (e) {
                this.$nuxt.$loading.finish()
                this.$toasted.global.error({
                    message: e?.response?.data?.message || 'Thao tác thất bại',
                })
            }
        },
```

---

### Task 11: Verify Frontend — Test trên trình duyệt

- [x] **Step 1: Test trang danh sách**

1. Mở `/sale/project`
2. Tìm dự toán có status = 2 (Chờ phân công)
3. Verify nút "Từ chối phân công" (icon X đỏ) hiện trong cột Hành động
4. Click nút → modal hiện ra với textarea "Lý do từ chối"
5. Click OK khi chưa nhập → hiện lỗi "Vui lòng nhập lý do từ chối"
6. Nhập lý do → click OK → toast "Đã từ chối phân công"
7. Dự toán chuyển sang status "Hủy dự toán" (màu đỏ)
8. Nút Từ chối biến mất (vì can_reject_assignment = false)

- [x] **Step 2: Test filter status**

1. Mở bộ lọc → chọn "Hủy dự toán" → verify chỉ hiện dự toán status = 17

- [x] **Step 3: Test trang chi tiết**

1. Mở chi tiết dự toán status = 2
2. Verify nút "Từ chối phân công" hiện ở footer cạnh "Phân công"
3. Click → modal → nhập lý do → OK → redirect về danh sách
4. Mở lại chi tiết dự toán vừa hủy → verify alert đỏ hiện lý do, người, thời gian
5. Verify không có nút action nào (phân công, từ chối, etc.)

- [x] **Step 4: Test edge case — race condition**

1. Mở 2 tab chi tiết cùng 1 dự toán status = 2
2. Tab 1: phân công nhân viên → thành công
3. Tab 2: click từ chối → phải nhận lỗi 403 "Không có quyền"
