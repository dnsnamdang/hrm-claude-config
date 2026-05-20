# Đính kèm file cho người thân — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Cho phép upload/xóa file đính kèm (tối đa 5 file, mọi định dạng) cho từng thành viên gia đình trong Thông tin nhân sự, hỗ trợ cả flow edit trực tiếp và flow yêu cầu cập nhật.

**Architecture:** Tạo bảng riêng `employee_relationship_attachments` (1 row = 1 file) + bảng tạm tương ứng. Tái sử dụng endpoint upload S3 hiện có (`FileController::uploadImage`). FE hiển thị danh sách file ngay trong hàng người thân.

**Tech Stack:** Laravel 8 (PHP 7.4), Nuxt 2 (Vue 2), Bootstrap-Vue, MySQL, AWS S3

---

## File Structure

| Action | File | Mô tả |
|--------|------|-------|
| Create | `Modules/Human/Database/Migrations/2026_05_20_000001_create_employee_relationship_attachments_table.php` | Migration bảng chính |
| Create | `Modules/Human/Database/Migrations/2026_05_20_000002_create_employee_relationship_attachment_tmps_table.php` | Migration bảng tạm |
| Create | `Modules/Human/Entities/EmployeeRelationshipAttachment.php` | Model bảng chính |
| Create | `Modules/Human/Entities/EmployeeRelationshipAttachmentTmp.php` | Model bảng tạm |
| Modify | `Modules/Human/Entities/EmployeeRelationship.php:42` | Thêm `attachments()` relationship |
| Modify | `Modules/Human/Entities/EmployeeRelationshipTmp.php:22` | Thêm `attachmentTmps()` relationship |
| Modify | `Modules/Human/Services/EmployeeInfoService.php:1,238,542` | Import model, eager load, sync attachments |
| Modify | `Modules/Human/Services/EmployeeInfoUpdateRequestService.php:1,225,577,627,778,798` | Import model, eager load, sync/add attachment tmps, approve flow map |
| Modify | `components/human-components/employee_info/EmployeeInfoForm.vue:1079,2136,2964,3059` | UI file list, data init, methods, submit |

---

### Task 1: Migration — Bảng `employee_relationship_attachments`

**Files:**
- Create: `hrm-thanhan-api/Modules/Human/Database/Migrations/2026_05_20_000001_create_employee_relationship_attachments_table.php`

- [x] **Step 1: Tạo file migration**

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateEmployeeRelationshipAttachmentsTable extends Migration
{
    public function up()
    {
        Schema::create('employee_relationship_attachments', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('employee_relationship_id');
            $table->string('file_url', 500);
            $table->string('file_name', 255);
            $table->unsignedInteger('file_size')->nullable();
            $table->timestamps();

            $table->index('employee_relationship_id', 'idx_rel_attach_relationship_id');
            $table->foreign('employee_relationship_id', 'fk_rel_attach_relationship')
                  ->references('id')->on('employee_relationships')->onDelete('cascade');
        });
    }

    public function down()
    {
        Schema::dropIfExists('employee_relationship_attachments');
    }
}
```

- [ ] **Step 2: Chạy migration**

```bash
cd hrm-thanhan-api
php artisan migrate
```

Expected: `Migrating: 2026_05_20_000001_create_employee_relationship_attachments_table` + `Migrated` success.

---

### Task 2: Migration — Bảng `employee_relationship_attachment_tmps`

**Files:**
- Create: `hrm-thanhan-api/Modules/Human/Database/Migrations/2026_05_20_000002_create_employee_relationship_attachment_tmps_table.php`

- [ ] **Step 1: Tạo file migration**

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateEmployeeRelationshipAttachmentTmpsTable extends Migration
{
    public function up()
    {
        Schema::create('employee_relationship_attachment_tmps', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('employee_relationship_tmp_id');
            $table->unsignedBigInteger('employee_relationship_attachment_id')->nullable();
            $table->string('file_url', 500);
            $table->string('file_name', 255);
            $table->unsignedInteger('file_size')->nullable();
            $table->timestamps();

            $table->index('employee_relationship_tmp_id', 'idx_rel_attach_tmp_rel_tmp_id');
            $table->foreign('employee_relationship_tmp_id', 'fk_rel_attach_tmp_relationship')
                  ->references('id')->on('employee_relationship_tmps')->onDelete('cascade');
        });
    }

    public function down()
    {
        Schema::dropIfExists('employee_relationship_attachment_tmps');
    }
}
```

- [ ] **Step 2: Chạy migration**

```bash
cd hrm-thanhan-api
php artisan migrate
```

Expected: `Migrating: 2026_05_20_000002_create_employee_relationship_attachment_tmps_table` + `Migrated` success.

---

### Task 3: Model — `EmployeeRelationshipAttachment`

**Files:**
- Create: `hrm-thanhan-api/Modules/Human/Entities/EmployeeRelationshipAttachment.php`
- Modify: `hrm-thanhan-api/Modules/Human/Entities/EmployeeRelationship.php:42`

- [ ] **Step 1: Tạo model `EmployeeRelationshipAttachment`**

```php
<?php

namespace Modules\Human\Entities;

use Illuminate\Database\Eloquent\Model;

class EmployeeRelationshipAttachment extends Model
{
    protected $table = 'employee_relationship_attachments';

    protected $fillable = [
        'employee_relationship_id',
        'file_url',
        'file_name',
        'file_size',
    ];

    public function relationship()
    {
        return $this->belongsTo(EmployeeRelationship::class, 'employee_relationship_id');
    }
}
```

- [ ] **Step 2: Thêm `attachments()` vào `EmployeeRelationship`**

Mở file `hrm-thanhan-api/Modules/Human/Entities/EmployeeRelationship.php`. Thêm method sau đây **trước dấu `}` cuối file** (sau dòng 42):

```php
    public function attachments()
    {
        return $this->hasMany(EmployeeRelationshipAttachment::class, 'employee_relationship_id');
    }
```

---

### Task 4: Model — `EmployeeRelationshipAttachmentTmp`

**Files:**
- Create: `hrm-thanhan-api/Modules/Human/Entities/EmployeeRelationshipAttachmentTmp.php`
- Modify: `hrm-thanhan-api/Modules/Human/Entities/EmployeeRelationshipTmp.php:22`

- [ ] **Step 1: Tạo model `EmployeeRelationshipAttachmentTmp`**

```php
<?php

namespace Modules\Human\Entities;

use Illuminate\Database\Eloquent\Model;

class EmployeeRelationshipAttachmentTmp extends Model
{
    protected $table = 'employee_relationship_attachment_tmps';

    protected $fillable = [
        'employee_relationship_tmp_id',
        'employee_relationship_attachment_id',
        'file_url',
        'file_name',
        'file_size',
    ];

    public function relationshipTmp()
    {
        return $this->belongsTo(EmployeeRelationshipTmp::class, 'employee_relationship_tmp_id');
    }
}
```

- [ ] **Step 2: Thêm `attachmentTmps()` vào `EmployeeRelationshipTmp`**

Mở file `hrm-thanhan-api/Modules/Human/Entities/EmployeeRelationshipTmp.php`. Thêm method sau đây **trước method `getDirty()`** (trước dòng 24):

```php
    public function attachmentTmps()
    {
        return $this->hasMany(EmployeeRelationshipAttachmentTmp::class, 'employee_relationship_tmp_id');
    }
```

---

### Task 5: Service — Cập nhật `EmployeeInfoService` (load + sync)

**Files:**
- Modify: `hrm-thanhan-api/Modules/Human/Services/EmployeeInfoService.php`

- [ ] **Step 1: Thêm import model**

Mở file `EmployeeInfoService.php`. Thêm dòng import sau vào nhóm `use` đầu file (sau dòng 18 — `use Modules\Human\Entities\EmployeeRelationship;`):

```php
use Modules\Human\Entities\EmployeeRelationshipAttachment;
```

- [ ] **Step 2: Cập nhật eager load khi lấy thông tin nhân viên**

Tìm dòng 238-240 (query lấy relationships):

```php
        $employeeRelationships = EmployeeRelationship::select('id', 'name', 'birthday', 'relation', 'job', 'address', 'phone_number', 'is_dependent', 'dependent_start_date', 'dependent_end_date')
            ->where('employee_info_id', $employeeInfo->id)
            ->get();
```

Thay bằng:

```php
        $employeeRelationships = EmployeeRelationship::select('id', 'name', 'birthday', 'relation', 'job', 'address', 'phone_number', 'is_dependent', 'dependent_start_date', 'dependent_end_date')
            ->where('employee_info_id', $employeeInfo->id)
            ->with('attachments:id,employee_relationship_id,file_url,file_name,file_size')
            ->get();
```

- [ ] **Step 3: Cập nhật `syncEmployeeRelationships()` để sync attachments**

Tìm method `syncEmployeeRelationships` (dòng 517-544). Thay toàn bộ method bằng:

```php
    private function syncEmployeeRelationships($employeeInfoId, $relationships)
    {
        $existIds = array_filter(array_column($relationships, 'id'));

        // Xóa records ko trong data tạo/sửa (cascade sẽ xóa attachments)
        EmployeeRelationship::where('employee_info_id', $employeeInfoId)->whereNotIn('id', $existIds)->delete();

        foreach ($relationships as $relationship) {
            if (!empty($relationship['id'])) {
                $employeeRelationship = EmployeeRelationship::find($relationship['id']);
            } else {
                $employeeRelationship = new EmployeeRelationship();
            }

            $employeeRelationship->employee_info_id = $employeeInfoId;
            $employeeRelationship->name = $relationship['name'];
            $employeeRelationship->birthday = $relationship['birthday'];
            $employeeRelationship->relation = $relationship['relation'];
            $employeeRelationship->job = $relationship['job'] ?? null;
            $employeeRelationship->phone_number = $relationship['phone_number'] ?? null;
            $employeeRelationship->address = $relationship['address'] ?? null;
            $employeeRelationship->is_dependent = !empty($relationship['is_dependent']);
            $employeeRelationship->dependent_start_date = $relationship['dependent_start_date'] ?? null;
            $employeeRelationship->dependent_end_date = $relationship['dependent_end_date'] ?? null;

            $employeeRelationship->save();

            if (isset($relationship['attachments'])) {
                $this->syncRelationshipAttachments($employeeRelationship->id, $relationship['attachments']);
            }
        }
    }
```

- [ ] **Step 4: Thêm method `syncRelationshipAttachments()`**

Thêm method mới ngay **sau** method `syncEmployeeRelationships()`:

```php
    private function syncRelationshipAttachments($relationshipId, $attachments)
    {
        if (count($attachments) > 5) {
            $attachments = array_slice($attachments, 0, 5);
        }

        $existIds = array_filter(array_column($attachments, 'id'));

        EmployeeRelationshipAttachment::where('employee_relationship_id', $relationshipId)
            ->whereNotIn('id', $existIds)
            ->delete();

        foreach ($attachments as $attachment) {
            if (!empty($attachment['id'])) {
                continue;
            }

            $newAttachment = new EmployeeRelationshipAttachment();
            $newAttachment->employee_relationship_id = $relationshipId;
            $newAttachment->file_url = $attachment['file_url'];
            $newAttachment->file_name = $attachment['file_name'];
            $newAttachment->file_size = $attachment['file_size'] ?? null;
            $newAttachment->save();
        }
    }
```

- [ ] **Step 5: Verify — kiểm tra file không có lỗi cú pháp**

```bash
cd hrm-thanhan-api
php artisan tinker --execute="echo 'OK';"
```

Expected: `OK` (không có syntax error)

---

### Task 6: Service — Cập nhật `EmployeeInfoUpdateRequestService` (load + sync + add + approve)

**Files:**
- Modify: `hrm-thanhan-api/Modules/Human/Services/EmployeeInfoUpdateRequestService.php`

- [ ] **Step 1: Thêm import model**

Thêm 2 dòng import vào nhóm `use` đầu file (sau dòng 22 — `use Modules\Human\Entities\EmployeeRelationshipTmp;`):

```php
use Modules\Human\Entities\EmployeeRelationshipAttachment;
use Modules\Human\Entities\EmployeeRelationshipAttachmentTmp;
```

- [ ] **Step 2: Cập nhật eager load khi lấy update request**

Tìm dòng 225-227 (query lấy relationships tmp):

```php
        $employeeRelationships = EmployeeRelationshipTmp::select('id', 'name', 'birthday', 'relation', 'job', 'address', 'phone_number', 'employee_relationship_id')
            ->where('employee_update_request_id', $employeeInfo->id)
            ->get();
```

Thay bằng:

```php
        $employeeRelationships = EmployeeRelationshipTmp::select('id', 'name', 'birthday', 'relation', 'job', 'address', 'phone_number', 'employee_relationship_id')
            ->where('employee_update_request_id', $employeeInfo->id)
            ->with('attachmentTmps:id,employee_relationship_tmp_id,employee_relationship_attachment_id,file_url,file_name,file_size')
            ->get();
```

- [ ] **Step 3: Cập nhật approve flow — map attachments từ tmp sang chính**

Tìm dòng 579-584 (block `foreach` map relationships):

```php
                        foreach ($dataEmployee['relationships'] as &$relationship) {
                            if (!empty($relationship['employee_relationship_id']))
                                $relationship['id'] = $relationship['employee_relationship_id'];
                            else
                                $relationship['id'] = null;
                        }
```

Thay bằng:

```php
                        foreach ($dataEmployee['relationships'] as &$relationship) {
                            if (!empty($relationship['employee_relationship_id']))
                                $relationship['id'] = $relationship['employee_relationship_id'];
                            else
                                $relationship['id'] = null;

                            if (!empty($relationship['attachment_tmps'])) {
                                $relationship['attachments'] = array_map(function ($att) {
                                    return [
                                        'id' => $att['employee_relationship_attachment_id'] ?? null,
                                        'file_url' => $att['file_url'],
                                        'file_name' => $att['file_name'],
                                        'file_size' => $att['file_size'] ?? null,
                                    ];
                                }, $relationship['attachment_tmps']);
                            } else {
                                $relationship['attachments'] = [];
                            }
                        }
```

- [ ] **Step 4: Cập nhật `syncEmployeeRelationships()` — thêm sync attachment tmps**

Tìm method `syncEmployeeRelationships` (dòng 753-780). Thay toàn bộ method bằng:

```php
    private function syncEmployeeRelationships($employeeInfoUpdateRequestId, $employeeInfoId, $relationships)
    {
        $existIds = array_filter(array_column($relationships, 'id'));

        // Xóa records ko trong data tạo/sửa (cascade sẽ xóa attachment tmps)
        EmployeeRelationshipTmp::where('employee_update_request_id', $employeeInfoUpdateRequestId)->whereNotIn('id', $existIds)->delete();

        foreach ($relationships as $relationship) {
            if (!empty($relationship['id'])) {
                $employeeRelationship = EmployeeRelationshipTmp::find($relationship['id']);
                $employeeRelationship->employee_relationship_id = $employeeRelationship['employee_relationship_id'];
            } else {
                $employeeRelationship = new EmployeeRelationshipTmp();
                $employeeRelationship->employee_relationship_id = null;
            }

            $employeeRelationship->employee_update_request_id = $employeeInfoUpdateRequestId;
            $employeeRelationship->employee_info_id = $employeeInfoId;
            $employeeRelationship->name = $relationship['name'];
            $employeeRelationship->birthday = $relationship['birthday'];
            $employeeRelationship->relation = $relationship['relation'];
            $employeeRelationship->job = $relationship['job'] ?? null;
            $employeeRelationship->phone_number = $relationship['phone_number'] ?? null;
            $employeeRelationship->address = $relationship['address'] ?? null;

            $employeeRelationship->save();

            if (isset($relationship['attachments'])) {
                $this->syncRelationshipAttachmentTmps($employeeRelationship->id, $relationship['attachments']);
            }
        }
    }
```

- [ ] **Step 5: Cập nhật `addEmployeeRelationships()` — thêm add attachment tmps**

Tìm method `addEmployeeRelationships` (dòng 782-801). Thay toàn bộ method bằng:

```php
    private function addEmployeeRelationships($employeeInfoUpdateRequestId, $employeeInfoId, $relationships)
    {
        foreach ($relationships as $relationship) {
            $employeeRelationship = new EmployeeRelationshipTmp();
            if (!empty($relationship['id']))
                $employeeRelationship->employee_relationship_id = $relationship['id'];
            else
                $employeeRelationship->employee_relationship_id = null;

            $employeeRelationship->employee_update_request_id = $employeeInfoUpdateRequestId;
            $employeeRelationship->employee_info_id = $employeeInfoId;
            $employeeRelationship->name = $relationship['name'];
            $employeeRelationship->birthday = $relationship['birthday'];
            $employeeRelationship->relation = $relationship['relation'];
            $employeeRelationship->job = $relationship['job'] ?? null;
            $employeeRelationship->phone_number = $relationship['phone_number'] ?? null;
            $employeeRelationship->address = $relationship['address'] ?? null;

            $employeeRelationship->save();

            if (isset($relationship['attachments'])) {
                $this->addRelationshipAttachmentTmps($employeeRelationship->id, $relationship['attachments']);
            }
        }
    }
```

- [ ] **Step 6: Thêm 2 method mới `syncRelationshipAttachmentTmps()` + `addRelationshipAttachmentTmps()`**

Thêm 2 method ngay **sau** method `addEmployeeRelationships()`:

```php
    private function syncRelationshipAttachmentTmps($relationshipTmpId, $attachments)
    {
        if (count($attachments) > 5) {
            $attachments = array_slice($attachments, 0, 5);
        }

        $existIds = array_filter(array_column($attachments, 'id'));

        EmployeeRelationshipAttachmentTmp::where('employee_relationship_tmp_id', $relationshipTmpId)
            ->whereNotIn('id', $existIds)
            ->delete();

        foreach ($attachments as $attachment) {
            if (!empty($attachment['id'])) {
                continue;
            }

            $newAttachment = new EmployeeRelationshipAttachmentTmp();
            $newAttachment->employee_relationship_tmp_id = $relationshipTmpId;
            $newAttachment->employee_relationship_attachment_id = $attachment['employee_relationship_attachment_id'] ?? null;
            $newAttachment->file_url = $attachment['file_url'];
            $newAttachment->file_name = $attachment['file_name'];
            $newAttachment->file_size = $attachment['file_size'] ?? null;
            $newAttachment->save();
        }
    }

    private function addRelationshipAttachmentTmps($relationshipTmpId, $attachments)
    {
        if (count($attachments) > 5) {
            $attachments = array_slice($attachments, 0, 5);
        }

        foreach ($attachments as $attachment) {
            $newAttachment = new EmployeeRelationshipAttachmentTmp();
            $newAttachment->employee_relationship_tmp_id = $relationshipTmpId;
            $newAttachment->employee_relationship_attachment_id = $attachment['id'] ?? null;
            $newAttachment->file_url = $attachment['file_url'];
            $newAttachment->file_name = $attachment['file_name'];
            $newAttachment->file_size = $attachment['file_size'] ?? null;
            $newAttachment->save();
        }
    }
```

- [ ] **Step 7: Verify — kiểm tra file không có lỗi cú pháp**

```bash
cd hrm-thanhan-api
php artisan tinker --execute="echo 'OK';"
```

Expected: `OK`

---

### Task 7: Frontend — Data init + methods

**Files:**
- Modify: `hrm-thanhan-client/components/human-components/employee_info/EmployeeInfoForm.vue`

- [ ] **Step 1: Cập nhật data init — thêm `attachments` vào default relationship**

Tìm dòng 2136-2149 (data `relationships`):

```js
            // Thông tin gia đình
            relationships: [
                {
                    name: null,
                    birthday: null,
                    job: null,
                    phone_number: null,
                    address: null,
                    relation: 0,
                    is_dependent: false,
                    dependent_start_date: null,
                    dependent_end_date: null,
                },
            ],
```

Thay bằng:

```js
            // Thông tin gia đình
            relationships: [
                {
                    name: null,
                    birthday: null,
                    job: null,
                    phone_number: null,
                    address: null,
                    relation: 0,
                    is_dependent: false,
                    dependent_start_date: null,
                    dependent_end_date: null,
                    attachments: [],
                },
            ],
```

- [ ] **Step 2: Cập nhật `addRelationship()` — thêm `attachments` vào object mới**

Tìm dòng 2964-2975 (method `addRelationship`):

```js
        addRelationship() {
            this.relationships.push({
                name: null,
                birthday: null,
                job: null,
                phone_number: null,
                address: null,
                relation: 0,
                is_dependent: false,
                dependent_start_date: null,
                dependent_end_date: null,
            })
        },
```

Thay bằng:

```js
        addRelationship() {
            this.relationships.push({
                name: null,
                birthday: null,
                job: null,
                phone_number: null,
                address: null,
                relation: 0,
                is_dependent: false,
                dependent_start_date: null,
                dependent_end_date: null,
                attachments: [],
            })
        },
```

- [ ] **Step 3: Cập nhật load data — đảm bảo attachments được map**

Tìm dòng 2353-2355 (load relationships từ response):

```js
                if (this.form.relationships.length) {
                    this.relationships = this.form.relationships
                }
```

Thay bằng:

```js
                if (this.form.relationships.length) {
                    this.relationships = this.form.relationships.map(r => ({
                        ...r,
                        attachments: (r.attachments || r.attachment_tmps || []).map(a => ({
                            id: a.id,
                            file_url: a.file_url,
                            file_name: a.file_name,
                            file_size: a.file_size,
                            employee_relationship_attachment_id: a.employee_relationship_attachment_id || null,
                        })),
                    }))
                }
```

- [ ] **Step 4: Thêm method upload file cho relationship**

Thêm method mới sau `removeRelationship(index)` (sau dòng 2978):

```js
        onRelationshipFileChange(event, index) {
            let files = event.target.files
            if (!files.length) return

            let currentCount = this.relationships[index].attachments.length
            let remainingSlots = 5 - currentCount
            if (remainingSlots <= 0) {
                this.$toasted.global.error({ message: 'Tối đa 5 file cho mỗi người thân' })
                event.target.value = ''
                return
            }

            let filesToUpload = Array.from(files).slice(0, remainingSlots)
            if (files.length > remainingSlots) {
                this.$toasted.global.error({ message: `Chỉ upload được ${remainingSlots} file nữa` })
            }

            let fileInfos = filesToUpload.map(f => ({ name: f.name, size: f.size }))

            this.uploadImage(filesToUpload).then((response) => {
                for (let i = 0; i < response.length; i++) {
                    this.relationships[index].attachments.push({
                        id: null,
                        file_url: response[i],
                        file_name: fileInfos[i].name,
                        file_size: fileInfos[i].size,
                    })
                }
                this.$forceUpdate()
            })

            event.target.value = ''
        },
        removeRelationshipAttachment(relIndex, attIndex) {
            this.relationships[relIndex].attachments.splice(attIndex, 1)
            this.$forceUpdate()
        },
        formatFileSize(bytes) {
            if (!bytes) return ''
            if (bytes < 1024) return bytes + ' B'
            if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
            return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
        },
```

- [ ] **Step 5: Cập nhật submit form — đảm bảo attachments được gửi kèm**

Tìm dòng 3059-3061 (filter relationships trước submit):

```js
            this.form.relationships = this.relationships.filter(function (relationship) {
                return relationship.name != null && relationship.name != ''
            })
```

Thay bằng:

```js
            this.form.relationships = this.relationships.filter(function (relationship) {
                return relationship.name != null && relationship.name != ''
            }).map(function (r) {
                return {
                    ...r,
                    attachments: (r.attachments || []).map(function (a) {
                        return {
                            id: a.id || null,
                            file_url: a.file_url,
                            file_name: a.file_name,
                            file_size: a.file_size,
                            employee_relationship_attachment_id: a.employee_relationship_attachment_id || null,
                        }
                    })
                }
            })
```

---

### Task 8: Frontend — UI bảng gia đình

**Files:**
- Modify: `hrm-thanhan-client/components/human-components/employee_info/EmployeeInfoForm.vue`

- [ ] **Step 1: Thêm hàng file đính kèm sau mỗi hàng người thân**

Tìm dòng 1079-1198 — block `<tr v-for="(relationship, index) of relationships">` hiện tại. Đây là 1 `<tr>` duy nhất. Cần wrap thành `<template>` và thêm `<tr>` thứ 2 cho attachments.

Thay toàn bộ block:

```html
                                                <tr v-for="(relationship, index) of relationships" :key="index">
```

... (từ dòng 1079 đến thẻ đóng `</tr>` ở dòng 1198)

Bằng:

```html
                                                <template v-for="(relationship, index) of relationships">
                                                <tr :key="'rel-' + index">
                                                    <th scope="row">{{ index + 1 }}</th>
                                                    <td>
                                                        <input
                                                            class="form-control"
                                                            type="text"
                                                            v-model="relationships[index].name"
                                                            placeholder="Nhập họ tên"
                                                        />
                                                    </td>
                                                    <td>
                                                        <date-picker
                                                            v-model="relationships[index].birthday"
                                                            type="date"
                                                            format="DD/MM/YYYY"
                                                            value-type="YYYY-MM-DD"
                                                            placeholder="dd/mm/yyyy"
                                                        ></date-picker>

                                                        <span
                                                            v-if="!relationships[index].birthday"
                                                            class="field-required"
                                                            >{{
                                                                formError['relationships.' + index + '.birthday']
                                                            }}</span
                                                        >
                                                    </td>
                                                    <td>
                                                        <input
                                                            class="form-control"
                                                            type="text"
                                                            v-model="relationships[index].job"
                                                            placeholder="Nhập nghề nghiệp"
                                                        />
                                                    </td>
                                                    <td>
                                                        <input
                                                            class="form-control"
                                                            type="text"
                                                            v-model="relationships[index].phone_number"
                                                            placeholder="Nhập số điện thoại"
                                                        />
                                                    </td>
                                                    <td>
                                                        <input
                                                            class="form-control"
                                                            type="text"
                                                            v-model="relationships[index].address"
                                                            placeholder="Nhập địa chỉ thường trú"
                                                        />
                                                    </td>
                                                    <td>
                                                        <b-form-select
                                                            :options="listRelations"
                                                            class="form-control"
                                                            v-model="relationships[index].relation"
                                                        />

                                                        <span
                                                            v-if="!relationships[index].relation"
                                                            class="field-required"
                                                            >{{
                                                                formError['relationships.' + index + '.relation']
                                                            }}</span
                                                        >
                                                    </td>
                                                    <td class="text-center">
                                                        <b-form-checkbox
                                                            v-model="relationships[index].is_dependent"
                                                        />
                                                    </td>
                                                    <td>
                                                        <date-picker
                                                            v-if="relationships[index].is_dependent"
                                                            v-model="relationships[index].dependent_start_date"
                                                            type="date"
                                                            format="DD/MM/YYYY"
                                                            value-type="YYYY-MM-DD"
                                                            placeholder="dd/mm/yyyy"
                                                        ></date-picker>
                                                        <span
                                                            v-if="
                                                                relationships[index].is_dependent &&
                                                                !relationships[index].dependent_start_date
                                                            "
                                                            class="field-required"
                                                            >{{
                                                                formError[
                                                                    'relationships.' + index + '.dependent_start_date'
                                                                ]
                                                            }}</span
                                                        >
                                                    </td>
                                                    <td>
                                                        <date-picker
                                                            v-if="relationships[index].is_dependent"
                                                            v-model="relationships[index].dependent_end_date"
                                                            type="date"
                                                            format="DD/MM/YYYY"
                                                            value-type="YYYY-MM-DD"
                                                            placeholder="dd/mm/yyyy"
                                                        ></date-picker>
                                                    </td>
                                                    <td v-if="!isShow">
                                                        <b-button
                                                            variant="success"
                                                            class="mr-1 btn-mini"
                                                            @click="addRelationship()"
                                                        >
                                                            <i class="mdi mdi-plus"></i>
                                                        </b-button>
                                                        <b-button
                                                            variant="danger"
                                                            class="btn-mini"
                                                            @click="removeRelationship(index)"
                                                        >
                                                            <i class="mdi mdi-minus"></i>
                                                        </b-button>
                                                    </td>
                                                </tr>
                                                <tr :key="'att-' + index" v-if="relationships[index].attachments && relationships[index].attachments.length > 0 || !isShow">
                                                    <td></td>
                                                    <td :colspan="isShow ? 9 : 10" class="pt-0 pb-2">
                                                        <div class="d-flex flex-wrap align-items-center" style="gap: 8px;">
                                                            <div
                                                                v-for="(att, attIdx) in relationships[index].attachments"
                                                                :key="attIdx"
                                                                class="d-flex align-items-center border rounded px-2 py-1"
                                                                style="font-size: 13px; background: #f8f9fa;"
                                                            >
                                                                <i class="mdi mdi-paperclip mr-1"></i>
                                                                <a
                                                                    :href="att.file_url"
                                                                    target="_blank"
                                                                    class="text-primary mr-1"
                                                                    :title="att.file_name"
                                                                    style="max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: inline-block;"
                                                                >{{ att.file_name }}</a>
                                                                <small class="text-muted mr-1" v-if="att.file_size">
                                                                    ({{ formatFileSize(att.file_size) }})
                                                                </small>
                                                                <b-button
                                                                    v-if="!isShow"
                                                                    variant="link"
                                                                    class="p-0 text-danger"
                                                                    style="font-size: 14px; line-height: 1;"
                                                                    @click="removeRelationshipAttachment(index, attIdx)"
                                                                    title="Xóa file"
                                                                >
                                                                    <i class="mdi mdi-close"></i>
                                                                </b-button>
                                                            </div>
                                                            <div v-if="!isShow && relationships[index].attachments.length < 5" class="d-inline-block position-relative">
                                                                <b-button
                                                                    variant="outline-secondary"
                                                                    size="sm"
                                                                >
                                                                    <i class="mdi mdi-plus mr-1"></i>Thêm file
                                                                    ({{ 5 - relationships[index].attachments.length }}/5)
                                                                </b-button>
                                                                <input
                                                                    type="file"
                                                                    multiple
                                                                    class="position-absolute"
                                                                    style="top: 0; left: 0; width: 100%; height: 100%; opacity: 0; cursor: pointer;"
                                                                    @change="onRelationshipFileChange($event, index)"
                                                                />
                                                            </div>
                                                        </div>
                                                    </td>
                                                </tr>
                                                </template>
```

- [ ] **Step 2: Verify — chạy dev server và kiểm tra UI**

```bash
cd hrm-thanhan-client
npm run dev
```

Mở trình duyệt, vào `human/employee_info/{id}/edit` → tab "Thông tin nhân sự" → phần "Thông tin gia đình":
- Kiểm tra bảng hiển thị đúng
- Nút "Thêm file" xuất hiện dưới mỗi hàng người thân
- Upload 1 file → hiện tên file + nút xóa
- Upload thêm đến 5 file → nút "Thêm file" biến mất
- Click xóa file → file bị xóa khỏi danh sách
- Click tên file → mở link S3 trong tab mới
- Submit form → không có lỗi
- Reload trang → file đã upload vẫn hiện đúng

---

### Task 9: Kiểm thử end-to-end

**Files:** Không thay đổi code

- [ ] **Step 1: Test flow edit trực tiếp**

1. Mở `human/employee_info/{id}/edit`
2. Thêm 1 người thân mới → upload 2 file → Submit
3. Reload → kiểm tra 2 file vẫn hiện
4. Xóa 1 file → thêm 1 file mới → Submit
5. Reload → kiểm tra chỉ còn 2 file đúng
6. Xóa người thân → Submit
7. Kiểm tra DB: records trong `employee_relationship_attachments` cũng bị xóa (cascade)

- [ ] **Step 2: Test flow yêu cầu cập nhật (nếu có quyền)**

1. Tạo yêu cầu cập nhật thông tin nhân sự
2. Thêm file đính kèm cho người thân
3. Submit yêu cầu
4. Kiểm tra DB: `employee_relationship_attachment_tmps` có records
5. Duyệt yêu cầu (approve)
6. Kiểm tra DB: records đã copy sang `employee_relationship_attachments`

- [ ] **Step 3: Test edge cases**

1. Thử upload 6 file cùng lúc → chỉ 5 file được nhận, toast cảnh báo
2. Upload file nặng → kiểm tra không bị lỗi timeout
3. Người thân chưa có file → chỉ hiện nút "Thêm file (5/5)"
4. Mode xem (isShow = true) → không hiện nút thêm/xóa, chỉ hiện tên file + link tải
