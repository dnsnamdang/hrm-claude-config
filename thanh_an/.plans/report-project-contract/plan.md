# BC Tổng hợp Vòng đời DT → HĐ — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Xây dựng trang báo cáo tổng hợp vòng đời Dự toán → Hợp đồng, mỗi dòng = 1 DT, hiển thị aggregate data qua 4 giai đoạn (DT/BG/GT/HĐ) với popup drill-down và export Excel.

**Architecture:** Single endpoint aggregate tại ProjectController. FE là 1 file Vue dùng `b-table-simple` với grouped headers 2 tầng, `b-modal` cho popup drill-down, ExcelJS cho export. Pattern theo `detail-report/index.vue` hiện có.

**Tech Stack:** PHP 7.4 / Laravel 8, Nuxt 2 / Vue 2, Bootstrap-Vue, ExcelJS, Select2

**Spec:** `docs/superpowers/specs/2026-05-25-report-project-contract-design.md`

---

## File Structure

| File | Action | Mô tả |
|------|--------|-------|
| `hrm-thanhan-api/Modules/Category/Routes/api.php` | Modify | Thêm 2 routes |
| `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/ProjectController.php` | Modify | Thêm `lifecycleReport()` + `lifecycleDetail()` |
| `hrm-thanhan-client/pages/sale/report-project-contract/index.vue` | Create | Trang báo cáo FE hoàn chỉnh |

---

## Task 1: BE — Thêm routes

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Routes/api.php`

- [x] **Step 1: Thêm 2 routes vào nhóm `/projects`**

Tìm block `Route::group(['prefix' => '/projects'], function () {` (khoảng dòng 233). Thêm 2 routes mới **sau** dòng `Route::get('/detail-report', ...)`:

```php
Route::get('/lifecycle-report', [ProjectController::class, 'lifecycleReport']);
Route::get('/{project}/lifecycle-detail', [ProjectController::class, 'lifecycleDetail']);
```

- [x] **Step 2: Verify route**

Chạy: `php artisan route:list --path=projects/lifecycle`
Expected: 2 routes GET hiện ra. ✓ OK

---

## Task 2: BE — Controller method `lifecycleReport`

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/ProjectController.php`

- [x] **Step 1: Thêm method `lifecycleReport` vào ProjectController**

Thêm method sau method `detailReport`. Method này:
- Query `projects` → aggregate qua quotations, bid_packages, contracts
- Dùng subquery để tránh cross-join inflation
- Phân quyền 3 cấp
- Trả paginated data + KPIs

```php
public function lifecycleReport(Request $request)
{
    $perPage = $request->get('per_page', 10);

    $statusMap = [
        1 => 'Đang tạo', 2 => 'Đã duyệt', 3 => 'Đã lập báo giá',
        4 => 'Đã phân công', 5 => 'Đã lập hợp đồng', 6 => 'Đang lập báo giá',
        7 => 'Đã gửi thầu', 8 => 'Đang lập gói thầu', 9 => 'Đã lập gói thầu',
        10 => 'Báo giá đã gửi thầu', 11 => 'Đang thực hiện thầu', 12 => 'Đã chuyển hợp đồng',
        13 => 'Báo giá đã bị hủy', 14 => 'Gói thầu đã bị hủy', 15 => 'Chờ BGĐ duyệt chuyển HĐ',
        16 => 'Đang lập hợp đồng', 17 => 'Hủy dự toán',
    ];

    $projectTypeMap = [
        1 => 'Trong thầu', 2 => 'Ngoài thầu', 3 => 'Nhảy thầu',
        4 => 'Hợp đồng Cho/Tặng', 5 => 'Hợp đồng Đặt/Mượn', 6 => 'Hợp đồng Nguyên tắc',
    ];

    // Subquery: tổng giá trị BG per project
    $bgSub = \DB::raw("(SELECT q.project_id,
        SUM(qtp.amount) as total_bg,
        MIN(q.id) as first_q_id
        FROM quotations q
        LEFT JOIN quotation_tab_products qtp ON qtp.quotation_id = q.id
        GROUP BY q.project_id) bg_agg");

    // Subquery: count + tổng GT per project
    $gtSub = \DB::raw("(SELECT bp.project_id,
        COUNT(DISTINCT bp.id) as bp_count,
        SUM(bpp.amount_bid_package) as total_gt
        FROM bid_packages bp
        LEFT JOIN bid_package_products bpp ON bpp.bid_package_id = bp.id
        GROUP BY bp.project_id) gt_agg");

    // Subquery: count + tổng HĐ per project
    $hdSub = \DB::raw("(SELECT c.project_id,
        COUNT(DISTINCT c.id) as ct_count,
        SUM(cp.amount) as total_hd,
        MIN(c.id) as first_c_id
        FROM contracts c
        LEFT JOIN contract_products cp ON cp.contract_id = c.id
        WHERE c.record_type = 2
        GROUP BY c.project_id) hd_agg");

    $query = \DB::table('projects as p')
        ->leftJoin('employees as e_creator', 'e_creator.id', '=', 'p.created_by')
        ->leftJoin('category_customers as cc', 'cc.id', '=', 'p.customer_id')
        ->leftJoin('customer_areas as ca', 'ca.id', '=', 'cc.customer_area_id')
        ->leftJoin('customer_provinces as cp_prov', 'cp_prov.id', '=', 'cc.customer_province_id')
        ->leftJoinSub($bgSub, 'bg_agg', 'bg_agg.project_id', '=', 'p.id')
        ->leftJoin('quotations as first_q', 'first_q.id', '=', 'bg_agg.first_q_id')
        ->leftJoin('employees as e_bg', 'e_bg.id', '=', 'first_q.created_by')
        ->leftJoinSub($gtSub, 'gt_agg', 'gt_agg.project_id', '=', 'p.id')
        ->leftJoinSub($hdSub, 'hd_agg', 'hd_agg.project_id', '=', 'p.id')
        ->leftJoin('contracts as first_c', 'first_c.id', '=', 'hd_agg.first_c_id')
        ->leftJoin('companies as comp', 'comp.id', '=', 'first_c.main_company_contractor')
        ->select([
            'p.id as project_id',
            'p.code as project_code',
            'p.project_type',
            'p.status',
            'p.created_at as created_date',
            'e_creator.full_name as creator_name',
            'cc.code as customer_code',
            'cc.name as customer_name',
            'ca.name as area',
            'cp_prov.name as province',
            'first_q.code as quotation_code',
            'e_bg.full_name as quotation_employee',
            'first_q.created_at as quotation_date',
            \DB::raw('COALESCE(bg_agg.total_bg, 0) as total_quotation'),
            \DB::raw('COALESCE(gt_agg.bp_count, 0) as bid_package_count'),
            \DB::raw('COALESCE(gt_agg.total_gt, 0) as total_bid_package'),
            \DB::raw('COALESCE(hd_agg.ct_count, 0) as contract_count'),
            \DB::raw('COALESCE(hd_agg.total_hd, 0) as total_contract'),
            'comp.name as company_name',
            'first_c.contract_sign_time as contract_sign_date',
            'first_c.contract_end_time as contract_end_date',
        ]);

    // Phân quyền 3 cấp
    if (isCurrentEmployeeHasPermission("Xem BC vòng đời DT theo tổng công ty")) {
        // Xem tất cả
    } elseif (isCurrentEmployeeHasPermission("Xem BC vòng đời DT theo công ty")) {
        $query->where('p.company_id', auth()->user()->info->company_id);
    } elseif (isCurrentEmployeeHasPermission("Xem BC vòng đời DT theo nhóm nghiệp vụ")) {
        $query->where(function ($q) {
            $q->whereIn('p.created_by', listManageEmployeeIdsByGroup())
                ->orWhere('p.created_by', auth()->user()->id);
        });
    } else {
        $query->where('p.created_by', auth()->user()->id);
    }

    // Filters
    if ($request->filled('company_id')) {
        $query->where('p.company_id', $request->company_id);
    }
    if ($request->filled('project_type')) {
        $query->where('p.project_type', $request->project_type);
    }
    if ($request->filled('status')) {
        $query->where('p.status', $request->status);
    }
    if ($request->filled('customer_id')) {
        $query->where('p.customer_id', $request->customer_id);
    }
    if ($request->filled('employee_id')) {
        $query->where('p.created_by', $request->employee_id);
    }
    if ($request->filled('date_from')) {
        $query->whereDate('p.created_at', '>=', $request->date_from);
    }
    if ($request->filled('date_to')) {
        $query->whereDate('p.created_at', '<=', $request->date_to);
    }
    if ($request->filled('search')) {
        $search = $request->search;
        $query->where(function ($q) use ($search) {
            $q->where('p.code', 'like', "%{$search}%")
                ->orWhere('cc.name', 'like', "%{$search}%");
        });
    }

    $query->orderBy('p.created_at', 'desc');

    $results = $query->paginate($perPage);

    // KPIs (tính trên toàn bộ filtered dataset, không phân trang)
    $kpiQuery = clone $query;
    $kpiQuery = $kpiQuery->getQuery();
    $kpiRaw = \DB::table(\DB::raw("({$kpiQuery->toSql()}) as sub"))
        ->mergeBindings($kpiQuery)
        ->selectRaw('COUNT(*) as total_projects')
        ->selectRaw('SUM(CASE WHEN sub.status = 5 THEN 1 ELSE 0 END) as has_contract_count')
        ->selectRaw('SUM(sub.total_quotation) as total_quotation_value')
        ->selectRaw('SUM(sub.total_contract) as total_contract_value')
        ->first();

    $totalBG = $kpiRaw->total_quotation_value ?: 0;
    $totalHD = $kpiRaw->total_contract_value ?: 0;

    $data = collect($results->items())->map(function ($row) use ($statusMap, $projectTypeMap) {
        $totalBG = floatval($row->total_quotation);
        $totalHD = floatval($row->total_contract);
        $difference = $totalHD - $totalBG;
        $conversionRate = $totalBG > 0 ? $totalHD / $totalBG : 0;

        return [
            'project_id' => $row->project_id,
            'project_code' => $row->project_code,
            'project_type' => $projectTypeMap[$row->project_type] ?? '',
            'product_group' => '',
            'customer_name' => $row->customer_name,
            'customer_code' => $row->customer_code,
            'area' => $row->area,
            'province' => $row->province,
            'creator_name' => $row->creator_name,
            'created_date' => $row->created_date ? date('d/m/Y', strtotime($row->created_date)) : '',
            'quotation_code' => $row->quotation_code,
            'quotation_employee' => $row->quotation_employee,
            'quotation_date' => $row->quotation_date ? date('d/m/Y', strtotime($row->quotation_date)) : '',
            'total_quotation' => $totalBG,
            'bid_package_count' => intval($row->bid_package_count),
            'total_bid_package' => floatval($row->total_bid_package),
            'contract_count' => intval($row->contract_count),
            'total_contract' => $totalHD,
            'company_name' => $row->company_name,
            'contract_sign_date' => $row->contract_sign_date ? date('d/m/Y', strtotime($row->contract_sign_date)) : '',
            'contract_end_date' => $row->contract_end_date ? date('d/m/Y', strtotime($row->contract_end_date)) : '',
            'difference' => $difference,
            'conversion_rate' => round($conversionRate, 4),
            'status' => $row->status,
            'status_label' => $statusMap[$row->status] ?? '',
        ];
    });

    return response()->json([
        'data' => $data,
        'meta' => [
            'total' => $results->total(),
            'per_page' => $results->perPage(),
            'current_page' => $results->currentPage(),
            'last_page' => $results->lastPage(),
        ],
        'kpis' => [
            'total_projects' => intval($kpiRaw->total_projects),
            'has_contract_count' => intval($kpiRaw->has_contract_count),
            'total_quotation_value' => floatval($totalBG),
            'total_contract_value' => floatval($totalHD),
            'conversion_rate' => $totalBG > 0 ? round($totalHD / $totalBG, 4) : 0,
        ],
    ]);
}
```

> **Lưu ý:** Subquery `leftJoinSub` được dùng thay vì join trực tiếp vào bảng product để tránh cross-join inflation khi 1 project có nhiều quotations/contracts. Mỗi subquery GROUP BY project_id trước khi join.

> **Lưu ý 2:** Cột `product_group` (Mảng HH) hiện để trống — cần kiểm tra xem field này nằm ở đâu trong model Project. Có thể là `project_array_product_ids` hoặc relation khác. Sẽ bổ sung khi implement.

- [x] **Step 2: Verify API hoạt động**

Dùng Postman hoặc curl:
```
GET /api/v1/category/projects/lifecycle-report?per_page=5
Authorization: Bearer {token}
```
Expected: JSON response với `data`, `meta`, `kpis`. ✓ OK

---

## Task 3: BE — Controller method `lifecycleDetail` (popup DT)

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/ProjectController.php`

- [x] **Step 1: Thêm method `lifecycleDetail`**

```php
public function lifecycleDetail($projectId)
{
    $project = \DB::table('projects as p')
        ->leftJoin('employees as e_creator', 'e_creator.id', '=', 'p.created_by')
        ->leftJoin('employees as e_approver', 'e_approver.id', '=', 'p.approver_id')
        ->leftJoin('category_customers as cc', 'cc.id', '=', 'p.customer_id')
        ->leftJoin('customer_areas as ca', 'ca.id', '=', 'cc.customer_area_id')
        ->leftJoin('customer_provinces as cp_prov', 'cp_prov.id', '=', 'cc.customer_province_id')
        ->where('p.id', $projectId)
        ->select([
            'p.id', 'p.code', 'p.project_type', 'p.status',
            'p.created_at as created_date',
            'e_creator.full_name as creator_name',
            'e_approver.full_name as approver_name',
            'cc.code as customer_code', 'cc.name as customer_name',
            'ca.name as area', 'cp_prov.name as province',
        ])
        ->first();

    if (!$project) {
        return response()->json(['message' => 'Không tìm thấy dự toán'], 404);
    }

    $projectTypeMap = [
        1 => 'Trong thầu', 2 => 'Ngoài thầu', 3 => 'Nhảy thầu',
        4 => 'Hợp đồng Cho/Tặng', 5 => 'Hợp đồng Đặt/Mượn', 6 => 'Hợp đồng Nguyên tắc',
    ];

    $items = \DB::table('project_products as pp')
        ->leftJoin('products as prod', 'prod.id', '=', 'pp.product_id')
        ->leftJoin('units as u', 'u.id', '=', 'pp.unit_id')
        ->where('pp.project_id', $projectId)
        ->select([
            'prod.code as product_code',
            'prod.name as product_name',
            'u.name as unit_name',
            'pp.qty',
        ])
        ->get();

    return response()->json([
        'data' => [
            'code' => $project->code,
            'project_type' => $projectTypeMap[$project->project_type] ?? '',
            'created_date' => $project->created_date ? date('d/m/Y', strtotime($project->created_date)) : '',
            'creator_name' => $project->creator_name,
            'approver_name' => $project->approver_name,
            'customer_name' => $project->customer_name,
            'customer_code' => $project->customer_code,
            'area' => $project->area,
            'province' => $project->province,
        ],
        'items' => $items,
    ]);
}
```

> **Lưu ý:** Cột `unit_id` trên `project_products` cần kiểm tra tồn tại. Nếu không có, lấy unit từ `products.unit_id`.

---

## Task 4: FE — Tạo trang báo cáo (KPI + Filters + Table + Popup + Export)

**Files:**
- Create: `hrm-thanhan-client/pages/sale/report-project-contract/index.vue`

**Đọc trước khi code:**
- `docs/superpowers/specs/2026-05-25-report-project-contract-design.md` — Section 5, 6, 7
- `pages/sale/detail-report/index.vue` — Reference pattern cho filters, pagination, export
- `docs/shared.md` — Base components (PageHeader, Select2, b-table-simple...)

- [x] **Step 1: Tạo file Vue hoàn chỉnh**

Tạo file `hrm-thanhan-client/pages/sale/report-project-contract/index.vue` với nội dung đầy đủ.

**Template bao gồm:**

1. **PageHeader** — title "BC Vòng đời DT → HĐ"
2. **KPI cards** — 4 cards (Số DT, Tổng BG, Tổng HĐ, % Chuyển đổi)
3. **Filter panel** — collapsible, 8 filters + nút "Xem chi tiết"
4. **Bảng grouped headers** — 2 hàng header (group + columns), toggle detail columns
5. **Pagination** — page select + b-pagination
6. **b-modal** — 1 modal duy nhất cho tất cả popup drill-down

**Script bao gồm:**

- `data()`: formFilter, tableData, kpis, showDetail, modalStack, modalType, modalData...
- `computed`: currentPage, companies, employees
- `mounted()`: getData, getCustomers, getProvinces
- `watch`: formFilter.per_page → reset page + getData
- `methods`:
  - `getData()` — fetch lifecycle-report API
  - `searchAndSave()`, `reset()` — filter actions
  - `getCustomers()`, `getProvinces()` — load filter options
  - `toggleDetail()` — show/hide detail columns
  - `openDTModal(projectId)` — fetch lifecycle-detail, show modal
  - `openGTListModal(projectId, projectCode)` — fetch bid_packages by project
  - `openHDListModal(projectId, projectCode)` — fetch contracts by project
  - `pushGTDetailModal(gtId)` — fetch GT detail
  - `pushHDDetailModal(hdId)` — fetch HĐ detail
  - `popModal()`, `closeModal()` — navigation stack
  - `formatNumber(n)` — format VNĐ
  - `exportExcel()`, `fetchAllPages()`, `generateWorkbook(rows)` — ExcelJS export

**Lưu ý quan trọng khi code:**

- **Grouped headers:** Dùng 2 `<b-tr>` trong `<b-thead>`. Row 1 = group headers với `colspan` dynamic (theo `showDetail`). Row 2 = column headers, cột detail dùng `v-if="showDetail"`.

- **Nhóm "Dự toán"**: Group header `v-if="showDetail"` (ẩn khi thu gọn vì không có cột chính). Colspan = 2 khi mở.

- **Sticky columns:** STT + Mã DT dùng `position: sticky; left: 0` và `left: 50px`.

- **Click cells:** Mã DT → `@click="openDTModal(row.project_id)"`. Số GT → `@click="openGTListModal(row.project_id, row.project_code)"` nếu > 0. Số HĐ → tương tự.

- **Delta cell (Chênh lệch):** `<span :class="row.difference > 0 ? 'text-success' : row.difference < 0 ? 'text-danger' : 'text-muted'">`. Hiển thị `+X đ` hoặc `-X đ` hoặc `±0`.

- **% Chuyển đổi:** Hiển thị text `XX.X%` + mini progress bar (Bootstrap `<b-progress>`).

- **Modal navigation stack:** Array `modalStack`. Mỗi entry = `{ type, data }`. `popModal()` bỏ entry cuối. Template modal switch theo `currentModal.type`:
  - `'dt-detail'` → metadata grid + items table (chỉ SL)
  - `'gt-list'` → bảng DS GT (click → pushGTDetailModal)
  - `'gt-detail'` → metadata + items table (SL, ĐG, TT)
  - `'hd-list'` → bảng DS HĐ (click → pushHDDetailModal)
  - `'hd-detail'` → metadata + items table (SL, ĐG, TT)

- **Export Excel:** Pattern giống `detail-report/index.vue`. Khác: có 2 hàng header (group + columns) với merge cells. Grouped headers dùng background color theo spec (section 5.4). Tất cả 23 cột đều export (bao gồm detail cols).

**Các API calls trong FE:**
```javascript
// Main table
`category/projects/lifecycle-report${buildQuery(this.formFilter)}`

// Popup DT
`category/projects/${projectId}/lifecycle-detail`

// Popup DS GT
`category/bid_packages${buildQuery({ project_id: projectId, per_page: 100 })}`

// Popup chi tiết GT
`category/bid_packages/${gtId}`

// Popup DS HĐ
`category/contracts${buildQuery({ project_id: projectId, per_page: 100, record_type: 2 })}`

// Popup chi tiết HĐ
`category/contracts/${hdId}`
```

- [x] **Step 2: Verify FE hiển thị đúng**

Mở browser → truy cập `/sale/report-project-contract`.
Kiểm tra:
- [x] KPI cards hiện đúng 4 giá trị
- [x] Bảng hiện data với grouped headers
- [x] Toggle "Xem chi tiết" mở/đóng cột phụ
- [x] Nhóm "Dự toán" header ẩn khi thu gọn, hiện khi mở
- [x] Click Mã DT → popup chi tiết DT (chỉ SL, không ĐG/TT)
- [x] Click Số GT → popup DS GT → click mã GT → popup chi tiết GT (có ĐG/TT)
- [x] Click Số HĐ → popup DS HĐ → click mã HĐ → popup chi tiết HĐ (có ĐG/TT)
- [x] Nút "← Quay lại" hoạt động trong popup
- [x] Bộ lọc + Reset hoạt động
- [x] Pagination hoạt động
- [x] Export Excel tạo file đúng format (grouped headers, number format)
- [x] Sticky 2 cột đầu khi scroll ngang

---

## Task 5: Phân quyền — Dùng lại bộ permission "Xem báo cáo chi tiết dự toán"

> **Quyết định:** Dùng lại bộ permission BC chi tiết dự toán (`Xem báo cáo chi tiết dự toán theo ...`, ID 504-506). Logic copy từ `applyProjectDetailReportPermissions()` tại `ProjectController.php:444-457`.

**Permissions sử dụng (đã có sẵn trong DB, KHÔNG cần seed):**
| Permission | ID | Scope |
|---|---|---|
| `Xem báo cáo chi tiết dự toán theo tổng công ty` | 504 | Xem tất cả |
| `Xem báo cáo chi tiết dự toán theo công ty` | 505 | Lọc theo `company_id` |
| `Xem báo cáo chi tiết dự toán theo nhóm nghiệp vụ` | 506 | Nhóm NV + cá nhân |
| _(else — cá nhân)_ | — | Chỉ `created_by` = chính mình |

**Files cần sửa:**

### Step 1: Sửa BE — `lifecycleReport()` trong ProjectController

- [x] **Thay block phân quyền cũ bằng logic giống `applyProjectDetailReportPermissions()`:**

```php
// Phân quyền giống BC chi tiết dự toán (ProjectController.php:444-457)
if (isCurrentEmployeeHasPermission("Xem báo cáo chi tiết dự toán theo tổng công ty")) {
    // Xem tất cả
} elseif (isCurrentEmployeeHasPermission("Xem báo cáo chi tiết dự toán theo công ty")) {
    $query->where('p.company_id', auth()->user()->info->company_id);
} elseif (isCurrentEmployeeHasPermission("Xem báo cáo chi tiết dự toán theo nhóm nghiệp vụ")) {
    $query->where(function ($q) {
        $q->whereIn('p.created_by', listManageEmployeeIdsByGroup())
            ->orWhere('p.created_by', auth()->user()->id);
    });
} else {
    $query->where('p.created_by', auth()->user()->id);
}
```

### Step 2: Sửa FE — Menu `isShow` trong `utils/MenuSale.js`

- [x] **Thêm `isShow` cho menu item báo cáo:**

```javascript
{
    label: 'Báo cáo chi tiết Dự toán -> Hợp đồng',
    link: '/sale/report-project-contract',
    isShow: [
        'Xem báo cáo chi tiết dự toán theo tổng công ty',
        'Xem báo cáo chi tiết dự toán theo công ty',
        'Xem báo cáo chi tiết dự toán theo nhóm nghiệp vụ',
    ],
}
```

### Step 3: Verify end-to-end

- [x] Truy cập `/sale/report-project-contract` với user có permission tổng công ty → thấy tất cả data
- [x] Test với user chỉ có permission công ty → chỉ thấy DT cùng công ty
- [x] Test với user không có permission nào → chỉ thấy DT mình tạo

---

### Checkpoint — 2026-05-25
Vừa hoàn thành: Task 1 (routes), Task 2 (lifecycleReport), Task 3 (lifecycleDetail), Task 4 Step 1 (FE Vue page), Task 5 Step 1 (menu đã có sẵn)
Đang làm dở: Chưa verify trên browser, chưa seed permissions
Bước tiếp theo: User test trên browser → fix lỗi nếu có → seed 3 permissions + gán role admin → verify end-to-end
Blocked: Cần user test FE + seed permissions vào DB

### Checkpoint — 2026-05-27
Vừa hoàn thành: Task 5 Step 1 + Step 2 — sửa phân quyền BE dùng bộ "Xem báo cáo chi tiết dự toán theo ..." (ID 504-506) + thêm isShow vào MenuSale.js
Đang làm dở: Chưa verify end-to-end
Bước tiếp theo: User test trên browser → verify phân quyền hoạt động đúng 3 cấp
Blocked: không

### Checkpoint — 2026-05-27 (hoàn tất)
Vừa hoàn thành: Toàn bộ feature đã verify trên browser — BE 2 endpoints + FE trang báo cáo + grouped headers + popup drill-down + export Excel + phân quyền 3 cấp đều hoạt động đúng
Đang làm dở: không
Bước tiếp theo: Chuyển STATUS.md sang mục Hoàn thành, merge code
Blocked: không

**Ghi chú implement:**
- `project_products` không có `qty` — popup DT chỉ hiển thị mã, tên, đơn vị, mảng HH, model
- `product_group` (Mảng HH) lấy từ `projects.array_product_name` (đã có trên bảng projects)
- Menu item đã có sẵn trong `utils/MenuSale.js` (không cần thêm)
- **Phân quyền:** Dùng lại permission danh sách DT (`Xem danh sách dự toán theo ...`), KHÔNG tạo permission mới. Logic copy từ `ProjectService.php:153-177`, bao gồm cả `TP duyệt báo giá`, `employee_id`, `contract_manager_id`, KH phụ trách

---
---

# Enhancement: Popup DT — Gom hàng hóa 4 phân hệ + Quy đổi ĐVT

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Nâng cấp popup chi tiết dự toán để hiển thị tất cả hàng hóa từ 4 phân hệ (DT/BG/Thầu/HĐ), thêm 3 cột SL (BG/Thầu/HĐ) đã quy đổi về ĐVT chính.

**Architecture:** Sửa method `lifecycleDetail` trong ProjectController — thay query `project_products` bằng UNION 4 bảng, lấy master info từ `products`, quy đổi SL qua `product_package_informations.conversion_factor` dùng `ConversionHelper`. FE thêm 3 cột vào popup `dt-detail`.

**Tech Stack:** PHP 7.4 / Laravel 8, Nuxt 2 / Vue 2, Bootstrap-Vue

**Spec:** `docs/superpowers/specs/2026-05-29-lifecycle-detail-aggregate-products-design.md`

---

## File Structure

| File | Action | Mô tả |
|------|--------|-------|
| `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/ProjectController.php` | Modify | Sửa method `lifecycleDetail` (dòng 774-843) |
| `hrm-thanhan-client/pages/sale/report-project-contract/index.vue` | Modify | Sửa popup `dt-detail` (dòng 487-563) |

---

## Task 6: BE — Sửa method `lifecycleDetail` để gom hàng hóa 4 phân hệ + quy đổi ĐVT

**Files:**
- Modify: `hrm-thanhan-api/Modules/Category/Http/Controllers/Api/V1/ProjectController.php:774-843`

- [x] **Step 1: Thêm import `ConversionHelper`**

Thêm dòng `use` ở đầu file (sau dòng 20, cùng khu vực `use`):

```php
use Modules\Category\Helpers\ConversionHelper;
```

- [x] **Step 2: Thay thế toàn bộ phần query `$items` trong method `lifecycleDetail`**

Thay thế đoạn code từ dòng 813-825 (query `project_products`) bằng logic mới. Giữ nguyên phần query `$project` metadata (dòng 790-811) và phần response format (dòng 827-843).

Thay đoạn:
```php
$items = DB::table('project_products as pp')
    ->where('pp.project_id', $projectId)
    ->select([
        'pp.product_code',
        'pp.internal_code',
        'pp.product_name',
        'pp.unit_name',
        'pp.array_product_name',
        'pp.specification',
        'pp.model',
        'pp.producer_country',
    ])
    ->get();
```

Bằng:
```php
// Bước 1: Lấy entity IDs liên quan
$quotationIds = DB::table('quotations')
    ->where('project_id', $projectId)->pluck('id')->toArray();
$bidPackageIds = DB::table('bid_packages')
    ->where('project_id', $projectId)->pluck('id')->toArray();
$contractIds = DB::table('contracts')
    ->where('project_id', $projectId)
    ->where('record_type', Contract::HOP_DONG)
    ->pluck('id')->toArray();

// Bước 2: UNION DISTINCT product_id từ 4 bảng
$productIdsFromProject = DB::table('project_products')
    ->where('project_id', $projectId)
    ->pluck('product_id')->toArray();

$productIdsFromQuotation = !empty($quotationIds)
    ? DB::table('quotation_tab_products')
        ->whereIn('quotation_id', $quotationIds)
        ->pluck('product_id')->toArray()
    : [];

$productIdsFromBidPackage = !empty($bidPackageIds)
    ? DB::table('bid_package_products')
        ->whereIn('bid_package_id', $bidPackageIds)
        ->pluck('product_id')->toArray()
    : [];

$productIdsFromContract = !empty($contractIds)
    ? DB::table('contract_products')
        ->whereIn('contract_id', $contractIds)
        ->pluck('product_id')->toArray()
    : [];

$allProductIds = collect(array_merge(
    $productIdsFromProject,
    $productIdsFromQuotation,
    $productIdsFromBidPackage,
    $productIdsFromContract
))->unique()->values()->toArray();

if (empty($allProductIds)) {
    $items = [];
} else {
    // Bước 3: Lấy thông tin master từ products + units + array_products
    $products = DB::table('products as p')
        ->leftJoin('units as u', 'u.id', '=', 'p.unit_id')
        ->leftJoin('array_products as ap', 'ap.id', '=', 'p.array_product_id')
        ->whereIn('p.id', $allProductIds)
        ->select([
            'p.id as product_id',
            'p.product_code',
            'p.internal_code',
            'p.product_name',
            'p.unit_id',
            'u.name as unit_name',
            'ap.name as array_product_name',
            'p.specification',
            'p.model',
            'p.producer_country',
        ])
        ->get()
        ->keyBy('product_id');

    // Bước 4: Lấy conversion factors từ product_package_informations
    $packageInfos = DB::table('product_package_informations')
        ->whereIn('product_id', $allProductIds)
        ->whereNull('deleted_at')
        ->select(['product_id', 'unit_id', 'conversion_factor'])
        ->get();

    // Build map: conversionMap[product_id][unit_id] = parsed_coeff
    $conversionMap = [];
    foreach ($packageInfos as $info) {
        $coeff = ConversionHelper::parseConversionFactor($info->conversion_factor);
        if ($coeff > 0) {
            $conversionMap[$info->product_id][$info->unit_id] = $coeff;
        }
    }

    // Bước 5: Lấy SUM(qty) GROUP BY (product_id, unit_id) cho 3 phân hệ
    $qtyQuotation = [];
    if (!empty($quotationIds)) {
        $rows = DB::table('quotation_tab_products')
            ->whereIn('quotation_id', $quotationIds)
            ->select([
                'product_id',
                'unit_id',
                DB::raw('SUM(qty) as total_qty'),
            ])
            ->groupBy('product_id', 'unit_id')
            ->get();
        foreach ($rows as $row) {
            $qtyQuotation[$row->product_id][$row->unit_id] = (float) $row->total_qty;
        }
    }

    $qtyBidPackage = [];
    if (!empty($bidPackageIds)) {
        $rows = DB::table('bid_package_products')
            ->whereIn('bid_package_id', $bidPackageIds)
            ->select([
                'product_id',
                'unit_id',
                DB::raw('SUM(qty) as total_qty'),
            ])
            ->groupBy('product_id', 'unit_id')
            ->get();
        foreach ($rows as $row) {
            $qtyBidPackage[$row->product_id][$row->unit_id] = (float) $row->total_qty;
        }
    }

    $qtyContract = [];
    if (!empty($contractIds)) {
        $rows = DB::table('contract_products')
            ->whereIn('contract_id', $contractIds)
            ->select([
                'product_id',
                'unit_id',
                DB::raw('SUM(qty) as total_qty'),
            ])
            ->groupBy('product_id', 'unit_id')
            ->get();
        foreach ($rows as $row) {
            $qtyContract[$row->product_id][$row->unit_id] = (float) $row->total_qty;
        }
    }

    // Bước 6: Quy đổi về ĐVT chính + build items
    $items = [];
    foreach ($allProductIds as $productId) {
        $prod = $products->get($productId);
        if (!$prod) {
            continue;
        }

        $primaryUnitId = $prod->unit_id;
        $primaryCoeff = $conversionMap[$productId][$primaryUnitId] ?? 1;

        // Hàm quy đổi SL về ĐVT chính
        $convertQty = function ($qtyMap) use ($productId, $primaryCoeff, $conversionMap) {
            if (empty($qtyMap[$productId])) {
                return 0;
            }
            $total = 0;
            foreach ($qtyMap[$productId] as $unitId => $qty) {
                $sourceCoeff = $conversionMap[$productId][$unitId] ?? 1;
                if ($primaryCoeff > 0) {
                    $total += $qty * ($sourceCoeff / $primaryCoeff);
                } else {
                    $total += $qty;
                }
            }
            return $total;
        };

        $items[] = [
            'product_code' => $prod->product_code,
            'internal_code' => $prod->internal_code,
            'product_name' => $prod->product_name,
            'array_product_name' => $prod->array_product_name,
            'unit_name' => $prod->unit_name,
            'specification' => $prod->specification,
            'model' => $prod->model,
            'producer_country' => $prod->producer_country,
            'qty_quotation' => $convertQty($qtyQuotation),
            'qty_bid_package' => $convertQty($qtyBidPackage),
            'qty_contract' => $convertQty($qtyContract),
        ];
    }
}
```

- [x] **Step 3: Verify — chạy API kiểm tra**

Dùng Postman hoặc curl:
```
GET /api/v1/category/projects/{project_id}/lifecycle-detail
Authorization: Bearer {token}
```

Expected response:
- `data` chứa metadata dự toán (giữ nguyên)
- `items` chứa danh sách sản phẩm với 11 trường: `product_code`, `internal_code`, `product_name`, `array_product_name`, `unit_name`, `specification`, `model`, `producer_country`, `qty_quotation`, `qty_bid_package`, `qty_contract`
- Sản phẩm từ tất cả 4 phân hệ đều xuất hiện
- SL đã quy đổi về ĐVT chính

---

## Task 7: FE — Thêm 3 cột SL vào popup chi tiết dự toán

**Files:**
- Modify: `hrm-thanhan-client/pages/sale/report-project-contract/index.vue:529-556`

- [x] **Step 1: Thêm 3 header cột vào `<b-thead>` của popup dt-detail**

Tìm block `<b-thead>` trong template `dt-detail` (dòng 529-541). Thêm 3 `<b-th>` mới sau cột "Hãng/Nước SX":

Thay đoạn:
```html
<b-th>Hãng/Nước SX</b-th>
</b-tr>
</b-thead>
```

(trong phần dt-detail) bằng:
```html
<b-th>Hãng/Nước SX</b-th>
<b-th class="text-center">SL trong BG</b-th>
<b-th class="text-center">SL trong Thầu</b-th>
<b-th class="text-center">SL trong HĐ</b-th>
</b-tr>
</b-thead>
```

- [x] **Step 2: Thêm 3 data cells vào `<b-tbody>` của popup dt-detail**

Tìm block `<b-tbody>` trong template `dt-detail` (dòng 542-557). Thêm 3 `<b-td>` mới sau cột `producer_country`:

Thay đoạn:
```html
<b-td>{{ item.producer_country }}</b-td>
</b-tr>
```

(trong v-for loop của dt-detail) bằng:
```html
<b-td>{{ item.producer_country }}</b-td>
<b-td class="text-center">{{ item.qty_quotation }}</b-td>
<b-td class="text-center">{{ item.qty_bid_package }}</b-td>
<b-td class="text-center">{{ item.qty_contract }}</b-td>
</b-tr>
```

- [x] **Step 3: Cập nhật colspan của dòng "Không có sản phẩm"**

Thay đoạn:
```html
<b-td colspan="9" class="text-center text-muted">Không có sản phẩm</b-td>
```

Bằng:
```html
<b-td colspan="12" class="text-center text-muted">Không có sản phẩm</b-td>
```

- [ ] **Step 4: Verify trên browser**

Mở browser → truy cập `/sale/report-project-contract`.
Kiểm tra:
- [ ] Click Mã DT → popup chi tiết DT mở
- [ ] Bảng sản phẩm hiển thị đủ 12 cột (9 cũ + 3 SL mới)
- [ ] Sản phẩm từ tất cả 4 phân hệ đều xuất hiện (không chỉ từ project_products)
- [ ] SL hiển thị đúng: có giá trị hoặc 0
- [ ] ĐVT hiển thị là ĐVT chính
- [ ] Sản phẩm dùng ĐVT khác ở BG/Thầu/HĐ → SL đã quy đổi đúng
- [ ] Các popup khác (GT, HĐ) vẫn hoạt động bình thường
