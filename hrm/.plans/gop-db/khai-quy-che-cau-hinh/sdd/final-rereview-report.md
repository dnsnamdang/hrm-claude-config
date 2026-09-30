# Re-review có phạm vi — bản vá cuối Slice 1 (Tab Công nợ versioning)

Phạm vi: chỉ 4 file trong `base-ff-to-after-ff.diff`
(`RegulationConfigService.php`, `RegulationConfigController.php` V1,
`ScheduleRegulationVersionRequest.php`, `Tests/Feature/RegulationCongnoVersioningTest.php`).
Không mở rộng ra ngoài diff, không review lại toàn nhánh.

## Kết luận nhanh

| # | Finding review tổng thể | Trạng thái |
|---|---|---|
| 1 | IDOR cross-company (company_id client-controlled) | **ĐÃ ĐÓNG** |
| 2 | `updateCongnoVersion` thiếu đuôi áp-ngay | **ĐÃ ĐÓNG** |
| 3 | Áp-ngay chỉ áp 1 bản thay vì tất cả bản đến hạn theo thứ tự | **ĐÃ ĐÓNG** |
| 4 | `applyVersion` không transaction/lock → race với cron | **ĐÃ ĐÓNG** |
| 5 | Dead code `baselineForDate` | **ĐÃ ĐÓNG** |

Phát sinh **1 lỗi mới mức LOW/MEDIUM** (chi tiết bên dưới) — không phải regression bảo mật
(không mở lại IDOR), là một gap fail-closed chưa được xử lý ở nhánh phụ hiếm gặp.

---

## Xác nhận từng finding

### #1 — IDOR cross-company: ĐÃ ĐÓNG

`RegulationConfigController.php`:
- Thêm `private function currentCompanyId(): int` (dòng 33-39) suy company từ
  `auth()->user()->current_company_role`, KHÔNG đọc `$request` nữa.
- `showCongno` (dòng 41-47): dùng `currentCompanyId()` thay vì `$request->query('company_id')`.
- `store` (dòng 49-62): dùng `currentCompanyId()` thay vì `(int) $data['company_id']`, cả khi tạo
  version lẫn khi build lại `config` trả về.
- `update` (dòng 64-79) và `cancel` (dòng 81-92): đều gọi `guard()` → `currentCompanyId()` →
  `findOrFail($id)` → `abort_unless((int) $version->scope_id === $companyId, 403, ...)` **TRƯỚC**
  khi gọi service. Đúng thứ tự yêu cầu (check trước khi thao tác).

Đã rà toàn bộ 4 method — không còn đường nào đọc `company_id` từ `$request`/client. Test mới
(`test_update_version_of_other_company_returns_403`, `test_cancel_version_of_other_company_returns_403`)
dựng 2 công ty thật + gọi API thật (không mock), xác nhận đúng 403. Test
`test_update_and_cancel_version_of_own_company_returns_200` xác nhận guard không chặn nhầm
same-company. Cả 3 test đều gọi qua HTTP thật (`putJson`/`deleteJson`) với user đăng nhập thật qua
JWT — không phải test giả/rỗng.

### #2 — `updateCongnoVersion` thiếu đuôi áp-ngay: ĐÃ ĐÓNG

`RegulationConfigService.php:229-235` — sau `recomputeDiffChain`, nếu
`$version->effective_date <= now()->startOfDay()` thì gọi áp-ngay, y hệt cơ chế `create`.
Test `it_applies_now_when_update_moves_effective_date_to_today` xác nhận version chuyển
`applied`, company field cập nhật, và **đúng 1 dòng lịch sử** (không double-apply, không thiếu).

### #3 — Áp-ngay phải áp TẤT CẢ bản đến hạn theo đúng thứ tự: ĐÃ ĐÓNG

Cả `createCongnoVersion` (dòng 142-146) và `updateCongnoVersion` (dòng 230-234) gọi
`applyDueCongnoVersions(null, $companyId)` thay vì gọi `applyVersion($version)` trực tiếp.
`applyDueCongnoVersions` (dòng 193-214) lọc theo `scope_id = $companyId` khi được truyền, và giữ
nguyên thứ tự `orderBy('scope_id')->orderBy('effective_date')->orderBy('id')` — khớp cron.

Test `it_applies_multiple_due_versions_in_date_order_on_apply_now` dựng đúng kịch bản: v1 kéo về
hôm qua (vẫn pending), v2 tạo hiệu lực hôm nay → đuôi áp-ngay của `create` phải quét và áp CẢ v1
lẫn v2 theo thứ tự ngày, kết quả cuối company nhận giá trị của v2 (bản mới nhất theo ngày). Test
assert cả hai đều `applied` và giá trị cuối đúng — chứng minh đúng hành vi #3, không phải test giả.

### #4 — `applyVersion` transaction + lock chống race với cron: ĐÃ ĐÓNG

`RegulationConfigService.php:150-191`:
- Fast-path idempotent giữ nguyên ở đầu hàm (dòng 152-154), kiểm tra trên đối tượng truyền vào
  trước khi mở transaction — tránh mở transaction thừa cho version đã applied.
- Bên trong `DB::transaction`, **re-fetch với `lockForUpdate()`** (dòng 158) rồi kiểm tra lại
  status (dòng 159-161) — đây là điểm mấu chốt chống lost-update khi 2 tiến trình (cron + request
  áp-ngay) cùng nhắm 1 version: tiến trình thua cuộc sẽ thấy `status !== PENDING` sau khi lấy lock
  và `return` êm, không ghi đè lịch sử/công ty lần 2.
- Toàn bộ phần ghi (`Company::save()`, `CompanyRegulationHistory::create()`,
  `$locked->status = APPLIED`) đều dùng biến `$locked` (không dùng `$version` gốc có thể stale) —
  đúng, tránh race đọc-ghi trên object cũ.
- `$version->refresh()` sau transaction (dòng 190) đồng bộ lại instance cho caller, kể cả trường
  hợp caller "thua cuộc" trong race (status vẫn được đồng bộ đúng thành `applied`).

Test `it_applies_now_when_date_is_today_and_writes_history` (không đổi trong diff nhưng vẫn chạy
qua code mới) xác nhận gọi `applyVersion()` lần 2 là no-op (đúng 2 dòng lịch sử, không tăng thêm).

### #5 — Dead code `baselineForDate`: ĐÃ ĐÓNG

Đã gỡ hẳn method này khỏi `RegulationConfigService.php` (không còn xuất hiện trong file sau khi
đọc toàn bộ 267 dòng). Không còn nơi nào gọi nó (đã kiểm tra file service đầy đủ).

---

## Lỗi mới phát hiện trong delta

### [LOW/MEDIUM] `currentCompanyId()` không fail-closed khi `current_company_role` null/0

**File**: `Modules/MasterData/Http/Controllers/V1/RegulationConfigController.php:33-39`, dùng ở
`showCongno` (dòng 44), `store` (dòng 52).

```php
private function currentCompanyId(): int
{
    return (int) optional(auth()->user())->current_company_role;
}
```

`TpEmployee::getCurrentCompanyRoleAttribute()` (`app/Models/TpEmployee.php:88-104`) trả về
`$employee_info->company_role`, fallback `$employee_info->company_id` — cả hai đều có thể `null`
nếu bản ghi `employee_infos` của nhân viên chưa gán công ty. `(int) null = 0`.

`guard()` của controller này (`ResponseTrait::isCurrentEmployeeHasPermission`, dòng 183-191 của
`app/Http/Controllers/Api/Traits/ResponseTrait.php`) **chỉ kiểm tra nhân viên có permission
"Cài đặt cấu hình" hay không**, KHÔNG scope theo company — khác với helper cùng tên ở
`BaseModel`/`PermissionHelper` (ghi trong memory dự án). Nghĩa là một nhân viên có permission này
nhưng `employee_infos.company_role` VÀ `company_id` đều null/0 (dữ liệu setup thiếu công ty) vẫn
**qua được `guard()`**, rồi `currentCompanyId()` âm thầm trả về `0`:

- `showCongno`: `getCongnoConfig(0)` → `Company::findOrFail(0)` → lỗi 404/`ModelNotFoundException`.
  Không leak dữ liệu, nhưng lỗi khó hiểu (nhân viên tưởng bug hệ thống, không phải do thiếu setup
  company).
- `store`: **nghiêm trọng hơn** — `createCongnoVersion(0, ...)` chạy TRƯỚC, ghi thành công 1 dòng
  `regulation_scheduled_versions` với `scope_id = 0` (không có ràng buộc khoá ngoại tới
  `companies.id`), rồi mới gọi `getCongnoConfig(0)` để build response → **404 ở bước này**. Kết quả:
  request trả lỗi cho user, nhưng **đã để lại 1 bản ghi rác `scope_id=0`** trong DB (không
  transaction bọc toàn bộ flow của `store()`) — dữ liệu mồ côi, không company nào sở hữu, không tự
  dọn.

**Đề xuất fix** (không bắt buộc phải làm ngay, nhưng nên có trước khi release do đúng tinh thần
"fail-closed" của dự án — xem `CLAUDE.md` mục cờ phân quyền):
```php
private function currentCompanyId(): int
{
    $companyId = (int) optional(auth()->user())->current_company_role;
    abort_unless($companyId > 0, 422, 'Tài khoản chưa được gán công ty, không thể thao tác cấu hình');
    return $companyId;
}
```
Việc này chặn ngay tại 1 điểm dùng chung cho cả 4 method, không cần sửa gì thêm.

**Mức độ**: không phải regression của 5 finding đã đóng (không mở lại IDOR — `update`/`cancel` vẫn
fail-closed nhờ `abort_unless(scope_id === companyId)`, kể cả khi companyId=0 vì không có version
thật nào scope_id=0). Đây là gap độc lập, chỉ trúng khi dữ liệu nhân viên thiếu company — khả năng
xảy ra thấp trong vận hành bình thường, nhưng đáng sửa vì để lại rác DB khi trúng.

### [Ghi nhận, không chặn] Diff-snapshot của các bản pending còn lại có thể "stale" sau khi áp-ngay gộp nhiều bản (finding #3)

`createCongnoVersion`/`updateCongnoVersion` gọi `recomputeDiffChain($companyId)` **TRƯỚC** khi chạy
đuôi áp-ngay (`applyDueCongnoVersions`). Sau khi áp-ngay xong, baseline công ty (`companies.*`) đã
đổi nhưng `recomputeDiffChain` không được gọi lại — các bản `pending` còn sót (hiệu lực tương lai,
không nằm trong batch vừa áp) sẽ hiển thị `diff_snapshot` tính trên baseline CŨ (trước khi áp) cho
tới lần `create`/`update`/`cancel` tiếp theo mới được tính lại đúng.

Đây là **hành vi đã tồn tại trước cả patch này** (bản gốc cũng không recompute sau khi
`applyVersion()` chạy inline trong `create`), nhưng finding #3 mở rộng phạm vi áp-ngay từ "1 bản"
sang "tất cả bản đến hạn của công ty" — nghĩa là bề mặt lộ ra của gap này rộng hơn trước (nhiều bản
hơn có thể bị áp trong 1 request, tăng khả năng có bản pending tương lai bị stale ngay sau đó). Chỉ
ảnh hưởng HIỂN THỊ (cột "chênh lệch" ở màn cấu hình), không ảnh hưởng số liệu company thật hay thứ
tự áp dụng. Không chặn merge, nêu ra để backlog nếu cần.

---

## Rà theo lens dự án

- **Fail-closed permission**: `guard()` không đổi, chạy trước mọi suy luận company — không nới lỏng.
  Điểm gap duy nhất là `currentCompanyId()` không tự fail-closed khi = 0 (nêu ở trên).
- **Không tạo permission mới**: xác nhận — vẫn dùng `PERM_EDIT = 'Cài đặt cấu hình'` có sẵn.
- **Model `extends BaseModel`**: `RegulationScheduledVersion` không đổi trong diff, vẫn `extends BaseModel`.
- **Định dạng số**: không có hiển thị số mới trong 4 file này (service/controller/request/test) — N/A.
- **Line ending / không commit git**: không kiểm tra git log (không được yêu cầu commit); các file
  đọc được đều là code PHP thuần LF theo chuẩn `hrm-api`, không phải file CRLF nhạy cảm.
- **N+1**: `applyDueCongnoVersions` loop gọi `applyVersion` từng bản — mỗi bản mở 1 transaction +
  1 `Company::findOrFail`. Số lượng bản pending/due trong thực tế rất nhỏ (vài bản/công ty), không
  phải N+1 theo nghĩa truy vấn danh sách lớn — chấp nhận được, không phải anti-pattern cần chặn.

---

## VERDICT

**CHANGES-NEEDED** (nhẹ) — cả 5 finding gốc đã đóng đúng và test chứng minh thật (không giả/rỗng),
nhưng phát sinh 1 gap mới nên xử lý trước khi merge:

1. **[LOW/MEDIUM]** `RegulationConfigController.php:33-39` (dùng tại dòng 44, 52) —
   `currentCompanyId()` không fail-closed khi `current_company_role` null/0, có thể tạo bản ghi
   `regulation_scheduled_versions.scope_id=0` mồ côi qua `store()` khi nhân viên có quyền nhưng
   thiếu company trong `employee_infos`. Đề xuất: `abort_unless($companyId > 0, 422, ...)` ngay
   trong `currentCompanyId()`.

Không có finding nào trong 5 finding gốc bị mở lại. Mục "Ghi nhận, không chặn" (diff-snapshot
stale) không bắt buộc xử lý trước merge, đưa vào backlog nếu team đồng ý.
