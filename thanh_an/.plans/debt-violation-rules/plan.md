# Phiếu xác định & quy tắc xử lý vi phạm công nợ — Plan

**Người phụ trách:** @khoipv
**Ngày bắt đầu:** 2026-05-18
**Trạng thái:** Đã có spec, chưa code
**Spec:** `docs/superpowers/specs/2026-05-18-debt-violation-rules-design.md`
**Mock:** `hrm-thanhan-client/pages/timesheet/setting/debt-limit/canh-bao-cong-no-v4.html` (mục 4)

---

## Phase 1 — BE Database (Task 1)

- [x] **Task 1:** 2 migrations + seed 1 row default
  - File: `hrm-thanhan-api/database/migrations/2026_05_18_110000_create_debt_violation_rules_table.php`
    - Schema: `id`, `doc_types` (json), `violation_action` (enum APPROVE|BLOCK default APPROVE), `created_by` (unsignedBigInteger nullable), `updated_by` (unsignedBigInteger nullable), `timestamps`
    - Seed 1 row: `doc_types = ["DELIVERY","VAT"]`, `violation_action = "APPROVE"`
  - File: `hrm-thanhan-api/database/migrations/2026_05_18_110001_create_debt_violation_rule_logs_table.php`
    - Schema: `id`, `debt_violation_rule_id` (unsignedBigInteger, FK cascade delete), `action` (enum create|update), `old_value` (json nullable), `new_value` (json), `changed_by` (unsignedBigInteger nullable), `changed_at` (timestamp), index `debt_violation_rule_id`
    - Seed 1 row log create tương ứng row config seed, `old_value = null`, `new_value = {doc_types:["DELIVERY","VAT"], violation_action:"APPROVE"}`

## Phase 2 — BE Models (Task 2)

- [x] **Task 2:** Tạo 2 model trong `Modules/Timesheet/Entities/`
  - File: `hrm-thanhan-api/Modules/Timesheet/Entities/DebtViolationRule.php`
    - `protected $guarded = []`
    - `protected $casts = ['doc_types' => 'array']`
    - Relation `logs()` → `hasMany(DebtViolationRuleLog::class)->orderByDesc('changed_at')`
  - File: `hrm-thanhan-api/Modules/Timesheet/Entities/DebtViolationRuleLog.php`
    - `public $timestamps = false`
    - `protected $guarded = []`
    - `protected $casts = ['old_value' => 'array', 'new_value' => 'array', 'changed_at' => 'datetime']`

## Phase 3 — BE API (Task 3-5)

- [x] **Task 3:** Request validator `DebtViolationRuleRequest`
  - File: `hrm-thanhan-api/Modules/Timesheet/Http/Requests/DebtViolationRuleRequest.php`
  - `authorize()` return `true`
  - Rules: `doc_types: required|array|min:1`, `doc_types.*: required|in:DELIVERY,VAT,EXPORT,SALES`, `violation_action: required|in:APPROVE,BLOCK`
  - Messages tiếng Việt:
    - `doc_types.required` / `.min` / `.array`: "Vui lòng chọn ít nhất 1 loại phiếu xác định tính nợ"
    - `doc_types.*.in`: "Loại phiếu không hợp lệ"
    - `violation_action.required` / `.in`: "Vui lòng chọn quy tắc xử lý vi phạm"

- [x] **Task 4:** Controller `DebtViolationRuleController` với 3 method
  - File: `hrm-thanhan-api/Modules/Timesheet/Http/Controllers/DebtViolationRuleController.php`
  - `show()`: query first row; nếu null → create row default + log action=create với `changed_by=auth()->id()`; return `['data' => $rule]`
  - `update(DebtViolationRuleRequest $request)`:
    - `firstOrFail()` row
    - Snapshot `oldSnapshot = ['doc_types' => $rule->doc_types, 'violation_action' => $rule->violation_action]`
    - Snapshot `newSnapshot = ['doc_types' => $request->doc_types, 'violation_action' => $request->violation_action]`
    - Nếu `oldSnapshot != newSnapshot` → update row + tạo log action=update với old/new snapshot
    - Return `['data' => $rule->fresh(), 'message' => 'Lưu cấu hình thành công']`
  - `history()`:
    - Query logs join `users` lấy `full_name` (xác minh tên cột thực tế: `full_name` hay `name`)
    - `COALESCE(users.full_name, '(Không xác định)') as changed_by_name`
    - Order desc `changed_at`
    - Map response: `{action, old_value, new_value, changed_by_name, changed_at: format 'd/m/Y H:i'}`
    - Return `['data' => $logs]`

- [x] **Task 5:** Routes
  - File: `hrm-thanhan-api/Modules/Timesheet/Routes/api.php`
  - Thêm group `prefix('timesheet/setting/debt-violation-rule')` với middleware `auth:api` (đồng nhất với các route setting khác trong module Timesheet):
    - `GET /` → `show`
    - `PUT /` → `update`
    - `GET /history` → `history`

## Phase 4 — FE Page (Task 6-8)

- [x] **Task 6:** Page `pages/timesheet/setting/debt-limit/index.vue`
  - Constants:
    - `DOC_TYPE_OPTIONS`: 4 option `{value, text}` cho DELIVERY/VAT/EXPORT/SALES (labels: "Phiếu giao hàng", "Hóa đơn VAT", "Phiếu xuất kho", "Phiếu bán hàng")
    - `VIOLATION_ACTION_OPTIONS`: 2 option (APPROVE/BLOCK) với label kèm mô tả ngắn
  - Data: `form: {doc_types: [], violation_action: 'APPROVE'}`, `errors: {}`, `saving: false`
  - Template:
    - `PageHeader` với breadcrumb `[{Cài đặt}, {Cảnh báo công nợ}]`
    - Card chứa 2 section:
      - Section 1: title "Phiếu xác định tính nợ" + mô tả + `b-form-checkbox-group` stacked + error message đỏ
      - Section 2: title "Quy tắc xử lý vi phạm" + mô tả + `b-form-radio-group` stacked
    - Footer: 2 nút "Lịch sử" (variant light, icon fa-history) + "Lưu" (variant success, icon fa-save, disabled khi `saving`)
  - Methods:
    - `fetch()`: GET `timesheet/setting/debt-violation-rule` → set `form.doc_types` và `form.violation_action`. Verify tên store action thực tế (`apiGetMethod` hoặc tương đương) và điều chỉnh theo helper repo.
    - `validate()`: clear errors; nếu `form.doc_types.length === 0` → `errors.doc_types = 'Vui lòng chọn ít nhất 1 loại phiếu xác định tính nợ'` + return false
    - `save()`: validate → PUT → toast success + reload qua `fetch()`; catch lỗi → toast error với message từ `e.response.data.message`
    - `openHistory()`: gọi `$refs.historyModal.open()`
  - `mounted()`: await `fetch()`
  - Component register: `DebtViolationHistoryModal` (file ở Task 7)

- [x] **Task 7:** Modal `pages/timesheet/setting/debt-limit/components/DebtViolationHistoryModal.vue`
  - Bê pattern `pages/category/product_unit_price/components/PriceHistoryModal.vue` (timeline UI, `ho-timeline-*` classes)
  - Modal id: `debt-violation-history-modal`, title "Lịch sử thay đổi cấu hình"
  - Data: `loading`, `historyItems: []`
  - Constants tái dùng từ page: `DOC_TYPE_LABELS`, `VIOLATION_ACTION_LABELS` (hoặc tách ra file shared)
  - Method `open()`: show modal, fetch history
  - Method `fetchHistory()`: GET `timesheet/setting/debt-violation-rule/history` → set `historyItems`
  - Method `parseHistoryItem(log)`:
    - Nếu `action === 'create'`: label "Khởi tạo cấu hình", `changes = [{label: 'Phiếu xác định', new: log.new_value.doc_types.map(t => DOC_TYPE_LABELS[t]).join(', ')}, {label: 'Quy tắc xử lý', new: VIOLATION_ACTION_LABELS[log.new_value.violation_action]}]`
    - Nếu `action === 'update'`: label "Cập nhật cấu hình", build 2 row diff:
      - Row "Phiếu xác định": old/new label list; `is_changed = !arraysEqual(old, new)`
      - Row "Quy tắc xử lý": old/new label; `is_changed = old !== new`
  - Template timeline:
    - Mỗi item: dot màu (green=create, amber=update), thời gian (`changed_at`), label action, actor (`changed_by_name`)
    - Bảng diff `table-sm`: cột "Trường" / "Cũ" / "Mới" (cột Cũ chỉ hiển thị khi action=update)
    - Row có `is_changed=true` → highlight `bg: #fef9c3`, cột cũ gạch chân đỏ, cột mới chữ xanh
    - Action=create → 2 row hiển thị cả 2 trường (chỉ cột "Mới")
  - Footer: nút Đóng (variant danger)

- [x] **Task 8:** Menu entry "Hạn mức công nợ"
  - File: `hrm-thanhan-client/components/SettingSlidebar.vue` (đã có sẵn từ trước, dòng 75-82)
  - Label: "Hạn mức công nợ", icon `fas fa-file-invoice`, route `/timesheet/setting/debt-limit`
  - Đã align page title + breadcrumb với label menu để tránh nhầm lẫn

## Phase 5 — Test (Task 9)

- [ ] **Task 9:** User test end-to-end 8 case
  1. Chạy `php artisan migrate` → 2 bảng được tạo, có 1 row config + 1 row log create
  2. Mở `/timesheet/setting/debt-limit` lần đầu → form load đúng default (Phiếu giao hàng + Hóa đơn VAT đã tick, BGĐ phê duyệt được chọn)
  3. Bỏ tick hết 4 loại → click Lưu → hiện lỗi đỏ "Vui lòng chọn ít nhất 1 loại phiếu xác định tính nợ", không gọi API
  4. Tick thêm "Phiếu xuất kho" → đổi action sang BLOCK → click Lưu → toast "Lưu cấu hình thành công" + form reload đúng giá trị mới
  5. Click Lưu lại không đổi gì → toast success vẫn hiện nhưng DB log không tăng (verify bằng count `debt_violation_rule_logs`)
  6. Mở modal "Lịch sử" → thấy 2 entry: 1 create (chỉ cột Mới, label "Khởi tạo cấu hình"), 1 update (có cột Cũ + Mới, row "Phiếu xác định" và "Quy tắc xử lý" đều highlight vàng)
  7. Logout user A, login user B, sửa config → mở lại modal → entry mới có `changed_by_name` = tên user B
  8. (Optional) Xóa account user vừa sửa → mở modal → fallback `(Không xác định)`

## Note: ràng buộc khi implement

- **Tên cột users**: xác minh `users.full_name` vs `users.name` (grep 1 trong vài file controller Timesheet thấy column nào hay dùng) — điều chỉnh ở Task 4.
- **Tên store action FE**: xác minh tên action thực tế (`apiGetMethod`, `apiPutMethod` hoặc namespace khác như `apiSetting/getDebtRule`) — điều chỉnh ở Task 6 & 7. Có thể dùng `this.$axios.$get/$put` trực tiếp nếu repo follow pattern đó.
- **Vị trí file menu**: xác minh khi implement Task 8 — không hard-code path nếu chưa chắc.
- **Toast helper**: verify `this.$toasted.global.success/error` có sẵn (grep `payment-working-fee` để chắc chắn).

## Checkpoint — 2026-05-18
Vừa hoàn thành: Code Task 1-8 (BE migrations + models + request + controller + routes; FE page + history modal; menu đã có sẵn, align page title)
Đang làm dở: User chạy `php artisan migrate` (tại `hrm-thanhan-api/`) → test browser theo Task 9
Bước tiếp theo: User reload FE + chạy migration + test 8 case → báo lỗi nếu có
Blocked: (không có)

## Files đã tạo / sửa

**BE (`hrm-thanhan-api/`):**
- Created `database/migrations/2026_05_18_110000_create_debt_violation_rules_table.php`
- Created `database/migrations/2026_05_18_110001_create_debt_violation_rule_logs_table.php`
- Created `Modules/Timesheet/Entities/DebtViolationRule.php`
- Created `Modules/Timesheet/Entities/DebtViolationRuleLog.php`
- Created `Modules/Timesheet/Http/Requests/DebtViolationRuleRequest.php`
- Created `Modules/Timesheet/Http/Controllers/Api/V1/DebtViolationRuleController.php`
- Modified `Modules/Timesheet/Routes/api.php` (thêm 3 routes + import)

**FE (`hrm-thanhan-client/`):**
- Created `pages/timesheet/setting/debt-limit/index.vue`
- Created `pages/timesheet/setting/debt-limit/components/DebtViolationHistoryModal.vue`
- Menu `components/SettingSlidebar.vue` đã có sẵn entry (không sửa)
