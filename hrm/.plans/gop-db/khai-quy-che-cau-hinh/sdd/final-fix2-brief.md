# Final-fix #2 brief — Siết company-scope theo auth (fail-closed) cho Tab Công nợ

Bối cảnh: review tổng thể phát hiện lỗ IDOR cross-company; user đã CHỐT phương án **"Siết theo auth (fail-closed)"**: server suy `company_id` từ nhân viên đăng nhập (KHÔNG tin `company_id` client gửi), và sửa/huỷ version phải thuộc đúng công ty của user (nếu không → 403). Giống module Training.

Sửa **3 file** (KHÔNG đụng file khác, KHÔNG commit git, giữ nguyên line ending):
1. `hrm-api/Modules/MasterData/Http/Controllers/V1/RegulationConfigController.php`
2. `hrm-api/Modules/MasterData/Http/Requests/ScheduleRegulationVersionRequest.php`
3. `hrm-api/Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php` (cập nhật helper + thêm test)

Nền tảng đã xác minh:
- `auth()->user()->current_company_role` = công ty NV đang thao tác. Accessor `TpEmployee::getCurrentCompanyRoleAttribute()` đọc `employee_infos.company_role` (fallback `company_id`) theo `employee_info_id` của user. Đây đúng bằng `company_role` FE gửi.
- `guard()` (kiểm quyền) LUÔN chạy trước khi suy công ty → user thiếu quyền vẫn bị 403 ở guard như cũ, không chạm phần công ty.

---

## File 1 — RegulationConfigController.php

Thêm import ở đầu (cạnh các `use` sẵn có):
```php
use Modules\MasterData\Entities\RegulationScheduledVersion;
```

Thêm helper private (đặt ngay sau `guard()`):
```php
    private function currentCompanyId(): int
    {
        // Suy công ty từ nhân viên đăng nhập (fail-closed) — KHÔNG tin company_id client gửi lên,
        // tránh đọc/sửa/huỷ cấu hình + version của công ty khác. current_company_role = công ty NV
        // đang thao tác (employee_infos.company_role, fallback company_id).
        return (int) optional(auth()->user())->current_company_role;
    }
```

Thay 4 method bằng (giữ nguyên `guard()` đầu mỗi hàm):
```php
    public function showCongno(Request $request)
    {
        $this->guard();
        $companyId = $this->currentCompanyId();
        $config = $this->service->getCongnoConfig($companyId);
        return $this->responseSuccessJson('OK', 200, $config);
    }

    public function store(ScheduleRegulationVersionRequest $request)
    {
        $this->guard();
        $companyId = $this->currentCompanyId();
        $data = $request->validated();
        $version = $this->service->createCongnoVersion(
            $companyId, $data['effective_date'], $data['values'],
            $data['note'] ?? null, auth()->id()
        );
        return $this->responseSuccessJson('Đã lưu phiên bản', 200, [
            'version' => $version,
            'config' => $this->service->getCongnoConfig($companyId),
        ]);
    }

    public function update(ScheduleRegulationVersionRequest $request, $id)
    {
        $this->guard();
        $companyId = $this->currentCompanyId();
        $version = RegulationScheduledVersion::findOrFail($id);
        abort_unless((int) $version->scope_id === $companyId, 403, 'Không thể thao tác phiên bản của công ty khác');

        $data = $request->validated();
        $version = $this->service->updateCongnoVersion(
            (int) $id, $data['effective_date'], $data['values'], $data['note'] ?? null
        );
        return $this->responseSuccessJson('Đã cập nhật phiên bản', 200, [
            'version' => $version,
            'config' => $this->service->getCongnoConfig($companyId),
        ]);
    }

    public function cancel($id)
    {
        $this->guard();
        $companyId = $this->currentCompanyId();
        $version = RegulationScheduledVersion::findOrFail($id);
        abort_unless((int) $version->scope_id === $companyId, 403, 'Không thể thao tác phiên bản của công ty khác');

        $this->service->cancelCongnoVersion((int) $id);
        return $this->responseSuccessJson('Đã huỷ phiên bản', 200, [
            'config' => $this->service->getCongnoConfig($companyId),
        ]);
    }
```
(Bỏ dòng `$companyId = (int) $request->query('company_id');` và mọi chỗ đọc `$data['company_id']`. Xoá FQCN `\Modules\MasterData\Entities\RegulationScheduledVersion::findOrFail` cũ trong cancel — nay dùng tên ngắn nhờ import.)

## File 2 — ScheduleRegulationVersionRequest.php

Đổi rule `company_id`:
```php
            'company_id' => 'nullable|integer', // server suy từ auth (current_company_role); giữ nhận để tương thích FE cũ, KHÔNG dùng
```
(Các rule khác giữ nguyên.)

## File 3 — Test: cập nhật helper + thêm test

### 3a. Sửa `actingAsSeededUserWithPermission()` → nhận `$companyId` và dựng EmployeeInfo thật
Vì controller nay suy công ty từ `auth()->user()->current_company_role` (đọc `employee_infos` theo `employee_info_id`), user test PHẢI có 1 dòng `employee_infos` với `company_role = $companyId`. Đổi chữ ký:
```php
    private function actingAsSeededUserWithPermission(int $companyId)
```
Trong helper, TRƯỚC khi insert `employees`, tạo employee_infos và dùng id của nó làm `employee_info_id`:
```php
        $infoId = \Illuminate\Support\Facades\DB::table('employee_infos')->insertGetId([
            'company_role' => $companyId, // → current_company_role = công ty này
            'code' => 'RC' . uniqid(),
            'fullname' => 'Regulation Tester',
            'telephone' => '0900000000',
            'department_id' => 0,
            'birthday' => '2000-01-01',
            'id_card' => '000000000000',
            'grant_date' => '2020-01-01',
            'grant_location' => 'HN',
            'gender' => 1,
            'marital_status' => 1,
            'enter_date' => '2020-01-01',
            'email' => 'rc-info-' . uniqid() . '@example.com',
            'created_at' => now(),
            'updated_at' => now(),
        ]);
```
rồi trong insert `employees` đổi `'employee_info_id' => 999999999` → `'employee_info_id' => $infoId`. Giữ nguyên phần gán quyền qua pivot + JWT.
⚠️ Nếu insert employee_infos báo thiếu cột NOT NULL khác (schema thật erp_hrm_check), bổ sung giá trị dummy hợp lý cho cột đó (đọc `information_schema` nếu cần) — mục tiêu: dòng info tồn tại và `company_role = $companyId`.

### 3b. Cập nhật test đang gọi helper
`test_api_creates_pending_version_and_returns_config`: đổi `$this->actingAsSeededUserWithPermission();` → `$this->actingAsSeededUserWithPermission($companyId);`. Payload vẫn gửi `company_id` (nay server bỏ qua) — test vẫn xanh vì server ghi vào đúng công ty của user (= $companyId). Giữ nguyên các assert.
> Lưu ý: 2 test còn lại (`..._permission_guard_fails_closed_without_auth` dùng user KHÔNG quyền, và `..._rejects_guest_with_401...`) KHÔNG gọi helper này và KHÔNG chạm phần công ty (bị chặn ở guard/middleware trước) → giữ nguyên, phải vẫn PASS.

### 3c. Thêm 2 test cross-company 403
- **update version công ty khác → 403**: `$myCompany = makeCompanyWithCongno([...])`; `$otherCompany = makeCompanyWithCongno([...])`; tạo 1 version cho `$otherCompany` bằng service (`app(RegulationConfigService::class)->createCongnoVersion($otherCompany,'2099-01-01', ...values..., 'x', 1)`); `actingAsSeededUserWithPermission($myCompany)`; gọi `putJson('/api/v1/master-data/regulation-config/congno/versions/'.$version->id, [payload hợp lệ])` → `assertStatus(403)`.
- **cancel version công ty khác → 403**: tương tự, `deleteJson(...'/versions/'.$version->id)` → `assertStatus(403)`.

### 3d. (Nên có) 1 test happy-path same-company để chứng minh guard KHÔNG chặn nhầm
- `actingAsSeededUserWithPermission($myCompany)`; tạo version pending cho CHÍNH `$myCompany` (qua service hoặc qua POST); `putJson` sửa nó với payload hợp lệ → `assertStatus(200)`; và/hoặc `deleteJson` → `assertStatus(200)`. (Nếu POST tạo, nhớ payload company_id gửi gì cũng được vì server bỏ qua.)

---

## Chạy test (BẮT BUỘC — phpunit, KHÔNG `artisan test --filter`)
```
cd hrm-api && vendor/bin/phpunit Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php --testdox
```
Tất cả test (11 hiện có + các test mới) phải PASS. Nếu 1 test cũ đỏ do đổi helper → sửa cho khớp, KHÔNG làm yếu guard/scope.

## Báo cáo
Ghi vào `HRM/.plans/gop-db/khai-quy-che-cau-hinh/sdd/final-fix2-report.md` (thay đổi từng file + output phpunit --testdox full + số test/assertion + concern). Trả về controller: STATUS + 1 dòng tóm tắt test + concern. KHÔNG tự spawn subagent.
