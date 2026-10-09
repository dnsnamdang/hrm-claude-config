# T11b — Khuôn FE cho `pages/finance/borrow-sell-requests/create.vue` (Yêu cầu xuất bán hàng mượn)

Khảo sát read-only trên `hrm-client` (branch `gop_db`). Mục tiêu: xác định khuôn (mẫu) tốt nhất để
copy khi dựng màn Tạo mới PYCXBHM: chọn hợp đồng qua modal picker + lưới sản phẩm nhập SL + submit
`apiPostMethod`, tuân thủ CLAUDE.md (unsaved-changes, form-validate, fail-closed permission).

---

## 1. Khuôn tổng thể nên copy: kiến trúc "trang vỏ mỏng + Form component"

KHÔNG có 1 file `create.vue` "to" nào trong `pages/finance/*` vừa có picker vừa có lưới — mọi
`create.vue` hiện tại trong `pages/finance/` (28-64 dòng) chỉ là **trang vỏ** render 1 component
`Form` dùng chung cho cả Tạo mới lẫn Sửa. Đây chính là kiến trúc phải theo (kiến trúc "A'" — xem
comment trong `ProductExportRequestForm.vue` dòng 567-573).

**Cặp khuôn tốt nhất để mirror** (kết hợp 2 nguồn — không có file nào có đủ 100% một mình):

| Thành phần                         | Copy từ                                                                                     |
|-------------------------------------|-----------------------------------------------------------------------------------------------|
| Trang vỏ `create.vue` (thin wrapper)| `pages/finance/product-export-requests/create.vue` (64 dòng)                                  |
| Modal chọn hợp đồng (picker)        | `pages/finance/product-export-requests/components/ContractSearchModal.vue` (143 dòng)         |
| Lưới sản phẩm dạng "chọn dòng theo HĐ + nhập SL" | `ProductExportRequestForm.vue` phần bảng `isContractType` (dòng 284-370)          |
| Validate realtime + `V2Footer` + `unsavedChangesMixin` (khuôn MỚI nhất, đúng CLAUDE.md) | `pages/finance/bill-incomes/components/BillIncomeForm.vue` |

Vì PYCXBHM đã có sẵn `getContracts` + `getBorrowSellData(contractId)` (xem mục 4) — luồng đúng y
hệt `ProductExportRequestForm.vue` biến thể `isContractType` (loại 20/21): chọn HĐ qua modal → BE
trả về danh sách dòng hàng còn lại của HĐ → user tick chọn + nhập SL → submit.

### Cấu trúc trang vỏ (copy `product-export-requests/create.vue`)
```
<ProductExportRequestForm ref="form" mode="create" :submitting="submitting"
    @submit="onSubmit" @back="goBack" @ready="onFormReady" />
```
- `mixins: [PageTitleMixin, unsavedChangesMixin]`
- `unsavedSnapshotSource()` → `this.$refs.form.snapshotSource()` (đọc snapshot từ component con)
- `onFormReady()` → `this.$nextTick(() => this.markFormPristine())`
- `onSubmit(payload)` → `apiPostMethod` → `this.markFormSaved()` → toast → `$router.push`
- `applyServerErrors` lỗi 422 đẩy ngược vào `this.$refs.form`

### Cấu trúc Form component (theo `ProductExportRequestForm.vue`, 1855 dòng — chỉ đọc phần liên quan)
`data()` chính (dòng 591-...): `showContractModal`, `typeOptions`, `customerOptions`,
`warehouseOptions`, `form {...}`, mảng dòng hàng (`contractLines` tương đương).
`methods` chính: `openContractModal`, `onContractSelected(contract)` (gọi API lấy chi tiết HĐ),
`contractQtyValid(line)`, `linePrice(line)`, `submit(status)`/`onSubmitClick(status)`.

---

## 2. Modal chọn hợp đồng (picker) — KHÔNG dùng `V2BaseSelectInModal` cho việc này

Điểm quan trọng cần làm rõ (dễ nhầm với quy tắc CLAUDE.md): `V2BaseSelectInModal` là bắt buộc cho
**dropdown/select nằm bên trong 1 modal khác** (để dropdown không bị modal che). Việc "mở modal để
chọn 1 bản ghi cha từ bảng danh sách" (chọn hợp đồng, chọn phiếu đề nghị…) là **pattern khác** —
khuôn chung của module Tài chính gọi là `*SearchModal.vue`: 1 `b-modal` riêng chứa `V2BaseInput`
tìm kiếm + bảng `<table>` click-để-chọn cả dòng, emit `select`/`choose` rồi tự đóng.

File khuôn: `pages/finance/product-export-requests/components/ContractSearchModal.vue`
- Props: `show: Boolean`
- Emit: `select(contract)`, `close`
- `watch: { show(val) { if (val) { this.keyword=''; this.fetch() } } }`
- `fetch()` gọi `apiGetMethod` (ở đây `assign/contracts?...`) — với PYCXBHM đổi thành
  `api.getContracts(this.$store.dispatch, params)` (đã có sẵn trong `api.js`, xem mục 4)
- Click dòng `<tr @click="pick(c)">` → `pick(c) { this.$emit('select', c); this.$emit('close') }`
- Cha dùng:
  ```
  <ContractSearchModal :show="showContractModal" @close="showContractModal=false" @select="onContractSelected" />
  ```

Biến thể tương đương khác cùng khuôn (nếu cần đối chiếu thêm ô lọc theo người lập):
`pages/finance/bill-incomes/components/IncomeRequestSearchModal.vue` — dùng `b-modal` (thay vì tự
bind `:visible`) + `V2BasePagination`, và **có dùng `V2BaseSelectInModal`** nhưng CHỈ cho ô lọc
"Người lập" nằm bên trong modal đó (đúng đúng phạm vi bắt buộc của CLAUDE.md), không phải cho bản
thân việc chọn dòng hợp đồng/phiếu.

---

## 3. Lưới sản phẩm nhập SL theo hợp đồng

Khuôn: `ProductExportRequestForm.vue` dòng 284-370 (bảng `v-if="isContractType"`), trên `<template>`
thường (không phải `V2BaseDataTable`, không phải `b-table`) — bảng HTML thuần `<table class="table
table-bordered table-sm mb-0 er-table">` lặp qua `contractDisplayLines`.

Điểm mấu chốt:
- Checkbox chọn dòng: `<input type="checkbox" v-model="line._checked">` — chỉ hiện khi
  `line._selectable` (dòng cha nhóm/header thì ẩn checkbox, PYCXBHM khả năng không cần phân cấp
  cha/con nên có thể bỏ field `_isParentHeader`/`_isChild`).
- Input SL: 
  ```html
  <input type="number" class="form-control form-control-sm text-right"
      :class="{ 'is-invalid': line._checked && !contractQtyValid(line) }"
      min="0" :max="line.remaining_qty" step="any"
      :disabled="!line._checked" v-model.number="line._qty" />
  ```
  → hint "còn lại" hiển thị ở cột riêng (`{{ formatNum(line.remaining_qty) }}`) NGAY TRƯỚC cột nhập
  SL, không phải placeholder — và việc chặn vượt max làm bằng attribute `:max` (browser-level, chỉ
  mang tính gợi ý) **CỘNG** validate JS thật sự qua hàm `contractQtyValid(line)`:
  ```js
  contractQtyValid(line) {
      const q = Number(line._qty)
      return q > 0 && q <= line.remaining_qty   // (mirror qtyValid() ở warehouse-export-requests/create.vue)
  }
  ```
  Submit bị chặn nếu có dòng `_checked` mà `!contractQtyValid(line)` (xem
  `warehouse-export-requests/create.vue` dòng 372-376 cho pattern chặn ở `submit()`, thông báo lỗi
  format: `"Số lượng xuất của "${name}" phải lớn hơn 0 và không vượt quá ... (${max})."`).
- Không có nút "Thêm dòng" tự do cho biến thể theo hợp đồng — số dòng cố định = số dòng còn lại của
  HĐ trả về từ BE; user chỉ tick chọn + sửa SL. (Biến thể "nhập tay" ở dòng 393-450 mới có nút
  thêm/xoá dòng qua modal chọn sản phẩm — KHÔNG áp dụng cho PYCXBHM vì đã có nguồn HĐ.)
- Dòng rỗng: `<tr v-if="!contractDisplayLines.length"><td colspan=... class="text-center text-muted">
  {{ form.emplement_contract_id ? 'Hợp đồng không có dòng hàng phù hợp...' : 'Chọn hợp đồng để hiển thị hàng hoá.' }}</td></tr>`

Alternative đơn giản hơn (nếu PYCXBHM không cần biến thể cha/con phức tạp): mirror thẳng
`pages/finance/warehouse-export-requests/create.vue` (666 dòng, đọc toàn văn) — cùng pattern
checkbox + input SL + `:max="row.qty"` + `qtyValid(row)`, nhưng đơn giản/phẳng hơn nhiều (không có
biến thể cha/con, không nhiều loại phiếu). Class CSS blocks `.c-section`, `.section-header`,
`.kv-grid`, `.er-table`, `.export-actionbar` (fixed bottom action bar) ở file này có thể copy y
nguyên cho style tổng thể trang.

---

## 4. `pages/finance/borrow-sell-requests/api.js` (đã có từ Task 10/11) — dùng lại, không viết lại

Đã có sẵn đủ hàm cần cho create:
```js
export const getContracts       = (dispatch, params = {}) => dispatch('apiGetMethod', `${BASE}/contracts${qs(params)}`)
export const getBorrowSellData  = (dispatch, id, params = {}) => dispatch('apiGetMethod', `${BASE}/contracts/${id}/borrow-sell-data${qs(params)}`)
export const store              = (dispatch, payload) => dispatch('apiPostMethod', { url: BASE, payload })
export const list, show, deny, managerApprove, switchBoardOfManager, boardOfManagerApprove, printData
```
→ **KHÔNG cần thêm hàm mới**: `getContracts` = data nguồn cho `ContractSearchModal`-style picker,
`getBorrowSellData(id)` = data nguồn cho lưới sản phẩm sau khi chọn HĐ (tương đương
`onContractSelected` gọi API lấy chi tiết trong `ProductExportRequestForm.vue`), `store` = submit
tạo phiếu. Không thấy `getExportRequests` trong file — nếu spec Task 11 cần nguồn khác (phiếu xuất
kho) thì phải hỏi lại, hiện `api.js` chỉ có luồng theo **hợp đồng**.

`index.vue` (đã có, Task 10) gọi qua namespace `import * as api from './api'` rồi
`api.list(this.$store.dispatch, params)`, `api.deny(this.$store.dispatch, id, comment)` v.v. — page
create mới nên theo đúng cách import này (`import * as api from './api'`).

---

## 5. Quy ước CLAUDE.md cho form MỚI — khuôn chuẩn nhất: `BillIncomeForm.vue`

`ProductExportRequestForm.vue` (khuôn picker+grid ở mục 1-3) là code **cũ hơn**, KHÔNG dùng
`vee-validate`/`V2Footer`/`formValidateMixin` — chỉ tự dựng nút Lưu bằng `V2BaseButton` thường (xem
dòng 500-516). Khi build PYCXBHM (màn MỚI), phần validate + nút hành động + unsaved-guard phải theo
khuôn MỚI NHẤT đúng CLAUDE.md: `pages/finance/bill-incomes/components/BillIncomeForm.vue`.

- **unsavedChangesMixin**: `import unsavedChangesMixin from '@/utils/mixins/unsavedChangesMixin'`
  (dòng 486), `mixins: [unsavedChangesMixin, formValidateMixin]` (dòng 546). Gọi
  `this.markFormPristine()` ở cuối `mounted()` sau khi nạp xong data (dòng 719), và
  `this.markFormSaved()` ngay sau `apiPostMethod` thành công, TRƯỚC khi chuyển route (dòng 1209,
  trong hàm `save()`).
- **vee-validate realtime, CHỈ trường Tên bắt buộc ở FE**: file này không có trường "Tên" đúng
  nghĩa (là phiếu thu từ đề nghị có sẵn) nên không minh hoạ trực tiếp `v-validate="'required'"`,
  nhưng show đúng pattern lỗi kết hợp FE+BE:
  ```html
  <V2BaseLabel>Số phiếu đề nghị <Required /></V2BaseLabel>
  <V2BaseSelect ... :invalid="hasFieldError('bill_income_request_id')" />
  <V2BaseError v-if="hasFieldError('bill_income_request_id')" :message="fieldError('bill_income_request_id')" />
  ```
  `Required` là `@/components/common/Required` (dấu * đỏ hiển thị, không phải rule). Với PYCXBHM,
  trường "Tên"/tương đương gắn `v-validate="'required'"` thật + `data-vv-name` + `data-vv-as` theo
  đúng mẫu trong `.claude/skills/form-validate/SKILL.md` mục 2 (file không có ví dụ `v-validate`
  thật trong `BillIncomeForm.vue` vì màn này không có ô Tên tự do — cần bám sát SKILL.md hơn là bám
  file này cho phần `v-validate` cụ thể).
  `hasFieldError`/`fieldError`/`clearServerErrors` đến từ `formValidateMixin`
  (`utils/mixins/formValidateMixin.js`): `fieldError(name)` ưu tiên lỗi FE (`this.errors.first`)
  rồi mới tới lỗi BE (`this.formErrors[name]`), `formErrors` set trong `catch` khi submit lỗi 422.
- **`V2Footer` cho khối nút hành động** (dòng 460-466):
  ```html
  <V2Footer v-if="!readonly" :menu="footerMenu" url-back="/finance/bill-incomes"
      @submitForm="save(1)" @saveAndSubmitApprove="save(2)" />
  ```
  `footerMenu` computed trả object cờ bật nút, vd `{ submit_form: true, save_and_submit_approve: true }`
  (dòng 691-694) — map sang event tương ứng: `menu.submit_form` → nút "Lưu" → emit `submitForm`;
  `menu.save_and_submit_approve` → nút "Lưu và gửi duyệt" (tự hỏi xác nhận trước khi emit, xem
  `components/V2Footer.vue` dòng ~26). PYCXBHM cần tối thiểu 2 nút: Lưu nháp (status=3, tra theo
  bảng `STATUS_OPTIONS` ở `index.vue`: 3=Đang tạo) + Gửi duyệt (status=2, Chờ duyệt) →
  `menu: { submit_and_draft: true, save_and_submit_approve: true }` là combo đúng nghĩa nhất trong
  `V2Footer.vue` (xem props `menu.submit_and_draft` dòng 8, `menu.save_and_submit_approve` dòng 25).
- **fail-closed permission**: `borrow-sell-requests/index.vue` đã đúng chuẩn — mọi nút hành động
  đọc thẳng cờ `is_can_*` từ BE (`item.is_can_view`, `item.is_can_edit`, …), KHÔNG hard-code `true`
  (dòng 359-401). Trang `create.vue` mới không cần cờ quyền cấp dòng (đang tạo mới, chưa có entity),
  nhưng NẾU cần ẩn/hiện action theo quyền tạo phiếu (vd chỉ nhân viên phòng KD mới tạo được) thì
  phải lấy từ `$store.state.permissions`, không tự đặt `true`.

---

## 6. Route/menu — nút "Tạo phiếu" đã có sẵn ở index.vue

`pages/finance/borrow-sell-requests/index.vue`:
- Nút "Tạo phiếu" (dòng 35-40, slot `#actions-bottom` của `V2BaseDataTable`):
  ```html
  <V2BaseButton primary size="sm" class="btn-compact" @click="createItem">
      <template #prefix><i class="ri-add-line" style="font-size: 13px"></i></template>
      Tạo phiếu
  </V2BaseButton>
  ```
- Handler (dòng 538-540):
  ```js
  createItem() {
      this.$router.push('/finance/borrow-sell-requests/create')
  }
  ```
  → xác nhận route đích đúng là `/finance/borrow-sell-requests/create`, khớp path file cần tạo.
  Không truyền query param nào — khác với `bill-incomes` (dùng `?bill_income_request_id=` khi
  điều hướng từ màn chi tiết đề nghị). Nếu PYCXBHM cũng cần luồng "tạo từ hợp đồng có sẵn" (từ màn
  chi tiết hợp đồng bấm "Tạo phiếu xuất bán mượn") thì cần bổ sung xử lý `this.$route.query.contract_id`
  tương tự `warehouse-export-requests/create.vue` dòng 244-249 (đọc `$route.query.request_id`, nếu
  thiếu thì toast lỗi + redirect) — hỏi lại spec Task 11 xem có luồng này không trước khi code.

---

## Danh sách file tham chiếu (đường dẫn tuyệt đối)

- `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client/pages/finance/product-export-requests/create.vue`
- `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client/pages/finance/product-export-requests/components/ContractSearchModal.vue`
- `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client/pages/finance/product-export-requests/components/ProductExportRequestForm.vue` (dòng 260-460, 500-620, 574-820)
- `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client/pages/finance/warehouse-export-requests/create.vue` (toàn văn, 666 dòng — khuôn đơn giản hơn cho phần style + qty-valid)
- `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client/pages/finance/bill-incomes/components/BillIncomeForm.vue` (dòng 440-720, 1180-1220 — khuôn validate/footer/unsaved chuẩn CLAUDE.md)
- `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client/pages/finance/bill-incomes/components/IncomeRequestSearchModal.vue` (toàn văn — khuôn picker biến thể `b-modal` + `V2BasePagination`)
- `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client/pages/finance/borrow-sell-requests/api.js` (toàn văn, 53 dòng)
- `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client/pages/finance/borrow-sell-requests/index.vue` (dòng 34-50, 538-540)
- `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client/utils/mixins/formValidateMixin.js`
- `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client/components/V2Footer.vue` (dòng 1-60)
- `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.claude/skills/form-validate/SKILL.md`
- `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/.claude/skills/unsaved-changes/SKILL.md`
