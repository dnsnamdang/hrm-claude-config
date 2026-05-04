# Lộ trình học (Learning Path) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Xây dựng màn Tạo mới / Sửa / Xem Lộ trình học (gom nhiều khoá học) trong module Training, cả BE + FE.

**Architecture:** 3 bảng DB (learning_paths + learning_path_subjects + learning_path_assignees). BE: migration → models → request → service → resources → controller → routes. FE: page orchestrator (add.vue) + 4 tab components (TabInfo, TabResult, TabLearners, TabCertificate). Dữ liệu khoá học lấy từ subjects/getAll, bài học read-only.

**Tech Stack:** PHP 7.4, Laravel 8, MySQL, Nuxt 2 (Vue 2), Bootstrap 4, vuedraggable, jsPDF

**Spec:** `docs/superpowers/specs/2026-04-29-learning-path-design.md`

---

## Phase 1: Backend — Database & Models

### Task 1: Migration tạo 3 bảng

**Files:**
- Create: `hrm-api/Modules/Training/Database/Migrations/2026_04_29_100000_create_learning_path_tables.php`

- [ ] **Step 1: Tạo file migration**

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateLearningPathTables extends Migration
{
    public function up()
    {
        Schema::create('learning_paths', function (Blueprint $table) {
            $table->id();
            $table->string('code', 50)->unique();
            $table->string('name', 255);
            $table->text('description')->nullable();
            $table->text('purpose')->nullable();
            $table->string('admin_note', 500)->nullable();
            $table->unsignedBigInteger('training_type_id')->nullable();
            $table->tinyInteger('status')->default(1);
            $table->boolean('is_public')->default(false);
            $table->boolean('linear_required')->default(false);
            $table->string('result_rule', 30)->default('REQUIRED_ONLY');
            $table->unsignedTinyInteger('result_min_pass_percent')->nullable();
            $table->boolean('certificate_enabled')->default(false);
            $table->string('certificate_template_path', 500)->nullable();
            $table->json('certificate_fields')->nullable();
            $table->unsignedBigInteger('company_id')->nullable();
            $table->unsignedBigInteger('department_id')->nullable();
            $table->unsignedBigInteger('part_id')->nullable();
            $table->unsignedBigInteger('created_by')->nullable();
            $table->unsignedBigInteger('updated_by')->nullable();
            $table->timestamps();
        });

        Schema::create('learning_path_subjects', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('learning_path_id');
            $table->unsignedBigInteger('subject_id');
            $table->integer('sort_order')->default(0);
            $table->boolean('is_required')->default(true);
            $table->string('note', 500)->nullable();
        });

        Schema::create('learning_path_assignees', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('learning_path_id');
            $table->string('assignee_type', 30);
            $table->unsignedBigInteger('assignee_id');
            $table->string('assignment_mode', 20);
        });
    }

    public function down()
    {
        Schema::dropIfExists('learning_path_assignees');
        Schema::dropIfExists('learning_path_subjects');
        Schema::dropIfExists('learning_paths');
    }
}
```

- [ ] **Step 2: Chạy migration**

```bash
cd hrm-api && php artisan migrate
```

Expected: 3 bảng được tạo thành công.

---

### Task 2: Model LearningPath

**Files:**
- Create: `hrm-api/Modules/Training/Entities/LearningPath.php`

- [ ] **Step 1: Tạo model**

```php
<?php

namespace Modules\Training\Entities;

use App\Models\BaseModel;

class LearningPath extends BaseModel
{
    const STATUS_DRAFT = 1;
    const STATUS_ACTIVE = 2;
    const STATUS_LOCKED = 3;

    const STATUSES = [
        ['id' => self::STATUS_DRAFT, 'name' => 'Nháp', 'color' => '#64748B'],
        ['id' => self::STATUS_ACTIVE, 'name' => 'Đang dùng', 'color' => '#16A34A'],
        ['id' => self::STATUS_LOCKED, 'name' => 'Khoá', 'color' => '#DC2626'],
    ];

    const RESULT_RULES = [
        ['id' => 'REQUIRED_ONLY', 'name' => 'Tất cả khoá bắt buộc ĐẠT'],
        ['id' => 'ALL_COURSES', 'name' => 'Tất cả khoá trong lộ trình ĐẠT'],
        ['id' => 'MIN_PERCENT', 'name' => 'Đạt tối thiểu X% số khoá'],
    ];

    protected $guarded = [];

    protected $casts = [
        'is_public' => 'boolean',
        'linear_required' => 'boolean',
        'certificate_enabled' => 'boolean',
        'certificate_fields' => 'array',
    ];

    public function getNextCode()
    {
        $maxId = static::max('id') ?? 0;
        return 'LP-' . date('Y') . '-' . str_pad($maxId + 1, 5, '0', STR_PAD_LEFT);
    }

    public function getStatusTextAttribute()
    {
        $map = [self::STATUS_DRAFT => 'Nháp', self::STATUS_ACTIVE => 'Đang dùng', self::STATUS_LOCKED => 'Khoá'];
        return $map[$this->status] ?? '';
    }

    public function subjects()
    {
        return $this->belongsToMany(Subject::class, 'learning_path_subjects')
            ->withPivot('sort_order', 'is_required', 'note')
            ->orderBy('learning_path_subjects.sort_order');
    }

    public function learningPathSubjects()
    {
        return $this->hasMany(LearningPathSubject::class)->orderBy('sort_order');
    }

    public function assignees()
    {
        return $this->hasMany(LearningPathAssignee::class);
    }

    public function trainingType()
    {
        return $this->belongsTo(TrainingType::class);
    }

    public function createdByEmployee()
    {
        return $this->belongsTo(\App\Models\Employee::class, 'created_by');
    }

    public function updatedByEmployee()
    {
        return $this->belongsTo(\App\Models\Employee::class, 'updated_by');
    }
}
```

---

### Task 3: Model LearningPathSubject

**Files:**
- Create: `hrm-api/Modules/Training/Entities/LearningPathSubject.php`

- [ ] **Step 1: Tạo model**

```php
<?php

namespace Modules\Training\Entities;

use App\Models\BaseModel;

class LearningPathSubject extends BaseModel
{
    public $timestamps = false;

    protected $fillable = [
        'learning_path_id',
        'subject_id',
        'sort_order',
        'is_required',
        'note',
    ];

    protected $casts = [
        'is_required' => 'boolean',
    ];

    public function learningPath()
    {
        return $this->belongsTo(LearningPath::class);
    }

    public function subject()
    {
        return $this->belongsTo(Subject::class);
    }
}
```

---

### Task 4: Model LearningPathAssignee

**Files:**
- Create: `hrm-api/Modules/Training/Entities/LearningPathAssignee.php`

- [ ] **Step 1: Tạo model**

```php
<?php

namespace Modules\Training\Entities;

use App\Models\BaseModel;

class LearningPathAssignee extends BaseModel
{
    public $timestamps = false;

    protected $fillable = [
        'learning_path_id',
        'assignee_type',
        'assignee_id',
        'assignment_mode',
    ];

    public function learningPath()
    {
        return $this->belongsTo(LearningPath::class);
    }
}
```

---

## Phase 2: Backend — Request, Service, Resources

### Task 5: LearningPathRequest (Form Validation)

**Files:**
- Create: `hrm-api/Modules/Training/Http/Requests/LearningPath/LearningPathRequest.php`

- [ ] **Step 1: Tạo request class**

```php
<?php

namespace Modules\Training\Http\Requests\LearningPath;

use Illuminate\Foundation\Http\FormRequest;

class LearningPathRequest extends FormRequest
{
    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'name' => 'required|string|max:255',
            'training_type_id' => 'nullable|integer|exists:training_types,id',
            'status' => 'required|in:1,2,3',
            'is_public' => 'nullable|boolean',
            'linear_required' => 'nullable|boolean',
            'description' => 'nullable|string',
            'purpose' => 'nullable|string',
            'admin_note' => 'nullable|string|max:500',
            'result_rule' => 'required|in:REQUIRED_ONLY,ALL_COURSES,MIN_PERCENT',
            'result_min_pass_percent' => 'nullable|required_if:result_rule,MIN_PERCENT|integer|min:1|max:100',
            'certificate_enabled' => 'nullable|boolean',
            'certificate_fields' => 'nullable',
            'certificate_template_file' => 'nullable|image|max:5120',

            'subjects' => 'nullable|array',
            'subjects.*.subject_id' => 'required|integer',
            'subjects.*.sort_order' => 'required|integer|min:0',
            'subjects.*.is_required' => 'nullable|boolean',
            'subjects.*.note' => 'nullable|string|max:500',

            'assignees' => 'nullable|array',
            'assignees.*.assignee_type' => 'required|in:department,position,capability',
            'assignees.*.assignee_id' => 'required|integer',
            'assignees.*.assignment_mode' => 'required|in:mandatory,recommended',
        ];
    }
}
```

---

### Task 6: LearningPathService

**Files:**
- Create: `hrm-api/Modules/Training/Services/LearningPath/LearningPathService.php`

- [ ] **Step 1: Tạo service class**

```php
<?php

namespace Modules\Training\Services\LearningPath;

use DB;
use Illuminate\Support\Facades\Storage;
use Modules\Training\Entities\LearningPath;
use Modules\Training\Entities\LearningPathAssignee;
use Modules\Training\Entities\LearningPathSubject;

class LearningPathService
{
    public function store(array $data)
    {
        return DB::transaction(function () use ($data) {
            $learningPath = new LearningPath();
            $learningPath->code = $learningPath->getNextCode();
            $learningPath->name = $data['name'];
            $learningPath->description = $data['description'] ?? null;
            $learningPath->purpose = $data['purpose'] ?? null;
            $learningPath->admin_note = $data['admin_note'] ?? null;
            $learningPath->training_type_id = $data['training_type_id'] ?? null;
            $learningPath->status = $data['status'] ?? LearningPath::STATUS_DRAFT;
            $learningPath->is_public = $data['is_public'] ?? false;
            $learningPath->linear_required = $data['linear_required'] ?? false;
            $learningPath->result_rule = $data['result_rule'] ?? 'REQUIRED_ONLY';
            $learningPath->result_min_pass_percent = $data['result_min_pass_percent'] ?? null;
            $learningPath->certificate_enabled = $data['certificate_enabled'] ?? false;
            $learningPath->certificate_fields = isset($data['certificate_fields'])
                ? (is_string($data['certificate_fields']) ? json_decode($data['certificate_fields'], true) : $data['certificate_fields'])
                : null;
            $learningPath->company_id = auth()->payload()->get('current_company');
            $learningPath->department_id = auth()->payload()->get('current_department');
            $learningPath->part_id = auth()->payload()->get('current_part');
            $learningPath->created_by = auth()->id();
            $learningPath->updated_by = auth()->id();
            $learningPath->save();

            $this->syncSubjects($learningPath, $data['subjects'] ?? []);
            $this->syncAssignees($learningPath, $data['assignees'] ?? []);

            if (isset($data['certificate_template_file'])) {
                $this->uploadCertificateTemplate($learningPath, $data['certificate_template_file']);
            }

            return $learningPath->fresh(['subjects', 'assignees', 'trainingType']);
        });
    }

    public function update(LearningPath $learningPath, array $data)
    {
        return DB::transaction(function () use ($learningPath, $data) {
            $learningPath->name = $data['name'];
            $learningPath->description = $data['description'] ?? null;
            $learningPath->purpose = $data['purpose'] ?? null;
            $learningPath->admin_note = $data['admin_note'] ?? null;
            $learningPath->training_type_id = $data['training_type_id'] ?? null;
            $learningPath->status = $data['status'] ?? $learningPath->status;
            $learningPath->is_public = $data['is_public'] ?? false;
            $learningPath->linear_required = $data['linear_required'] ?? false;
            $learningPath->result_rule = $data['result_rule'] ?? 'REQUIRED_ONLY';
            $learningPath->result_min_pass_percent = $data['result_min_pass_percent'] ?? null;
            $learningPath->certificate_enabled = $data['certificate_enabled'] ?? false;
            $learningPath->certificate_fields = isset($data['certificate_fields'])
                ? (is_string($data['certificate_fields']) ? json_decode($data['certificate_fields'], true) : $data['certificate_fields'])
                : null;
            $learningPath->updated_by = auth()->id();
            $learningPath->save();

            $this->syncSubjects($learningPath, $data['subjects'] ?? []);
            $this->syncAssignees($learningPath, $data['assignees'] ?? []);

            if (isset($data['certificate_template_file'])) {
                if ($learningPath->certificate_template_path) {
                    Storage::disk('s3')->delete($learningPath->certificate_template_path);
                }
                $this->uploadCertificateTemplate($learningPath, $data['certificate_template_file']);
            }

            return $learningPath->fresh(['subjects', 'assignees', 'trainingType']);
        });
    }

    public function delete(LearningPath $learningPath)
    {
        return DB::transaction(function () use ($learningPath) {
            LearningPathSubject::where('learning_path_id', $learningPath->id)->delete();
            LearningPathAssignee::where('learning_path_id', $learningPath->id)->delete();

            if ($learningPath->certificate_template_path) {
                Storage::disk('s3')->delete($learningPath->certificate_template_path);
            }

            $learningPath->delete();
        });
    }

    private function syncSubjects(LearningPath $learningPath, array $subjects)
    {
        LearningPathSubject::where('learning_path_id', $learningPath->id)->delete();

        $rows = [];
        foreach ($subjects as $item) {
            $rows[] = [
                'learning_path_id' => $learningPath->id,
                'subject_id' => $item['subject_id'],
                'sort_order' => $item['sort_order'] ?? 0,
                'is_required' => $item['is_required'] ?? true,
                'note' => $item['note'] ?? null,
            ];
        }

        collect($rows)->chunk(1000)->each(function ($chunk) {
            LearningPathSubject::insert($chunk->toArray());
        });
    }

    private function syncAssignees(LearningPath $learningPath, array $assignees)
    {
        LearningPathAssignee::where('learning_path_id', $learningPath->id)->delete();

        $rows = [];
        foreach ($assignees as $item) {
            $rows[] = [
                'learning_path_id' => $learningPath->id,
                'assignee_type' => $item['assignee_type'],
                'assignee_id' => $item['assignee_id'],
                'assignment_mode' => $item['assignment_mode'],
            ];
        }

        collect($rows)->chunk(1000)->each(function ($chunk) {
            LearningPathAssignee::insert($chunk->toArray());
        });
    }

    private function uploadCertificateTemplate(LearningPath $learningPath, $file)
    {
        $path = $file->store('learning-paths/certificates', 's3');
        $learningPath->certificate_template_path = $path;
        $learningPath->save();
    }
}
```

---

### Task 7: LearningPathListResource

**Files:**
- Create: `hrm-api/Modules/Training/Transformers/LearningPathResource/LearningPathListResource.php`

- [ ] **Step 1: Tạo resource**

```php
<?php

namespace Modules\Training\Transformers\LearningPathResource;

use Illuminate\Http\Resources\Json\ResourceCollection;

class LearningPathListResource extends ResourceCollection
{
    public function toArray($request)
    {
        $currentPage = $this->currentPage();
        $perPage = $this->perPage();

        return $this->collection->map(function ($item, $index) use ($currentPage, $perPage) {
            return [
                'stt' => (($currentPage - 1) * $perPage) + 1 + $index,
                'id' => $item->id,
                'code' => $item->code,
                'name' => $item->name,
                'training_type_id' => $item->training_type_id,
                'training_type_name' => optional($item->trainingType)->name,
                'status' => $item->status,
                'status_text' => $item->status_text,
                'is_public' => $item->is_public,
                'linear_required' => $item->linear_required,
                'result_rule' => $item->result_rule,
                'subjects_count' => $item->learningPathSubjects->count(),
                'certificate_enabled' => $item->certificate_enabled,
                'created_at' => optional($item->created_at)->format('Y-m-d H:i:s'),
                'created_by_name' => optional($item->createdByEmployee)->name,
                'updated_at' => optional($item->updated_at)->format('Y-m-d H:i:s'),
                'updated_by_name' => optional($item->updatedByEmployee)->name,
                'is_can_delete' => $item->status == \Modules\Training\Entities\LearningPath::STATUS_DRAFT,
                'selected' => false,
            ];
        });
    }
}
```

---

### Task 8: LearningPathDetailResource

**Files:**
- Create: `hrm-api/Modules/Training/Transformers/LearningPathResource/LearningPathDetailResource.php`

- [ ] **Step 1: Tạo resource**

```php
<?php

namespace Modules\Training\Transformers\LearningPathResource;

use Illuminate\Http\Resources\Json\JsonResource;

class LearningPathDetailResource extends JsonResource
{
    public function toArray($request)
    {
        $subjects = $this->learningPathSubjects->map(function ($lps) {
            $subject = $lps->subject;
            $lessons = [];
            if ($subject && $subject->relationLoaded('subjectLessons')) {
                $lessons = $subject->subjectLessons->map(function ($sl) {
                    $lesson = $sl->lesson;
                    return [
                        'id' => $sl->id,
                        'lesson_id' => $sl->lesson_id,
                        'code' => optional($lesson)->code,
                        'name' => optional($lesson)->name,
                        'type' => optional($lesson)->type,
                        'type_text' => optional($lesson)->type_text,
                        'duration' => optional($lesson)->duration,
                        'sort_order' => $sl->sort_order,
                    ];
                });
            }

            return [
                'id' => $lps->id,
                'subject_id' => $lps->subject_id,
                'sort_order' => $lps->sort_order,
                'is_required' => $lps->is_required,
                'note' => $lps->note,
                'subject' => $subject ? [
                    'id' => $subject->id,
                    'code' => $subject->code,
                    'name' => $subject->name,
                    'status' => $subject->status,
                    'evaluation_mode' => $subject->evaluation_mode ?? null,
                    'training_type_id' => $subject->training_type_id,
                ] : null,
                'lessons' => $lessons,
            ];
        });

        $assignees = $this->assignees->map(function ($a) {
            return [
                'id' => $a->id,
                'assignee_type' => $a->assignee_type,
                'assignee_id' => $a->assignee_id,
                'assignment_mode' => $a->assignment_mode,
            ];
        });

        return [
            'id' => $this->id,
            'code' => $this->code,
            'name' => $this->name,
            'description' => $this->description,
            'purpose' => $this->purpose,
            'admin_note' => $this->admin_note,
            'training_type_id' => $this->training_type_id,
            'training_type_name' => optional($this->trainingType)->name,
            'status' => $this->status,
            'status_text' => $this->status_text,
            'is_public' => $this->is_public,
            'linear_required' => $this->linear_required,
            'result_rule' => $this->result_rule,
            'result_min_pass_percent' => $this->result_min_pass_percent,
            'certificate_enabled' => $this->certificate_enabled,
            'certificate_template_path' => $this->certificate_template_path,
            'certificate_template_url' => $this->certificate_template_path
                ? \Storage::disk('s3')->url($this->certificate_template_path)
                : null,
            'certificate_fields' => $this->certificate_fields,
            'company_id' => $this->company_id,
            'department_id' => $this->department_id,
            'part_id' => $this->part_id,
            'subjects' => $subjects,
            'assignees' => $assignees,
            'created_by' => $this->created_by,
            'created_by_name' => optional($this->createdByEmployee)->name,
            'updated_by' => $this->updated_by,
            'updated_by_name' => optional($this->updatedByEmployee)->name,
            'created_at' => optional($this->created_at)->format('Y-m-d H:i:s'),
            'updated_at' => optional($this->updated_at)->format('Y-m-d H:i:s'),
        ];
    }
}
```

---

### Task 9: LearningPathController

**Files:**
- Create: `hrm-api/Modules/Training/Http/Controllers/V1/LearningPathController.php`

- [ ] **Step 1: Tạo controller**

```php
<?php

namespace Modules\Training\Http\Controllers\V1;

use App\Http\Controllers\BaseApiController;
use Illuminate\Http\Request;
use Modules\Training\Entities\LearningPath;
use Modules\Training\Http\Requests\LearningPath\LearningPathRequest;
use Modules\Training\Services\LearningPath\LearningPathService;
use Modules\Training\Transformers\LearningPathResource\LearningPathDetailResource;
use Modules\Training\Transformers\LearningPathResource\LearningPathListResource;

class LearningPathController extends BaseApiController
{
    protected $service;

    public function __construct(LearningPathService $service)
    {
        $this->service = $service;
    }

    public function index(Request $request)
    {
        if (!$this->isCurrentEmployeeHasPermission('Quản lý lộ trình học')) {
            return $this->responseJson('Không có quyền', 403);
        }

        $query = LearningPath::with(['trainingType', 'learningPathSubjects', 'createdByEmployee', 'updatedByEmployee']);

        if ($request->company_id) {
            $query->where('company_id', $request->company_id);
        }
        if ($request->department_id) {
            $query->where('department_id', $request->department_id);
        }
        if ($request->keyword) {
            $keyword = $request->keyword;
            $query->where(function ($q) use ($keyword) {
                $q->where('code', 'like', "%{$keyword}%")
                  ->orWhere('name', 'like', "%{$keyword}%");
            });
        }
        if ($request->training_type_id) {
            $query->where('training_type_id', $request->training_type_id);
        }
        if ($request->status) {
            $query->where('status', $request->status);
        }

        $query->orderBy('id', 'desc');
        $perPage = $request->per_page ?? 20;
        $data = $query->paginate($perPage);

        return (new LearningPathListResource($data))->additional([
            'total' => $data->total(),
            'perPage' => $data->perPage(),
            'currentPage' => $data->currentPage(),
        ]);
    }

    public function getAll()
    {
        $data = LearningPath::select('id', 'code', 'name', 'status')
            ->where('status', LearningPath::STATUS_ACTIVE)
            ->orderBy('name')
            ->get();

        return $this->responseJson('success', 200, $data);
    }

    public function getNextCode()
    {
        $code = (new LearningPath())->getNextCode();
        return $this->responseJson('success', 200, ['code' => $code]);
    }

    public function store(LearningPathRequest $request)
    {
        if (!$this->isCurrentEmployeeHasPermission('Quản lý lộ trình học')) {
            return $this->responseJson('Không có quyền', 403);
        }

        try {
            $data = $request->validated();
            if ($request->hasFile('certificate_template_file')) {
                $data['certificate_template_file'] = $request->file('certificate_template_file');
            }
            $learningPath = $this->service->store($data);
            return $this->responseJson('Tạo lộ trình học thành công', 200, ['id' => $learningPath->id]);
        } catch (\Exception $e) {
            \Log::error('LearningPath store error: ' . $e->getMessage());
            return $this->responseJson('Có lỗi xảy ra', 500);
        }
    }

    public function show(LearningPath $learningPath)
    {
        if (!$this->isCurrentEmployeeHasPermission('Quản lý lộ trình học')) {
            return $this->responseJson('Không có quyền', 403);
        }

        $learningPath->load([
            'trainingType',
            'learningPathSubjects.subject.subjectLessons.lesson',
            'assignees',
            'createdByEmployee',
            'updatedByEmployee',
        ]);

        return new LearningPathDetailResource($learningPath);
    }

    public function update(LearningPathRequest $request, LearningPath $learningPath)
    {
        if (!$this->isCurrentEmployeeHasPermission('Quản lý lộ trình học')) {
            return $this->responseJson('Không có quyền', 403);
        }

        try {
            $data = $request->validated();
            if ($request->hasFile('certificate_template_file')) {
                $data['certificate_template_file'] = $request->file('certificate_template_file');
            }
            $this->service->update($learningPath, $data);
            return $this->responseJson('Cập nhật lộ trình học thành công', 200);
        } catch (\Exception $e) {
            \Log::error('LearningPath update error: ' . $e->getMessage());
            return $this->responseJson('Có lỗi xảy ra', 500);
        }
    }

    public function delete(LearningPath $learningPath)
    {
        if (!$this->isCurrentEmployeeHasPermission('Quản lý lộ trình học')) {
            return $this->responseJson('Không có quyền', 403);
        }

        if ($learningPath->status !== LearningPath::STATUS_DRAFT) {
            return $this->responseJson('Chỉ xoá được lộ trình ở trạng thái Nháp', 400);
        }

        try {
            $this->service->delete($learningPath);
            return $this->responseJson('Xoá lộ trình học thành công', 200);
        } catch (\Exception $e) {
            \Log::error('LearningPath delete error: ' . $e->getMessage());
            return $this->responseJson('Có lỗi xảy ra', 500);
        }
    }
}
```

---

### Task 10: Thêm routes

**Files:**
- Modify: `hrm-api/Modules/Training/Routes/api.php`

- [ ] **Step 1: Thêm import controller ở đầu file** (cùng nhóm use statements)

```php
use Modules\Training\Http\Controllers\V1\LearningPathController;
```

- [ ] **Step 2: Thêm route group** vào trong `Route::group(['prefix' => 'training', 'middleware' => 'auth:api'], function () {`

Thêm block sau (vị trí sau nhóm `/lessons`):

```php
        Route::group(['prefix' => '/learning-paths'], function () {
            Route::get('/', [LearningPathController::class, 'index']);
            Route::get('/getAll', [LearningPathController::class, 'getAll']);
            Route::get('/get-next-code', [LearningPathController::class, 'getNextCode']);
            Route::post('/', [LearningPathController::class, 'store']);
            Route::get('/{learningPath}', [LearningPathController::class, 'show']);
            Route::post('/{learningPath}', [LearningPathController::class, 'update']);
            Route::delete('/{learningPath}', [LearningPathController::class, 'delete']);
        });
```

- [ ] **Step 3: Verify API hoạt động**

```bash
cd hrm-api && php artisan route:list --path=learning-paths
```

Expected: 7 routes hiển thị.

---

## Phase 3: Frontend — Page Orchestrator + Store

### Task 11: Thêm API calls vào store

**Files:**
- Không cần tạo file store riêng — dùng `this.$store.dispatch('apiGetMethod', url)` pattern đã có.

- [ ] **Step 1: Skip** — FE gọi API trực tiếp qua store dispatch, không cần thêm file store. Các component sẽ gọi:

```js
// GET
await this.$store.dispatch('apiGetMethod', 'training/learning-paths/get-next-code')
await this.$store.dispatch('apiGetMethod', `training/learning-paths/${id}`)
await this.$store.dispatch('apiGetMethod', 'training/subjects/getAll')

// POST (store)
await this.$store.dispatch('apiPostMethod', { url: 'training/learning-paths', payload })

// POST (update)
await this.$store.dispatch('apiPostMethod', { url: `training/learning-paths/${id}`, payload })

// DELETE
await this.$store.dispatch('apiDeleteMethod', `training/learning-paths/${id}`)
```

---

### Task 12: Page add.vue — Orchestrator

**Files:**
- Modify: `hrm-client/pages/training/learning-path/add.vue`

- [ ] **Step 1: Viết page orchestrator**

```vue
<template>
    <div class="v2-styles">
        <div class="container-fluid mt-3" v-if="hasAPermission('Quản lý lộ trình học')">
            <div class="page-shell">
                <!-- HEADER -->
                <div class="d-flex flex-column flex-md-row align-items-md-center justify-content-md-between mb-3">
                    <div class="mb-2 mb-md-0">
                        <div class="text-uppercase text-muted" style="font-size: 11px; letter-spacing: 0.08em">
                            Đào tạo • Lộ trình học
                        </div>
                        <h1 class="h6 font-weight-bold mb-0 text-dark mt-1" style="font-size: 15px">
                            {{ isEdit ? 'Sửa lộ trình học' : 'Tạo lộ trình học' }}
                        </h1>
                        <div class="tp-sub mt-1">
                            Lộ trình gồm nhiều <b>Khoá học</b> • Kết quả dựa trên <b>Đạt/Không đạt</b> của các khoá.
                        </div>
                    </div>
                    <div class="d-flex flex-wrap align-items-center justify-content-end" style="gap: 10px">
                        <span class="badge badge-light border px-2 py-1">
                            <i class="ri-stack-line mr-1"></i>{{ formData.subjects.length }} khoá
                        </span>
                    </div>
                </div>

                <!-- TABS -->
                <ul class="nav nav-pills tp-tabs mb-3" role="tablist">
                    <li class="nav-item mr-2">
                        <a class="nav-link" :class="{ active: currentTab === 0 }" href="#" @click.prevent="currentTab = 0">
                            <i class="ri-settings-3-line mr-1"></i>Thông tin lộ trình học
                        </a>
                    </li>
                    <li class="nav-item mr-2">
                        <a class="nav-link" :class="{ active: currentTab === 1 }" href="#" @click.prevent="currentTab = 1">
                            <i class="ri-shield-check-line mr-1"></i>Cấu hình kết quả
                        </a>
                    </li>
                    <li class="nav-item mr-2">
                        <a class="nav-link" :class="{ active: currentTab === 2 }" href="#" @click.prevent="currentTab = 2">
                            <i class="ri-team-line mr-1"></i>Cấu hình người học
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" :class="{ active: currentTab === 3 }" href="#" @click.prevent="currentTab = 3">
                            <i class="ri-award-line mr-1"></i>Chứng chỉ
                        </a>
                    </li>
                </ul>

                <!-- ALERT -->
                <div v-if="formError" class="alert alert-danger mb-3" style="font-size: 12px">
                    <i class="ri-error-warning-line mr-1"></i>{{ formError }}
                </div>

                <!-- TAB CONTENT -->
                <div v-show="currentTab === 0">
                    <TabInfo
                        :form-data="formData"
                        :training-types="trainingTypes"
                        :code="nextCode"
                        :is-show="isShow"
                        :errors="errors"
                        @update="handleUpdate"
                        @update-subjects="handleUpdateSubjects"
                    />
                </div>

                <div v-show="currentTab === 1">
                    <TabResult
                        :result-rule="formData.result_rule"
                        :min-pass-percent="formData.result_min_pass_percent"
                        :subjects="formData.subjects"
                        :is-show="isShow"
                        @update="handleUpdate"
                    />
                </div>

                <div v-show="currentTab === 2">
                    <TabLearners
                        :assignees="formData.assignees"
                        :is-show="isShow"
                        @update-assignees="handleUpdateAssignees"
                    />
                </div>

                <div v-show="currentTab === 3">
                    <TabCertificate
                        :certificate-enabled="formData.certificate_enabled"
                        :certificate-fields="formData.certificate_fields"
                        :certificate-template-url="formData.certificate_template_url"
                        :course-name="formData.name"
                        :is-show="isShow"
                        @update="handleUpdate"
                        @update-template-file="handleUpdateTemplateFile"
                    />
                </div>

                <!-- FOOTER -->
                <div class="d-flex justify-content-end mt-3" style="gap: 10px" v-if="!isShow">
                    <button class="btn btn-light border btn-sm" @click="goBack">
                        <i class="ri-arrow-left-line mr-1"></i>Quay về
                    </button>
                    <button class="btn btn-outline-secondary btn-sm" @click="saveDraft" :disabled="isSaving">
                        <i class="ri-save-3-line mr-1"></i>Lưu tạm
                    </button>
                    <button class="btn btn-success btn-sm" @click="savePublish" :disabled="isSaving">
                        <i class="ri-check-line mr-1"></i>Lưu
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import PageTitleMixin from '@/utils/mixins/PageTitleMixin'
import CheckPermission from '@/utils/mixins/CheckPermission'
import TabInfo from './components/TabInfo.vue'
import TabResult from './components/TabResult.vue'
import TabLearners from './components/TabLearners.vue'
import TabCertificate from './components/TabCertificate.vue'

const DEFAULT_FORM = () => ({
    name: '',
    training_type_id: null,
    status: 1,
    is_public: false,
    linear_required: false,
    description: '',
    purpose: '',
    admin_note: '',
    subjects: [],
    result_rule: 'REQUIRED_ONLY',
    result_min_pass_percent: null,
    assignees: [],
    certificate_enabled: false,
    certificate_fields: null,
    certificate_template_file: null,
    certificate_template_url: null,
})

export default {
    layout: 'default-sidebar',
    mixins: [PageTitleMixin, CheckPermission],
    components: { TabInfo, TabResult, TabLearners, TabCertificate },

    head() {
        return { title: this.pageTitle }
    },

    data() {
        return {
            currentTab: 0,
            formData: DEFAULT_FORM(),
            nextCode: '',
            formError: '',
            errors: {},
            isSaving: false,
            isEdit: false,
            isShow: false,
            trainingTypes: [],
        }
    },

    computed: {
        pageTitle() {
            return this.isEdit ? 'Sửa lộ trình học' : 'Tạo lộ trình học'
        },
    },

    async mounted() {
        await this.fetchTrainingTypes()
        await this.fetchNextCode()
    },

    methods: {
        async fetchTrainingTypes() {
            await this.$store.dispatch('optionsSelect/fetchTrainingTypes')
            this.trainingTypes = this.$store.getters['optionsSelect/getTrainingTypes']
        },

        async fetchNextCode() {
            try {
                const res = await this.$store.dispatch('apiGetMethod', 'training/learning-paths/get-next-code')
                this.nextCode = res.data?.code || res.code || ''
            } catch (e) {
                console.error('fetchNextCode error', e)
            }
        },

        handleUpdate(payload) {
            Object.keys(payload).forEach((key) => {
                this.$set(this.formData, key, payload[key])
            })
        },

        handleUpdateSubjects(subjects) {
            this.$set(this.formData, 'subjects', subjects)
        },

        handleUpdateAssignees(assignees) {
            this.$set(this.formData, 'assignees', assignees)
        },

        handleUpdateTemplateFile(file) {
            this.formData.certificate_template_file = file
        },

        validate() {
            this.errors = {}
            this.formError = ''

            if (!this.formData.name || !this.formData.name.trim()) {
                this.errors.name = 'Vui lòng nhập tên lộ trình học'
                this.formError = 'Vui lòng nhập tên lộ trình học'
                this.currentTab = 0
                return false
            }

            if (this.formData.result_rule === 'MIN_PERCENT') {
                const pct = this.formData.result_min_pass_percent
                if (!pct || pct < 1 || pct > 100) {
                    this.errors.result_min_pass_percent = 'Ngưỡng % phải từ 1 đến 100'
                    this.formError = 'Vui lòng nhập ngưỡng % hợp lệ (1-100)'
                    this.currentTab = 1
                    return false
                }
            }

            return true
        },

        buildPayload(statusOverride) {
            const fd = new FormData()

            fd.append('name', this.formData.name?.trim() || '')
            fd.append('training_type_id', this.formData.training_type_id || '')
            fd.append('status', statusOverride != null ? statusOverride : this.formData.status)
            fd.append('is_public', this.formData.is_public ? 1 : 0)
            fd.append('linear_required', this.formData.linear_required ? 1 : 0)
            fd.append('description', this.formData.description || '')
            fd.append('purpose', this.formData.purpose || '')
            fd.append('admin_note', this.formData.admin_note || '')
            fd.append('result_rule', this.formData.result_rule || 'REQUIRED_ONLY')
            fd.append('result_min_pass_percent', this.formData.result_min_pass_percent || '')
            fd.append('certificate_enabled', this.formData.certificate_enabled ? 1 : 0)

            if (this.formData.certificate_fields) {
                fd.append('certificate_fields', JSON.stringify(this.formData.certificate_fields))
            }

            if (this.formData.certificate_template_file) {
                fd.append('certificate_template_file', this.formData.certificate_template_file)
            }

            this.formData.subjects.forEach((s, i) => {
                fd.append(`subjects[${i}][subject_id]`, s.subject_id)
                fd.append(`subjects[${i}][sort_order]`, s.sort_order ?? i)
                fd.append(`subjects[${i}][is_required]`, s.is_required ? 1 : 0)
                fd.append(`subjects[${i}][note]`, s.note || '')
            })

            this.formData.assignees.forEach((a, i) => {
                fd.append(`assignees[${i}][assignee_type]`, a.assignee_type)
                fd.append(`assignees[${i}][assignee_id]`, a.assignee_id)
                fd.append(`assignees[${i}][assignment_mode]`, a.assignment_mode)
            })

            return fd
        },

        async saveDraft() {
            if (!this.formData.name || !this.formData.name.trim()) {
                this.formError = 'Vui lòng nhập tên lộ trình học'
                this.errors = { name: 'Vui lòng nhập tên lộ trình học' }
                this.currentTab = 0
                return
            }
            await this.doSave(1)
        },

        async savePublish() {
            if (!this.validate()) return
            await this.doSave(null)
        },

        async doSave(statusOverride) {
            this.isSaving = true
            this.formError = ''
            try {
                const payload = this.buildPayload(statusOverride)
                const url = this.isEdit
                    ? `training/learning-paths/${this.$route.params.id}`
                    : 'training/learning-paths'
                await this.$store.dispatch('apiPostMethod', { url, payload })
                this.$toasted?.global?.success?.({
                    message: this.isEdit ? 'Cập nhật lộ trình học thành công' : 'Tạo lộ trình học thành công',
                })
                this.$router.push('/training/learning-path')
            } catch (e) {
                const msg = e?.response?.data?.message || 'Có lỗi xảy ra'
                this.formError = msg
            } finally {
                this.isSaving = false
            }
        },

        goBack() {
            this.$router.push('/training/learning-path')
        },
    },
}
</script>

<style scoped>
.page-shell {
    max-width: calc(100% - 50px);
}
</style>
```

---

## Phase 4: Frontend — Tab Components

### Task 13: TabInfo.vue — Thông tin + Builder khoá học

**Files:**
- Create: `hrm-client/pages/training/learning-path/components/TabInfo.vue`

- [ ] **Step 1: Tạo component TabInfo.vue**

Đây là component lớn nhất — gồm form thông tin (trái) + builder khoá học drag-drop (phải) + modal chọn khoá.

Template gồm:
- **Cột trái (col-lg-5):** form fields — Loại đào tạo (V2BaseSelect), Mã LP (disabled input), Tên (required input), Trạng thái (select), Học tuần tự (select), Switch Public, Ghi chú, Mô tả, Mục đích
- **Cột phải (col-lg-7):** panel với header (nút "Thêm khoá học"), body là `<draggable>` chứa danh sách khoá, mỗi khoá hiển thị code + name + badge bài học + expand bài học (read-only) + actions (cấu hình modal, xoá)
- **Modal "Thêm khoá học":** bảng subjects (từ `/subjects/getAll`), tìm kiếm, nút thêm (disable nếu đã có)
- **Modal "Cấu hình khoá trong lộ trình":** form bắt buộc/không + ghi chú

Script cần:
- Props: `formData`, `trainingTypes`, `code`, `isShow`, `errors`
- Events: `@update(payload)`, `@update-subjects(subjects)`
- Data: `subjectBank[]`, `bankSearch`, `showPickerModal`, `showConfigModal`, `configEditing`, `configForm`
- Methods: `fetchSubjectBank()`, `addSubject(subject)`, `removeSubject(index)`, `openConfig(item)`, `saveConfig()`, `onDragEnd()`
- Import: `draggable` from `vuedraggable`
- Mounted: gọi `fetchSubjectBank()`

Xem chi tiết code trong file tạo ra — file này sẽ ~400 dòng template + ~200 dòng script.

- [ ] **Step 2: Viết code đầy đủ TabInfo.vue** (xem file thực tế khi implement)

---

### Task 14: TabResult.vue — Cấu hình kết quả

**Files:**
- Create: `hrm-client/pages/training/learning-path/components/TabResult.vue`

- [ ] **Step 1: Tạo component**

```vue
<template>
    <div class="row">
        <div class="col-lg-7 mb-3 mb-lg-0">
            <section class="tp-card p-3">
                <div class="d-flex align-items-center mb-3 p-2 rounded" style="background: #f8fafc; border: 1px solid #e5e7eb">
                    <div class="d-flex align-items-center justify-content-center mr-2"
                        style="width: 28px; height: 28px; border-radius: 999px; background: rgba(22,163,74,.1); color: #16a34a">
                        <i class="ri-award-line"></i>
                    </div>
                    <div>
                        <div class="font-weight-bold text-dark" style="font-size: 12px">Cấu hình kết quả lộ trình học</div>
                        <div class="text-muted" style="font-size: 11px">Dựa trên Đạt/Không đạt của khoá</div>
                    </div>
                </div>

                <div class="form-row">
                    <div class="col-md-8 mb-2">
                        <label class="tp-label">Điều kiện đạt lộ trình</label>
                        <select
                            :value="resultRule"
                            @change="$emit('update', { result_rule: $event.target.value })"
                            class="form-control form-control-sm"
                            :disabled="isShow"
                        >
                            <option value="REQUIRED_ONLY">Tất cả khoá bắt buộc ĐẠT</option>
                            <option value="ALL_COURSES">Tất cả khoá trong lộ trình ĐẠT</option>
                            <option value="MIN_PERCENT">Đạt tối thiểu X% số khoá</option>
                        </select>
                    </div>
                    <div class="col-md-4 mb-2" v-if="resultRule === 'MIN_PERCENT'">
                        <label class="tp-label">Ngưỡng (%)</label>
                        <input
                            type="number"
                            :value="minPassPercent"
                            @input="$emit('update', { result_min_pass_percent: Number($event.target.value) || null })"
                            class="form-control form-control-sm"
                            min="1"
                            max="100"
                            :disabled="isShow"
                        />
                    </div>
                </div>

                <div class="border rounded p-2 mt-2" style="background: #f8fafc; font-size: 12px">
                    <div class="d-flex flex-wrap" style="gap: 10px">
                        <div><b>Tổng khoá:</b> <span class="font-monospace">{{ stats.total }}</span></div>
                        <div>•</div>
                        <div><b>Bắt buộc:</b> <span class="font-monospace">{{ stats.required }}</span></div>
                        <div>•</div>
                        <div><b>Không bắt buộc:</b> <span class="font-monospace">{{ stats.optional }}</span></div>
                    </div>
                    <div class="text-muted mt-1" style="font-size: 11px">
                        "Đạt/Không đạt" của từng khoá do cấu hình khoá quyết định. Lộ trình chỉ gom kết quả.
                    </div>
                </div>
            </section>
        </div>

        <div class="col-lg-5">
            <section class="tp-card p-3">
                <div class="d-flex align-items-center mb-3 p-2 rounded" style="background: #f8fafc; border: 1px solid #e5e7eb">
                    <div class="d-flex align-items-center justify-content-center mr-2"
                        style="width: 28px; height: 28px; border-radius: 999px; background: rgba(22,163,74,.1); color: #16a34a">
                        <i class="ri-lightbulb-flash-line"></i>
                    </div>
                    <div>
                        <div class="font-weight-bold text-dark" style="font-size: 12px">Tóm tắt kết quả</div>
                        <div class="text-muted" style="font-size: 11px">Hiển thị nhanh cho admin</div>
                    </div>
                </div>

                <div class="border rounded p-2" style="background: #f8fafc; font-size: 12px">
                    <div class="font-weight-bold text-dark mb-1">Hiện tại</div>
                    <div class="text-muted" style="line-height: 1.6">
                        • Rule: <b>{{ ruleLabel }}</b><br />
                        • Khoá: <b>{{ stats.total }}</b> (bắt buộc <b>{{ stats.required }}</b>)<br />
                        <template v-if="resultRule === 'MIN_PERCENT'">
                            • Ngưỡng: <b>{{ minPassPercent || 0 }}%</b>
                        </template>
                    </div>
                </div>
            </section>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        resultRule: { type: String, default: 'REQUIRED_ONLY' },
        minPassPercent: { type: Number, default: null },
        subjects: { type: Array, default: () => [] },
        isShow: { type: Boolean, default: false },
    },
    computed: {
        stats() {
            const total = this.subjects.length
            const required = this.subjects.filter((s) => s.is_required).length
            return { total, required, optional: total - required }
        },
        ruleLabel() {
            const map = {
                REQUIRED_ONLY: 'Tất cả khoá bắt buộc ĐẠT',
                ALL_COURSES: 'Tất cả khoá trong lộ trình ĐẠT',
                MIN_PERCENT: `Đạt tối thiểu ${this.minPassPercent || 0}%`,
            }
            return map[this.resultRule] || this.resultRule
        },
    },
}
</script>
```

---

### Task 15: TabLearners.vue — Cấu hình người học

**Files:**
- Create: `hrm-client/pages/training/learning-path/components/TabLearners.vue`

- [ ] **Step 1: Tạo component**

Component gồm 2 cột (Bắt buộc / Khuyến khích), mỗi cột có 3 pill toggle (Phòng ban, Chức vụ, Năng lực), khi active hiện multi-select.

Script cần:
- Props: `assignees`, `isShow`
- Events: `@update-assignees(assignees)`
- Data: `departments[]`, `positions[]`, `capabilities[]`, `mandatoryTypes[]`, `recommendedTypes[]`
- Computed: `mandatoryDepartments`, `mandatoryPositions`, `mandatoryCapabilities`, `recommendedDepartments`, `recommendedPositions`, `recommendedCapabilities` — filter từ assignees theo type + mode
- Methods: `fetchDepartments()`, `fetchPositions()`, `fetchCapabilities()`, `toggleType(types, type)`, `hasType(types, type)`, `onSelectChange(mode, type, ids)` — rebuild assignees array
- Mounted: fetch departments, positions, capabilities

Multi-select: dùng `V2BaseSelect` với `multiple` nếu có, hoặc tự build dropdown giống file mẫu HTML.

- [ ] **Step 2: Viết code đầy đủ TabLearners.vue** (xem file thực tế khi implement)

---

### Task 16: TabCertificate.vue — Chứng chỉ

**Files:**
- Create: `hrm-client/pages/training/learning-path/components/TabCertificate.vue`

- [ ] **Step 1: Cài jsPDF**

```bash
cd hrm-client && npm install jspdf@2.5.1 --save
```

- [ ] **Step 2: Tạo component**

Component gồm:
- Switch bật/tắt certificate
- Khi bật: layout 2 cột (config trái + canvas preview phải)
- Config: upload ảnh + 4 field (courseName, fullName, issueDate, signer) mỗi field có text/x/y/size/weight
- Canvas: ref="certCanvas", 1600x900, render ảnh + 4 text overlay
- Nút: "Render lại" + "Download PDF"

Script cần:
- Props: `certificateEnabled`, `certificateFields`, `certificateTemplateUrl`, `courseName`, `isShow`
- Events: `@update(payload)`, `@update-template-file(file)`
- Data: `fields` (4 trường với default x/y/size/weight), `templateDataUrl` (base64 ảnh preview)
- Methods: `onToggle()`, `onTemplateChange(e)`, `renderCertificate()`, `downloadPdf()`
- Watch: `fields` deep → auto renderCertificate
- Import: `jsPDF` from `jspdf`

Canvas render logic:
1. Clear canvas
2. Nếu có template image → drawImage fill canvas
3. Nếu không → fill background xám + border
4. Vẽ 4 text tại vị trí x/y với font-size + font-weight

Download PDF:
1. Tạo jsPDF landscape A4
2. Add canvas as image
3. Save file

- [ ] **Step 3: Viết code đầy đủ TabCertificate.vue** (xem file thực tế khi implement)

---

## Phase 5: Frontend — Edit + Show Pages

### Task 17: Page _id/edit.vue

**Files:**
- Create: `hrm-client/pages/training/learning-path/_id/edit.vue`

- [ ] **Step 1: Tạo page**

Tái sử dụng `add.vue` pattern nhưng set `isEdit = true` và load data từ API.

```vue
<template>
    <div class="v2-styles">
        <div class="container-fluid mt-3" v-if="hasAPermission('Quản lý lộ trình học')">
            <!-- Copy toàn bộ template từ add.vue -->
            <!-- Chỉ khác: isEdit = true, mounted gọi fetchDetail() -->
        </div>
    </div>
</template>

<script>
// Import giống add.vue
// Thêm:
// - async mounted(): fetchDetail() trước fetchNextCode()
// - methods.fetchDetail(): gọi API show, map response vào formData
// - isEdit: true
</script>
```

Cách tiếp cận tốt hơn: **extract logic chung vào mixin hoặc dùng chung component** — `add.vue` nhận prop `learningPathId` nullable, nếu có thì load data. `edit.vue` truyền `$route.params.id`.

Pattern theo subjects:

```vue
<template>
    <div class="v2-styles">
        <div class="container-fluid mt-3">
            <!-- Dùng lại add.vue nhưng truyền id -->
        </div>
    </div>
</template>

<script>
import PageTitleMixin from '@/utils/mixins/PageTitleMixin'

export default {
    layout: 'default-sidebar',
    mixins: [PageTitleMixin],
    head() {
        return { title: this.pageTitle }
    },
    computed: {
        pageTitle() {
            return 'Sửa lộ trình học'
        },
    },
}
</script>
```

Thực tế: **refactor add.vue thành component `LearningPathForm.vue`** tương tự `SubjectBuilderForm.vue`, rồi cả `add.vue` và `edit.vue` đều import nó.

- [ ] **Step 2: Refactor add.vue → LearningPathForm.vue component**

Move toàn bộ logic hiện tại của `add.vue` vào `components/LearningPathForm.vue`, thêm prop `learningPathId` (nullable). Khi có `learningPathId` → gọi API show để load data.

- [ ] **Step 3: Cập nhật add.vue thành wrapper đơn giản**

```vue
<template>
    <div class="v2-styles">
        <div class="container-fluid mt-3">
            <LearningPathForm :learning-path-id="null" @saved="handleSaved" @cancel="handleCancel" />
        </div>
    </div>
</template>

<script>
import LearningPathForm from './components/LearningPathForm.vue'
import PageTitleMixin from '@/utils/mixins/PageTitleMixin'

export default {
    layout: 'default-sidebar',
    mixins: [PageTitleMixin],
    components: { LearningPathForm },
    head() {
        return { title: this.pageTitle }
    },
    computed: {
        pageTitle() {
            return 'Tạo lộ trình học'
        },
    },
    methods: {
        handleSaved() {
            this.$router.push('/training/learning-path')
        },
        handleCancel() {
            this.$router.push('/training/learning-path')
        },
    },
}
</script>
```

- [ ] **Step 4: Tạo edit.vue**

```vue
<template>
    <div class="v2-styles">
        <div class="container-fluid mt-3">
            <LearningPathForm :learning-path-id="$route.params.id" @saved="handleSaved" @cancel="handleCancel" />
        </div>
    </div>
</template>

<script>
import LearningPathForm from '../components/LearningPathForm.vue'
import PageTitleMixin from '@/utils/mixins/PageTitleMixin'

export default {
    layout: 'default-sidebar',
    mixins: [PageTitleMixin],
    components: { LearningPathForm },
    head() {
        return { title: this.pageTitle }
    },
    computed: {
        pageTitle() {
            return 'Sửa lộ trình học'
        },
    },
    methods: {
        handleSaved() {
            this.$router.push('/training/learning-path')
        },
        handleCancel() {
            this.$router.push('/training/learning-path')
        },
    },
}
</script>
```

---

### Task 18: Page _id/index.vue (Show/Chi tiết)

**Files:**
- Create: `hrm-client/pages/training/learning-path/_id/index.vue`

- [ ] **Step 1: Tạo page xem chi tiết**

```vue
<template>
    <div class="v2-styles">
        <div class="container-fluid mt-3">
            <LearningPathForm
                :learning-path-id="$route.params.id"
                :is-show-mode="true"
                @cancel="handleBack"
            />
        </div>
    </div>
</template>

<script>
import LearningPathForm from '../components/LearningPathForm.vue'
import PageTitleMixin from '@/utils/mixins/PageTitleMixin'

export default {
    layout: 'default-sidebar',
    mixins: [PageTitleMixin],
    components: { LearningPathForm },
    head() {
        return { title: this.pageTitle }
    },
    computed: {
        pageTitle() {
            return 'Chi tiết lộ trình học'
        },
    },
    methods: {
        handleBack() {
            this.$router.push('/training/learning-path')
        },
    },
}
</script>
```

- [ ] **Step 2: Cập nhật LearningPathForm.vue** — thêm prop `isShowMode` (default false), khi true thì set `isShow = true` và ẩn nút Lưu.

---

## Phase 6: Verify & Polish

### Task 19: Kiểm tra toàn bộ flow

- [ ] **Step 1: Chạy migration verify**

```bash
cd hrm-api && php artisan migrate:status | grep learning
```

Expected: 3 bảng status "Ran".

- [ ] **Step 2: Verify routes**

```bash
cd hrm-api && php artisan route:list --path=learning-paths
```

Expected: 7 routes hiển thị.

- [ ] **Step 3: Test API tạo mới** (dùng Postman hoặc curl)

```
POST /v1/training/learning-paths
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Test Lộ trình",
  "status": 1,
  "result_rule": "REQUIRED_ONLY"
}
```

Expected: 200, trả về `{ id: 1 }`.

- [ ] **Step 4: Mở browser test FE**

Truy cập: `http://localhost:3000/training/learning-path/add`

Verify:
- 4 tabs hiển thị đúng
- Form fields hoạt động
- Modal thêm khoá học load subjects
- Drag-drop khoá hoạt động
- Tab kết quả cập nhật stats
- Tab người học load departments/positions/capabilities
- Tab chứng chỉ: switch, upload, canvas preview
- Lưu tạm / Lưu hoạt động → redirect về danh sách

---

## Bug fix: Lưu lộ trình học bị 500

- [ ] Thu thập log lỗi từ `hrm-api/storage/logs/laravel-YYYY-MM-DD.log`
- [ ] Trace endpoint save `LearningPathController` + request payload
- [ ] Fix nguyên nhân và verify flow lưu (create/update)

---

## UI polish: Thông báo lỗi dùng toast

- [ ] Bỏ alert inline `formError` ở `LearningPathForm.vue`
- [ ] Hiển thị toast lỗi khi validate/save thất bại

---

## File Map (Tổng kết)

### Backend — Tạo mới:
| # | File | Mô tả |
|---|------|-------|
| 1 | `Modules/Training/Database/Migrations/2026_04_29_100000_create_learning_path_tables.php` | Migration 3 bảng |
| 2 | `Modules/Training/Entities/LearningPath.php` | Model chính |
| 3 | `Modules/Training/Entities/LearningPathSubject.php` | Model pivot subjects |
| 4 | `Modules/Training/Entities/LearningPathAssignee.php` | Model pivot assignees |
| 5 | `Modules/Training/Http/Requests/LearningPath/LearningPathRequest.php` | Form validation |
| 6 | `Modules/Training/Services/LearningPath/LearningPathService.php` | Business logic |
| 7 | `Modules/Training/Transformers/LearningPathResource/LearningPathListResource.php` | List transformer |
| 8 | `Modules/Training/Transformers/LearningPathResource/LearningPathDetailResource.php` | Detail transformer |
| 9 | `Modules/Training/Http/Controllers/V1/LearningPathController.php` | Controller |

### Backend — Sửa:
| # | File | Mô tả |
|---|------|-------|
| 10 | `Modules/Training/Routes/api.php` | Thêm routes |

### Frontend — Tạo mới:
| # | File | Mô tả |
|---|------|-------|
| 11 | `pages/training/learning-path/components/LearningPathForm.vue` | Form chính (refactor từ add.vue) |
| 12 | `pages/training/learning-path/components/TabInfo.vue` | Tab 1: Thông tin + Builder |
| 13 | `pages/training/learning-path/components/TabResult.vue` | Tab 2: Kết quả |
| 14 | `pages/training/learning-path/components/TabLearners.vue` | Tab 3: Người học |
| 15 | `pages/training/learning-path/components/TabCertificate.vue` | Tab 4: Chứng chỉ |

### Frontend — Sửa:
| # | File | Mô tả |
|---|------|-------|
| 16 | `pages/training/learning-path/add.vue` | Page wrapper tạo mới |
| 17 | `pages/training/learning-path/_id/edit.vue` | Page wrapper sửa |
| 18 | `pages/training/learning-path/_id/index.vue` | Page wrapper xem |
