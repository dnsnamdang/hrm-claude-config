# Subject Enrollment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Cho phép user enroll khoá học riêng lẻ, navigate tới trang placeholder sau enroll, hiển thị trạng thái "Đã tham gia" khi quay lại detail.

**Architecture:** BE tạo bảng + model + service + controller endpoint cho subject enrollment. FE sửa store gọi API thật, thêm trang placeholder, cập nhật button theo trạng thái enrollment.

**Tech Stack:** PHP 7.4, Laravel 8 (Modules/Training), Vue 3.5 + Pinia + Vite (elearning/)

**Spec:** `docs/superpowers/specs/2026-05-21-subject-enrollment-design.md`

---

## File Map

| Action | File | Responsibility |
|--------|------|---------------|
| Create | `hrm-api/Modules/Training/Database/Migrations/2026_05_21_100000_create_table_subject_enrollments.php` | Migration tạo bảng |
| Create | `hrm-api/Modules/Training/Entities/SubjectEnrollment.php` | Model |
| Create | `hrm-api/Modules/Training/Services/Subject/SubjectEnrollmentService.php` | Business logic enroll |
| Modify | `hrm-api/Modules/Training/Http/Controllers/V1/SubjectController.php` | Thêm method `enroll()` + sửa `showBuilder()` |
| Modify | `hrm-api/Modules/Training/Routes/api.php:126` | Thêm route POST enroll |
| Modify | `elearning/src/stores/subjectDetail.js:99-127,199-200` | Map enrollment + sửa `enroll()` async |
| Modify | `elearning/src/composables/useContentDetail.js:1-2,132-148` | Thêm router + navigate sau enroll |
| Modify | `elearning/src/components/content-detail/DetailEnrollCard.vue:65-85,109` | Thêm button "Bắt đầu học" cho enrolled |
| Modify | `elearning/src/views/ContentDetailView.vue:71-74` | Handle event start-learn |
| Modify | `elearning/src/constants/subjectDetail.js:1-6` | Sửa label enrolled |
| Create | `elearning/src/views/subject/SubjectLearnView.vue` | Trang placeholder |
| Modify | `elearning/src/router/index.js` | Thêm route subject-learn |

---

## Phase 1: Backend

### Task 1: Migration

**Files:**
- Create: `hrm-api/Modules/Training/Database/Migrations/2026_05_21_100000_create_table_subject_enrollments.php`

- [ ] **Step 1: Tạo file migration**

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateTableSubjectEnrollments extends Migration
{
    public function up()
    {
        Schema::create('subject_enrollments', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('subject_id')->comment('FK tới subjects');
            $table->unsignedBigInteger('employee_id')->comment('Người học');
            $table->tinyInteger('status')->default(1)->comment('1=enrolled, 2=learning, 3=done');
            $table->unsignedTinyInteger('progress')->default(0)->comment('0-100, phần trăm bài hoàn thành');
            $table->timestamp('enrolled_at')->nullable()->comment('Thời điểm đăng ký');
            $table->timestamp('completed_at')->nullable()->comment('Thời điểm hoàn thành');
            $table->timestamps();

            $table->unique(['subject_id', 'employee_id'], 'subject_employee_unique');
        });
    }

    public function down()
    {
        Schema::dropIfExists('subject_enrollments');
    }
}
```

---

### Task 2: Model SubjectEnrollment

**Files:**
- Create: `hrm-api/Modules/Training/Entities/SubjectEnrollment.php`

- [ ] **Step 1: Tạo model**

```php
<?php

namespace Modules\Training\Entities;

use App\Models\BaseModel;

class SubjectEnrollment extends BaseModel
{
    const STATUS_ENROLLED = 1;
    const STATUS_LEARNING = 2;
    const STATUS_DONE = 3;

    protected $table = 'subject_enrollments';

    protected $guarded = [];

    protected $casts = [
        'enrolled_at' => 'datetime',
        'completed_at' => 'datetime',
    ];

    public function subject()
    {
        return $this->belongsTo(Subject::class);
    }

    public function employee()
    {
        return $this->belongsTo(\App\Models\Employee::class, 'employee_id');
    }
}
```

---

### Task 3: Service SubjectEnrollmentService

**Files:**
- Create: `hrm-api/Modules/Training/Services/Subject/SubjectEnrollmentService.php`

- [ ] **Step 1: Tạo service**

```php
<?php

namespace Modules\Training\Services\Subject;

use Modules\Training\Entities\Subject;
use Modules\Training\Entities\SubjectEnrollment;

class SubjectEnrollmentService
{
    public function enrollSubject(Subject $subject)
    {
        $employeeId = auth()->id();

        $existing = SubjectEnrollment::where('subject_id', $subject->id)
            ->where('employee_id', $employeeId)
            ->first();

        if ($existing) {
            return [
                'enrollment' => $existing,
                'already_enrolled' => true,
            ];
        }

        $enrollment = SubjectEnrollment::create([
            'subject_id' => $subject->id,
            'employee_id' => $employeeId,
            'status' => SubjectEnrollment::STATUS_ENROLLED,
            'progress' => 0,
            'enrolled_at' => now(),
        ]);

        return [
            'enrollment' => $enrollment,
            'already_enrolled' => false,
        ];
    }
}
```

---

### Task 4: Controller + Route

**Files:**
- Modify: `hrm-api/Modules/Training/Http/Controllers/V1/SubjectController.php`
- Modify: `hrm-api/Modules/Training/Routes/api.php:126`

- [ ] **Step 1: Thêm method `enroll()` vào SubjectController**

Thêm import ở đầu file (sau các use hiện có):

```php
use Modules\Training\Services\Subject\SubjectEnrollmentService;
```

Thêm method sau method `showBuilder()` (sau dòng 618):

```php
    public function enroll($slug)
    {
        try {
            $subject = Subject::where('slug', $slug)->first();

            if (!$subject) {
                return $this->responseJson('Không tìm thấy khoá học', 404);
            }

            if ($subject->status !== Subject::HOAT_DONG) {
                return $this->responseJson('Khoá học chưa được kích hoạt', 422);
            }

            $result = app(SubjectEnrollmentService::class)->enrollSubject($subject);

            return $this->responseJson('Đã tham gia khoá học thành công', 200, $result);
        } catch (\Exception $e) {
            \Log::error('Subject enroll error: ' . $e->getMessage());
            return $this->responseJson('Đã có lỗi xảy ra', 500);
        }
    }
```

- [ ] **Step 2: Thêm route**

Trong file `api.php`, trong group `/subjects` (dòng 121-148), thêm route enroll **sau dòng 126** (sau `/{id}/builder` GET):

```php
            Route::post('/{slug}/enroll', [SubjectController::class, 'enroll']);
```

Vị trí chính xác — sau dòng 126 `Route::get('/{id}/builder', ...)`:

```
            Route::get('/{id}/builder', [SubjectController::class, 'showBuilder']);
            Route::post('/{slug}/enroll', [SubjectController::class, 'enroll']);   // ← thêm dòng này
            Route::post('/{id}/builder', [SubjectController::class, 'updateBuilder']);
```

---

### Task 5: Sửa showBuilder trả enrollment info

**Files:**
- Modify: `hrm-api/Modules/Training/Http/Controllers/V1/SubjectController.php:587-618`

- [ ] **Step 1: Thêm import SubjectEnrollment**

Thêm ở đầu file (cùng block use):

```php
use Modules\Training\Entities\SubjectEnrollment;
```

- [ ] **Step 2: Sửa method showBuilder**

Thay dòng 617 (`return new SubjectDetailResource($subject);`) bằng:

```php
        $enrollment = null;
        if (auth()->check()) {
            $enrollment = SubjectEnrollment::where('subject_id', $subject->id)
                ->where('employee_id', auth()->id())
                ->first();
        }

        return (new SubjectDetailResource($subject))->additional([
            'enrollment' => $enrollment ? [
                'status' => $enrollment->status,
                'progress' => $enrollment->progress,
                'enrolled_at' => $enrollment->enrolled_at,
                'completed_at' => $enrollment->completed_at,
            ] : null,
        ]);
```

**Lưu ý:** Dùng `->additional()` để thêm data mà không sửa Resource class. FE sẽ nhận `enrollment` ở ngoài `data`.

---

## Phase 2: Frontend

### Task 6: Sửa constants

**Files:**
- Modify: `elearning/src/constants/subjectDetail.js:1-6`

- [ ] **Step 1: Sửa label enrolled**

Sửa dòng 3 từ:
```js
  enrolled: 'Đã tham gia (chưa học)',
```
thành:
```js
  enrolled: 'Đã tham gia',
```

---

### Task 7: Sửa store subjectDetail.js

**Files:**
- Modify: `elearning/src/stores/subjectDetail.js:99-127,199-200`

- [ ] **Step 1: Thêm helper mapLearnStatus**

Thêm trước function `mapSubject` (trước dòng 99):

```js
function mapLearnStatus(enrollment) {
  if (!enrollment) return 'not_enrolled'
  const statusMap = { 1: 'enrolled', 2: 'learning', 3: 'done' }
  return statusMap[enrollment.status] || 'not_enrolled'
}
```

- [ ] **Step 2: Sửa mapSubject nhận enrollment**

Sửa signature dòng 99 từ `function mapSubject(data)` thành:

```js
function mapSubject(data, enrollment) {
```

Sửa 2 dòng trong body (dòng 114-115) từ:

```js
    learnStatus: 'not_enrolled',
    progress: 0,
```

thành:

```js
    learnStatus: mapLearnStatus(enrollment),
    progress: enrollment?.progress || 0,
```

- [ ] **Step 3: Sửa fetchSubject truyền enrollment**

Trong action `fetchSubject` (dòng 164-165), sửa từ:

```js
        const raw = res.data || res
        this.subject = mapSubject(raw)
```

thành:

```js
        const raw = res.data || res
        const enrollment = res.enrollment || null
        this.subject = mapSubject(raw, enrollment)
```

**Giải thích:** `->additional()` của Laravel Resource trả enrollment ở cùng cấp với `data`, tức response JSON có dạng `{ data: {...}, enrollment: {...} }`. Biến `res` từ `api.get()` chứa toàn bộ response body.

- [ ] **Step 4: Sửa enroll() thành async**

Sửa action `enroll()` (dòng 199-200) từ:

```js
    enroll() {
      if (this.subject) this.subject.learnStatus = 'enrolled'
    },
```

thành:

```js
    async enroll() {
      const slug = this.subject?.slug
      if (!slug) throw new Error('No subject')
      await api.post(`/training/subjects/${slug}/enroll`)
      if (this.subject) this.subject.learnStatus = 'enrolled'
    },
```

---

### Task 8: Sửa useContentDetail.js

**Files:**
- Modify: `elearning/src/composables/useContentDetail.js:1-2,132-148,150-166`

- [ ] **Step 1: Thêm import useRouter**

Sửa dòng 2 từ:

```js
import { useRoute } from 'vue-router'
```

thành:

```js
import { useRoute, useRouter } from 'vue-router'
```

- [ ] **Step 2: Thêm router instance**

Sau dòng `const route = useRoute()` (bên trong function `useContentDetail`), thêm:

```js
  const router = useRouter()
```

Tức sau dòng 54 `const route = useRoute()`, thêm dòng mới:

```js
  const router = useRouter()
```

- [ ] **Step 3: Sửa handleEnroll cho subject**

Sửa toàn bộ function `handleEnroll()` (dòng 132-148) thành:

```js
  async function handleEnroll() {
    if (!isLoggedIn.value) {
      toast.show(labels.enrollToast)
      return
    }
    try {
      if (entityType === 'subject') {
        await store.enroll()
        toast.show(labels.enrolledToast)
        router.push({ name: 'subject-learn', params: { slug: route.params.slug } })
      } else {
        await store.enrollPath()
        await store.fetchPath(route.params.slug)
        toast.show(labels.enrolledToast)
      }
    } catch {
      toast.show(labels.enrollFailToast)
    }
  }
```

- [ ] **Step 4: Thêm handleStartLearn vào return**

Thêm function mới trước block `return`:

```js
  function handleStartLearn() {
    router.push({ name: 'subject-learn', params: { slug: route.params.slug } })
  }
```

Và thêm `handleStartLearn` vào object return (sau `handleEnroll,`):

```js
    handleEnroll,
    handleStartLearn,
```

---

### Task 9: Sửa DetailEnrollCard.vue

**Files:**
- Modify: `elearning/src/components/content-detail/DetailEnrollCard.vue:65-85,109`

- [ ] **Step 1: Thêm button "Bắt đầu học" cho enrolled**

Sửa block buttons (dòng 64-85) thành:

```html
      <!-- Buttons -->
      <div class="mt-2.5 flex gap-2.5">
        <button
          v-if="entity.learnStatus === 'learning'"
          class="flex h-9 flex-1 items-center justify-center gap-2 rounded-[10px] border border-brand bg-brand text-[12px] font-bold text-white hover:bg-brand-2"
          @click="$emit('continue')"
        >
          <i class="ri-play-circle-line"></i> Tiếp tục học
        </button>
        <button
          v-else-if="entity.learnStatus === 'enrolled'"
          class="flex h-9 flex-1 items-center justify-center gap-2 rounded-[10px] border border-brand bg-brand text-[12px] font-bold text-white hover:bg-brand-2"
          @click="$emit('start-learn')"
        >
          <i class="ri-play-circle-line"></i> Bắt đầu học
        </button>
        <button
          v-else-if="entity.learnStatus === 'done'"
          class="flex h-9 flex-1 items-center justify-center gap-2 rounded-[10px] border border-brand bg-brand text-[12px] font-bold text-white hover:bg-brand-2"
          @click="$emit('certificate')"
        >
          <i class="ri-medal-line"></i> Chứng nhận
        </button>
        <button
          v-else
          class="flex h-9 flex-1 items-center justify-center gap-2 rounded-[10px] border border-brand bg-brand text-[12px] font-bold text-white hover:bg-brand-2"
          @click="$emit('enroll')"
        >
          <i class="ri-login-box-line"></i> Tham gia
        </button>
```

- [ ] **Step 2: Thêm emit 'start-learn'**

Sửa dòng 109 `defineEmits` từ:

```js
defineEmits(['enroll', 'continue', 'certificate', 'save'])
```

thành:

```js
defineEmits(['enroll', 'start-learn', 'continue', 'certificate', 'save'])
```

---

### Task 10: Sửa ContentDetailView.vue

**Files:**
- Modify: `elearning/src/views/ContentDetailView.vue:66-74,184-189`

- [ ] **Step 1: Thêm event start-learn vào DetailEnrollCard**

Sửa block `<DetailEnrollCard>` (dòng 66-75) thêm handler `@start-learn`:

```html
          <DetailEnrollCard
            :entity="entity"
            :mandatory-label="labels.mandatoryLabel"
            :optional-label="labels.optionalLabel"
            :status-labels="statusLabels"
            @enroll="handleEnroll"
            @start-learn="handleStartLearn"
            @continue="isLoggedIn ? toast.show('Mở trang học (Demo)') : toast.show('Vui lòng đăng nhập')"
            @certificate="isLoggedIn ? toast.show('Xem chứng nhận (Demo)') : toast.show('Vui lòng đăng nhập')"
            @save="isLoggedIn ? toast.show('Đã lưu (Demo)') : toast.show('Vui lòng đăng nhập')"
          />
```

- [ ] **Step 2: Destructure handleStartLearn từ composable**

Sửa destructure (dòng 184-189) thêm `handleStartLearn`:

```js
const {
  store, entity, items, ratingSummary, allItemsOpen,
  errorUI, isLoggedIn, loginUrl,
  activeTab, tabs,
  scrollTo, handleEnroll, handleStartLearn, labels, statusLabels, heroBadges,
} = useContentDetail(entityType)
```

---

### Task 11: Tạo trang placeholder + route

**Files:**
- Create: `elearning/src/views/subject/SubjectLearnView.vue`
- Modify: `elearning/src/router/index.js`

- [ ] **Step 1: Tạo SubjectLearnView.vue**

```vue
<template>
  <div class="flex min-h-[60vh] flex-col items-center justify-center px-4 text-center">
    <div class="flex h-20 w-20 items-center justify-center rounded-full bg-brand/[0.08]">
      <i class="ri-slideshow-3-line text-3xl text-brand"></i>
    </div>
    <h2 class="mt-5 text-lg font-extrabold text-ink">
      Tính năng học đang phát triển
    </h2>
    <p class="mt-2 max-w-md text-[13px] font-semibold leading-relaxed text-muted">
      Vui lòng quay lại sau. Chúng tôi đang xây dựng trải nghiệm học tập tốt nhất cho bạn.
    </p>
    <router-link
      :to="{ name: 'subject-detail', params: { slug: $route.params.slug } }"
      class="mt-5 flex h-9 items-center gap-1.5 rounded-[10px] border border-brand/25 bg-white px-4 text-[13px] font-bold text-brand hover:bg-brand/[0.06]"
    >
      <i class="ri-arrow-left-line"></i> Quay về khoá học
    </router-link>
  </div>
</template>
```

- [ ] **Step 2: Thêm route**

Trong `elearning/src/router/index.js`, thêm route mới **sau** route `subject-detail` (sau dòng 15):

```js
    {
      path: '/khoa-hoc/:slug/hoc',
      name: 'subject-learn',
      component: () => import('@/views/subject/SubjectLearnView.vue'),
    },
```

Vị trí chính xác — giữa subject-detail và subject-discussion:

```js
    {
      path: '/khoa-hoc/:slug',
      name: 'subject-detail',
      component: () => import('@/views/ContentDetailView.vue'),
      meta: { entityType: 'subject' },
    },
    {                                                              // ← thêm block này
      path: '/khoa-hoc/:slug/hoc',
      name: 'subject-learn',
      component: () => import('@/views/subject/SubjectLearnView.vue'),
    },
    {
      path: '/khoa-hoc/:slug/thao-luan',
      ...
    },
```

**Quan trọng:** Route `/khoa-hoc/:slug/hoc` phải đặt **SAU** `/khoa-hoc/:slug` vì Vue Router 4 match theo thứ tự khai báo. Nhưng `/hoc` là path cụ thể hơn `:slug` nên Vue Router 4 sẽ match đúng. Tuy nhiên để an toàn, đặt trước route discussion là đủ.

---

## Verification

### Task 12: Kiểm tra thủ công

- [ ] **Step 1: Chạy migration**

```bash
cd hrm-api
php artisan migrate
```

Verify: bảng `subject_enrollments` được tạo với đúng cấu trúc.

- [ ] **Step 2: Test API enroll**

```bash
# Với token hợp lệ, thay {slug} bằng slug khoá học đang active
curl -X POST http://localhost:8000/api/v1/training/subjects/{slug}/enroll \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json"
```

Expected: `{"message": "Đã tham gia khoá học thành công", ...}`

- [ ] **Step 3: Test FE flow**

1. Mở trang chi tiết khoá học → nút "Tham gia" hiện
2. Nhấn "Tham gia" → toast "Đã tham gia khoá học" → redirect tới `/khoa-hoc/:slug/hoc`
3. Trang placeholder hiện đúng text + nút "Quay về khoá học"
4. Nhấn "Quay về khoá học" → về trang detail → hiện "Đã tham gia" + nút "Bắt đầu học"
5. Nhấn "Bắt đầu học" → redirect lại trang placeholder

---

### Checkpoint — Plan hoàn thành

```
Phase 1: BE — 5 task (migration, model, service, controller+route, sửa showBuilder)
Phase 2: FE — 6 task (constants, store, composable, DetailEnrollCard, ContentDetailView, placeholder+route)
Verification: 1 task (migration + test API + test FE)
Tổng: 12 task
```
