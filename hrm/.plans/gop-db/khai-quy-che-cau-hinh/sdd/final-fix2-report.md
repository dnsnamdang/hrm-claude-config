# Final-fix #2 — Report: Siết company-scope theo auth (fail-closed) cho Tab Công nợ

Ngày thực hiện: 2026-09-12
Bối cảnh: vá lỗ IDOR cross-company phát hiện ở review tổng thể. Phương án đã chốt: **fail-closed** —
server suy `company_id` từ nhân viên đăng nhập (`auth()->user()->current_company_role`), KHÔNG tin
`company_id` client gửi; sửa/huỷ version phải thuộc đúng công ty của user (khác công ty → 403).

## 1. File thay đổi

### 1.1 `hrm-api/Modules/MasterData/Http/Controllers/V1/RegulationConfigController.php`
- Thêm `use Modules\MasterData\Entities\RegulationScheduledVersion;`.
- Thêm helper `private function currentCompanyId(): int` — đọc `optional(auth()->user())->current_company_role`, KHÔNG đọc `$request->query('company_id')` / `$data['company_id']` nữa.
- `showCongno`: `$companyId` nay lấy từ `currentCompanyId()` thay vì `$request->query('company_id')`.
- `store`: `$companyId` từ `currentCompanyId()`, bỏ dùng `$data['company_id']` khi tạo version và khi lấy config trả về.
- `update`: thêm bước tra `RegulationScheduledVersion::findOrFail($id)` rồi `abort_unless((int) $version->scope_id === $companyId, 403, 'Không thể thao tác phiên bản của công ty khác')` **trước khi** gọi service update; `config` trả về theo `$companyId` của user (không còn dựa vào `$version->scope_id` sau update).
- `cancel`: cùng pattern — tra version, kiểm `scope_id === $companyId` → 403 nếu khác, rồi mới gọi `cancelCongnoVersion`.
- Bỏ hoàn toàn FQCN `\Modules\MasterData\Entities\RegulationScheduledVersion::findOrFail` (dùng tên ngắn nhờ import).
- `guard()` giữ nguyên, luôn chạy đầu mỗi method trước khi suy công ty (đúng như brief xác nhận).

### 1.2 `hrm-api/Modules/MasterData/Http/Requests/ScheduleRegulationVersionRequest.php`
- Đổi rule `'company_id' => 'required|integer'` → `'company_id' => 'nullable|integer', // server suy từ auth (current_company_role); giữ nhận để tương thích FE cũ, KHÔNG dùng`.
- Các rule khác giữ nguyên.

### 1.3 `hrm-api/Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php`
- **Helper `actingAsSeededUserWithPermission()`** đổi chữ ký thành `actingAsSeededUserWithPermission(int $companyId)`:
  - Trước khi insert `employees`, insert 1 dòng `employee_infos` với `company_role = $companyId` (+ các cột NOT NULL dummy: `code`, `fullname`, `telephone`, `department_id=0`, `birthday`, `id_card`, `grant_date`, `grant_location`, `gender=1`, `marital_status=1`, `enter_date`, `email` unique).
  - `employees.employee_info_id` đổi từ hard-code `999999999` → `$infoId` vừa insert.
  - Giữ nguyên phần gán quyền qua pivot `employee_has_permissions` + phát JWT qua `withToken`.
  - Không cần bổ sung cột nào khác ngoài các cột brief liệt kê — `DESCRIBE employee_infos` xác nhận không có FK ràng buộc và các NOT NULL còn lại đều có default hoặc nullable.
- **`test_api_creates_pending_version_and_returns_config`**: gọi `actingAsSeededUserWithPermission($companyId)` thay vì không tham số. Payload vẫn gửi `company_id` (server bỏ qua) — test vẫn xanh vì server ghi đúng công ty của user.
- **Test giữ nguyên không đổi** (đúng như lưu ý brief, không chạm phần công ty): `test_api_routes_registered_and_permission_guard_fails_closed_without_auth`, `test_api_rejects_guest_with_401_on_all_endpoints`.
- **3 test mới thêm** (đặt trước 2 test "XANH THẬT #2/#3" cũ):
  1. `test_update_version_of_other_company_returns_403` — tạo version cho `$otherCompany`, `actingAsSeededUserWithPermission($myCompany)`, `putJson` sửa version đó → `assertStatus(403)`.
  2. `test_cancel_version_of_other_company_returns_403` — tương tự với `deleteJson` → `assertStatus(403)`.
  3. `test_update_and_cancel_version_of_own_company_returns_200` — happy-path: tạo version cho `$myCompany`, `actingAsSeededUserWithPermission($myCompany)`, `putJson` → 200, sau đó `deleteJson` → 200 (chứng minh guard công ty không chặn nhầm chính chủ).

Không sửa file nào khác ngoài 3 file trên. Không commit git.

## 2. Kiểm tra line ending
Cả 3 file gốc đều LF (`file <path>` → "PHP script text, Unicode text, UTF-8 text", không có CRLF terminators; `grep -c $'\r'` = 0 trước và sau khi sửa). Không cần xử lý gì thêm — sửa bằng Edit tool giữ nguyên LF.

## 3. Kết quả `vendor/bin/phpunit Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php --testdox`

```
PHPUnit 9.5.26 by Sebastian Bergmann and contributors.

Regulation Congno Versioning (Modules\MasterData\Tests\Feature\RegulationCongnoVersioning)
 ✔ It casts payload and diff to array
 ✔ It reads current congno values from companies
 ✔ It creates pending version with diff and rechains
 ✔ It applies now when date is today and writes history
 ✔ Cron applies due pending in date order
 ✔ It applies now when update moves effective date to today
 ✔ It applies multiple due versions in date order on apply now
 ✔ Command applies due versions
 ✔ Api creates pending version and returns config
 ✔ Update version of other company returns 403
 ✔ Cancel version of other company returns 403
 ✔ Update and cancel version of own company returns 200
 ✔ Api routes registered and permission guard fails closed without auth
 ✔ Api rejects guest with 401 on all endpoints

Time: 00:09.183, Memory: 90.50 MB

OK (14 tests, 57 assertions)
```

**14/14 test PASS, 57 assertions** (11 test cũ giữ nguyên xanh + 3 test cross-company/happy-path mới).

## 4. Concern
- Không có concern kỹ thuật đáng kể. `guard()` (permission check) chạy trước `currentCompanyId()` ở mọi method — đúng thứ tự brief yêu cầu (user thiếu quyền vẫn 403 ở guard, không lộ thông tin có/không có version công ty khác).
- `showCongno` (GET) hiện bỏ hẳn tham số `company_id` từ query string — response luôn theo công ty của chính user đăng nhập. FE cũ vẫn gửi `?company_id=...` sẽ không lỗi (server chỉ bỏ qua), nhưng cần đảm bảo FE thực sự muốn hiển thị cấu hình của "công ty NV đang thao tác" chứ không phải công ty được chọn ở dropdown khác (nếu có màn nào cho phép xem chéo — hiện tại code base không thấy use-case đó, nhưng nên FE lưu ý khi test tay).
- `ScheduleRegulationVersionRequest.company_id` đổi `required` → `nullable` — nếu có validate khác dựa vào field này (không thấy trong 2 file được sửa) cần rà soát thêm, nhưng nằm ngoài phạm vi 3 file được giao.
