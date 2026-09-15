# Task 8 report — FE nối tab Công nợ với API thật

## File đã sửa

- `hrm-client/pages/master-data/regulation-config/index.vue`
- `hrm-client/pages/master-data/regulation-config/data.js`

Cả 2 file giữ nguyên LF thuần (đã kiểm `grep -c $'\r'` = 0 trước và sau khi sửa).

## Tóm tắt thay đổi

### `data.js`
- Thêm export `CONGNO_API_FIELD_KEYS`: mảng 7 `{key, label}` khớp 1-1 với
  `RegulationConfigService::CONGNO_FIELDS` (BE) — dùng để map 2 chiều giữa
  `field.label` (FE hiển thị) và `key` BE cần (`limit_export_debt_employee`,
  `adjust_odd_balance`, `overdue_date_max_customer`, `overdue_date_max_agency`,
  `overdue_date_max_service`, `warning_due_date`, `interest_rate`).
- Thêm comment đánh dấu group `congno` trong `DATA` là "đã nạp từ API thật", các
  giá trị `eff/pending/fields.val` mock chỉ còn là fallback hiển thị tạm lúc
  loading. Không đổi field nào khác, không đụng tab/group khác.

### `index.vue`
- Import thêm `CONGNO_API_FIELD_KEYS` từ `data.js`.
- `data()`: thêm `congnoLoading: false`, `congnoApi: null`; thêm `id: null` vào
  `verForm` (cần để PUT sửa đúng version khi mở modal Sửa lịch hẹn).
- `computed.companyId`: `(current_employee_info.company_role) || (current_employee.company_id) || null`
  — bám đúng pattern dùng chung toàn repo (xem mục "companyId" bên dưới).
- `watch.curGroup` (mới, `immediate: true`): khi `curGroup.id === 'congno'` và
  `scope === 'company'` và chưa nạp (`!congnoApi && !congnoLoading`) → gọi
  `fetchCongno()`. Thay cho cách polling trong `mounted()` vì `curGroup` đã là
  computed phản ánh đúng thời điểm user mở tab.
- Methods mới: `fetchCongno()`, `applyCongnoToModel(data)`, `collectCongnoValues()`,
  `cancelPending(pending)`.
- `openVer()`: thêm `id: p ? p.id : null` vào `verForm` khi mở modal sửa lịch hẹn
  (để `saveVer()` biết PUT vào version nào).
- `saveVer()`: guard `if (!this.verGroup || this.verGroup.id !== 'congno')` → tab
  khác giữ nguyên hành vi cũ (chỉ đóng modal). Nhánh `congno`: build payload
  `{company_id, effective_date, note, values}`, dispatch `apiPutMethod` (đang sửa)
  hoặc `apiPostMethod` (tạo mới), toast, đóng modal, gọi lại `fetchCongno()` để
  đồng bộ lại toàn bộ state (áp dụng ngay nếu ngày <= hôm nay, `pending` mới,
  diff đã recompute ở BE).
- Template:
  - `.vcur` trong khối `verbar` (dùng chung cho mọi tab `form`): thêm nhánh
    `v-if="curGroup.id === 'congno' && curGroup.isOriginal"` → hiện "Bản gốc"
    thay vì "từ {{ fmtDate(curGroup.eff) }}" khi `applied_version` là `null`.
    Guard chặt theo `id === 'congno'`, tab khác đi nhánh `v-else` y hệt code cũ.
  - Nút `.iconbtn.danger` (Huỷ lịch hẹn) trong `.vq-item` của khối `form`: thêm
    `@click="cancelPending(p)"`. `cancelPending()` tự guard
    `curGroup.id !== 'congno' → return` nên các tab `form` khác (báo giá, giá
    bán, chiết khấu, xnk, hàng hóa, điều khoản) bấm nút này vẫn không có tác
    dụng (giữ hành vi mock cũ) — chỉ tab `congno` thực sự gọi DELETE.
  - Khối `ladder` (department scope, `themquy`) và khối `grid` (`hoahong`)
    KHÔNG đụng — 2 tab đó không nằm trong scope Task 8.

## Vuex action đã dùng (bằng chứng grep `hrm-client/store/actions.js`)

```
export async function apiGetMethod(context, payload, options = {}) { ... const { data } = await axios.get(...); return data }   // line 1455
export async function apiPostMethod(context, options) { ... const { data } = await axios.post(`/api/v1/${options.url}`, options.payload, opt); return data }  // line 1474
export async function apiPutMethod(context, options) { ... const { data } = await axios.put(`/api/v1/${options.url}`, options.payload, opt); return data }   // line 1486
export async function apiDelete(context, url, options = {}) { ... const response = await axios.delete(`/api/v1/${url}`, ...); return response }              // line 400
```

Shape tham số:
- `apiGetMethod`: payload là **string URL** (hoặc object `{url, ...axiosConfig}`
  theo comment dòng 1453) → dùng `dispatch('apiGetMethod', 'master-data/...')`.
- `apiPostMethod` / `apiPutMethod`: nhận **object** `{url, payload}` → dùng
  đúng shape brief đề xuất.
- `apiDelete` (KHÔNG phải `apiDeleteMethod`): nhận **string URL trực tiếp** làm
  payload thứ 2 → `dispatch('apiDelete', 'master-data/.../versions/123')`.
  Đối chiếu pattern thật đang chạy: `pages/rice/category/conn-info/index.vue:311`,
  `pages/training/capability_groups/index.vue:591`, nhiều màn khác — tất cả gọi
  y hệt kiểu này rồi tự gọi lại API load-list để refresh (không dựa vào body trả
  về của delete). Task 8 làm theo đúng convention này: `cancelPending()` sau khi
  DELETE thành công gọi lại `fetchCongno()` thay vì cố bóc `response.data` của
  `apiDelete` (action này trả nguyên **axios response**, khác hẳn 3 action kia
  trả thẳng `response.data` — hai shape lẫn lộn nhau trong cùng file
  `actions.js`, rất dễ bóc sai nếu không grep kỹ).

## Cách bóc response envelope

BE (`RegulationConfigController` + `ResponseTrait::responseSuccessJson`) luôn trả:
```json
{ "code": 200, "message": "...", "data": { ... } }
```
(`ResponseTrait.php:211-218`, không có khoá `meta` — brief đoán `e?.response?.data?.meta?.message`
là SAI, đã sửa lại dùng `e.response.data.message` trực tiếp).

- `apiGetMethod` trả thẳng `response.data` (= envelope trên) → `fetchCongno()`
  dùng `res.data` để lấy đúng payload `{fields, applied_version, pending}`
  (`RegulationConfigService::getCongnoConfig`, `RegulationConfigController.php:36-38`).
- `apiPostMethod`/`apiPutMethod` cũng trả thẳng envelope, `data.data` chứa
  `{version, config}` (`RegulationConfigController.php:48-51, 61-64`) — nhưng
  Task 8 KHÔNG dùng `config` trả về trực tiếp mà gọi lại `fetchCongno()` (xem
  lý do lệch brief bên dưới).
- Lỗi validate (`ScheduleRegulationVersionRequest`) và lỗi `abort_unless(...,422,'msg')`
  (huỷ/sửa version không ở trạng thái pending) đều theo format Laravel mặc định
  `{"message": "...", "errors": {...}}` — cũng đọc bằng `e.response.data.message`.

## Cách lấy `companyId`

Grep pattern dùng chung ~15 file trong repo (không riêng brief đoán):
```
pages/timesheet/attendance/index.vue:428-433
  company_roles() { return this.$store.state.current_employee_info },
  auth() { return this.$store.state.current_employee },
  ... this.company_roles.company_role ?? this.auth.company_id
```
Cùng pattern lặp lại ở `pages/assign/job_requests`, `pages/decision/decision-reward/*`,
`pages/decision/employee-discipline/*`, `pages/timesheet/*` (≥ 10 chỗ).

→ Task 8 dùng đúng pattern này, viết gọn thành 1 computed:
```js
companyId() {
    const info = this.$store.state.current_employee_info
    const emp = this.$store.state.current_employee
    return (info && info.company_role) || (emp && emp.company_id) || null
},
```
`store/state.js:7,9` xác nhận 2 state field `current_employee` / `current_employee_info`
tồn tại thật, được set ở `store/actions.js:93-94` lúc login
(`current_employee = res.data.employee_data`, `current_employee_info = res.data.employee_info`).

**Đã ghi vào `design.md`** phần "cách lấy companyId" theo yêu cầu brief (xem mục
Cập nhật design.md bên dưới).

## Lệch so với brief — kèm lý do

1. **`e?.response?.data?.meta?.message` → `e.response.data.message`**: brief đoán
   sai envelope (không có `meta`). Đã xác minh bằng cách đọc thẳng
   `ResponseTrait::responseSuccessJson` (`code/message/data`, không `meta`) và
   format lỗi mặc định Laravel (`message/errors`).
2. **`saveVer()`/`cancelPending()` gọi lại `fetchCongno()` thay vì dùng `data.config`
   trả sẵn trong response POST/PUT/DELETE**: BE thực tế CÓ trả `config` mới trong
   `data.config` (`RegulationConfigController.php:48-51,61-64,73-75`) nên về lý
   thuyết có thể tiết kiệm 1 request. Nhưng:
   - `apiDelete` (action dùng cho Huỷ) trả **nguyên axios response**, khác hẳn
     shape `apiPostMethod`/`apiPutMethod` (trả thẳng `response.data`) — muốn bóc
     đúng `config` từ 3 action này phải viết 2 kiểu unwrap khác nhau, dễ sai.
   - Toàn bộ pattern CRUD hiện có trong repo (đối chiếu ~10 file `apiDelete`)
     đều KHÔNG dựa vào body trả về của thao tác ghi, mà gọi lại API load để
     refresh y hệt cách Task 8 đang làm.
   - Đây là thao tác quản trị (hẹn/sửa/huỷ version), tần suất thấp — đánh đổi
     "thêm 1 GET" lấy "code đơn giản, đúng convention, ít rủi ro bóc sai
     envelope" là hợp lý. Đã cân nhắc theo đúng tinh thần rule hiệu năng của
     CLAUDE.md (ít request) nhưng ưu tiên đúng-nhất-quán hơn vì đây không phải
     đường nóng (hot path).
3. **Thêm `v-if` "Bản gốc" vào `.vcur`**: brief Step 2 chỉ nói "set cờ
   `group.isOriginal`" nhưng không có nhánh template nào hiển thị nó — nếu
   không sửa template thì cờ vô nghĩa (`fmtDate(null)` vẫn hiện "—", không phải
   "Bản gốc" như spec yêu cầu). Đã thêm 1 dòng `v-if`/`v-else` guard chặt theo
   `curGroup.id === 'congno'`, tab khác đi nguyên `v-else` cũ, không đổi hành
   vi hiển thị của các tab đó.
4. **`this.$toasted?.global?.error?.(...)` → `this.$toasted.global.error(...)`**
   (bỏ optional chaining): đã grep xác nhận `$toasted` luôn được `inject` qua
   `plugins/toast.js` cho mọi trang (`Vue.toasted` + `inject('toasted', ...)`),
   không cần optional chaining; giữ nguyên style gọi thẳng như các màn khác
   đang dùng (`pages/rice/category/conn-info/index.vue:314` v.v.).

## Verify tĩnh đã làm (bằng chứng cụ thể)

- `node --check` trên nội dung `<script>` tách ra (đổi tạm sang `.mjs` để cho
  phép `import/export`) → **PASS** (`SCRIPT_SYNTAX_OK`).
- `vue-template-compiler` (`node_modules/vue-template-compiler`) compile riêng
  nội dung `<template>` → **PASS**, không lỗi, không tip.
- `node --check` cho `data.js` (qua bản sao `.mjs`) → **PASS**.
- `grep -c $'\r'` cả 2 file trước/sau khi sửa = 0 → LF được giữ nguyên, không
  bị script/editor nào lẫn CRLF.
- Grep xác nhận tồn tại thật: 4 action Vuex (`apiGetMethod/apiPostMethod/
  apiPutMethod/apiDelete` — không phải `apiDeleteMethod`), 2 state field
  `current_employee`/`current_employee_info`, route BE
  `master-data/regulation-config/congno[...]` (`Modules/MasterData/Routes/api.php:16-19`),
  cấu trúc trả về của `RegulationConfigService::getCongnoConfig` và 7 field
  key khớp `ScheduleRegulationVersionRequest::rules()`.
- Rà soát thủ công: mọi nhánh mới (`applyCongnoToModel`, nhánh template "Bản
  gốc", `cancelPending`, `saveVer` congno-branch) đều có guard `id === 'congno'`
  hoặc tương đương; các tab/group khác (`chung, baogia, kythuat, giaban,
  chietkhau, thitruong, xnk, hanghoa, quyettoan, dieukhoan, hoahong, themquy,
  khac`) không bị đổi hành vi — so khớp lại từng đoạn diff bằng Read trước/sau.

## Còn chờ kiểm trình duyệt (KHÔNG verify được trong môi trường này)

Không có dev server / browser trong môi trường này nên KHÔNG tự mở màn được.
Cần user (hoặc phase test riêng) xác nhận thủ công theo đúng Step 6 của brief:
- Mở `/master-data/regulation-config`, tab "Công nợ & tài chính" → 7 field nạp
  đúng từ BE, nhãn "đang áp dụng"/"Bản gốc" đúng theo `applied_version`.
- Hẹn phiên bản mới ngày tương lai → xuất hiện đúng ở "chờ áp dụng", diff hiển
  thị đúng nhãn/đơn vị/giá trị cũ-mới.
- Hẹn ngày = hôm nay → BE tự áp ngay (`createCongnoVersion` áp-ngay nếu
  `effective_date <= now`), field cập nhật, biến mất khỏi hàng đợi sau khi
  `fetchCongno()` chạy lại.
- Sửa/Huỷ phiên bản pending (nút bút chì/thùng rác) hoạt động đúng, hàng đợi
  cập nhật lại sau mỗi thao tác.
- Test permission: tài khoản không có quyền "Cài đặt cấu hình" gọi API phải
  nhận lỗi 403 và FE hiện toast lỗi tương ứng (nhánh `catch` đã viết nhưng
  chưa thấy trên trình duyệt thật).
- Kiểm định dạng số/ngày hiển thị đúng chuẩn hệ thống (`V2BaseCurrencyInput`
  dấu `,` nghìn, ngày `DD/MM/YYYY` qua `fmtDate()`).

## Cập nhật design.md

`design.md` thực tế nằm ở feature root
`HRM/.plans/gop-db/khai-quy-che-cau-hinh/design.md` (KHÔNG phải trong `sdd/` —
`sdd/` chỉ chứa `progress.md`, `global-constraints.md`, các `task-N-brief.md`
và `reports/`). Đã thêm mục mới **"Slice 1 — Task 8: cách lấy `companyId` ở
FE"** vào cuối file đó, nội dung khớp phần "Cách lấy companyId" ở trên.

## Concern cần controller lưu ý

`design.md` mục "Slice 1 — Quyền" (dòng 57-58, viết từ trước Task 8) đã ghi sẵn
yêu cầu: khi nối API thật phải **ẩn/hiện nút theo quyền "Cài đặt cấu hình"**
(fail-closed). Task 8 brief (5 step) KHÔNG yêu cầu việc này, nên **CHƯA làm** —
hiện tab `congno` gọi thẳng API không kiểm tra quyền ở FE (BE vẫn chặn 403 nếu
thiếu quyền qua `guard()`, nhưng nút "Hẹn phiên bản mới"/"Sửa"/"Huỷ" vẫn hiện
cho mọi user, bấm vào mới nhận lỗi). Đã ghi rõ thành mục treo trong design.md,
cần task riêng để bổ sung gate quyền ở FE trước khi lên production.
