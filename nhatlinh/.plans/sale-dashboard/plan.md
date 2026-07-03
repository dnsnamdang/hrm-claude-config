# Dashboard Kinh doanh — Implementation Plan

> **Cho agentic worker:** Dùng skill `superpowers:subagent-driven-development` để thực thi từng task. Track bằng checkbox `- [ ]`.
> Design: `.plans/sale-dashboard/design.md` · Spec đầy đủ: `docs/superpowers/specs/2026-06-28-sale-dashboard-design.md`
> Phụ trách: @manhcuong

**Goal:** Trang tổng quan phân hệ Kinh doanh hiển thị việc chờ duyệt, doanh số theo thời gian, tỉ lệ chuyển đổi báo giá→HĐ, top khách hàng — dữ liệu co giãn theo cấp quyền user.

**Architecture:** 1 endpoint `GET /v1/sale/dashboard` trả toàn bộ khối, tính bằng SQL aggregate. Scope theo cấp viết RIÊNG trong `SaleDashboardService` (nhân bản pattern `getListForUser`, KHÔNG sửa hàm chung). FE 1 trang `pages/sale/dashboard/index.vue` dùng VueApexCharts.

**Tech Stack:** PHP 7.4 / Laravel 8, MySQL · Nuxt 2 (Vue 2) / Bootstrap-Vue / vue-apexcharts.

## Global Constraints (copy từ spec — áp cho mọi task)

- Status const (cả 2 entity): `1 Nháp / 2 Chờ duyệt / 3 Đã duyệt / 4 Từ chối`. Doanh số/chuyển đổi/top KH chỉ tính `status = 3`.
- KPI "chờ duyệt" = `status = 2`, KHÔNG lọc theo khoảng ngày. Các khối còn lại lọc theo `approved_at BETWEEN from_date AND to_date`.
- Mặc định khoảng ngày: `from_date` = 01/01 năm hiện tại, `to_date` = hôm nay.
- Scope theo cấp viết RIÊNG cho Dashboard, KHÔNG đụng `SaleQuotationService::getListForUser` / `SaleContractService::getListForUser`.
- Permission MỚI: `1123 — Xem dashboard kinh doanh`, group `'Báo giá bán'`, type 4, guard `api`.
- Tiền hiển thị FE: filter `formatNumber` (`plugins/filter.js`).
- Container chính FE: `padding-bottom: 60px` (V2Footer).

---

## PHASE 1 — Backend

### Task 1: Permission 1123

**Files:**
- Modify: `nhatlinh-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (sau block id 1122 'Duyệt hợp đồng')

- [ ] **Bước 1:** Thêm block permission theo đúng mẫu seeder:

```php
Permission::create([
    'id' => 1123,
    'guard_name' => 'api',
    'name' => 'Xem dashboard kinh doanh',
    'display_name' => 'Xem dashboard kinh doanh',
    'group' => 'Báo giá bán',
    'type' => 4
]);
```

- [ ] **Bước 2 (setup dev):** Cấp quyền 1123 cho role test bằng chèn pivot trực tiếp + reset cache (KHÔNG chạy lại seeder vì seeder TRUNCATE bảng permissions). Tinker:

```php
DB::table('role_has_permissions')->insertOrIgnore(['permission_id'=>1123,'role_id'=>1]);
app()['cache']->forget('spatie.permission.cache');
```

- [ ] **Bước 3 Verify:** `php artisan permission:show` hoặc tinker `Permission::find(1123)` ra đúng tên. Lưu ý team khi deploy: seed 1123 + gán role.

---

### Task 2: SaleDashboardService — scope + aggregate

**Files:**
- Create: `nhatlinh-api/Modules/Sale/Services/SaleDashboardService.php`

**Interfaces:**
- Produces:
  - `getData(array $filters): array` — `$filters` keys: `from_date`,`to_date`,`company_id`,`department_id`,`part_id` (đã validate, có default). Return mảng đúng response spec mục 3.2.
  - private `applyScope(\Illuminate\Database\Eloquent\Builder $q, string $entity): Builder` — `$entity` ∈ `['quotation','contract']`.
  - private `applyExtraFilter(Builder $q, array $filters): Builder` — áp `company_id/department_id/part_id` từ query (giao nhau).

- [ ] **Bước 1:** Viết `applyScope()` — nhân bản pattern từ `getListForUser`, dùng permission string theo entity:

```php
use Modules\Sale\Entities\SaleQuotation;
use Modules\Sale\Entities\SaleContract;

private function applyScope($query, string $entity)
{
    // map permission theo entity
    $perm = $entity === 'quotation'
        ? ['all' => 'Xem tất cả báo giá bán', 'company' => 'Xem báo giá bán theo công ty',
           'dept' => 'Xem báo giá bán theo phòng ban', 'part' => 'Xem báo giá bán theo bộ phận']
        : ['all' => 'Xem tất cả hợp đồng', 'company' => 'Xem hợp đồng theo công ty',
           'dept' => 'Xem hợp đồng theo phòng ban', 'part' => 'Xem hợp đồng theo bộ phận'];

    $user = auth()->user();

    if (isCurrentEmployeeHasPermission($perm['all'])) {
        return $query; // không giới hạn cấp
    }
    if (isCurrentEmployeeHasPermission($perm['company'])) {
        return $query->where('company_id', $user->current_company_role);
    }
    if (isCurrentEmployeeHasPermission($perm['dept'])) {
        $deptIds = listManageDepartmentIds();
        $partIds = listManagePartIds();
        return $query->where(function ($q) use ($deptIds, $partIds, $user) {
            $q->whereIn('department_id', $deptIds)
              ->orWhereIn('part_id', $partIds)
              ->orWhere('created_by', $user->id);
        });
    }
    if (isCurrentEmployeeHasPermission($perm['part'])) {
        $partIds = listManagePartIds();
        return $query->where(function ($q) use ($partIds, $user) {
            $q->whereIn('part_id', $partIds)->orWhere('created_by', $user->id);
        });
    }
    return $query->where('created_by', $user->id);
}
```

> Đối chiếu chính xác từng nhánh với `SaleQuotationService::getListForUser()` (dòng 13-69) và `SaleContractService::getListForUser()` (dòng 18-74) khi code, giữ y hệt điều kiện.

- [ ] **Bước 2:** Viết `applyExtraFilter()` (giao nhau với scope, không nới rộng):

```php
private function applyExtraFilter($query, array $f)
{
    if (!empty($f['company_id']))    $query->where('company_id', $f['company_id']);
    if (!empty($f['department_id'])) $query->where('department_id', $f['department_id']);
    if (!empty($f['part_id']))       $query->where('part_id', $f['part_id']);
    return $query;
}
```

- [ ] **Bước 3:** Viết helper dựng base query đã scope + filter cho từng entity:

```php
private function baseQuery(string $entity, array $f)
{
    $model = $entity === 'quotation' ? SaleQuotation::query() : SaleContract::query();
    $q = $this->applyScope($model, $entity);
    return $this->applyExtraFilter($q, $f);
}
```

- [ ] **Bước 4:** Viết các phần tổng hợp trong `getData()`:

```php
public function getData(array $f): array
{
    // 1) KPI chờ duyệt (status=2, KHÔNG lọc ngày)
    $pendingQ = (clone $this->baseQuery('quotation', $f))->where('status', 2);
    $pendingC = (clone $this->baseQuery('contract', $f))->where('status', 2);

    // 2) revenue_by_month (status=3, theo approved_at trong khoảng), fill đủ tháng
    $qByMonth = $this->sumByMonth('quotation', $f); // ['2026-01'=>amount,...]
    $cByMonth = $this->sumByMonth('contract', $f);
    $months   = $this->monthRange($f['from_date'], $f['to_date']);
    $revenueByMonth = array_map(fn ($m) => [
        'month' => $m,
        'quotation_amount' => $qByMonth[$m] ?? 0,
        'contract_amount'  => $cByMonth[$m] ?? 0,
    ], $months);

    // 3) conversion: báo giá đã duyệt (mẫu số) vs HĐ có quotation_id thuộc tập đó (tử số)
    $apprQ = (clone $this->baseQuery('quotation', $f))
        ->where('status', 3)->whereBetween('approved_at', [$f['from_date'].' 00:00:00', $f['to_date'].' 23:59:59']);
    $quotationIds = (clone $apprQ)->pluck('id');
    $quotationCount  = $quotationIds->count();
    $quotationAmount = (clone $apprQ)->sum('total_amount');

    $apprC = (clone $this->baseQuery('contract', $f))
        ->where('status', 3)
        ->whereBetween('approved_at', [$f['from_date'].' 00:00:00', $f['to_date'].' 23:59:59']);
    $contractCount  = (clone $apprC)->whereIn('quotation_id', $quotationIds)->count();
    $contractAmount = (clone $apprC)->whereIn('quotation_id', $quotationIds)->sum('total_amount');
    $approvedContractAmount = (clone $apprC)->sum('total_amount'); // tổng HĐ đã duyệt (KPI doanh số)

    // 4) top_customers theo tổng giá trị HĐ đã duyệt
    $topCustomers = (clone $apprC)
        ->select('customer_id',
            DB::raw('SUM(total_amount) as contract_amount'),
            DB::raw('COUNT(*) as contract_count'))
        ->groupBy('customer_id')
        ->orderByDesc('contract_amount')
        ->limit(10)->get()
        ->map(function ($r) {
            $r->customer_name = optional(\Modules\Category\Entities\Customer::find($r->customer_id))->name; // canh đúng entity KH category_customers
            return [
                'customer_id' => $r->customer_id,
                'customer_name' => $r->customer_name,
                'contract_amount' => (float) $r->contract_amount,
                'contract_count' => (int) $r->contract_count,
            ];
        });

    $conversionRate = $quotationCount > 0 ? round($contractCount / $quotationCount * 100, 1) : 0;

    return [
        'kpis' => [
            'pending_quotations' => ['count' => (clone $pendingQ)->count(), 'amount' => (float) (clone $pendingQ)->sum('total_amount')],
            'pending_contracts'  => ['count' => (clone $pendingC)->count(), 'amount' => (float) (clone $pendingC)->sum('total_amount')],
            'approved_contract_amount' => (float) $approvedContractAmount,
            'conversion_rate' => $conversionRate,
        ],
        'revenue_by_month' => $revenueByMonth,
        'conversion' => [
            'quotation_count' => $quotationCount,
            'contract_count' => $contractCount,
            'quotation_amount' => (float) $quotationAmount,
            'contract_amount' => (float) $contractAmount,
        ],
        'top_customers' => $topCustomers,
    ];
}
```

- [ ] **Bước 5:** Viết `sumByMonth()` + `monthRange()`:

```php
private function sumByMonth(string $entity, array $f): array
{
    return (clone $this->baseQuery($entity, $f))
        ->where('status', 3)
        ->whereBetween('approved_at', [$f['from_date'].' 00:00:00', $f['to_date'].' 23:59:59'])
        ->select(DB::raw("DATE_FORMAT(approved_at,'%Y-%m') as m"), DB::raw('SUM(total_amount) as amt'))
        ->groupBy('m')->pluck('amt', 'm')->toArray();
}

private function monthRange(string $from, string $to): array
{
    $start = \Carbon\Carbon::parse($from)->startOfMonth();
    $end   = \Carbon\Carbon::parse($to)->startOfMonth();
    $out = [];
    while ($start <= $end) { $out[] = $start->format('Y-m'); $start->addMonth(); }
    return $out;
}
```

> Xác nhận tên Entity Khách hàng đúng (danh mục `category_customers`) khi code — sửa `\Modules\Category\Entities\Customer` cho khớp. Cân nhắc join 1 lần thay vì `find()` trong map nếu cần (top 10 nên không nặng).

- [ ] **Bước 6 Verify:** `php -l SaleDashboardService.php` sạch.

---

### Task 3: DashboardRequest (validate ngày)

**Files:**
- Create: `nhatlinh-api/Modules/Sale/Http/Requests/DashboardRequest.php`

- [ ] **Bước 1:** Rules tối thiểu + default ngày trong controller (không bắt buộc):

```php
public function rules() {
    return [
        'from_date' => 'nullable|date_format:Y-m-d',
        'to_date'   => 'nullable|date_format:Y-m-d',
        'company_id' => 'nullable|integer',
        'department_id' => 'nullable|integer',
        'part_id' => 'nullable|integer',
    ];
}
public function authorize() { return true; }
```

- [ ] **Bước 2 Verify:** `php -l` sạch. (BE phải rethrow ValidationException — BaseRequest đã xử lý, không catch chung Exception.)

---

### Task 4: DashboardController@index + middleware route

**Files:**
- Modify: `nhatlinh-api/Modules/Sale/Http/Controllers/Api/V1/DashboardController.php`
- Modify: `nhatlinh-api/Modules/Sale/Routes/api.php` (dòng 9)

**Interfaces:**
- Consumes: `SaleDashboardService::getData(array)` (Task 2).

- [ ] **Bước 1:** Viết index():

```php
public function index(DashboardRequest $request, SaleDashboardService $service)
{
    $filters = [
        'from_date' => $request->input('from_date', date('Y-01-01')),
        'to_date'   => $request->input('to_date', date('Y-m-d')),
        'company_id' => $request->input('company_id'),
        'department_id' => $request->input('department_id'),
        'part_id' => $request->input('part_id'),
    ];
    return response()->json(['code' => 200, 'data' => $service->getData($filters)]);
}
```

- [ ] **Bước 2:** Gắn middleware route:

```php
Route::get('/dashboard', [DashboardController::class, 'index'])
    ->middleware('checkPermission:Xem dashboard kinh doanh');
```

- [ ] **Bước 3 Verify (tinker / E2E):** đăng nhập user có quyền, gọi `GET /v1/sale/dashboard?from_date=2026-01-01&to_date=2026-06-28`. Kiểm:
  - response đủ 4 nhánh `kpis/revenue_by_month/conversion/top_customers`.
  - `revenue_by_month` đủ tháng liền mạch (tháng trống = 0).
  - user cấp thấp (chỉ created_by) → số liệu thu hẹp đúng.
  - user KHÔNG có quyền 1123 → 403.
  - `php -l` 2 file sạch.

---

## PHASE 2 — Frontend

### Task 5: Store sale-dashboard

**Files:**
- Create: `nhatlinh-client/store/sale-dashboard.js`

- [ ] **Bước 1:** Theo mẫu `store/sale-quotation.js`:

```javascript
export const actions = {
    async get({ dispatch }, query) {
        return await dispatch('apiGetMethod', `sale/dashboard${query || ''}`, { root: true })
    },
}
```

- [ ] **Bước 2 Verify:** import được, không lỗi build.

---

### Task 6: Trang dashboard — thanh lọc + 4 KPI card

**Files:**
- Modify: `nhatlinh-client/pages/sale/dashboard/index.vue` (thay placeholder)

- [ ] **Bước 1:** Thanh lọc đầu trang (tái dùng đúng như `pages/sale/quotation-approval/index.vue`):

```html
<V2BaseCompanyDepartmentFilter :form="filters" :permissions="permissions" :disable_employee="true" wrapper-class="d-contents" />
<V2BaseDatePicker v-model="filters.from_date" placeholder="Từ ngày" />
<V2BaseDatePicker v-model="filters.to_date" placeholder="Đến ngày" />
```

- [ ] **Bước 2:** `data()` default: `filters.from_date` = `dayjs().startOf('year')`, `filters.to_date` = `dayjs()` (format `YYYY-MM-DD`). `loadData()` build query (dùng `buildQueryString`) gọi `this.$store.dispatch('sale-dashboard/get', query)`; gọi khi mounted + watch `filters` (debounce nhẹ).

- [ ] **Bước 3:** 4 KPI card (Bootstrap row/cols), mỗi card hiện số + tiền `| formatNumber`:
  - "Báo giá chờ duyệt" → `kpis.pending_quotations` → `<nuxt-link to="/sale/quotation-approval">`.
  - "Hợp đồng chờ duyệt" → `kpis.pending_contracts` → `/sale/contract-approval`.
  - "Doanh số HĐ đã duyệt" → `kpis.approved_contract_amount`.
  - "Tỉ lệ chốt" → `kpis.conversion_rate + '%'`.

- [ ] **Bước 4:** Container chính `padding-bottom: 60px`. Loading spinner khi đang fetch.

- [ ] **Bước 5 Verify:** đổi khoảng ngày / công ty → KPI reload đúng; link sang 2 màn approval chạy.

---

### Task 7: Chart Doanh số theo thời gian

**Files:**
- Modify: `nhatlinh-client/pages/sale/dashboard/index.vue`

- [ ] **Bước 1:** Register `apexchart: () => import('vue-apexcharts')`.

- [ ] **Bước 2:** Computed dựng series/options từ `revenue_by_month`:

```javascript
revenueSeries() {
  return [
    { name: 'Báo giá đã duyệt', data: this.data.revenue_by_month.map(x => x.quotation_amount) },
    { name: 'Hợp đồng đã duyệt', data: this.data.revenue_by_month.map(x => x.contract_amount) },
  ]
},
revenueOptions() {
  return {
    chart: { type: 'bar', toolbar: { show: false } },
    xaxis: { categories: this.data.revenue_by_month.map(x => x.month) },
    yaxis: { labels: { formatter: v => this.shortMoney(v) } },
    tooltip: { y: { formatter: v => this.$options.filters.formatNumber(v) } },
    plotOptions: { bar: { columnWidth: '55%' } },
  }
},
```
`shortMoney(v)`: chia tr/tỷ (vd `>=1e9 → (v/1e9)+' tỷ'`, `>=1e6 → (v/1e6)+' tr'`).

- [ ] **Bước 3:** `<apexchart type="bar" height="350" :options="revenueOptions" :series="revenueSeries" />`. Full width.

- [ ] **Bước 4:** Empty-state khi `revenue_by_month` toàn 0 → hiện "Chưa có dữ liệu".

- [ ] **Bước 5 Verify:** cột đúng theo tháng, tooltip ra số đầy đủ.

---

### Task 8: Chart Tỉ lệ chuyển đổi + Top 10 KH (2 cột)

**Files:**
- Modify: `nhatlinh-client/pages/sale/dashboard/index.vue`

- [ ] **Bước 1 (Chuyển đổi):** 2 cột row. Khối 4a hiển thị bar ngang 2 bậc từ `conversion`:

```javascript
conversionSeries() {
  return [{ data: [this.data.conversion.quotation_count, this.data.conversion.contract_count] }]
},
conversionOptions() {
  return {
    chart: { type: 'bar', toolbar: { show: false } },
    plotOptions: { bar: { horizontal: true, distributed: true } },
    xaxis: { categories: ['Báo giá đã duyệt', 'HĐ chốt'] },
  }
},
```
Kèm 2 dòng text % dưới chart: theo số lượng `contract_count/quotation_count*100` và theo giá trị `contract_amount/quotation_amount*100` (guard chia 0).

- [ ] **Bước 2 (Top KH):** Khối 4b bar ngang:

```javascript
topSeries() { return [{ name: 'Giá trị HĐ', data: this.data.top_customers.map(c => c.contract_amount) }] },
topOptions() {
  return {
    chart: { type: 'bar', toolbar: { show: false } },
    plotOptions: { bar: { horizontal: true } },
    xaxis: { categories: this.data.top_customers.map(c => c.customer_name), labels: { formatter: v => this.shortMoney(v) } },
    tooltip: { y: { formatter: v => this.$options.filters.formatNumber(v) } },
  }
},
```

- [ ] **Bước 3:** Empty-state mỗi khối khi mảng rỗng.

- [ ] **Bước 4 Verify:** 2 chart render, % chuyển đổi đúng, top KH xếp giảm dần.

---

### Task 9: Menu + route guard

**Files:**
- Modify: file cấu hình menu sidebar Kinh doanh (canh theo nơi đăng ký menu Sale hiện có) + route guard `checkPermission`

- [ ] **Bước 1:** Thêm mục menu "Dashboard"/"Tổng quan" nhóm Kinh doanh, ẩn/hiện theo quyền `Xem dashboard kinh doanh` (theo đúng pattern các màn Sale khác — đăng ký permission name vào guard route + `isShow`).

- [ ] **Bước 2 Verify (2 chiều):** user có quyền → thấy menu + vào được; user thiếu quyền → ẩn menu + chặn truy cập trực tiếp URL.

---

## PHASE 3 — Hiện nhóm quyền Kinh doanh trên màn Role (fix)

Vấn đề: màn `/timesheet/setting/roles/add/:id` không hiện nhóm `Báo giá bán`/`Hợp đồng`/`Xem dashboard kinh doanh` vì chúng bị gán chung `type=4` (phân hệ Giao việc đang cố ý ẩn — accordion type=4 comment out trong `Permission.vue`). Quyết định: **tách `type` riêng cho Kinh doanh = 9 "Phân hệ kinh doanh"** (đã xác nhận không có chỗ nào BE/FE lọc Sale theo type=4; `PermissionService::getLists()` chỉ `->get()`).

- [x] **T10:** Seeder `PermissionsTableSeeder.php`: đổi `type` 4→9 cho mọi permission group `Báo giá bán` (1105-1112, 1123) + `Hợp đồng` (1115-1122). php -l sạch.
- [x] **T11:** DB dev: `UPDATE permissions SET type=9 WHERE \`group\` IN ('Báo giá bán','Hợp đồng')` (17 dòng).
- [x] **T12:** FE `components/setting/Permission.vue`: thêm accordion "Phân hệ kinh doanh" `filterPermission(9)` (đặt sau phân hệ HCNS type=3).
- [ ] **T13 (user test):** reload màn role → thấy accordion "Phân hệ kinh doanh" với 2 nhóm Báo giá bán (gồm "Xem dashboard kinh doanh") + Hợp đồng; tick gán quyền + lưu role OK.

## PHASE 4 — Redesign FE dashboard (hiện đại + gradient)

- [x] **T16:** Restyle **sidebar menu** (theme Light tinh tế, dùng chung toàn app) trong `assets/scss/custom/structure/_left-menu.scss` — CHỈ CSS, không đụng template/logic/permission. Mục active = **pill gradient xanh** (`#16a34a→#22c55e`) + glow; hover bo tròn nền xám mềm; item bo góc 10px + inset margin; section title dịu (slate, uppercase); viền/đổ bóng sidebar nhẹ. Reset margin/radius ở chế độ condensed (mini) để không vỡ icon. Theme dark/brand có override specificity cao hơn → không ảnh hưởng. Format nhãn chart doanh số sang Tháng/Năm (MM/YYYY).
- [x] **T15:** Tiêu đề "Tổng quan Kinh doanh" đưa lên **topbar** chuẩn dự án (import `PageTitleMixin` + computed `pageTitle()`); bỏ header trong thân trang. Tạm **ẩn bộ lọc** (`showFilter: false`, dễ bật lại) + khoảng ngày mở rộng `from_date='2020-01-01'`→nay để **hiển thị toàn bộ dữ liệu**; computed `revenueMonths` lọc chart "Doanh số theo thời gian" **chỉ các tháng trong năm hiện tại** (KPI/chuyển đổi/top KH vẫn all data).
- [x] **T14:** Thiết kế lại `pages/sale/dashboard/index.vue` — phong cách enterprise hiện đại: header có title gradient + subtitle; 4 KPI card full-gradient (amber/blue/emerald/violet, KHÔNG dùng đỏ) với blob trang trí + icon kính mờ + hover lift + entrance staggered; panel bo 16px shadow mềm, panel-head có dải accent gradient; chart bar bo góc (borderRadius 6) + fill gradient + grid dashed nhạt; conversion % đổi sang pill gradient (bỏ text màu). Giữ nguyên 100% logic/dữ liệu/computed. Không build được (node cũ) → user reload test.

## Checkpoint cuối Phase
- [x] BE: `php -l` toàn bộ file mới sạch (5 file). Service smoke-test tinker cấu trúc OK. **E2E HTTP với auth chưa chạy** (DB dev thiếu users) → user test sau.
- [x] FE: review tĩnh PASS (Spec ✅ + Quality Approved, đã fix I-1). Build node dev cũ KHÔNG chạy được → user test UI trình duyệt.
- [x] Final whole-branch review (opus): SẴN SÀNG BÀN GIAO, 0 Critical/Important; contract BE↔FE khớp, permission string trùng khớp 3 nơi, scope không nới rộng.
- [ ] Lưu ý team deploy: seed permission 1123 + gán role; không sửa `getListForUser`.

### Checkpoint — 2026-06-28
Vừa hoàn thành: Phase 1 BE (permission 1123 + SaleDashboardService + DashboardRequest + DashboardController + route; review Spec ✅/Quality Approved, đã fix 1 Important + 2 Minor). Phase 2 FE (store + page 4 KPI + 3 chart + menu guard; review Spec ✅/Quality Approved, đang fix I-1 emptyDashboard→factory).
Đang làm dở: chờ FE fix I-1 xong → final review tổng (integration BE↔FE).
Bước tiếp theo: final whole-branch review (opus) rồi bàn giao cho user test trình duyệt + (nếu cần) E2E HTTP có auth.
Blocked: E2E HTTP cần seed users ở DB dev; FE không build được do node cũ → phụ thuộc user test.

Entity Khách hàng thực tế: `Modules\Category\Entities\CustomerCategory` (không phải Customer). Menu Sale: sửa `isShow` mục "Tổng quan" trong `components/default-menu/sale.js` → `['Xem dashboard kinh doanh']`.
