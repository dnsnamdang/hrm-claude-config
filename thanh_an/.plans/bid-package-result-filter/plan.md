# Bộ lọc Kết quả thầu — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thêm filter "Kết quả thầu" vào màn danh sách gói thầu, lọc theo trường `result` (Trúng thầu / Trượt thầu / Chưa có kết quả).

**Architecture:** Thêm 1 param `result` vào query BE + 1 Select2 dropdown vào filter panel FE. Không cần migration, không cần API mới.

**Tech Stack:** Laravel 8 (PHP 7.4), Nuxt 2 (Vue 2), Bootstrap-Vue, Select2

---

## File Structure

| File | Hành động | Mô tả |
|------|-----------|-------|
| `Modules/Category/Services/BidPackageService.php` | Modify (dòng ~113) | Thêm `->when()` filter `result` |
| `pages/bid_package/bid_package/index.vue` | Modify (dòng ~418-432, ~481-497, ~136-146) | Thêm `result` vào form, options, template |

---

### Task 1: BE — Thêm filter `result` vào `BidPackageService::index()`

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Services/BidPackageService.php:112-114`

- [x] **Step 1: Thêm `->when()` cho param `result`**

Trong hàm `index()`, thêm đoạn sau **ngay sau** dòng `->when($request->employee_id, ...)` (dòng 112-114) và **trước** dòng `->when(!empty($statusFilters), ...)` (dòng 115):

```php
->when($request->result !== null && $request->result !== '', function ($query) use ($request) {
    if ($request->result == 0) {
        return $query->whereNull('result');
    }
    return $query->where('result', $request->result);
})
```

Kết quả sau khi sửa, đoạn dòng 112-120 sẽ là:

```php
->when($request->employee_id, function ($query) use ($request) {
    return $query->where('employee_id', $request->employee_id);
})
->when($request->result !== null && $request->result !== '', function ($query) use ($request) {
    if ($request->result == 0) {
        return $query->whereNull('result');
    }
    return $query->where('result', $request->result);
})
->when(!empty($statusFilters), function ($query) use ($statusFilters) {
    return $query->whereIn('status', $statusFilters);
})
```

- [ ] **Step 2: Verify BE** (chờ user test)

Gọi thử API qua browser hoặc Postman:
- `GET /api/v1/category/bid_packages?result=1` → chỉ trả về gói thầu trúng thầu
- `GET /api/v1/category/bid_packages?result=2` → chỉ trả về gói thầu trượt thầu
- `GET /api/v1/category/bid_packages?result=0` → chỉ trả về gói thầu chưa có kết quả (result = null)
- `GET /api/v1/category/bid_packages` (không truyền result) → trả về tất cả (không filter)

---

### Task 2: FE — Thêm Select2 filter "Kết quả thầu" vào `index.vue`

**Files:**
- Modify: `hrm-thanhan-client/pages/bid_package/bid_package/index.vue:418-432, 481-497, 136-146`

- [x] **Step 1: Thêm `result` vào `initialStateForm`**

Tại dòng ~418-432, thêm `result: undefined` vào object `initialStateForm`:

```js
const initialStateForm = {
    page: 1,
    per_page: 10,
    customer_id: undefined,
    status: undefined,
    created_by: undefined,
    from_time: undefined,
    to_time: undefined,
    main_company_id: undefined,
    project_id: undefined,
    quotation_id: undefined,
    employee_id: undefined,
    customer_code: undefined,
    province_id: undefined,
    result: undefined,
}
```

- [x] **Step 2: Thêm mảng `results` vào `data()`**

Tại dòng ~481-497, thêm mảng `results` ngay sau mảng `statuses`:

```js
results: [
    { id: 1, text: 'Trúng thầu' },
    { id: 2, text: 'Trượt thầu' },
    { id: 0, text: 'Chưa có kết quả' },
],
```

- [x] **Step 3: Thêm Select2 vào template**

Tại dòng ~136-146, thêm Select2 **ngay sau** filter "Nhân viên thực hiện" và **trước** div chứa nút "Đặt lại" / "Áp dụng":

```html
<div class="col-md-3 search-filter">
    <Select2
        v-select2-focus
        :settings="{ allowClear: true }"
        v-model="formFilter.result"
        :options="results"
        placeholder="Kết quả thầu"
        v-on:keyup.enter="searchAndSave"
    />
</div>
```

- [ ] **Step 4: Verify FE**

Mở trình duyệt → vào màn danh sách gói thầu → mở Bộ lọc:
1. Chọn "Trúng thầu" → bấm Áp dụng → danh sách chỉ hiện gói thầu trúng
2. Chọn "Trượt thầu" → bấm Áp dụng → danh sách chỉ hiện gói thầu trượt
3. Chọn "Chưa có kết quả" → bấm Áp dụng → danh sách hiện gói thầu chưa khai báo kết quả
4. Bấm "Đặt lại" → filter về trống, danh sách hiện tất cả
5. Kết hợp filter kết quả thầu + filter khác (vd: Trạng thái) → hoạt động đúng
