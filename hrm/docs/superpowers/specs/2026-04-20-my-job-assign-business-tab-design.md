# Spec: Tab "Phiếu công tác" trong "Công việc của tôi"

**Ngày:** 2026-04-20
**Người phụ trách:** @manhcuong
**Module:** Assign
**Trạng thái:** Đã chốt design, chuẩn bị viết plan

---

## 1. Mục tiêu

Đưa màn `Quản lý phiếu giao đi công tác` (`/assign/assign_business?type=all`) vào làm 1 tab
mới trong `/assign/my-job` theo phong cách V2Base giống tab "Giải pháp". Tính năng giữ
nguyên như màn cũ, khác biệt lớn: chỉ hiển thị **phiếu liên quan đến user đăng nhập**,
UI dùng V2Base.

## 2. Scope

### Trong phạm vi
- Thêm 1 tab mới "Phiếu công tác" vào `/assign/my-job` (vị trí sau Meeting, trước Chờ duyệt).
- Tạo endpoint BE mới riêng cho "phiếu công tác của tôi" (không dùng lại `/assign/assign_business?type=all`).
- Port toàn bộ 13 hành động row-level, filter, xuất Excel, tạo mới từ màn cũ sang UI V2Base.
- Hỗ trợ `column-customization-modal` giống tab Giải pháp (table key: `my_job_assign_business`).
- Giữ các modal: ExtendTime, EndSoon, ConfirmCancelApprove, ConfirmDeleteSelected, ExportModal.

### Ngoài phạm vi
- Không sửa `AssignBusinessController`, `AssignBusinessService`, model `AssignRequest`.
- Không chạm schema / migration.
- Không thêm permission master mới (scope đã giới hạn theo user).
- Không port các `type` khác (`waiting`, `waiting-payment-profile`, `waiting-payment-business`).

## 3. Định nghĩa "phiếu của tôi"

Một phiếu (entity `AssignRequest`, `type = PHIEU_CONG_TAC`) thuộc về user đăng nhập khi:
- `created_by = auth()->user()->id`, HOẶC
- Tồn tại bản ghi `AssignRequestEmployee` với `assign_request_id = phiếu.id` và
  `employee_id = auth()->user()->id` (bao gồm trưởng nhóm + nhân viên tham gia).

## 4. Backend

### 4.1 Route mới

File: `hrm-api/Modules/Assign/Routes/api.php`, group `/assign/my-job`:

```php
Route::get('/assign-business-list', [MyJobController::class, 'assignBusinessList']);
Route::get('/assign-business-list/export', [MyJobController::class, 'exportAssignBusinesses']);
```

### 4.2 Controller

File: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/MyJobController.php` — thêm 2 method:

- `assignBusinessList(Request $request)` → `apiGetList(MyJobAssignBusinessResource::apiPaginate(...))`
- `exportAssignBusinesses(Request $request)` → `Excel::download(new MyJobAssignBusinessExport(...), 'phieu_cong_tac_cua_toi.xls')`

Cả 2 bọc try/catch + Log::error theo convention.

### 4.3 Service

File: `hrm-api/Modules/Assign/Services/MyJobService.php` — thêm 1 method builder chính
(tái sử dụng cho cả list + export):

```php
public function getAssignBusinessList(Request $request)
{
    $userId = auth()->user()->id;

    $query = AssignRequest::query()
        ->where('type', AssignRequest::PHIEU_CONG_TAC)
        ->where(function ($q) use ($userId) {
            $q->where('created_by', $userId)
              ->orWhereHas('employees', fn ($q2) => $q2->where('employee_id', $userId));
        });

    // Ẩn nháp của người khác — chỉ hiển thị nháp khi chính mình tạo
    $query->where(function ($q) use ($userId) {
        $q->where('status', '!=', AssignRequest::DANG_TAO)
          ->orWhere('created_by', $userId);
    });

    // Filter
    $query->when($request->keyword, fn ($q) =>
        $q->where('code', 'like', '%' . escapeLikeKeyword($request->keyword) . '%')
    );
    $query->when($request->business_type, fn ($q) =>
        $q->where('business_type', $request->business_type)
    );
    $query->when($request->status, function ($q) use ($request) {
        $statuses = is_array($request->status)
            ? $request->status
            : explode(',', $request->status);
        $q->whereIn('status', $statuses);
    });
    $query->when($request->customer_id, fn ($q) =>
        $q->where('customer_id', $request->customer_id)
    );
    $query->when($request->contract_code, fn ($q) =>
        $q->where(function ($q2) use ($request) {
            $q2->where('contract_code', 'like', '%' . $request->contract_code . '%')
               ->orWhereHas('assignBusinessTasks', fn ($q3) =>
                   $q3->where('wr_service_contract_code', 'like', '%' . $request->contract_code . '%'));
        })
    );
    $query->when($request->parent_code, function ($q) use ($request) {
        $needle = escapeLikeKeyword($request->parent_code);
        $wrIds = TpWrAssignTask::where('code', 'like', "%$needle%")->pluck('id')->toArray();
        $jobIds = JobRequest::where('code', 'like', "%$needle%")->pluck('id')->toArray();

        $q->where(function ($q2) use ($needle, $wrIds, $jobIds) {
            $q2->where('parent_code', 'like', "%$needle%")
               ->orWhereHas('assignBusinessTasks', function ($q3) use ($wrIds, $jobIds) {
                   $q3->where(function ($q4) use ($wrIds, $jobIds) {
                       $q4->where(function ($q5) use ($wrIds) {
                           $q5->whereIn('jobinvoiceable_id', $wrIds)
                              ->where('jobinvoiceable_type', TpWrAssignTask::class);
                       })->orWhere(function ($q5) use ($jobIds) {
                           $q5->whereIn('jobinvoiceable_id', $jobIds)
                              ->where('jobinvoiceable_type', JobRequest::class);
                       });
                   });
               });
        });
    });
    $query->when($request->from_time, fn ($q) =>
        $q->whereDate('from_time', '>=', $request->from_time)
    );
    $query->when($request->to_time, fn ($q) =>
        $q->whereDate('to_time', '<=', $request->to_time)
    );

    // Sort
    $sortField = in_array($request->sort_field, ['from_time', 'to_time', 'updated_at', 'created_at', 'code'])
        ? $request->sort_field : 'updated_at';
    $sortDir = strtolower($request->sort_dir) === 'asc' ? 'asc' : 'desc';
    $query->orderBy($sortField, $sortDir);

    return $query->with([
        'leaderEmployee.employee.info',
        'assignBusinessTasks',
        'employees',
    ]);
}
```

### 4.4 Resource

Tạo `Modules/Assign/Transformers/MyJobAssignBusinessResource/MyJobAssignBusinessResource.php`
và `MyJobAssignBusinessDetailResource.php` (tách list/detail theo convention).

**Fields của List Resource:**
- `id, code`
- `business_type` (id), `business_type_name`
- `job_invoiceable_links` — array của `{code, id, type, url}` để FE render link (logic
  gom từ helper FE cũ `splitJobInvoiceableData` + `generateLink` được port sang BE —
  xem 4.6)
- `leader_name, leader_phone`
- `customer_code, customer_name, contract_code`
- `created_by_name, updated_at, from_time, to_time`
- `status, status_text, status_color`
- Cờ hành động (khớp màn cũ):
  - `can_edit` — dựa `canEditAssignBusiness`
  - `can_approve` — `canApproveAssignBusiness`
  - `can_import_result` — `canImportResultAssignBusiness`
  - `can_approve_result` — `canApproveResultAssignBusiness`
  - `can_create_payment_profile` — `canCreatePaymentProfile`
  - `can_create_payment_business_request` — `canCreatePaymentBusinessRequest`
  - `can_extend_time` — `canExtendTime`
  - `can_end_soon` — `canEndSoon`
  - `can_add_employee` — `canAddEmployee`
  - `can_add_wr_assign_task` — `canAddWrAssignTask`
  - `can_delete` — same as `can_edit`

Nếu các cờ trên đang được tính ở layer Transformer/Service cũ thì **tách ra helper chung**
trong `AssignRequest` model (ví dụ accessor `is_can_edit`, `is_can_approve`, …) để
Resource mới tái sử dụng, tránh duplicate logic.

### 4.5 Export

File mới: `hrm-api/app/ExcelExport/MyJobAssignBusinessExport.php` — pattern giống
`MyJobSolutionExport`. Cột xuất khớp `fieldsExport` của màn cũ
(`code, business_type_name, jobInvoiceableCode, leader, customer_name, contract_code,
created_by, updated_at, status`).

### 4.6 Helper BE cho link phiếu giao việc/đề xuất

Hiện tại logic `generateLink` nằm ở FE (màn cũ). Để Resource trả trực tiếp URL cho FE
mới, port helper này sang BE tại `Modules/Assign/Helper/AssignBusinessHelper.php`:

```php
public static function generateJobInvoiceableLink(string $code, int $id): string
{
    if (Str::startsWith($code, 'TPE.PGV.') || Str::startsWith($code, 'TPSG.PGV.')) {
        return env('ERP_URL') . "/admin/customer-care/wr_assign_tasks/{$id}/show";
    }
    if (Str::startsWith($code, 'PGV')) {
        return "/assign/assign_jobs/{$id}/show";
    }
    return "/assign/job_requests/{$id}/show";
}
```

## 5. Frontend

### 5.1 Wiring tab mới vào index.vue

File: `hrm-client/pages/assign/my-job/index.vue`:
- Import `AssignBusinessTab` from `./components/AssignBusinessTab.vue`.
- Thêm vào `tabs` array giữa Meeting và Chờ duyệt:
  ```js
  { key: 'assign-business', label: 'Phiếu công tác', icon: 'ri-briefcase-line' },
  ```
- Thêm render `<AssignBusinessTab v-else-if="activeTab === 'assign-business'" />`.
- Thêm `'assign-business'` vào `validTabs` trong `mounted()`.

### 5.2 Component mới AssignBusinessTab.vue

File: `hrm-client/pages/assign/my-job/components/AssignBusinessTab.vue`. Cấu trúc copy
template từ `SolutionsTab.vue`, thay data/logic.

**Data:**
```js
const initialStateForm = {
    keyword: undefined,
    business_type: undefined,
    status: undefined,
    customer_id: undefined,
    contract_code: undefined,
    parent_code: undefined,
    from_time: undefined,
    to_time: undefined,
    sort_field: 'updated_at',
    sort_dir: 'desc',
}
```

`pagination` snake-case-ish như SolutionsTab (currentPage, pageSize, total, totalPages,
from, to).

**Options:**
- `business_types` — hardcode `[{id:1, text:'Phiếu công tác kỹ thuật'}, {id:2, text:'Phiếu công tác khác'}]` (khớp màn cũ)
- `statuses` — 6 trạng thái: 1 Đang tạo, 2 Chờ duyệt, 3 Đã duyệt, 5 Chờ duyệt kết quả,
  6 Không duyệt, 7 Đã duyệt kết quả
- Khách hàng — live search qua `assign/meeting/getListCustomer?q=...` (dùng lại pattern
  SolutionsTab)

**Bảng (8 cột, dùng `column-customization-modal` table=`my_job_assign_business`):**

| # | key | label | mặc định isVisible |
|---|------|-------|---------|
| 1 | `index` | STT | true |
| 2 | `codeInfo` | Số phiếu (title `code`, sub: Loại CT + Cập nhật) | true |
| 3 | `jobInvoiceable` | Phiếu giao việc/đề xuất (multi-link render) | true |
| 4 | `customerInfo` | Khách hàng (title `customer_name/code`, sub: Hợp đồng) | true |
| 5 | `leaderInfo` | Trưởng nhóm (title `leader_name`, sub: SĐT + Người tạo) | true |
| 6 | `scheduleInfo` | Ngày đi CT (`from_time → to_time`) | true |
| 7 | `status` | Trạng thái (V2BaseBadge) | true |
| 8 | `updated_at` | Ngày sửa | false (ẩn mặc định) |

**Filter nâng cao (grid 3-4 cột):**
- Quick search: Số phiếu (tìm trên `code`)
- Loại công tác (V2BaseSelect)
- Trạng thái (V2BaseSelect — multi `allowClear`)
- Khách hàng (V2BaseInput + dropdown live search — port pattern từ SolutionsTab)
- Số hợp đồng (V2BaseInput)
- Phiếu giao việc/đề xuất (V2BaseInput, gộp 3 mã)
- Từ ngày (V2BaseDatePicker → map sang `from_time`)
- Đến ngày (V2BaseDatePicker → map sang `to_time`)

**Header actions:**
- Tạo mới → `/assign/assign_business/add?from=my-job&tab=assign-business`
- Xuất Excel → GET `/api/v1/assign/my-job/assign-business-list/export` với filter hiện tại,
  tải file `phieu_cong_tac_cua_toi.xls`
- Cấu hình cột → mở `column-customization-modal`

**Row actions (dropdown ⋯):** 13 item, chỉ render khi cờ tương ứng true:
1. Xem → `/assign/assign_business/{id}/show?from=my-job&tab=assign-business` (luôn hiện)
2. Sửa → `/assign/assign_business/{id}?…` (can_edit)
3. Xóa → open `modal-delete-selected` (can_delete)
4. Duyệt → `/assign/assign_business/{id}/approve?…` (can_approve)
5. Từ chối → open `modal-confirm-cancel-approve` (can_approve)
6. Nhập kết quả → `/assign/assign_business/{id}/import_result?…` (can_import_result)
7. Duyệt kết quả → `/assign/assign_business/{id}/approve_result?…` (can_approve_result)
8. Lập hồ sơ thanh toán → `/assign/payment_profile/create?assign_business_id={id}&from=my-job&tab=assign-business` (can_create_payment_profile)
9. Lập đề nghị thanh toán → `/assign/payment_business_request/create?…` (can_create_payment_business_request)
10. Gia hạn → flow kiểm tra `assign/extend-end-soon-request/check` rồi navigate (can_extend_time)
11. Kết thúc sớm → tương tự (can_end_soon)
12. Thêm nhân viên → `/assign/assign_business/{id}/add-employee?…` (can_add_employee)
13. Thêm phiếu giao việc → `/assign/assign_business/{id}/add-wr-assign-task?…` (can_add_wr_assign_task)

**Modal tái sử dụng (import từ file cũ):**
- `@/components/modal/confirm-delete-selected`
- `@/components/modal/confirm-cancel-approve`
- `@/components/modals/assign_business/ExtendTimeModal`
- `@/components/modals/assign_business/EndSoonModal`
- `@/components/modal/export-modal` — CHÚ Ý: màn cũ dùng `export-modal` cho phép chọn cột
  xuất. Trong tab mới **giữ nguyên flow này** (mở modal → chọn cột → submit), tái sử
  dụng `fieldsExport` copy từ màn cũ.

### 5.3 `from=my-job&tab=assign-business`

Mọi navigation từ tab này truyền query string đó để các màn detail/edit/add biết nguồn
điều hướng và trả về đúng tab khi bấm "Quay lại".

## 6. Không thay đổi

- Schema DB: không.
- Model `AssignRequest`: chỉ thêm accessor `is_can_*` nếu logic hiện chưa gom trong model (xem 4.4).
- `AssignBusinessController` / `AssignBusinessService`: không.
- Permission master: không.
- Menu sidebar: không (tab nằm trong trang my-job đã có).

## 7. Edge case

- **Filter status multi-select**: màn cũ cho chọn 1 status (Select2 single). Tab mới giữ
  single-select để đơn giản; BE đã hỗ trợ `whereIn` để sau này mở rộng.
- **Phiếu nháp (`status = DANG_TAO`)**: chỉ hiện nếu `created_by = me` — khớp pattern
  của `getSolutionList` trong my-job.
- **Phiếu đã chuyển trạng thái sang thanh toán (8, 9)**: không có ở dropdown status của
  màn cũ nhưng vẫn có thể tồn tại. Tab mới thêm vào options (hoặc phơi trong badge thôi
  nếu user không lọc được).
- **Xuất Excel lượng lớn**: dùng `Excel::download` synchronous (giống màn cũ). Không
  queue vì data đã được limit theo "của tôi".
- **Nhân viên có nhiều phiếu (user trả phiếu trùng)**: `whereHas('employees',…)` đã dedupe
  tự nhiên ở cấp `AssignRequest`.

## 8. Downstream impact

- FE: `pages/assign/my-job/index.vue` (thêm tab), tạo mới `AssignBusinessTab.vue`.
- BE: thêm route + 2 method controller + 1 method service + 2 Resource class + 1 Export
  class + (nếu cần) helper link + accessor cờ `is_can_*` trong model AssignRequest.
- Không ảnh hưởng màn cũ `/assign/assign_business` vì dùng endpoint riêng.
- `column-customization-modal` — thêm 1 table key mới `my_job_assign_business`, seeder
  mặc định (nếu có) không bắt buộc (fallback vào `allColumns` khi DB chưa có).

## 9. UX chi tiết

- Sort: cột `Ngày sửa` + `Số phiếu` + `Ngày đi CT` có icon sort.
- Empty state: "Không có phiếu công tác nào phù hợp bộ lọc."
- Loading: spinner của `V2BaseDataTable`.
- Toast lỗi: `$toasted.global.error` khi API fail (pattern SolutionsTab).
- Pagination: `per_page` mặc định 10, options `[10, 25, 50, 100]`.
- Responsive: tái sử dụng `v2-styles.scss` — mobile sẽ auto-wrap filter thành 1-2 cột.

## 10. Testcases

Theo feedback memory "testcase end-user only": viết test case UI theo góc nhìn người
dùng cuối **sau khi** implementation xong. Không viết test BE/API trừ khi user yêu cầu.
