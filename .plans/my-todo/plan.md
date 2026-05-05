# My To Do — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tao trang My To Do trong module Assign, aggregate Task/Issue/Meeting/Request + CRUD Todo ca nhan voi danh sach va sub-task.

**Architecture:** Unified API query truc tiep cac entity he thong, normalize ve format chung. 2 bang DB moi cho Personal Todo. FE layout 2 cot voi calendar sidebar.

**Tech Stack:** Laravel 8 (PHP 7.4), Nuxt 2 (Vue 2), Bootstrap-Vue, MySQL

---

## Phase 0: Brainstorming & Design
- [x] Brainstorm requirements
- [x] Viet spec chi tiet
- [x] Review & confirm voi user
- [x] Thiet ke UI tren Pencil (2 man hinh)

---

## Phase 1: Database — Migration + Entity

### Task 1: Migration `personal_todo_lists`

**Files:**
- Create: `hrm-api/Modules/Assign/Database/Migrations/2026_04_30_000001_create_personal_todo_lists_table.php`

- [ ] **Step 1: Tao migration**

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreatePersonalTodoListsTable extends Migration
{
    public function up()
    {
        Schema::create('personal_todo_lists', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->unsignedBigInteger('user_id');
            $table->string('name', 255);
            $table->text('description')->nullable();
            $table->integer('sort_order')->default(0);
            $table->unsignedBigInteger('company_id')->nullable();
            $table->timestamps();
            $table->unsignedBigInteger('created_by')->nullable();
            $table->unsignedBigInteger('updated_by')->nullable();

            $table->index('user_id');
            $table->index('company_id');
        });
    }

    public function down()
    {
        Schema::dropIfExists('personal_todo_lists');
    }
}
```

- [ ] **Step 2: Chay migration**

Run: `cd hrm-api && php artisan migrate`
Expected: table `personal_todo_lists` duoc tao thanh cong

---

### Task 2: Migration `personal_todos`

**Files:**
- Create: `hrm-api/Modules/Assign/Database/Migrations/2026_04_30_000002_create_personal_todos_table.php`

- [ ] **Step 1: Tao migration**

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreatePersonalTodosTable extends Migration
{
    public function up()
    {
        Schema::create('personal_todos', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->unsignedBigInteger('list_id');
            $table->unsignedBigInteger('parent_id')->nullable();
            $table->unsignedBigInteger('user_id');
            $table->string('title', 500);
            $table->text('description')->nullable();
            $table->date('due_date')->nullable();
            $table->time('due_time')->nullable();
            $table->tinyInteger('is_completed')->default(0);
            $table->dateTime('completed_at')->nullable();
            $table->integer('sort_order')->default(0);
            $table->unsignedBigInteger('company_id')->nullable();
            $table->timestamps();
            $table->unsignedBigInteger('created_by')->nullable();
            $table->unsignedBigInteger('updated_by')->nullable();

            $table->foreign('list_id')->references('id')->on('personal_todo_lists')->onDelete('cascade');
            $table->index('user_id');
            $table->index('list_id');
            $table->index('parent_id');
            $table->index('due_date');
            $table->index('company_id');
        });
    }

    public function down()
    {
        Schema::dropIfExists('personal_todos');
    }
}
```

- [ ] **Step 2: Chay migration**

Run: `cd hrm-api && php artisan migrate`
Expected: table `personal_todos` duoc tao thanh cong

---

### Task 3: Entity `PersonalTodoList`

**Files:**
- Create: `hrm-api/Modules/Assign/Entities/MyTodo/PersonalTodoList.php`

- [ ] **Step 1: Tao model**

```php
<?php

namespace Modules\Assign\Entities\MyTodo;

use App\Models\BaseModel;

class PersonalTodoList extends BaseModel
{
    protected $table = 'personal_todo_lists';

    protected $fillable = [
        'user_id',
        'name',
        'description',
        'sort_order',
        'company_id',
        'created_by',
        'updated_by',
    ];

    protected $casts = [
        'user_id' => 'integer',
        'sort_order' => 'integer',
        'company_id' => 'integer',
    ];

    public function todos()
    {
        return $this->hasMany(PersonalTodo::class, 'list_id')
            ->whereNull('parent_id')
            ->orderBy('sort_order');
    }

    public function allTodos()
    {
        return $this->hasMany(PersonalTodo::class, 'list_id');
    }
}
```

---

### Task 4: Entity `PersonalTodo`

**Files:**
- Create: `hrm-api/Modules/Assign/Entities/MyTodo/PersonalTodo.php`

- [ ] **Step 1: Tao model**

```php
<?php

namespace Modules\Assign\Entities\MyTodo;

use App\Models\BaseModel;

class PersonalTodo extends BaseModel
{
    protected $table = 'personal_todos';

    protected $fillable = [
        'list_id',
        'parent_id',
        'user_id',
        'title',
        'description',
        'due_date',
        'due_time',
        'is_completed',
        'completed_at',
        'sort_order',
        'company_id',
        'created_by',
        'updated_by',
    ];

    protected $casts = [
        'list_id' => 'integer',
        'parent_id' => 'integer',
        'user_id' => 'integer',
        'is_completed' => 'integer',
        'sort_order' => 'integer',
        'company_id' => 'integer',
    ];

    protected $dates = [
        'due_date',
        'completed_at',
    ];

    public function todoList()
    {
        return $this->belongsTo(PersonalTodoList::class, 'list_id');
    }

    public function subItems()
    {
        return $this->hasMany(PersonalTodo::class, 'parent_id')
            ->orderBy('sort_order');
    }

    public function parent()
    {
        return $this->belongsTo(PersonalTodo::class, 'parent_id');
    }
}
```

---

## Phase 2: Backend — CRUD Personal Todo

### Task 5: FormRequest classes

**Files:**
- Create: `hrm-api/Modules/Assign/Http/Requests/MyTodo/StorePersonalTodoListRequest.php`
- Create: `hrm-api/Modules/Assign/Http/Requests/MyTodo/UpdatePersonalTodoListRequest.php`
- Create: `hrm-api/Modules/Assign/Http/Requests/MyTodo/StorePersonalTodoRequest.php`
- Create: `hrm-api/Modules/Assign/Http/Requests/MyTodo/UpdatePersonalTodoRequest.php`

- [ ] **Step 1: StorePersonalTodoListRequest**

```php
<?php

namespace Modules\Assign\Http\Requests\MyTodo;

use Modules\Training\Http\Requests\BaseRequest;

class StorePersonalTodoListRequest extends BaseRequest
{
    public function rules()
    {
        return [
            'name' => 'required|string|max:255',
            'description' => 'nullable|string',
        ];
    }

    public function messages()
    {
        return [
            'name.required' => 'Ten danh sach khong duoc de trong',
            'name.max' => 'Ten danh sach toi da 255 ky tu',
        ];
    }
}
```

- [ ] **Step 2: UpdatePersonalTodoListRequest** — giong StorePersonalTodoListRequest

- [ ] **Step 3: StorePersonalTodoRequest**

```php
<?php

namespace Modules\Assign\Http\Requests\MyTodo;

use Modules\Training\Http\Requests\BaseRequest;

class StorePersonalTodoRequest extends BaseRequest
{
    public function rules()
    {
        return [
            'list_id' => 'required|integer|exists:personal_todo_lists,id',
            'parent_id' => 'nullable|integer|exists:personal_todos,id',
            'title' => 'required|string|max:500',
            'description' => 'nullable|string',
            'due_date' => 'nullable|date',
            'due_time' => 'nullable|date_format:H:i',
        ];
    }

    public function messages()
    {
        return [
            'title.required' => 'Tieu de khong duoc de trong',
            'list_id.required' => 'Phai chon danh sach',
            'list_id.exists' => 'Danh sach khong ton tai',
        ];
    }
}
```

- [ ] **Step 4: UpdatePersonalTodoRequest** — giong Store nhung `list_id` la `nullable`

---

### Task 6: Resource classes

**Files:**
- Create: `hrm-api/Modules/Assign/Transformers/MyTodoResource/PersonalTodoListResource.php`
- Create: `hrm-api/Modules/Assign/Transformers/MyTodoResource/PersonalTodoResource.php`
- Create: `hrm-api/Modules/Assign/Transformers/MyTodoResource/MyTodoItemResource.php`

- [ ] **Step 1: PersonalTodoListResource**

```php
<?php

namespace Modules\Assign\Transformers\MyTodoResource;

use Modules\Human\Transformers\ApiResource;

class PersonalTodoListResource extends ApiResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'description' => $this->description,
            'sort_order' => $this->sort_order,
            'todo_count' => $this->allTodos()->whereNull('parent_id')->count(),
            'completed_count' => $this->allTodos()->whereNull('parent_id')->where('is_completed', 1)->count(),
        ];
    }
}
```

- [ ] **Step 2: PersonalTodoResource**

```php
<?php

namespace Modules\Assign\Transformers\MyTodoResource;

use Modules\Human\Transformers\ApiResource;
use App\Helpers\Helper;

class PersonalTodoResource extends ApiResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'list_id' => $this->list_id,
            'parent_id' => $this->parent_id,
            'title' => $this->title,
            'description' => $this->description,
            'due_date' => $this->due_date ? $this->due_date->format('Y-m-d') : null,
            'due_time' => $this->due_time,
            'is_completed' => $this->is_completed,
            'completed_at' => Helper::formatDateTime($this->completed_at),
            'sort_order' => $this->sort_order,
            'sub_items' => $this->whenLoaded('subItems', function () {
                return PersonalTodoResource::collection($this->subItems);
            }),
        ];
    }
}
```

- [ ] **Step 3: MyTodoItemResource** — resource chuan hoa cho unified list

```php
<?php

namespace Modules\Assign\Transformers\MyTodoResource;

use Illuminate\Http\Resources\Json\JsonResource;

class MyTodoItemResource extends JsonResource
{
    public function toArray($request): array
    {
        return $this->resource;
    }
}
```

---

### Task 7: MyTodoService — CRUD Personal Todo

**Files:**
- Create: `hrm-api/Modules/Assign/Services/MyTodo/MyTodoService.php`

- [ ] **Step 1: Tao service voi CRUD methods cho Personal Todo**

```php
<?php

namespace Modules\Assign\Services\MyTodo;

use Modules\Assign\Entities\MyTodo\PersonalTodoList;
use Modules\Assign\Entities\MyTodo\PersonalTodo;
use Carbon\Carbon;

class MyTodoService
{
    // --- Personal Todo Lists ---

    public function getLists($userId)
    {
        return PersonalTodoList::where('user_id', $userId)
            ->orderBy('sort_order')
            ->get();
    }

    public function getOrCreateDefaultList($userId)
    {
        $list = PersonalTodoList::where('user_id', $userId)->first();
        if (!$list) {
            $list = PersonalTodoList::create([
                'user_id' => $userId,
                'name' => 'Mac dinh',
                'sort_order' => 0,
                'company_id' => auth()->user()->company_id ?? null,
                'created_by' => $userId,
            ]);
        }
        return $list;
    }

    public function storeList($data, $userId)
    {
        $maxSort = PersonalTodoList::where('user_id', $userId)->max('sort_order') ?? 0;
        return PersonalTodoList::create(array_merge($data, [
            'user_id' => $userId,
            'sort_order' => $maxSort + 1,
            'company_id' => auth()->user()->company_id ?? null,
            'created_by' => $userId,
        ]));
    }

    public function updateList($id, $data, $userId)
    {
        $list = PersonalTodoList::where('id', $id)->where('user_id', $userId)->firstOrFail();
        $list->update(array_merge($data, ['updated_by' => $userId]));
        return $list;
    }

    public function destroyList($id, $userId)
    {
        $list = PersonalTodoList::where('id', $id)->where('user_id', $userId)->firstOrFail();
        $list->delete();
    }

    // --- Personal Todos ---

    public function getTodosByList($listId, $userId)
    {
        $list = PersonalTodoList::where('id', $listId)->where('user_id', $userId)->firstOrFail();
        $todos = PersonalTodo::where('list_id', $listId)
            ->whereNull('parent_id')
            ->with('subItems')
            ->orderBy('is_completed')
            ->orderBy('sort_order')
            ->get();

        return [
            'list' => $list,
            'todos' => $todos,
            'stats' => [
                'total' => $todos->count(),
                'completed' => $todos->where('is_completed', 1)->count(),
                'pending' => $todos->where('is_completed', 0)->count(),
            ],
        ];
    }

    public function storeTodo($data, $userId)
    {
        if (!empty($data['parent_id'])) {
            $parent = PersonalTodo::where('id', $data['parent_id'])
                ->where('user_id', $userId)
                ->whereNull('parent_id')
                ->firstOrFail();
        }

        $maxSort = PersonalTodo::where('list_id', $data['list_id'])
            ->where('parent_id', $data['parent_id'] ?? null)
            ->max('sort_order') ?? 0;

        return PersonalTodo::create(array_merge($data, [
            'user_id' => $userId,
            'sort_order' => $maxSort + 1,
            'company_id' => auth()->user()->company_id ?? null,
            'created_by' => $userId,
        ]));
    }

    public function updateTodo($id, $data, $userId)
    {
        $todo = PersonalTodo::where('id', $id)->where('user_id', $userId)->firstOrFail();
        $todo->update(array_merge($data, ['updated_by' => $userId]));
        return $todo;
    }

    public function toggleTodo($id, $userId)
    {
        $todo = PersonalTodo::where('id', $id)->where('user_id', $userId)->firstOrFail();
        $todo->update([
            'is_completed' => $todo->is_completed ? 0 : 1,
            'completed_at' => $todo->is_completed ? null : Carbon::now(),
            'updated_by' => $userId,
        ]);
        return $todo;
    }

    public function destroyTodo($id, $userId)
    {
        $todo = PersonalTodo::where('id', $id)->where('user_id', $userId)->firstOrFail();
        PersonalTodo::where('parent_id', $id)->delete();
        $todo->delete();
    }

    public function reorderTodos($items, $userId)
    {
        foreach ($items as $item) {
            PersonalTodo::where('id', $item['id'])
                ->where('user_id', $userId)
                ->update(['sort_order' => $item['sort_order']]);
        }
    }
}
```

---

### Task 8: MyTodoController — CRUD routes

**Files:**
- Create: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/MyTodoController.php`
- Modify: `hrm-api/Modules/Assign/Routes/api.php` — them routes

- [ ] **Step 1: Tao controller**

```php
<?php

namespace Modules\Assign\Http\Controllers\Api\V1;

use App\Http\Controllers\ApiController;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\DB;
use Modules\Assign\Services\MyTodo\MyTodoService;
use Modules\Assign\Http\Requests\MyTodo\StorePersonalTodoListRequest;
use Modules\Assign\Http\Requests\MyTodo\UpdatePersonalTodoListRequest;
use Modules\Assign\Http\Requests\MyTodo\StorePersonalTodoRequest;
use Modules\Assign\Http\Requests\MyTodo\UpdatePersonalTodoRequest;
use Modules\Assign\Transformers\MyTodoResource\PersonalTodoListResource;
use Modules\Assign\Transformers\MyTodoResource\PersonalTodoResource;

class MyTodoController extends ApiController
{
    protected $myTodoService;

    public function __construct(MyTodoService $myTodoService)
    {
        $this->myTodoService = $myTodoService;
    }

    // --- Lists ---

    public function listLists()
    {
        $userId = auth()->id();
        $this->myTodoService->getOrCreateDefaultList($userId);
        $lists = $this->myTodoService->getLists($userId);
        return $this->responseJson('success', Response::HTTP_OK, PersonalTodoListResource::collection($lists));
    }

    public function storeList(StorePersonalTodoListRequest $request)
    {
        try {
            $list = $this->myTodoService->storeList($request->validated(), auth()->id());
            return $this->responseJson('success', Response::HTTP_OK, new PersonalTodoListResource($list));
        } catch (\Exception $e) {
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function updateList(UpdatePersonalTodoListRequest $request, $id)
    {
        try {
            $list = $this->myTodoService->updateList($id, $request->validated(), auth()->id());
            return $this->responseJson('success', Response::HTTP_OK, new PersonalTodoListResource($list));
        } catch (\Exception $e) {
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function destroyList($id)
    {
        try {
            $this->myTodoService->destroyList($id, auth()->id());
            return $this->responseJson('success', Response::HTTP_OK);
        } catch (\Exception $e) {
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    // --- Todos ---

    public function listTodosByList($listId)
    {
        $result = $this->myTodoService->getTodosByList($listId, auth()->id());
        return $this->responseJson('success', Response::HTTP_OK, [
            'list' => new PersonalTodoListResource($result['list']),
            'todos' => PersonalTodoResource::collection($result['todos']),
            'stats' => $result['stats'],
        ]);
    }

    public function storeTodo(StorePersonalTodoRequest $request)
    {
        try {
            $todo = $this->myTodoService->storeTodo($request->validated(), auth()->id());
            return $this->responseJson('success', Response::HTTP_OK, new PersonalTodoResource($todo));
        } catch (\Exception $e) {
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function updateTodo(UpdatePersonalTodoRequest $request, $id)
    {
        try {
            $todo = $this->myTodoService->updateTodo($id, $request->validated(), auth()->id());
            return $this->responseJson('success', Response::HTTP_OK, new PersonalTodoResource($todo));
        } catch (\Exception $e) {
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function toggleTodo($id)
    {
        try {
            $todo = $this->myTodoService->toggleTodo($id, auth()->id());
            return $this->responseJson('success', Response::HTTP_OK, new PersonalTodoResource($todo));
        } catch (\Exception $e) {
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function destroyTodo($id)
    {
        try {
            $this->myTodoService->destroyTodo($id, auth()->id());
            return $this->responseJson('success', Response::HTTP_OK);
        } catch (\Exception $e) {
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }

    public function reorderTodos(Request $request)
    {
        try {
            $this->myTodoService->reorderTodos($request->input('items', []), auth()->id());
            return $this->responseJson('success', Response::HTTP_OK);
        } catch (\Exception $e) {
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }
}
```

- [ ] **Step 2: Them routes vao `api.php`**

Them vao cuoi file `hrm-api/Modules/Assign/Routes/api.php`:

```php
// My Todo
Route::group(['prefix' => 'my-todo'], function () {
    Route::get('/', [MyTodoController::class, 'index']);
    // Lists
    Route::get('/lists', [MyTodoController::class, 'listLists']);
    Route::post('/lists', [MyTodoController::class, 'storeList']);
    Route::put('/lists/{id}', [MyTodoController::class, 'updateList']);
    Route::delete('/lists/{id}', [MyTodoController::class, 'destroyList']);
    // Todos
    Route::get('/lists/{listId}/todos', [MyTodoController::class, 'listTodosByList']);
    Route::post('/todos', [MyTodoController::class, 'storeTodo']);
    Route::put('/todos/{id}', [MyTodoController::class, 'updateTodo']);
    Route::patch('/todos/{id}/toggle', [MyTodoController::class, 'toggleTodo']);
    Route::delete('/todos/{id}', [MyTodoController::class, 'destroyTodo']);
    Route::patch('/todos/reorder', [MyTodoController::class, 'reorderTodos']);
});
```

- [ ] **Step 3: Test API CRUD bang Postman/curl**

Run: `cd hrm-api && php artisan route:list --path=my-todo`
Expected: 11 routes hien thi dung

---

## Phase 3: Backend — Unified API (Aggregator)

### Task 9: MyTodoService — Aggregator methods

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/MyTodo/MyTodoService.php` — them cac method aggregate

- [ ] **Step 1: Them method `getAssignedTasks()`**

```php
public function getAssignedTasks($userId)
{
    $excludeStatuses = [
        \Modules\Assign\Entities\Task\Task::DRAFT,
        \Modules\Assign\Entities\Task\Task::DONE,
        \Modules\Assign\Entities\Task\Task::CANCELLED,
    ];

    $tasks = \Modules\Assign\Entities\Task\Task::query()
        ->whereNotIn('status', $excludeStatuses)
        ->where(function ($q) use ($userId) {
            $q->where('assignee_id', $userId)
              ->orWhereHas('watchers', function ($w) use ($userId) {
                  $w->where('employee_id', $userId);
              })
              ->orWhere(function ($q2) use ($userId) {
                  $q2->where('approver_id', $userId)
                      ->where('status', \Modules\Assign\Entities\Task\Task::PENDING_APPROVAL);
              });
        })
        ->select('id', 'name', 'due_date', 'due_time', 'status', 'priority', 'assignee_id', 'approver_id')
        ->with(['assignee:id,name', 'solution:id,name'])
        ->get();

    return $tasks->map(function ($task) use ($userId) {
        $source = 'watching';
        if ($task->assignee_id == $userId) $source = 'assigned';
        elseif ($task->approver_id == $userId) $source = 'approver';
        return $this->normalizeItem($task, 'task', $source);
    });
}
```

- [ ] **Step 2: Them method `getAssignedIssues()`**

```php
public function getAssignedIssues($userId)
{
    $excludeStatuses = ['closed', 'completed', 'rejected'];

    $issues = \Modules\Assign\Entities\Issue::query()
        ->whereNotIn('status', $excludeStatuses)
        ->where(function ($q) use ($userId) {
            $q->where('assignee_id', $userId)
              ->orWhereHas('watchers', function ($w) use ($userId) {
                  $w->where('employee_id', $userId);
              });
        })
        ->select('id', 'title', 'due_date', 'due_time', 'status', 'priority', 'assignee_id')
        ->get();

    return $issues->map(function ($issue) use ($userId) {
        $source = $issue->assignee_id == $userId ? 'assigned' : 'watching';
        return $this->normalizeItem($issue, 'issue', $source);
    });
}
```

- [ ] **Step 3: Them method `getUpcomingMeetings()`**

```php
public function getUpcomingMeetings($userId)
{
    $meetings = \Modules\Assign\Entities\Meeting\Meeting::query()
        ->whereIn('status', [
            \Modules\Assign\Entities\Meeting\Meeting::LEN_LICH,
            \Modules\Assign\Entities\Meeting\Meeting::CHOT_LICH,
        ])
        ->where('start_date', '>=', Carbon::today())
        ->whereHas('company_members', function ($q) use ($userId) {
            $q->where('employee_id', $userId);
        })
        ->select('id', 'name', 'start_date', 'end_date', 'status', 'location')
        ->withCount('company_members')
        ->get();

    return $meetings->map(function ($meeting) {
        return $this->normalizeItem($meeting, 'meeting', 'participant');
    });
}
```

- [ ] **Step 4: Them method `getPendingApprovals()`**

```php
public function getPendingApprovals($userId)
{
    $items = collect();

    // AssignRequest
    $requests = \Modules\Assign\Entities\AssignRequest::query()
        ->where('approver', $userId)
        ->where('status', \Modules\Assign\Entities\AssignRequest::CHO_DUYET)
        ->select('id', 'code', 'title', 'type', 'status', 'created_at')
        ->get();

    foreach ($requests as $req) {
        $items->push($this->normalizeItem($req, 'request', 'approver'));
    }

    // JobRequest
    $jobRequests = \Modules\Assign\Entities\JobRequest::query()
        ->where('approver', $userId)
        ->where('status', \Modules\Assign\Entities\JobRequest::CHO_DUYET)
        ->select('id', 'code', 'title', 'deadline', 'status')
        ->get();

    foreach ($jobRequests as $jr) {
        $items->push($this->normalizeItem($jr, 'request', 'approver'));
    }

    return $items;
}
```

- [ ] **Step 5: Them method `normalizeItem()`**

```php
protected function normalizeItem($entity, $type, $source)
{
    $statusMap = $this->getStatusText($entity, $type);

    $item = [
        'type' => $type,
        'id' => $entity->id,
        'title' => $this->getTitle($entity, $type),
        'due_date' => $this->getDueDate($entity, $type),
        'due_time' => $this->getDueTime($entity, $type),
        'status_text' => $statusMap['text'],
        'status_color' => $statusMap['color'],
        'source' => $source,
        'source_text' => $this->getSourceText($source),
        'url' => $this->getUrl($entity, $type),
        'priority' => $entity->priority ?? null,
    ];

    if ($type === 'task') {
        $item['project_name'] = optional($entity->solution)->name;
        $item['assignee_name'] = optional($entity->assignee)->name;
    }

    if ($type === 'meeting') {
        $item['location'] = $entity->location;
        $item['member_count'] = $entity->company_members_count ?? null;
    }

    return $item;
}

protected function getTitle($entity, $type)
{
    switch ($type) {
        case 'task': return $entity->name;
        case 'issue': return $entity->title;
        case 'meeting': return $entity->name;
        case 'request': return ($entity->code ?? '') . ' — ' . ($entity->title ?? '');
        case 'personal': return $entity->title;
        default: return '';
    }
}

protected function getDueDate($entity, $type)
{
    switch ($type) {
        case 'meeting': return $entity->start_date ? Carbon::parse($entity->start_date)->format('Y-m-d') : null;
        case 'request': return $entity->deadline ? Carbon::parse($entity->deadline)->format('Y-m-d') : null;
        default: return $entity->due_date ? Carbon::parse($entity->due_date)->format('Y-m-d') : null;
    }
}

protected function getDueTime($entity, $type)
{
    if ($type === 'meeting') return $entity->start_time ?? null;
    if ($type === 'request') return null;
    return $entity->due_time ?? null;
}

protected function getSourceText($source)
{
    $map = [
        'assigned' => 'Duoc giao',
        'watching' => 'Theo doi',
        'approver' => 'Can duyet',
        'participant' => 'Tham gia',
        'personal' => 'Ca nhan',
    ];
    return $map[$source] ?? $source;
}

protected function getUrl($entity, $type)
{
    $map = [
        'task' => '/assign/task/',
        'issue' => '/assign/issue/',
        'meeting' => '/assign/meeting/',
        'request' => '/assign/assign_request/',
    ];
    return isset($map[$type]) ? $map[$type] . $entity->id : null;
}

protected function getStatusText($entity, $type)
{
    // Map status -> text + color cho tung loai entity
    // Day la logic cu the, can doc STATUS constants tu tung entity
    // Tra ve ['text' => '...', 'color' => '...']
    // Implement chi tiet khi code — doc Task::STATUS, Issue statuses, Meeting::STATUS, etc.
    return ['text' => '', 'color' => 'secondary'];
}
```

---

### Task 10: MyTodoService — method `getAll()` + `getCalendarSummary()`

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/MyTodo/MyTodoService.php`

- [ ] **Step 1: Them `getAll()`**

```php
public function getAll($filters, $userId)
{
    $items = collect();

    // Aggregate tu cac nguon
    if (!isset($filters['type']) || str_contains($filters['type'] ?? '', 'task')) {
        $items = $items->merge($this->getAssignedTasks($userId));
    }
    if (!isset($filters['type']) || str_contains($filters['type'] ?? '', 'issue')) {
        $items = $items->merge($this->getAssignedIssues($userId));
    }
    if (!isset($filters['type']) || str_contains($filters['type'] ?? '', 'meeting')) {
        $items = $items->merge($this->getUpcomingMeetings($userId));
    }
    if (!isset($filters['type']) || str_contains($filters['type'] ?? '', 'request')) {
        $items = $items->merge($this->getPendingApprovals($userId));
    }
    if (!isset($filters['type']) || str_contains($filters['type'] ?? '', 'personal')) {
        $items = $items->merge($this->getPersonalTodosNormalized($userId));
    }

    // De-duplicate: neu cung entity + cung id, uu tien source: assigned > approver > watching
    $items = $this->deduplicateItems($items);

    // Filter by source
    if (!empty($filters['source'])) {
        $items = $items->filter(fn($i) => $i['source'] === $filters['source']);
    }

    // Filter by date range
    if (!empty($filters['date_from'])) {
        $items = $items->filter(fn($i) => $i['due_date'] && $i['due_date'] >= $filters['date_from']);
    }
    if (!empty($filters['date_to'])) {
        $items = $items->filter(fn($i) => $i['due_date'] && $i['due_date'] <= $filters['date_to']);
    }

    // Filter overdue
    $today = Carbon::today()->format('Y-m-d');
    if (isset($filters['is_overdue']) && $filters['is_overdue']) {
        $items = $items->filter(fn($i) => $i['due_date'] && $i['due_date'] < $today);
    }

    // Sort: due_date ASC, null cuoi
    $items = $items->sort(function ($a, $b) {
        if (is_null($a['due_date']) && is_null($b['due_date'])) return 0;
        if (is_null($a['due_date'])) return 1;
        if (is_null($b['due_date'])) return -1;
        return strcmp($a['due_date'], $b['due_date']);
    })->values();

    // Calendar summary
    $month = $filters['month'] ?? Carbon::now()->format('Y-m');
    $calendarSummary = $this->getCalendarSummary($items, $month);

    // Lists
    $this->getOrCreateDefaultList($userId);
    $lists = $this->getLists($userId);

    return [
        'items' => $items,
        'calendar_summary' => $calendarSummary,
        'lists' => $lists,
    ];
}

protected function getPersonalTodosNormalized($userId)
{
    $todos = PersonalTodo::where('user_id', $userId)
        ->whereNull('parent_id')
        ->where('is_completed', 0)
        ->with(['subItems', 'todoList'])
        ->orderBy('sort_order')
        ->get();

    return $todos->map(function ($todo) {
        $item = $this->normalizeItem($todo, 'personal', 'personal');
        $item['list_id'] = $todo->list_id;
        $item['list_name'] = optional($todo->todoList)->name;
        $item['sub_items'] = $todo->subItems->map(fn($s) => [
            'id' => $s->id,
            'title' => $s->title,
            'is_completed' => (bool) $s->is_completed,
        ])->values();
        return $item;
    });
}

protected function deduplicateItems($items)
{
    $priority = ['assigned' => 1, 'approver' => 2, 'watching' => 3, 'participant' => 4, 'personal' => 5];
    $grouped = $items->groupBy(fn($i) => $i['type'] . '_' . $i['id']);

    return $grouped->map(function ($group) use ($priority) {
        return $group->sortBy(fn($i) => $priority[$i['source']] ?? 99)->first();
    })->values();
}

public function getCalendarSummary($items, $month)
{
    $summary = [];
    foreach ($items as $item) {
        if (!$item['due_date']) continue;
        if (substr($item['due_date'], 0, 7) === $month) {
            $day = $item['due_date'];
            $summary[$day] = ($summary[$day] ?? 0) + 1;
        }
    }
    return $summary;
}
```

---

### Task 11: MyTodoController — method `index()`

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/MyTodoController.php`

- [ ] **Step 1: Them method `index()`**

```php
public function index(Request $request)
{
    $filters = $request->only(['type', 'source', 'date_from', 'date_to', 'is_completed', 'is_overdue', 'list_id', 'month']);
    $result = $this->myTodoService->getAll($filters, auth()->id());

    return $this->responseJson('success', Response::HTTP_OK, [
        'items' => $result['items'],
        'calendar_summary' => $result['calendar_summary'],
        'lists' => PersonalTodoListResource::collection($result['lists']),
    ]);
}
```

- [ ] **Step 2: Test API unified list**

Run: `curl -H "Authorization: Bearer {token}" http://localhost:8000/api/v1/assign/my-todo`
Expected: tra ve JSON voi items, calendar_summary, lists

---

## Phase 4: Frontend — Trang chinh

### Task 12: index.vue — Layout + API call

**Files:**
- Create: `hrm-client/pages/assign/my-todo/index.vue`

- [ ] **Step 1: Tao trang chinh voi layout 2 cot, goi API, render data**

Component chinh voi:
- `data()`: items, calendarSummary, lists, filters, loading
- `mounted()`: goi `loadData()`
- `methods.loadData()`: `this.$store.dispatch('apiGet', 'assign/my-todo' + query)`
- Template: 2 cot — `TodoMainList` (trai) + `TodoCalendarSidebar` (phai)
- Stats row inline
- Filter bar voi 3 select

---

### Task 13: TodoFilterBar.vue

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/TodoFilterBar.vue`

- [ ] **Step 1: Component filter voi 3 dropdown + nut "Tao todo"**

Props: `filters` (object)
Emit: `@filter-change`, `@add-todo`
3 select: Loai (task/issue/meeting/request/personal), Vai tro (assigned/watching/approver), Trang thai (chua xong/da xong/tat ca)

---

### Task 14: TodoGroupHeader.vue

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/TodoGroupHeader.vue`

- [ ] **Step 1: Component header nhom thoi gian**

Props: `group` (string: overdue/today/tomorrow/this_week/next_week/later/no_deadline), `count` (number)
Render: icon + ten nhom + so luong, mau do cho overdue

---

### Task 15: TodoItem.vue

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/TodoItem.vue`

- [ ] **Step 1: Component 1 item trong danh sach**

Props: `item` (object)
Emit: `@toggle`, `@click-item`
Render:
- Thanh mau trai (3px) theo type
- Title + tag loai + tag source
- Metadata row (status, project, assignee)
- Due date/time
- Mui ten navigate (chi system entity)
- Checkbox (chi personal todo)
- Sub-items (chi personal todo)
Click: navigate cho system entity, inline edit cho personal

---

### Task 16: TodoSubItem.vue

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/TodoSubItem.vue`

- [ ] **Step 1: Component sub-task**

Props: `subItem` (object)
Emit: `@toggle`
Render: checkbox + title, strike-through khi completed

---

### Task 17: TodoMainList.vue

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/TodoMainList.vue`

- [ ] **Step 1: Component danh sach chinh, nhom items theo thoi gian**

Props: `items` (array)
Computed: `groupedItems` — nhom items theo 7 nhom thoi gian (overdue, today, tomorrow, this_week, next_week, later, no_deadline)
Render: loop qua cac nhom, moi nhom co TodoGroupHeader + danh sach TodoItem

---

### Task 18: TodoCalendarSidebar.vue

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/TodoCalendarSidebar.vue`

- [ ] **Step 1: Component mini calendar + danh sach ca nhan**

Props: `calendarSummary` (object), `lists` (array)
Emit: `@select-date`, `@select-list`, `@add-list`
Render:
- Calendar thang: grid 7 cot, highlight today, dot cho ngay co item
- Click ngay -> emit filter
- Danh sach ca nhan: ten list + count, click -> emit
- Nut "Tao danh sach"

---

### Task 19: TodoFormModal.vue

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/TodoFormModal.vue`

- [ ] **Step 1: Modal tao/sua todo ca nhan**

Props: `show` (boolean), `todo` (object nullable), `lists` (array)
Emit: `@save`, `@close`
Fields: title (required), description (optional), list_id (select), due_date (datepicker), due_time (timepicker)

---

### Task 20: Menu sidebar

**Files:**
- Modify: `hrm-client/components/assign-components/assign-slidebar.vue`

- [ ] **Step 1: Them menu "My To Do" vao vi tri dau tien**

Them item moi vao `menuItems` array, truoc item "Tong quan":

```javascript
{
    id: 100,
    label: 'My To Do',
    link: '/assign/my-todo',
    icon: 'ri-checkbox-circle-line',
    isShow: true,
},
```

---

## Phase 5: Frontend — Man chi tiet danh sach

### Task 21: TodoListDetail.vue

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/TodoListDetail.vue`

- [ ] **Step 1: Component man chi tiet 1 danh sach ca nhan**

Hien thi khi user click vao 1 list tren sidebar.
- Header: ten list + mo ta + nut sua/xoa
- Danh sach todos voi checkbox + sub-items
- Input "Them viec moi" o cuoi
- API: `GET assign/my-todo/lists/{listId}/todos`
- CRUD: POST/PUT/DELETE/PATCH toggle

---

### Task 22: TodoListFormModal.vue

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/TodoListFormModal.vue`

- [ ] **Step 1: Modal tao/sua danh sach**

Props: `show`, `list` (object nullable)
Fields: name (required), description (optional)
API: POST/PUT `assign/my-todo/lists`

---

### Task 23: Ket noi index.vue voi TodoListDetail

**Files:**
- Modify: `hrm-client/pages/assign/my-todo/index.vue`

- [ ] **Step 1: Them logic chuyen doi giua man chinh va man chi tiet danh sach**

Data: `selectedListId` (null = man chinh, co gia tri = man chi tiet)
Khi click list tren sidebar -> set selectedListId -> render TodoListDetail thay cho TodoMainList
Khi click "My To Do" tren breadcrumb -> reset selectedListId -> ve man chinh

---

## Phase 6: Test + Polish

### Task 24: Test toan bo flow

- [ ] **Step 1: Test man chinh** — mo `/assign/my-todo`, xac nhan hien thi items tu cac entity
- [ ] **Step 2: Test filter** — loc theo loai, vai tro, trang thai
- [ ] **Step 3: Test calendar** — click ngay, xac nhan filter
- [ ] **Step 4: Test CRUD todo** — tao, sua, xoa, toggle complete
- [ ] **Step 5: Test sub-task** — tao sub-task, toggle
- [ ] **Step 6: Test CRUD list** — tao, sua, xoa danh sach
- [ ] **Step 7: Test man chi tiet list** — click list, xem todos, them moi, toggle
- [ ] **Step 8: Test edge cases** — user chua co list, todo khong co deadline, xoa list co todos
- [ ] **Step 9: Test navigate** — click item he thong, xac nhan chuyen sang trang chi tiet dung

---

## Phase 7: UI Polish theo Pencil Design

### Task 25: Trạng thái hiển thị đúng Pencil + drag-drop danh sách
- [x] BE: Thêm `role_text`, `role_color`, `role_bg` vào `normalizeItem()` — badge vai trò (Được giao/Tham gia/Cần duyệt/Theo dõi/Cá nhân)
- [x] BE: Thêm method `getRoleInfo()` + cập nhật `getSourceText()` (thêm participant, approver, watching)
- [x] BE: Meeting source `'assigned'` → `'participant'`
- [x] BE: `getStatusText()` giữ Bootstrap color, sửa Issue `in_progress` → warning, Meeting Lên lịch/Chốt lịch → success, Personal → 'Việc cần làm'
- [x] FE TodoItem: Row 1 — thay `tag-type` (Task/Issue...) bằng **role badge pill** (vai trò + màu inline)
- [x] FE TodoItem: Row 2 — status badge có **border + background** theo Bootstrap color (`.status-primary/success/warning/danger/info/secondary`) + dot separator giữa meta
- [x] FE TodoItem: Title font-weight 600, bỏ màu đỏ title overdue (chỉ giữ đỏ ở ngày hạn)
- [x] FE TodoItem: Hiển thị giờ (due_time) thay vì ngày khi item hôm nay
- [x] FE TodoGroupHeader: Ngày mai → amber, Tuần này → teal (theo design Pencil)
- [x] FE index.vue: Xóa 3 dòng console.log debug
- [x] FE TodoCalendarSidebar: Drag-drop danh sách cá nhân (vuedraggable + handle icon)
- [x] FE index.vue: `onReorderLists()` optimistic update + API call
- [x] BE: Route `POST /lists/reorder` + controller `reorderLists()` + service `reorderLists()`
- [x] FE: Fix `apiPostMethod` gửi `payload` thay vì `data`

---

## Phase 9: Bug Fix + UX Enhancement (session 5)

### Task 29: Đổi tên UI
- [x] Menu sidebar: "My To Do" → "Lịch làm việc của tôi"
- [x] Page title + breadcrumb
- [x] Button "Tạo todo" → "Tạo nhắc việc cá nhân"
- [x] Modal title: "Tạo nhắc việc cá nhân" / "Chỉnh sửa nhắc việc cá nhân"
- [x] Toast messages

### Task 30: Cho phép sửa nhắc việc cá nhân
- [x] Màn chính: click vào personal todo → mở form sửa
- [x] Màn chính: thêm nút edit action cho personal todo
- [x] Màn danh sách cá nhân: thêm nút sửa (icon bút) cho pending + completed todos
- [x] Forward event edit-todo → index.vue mở TodoFormModal

### Task 31: Confirm hoàn thành bằng BaseConfirmModal
- [x] Thay confirm() native bằng BaseConfirmModal (đúng mẫu project)
- [x] Áp dụng cho cả màn chính và màn danh sách cá nhân
- [x] Checkbox dùng @click.prevent thay @change (ngăn toggle visual trước confirm)

### Task 32: Fix reload sau khi lưu
- [x] Tạo nhắc việc mới: await loadData() + loadLists()
- [x] Sửa nhắc việc: reload TodoListDetail khi đang ở màn danh sách
- [x] Sửa tên danh sách: reload TodoListDetail
- [x] Fix lỗi 422 due_time (cắt HH:mm:ss → HH:mm khi load vào form)

### Task 33: Sắp xếp theo thời gian
- [x] Trong mỗi group box, sort items theo due_date + due_time tăng dần

### Task 34: Hiển thị sub-items đồng nhất
- [x] BE aggregator: eager load subItems, trả sub_items trong normalizeItem
- [x] FE màn danh sách cá nhân: completed todos hiển thị sub-items
- [x] Forward event toggle-sub từ TodoItem → TodoMainList → index.vue

### Task 35: Cascade toggle logic (kiểu Google Tasks)
- [x] BE: Check parent → tất cả sub-items hoàn thành theo
- [x] BE: Bỏ check parent → tất cả sub-items bỏ hoàn thành
- [x] BE: Check sub-item cuối → parent tự hoàn thành
- [x] BE: Bỏ check 1 sub-item → parent bỏ hoàn thành
- [x] FE: toggle sub-item hiện confirm popup

---

## Phase 8: Tài liệu SRS + Test Cases

### Task 26: SRS Document
- [x] Tạo SRS markdown: `docs/srs/my-todo.md` (10 sections đầy đủ)
- [x] Tạo SRS HTML: `docs/srs/my-todo.html` (bao gồm sơ đồ Use Case SVG + 5 Swimlane Diagrams + ERD)
- [x] Cập nhật SKILL.md srs-documenter: bổ sung yêu cầu sơ đồ Use Case, Swimlane + output .html

### Task 27: Test Cases
- [x] Tạo testcase HTML: `docs/srs/my-todo-testcases.html` (95 test cases, 6 sections)
- [x] Tạo testcase Excel generator: `docs/srs/my-todo-generate-testcase.py`
- [x] Generate file Excel: `docs/srs/my-todo-testcases.xlsx` (94 test cases, 11 sections)

### Task 28: Skill testcase-documenter
- [x] Tạo `.claude/skills/testcase-documenter/SKILL.md` — hướng dẫn generate test case Excel + HTML cho mọi feature

---

## Checkpoint

### Checkpoint — 2026-05-04 (session 5)
Vừa hoàn thành: Phase 9 — Bug fix + UX Enhancement (Task 29-35): đổi tên UI, sửa nhắc việc, confirm popup BaseConfirmModal, fix reload, sort theo thời gian, sub-items đồng nhất, cascade toggle logic
Đang làm dở: không
Bước tiếp theo: Test toàn bộ flow trên trình duyệt (Phase 6)
Blocked: không

### Checkpoint — 2026-05-02 (session 4)
Vừa hoàn thành: Phase 8 — Tài liệu SRS (HTML + sơ đồ) + Test Cases (HTML + Excel) + Skill testcase-documenter
Đang làm dở: Phase 6 (Test) — chưa test thực tế trên trình duyệt
Bước tiếp theo: Test toàn bộ flow trên trình duyệt theo 94 test cases đã viết
Blocked: không

### Checkpoint — 2026-05-02 (session 3)
Vừa hoàn thành: Phase 7 — UI Polish theo Pencil Design (status badge, role badge, drag-drop danh sách, group header colors)
Đang làm dở: Phase 6 (Test) — chưa test đầy đủ
Bước tiếp theo: Test toàn bộ flow trên trình duyệt
Blocked: không

### Checkpoint — 2026-04-30 22:55
Vừa hoàn thành: Phase 1-5 (DB + BE CRUD + BE Aggregator + FE trang chính + FE chi tiết danh sách)
Đang làm dở: Phase 6 (Test) — chưa bắt đầu, cần migrate DB và chạy dev server
Bước tiếp theo: Chạy `php artisan migrate` trên hrm-api, start dev server, test toàn bộ flow
Blocked: Chưa run migration
