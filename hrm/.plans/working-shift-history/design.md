# working-shift-history — Tóm tắt

## Mục tiêu
Bổ sung "Lịch sử thay đổi" cho màn **Ca làm việc** (`/timesheet/timeworking/working-shift`) — audit ai tạo/sửa/xóa/khóa-mở khóa ca làm việc nào, cũ → mới, lúc nào.

## Bối cảnh kỹ thuật
- Entity: `Modules\Timesheet\Entities\WorkShift` (bảng `working_shifts`).
- Màn list dùng `WorkingShiftController`:
  - `POST timesheet/timeworking/` → `store()` → `WorkShiftService::store()` (create + update). Lưu: các trường ca + 2 danh sách con: `punishment_rules` (khung giờ phạt, quan hệ hasMany) + `conn_infos` (máy chấm công, belongsToMany).
  - `PUT timesheet/timeworking/{workingShift}/toggle-lock` → `toggleLock()` (đổi `status` 1↔2 = Hoạt động↔Khóa).
  - `DELETE timesheet/timeworking/{id}` → `delete()` (chỉ khi `isCanDelete()`).
- Có nhánh store() "sửa hình thức chấm công" riêng trong controller khi `$id && !isCanDelete()` (chỉ update allow_conn/allow_app/place/conn_infos) — cũng cần log.

## Quyết định (đã chốt với user)
1. Track **TOÀN BỘ trường** (đầy đủ) + 2 danh sách con (máy chấm công + khung giờ phạt).
2. Ghi **cả 4 thao tác**: create + update + delete + lock/unlock (Khóa/Mở khóa).
3. Nút "Lịch sử thay đổi" **CHỈ ở màn danh sách** (dropdown thao tác từng dòng).
4. **KHÔNG** permission riêng (ai xem được màn thì xem lịch sử — mặc định skill).
5. Biến thể **full-snapshot** (lưu snapshot đầy đủ 2 phía, FE tự diff) — vì nhiều trường + có list + nhiều loại action.

## Thiết kế
- **DB**: bảng `working_shift_history` (module Timesheet): `working_shift_id` (index), `company_id` (nullable index — scope theo công ty khi liệt kê), `action` (create|update|delete|lock|unlock), `old_value`/`new_value` (JSON snapshot đầy đủ), `changed_by`, `changed_at`, timestamps. KHÔNG FK cứng, KHÔNG SoftDeletes.
- **BE**: `WorkShiftService`:
  - `buildShiftSnapshot($id)` — đọc `working_shifts` + `punishment_rules` + `conn_infos` (resolve TÊN máy chấm công), trả về mảng đầy đủ field + `conn_infos:[tên]` + `punishment_rules:[{type,time_from,time_to,working_hour_deducted,working_day_deducted}]`. Null nếu không tồn tại.
  - `store()`: nhánh create → sau khi lưu build snapshot → `logShiftHistory('create', null, new)`. Nhánh update → chụp snapshot TRƯỚC mutation → sau mutation build new → nếu JSON khác → `logShiftHistory('update', old, new)`.
  - `toggleLock()`: chụp old trước, update status, build new → log 'lock' (status=2) hoặc 'unlock' (status=1).
  - `logShiftHistory($id, $action, $old, $new)` — `changed_by = Auth::id()`, `company_id` từ snapshot, JSON_UNESCAPED_UNICODE.
  - `shiftHistories($id)` sort cũ→mới, trả `changed_by_name` (fullname ?? email ?? '—') + `changed_at` (d/m/Y H:i:s) + `changed_at_raw` (Y-m-d).
  - Controller: nhánh "sửa hình thức chấm công" trong `store()` cũng log update. `histories(Request)` đọc `working_shift_id`. `delete()` chụp snapshot TRƯỚC `delete()` → log 'delete'.
  - Route `GET timesheet/timeworking/histories` đặt **TRƯỚC** `/{id}`.
- **FE**: `components/timesheet/working-shift/WorkingShiftHistoryModal.vue` — `open(id, name)`, tự diff:
  - create/delete → hiển thị full snapshot (create xanh, delete đỏ) theo nhóm: Thông tin ca / Tính công / Cài đặt / Máy chấm công / Khung giờ phạt.
  - update → diff từng trường cũ(đỏ)→mới(xanh) + máy chấm công +xanh/−đỏ + khung giờ phạt +/−.
  - lock/unlock → hiện đổi Trạng thái.
  - Bộ lọc Thao tác/Người/ngày. Dot: create xanh / update+lock+unlock amber / delete đỏ.
  - Gắn vào màn list (dropdown-item "Lịch sử thay đổi").
- **FIELD_LABELS** (nhãn tiếng Việt, khớp form): name=Tên ca, code=Mã ca, start_at=Giờ bắt đầu ca, end_at=Giờ kết thúc ca, has_time_check_in=Chấm giờ vào, attendance_start_at_from/to=Chấm vào từ/đến, has_time_check_out=Chấm giờ ra, attendance_end_at_from/to=Chấm ra từ/đến, has_recess=Nghỉ giữa ca, recess_start_at=Nghỉ từ, recess_end_at=Nghỉ đến, has_recess_check_in=Nghỉ chấm ra, attendance_recess_start_at_from/to=Nghỉ chấm ra từ/đến, has_recess_check_out=Nghỉ chấm vào, attendance_recess_end_at_from/to=Nghỉ chấm vào từ/đến, allow_conn=Cho phép máy chấm công, allow_app=Cho phép app, location_conn_info_id=Địa điểm máy chấm công, labour_hour=Giờ công, labour_day=Ngày công, coefficient_normal_day/day_off/day_holiday=Hệ số ngày thường/nghỉ/lễ, setting_late_leave_early=Đi muộn về sớm, allow_setting_late=Cho phép đi muộn, allow_setting_leave_early=Cho phép về sớm, has_penalty_work_late_leaving_early=Phạt đi muộn/về sớm, has_notime_checkin=Không giờ vào bị trừ công, penalty_notime_checkin_hour/day=Trừ giờ/ngày khi thiếu giờ vào, has_notime_checkout=Không giờ ra bị trừ công, penalty_notime_checkout_hour/day=Trừ giờ/ngày khi thiếu giờ ra, has_calculation_overtime=Tính công ăn ca, excluded_no_enough_worktime=Loại trừ khi không đủ công, ca_dem=Ca đêm, no_meal_allowance=Không hỗ trợ tiền cơm, status=Trạng thái.

## Auth note
Auth model = `App\Models\TpEmployee`, id khớp Employee id → `user.info->fullname` (xem [[master-settings-notes]]).
