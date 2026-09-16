# Khai Quy chế – Cấu hình (gộp 3 miền) — Design (tóm tắt)

> Feature nhánh `gop_db`. Port từ ERP (hướng A — dùng lại bảng ERP có sẵn trên DB gộp, đắp thêm lớp
> versioning cho tính năng "hẹn ngày áp dụng"). Spec chi tiết:
> `docs/superpowers/specs/gop-db/2026-09-09-khai-quy-che-cau-hinh-design.md`

## Mục tiêu

Gộp về 1 màn HRM (`/master-data/regulation-config`) 3 miền cấu hình/quy chế đang nằm rải ở ERP:

1. **Cấu hình chung công ty** — 11 nhóm form (Chung, Báo giá–HĐ, Kỹ thuật, Giá bán, Chiết khấu, Thị
   trường, Công nợ, XNK, Hàng hóa, Quyết toán, Điều khoản). Phạm vi theo `company_id`.
2. **Quy chế kinh doanh theo phòng ban** — hoa hồng (bảng nhiều dòng), thưởng thêm lũy tiến (bậc thang),
   quy chế khác (quỹ rủi ro/% LN/hạn mức duyệt — chỉ cấp phòng ban). Phạm vi `department_id`/`part_id`.
3. Điểm mới so với ERP: **hẹn ngày áp dụng** (phiên bản có `effective_from` + `status`, tới ngày tự áp
   dụng, phiếu đã lập giữ bản chụp).

## Hiện trạng

- **UI đã xong (mock)**: `pages/master-data/regulation-config/index.vue` + `data.js` + menu master-data.
  Biến thể B (có "hẹn ngày áp dụng"). Chỉ dữ liệu tĩnh, chưa nối API.
- **Đang chốt**: hướng A (port ERP). Đang dò bảng/controller ERP nguồn (agent Explore).

## Quyết định lớn

- [x] Nguồn: **A — port bảng ERP có sẵn** (đã chốt).
- [x] Map từng miền → bảng ERP (đã dò xong 2026-09-09 — chi tiết ở spec mục 2).
  - Miền 1: `configs` (toàn hệ thống, singleton) + `companies`/`company_rule_commissions` (`company_id`) + `due_configs`/`company_due_configs` (công nợ).
  - Miền 2: `regulations` (polymorphic `objectable_type` = Department/Part) + cột trực tiếp trên `departments`.
- [ ] Cơ chế versioning "hẹn ngày": **ERP KHÔNG có** (chỉ audit-log diff, ghi đè trực tiếp) → HRM phải thiết kế mới. ĐANG brainstorm.
- [ ] Slice code đầu tiên (đề xuất: Cấu hình chung — nhóm form đơn giản, thiết lập pattern read/save + version).

## Phát hiện then chốt (2026-09-09)

ERP lưu 3 miền ở **3 nhóm bảng riêng**, không gộp, và **không có bảng versioning theo ngày hiệu lực**:
mọi thay đổi là overwrite bản ghi hiện hành + audit-log diff. Vì vậy "hẹn ngày áp dụng" là phần HRM
làm mới hoàn toàn — quyết định schema versioning là điểm brainstorm quan trọng nhất trước khi code.

## Trạng thái

Có mapping ERP. Chờ chốt cơ chế versioning "hẹn ngày áp dụng" → viết spec đầy đủ → duyệt → code.

## Slice 1 — Quyền

Gate quyền cho `RegulationConfigController` (tab Công nợ) dùng lại quyền có sẵn
**`'Cài đặt cấu hình'`** (seeder id 149, group "Cấu hình", `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`).
KHÔNG tạo quyền mới. Lý do: màn `regulation-config` chưa gắn quyền riêng ở FE; đối chiếu
`Modules/Human/Http/Controllers/Api/V1/CompanyController` cho thấy các endpoint sửa cấu hình công ty
ở đó không gate bằng quyền riêng nào (perm "Danh mục công ty" đang bị comment), nên tái dùng quyền
"Cài đặt cấu hình" là lựa chọn hợp lý nhất hiện có. `const PERM_EDIT = 'Cài đặt cấu hình';` trong controller.

**Middleware:** group route `/v1/master-data` bọc `auth:api` (khớp mọi module khác). 3 tầng chặn:
guest → 401 (middleware), đăng nhập nhưng thiếu quyền → 403 (`guard()` trong controller),
đủ quyền → 200. (Trước khi thêm auth:api, guest chạm controller → `ResponseTrait::isCurrentEmployeeHasPermission`
deref `auth()->user()` null → 500; auth:api fix triệt để.)

**FE lưu ý (Task 8):** màn hiện là mock chưa gắn quyền — khi nối API thật cần: (a) gửi JWT như mọi màn HRM;
(b) ẩn/hiện nút theo quyền "Cài đặt cấu hình" (fail-closed). Cần user xác nhận đây là quyền đúng khi dựng menu thật.

## Slice 3f — Lịch sử quy chế THẬT (①A) + Dirty-guard rời trang (②A) — ĐÓNG 2026-09-15

Hai việc cuối để đóng lớp lịch sử + trải nghiệm rời trang của màn (đã duyệt "ok theo đề xuất").

**①A — endpoint lịch sử thật (thay mock `HIST` ở FE):**
`GET /v1/master-data/regulation-config-history?scope=company|department[&department_id=]`
- Gate: middleware `checkPermission:Cài đặt cấu hình` + `guard()` (403) + `currentCompanyId()` (422).
  `scope` ∉ {company, department} → 422; `scope=department` bắt buộc `department_id` + `assertDepartmentInCompany`
  (fail-closed 403 nếu phòng ban không thuộc công ty hiện tại).
- `RegulationConfigService::getHistory($scope, $scopeId, $companyId)` GỘP 4 nguồn theo scope, sort `created_at` desc
  với tie-break khóa phụ `_seq` (PHP 7.4 `usort` KHÔNG stable → cùng-giây phải ổn định theo thứ tự nạp), cắt `HISTORY_LIMIT=50`
  **SAU** sort. Trả **mảng vị trí 6 phần tử** mỗi dòng: `[timeStr, whoName, contentStr, scopeAppliedName, noteStr, isScheduledBool]`.
- Nguồn theo scope:
  - company: `regulation_config_histories` (company scope_id + global scope_id=0) + `company_regulation_histories` (company_id)
    + `regulation_scheduled_versions` pending (company + global).
  - department: `regulation_config_histories` (department) + `regulation_histories` (department_id, logs json cho grid hoahong)
    + `regulation_scheduled_versions` pending (department).
- Format: time `d/m/Y H:i`; who = "code - fullname" (join employees↔employee_infos trong **1 query**, không N+1);
  content mỗi field `"{label}: {old} → {new}"` nối "; ", `number_format` QUỐC TẾ (`,` nghìn `.` thập phân),
  bool→Có/Không, null/''→"—", >3 field → 3 + " …(+N)"; scheduled prefix "Hẹn phiên bản mới — ";
  scopeApplied: global→"Toàn hệ thống", company→companies.name, department→departments.name;
  note: applied→"Đã áp dụng", pending→"Hiệu lực {dd/mm/yyyy}".

**②A — cảnh báo chưa lưu khi rời tab/scope/phòng ban:**
`index.vue` dùng mixin `@/utils/mixins/unsavedChangesMixin` (`unsavedSnapshotSource(){ return this.model }`).
`guardLeaveDirty()` bật `$confirm` khi chuyển tab (`selectGroup`), đổi scope (`setScope`), đổi phòng ban (`onDeptChange`
hoàn tác `selectedDeptId=prevDeptId`); xác nhận rời thì `revertCurrentTab()` **re-fetch** tab đang rời để bỏ edit dở
RỒI mới `markFormPristine()`. Dùng `markFormPristine()` (KHÔNG `markFormSaved()`) — reset baseline nhưng GIỮ cảnh báo cho
lần sửa sau — gọi sau onSave/onCancel/saveVer/cancelPending/saveReg/deleteReg. `beforeRouteLeave` dùng bản built-in của mixin.
`data.js` gỡ export `HIST` + `SCOPE_UNITS`; giữ `CURRENT_COMPANY` (index.vue còn dùng).

**Review + test:** review độc lập (opus) APPROVED, không blocker (2 MEDIUM + 3 LOW + 2 NIT). Fix round 1 xử
M1 (sort ổn định `_seq`), M2 (revert model thật, không chỉ markFormPristine), L1 (truyền `$type` cho field company),
L2 (null-safe `created_at`), L3 (3 test tầng HTTP 403/422). `RegulationHistoryTest` = 6 test (3 service + 3 HTTP) →
full MasterData suite **82/82 PASS**. CR=0 cả 6 file (Routes/api.php, RegulationConfigController, RegulationConfigService,
RegulationHistoryTest, index.vue, data.js). NOT committed (rule gop_db).

**Kết quả:** màn code-complete 14 tab (company scalar/text/csv/json/subtable + global + department form/ladder/grid)
+ lịch sử thật + dirty-guard. Blocked: QA trình duyệt (chưa deploy dev) + quyết định commit/merge (git chưa uỷ quyền).

## Slice 1 — Task 8: cách lấy `companyId` ở FE

Đã nối tab `congno` (`pages/master-data/regulation-config/index.vue`) với API thật
(`GET/POST/PUT/DELETE master-data/regulation-config/congno[...]`). `companyId` lấy
theo đúng pattern dùng chung toàn repo (grep thấy ở ≥10 màn khác, vd
`pages/timesheet/attendance/index.vue:428-433`, `pages/decision/decision-reward/*`):

```js
companyId() {
    const info = this.$store.state.current_employee_info
    const emp = this.$store.state.current_employee
    return (info && info.company_role) || (emp && emp.company_id) || null
},
```

Ưu tiên `current_employee_info.company_role` (công ty NV đang thao tác — có thể
khác `company_id` gốc nếu NV multi-company), rớt về `current_employee.company_id`.
2 state field được set lúc login ở `store/actions.js:93-94`.

⚠️ **Chưa gắn quyền ở FE cho Task 8** (đúng scope brief chỉ yêu cầu nối API, không
yêu cầu ẩn/hiện nút theo quyền) — mục "FE lưu ý" phía trên vẫn còn treo, cần làm ở
task riêng trước khi lên production.
