# Filter NV màn Chấm dứt HĐLĐ hiển thị cả người đã nghỉ việc — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) hoặc superpowers:executing-plans để thực thi plan theo từng task. Step dùng checkbox (`- [ ]`).

**Goal:** Cho dropdown filter "Nhân viên" trên màn `decision/termination-labor-contract/index` hiển thị cả nhân viên đã nghỉ việc (không chỉ đang làm việc).

**Architecture:** Hướng A — endpoint riêng cho màn này. BE thêm 1 route + 1 method trả toàn bộ `employee_infos` bất kể `status`. FE bind Select2 vào data local nạp từ endpoint này thay vì state Vuex toàn cục (vốn chỉ chứa người đang làm việc, dùng chung mọi màn).

**Tech Stack:** Laravel 8 (Module Decision), Nuxt 2 / Vue 2 + bootstrap-vue, Select2.

**Lưu ý dự án:** Không có test harness tự động cho BE/FE → kiểm thử thủ công qua browser. Không commit/push (theo CLAUDE.md, chỉ commit khi user yêu cầu).

---

## Phase 1 — Backend (Module Decision)

**Files:**
- Modify: `hrm-api/Modules/Decision/Http/Controllers/V1/TerminationLaborContractController.php`
- Modify: `hrm-api/Modules/Decision/Routes/api.php` (group `termination-labor-contract`, dòng ~378-387)

- [x] **Step 1: Thêm import `EmployeeInfo` vào controller**

File `TerminationLaborContractController.php`, khối `use` đầu file (sau dòng `use Modules\Human\Helper\Helper;` ~dòng 22), thêm:

```php
use App\Models\EmployeeInfo;
```

- [x] **Step 2: Thêm method `employeeOptions()` vào controller**

Thêm method này vào trong class `TerminationLaborContractController` (vd ngay sau `index()`):

```php
    /**
     * Danh sách nhân viên cho filter màn Chấm dứt HĐLĐ.
     * Trả TOÀN BỘ employee_infos (gồm cả người đã nghỉ việc) — KHÔNG lọc status,
     * khác với state global employeeInfoOptions vốn chỉ chứa người đang làm việc.
     */
    public function employeeOptions()
    {
        try {
            $data = EmployeeInfo::select('id', 'code', 'fullname')
                ->orderBy('id', 'desc')
                ->get();

            return response()->json(['data' => $data]);
        } catch (Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
        }
    }
```

- [x] **Step 3: Thêm route `GET /employee-options`**

File `Modules/Decision/Routes/api.php`, trong group `termination-labor-contract`. Đặt route mới **TRƯỚC** route `/{terminationLaborContract}` để không bị route param nuốt. Sửa thành:

```php
    Route::group(['prefix' => 'termination-labor-contract'], function () {
        Route::get('/', [TerminationLaborContractController::class, 'index']);
        Route::get('/employee-options', [TerminationLaborContractController::class, 'employeeOptions']);
        Route::get('/export', [TerminationLaborContractController::class, 'export']);
        Route::post('/', [TerminationLaborContractController::class, 'store'])->middleware('checkPermission:Quản lý quyết định');
        Route::put('/{terminationLaborContract}', [TerminationLaborContractController::class, 'update'])->middleware('checkPermission:Quản lý quyết định');
        Route::get('/{terminationLaborContract}', [TerminationLaborContractController::class, 'show']);
        Route::delete('/{terminationLaborContract}', [TerminationLaborContractController::class, 'destroy'])->middleware('checkPermission:Quản lý quyết định');
        Route::put('/{terminationLaborContract}/toggle-approve', [TerminationLaborContractController::class, 'toggleApprove'])->middleware('checkPermission:Duyệt quyết định|Xem xét quyết định');
        Route::get('/{terminationLaborContract}/print', [TerminationLaborContractController::class, 'print']);
    });
```

(Không gắn `checkPermission` — đồng nhất với route `index`/`export`.)

- [ ] **Step 4: Verify endpoint trả dữ liệu**

Mở browser DevTools (đã đăng nhập, có token) hoặc gọi qua app, request:
`GET /api/v1/decision/termination-labor-contract/employee-options`
Expected: JSON `{ "data": [ { "id":..., "code":"...", "fullname":"..." }, ... ] }`, và **có chứa** ít nhất 1 nhân viên đã nghỉ việc (`status != 1`).

---

## Phase 2 — Frontend

**Files:**
- Modify: `hrm-client/pages/decision/termination-labor-contract/index.vue`

- [x] **Step 5: Thêm data local `employeeFilterOptions`**

Trong `data()` (sau `rankOptions: [],` ~dòng 387), thêm:

```js
            employeeFilterOptions: [],
```

- [x] **Step 6: Đổi computed `employeeInfoOptions` trỏ vào data local**

Trong `computed`, sửa:

```js
        employeeInfoOptions() {
            return this.$store.state.employeeInfoOptions
        },
```

thành:

```js
        employeeInfoOptions() {
            return this.employeeFilterOptions
        },
```

- [x] **Step 7: Thêm method `fetchEmployeeFilterOptions()`**

Trong `methods`, thêm method (vd sau `getNumericalOrder,`):

```js
        async fetchEmployeeFilterOptions() {
            const { data } = await this.$store.dispatch(
                'apiGetMethod',
                'decision/termination-labor-contract/employee-options'
            )
            this.employeeFilterOptions = (data || []).map((e) => ({
                text: e.code + ' - ' + e.fullname,
                id: e.id,
            }))
        },
```

- [x] **Step 8: Gọi trong `mounted()`**

Sửa `mounted()`:

```js
    mounted() {
        this.$store.dispatch('optionsSelect/fetchWorkingPositions')
    },
```

thành:

```js
    mounted() {
        this.$store.dispatch('optionsSelect/fetchWorkingPositions')
        this.fetchEmployeeFilterOptions()
    },
```

---

## Phase 3 — Kiểm thử thủ công (browser)

- [ ] **Step 9:** Mở màn `Chấm dứt HĐLĐ` → mở "Bộ lọc" → dropdown "Nhân viên" hiển thị **cả người đã nghỉ việc**.
- [ ] **Step 10:** Chọn 1 người đã nghỉ → Search → ra đúng các QĐ chấm dứt của người đó.
- [ ] **Step 11:** Mở 1 màn decision khác (vd `accept-personnel`) → dropdown nhân viên **vẫn chỉ active** (state global không đổi).
- [ ] **Step 12:** Export Excel + In với filter nhân viên đã nghỉ → ra đúng dữ liệu (các phần này dùng `employee_info_id`, không phụ thuộc nguồn options nên không cần sửa).

---

## Checkpoint — 2026-06-02
Vừa hoàn thành: Phase 1 (BE) + Phase 2 (FE) CODE DONE. BE: `TerminationLaborContractController::employeeOptions()` + route `GET decision/termination-labor-contract/employee-options` (đặt trước `/{terminationLaborContract}`). FE: `index.vue` data `employeeFilterOptions`, computed `employeeInfoOptions` trỏ data local, method `fetchEmployeeFilterOptions()` gọi endpoint mới, gọi trong `mounted()`. Đã review đọc code thực tế: đúng spec.
Đang làm dở: (không)
Bước tiếp theo: Phase 3 — user test thủ công trên browser (Step 9-12).
Blocked:
