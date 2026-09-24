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

## Bổ sung 3 trường DSTC vào tab "Báo giá – Hợp đồng" (22/09/2026)

Yêu cầu user: thiếu 3 trường (đã có bên ERP) → bổ sung, viết THẲNG 3 bảng ERP có sẵn
(`company_price_types`, `company_product_types`, `company_rule_commissions`), đặt ở tab
`baogia`, có HẸN NGÀY ÁP DỤNG (user uỷ quyền tự thiết kế cơ chế), hành vi GIỐNG ERP.

### 3 trường (label khớp 1-1 registry ⇄ data.js)
| # | Label | Bảng ERP | fk | Cột sửa được | Preset |
|---|---|---|---|---|---|
| ① | Hệ số quy đổi loại giá tính DSTC | company_price_types | company_id | coefficient | price_types (order) + dòng ảo id=99 "Giá dịch vụ" |
| ② | Hệ số quy đổi theo tính chất hàng hóa tính DSTC | company_product_types | company_id | coefficient | PRODUCT_TYPES lọc theo configs.product_types + dòng ảo 'service' "Dịch vụ" |
| ③ | Tỷ lệ chia DS theo quy chế phối hợp thực hiện | company_rule_commissions | company_id | 3 % (main/sup1/sup2) | 5 dòng RULE_COMMISSIONS ERP: (2,1,1)(2,1,2)(2,3,3)(3,1,1)(3,1,2) |

### Cơ chế (quyết định đã chốt — user uỷ quyền thiết kế "hẹn ngày")
- **KHÔNG bảng/pipeline mới.** Dùng lại NGUYÊN cơ chế `type=subtable` (như "Bảng tính công khoán"/
  contract_rows) nhưng **store=company, fk=company_id** thay vì config. 3 trường đi CHUNG version công ty
  của tab baogia (SCOPE_MIXED, no_hen=false → hỗ trợ hẹn qua `regulation_scheduled_versions`; cron
  `regulation-config:apply-scheduled` → applyDueVersions() tự quét vì baogia có field scalar company).
- **Áp = REPLACE-ALL** (xoá theo company_id + insert lại) trong transaction applyVersion — khớp ERP
  `Company::syncPriceTypes/syncProductTypes/syncRuleCommissions` (đều delete+insert).
- **Preset (giống ERP)**: dòng CỐ ĐỊNH, user chỉ sửa hệ số/%. `loadSubtable` merge preset (base rows từ
  nguồn ERP) với giá trị đã lưu theo cột định danh (price_type_id / product_type_id / room+deliv+cust).
- **Diff/lịch sử**: subtable so ở mức toàn bảng (json_encode), không phải field số → vào
  `RegulationConfigHistory` (json diff), scope=company. Không đụng company_regulation_histories.

### Thay đổi generalize (dùng chung, không phá contract_rows)
- `loadSubtable($meta,$scopeId)`: fk=company_id → dùng $scopeId; fk=config_id → configs singleton (như cũ).
  Cast theo cột (`cast`: int/decimal/string/json; mặc định number→int, else→json = tương thích contract_rows).
  Có `preset` tag → merge preset.
- `applySubtable($meta,$fkValue,$rows)`: cast theo cột khi insert (thêm decimal/string ngoài int/json).
- `applyVersion` nhánh store=company: TÁCH field subtable (applySubtable company_id) khỏi cột companies
  (giống nhánh global đã làm cho contract_rows) — nếu không sẽ gán mảng vào cột không tồn tại.
- `getTabConfig` cột subtable: thêm passthrough `unit` (suffix % / hệ số cho FE).
- `resolveOptions`: thêm `inline:coordination_address` (1 Thuộc phòng thực hiện / 2 Thuộc phòng hỗ trợ /
  3 Thuộc cả 2 phòng) cho 2 cột địa chỉ của ③.
- `ScheduleRegulationVersionRequest`: item_rules per-cột (coefficient required|numeric|min:0|max:99.99;
  3 % required|numeric|min:0|max:100) + withValidator branch `preset_rule_commissions` chặn tổng %≠100/dòng
  (room=2 ẩn sup2=0 → main+sup1 phải=100, giống ERP CompanyRegulationRequest).

### FE
- `data.js`: helper `subPreset(label,rowHeader)` (t=subtable, preset:true) + 3 field vào group baogia.
- `RegulationConfigScreen.vue`: editor mới `f.t==='subtable' && f.preset` — cột đầu = nhãn dòng (r.name cho
  ①②; ③ ghép "N phòng · Giao: X · KH: Y" từ options địa chỉ) READ-ONLY, các cột số (input==='number')
  render V2BaseInput; ③ ẩn ô sup2 khi room_qty==2 (hiện "—", giữ 0) — khớp ng-if ERP. applyTabToModel/
  collect subtable branch dùng lại NGUYÊN (map theo f.cols): cột number→Number, còn lại (định danh)→raw.

## #13 — Quy chế thưởng năm (port ERP "Cấu hình thưởng cuối năm công ty")

Bổ sung khâu KHAI thưởng cuối năm mà HRM thiếu; port màn ERP `admin/companies/{id}/config-bonus-end-year`
thành nhóm MỚI **"Quy chế thưởng năm"** ở phạm vi **Theo công ty**. Spec đầy đủ:
`docs/superpowers/specs/gop-db/2026-09-24-khai-quy-che-thuong-nam-design.md`.

- **SHAPE mới `SHAPE_DEPT_GRID`** (khác hoahong=grid per-row scope phòng ban, khác subtable=preset dòng cố
  định): lưới ĐỘNG theo phòng ban, scope công ty, lưu **replace-all cả form** theo `company_id` (delete →
  reinsert trong transaction) — khớp ERP `storeConfigBonusEndYear`. KHÔNG qua version pipeline.
- Ghi thẳng bảng ERP **`company_bonus_end_year_configs`** (đã có trong DB gộp, 0 dòng — gop_db convention:
  không migration/bảng mới). Entity mới `extends Model` (bảng ERP) → service tự gán created_by/updated_by.
- 6 cột/dòng: department_id · bonus_rate · settlement_type (1 DSTC quyết toán/2 Lợi nhuận phòng/3 Lợi nhuận
  công ty) · reserve_fund_percent **XOR** reserve_fund_value · max_risk_reserve_fund. Validate: department
  bắt buộc + không trùng; bonus_rate số; settlement_type ∈{1,2,3}; %/value không cùng >0.
- BE: registry const+tab · Entity mới · service getDeptGridConfig/saveDeptGrid · controller show() nhánh
  DEPT_GRID + endpoint saveDeptGrid + route `regulation-config/{tabKey}/dept-grid` · FormRequest
  RegulationDeptGridRequest. FE: data.js group + renderer `dept-grid` trong RegulationConfigScreen.vue.

### Quyết định đã chốt (#13)
- **A** Approach A (SHAPE_DEPT_GRID + nhánh replace-all riêng) — user "ok".
- **B** Khai theo công ty · **không hẹn ngày** (`no_hen=true`) — user: "nó khai theo công ty", "ko hẹn".
- **C** Ghi thẳng `company_bonus_end_year_configs` có sẵn (không migration/bảng mới).
- **H** **KHÔNG ghi lịch sử** cho tab này (ERP cũng không; formatter lịch sử dựng cho field scalar → ép
  vào rủi ro cao). Rows vẫn có created_by/updated_by. Tab Lịch sử màn sẽ không hiển thị thưởng năm — chấp
  nhận, khớp ERP; đảo được sau nếu user yêu cầu.
- **G** GIỮ gate quyền `Cài đặt cấu hình` (KHÁC ERP ungated) — đúng thiết kế màn HRM, không thêm quyền mới.
