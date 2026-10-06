# Chuyển popup lịch sử màn Thiết lập sang khuôn chung (#10455 — Phase 4)

Khung đã dựng xong (30/09/2026, nhánh `develop`). Mỗi popup còn lại = **1 adapter BE + sửa chỗ gọi FE + xoá popup cũ**.
Các nhóm làm song song KHÔNG đụng file của nhau: không có mảng đăng ký chung, service tự tìm adapter theo tên.

Đọc trước: skill `entity-history` (SKILL.md §0a, §4, §4b + ui-base.md), skill `modal-popup` mục 0.

## 1. Kiến trúc

| Lớp | File |
| --- | --- |
| Interface | `hrm-api/app/Services/SettingHistory/SettingHistoryAdapter.php` |
| Base (dùng chung) | `hrm-api/app/Services/SettingHistory/AbstractSettingHistoryAdapter.php` |
| Service | `hrm-api/app/Services/SettingHistory/SettingHistoryService.php` (`getLogs`, `getFilterOptions`, `groupOfAction`) |
| Controller | `hrm-api/app/Http/Controllers/Api/V1/SettingHistoryController.php` (kiểm type → quyền → phạm vi) |
| Route | `hrm-api/routes/api.php`: `GET /api/v1/setting-histories/{type}/{id}` + `/{type}/{id}/filter-options` |
| Adapter mẫu | `Adapters/GeneralRegulationAdapter.php` (subset-diff, theo CÔNG TY) · `Adapters/LeaveTypeAdapter.php` (full-snapshot, theo DÒNG, có lock/unlock/delete) |
| Popup FE | `hrm-client/components/modal/SettingHistoryModal.vue` (V2BaseModal + SystemInfoSection, `endpoint-base="setting-histories"`) |

Luồng: `{type}` snake_case → `Str::studly` → `App\Services\SettingHistory\Adapters\<Studly>Adapter`.
`leave_type` → `LeaveTypeAdapter`, `overtime_hour` → `OvertimeHourAdapter`. Không có class → 400.

Service lo sẵn (adapter KHÔNG làm lại): người thực hiện + phòng ban (1 query cho cả danh sách), `action_group`
theo `SystemLogService::ACTION_GROUP_MAP` (action chưa khai như `delete` → nhóm Thay đổi trạng thái),
sắp mới → cũ, `created_at` / `created_at_raw`, filter-options (3 nhóm cố định + `HistoryPerformerOptions::forCompany`).

Base lo sẵn: nhãn/màu theo action (mặc định `CatalogHistoryService::ACTION_LABELS/COLORS`), diff, định dạng.

## 2. Viết 1 adapter — các bước

1. **Đọc popup cũ** (file `.vue`) và service ghi log BE: lấy đúng `FIELD_LABELS`, thứ tự trường, map enum,
   trường boolean, trường chữ (không format số), nhãn tiêu đề từng dòng (`ACTION_META` / chữ cứng trong template),
   và **PHẠM VI**: popup xem cả công ty (không có id) hay từng dòng (`?xxx_id=`).
2. **Tra quyền route cũ** ở `Modules/*/Routes/api.php` (`->middleware('checkPermission:...')`). Trả đúng tên đó trong
   `permissions()`; nhiều quyền nối `|` thì trả mảng nhiều phần tử. Route cũ không gắn quyền → trả `[]`.
3. Tạo `app/Services/SettingHistory/Adapters/<Studly>Adapter.php` extends `AbstractSettingHistoryAdapter`, khai:

| Hàm | Làm gì |
| --- | --- |
| `permissions()` | quyền xem (bước 2) |
| `authorize($id)` | chặn phạm vi, **không tin `$id`**. Theo công ty: `return $this->isCurrentCompany($id);`. Theo dòng: tra `company_id` của bản ghi (bản ghi đã xoá thì tra trên chính bảng log) rồi `isCurrentCompany(...)`. Bảng không có company (vai trò, người dùng…) → kiểm bản ghi thuộc phạm vi mà màn cũ cho xem |
| `fetchRows($id)` | `DB::table('<bảng>_history')->where(...)->get()` — **luôn kèm điều kiện công ty** giống service cũ. Cột bắt buộc: `id, action, old_value, new_value, changed_by, changed_at`. Bảng đặt tên cột khác thì `select('x as changed_at')` |
| `mapRow($row)` | trả `['changes' => …]` (+ tuỳ chọn `action`, `action_label`, `action_color`, `note`). Trả `null` để bỏ dòng |
| `fieldLabels()` | `['field' => 'Nhãn']`, thứ tự = thứ tự hiển thị |
| `formatValue($field, $value)` | dùng `formatBoolean` (Có/Không) · `formatText` (chữ) · `formatEnum($v, [..])` · `formatDate` (dd/mm/yyyy) · `formatNumberOrText` (số en-US `1,500` / `7.5`). Trống trả `null` — FE tự in `(trống)` |
| `actionLabels()` | (tuỳ chọn) giữ nhãn timeline cũ: `['create' => 'Thêm loại nghỉ', …]` |
| `performerCompanyId($id)` | (tuỳ chọn) mặc định công ty đang làm việc |

4. Dựng `changes[]` bằng hàm của base:
   - log **subset-diff** (JSON chỉ có trường đổi): `$this->subsetChanges($old, $new)`
   - log **full-snapshot**: `$this->snapshotChanges($old, $new)` (chỉ lấy trường khác nhau)
   - dòng **tạo mới / xoá** snapshot: `$this->snapshotList($new, 'new')` / `$this->snapshotList($old, 'old')`
   - **danh sách / bảng con** (quyền của vai trò, phòng ban áp dụng, khung giờ…): `$this->listChange('Danh sách quyền', $oldRows, $newRows, 'Quyền')`
     — phần tử là chuỗi (danh sách đơn giản) hoặc bản ghi `['__key' => id, '__name' => tên, 'Nhãn cột' => giá trị]`.
     Trả `null` khi không có gì đổi (đừng push `null` vào `changes`). Kết quả đúng DTO §4b (`added/removed/changed` + `*_label` + `*_rows`).
   - id → tên: tra danh mục **1 lần** cho cả danh sách (gom id từ mọi dòng trong `fetchRows` rồi cache vào property), KHÔNG query trong `mapRow` từng dòng.
5. **Nhóm lọc**: đặt `action` đúng nghĩa (create / update / lock / unlock / change_status / delete…). Thao tác làm
   đổi trạng thái mà log cũ ghi `update` → trong `mapRow` trả `'action' => 'change_status'` (xem skill §3a). KHÔNG khai lại
   `ACTION_GROUP_MAP`.
6. `php -l` file mới. Không sửa `SettingHistoryService` / base — thiếu hàm dùng chung thì báo người giữ khung (mục 6).

Ví dụ khung tối thiểu (theo công ty, subset-diff):

```php
class OvertimeRegulationAdapter extends AbstractSettingHistoryAdapter
{
    public function permissions(): array { return ['Thiết lập thông số']; }
    public function authorize($id): bool { return $this->isCurrentCompany($id); }
    public function performerCompanyId($id) { return (int) $id; }
    public function fetchRows($id)
    {
        return DB::table('overtime_regulation_history')->where('company_id', (int) $id)->get();
    }
    public function mapRow($row)
    {
        return ['action_label' => 'Cập nhật quy định làm thêm',
                'changes' => $this->subsetChanges($this->decode($row->old_value), $this->decode($row->new_value))];
    }
    protected function fieldLabels(): array { return ['max_hour_month' => 'Số giờ tối đa/tháng']; }
}
```

## 3. FE — thay popup

```vue
<SettingHistoryModal ref="historyModal" modal-id="history-<màn>" />
import SettingHistoryModal from '@/components/modal/SettingHistoryModal.vue'
```

- Theo công ty: `this.$refs.historyModal.open('<type>', this.$store.state.current_company, '<Tên màn>')`
- Theo dòng: `this.$refs.historyModal.open('<type>', item.id, '<mã> - <tên>')` → tiêu đề `Lịch sử thay đổi: <nhãn>`
- **Giữ nguyên** nút/menu "Lịch sử thay đổi" và điều kiện quyền `canViewHistory` đang có (chỉ thay handler).
- `modal-id` riêng mỗi màn (2 popup cùng trang không đụng nhau).
- Popup có nhiều phạm vi (vd `TimekeepingExemptionHistoryModal` theo `type`, `HumanSettingHistoryModal` theo `scope`)
  → mỗi phạm vi là 1 `{type}` riêng (`timekeeping_exemption`, `timekeeping_exemption_ctv`…), không nhét tham số query.
- Xoá file popup cũ sau khi grep `pages components layouts utils store mixins` + `e2e/` không còn ai import.
- Route lịch sử cũ ở BE: **GIỮ**, thêm 2 dòng ghi chú `// ĐÃ THAY THẾ (#10455 …)` ngay trên route (xem `Modules/Timesheet/Routes/api.php`, 2 route leave-type + general-regulations).

## 4. Test (bắt buộc trước khi báo xong)

1. `php -l` các file sửa.
2. API (token: `POST :8000/api/v1/users/auth/login` `{email:'namdangit@gmail.com',password:'2025Dns@2'}`):
   - `GET setting-histories/<type>/<id>` → 200, đủ khoá DTO (`id, action, action_label, action_color, action_group, actor_id, actor_code, actor_name, actor_dept_code, department_name, note, changes, created_at, created_at_raw`), mới → cũ, **log cũ vẫn hiện**, nhãn/giá trị khớp popup cũ.
   - `.../filter-options` → `actions` đúng 3 nhóm; `performers` = số NV công ty (công ty 1 = 783).
   - Công ty khác / bản ghi công ty khác → 403. Loại lạ → 400.
   - TK không có quyền → 403 (local: TK `manhnv.kd1@tanphat.com` id 30 không có "Thiết lập thông số"; đổi mật khẩu tạm, **lưu hash cũ rồi trả lại**).
3. Thao tác thật 1 lần mỗi loại action (sửa 1 trường, khoá/mở khoá, thêm, xoá dòng con…) → đọc API thấy dòng mới đúng nhóm/nhãn/giá trị.
4. Playwright (`python /opt/homebrew/opt/python@3.14/bin/python3.14`, `wait_until='domcontentloaded'`, token vào localStorage `access_token` ở origin `http://127.0.0.1:3000`):
   mở popup → tiêu đề, `Bộ lọc` (Loại hành động / Người thực hiện / Từ ngày / Đến ngày / Làm mới), nút `Đóng`, lọc 3 nhóm + người + ngày.
   Mẫu script: `pw_setting_history_sample.py` (cùng thư mục, test 2 màn mẫu) (logic: đọc `document.querySelector('.modal.show .system-info-section').__vue__`, gán `filters`, đọc `filteredItems`).
   Lưu ý: `SystemInfoSection` lọc NGAY khi chọn (không có nút "Tìm kiếm") — đó là hành vi chuẩn hiện hành của component dùng chung.
5. Dọn: ghi lại `max(id)` bảng log trước khi test, xoá log `> max` sau test, trả dữ liệu đã đổi về như cũ.

## 5. Bảng 15 popup còn lại (tra nhanh)

| Popup cũ | Endpoint cũ | Phạm vi | Gợi ý `{type}` |
| --- | --- | --- | --- |
| `components/setting/general/TimekeepingExemptionHistoryModal.vue` | `timekeeping-exemptions/histories?type=` | công ty × type | `timekeeping_exemption` (+ biến thể theo type) |
| `components/setting/overtime/OvertimeHistoryModal.vue` | `overtime_regulations/histories` | công ty | `overtime_regulation` |
| `components/setting/overtime/OvertimeHourHistoryModal.vue` | `timesheet/overtime-hour/histories?overtime_hour_id=` | dòng | `overtime_hour` |
| `components/setting/holiday/AttendanceWatchHistoryModal.vue` | `attendance_watch_regulations/histories` | công ty | `attendance_watch_regulation` |
| `components/setting/holiday/HolidayHistoryModal.vue` | `timesheet/holiday/histories?holiday_id=` | dòng | `holiday` |
| `components/setting/holiday/TruncatedLeaveHistoryModal.vue` | `timesheet/truncated-leave/histories?truncated_leave_id=` | dòng | `truncated_leave` |
| `components/setting/master/MasterSettingHistoryModal.vue` | `master-settings/histories` | công ty | `master_setting` |
| `components/setting/roles/RolePermissionHistoryModal.vue` | `timesheet/roles/histories?role_id=` | dòng | `role_permission` |
| `components/setting/employee-permission/EmployeePermissionHistoryModal.vue` | `timesheet/employees/histories?employee_id=` | dòng | `employee_permission` |
| `components/timesheet/working-shift/WorkingShiftHistoryModal.vue` | `timesheet/timeworking/histories?working_shift_id=` | dòng | `working_shift` |
| `pages/human/settings/components/HumanSettingHistoryModal.vue` | `human/settings/histories?scope=` | công ty × scope | `human_setting` (+ theo scope) |
| `pages/assign/settings/components/AssignConfigHistoryModal.vue` | `assign/configs/histories?company_id=` | công ty | `assign_config` |
| `pages/assign/settings/components/PriorityLevelHistoryModal.vue` | `assign/priority-levels/histories` | công ty | `priority_level` |
| `pages/assign/settings/components/DeadlineConfigHistoryModal.vue` | `assign/my-job/deadline-config/histories` | công ty | `deadline_config` |
| `pages/assign/settings/components/ProjectCloseConfigHistoryModal.vue` | `assign/project-close-configs/logs` | công ty | `project_close_config` |

Quyền từng route: tra `Modules/Timesheet/Routes/api.php`, `Modules/Human/Routes/api.php`, `Modules/Assign/Routes/api.php` (nhiều route nhóm chấm công gắn `Thiết lập thông số`; `timesheet/roles/histories` và `timesheet/employees/histories` KHÔNG gắn quyền ở route — xem controller có tự gate không trước khi chọn `[]`).

## 6. Không được làm

- Không đổi bảng log / không migrate / không sửa log cũ.
- Không sửa `SettingHistoryService`, `AbstractSettingHistoryAdapter`, `SettingHistoryController`, `SettingHistoryModal.vue`, `SystemInfoSection.vue` — cần thêm hàm dùng chung thì nhắn người giữ khung, tránh 3 nhóm sửa cùng file.
- Không khai lại 3 nhóm lọc / `ACTION_GROUP_MAP`; không tự suy "Người thực hiện" từ log.
- Không format số kiểu VN; không in `(trống)` ở BE.
