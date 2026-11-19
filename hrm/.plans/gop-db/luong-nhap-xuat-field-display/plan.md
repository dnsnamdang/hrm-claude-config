# Chuẩn hóa hiển thị trường — 8 màn luồng nhập/xuất HRM — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Chuẩn hóa hiển thị trường trong khối THÔNG TIN CHUNG của 8 màn luồng nhập/xuất ở cả 3 chế độ (Tạo/Sửa/Chi tiết): (a) "Xuất/Nhập thẳng" luôn là checkbox; (b) bỏ "Trạng thái" khỏi thông tin chung ở màn chi tiết; (c) ẩn trường khi-và-chỉ-khi vừa-không-liên-quan vừa-rỗng.

**Architecture:** Một helper thuần (`utils/flow-field-visibility.js`) đóng gói quy tắc `showField = isRelevant(ctx) || !isEmpty(value)`, cộng với một file `field-relevance.js` khai ma trận predicate cho mỗi màn. Component thêm 2 computed (`fieldCtx`, `showField`) và bọc `v-if="showField('key')"` lên các trường biến thiên. Không đụng payload lưu, không đụng hạch toán, không đụng layout card.

**Tech Stack:** Nuxt 2.14 / Vue 2 (hrm-client), Bootstrap-Vue 2.15, component dùng chung `V2Base*`. Không có test runner trong hrm-client → logic thuần (helper + field-relevance) kiểm bằng script `node` assertion (`.mjs`, `node:assert`, Node 20); wiring component kiểm bằng Playwright MCP.

**Spec:** `HRM/docs/superpowers/specs/gop-db/2026-10-12-luong-nhap-xuat-field-display-design.md` (đã duyệt). Tóm tắt: `HRM/.plans/gop-db/luong-nhap-xuat-field-display/design.md`. Đọc spec song song với plan — plan lập luận từ spec, mâu thuẫn giải quyết theo spec.

## Global Constraints

- Nhánh git: `gop_db`. Repo FE: `hrm-client/`. Repo BE: `hrm-api/`. Mọi thao tác trong `HRM/`.
- **gộp DB (gop_db): KHÔNG dùng `mysql2` / `DB_CONNECTION_SECOND`.** Tất cả 1 DB chung.
- **KHÔNG commit/push khi chưa có yêu cầu của user.** Mỗi task có bước commit nhưng ĐÁNH DẤU HOÃN — chỉ chạy `git commit` khi user cho phép. Message format cuối file.
- **KHÔNG tự sửa hàm dùng chung** (`V2BaseCheckbox`, `V2BaseBadge`, `buildStatusTitle`, store actions...) — chỉ *dùng*. Nếu cần sửa → dừng, hỏi user.
- Mọi element form dùng `V2Base*` (màn/khối đang chuẩn hóa).
- `V2BaseCheckbox` single-mode: truyền nhãn qua **prop `label`**, KHÔNG dùng default slot (slot làm `singleMode=false` → render rỗng 0x0).
- Badge trạng thái: màu do BE trả (`status_color`), FE chỉ hiển thị.
- SKILL thắng SPEC về hình thức UI (checkbox/badge/card theo `.claude/skills/`).
- Test chạy Node 20: `source ~/.nvm/nvm.sh; nvm use 20`. File test `.mjs` đặt ở `/Users/nguyentrancu/.claude/jobs/c518e480/tmp`. File nguồn (`utils/*.js`, `field-relevance.js`) viết dạng ESM (`export`).
- Playwright: `http://127.0.0.1:3000` (KHÔNG `localhost`), chạy e2e bằng Node 20. Hoàn trả data nếu chỉnh tạm khi test.
- Verify FE bằng Playwright TRƯỚC khi báo xong.

## Review Focus

Các input/điều kiện spec hàm ý nhưng dễ vỡ, cần kiểm riêng (xếp theo khả năng cắn người dùng):

1. **Số type HRM lệch số type trong ma trận ERP** — ma trận §5 dùng số type của ERP; một số màn HRM (nhất là ĐNXK, ĐNNK) đánh số type khác. Nếu copy nguyên list số từ ma trận mà không đối chiếu hằng type thật của màn → ẩn/hiện SAI loại. → Mỗi task màn có bước "reconcile hằng type", test predicate dùng ĐÚNG số type HRM. (Pinned: Task 3–10 bước 1.)
2. **`HAS_DELIVERY` của YCXH** — spec §5.1/D4 để mở (ERP `getHasDeliveryTypes` vs HRM `DELIVERY_TYPES` hiện tại). **Ruling plan: GIỮ `DELIVERY_TYPES` hiện tại của HRM** (D3/D4 cấm đổi list type/hành vi). Cần user xác nhận ở plan-review; nếu user muốn theo ERP, chỉ đổi 1 hằng. (Pinned: Task 3.)
3. **Trường ẩn mà còn `v-model` (tạo/sửa đổi loại)** — ẩn khỏi UI nhưng GIỮ giá trị trong `form` (edge case §8.3), KHÔNG tự clear. Test reactivity phải khẳng định số liệu đã nhập không mất khi đổi loại. (Pinned: Task 11 bước reactivity.)
4. **`is_export_direct` dạng số vs boolean** — BE trả `0/1` (number) hoặc `"0"/"1"` (string); checkbox `:value` cần boolean. Luôn `Number(x) === 1`. `isEmptyValue(0) === false` nên cờ=0 KHÔNG bị coi rỗng. (Pinned: Task 1 test + Task 3/4/6/8 checkbox.)
5. **Màn chi tiết CHƯA có `buildStatusTitle`** — (b) chỉ được xóa "Trạng thái" khi header đã có badge. 8 màn đã xác nhận có (extraction). Nếu task nào phát hiện thiếu → bổ sung `buildStatusTitle` TRƯỚC khi xóa, không để phiếu mất trạng thái. (Pinned: mỗi task màn, bước (b).)

---

## File Structure

**Tạo mới (FE):**
- `hrm-client/utils/flow-field-visibility.js` — helper thuần dùng chung (Task 1).
- `hrm-client/pages/finance/product-export-requests/field-relevance.js` — YCXH (Task 3).
- `hrm-client/pages/finance/product-exports/field-relevance.js` — PXH (Task 4).
- `hrm-client/pages/finance/warehouse-export-requests/field-relevance.js` — ĐNXK (Task 5).
- `hrm-client/pages/finance/product-import-requests/field-relevance.js` — YCNH (Task 6).
- `hrm-client/pages/finance/warehouse-import-requests/field-relevance.js` — ĐNNK (Task 7).
- `hrm-client/pages/finance/product-imports/field-relevance.js` — PNK (Task 8).
- `hrm-client/pages/finance/borrow-sell-requests/field-relevance.js` — YCXBHM (Task 9).
- `hrm-client/pages/finance/borrow-sells/field-relevance.js` — PXBHM (Task 10).

**Sửa (FE):** các component/màn liệt kê trong từng task (spec §7.1).

**BE (`hrm-api`):** chỉ bổ sung field vào Resource chi tiết NẾU thiếu (Task 2) — không đổi logic nghiệp vụ.

**Trách nhiệm từng file:** `flow-field-visibility.js` chứa toàn bộ quy tắc ẩn/hiện (1 nơi). Mỗi `field-relevance.js` chỉ khai dữ liệu (ma trận predicate + hằng type của màn) — thuần, không import Vue, test được độc lập. Component chỉ ráp 2 computed + bọc `v-if`.

---

## Task 1: Helper `flow-field-visibility.js`

**Files:**
- Create: `hrm-client/utils/flow-field-visibility.js`
- Test: `/Users/nguyentrancu/.claude/jobs/c518e480/tmp/test-flow-field-visibility.mjs`

**Interfaces:**
- Produces:
  - `isEmptyValue(value): boolean` — null/undefined/''/chuỗi-trim-rỗng/[]/{} → true; số 0 và false → false.
  - `shouldShowField(isRelevant, value): boolean` = `!!isRelevant || !isEmptyValue(value)`.
  - `makeFieldVisibility(relevanceMap, getValue, getCtx): (key) => boolean` — `rule===true`→relevant; `typeof rule==='function'`→`rule(ctx)`; `rule===undefined`→`true` (không gate).

- [ ] **Step 1: Viết test thất bại** — `/Users/nguyentrancu/.claude/jobs/c518e480/tmp/test-flow-field-visibility.mjs`

```js
import assert from 'node:assert/strict'
import { isEmptyValue, shouldShowField, makeFieldVisibility } from '/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client/utils/flow-field-visibility.js'

// isEmptyValue
assert.equal(isEmptyValue(null), true)
assert.equal(isEmptyValue(undefined), true)
assert.equal(isEmptyValue(''), true)
assert.equal(isEmptyValue('   '), true)
assert.equal(isEmptyValue([]), true)
assert.equal(isEmptyValue({}), true)
assert.equal(isEmptyValue(0), false, '0 KHÔNG rỗng')
assert.equal(isEmptyValue(false), false, 'false KHÔNG rỗng')
assert.equal(isEmptyValue('x'), false)
assert.equal(isEmptyValue([1]), false)
assert.equal(isEmptyValue({ a: 1 }), false)

// shouldShowField
assert.equal(shouldShowField(true, ''), true, 'liên quan + rỗng → hiện')
assert.equal(shouldShowField(false, 'abc'), true, 'không liên quan + có data → hiện')
assert.equal(shouldShowField(false, ''), false, 'không liên quan + rỗng → ẩn')
assert.equal(shouldShowField(false, 0), true, '0 không rỗng → hiện')

// makeFieldVisibility
const ctx = { type: 14, isDirect: false }
const values = { a: '', b: '', c: 'data', d: '' }
const show = makeFieldVisibility(
  {
    a: true,                       // luôn liên quan
    b: (c) => c.type === 99,       // không khớp (type=14) → không liên quan
    c: (c) => c.type === 99,       // không liên quan nhưng có data
    // d không khai → undefined
  },
  (k) => values[k],
  () => ctx
)
assert.equal(show('a'), true, 'rule===true + rỗng → hiện')
assert.equal(show('b'), false, 'predicate false + rỗng → ẩn')
assert.equal(show('c'), true, 'predicate false + có data → hiện')
assert.equal(show('d'), true, 'không khai → luôn hiện')

console.log('OK test-flow-field-visibility')
```

- [ ] **Step 2: Chạy test để thấy FAIL**

Run: `source ~/.nvm/nvm.sh; nvm use 20; node /Users/nguyentrancu/.claude/jobs/c518e480/tmp/test-flow-field-visibility.mjs`
Expected: FAIL — `Cannot find module .../utils/flow-field-visibility.js`.

- [ ] **Step 3: Viết helper (ESM)** — `hrm-client/utils/flow-field-visibility.js`

```js
// utils/flow-field-visibility.js
// Hiển thị trường cho 8 màn luồng nhập/xuất (YCXH, ĐNXK, PXH, YCNH, ĐNNK, PNK, YCXBHM, PXBHM).
// Quy tắc (yêu cầu c): ẩn CHỈ KHI vừa-không-liên-quan vừa-rỗng.

/**
 * Giá trị coi là "rỗng" cho mục đích ẩn trường.
 * KHÔNG coi số 0 / false là rỗng — 0 có thể là giá trị nghiệp vụ hợp lệ.
 */
export function isEmptyValue(value) {
  if (value === null || value === undefined) return true
  if (typeof value === 'string') return value.trim() === ''
  if (Array.isArray(value)) return value.length === 0
  if (typeof value === 'object') return Object.keys(value).length === 0
  return false
}

/**
 * Quy tắc hiển thị: hiện khi liên-quan HOẶC có dữ liệu.
 */
export function shouldShowField(isRelevant, value) {
  return !!isRelevant || !isEmptyValue(value)
}

/**
 * Dựng hàm showField(key) cho 1 màn.
 * @param {Object}   relevanceMap { [fieldKey]: (ctx) => boolean | boolean }  // true = luôn liên quan
 * @param {Function} getValue     (fieldKey) => giá trị hiện tại (form[key] khi tạo/sửa, detail[key] khi xem)
 * @param {Function} getCtx       () => { type, isDirect, transitionType, customerType, isSettlement, ... }
 * @returns {Function} showField(key): boolean
 */
export function makeFieldVisibility(relevanceMap, getValue, getCtx) {
  return function showField(key) {
    const rule = relevanceMap[key]
    if (rule === undefined) return true // không khai => trường luôn hiện
    let isRelevant = false
    if (rule === true) isRelevant = true
    else if (typeof rule === 'function') isRelevant = !!rule(getCtx())
    return shouldShowField(isRelevant, getValue(key))
  }
}
```

- [ ] **Step 4: Chạy test để thấy PASS**

Run: `source ~/.nvm/nvm.sh; nvm use 20; node /Users/nguyentrancu/.claude/jobs/c518e480/tmp/test-flow-field-visibility.mjs`
Expected: `OK test-flow-field-visibility` (có thể kèm warning `MODULE_TYPELESS_PACKAGE_JSON` — vô hại).

- [ ] **Step 5: Commit (HOÃN — chỉ chạy khi user cho phép)**

```bash
git -C hrm-client add utils/flow-field-visibility.js
git -C hrm-client commit -m "feat(flow): them helper flow-field-visibility (showField = isRelevant || !isEmpty)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 2: BE — audit Resource chi tiết trả đủ field cho `fieldCtx`

**Files:**
- Đọc (audit): các Resource/Service build response chi tiết của 8 màn trong `hrm-api/Modules/.../`.
- Modify (chỉ nếu thiếu): Resource tương ứng — thêm field vào mảng trả về, KHÔNG đổi logic.

**Interfaces:**
- Produces (đảm bảo mỗi response chi tiết CÓ, cho các màn áp dụng): `type` (hoặc `import_type`), `is_export_direct`/`is_import_direct`, `customer_type`, `transition_type`, `is_settlement`, `status_name`, `status_color`. Màn nào không có khái niệm nào thì bỏ qua field đó (ví dụ ĐNNK không có `is_*_direct`).

> Đây là task AUDIT: phần lớn field đã có (các màn đang hiển thị chúng). Chỉ thêm field thực sự thiếu. Nếu audit cho thấy đủ → task là no-op (vẫn ghi ledger "đã kiểm, đủ").

- [ ] **Step 1: Grep field trong response build của từng màn**

Run (ví dụ YCXH):
```bash
grep -rn "is_export_direct\|customer_type\|transition_type\|is_settlement\|status_color" hrm-api/Modules/*/Transformers hrm-api/Modules/*/Resources hrm-api/Modules/*/Services 2>/dev/null | grep -i "export\|import\|borrow"
```
Expected: liệt kê nơi các field được set. Ghi lại màn nào thiếu field nào.

- [ ] **Step 2: Với field THIẾU — thêm vào Resource**

Chỉ khi grep cho thấy field vắng mặt trong response của màn cụ thể. Pattern (minh họa, thay đúng model/field của màn):

```php
// trong toArray()/transform() của Resource chi tiết
'customer_type'   => $this->customer_type,
'transition_type' => $this->transition_type,
```

Nếu không màn nào thiếu → bỏ qua Step 2–4, ghi ledger và sang Task 3.

- [ ] **Step 3: Verify response thực tế**

Run (thay id thật, token thật qua trình duyệt Playwright hoặc tinker):
```bash
grep -c "fieldCtx cần: type/is_*_direct/customer_type/transition_type/is_settlement" /dev/null # placeholder audit note
```
Thực tế: mở 1 phiếu mỗi màn trên FE bằng Playwright, xem Network response chi tiết có đủ field (làm chung trong Task 11). Ở task này chỉ cần khẳng định bằng đọc code Resource.

- [ ] **Step 4: Commit (HOÃN)** — chỉ nếu có sửa BE

```bash
git -C hrm-api add Modules/
git -C hrm-api commit -m "feat(flow): resource chi tiet tra du field cho field-visibility (type/customer_type/transition_type/is_settlement)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 3: YCXH — `product-export-requests`

**Files:**
- Create: `hrm-client/pages/finance/product-export-requests/field-relevance.js`
- Modify: `hrm-client/pages/finance/product-export-requests/components/ProductExportRequestForm.vue` (1 component, 3 chế độ qua prop `readonly`)
- Test: `/Users/nguyentrancu/.claude/jobs/c518e480/tmp/test-fr-ycxh.mjs`

**Interfaces:**
- Consumes: `makeFieldVisibility` (Task 1).
- Produces: `fieldRelevance` (YCXH), `HAS_DELIVERY` (YCXH). ctx = `{ type, isDirect, transitionType, customerType }`.

Hằng HRM hiện có trong component (dòng 992-1004, để reconcile): `CONTRACT_TYPES=[20,21]`, `FIRM_CONTRACT_TYPES=[14]`, `EMPLEMENT_CONTRACT_TYPES=[19]`, `MANUAL_TYPES=[3,6,12,18,19,99]`, `BRANCH_TRANSFER_TYPE=7`, `DELIVERY_TYPES=[3,6,7,12,18,19,99,20,21,14]`. Computeds hiện có: `showExportDirect` (1179: `type != null && ![3,15].includes(type)`), `detailIsContract` (1321: `[20,21].includes(detail.type)`), `detailIsSale` (1325), `needWarehouse` (1227), `needTransition` (1242), `needCustomer` (1246: `===12`).

- [ ] **Step 1: Reconcile hằng type + viết test thất bại** — `test-fr-ycxh.mjs`

Xác nhận số type trên bám đúng component (đã trích). `HAS_DELIVERY` = **giữ `DELIVERY_TYPES` hiện tại** `[3,6,7,12,18,19,99,20,21,14]` (Review Focus #2).

```js
import assert from 'node:assert/strict'
import { fieldRelevance as FR, HAS_DELIVERY } from '/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client/pages/finance/product-export-requests/field-relevance.js'

const C = (o) => ({ type: 0, isDirect: false, transitionType: 0, customerType: 1, ...o })

// (a) is_export_direct: ẩn ở 3 (mượn) và 15 (KM hãng)
assert.equal(FR.is_export_direct(C({ type: 14 })), true)
assert.equal(FR.is_export_direct(C({ type: 3 })), false)
assert.equal(FR.is_export_direct(C({ type: 15 })), false)

// cụm KH chỉ-đọc: [14,15,16,17] (+20/21 D1)
assert.equal(FR.customer_tax_code(C({ type: 14 })), true)
assert.equal(FR.customer_tax_code(C({ type: 20 })), true)
assert.equal(FR.customer_tax_code(C({ type: 12 })), false)

// contact chỉ KH doanh nghiệp (ct>1)
assert.equal(FR.customer_contact_name(C({ type: 14, customerType: 2 })), true)
assert.equal(FR.customer_contact_name(C({ type: 14, customerType: 1 })), false)

// customer_name: cụm + 12 (picker) + 19 (từ HĐ)
assert.equal(FR.customer_name(C({ type: 12 })), true)
assert.equal(FR.customer_name(C({ type: 19 })), true)
assert.equal(FR.customer_name(C({ type: 6 })), false)

// Kho xuất: != 7 và không thẳng
assert.equal(FR.warehouse_name(C({ type: 14, isDirect: false })), true)
assert.equal(FR.warehouse_name(C({ type: 14, isDirect: true })), false)
assert.equal(FR.warehouse_name(C({ type: 7 })), false)

// Vận chuyển: 18 luôn hiện kể cả thẳng; còn lại HAS_DELIVERY && !direct
assert.equal(FR.transition_type_name(C({ type: 18, isDirect: true })), true)
assert.equal(FR.transition_type_name(C({ type: 12, isDirect: false })), true)
assert.equal(FR.transition_type_name(C({ type: 12, isDirect: true })), false)
assert.equal(FR.transition_type_name(C({ type: 4, isDirect: false })), false, '4 không trong DELIVERY_TYPES HRM')

// Số km: chỉ khi Vận chuyển = Công ty vận chuyển (tt===2)
assert.equal(FR.total_km_expected(C({ type: 18, transitionType: 2 })), true)
assert.equal(FR.total_km_expected(C({ type: 18, transitionType: 1 })), false)
assert.equal(FR.total_km_expected(C({ type: 12, transitionType: 2, isDirect: false })), true)
assert.equal(FR.total_km_expected(C({ type: 12, transitionType: 2, isDirect: true })), false)

assert.deepEqual(HAS_DELIVERY, [3, 6, 7, 12, 18, 19, 99, 20, 21, 14])
console.log('OK test-fr-ycxh')
```

- [ ] **Step 2: Chạy test → FAIL** (module chưa tồn tại). Run: `source ~/.nvm/nvm.sh; nvm use 20; node /Users/nguyentrancu/.claude/jobs/c518e480/tmp/test-fr-ycxh.mjs`

- [ ] **Step 3: Viết `field-relevance.js`**

```js
// pages/finance/product-export-requests/field-relevance.js — YCXH
// Ma trận ERP spec §5.1. ctx = { type, isDirect, transitionType, customerType }.
// HAS_DELIVERY: GIỮ DELIVERY_TYPES hiện tại của HRM (D3/D4 — chờ user xác nhận ở plan-review).
export const HAS_DELIVERY = [3, 6, 7, 12, 18, 19, 99, 20, 21, 14]

const CONTRACT_CUSTOMER = [14, 15, 16, 17, 20, 21] // cụm KH chỉ-đọc (+20/21 theo D1)

export const fieldRelevance = {
  is_export_direct: (c) => c.type !== 3 && c.type !== 15,
  customer_name: (c) => CONTRACT_CUSTOMER.includes(c.type) || c.type === 12 || c.type === 19,
  customer_tax_code: (c) => CONTRACT_CUSTOMER.includes(c.type),
  customer_address: (c) => CONTRACT_CUSTOMER.includes(c.type) || c.type === 19,
  customer_contact_name: (c) => CONTRACT_CUSTOMER.includes(c.type) && c.customerType > 1,
  customer_contact_phone: (c) => CONTRACT_CUSTOMER.includes(c.type) && c.customerType > 1,
  warehouse_name: (c) => c.type !== 7 && !c.isDirect,
  transition_type_name: (c) => (c.type === 18 ? true : HAS_DELIVERY.includes(c.type) && !c.isDirect),
  total_km_expected: (c) =>
    c.type === 18 ? c.transitionType === 2 : HAS_DELIVERY.includes(c.type) && c.transitionType === 2 && !c.isDirect,
}
```

- [ ] **Step 4: Chạy test → PASS.**

- [ ] **Step 5: Ráp component** — `ProductExportRequestForm.vue`

Thêm import + 2 computed (đặt cạnh computed hiện có):

```js
import { makeFieldVisibility } from '@/utils/flow-field-visibility'
import { fieldRelevance } from '../field-relevance'
// ...
fieldCtx() {
  const src = this.readonly ? this.detail : this.form
  return {
    type: Number(src.type),
    isDirect: Number(src.is_export_direct) === 1,
    transitionType: Number(src.transition_type),
    customerType: Number(src.customer_type),
  }
},
showField() {
  const src = this.readonly ? this.detail : this.form
  return makeFieldVisibility(fieldRelevance, (k) => src[k], () => this.fieldCtx)
},
```

**(a) Chi tiết — đổi "Xuất thẳng" text→checkbox** (dòng 739-742):

```html
<!-- TRƯỚC -->
<V2BaseLabel>Xuất thẳng</V2BaseLabel>
<V2BaseInput :value="detail.is_export_direct ? 'Có' : 'Không'" disabled size="sm" />
<!-- SAU -->
<V2BaseCheckbox :value="Number(detail.is_export_direct) === 1" disabled label="Xuất thẳng" />
```
Bọc ô này `v-if="showField('is_export_direct')"`.

**(a) Tạo/sửa** — đổi gate checkbox raw (dòng 232-244) từ `v-if="showExportDirect"` → `v-if="showField('is_export_direct')"`. GIỮ nguyên checkbox raw + handler `onExportDirectChange` (1486-1490). KHÔNG đụng "Cần lắp đặt" (743-746).

**(b) Chi tiết — XÓA "Trạng thái"** (dòng 675-680) — header đã có `buildStatusTitle` (xác nhận `_id/index.vue:28,52-54`):

```html
<!-- XÓA -->
<V2BaseLabel>Trạng thái</V2BaseLabel>
<V2BaseBadge v-if="detail.status_name" :color="detail.status_color">...</V2BaseBadge>
```

**(c) Chi tiết — thay `v-if="detailIsContract"` / `need_*` bằng `showField`:**
- MST `customer_tax_code` (703-706): `v-if="showField('customer_tax_code')"`.
- Người liên hệ `customer_contact_name` (707-710): `v-if="showField('customer_contact_name')"`.
- SĐT `customer_contact_phone` (711-714): `v-if="showField('customer_contact_phone')"`.
- Địa chỉ `customer_address` (715-718): `v-if="showField('customer_address')"`.
- Khách hàng `customer_name` (699-702): `v-if="showField('customer_name')"`.
- Kho xuất `warehouse_name` (735-738): `v-if="showField('warehouse_name')"` (thay `!detailIsContract && detail.need_warehouse`).
- Vận chuyển `transition_type_name` (747-750): `v-if="showField('transition_type_name')"`.
- Số km `total_km_expected` (751-761): `v-if="showField('total_km_expected')"`.

> Ruling scope (c) YCXH: áp `showField` cho khối CHI TIẾT + cờ `is_export_direct` (3 chế độ). Các field tạo/sửa khác giữ computed hiện có (`needWarehouse`/`needTransition`/`needCustomer`/`firm`/`emplement` — đã khớp ma trận; D4 cấm đổi hành vi). Nếu user muốn mở rộng `showField` sang toàn bộ field tạo/sửa → flag ở plan-review (một task bổ sung).

- [ ] **Step 6: Build check FE**

Run: `cd hrm-client && node -e "require('@vue/compiler-sfc')" 2>/dev/null; echo "lint sẽ chạy ở Task 11 qua dev server"` — thực tế xác nhận cú pháp bằng mở màn trên Playwright (Task 11). Ở task này: đọc lại diff, đảm bảo không còn `detailIsContract` mồ côi.

- [ ] **Step 7: Commit (HOÃN)**

```bash
git -C hrm-client add pages/finance/product-export-requests/
git -C hrm-client commit -m "feat(ycxh): checkbox xuat thang + bo trang thai + showField theo loai

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 4: PXH — `product-exports`

**Files:**
- Create: `hrm-client/pages/finance/product-exports/field-relevance.js`
- Modify: `hrm-client/pages/finance/product-exports/create.vue`, `hrm-client/pages/finance/product-exports/_id/index.vue`
- Test: `/Users/nguyentrancu/.claude/jobs/c518e480/tmp/test-fr-pxh.mjs`

**Interfaces:**
- Produces: `fieldRelevance` (PXH). ctx = `{ type, isDirect, transitionType }`.

Hằng HRM: `hasCustomer=[1,2,8,12,14,16,17]` (create 704), `hasContract=[1,2,8,11,13,14,16,17]` (731), `hasDelivery` (734: `transition_type===2`). "Loại xuất" `exportType===18||19` (49-52). Ngày hạch toán `[9,10,18,19]` (76-79).

- [ ] **Step 1: Viết test thất bại** — `test-fr-pxh.mjs`

```js
import assert from 'node:assert/strict'
import { fieldRelevance as FR } from '/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client/pages/finance/product-exports/field-relevance.js'
const C = (o) => ({ type: 0, isDirect: false, transitionType: 0, ...o })

assert.equal(FR.is_export_direct, true, 'luôn hiện → áp (a)')
assert.equal(FR.export_type_name(C({ type: 18 })), true)
assert.equal(FR.export_type_name(C({ type: 1 })), false)
assert.equal(FR.code(C({ isDirect: false })), true)
assert.equal(FR.code(C({ isDirect: true })), false)
assert.equal(FR.warehouse_name(C({ isDirect: true })), false)
assert.equal(FR.accounting_date(C({ type: 9 })), true)
assert.equal(FR.accounting_date(C({ type: 1 })), false)
assert.equal(FR.emplement_contract_code(C({ type: 19 })), true)
assert.equal(FR.account_has(C({ type: 18 })), true)
assert.equal(FR.account_has(C({ type: 9 })), false)
assert.equal(FR.cost_debt_id(C({ type: 19 })), true)
assert.equal(FR.contract_code(C({ type: 11 })), true)
assert.equal(FR.contract_code(C({ type: 12 })), false)
assert.equal(FR.customer_name(C({ type: 12 })), true)
assert.equal(FR.customer_name(C({ type: 11 })), false)
// cụm KH "thừa" của HRM → () => false (chỉ hiện khi có data)
assert.equal(FR.customer_mobile(C({ type: 1 })), false)
assert.equal(FR.customer_contact_name(C({ type: 1 })), false)
assert.equal(FR.customer_address(C({ type: 1 })), false)
assert.equal(FR.delivery_place(C({ type: 1 })), false)
console.log('OK test-fr-pxh')
```

- [ ] **Step 2: Chạy → FAIL.**

- [ ] **Step 3: Viết `field-relevance.js`**

```js
// pages/finance/product-exports/field-relevance.js — PXH. Spec §5.2. ctx = { type, isDirect, transitionType }.
const HAS_CUSTOMER = [1, 2, 8, 12, 14, 16, 17]
const HAS_CONTRACT = [1, 2, 8, 11, 13, 14, 16, 17]
const ACCOUNTING = [9, 10, 18, 19]

export const fieldRelevance = {
  is_export_direct: true,
  export_type_name: (c) => c.type === 18 || c.type === 19,
  code: (c) => !c.isDirect,
  stocker_name: (c) => !c.isDirect,
  warehouse_name: (c) => !c.isDirect,
  receiver_name: (c) => !c.isDirect,
  accounting_date: (c) => ACCOUNTING.includes(c.type),
  emplement_contract_code: (c) => c.type === 19,
  account_debt: (c) => ACCOUNTING.includes(c.type),
  account_has: (c) => c.type === 18,
  cost_debt_id: (c) => c.type === 18 || c.type === 19,
  work: (c) => ACCOUNTING.includes(c.type),
  branch_transfer_coefficient: (c) => c.type === 7,
  contract_code: (c) => HAS_CONTRACT.includes(c.type),
  customer_name: (c) => HAS_CUSTOMER.includes(c.type),
  // cụm KH "thừa" của HRM (ERP PXH không có) → chỉ hiện khi có dữ liệu
  customer_mobile: () => false,
  customer_contact_name: () => false,
  customer_address: () => false,
  delivery_place: () => false,
}
```

- [ ] **Step 4: Chạy → PASS.**

- [ ] **Step 5: Ráp `_id/index.vue` (chi tiết)**

Import + computed (readonly thuần — chi tiết; ctx đọc `detail.*`):
```js
import { makeFieldVisibility } from '@/utils/flow-field-visibility'
import { fieldRelevance } from '../field-relevance'
// ...
fieldCtx() {
  return { type: Number(this.detail.type), isDirect: Number(this.detail.is_export_direct) === 1, transitionType: Number(this.detail.transition_type) }
},
showField() { return makeFieldVisibility(fieldRelevance, (k) => this.detail[k], () => this.fieldCtx) },
```
- **(a) THÊM "Xuất thẳng" checkbox** (PXH chi tiết hiện KHÔNG có field này) — chèn vào khối thông tin chung, gate `v-if="showField('is_export_direct')"`:
```html
<div v-if="showField('is_export_direct')" class="col-md-4 mb-2">
  <V2BaseCheckbox :value="Number(detail.is_export_direct) === 1" disabled label="Xuất thẳng" />
</div>
```
- **(b) XÓA "Trạng thái"** (24-29) — header có `buildStatusTitle` (443,466).
- **(c)** bọc `showField`: cụm KH block (85-107) → từng field `customer_name`/`customer_mobile`/`customer_contact_name`/`customer_address`/`delivery_place`; `accounting_date` (82-84); TK nợ/Mã phí/Vụ việc trong tab Vận chuyển (221-232) → `account_debt`/`cost_debt_id`/`work`.

- [ ] **Step 6: Ráp `create.vue`**

Import + computed tương tự (ctx đọc `info.*`/form; readonly form). "Loại xuất" text (49-52) → `v-if="showField('export_type_name')"`. "Xuất thẳng" text (68-71) → đổi sang checkbox read-only + gate `showField('is_export_direct')`:
```html
<V2BaseCheckbox :value="Number(info.is_export_direct) === 1" disabled label="Xuất thẳng" />
```
Customer block (141-160) `v-if="hasCustomer"` → từng field `showField(...)`; Contract block (121-136) `v-if="hasContract"` → `showField('contract_code')`; Ngày hạch toán (76-79) → `showField('accounting_date')`.

> Ruling: PXH create là READ-ONLY (nạp từ phiếu đã duyệt). ctx đọc field nguồn `info.*`; nếu `info` không có `transition_type`/`is_export_direct` thì checkbox hiển thị theo giá trị thực; không cần clear.

- [ ] **Step 7: Commit (HOÃN)**
```bash
git -C hrm-client add pages/finance/product-exports/
git -C hrm-client commit -m "feat(pxh): them checkbox xuat thang (chi tiet) + bo trang thai + showField

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 5: ĐNXK — `warehouse-export-requests` (thống nhất 3 màn)

**Files:**
- Create: `hrm-client/pages/finance/warehouse-export-requests/field-relevance.js`
- Modify: `create.vue`, `_id/edit.vue`, `_id/index.vue`
- Test: `/Users/nguyentrancu/.claude/jobs/c518e480/tmp/test-fr-dnxk.mjs`

**Interfaces:**
- Produces: `fieldRelevance` (ĐNXK). ctx = `{ type, customerType }`.

Hằng HRM hiện có: `hasCustomer=[12,20,21]`, `showBearShipping=![18,19]`. **Bất đồng bộ cần sửa:** `edit.vue` hiện customer block (44-63) + bear_the_shipping (41-43) VÔ ĐIỀU KIỆN, không có computed → thống nhất dùng chung `fieldRelevance`.

- [ ] **Step 1: Reconcile hằng type (Review Focus #1)**

ĐỌC `create.vue`/`index.vue` xác nhận giá trị `type` thật của ĐNXK HRM (hiện `hasCustomer=[12,20,21]`). Ma trận §5.4 dùng số ERP A=[1,2,8,14]. **Phải xác nhận ĐNXK HRM có dùng các type 1/2/8/14/19/12 không** — nếu HRM chỉ có [12,20,21] (+ loại khác), danh sách predicate chỉ giữ các type HRM thực sự phát sinh; thêm 1/2/8/14/19 CHỈ khi HRM có các loại đó. Ghi kết luận vào ledger trước khi viết predicate. Test dưới dùng tập type đã reconcile (ví dụ minh họa theo ma trận ERP — thay bằng tập HRM thực tế nếu khác).

- [ ] **Step 2: Viết test thất bại** — `test-fr-dnxk.mjs`

```js
import assert from 'node:assert/strict'
import { fieldRelevance as FR } from '/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client/pages/finance/warehouse-export-requests/field-relevance.js'
const C = (o) => ({ type: 0, customerType: 1, ...o })

assert.equal(FR.emplement_contract_code(C({ type: 14 })), true)
assert.equal(FR.emplement_contract_code(C({ type: 19 })), true)
assert.equal(FR.emplement_contract_code(C({ type: 18 })), false)
assert.equal(FR.customer_code(C({ type: 14 })), true)
assert.equal(FR.customer_code(C({ type: 19 })), false, '19 chỉ có tên')
assert.equal(FR.customer_name(C({ type: 19 })), true)
assert.equal(FR.customer_name(C({ type: 12 })), true)
assert.equal(FR.customer_name(C({ type: 18 })), false)
assert.equal(FR.customer_contact_name(C({ type: 14, customerType: 2 })), true)
assert.equal(FR.customer_contact_name(C({ type: 14, customerType: 1 })), false)
assert.equal(FR.delivery_place(C({ type: 19 })), true)
assert.equal(FR.delivery_place(C({ type: 18 })), false)
assert.equal(FR.bear_the_shipping(C({ type: 1 })), true)
assert.equal(FR.bear_the_shipping(C({ type: 18 })), false)
assert.equal(FR.bear_the_shipping(C({ type: 9 })), false)
assert.equal(FR.export_type_name(C({ type: 18 })), true)
console.log('OK test-fr-dnxk')
```

- [ ] **Step 3: Chạy → FAIL.**

- [ ] **Step 4: Viết `field-relevance.js`** (danh sách type theo kết quả reconcile Step 1)

```js
// pages/finance/warehouse-export-requests/field-relevance.js — ĐNXK. Spec §5.4. ctx = { type, customerType }.
const FULL_CUSTOMER = [1, 2, 8, 14, 20, 21] // khối KH đầy đủ (+20/21 D1)
const NAME_ONLY = [12, 19]                   // chỉ có tên
const NO_BEAR = [9, 10, 18, 19]

export const fieldRelevance = {
  export_type_name: (c) => c.type === 18 || c.type === 19,
  emplement_contract_code: (c) => FULL_CUSTOMER.includes(c.type) || c.type === 19,
  customer_code: (c) => FULL_CUSTOMER.includes(c.type),
  customer_name: (c) => FULL_CUSTOMER.includes(c.type) || NAME_ONLY.includes(c.type),
  customer_mobile: (c) => FULL_CUSTOMER.includes(c.type),
  customer_address: (c) => FULL_CUSTOMER.includes(c.type),
  customer_contact_name: (c) => FULL_CUSTOMER.includes(c.type) && c.customerType > 1,
  customer_contact_phone: (c) => FULL_CUSTOMER.includes(c.type) && c.customerType > 1,
  delivery_place: (c) => FULL_CUSTOMER.includes(c.type) || c.type === 19,
  bear_the_shipping: (c) => !NO_BEAR.includes(c.type),
}
```

- [ ] **Step 5: Chạy → PASS.**

- [ ] **Step 6: Ráp 3 màn dùng CHUNG config.** Mỗi file thêm import + `fieldCtx`/`showField` (create/edit đọc `form`/`info`; index đọc `detail`).
  - **index.vue:** (b) XÓA Trạng thái (19-24, header `buildStatusTitle` 214,231-233); (c) customer block (81-102) + bear_the_shipping (59-62) + Số hợp đồng + export_type_name → `showField`.
  - **create.vue:** đổi `v-if="hasCustomer"` (46) → từng field `showField`; `v-if="showBearShipping"` (42-44) → `showField('bear_the_shipping')`.
  - **edit.vue:** customer block (44-63) + bear_the_shipping (41-43) ĐANG VÔ ĐIỀU KIỆN → bọc `showField(...)` cho từng field, hết lệch với create/index.
  - (a): KHÔNG áp (ĐNXK không có cờ "thẳng").

- [ ] **Step 7: Commit (HOÃN)**
```bash
git -C hrm-client add pages/finance/warehouse-export-requests/
git -C hrm-client commit -m "feat(dnxk): bo trang thai + showField 3 man (create/edit/index) dong bo

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 6: YCNH — `product-import-requests`

**Files:**
- Create: `hrm-client/pages/finance/product-import-requests/field-relevance.js`
- Modify: `components/ProductImportRequestForm.vue` (tạo/sửa), `_id/index.vue` (chi tiết — **NGOÀI spec §7.1, bổ sung vào scope**)
- Test: `/Users/nguyentrancu/.claude/jobs/c518e480/tmp/test-fr-ycnh.mjs`

**Interfaces:**
- Produces: `fieldRelevance` (YCNH), `HAS_DELIVERY` (YCNH). ctx = `{ type, isDirect, transitionType, isSettlement }`.

Hằng HRM form: TYPE 2/3/4/9/14/15/99 (823-829), `DELIVERY_TYPES=[2,3,4,9,15,99]` (852), `SOURCE_OPTIONAL_TYPES=[99]`, `NO_INLAND_COST_TYPES=[3]`. Form đã có "Nhập thẳng" checkbox (53-68). Detail `_id/index.vue` hiện "Nhập thẳng" TEXT (53-57) + Trạng thái (17-22). Detail consts TYPE 2/4/9/15 (457-460).

- [ ] **Step 1: Reconcile + viết test thất bại** — `test-fr-ycnh.mjs`

`HAS_DELIVERY` (import) = GIỮ HRM hiện tại `[2,3,4,9,15,99]` (D3/D4; lưu ý ma trận §5.3 ghi `[2,3,4,9,12,15,99]` — HRM không có 12, giữ HRM).

```js
import assert from 'node:assert/strict'
import { fieldRelevance as FR, HAS_DELIVERY } from '/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client/pages/finance/product-import-requests/field-relevance.js'
const C = (o) => ({ type: 0, isDirect: false, transitionType: 0, isSettlement: false, ...o })

assert.equal(FR.is_import_direct, true)
assert.equal(FR.source_report(C({ type: 2 })), true)         // nguồn phiếu báo hàng về
assert.equal(FR.source_report(C({ type: 3 })), false)
assert.equal(FR.source_export_request(C({ type: 3 })), true) // YC xuất hàng
assert.equal(FR.source_export_request(C({ type: 14 })), true)
assert.equal(FR.source_export_request(C({ type: 9 })), false)
assert.equal(FR.source_borrow_sell(C({ type: 9 })), true)
assert.equal(FR.purchase_contract(C({ type: 2 })), true)
assert.equal(FR.settlement_contract(C({ type: 4, isSettlement: true })), true)
assert.equal(FR.settlement_contract(C({ type: 4, isSettlement: false })), false)
assert.equal(FR.supplier_id(C({ type: 99 })), true)
assert.equal(FR.supplier_id(C({ type: 2 })), false)
assert.equal(FR.employee_id(C({ type: 99 })), true)
assert.equal(FR.customer_id(C({ type: 14 })), true)
assert.equal(FR.customer_id(C({ type: 9 })), false)
assert.equal(FR.warehouse_id(C({ isDirect: false })), true)
assert.equal(FR.warehouse_id(C({ isDirect: true })), false)
assert.equal(FR.transition_type(C({ type: 2, isDirect: false })), true)
assert.equal(FR.transition_type(C({ type: 2, isDirect: true })), false)
assert.equal(FR.total_km_expected(C({ type: 2, transitionType: 2, isDirect: false })), true)
assert.deepEqual(HAS_DELIVERY, [2, 3, 4, 9, 15, 99])
console.log('OK test-fr-ycnh')
```

- [ ] **Step 2: Chạy → FAIL.**

- [ ] **Step 3: Viết `field-relevance.js`**

```js
// pages/finance/product-import-requests/field-relevance.js — YCNH. Spec §5.3. ctx = { type, isDirect, transitionType, isSettlement }.
export const HAS_DELIVERY = [2, 3, 4, 9, 15, 99] // GIỮ DELIVERY_TYPES HRM hiện tại (D3/D4)

export const fieldRelevance = {
  is_import_direct: true,
  source_report: (c) => c.type === 2,
  source_export_request: (c) => [3, 4, 14, 99].includes(c.type),
  source_borrow_sell: (c) => c.type === 9,
  source_inland_arrived: (c) => c.type === 15,
  purchase_contract: (c) => c.type === 2 || c.type === 15,
  settlement_contract: (c) => (c.type === 4 || c.type === 9) && c.isSettlement,
  settlement_export_date: (c) => (c.type === 4 || c.type === 9) && c.isSettlement,
  supplier_name: (c) => c.type === 2, // NCC chỉ-đọc loại 2; ngoài 2 → chỉ hiện khi có data
  supplier_id: (c) => c.type === 99,
  employee_id: (c) => c.type === 99,
  customer_id: (c) => c.type === 14,
  warehouse_id: (c) => !c.isDirect,
  transition_type: (c) => HAS_DELIVERY.includes(c.type) && !c.isDirect,
  total_km_expected: (c) => HAS_DELIVERY.includes(c.type) && c.transitionType === 2 && !c.isDirect,
}
```

> Ghi chú key: `source_*` là 4 nhãn nguồn khác nhau của YCNH (map theo `sourceLabel`/`sourceInfoFields`). Khi ráp, bọc `showField` lên đúng ô nguồn tương ứng loại. NCC ngoài loại 2 KHÔNG khai (undefined → luôn hiện) HOẶC khai `() => false` nếu muốn ẩn-khi-rỗng; theo §5.3 "NCC chỉ đọc (ngoài loại 2) → () => false". Bổ sung key `supplier_name_other: () => false` nếu markup có ô NCC riêng ngoài 2; nếu dùng chung 1 ô thì giữ `supplier_name` như trên.

- [ ] **Step 4: Chạy → PASS.**

- [ ] **Step 5: Ráp `ProductImportRequestForm.vue` (tạo/sửa)** — import + `fieldCtx`/`showField` (đọc `form`). (a): "Nhập thẳng" ĐÃ là checkbox (53-68) → giữ. (c): Kho nhập (136-150, hiện `v-if="!form.is_import_direct"`) → `showField('warehouse_id')`; Khách hàng (153-166, `isConsignment`) → `showField('customer_id')`; NCC/NV (170-187, `isOther`) → `showField('supplier_id')`/`showField('employee_id')`; Vận chuyển (192, `showDeliveryFields`) → `showField('transition_type')`; Số km (208) → `showField('total_km_expected')`; ô nguồn theo loại → `source_*`.

- [ ] **Step 6: Ráp `_id/index.vue` (chi tiết — bổ sung scope)** — import + `fieldCtx`/`showField` (đọc `data`; dùng key `data.*`).
  - **(a)** "Nhập thẳng" TEXT (53-57) → checkbox: `<V2BaseCheckbox :value="Number(data.is_import_direct) === 1" disabled label="Nhập thẳng" />`, gate `v-if="showField('is_import_direct')"`.
  - **(b)** XÓA Trạng thái (17-22) — header `buildStatusTitle` (428,507-512).
  - **(c)** Kho nhập (49-52), Khách hàng (58-61), NCC (62-65), Nhân viên (67-70), Vận chuyển (72-75), Số km (77-80), nguồn (29-47) → `showField`.

> Lưu ý: detail dùng `data`, không phải `detail`. `getValue = (k) => this.data[k]`, ctx đọc `data.*`.

- [ ] **Step 7: Commit (HOÃN)**
```bash
git -C hrm-client add pages/finance/product-import-requests/
git -C hrm-client commit -m "feat(ycnh): checkbox nhap thang (chi tiet) + bo trang thai + showField

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 7: ĐNNK — `warehouse-import-requests` (thống nhất 3 màn + nhãn đối tác động)

**Files:**
- Create: `hrm-client/pages/finance/warehouse-import-requests/field-relevance.js`
- Modify: `create.vue`, `_id/edit.vue`, `_id/index.vue`
- Test: `/Users/nguyentrancu/.claude/jobs/c518e480/tmp/test-fr-dnnk.mjs`

**Interfaces:**
- Produces: `fieldRelevance` (ĐNNK). ctx = `{ type }`.

Hiện trạng (extraction): KHÔNG có biến `type` số/computed gate-theo-loại ở cả 3 file; "Loại" chỉ là chuỗi `type_name`. Nhãn đối tác: create dùng `info.use_customer` (động 1 ô), edit dùng v-if `supplier_name`/v-else-if `customer_name`, index CỨNG "Nhà cung cấp". `emplement_contract_code`/`department_name` là trường HRM THÊM (ERP không có).

- [ ] **Step 1: Reconcile — xác định `type` khả dụng (Review Focus #1)**

ĐNNK hiện không đọc `type` số ở FE. Để gate theo loại, cần `info.type`/`detail.type` từ BE. **Kiểm BE (Task 2 đã audit)**: nếu response ĐNNK KHÔNG trả `type` số → hoặc (a) bổ sung `type` vào Resource ĐNNK (Task 2), hoặc (b) ruling: các field ĐNNK HRM-thêm (`emplement_contract_code`, `department_name`) khai `() => false` (chỉ hiện khi có data) — KHÔNG cần `type`; nhãn đối tác giữ cơ chế hiện tại (`use_customer`/tồn tại data). Ghi ruling vào ledger. Test dưới chỉ kiểm các predicate không cần type + đối tác theo type nếu type có sẵn.

- [ ] **Step 2: Viết test thất bại** — `test-fr-dnnk.mjs`

```js
import assert from 'node:assert/strict'
import { fieldRelevance as FR } from '/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client/pages/finance/warehouse-import-requests/field-relevance.js'
const C = (o) => ({ type: 0, ...o })

// Trường HRM-thêm → chỉ hiện khi có data
assert.equal(FR.emplement_contract_code(C({ type: 4 })), false)
assert.equal(FR.department_name(C({ type: 4 })), false)
// Đối tác KH vs NCC theo loại (nếu type có sẵn)
assert.equal(FR.customer_name(C({ type: 4 })), true)
assert.equal(FR.customer_name(C({ type: 9 })), true)
assert.equal(FR.customer_name(C({ type: 14 })), true)
assert.equal(FR.customer_name(C({ type: 2 })), false)
assert.equal(FR.supplier_name(C({ type: 2 })), true)
assert.equal(FR.supplier_name(C({ type: 11 })), true)
assert.equal(FR.supplier_name(C({ type: 4 })), false)
// Nguồn (Mã YCNH): loại 10 đổi nhãn → vẫn liên quan (hiển thị), test chỉ khẳng định != gây ẩn sai
assert.equal(FR.warehouse_id, true)
console.log('OK test-fr-dnnk')
```

- [ ] **Step 3: Chạy → FAIL.**

- [ ] **Step 4: Viết `field-relevance.js`**

```js
// pages/finance/warehouse-import-requests/field-relevance.js — ĐNNK. Spec §5.5. ctx = { type }.
const CUSTOMER_PARTNER = [4, 9, 14]
const SUPPLIER_PARTNER = [1, 2, 3, 11, 12, 13, 15, 16]

export const fieldRelevance = {
  warehouse_id: true,                                   // luôn hiện
  emplement_contract_code: () => false,                 // HRM thêm → hiện khi có data
  department_name: () => false,                         // HRM thêm → hiện khi có data
  customer_name: (c) => CUSTOMER_PARTNER.includes(c.type),
  supplier_name: (c) => SUPPLIER_PARTNER.includes(c.type),
}
```

- [ ] **Step 5: Chạy → PASS.**

- [ ] **Step 6: Ráp 3 màn dùng CHUNG config.**
  - **index.vue:** (b) XÓA Trạng thái (19-24, header `buildStatusTitle` pageTitle 276-282). (c) `emplement_contract_code`/`contract_code` (41-53), `department_name` (62-65), đối tác (58-61) → `showField`. **Nhãn đối tác động:** index đang CỨNG "Nhà cung cấp" `detail.supplier_name` → sửa thành: nếu `showField('customer_name')` hiện "Khách hàng" + `detail.customer_name`, else "Nhà cung cấp" + `detail.supplier_name` (dùng `fieldCtx.type`; đồng bộ create `use_customer`/edit v-if).
  - **create.vue:** `emplement_contract_code` (37-40) → `showField`; nhãn đối tác (41-44, `use_customer`) giữ hoặc đồng bộ theo type nếu type có.
  - **edit.vue:** đối tác (31-38, v-if supplier/v-else-if customer) → thống nhất qua `showField` + nhãn động.
  - (a): KHÔNG áp.

> Ruling nhãn đối tác: nếu BE trả `type` → nhãn theo type (nhất quán 3 màn). Nếu không → GIỮ cơ chế hiện tại từng màn (create `use_customer`, edit/index theo tồn tại data), chỉ bọc `showField` phần ẩn-khi-rỗng. Ghi quyết định vào ledger theo kết quả Step 1.

- [ ] **Step 7: Commit (HOÃN)**
```bash
git -C hrm-client add pages/finance/warehouse-import-requests/
git -C hrm-client commit -m "feat(dnnk): bo trang thai + showField 3 man + nhan doi tac dong

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 8: PNK — `product-imports`

**Files:**
- Create: `hrm-client/pages/finance/product-imports/field-relevance.js`
- Modify: `components/ProductImportForm.vue` (tạo/sửa), `_id/index.vue` (chi tiết — **NGOÀI spec §7.1, bổ sung vào scope**)
- Test: `/Users/nguyentrancu/.claude/jobs/c518e480/tmp/test-fr-pnk.mjs`

**Interfaces:**
- Produces: `fieldRelevance` (PNK). ctx = `{ type, isDirect, isSettlement }` (`type` = `import_type`).

Hằng HRM: `accountRows` theo import_type 4/9/2/11 (1431-1460), `isSettlementHeader` ([4,9] && is_settlement, 1426). Form "Nhập thẳng" TEXT (93-97); fields gate bằng `header.is_import_direct===0`. Detail `_id/index.vue`: "Nhập thẳng" TEXT (42-45), Trạng thái (26-33), template A/B theo `is_import_direct`.

- [ ] **Step 1: Reconcile + viết test thất bại** — `test-fr-pnk.mjs`

```js
import assert from 'node:assert/strict'
import { fieldRelevance as FR } from '/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client/pages/finance/product-imports/field-relevance.js'
const C = (o) => ({ type: 0, isDirect: false, isSettlement: false, ...o })

assert.equal(FR.is_import_direct, true)
assert.equal(FR.warehouse_import_code(C({ isDirect: false })), true)
assert.equal(FR.warehouse_import_code(C({ isDirect: true })), false)
assert.equal(FR.product_import_request_code(C({ isDirect: true })), true)
assert.equal(FR.product_import_request_code(C({ isDirect: false })), false)
assert.equal(FR.warehouse_name(C({ isDirect: false })), false, 'ERP ẩn theo data → !isEmpty')
assert.equal(FR.customer_name(C({ type: 2 })), false, 'ẩn khi rỗng (HRM đang hiện luôn)')
assert.equal(FR.accounting_date(C({ type: 8 })), true)
assert.equal(FR.accounting_date(C({ type: 4 })), false)
assert.equal(FR.account_has(C({ type: 10 })), true)
assert.equal(FR.work_id(C({ type: 8 })), true)
assert.equal(FR.settlement_contract_code(C({ type: 4, isSettlement: true })), true)
assert.equal(FR.settlement_contract_code(C({ type: 4, isSettlement: false })), false)
assert.equal(FR.not_paying_bill(C({ type: 4 })), true)
assert.equal(FR.not_paying_bill(C({ type: 2 })), false)
assert.equal(FR.account_rows(C({ type: 2 })), true)
assert.equal(FR.account_rows(C({ type: 5 })), false)
console.log('OK test-fr-pnk')
```

- [ ] **Step 2: Chạy → FAIL.**

- [ ] **Step 3: Viết `field-relevance.js`**

```js
// pages/finance/product-imports/field-relevance.js — PNK. Spec §5.6. ctx = { type, isDirect, isSettlement }. type = import_type.
const ACCOUNTING = [8, 10]
const ACCOUNT_ROWS_TYPES = [2, 4, 9, 11]

export const fieldRelevance = {
  is_import_direct: true,
  warehouse_import_code: (c) => !c.isDirect,           // đường A
  product_import_request_code: (c) => c.isDirect,      // đường B
  warehouse_name: () => false,                         // theo data
  warehouse_keeper_name: () => false,
  shipper: () => false,
  supplier_name: () => false,
  customer_name: () => false,                          // HRM đang hiện luôn → đổi ẩn-khi-rỗng
  accounting_date: (c) => ACCOUNTING.includes(c.type),
  account_has: (c) => ACCOUNTING.includes(c.type),
  work_id: (c) => ACCOUNTING.includes(c.type),
  settlement_contract_code: (c) => (c.type === 4 || c.type === 9) && c.isSettlement,
  settlement_export_date: (c) => (c.type === 4 || c.type === 9) && c.isSettlement,
  not_paying_bill: (c) => c.type === 4 || c.type === 9,
  account_rows: (c) => ACCOUNT_ROWS_TYPES.includes(c.type),
}
```

- [ ] **Step 4: Chạy → PASS.**

- [ ] **Step 5: Ráp `ProductImportForm.vue` (tạo/sửa)** — import + `fieldCtx`/`showField` (đọc `header`; ctx `type: Number(header.import_type)`).
  - (a) "Nhập thẳng" TEXT (93-97) → checkbox: `<V2BaseCheckbox :value="Number(header.is_import_direct) === 1" disabled label="Nhập thẳng" />` (read-only — form này đọc từ nguồn), gate `showField('is_import_direct')`.
  - (c) Thay gate `header.is_import_direct===0/===1` bằng `showField('warehouse_import_code')`/`showField('product_import_request_code')`/`showField('warehouse_name')`/`showField('warehouse_keeper_name')`/`showField('shipper')`; `supplier_name` (118-121) + `customer_name` (122-125) → `showField`; `not_paying_bill` (133-140, `cfg.flags.hasNotPayingBill`) → `showField('not_paying_bill')`; accountRows (156-166) → `showField('account_rows')`.

> Ruling: KHÔNG có "Xuất thẳng"; chỉ "Nhập thẳng". PNK không có `type` biến đổi trong form (type 4 cố định, template A/B theo `is_import_direct`) → các gate bằng `isDirect` là chính; type-based chỉ cho tab hạch toán.

- [ ] **Step 6: Ráp `_id/index.vue` (chi tiết — bổ sung scope)** — import + `fieldCtx`/`showField` (đọc `data`; `type: Number(data.import_type)`).
  - (a) "Nhập thẳng" TEXT (42-45) → checkbox, gate `showField('is_import_direct')`.
  - (b) XÓA Trạng thái (26-33) — header `buildStatusTitle` (433,474-478).
  - (c) Template A (`!data.is_import_direct`: 48-72) / B (`v-else`: 76-97) giữ cấu trúc A/B (đó là 2 nhánh nguồn), nhưng các ô Kho/Thủ kho/shipper/supplier/customer bọc `showField` để ẩn-khi-rỗng; `not_paying_bill` (118-121); TK/Mã vụ việc ở tab Hạch toán → `showField('account_has')`/`showField('work_id')`.

- [ ] **Step 7: Commit (HOÃN)**
```bash
git -C hrm-client add pages/finance/product-imports/
git -C hrm-client commit -m "feat(pnk): checkbox nhap thang + bo trang thai + showField

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 9: YCXBHM — `borrow-sell-requests`

**Files:**
- Create: `hrm-client/pages/finance/borrow-sell-requests/field-relevance.js`
- Modify: `components/BorrowSellRequestForm.vue` (tạo), `_id/index.vue` (chi tiết)
- Test: `/Users/nguyentrancu/.claude/jobs/c518e480/tmp/test-fr-ycxbhm.mjs`

**Interfaces:**
- Produces: `fieldRelevance` (YCXBHM). ctx = `{ customerType, isFirm, contractType, hasRebate }`.

Hiện trạng: form tạo minimal (Số HĐ picker, Khách hàng tên, Loại HĐ, Ghi chú) — KHÔNG có cụm KH chi tiết. Detail (`_id/index.vue`): Trạng thái (19-24, `buildStatusTitle` 295,337); cụm KH đầy đủ; Người liên hệ/ĐT liên hệ ĐÃ gate `Number(data.customer_type) > 1` (template 84-93) — GIỮ; Nơi giao `v-if="data.delivery_place"` (94) — GIỮ; `need_repair` (61-62) GIỮ; Lý do từ chối `v-if="isDenied"`.

- [ ] **Step 1: Viết test thất bại** — `test-fr-ycxbhm.mjs`

```js
import assert from 'node:assert/strict'
import { fieldRelevance as FR } from '/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client/pages/finance/borrow-sell-requests/field-relevance.js'
const C = (o) => ({ customerType: 1, isFirm: false, contractType: 1, hasRebate: false, ...o })

// cụm KH luôn hiện (ERP hiện cả khi rỗng)
assert.equal(FR.customer_name, true)
assert.equal(FR.customer_code, true)
assert.equal(FR.customer_tax_code, true)
assert.equal(FR.customer_mobile, true)
assert.equal(FR.customer_address, true)
assert.equal(FR.need_repair, true, 'ERP luôn hiện — KHÔNG đụng')
// liên hệ theo loại khách hàng
assert.equal(FR.customer_contact_name(C({ customerType: 2 })), true)
assert.equal(FR.customer_contact_name(C({ customerType: 1 })), false)
assert.equal(FR.customer_contact_phone(C({ customerType: 2 })), true)
// Nơi giao (HRM thêm) → hiện khi có data
assert.equal(FR.delivery_place(C()), false)
console.log('OK test-fr-ycxbhm')
```

- [ ] **Step 2: Chạy → FAIL.**

- [ ] **Step 3: Viết `field-relevance.js`**

```js
// pages/finance/borrow-sell-requests/field-relevance.js — YCXBHM. Spec §5.7.
// ctx = { customerType, isFirm, contractType, hasRebate }. form.type (Hàng bán/KM) KHÔNG gate header.
export const fieldRelevance = {
  customer_name: true,
  customer_code: true,
  customer_tax_code: true,
  customer_mobile: true,
  customer_address: true,
  need_repair: true, // ERP luôn hiện — KHÔNG đụng
  customer_contact_name: (c) => c.customerType > 1,
  customer_contact_phone: (c) => c.customerType > 1,
  delivery_place: () => false, // HRM thêm → hiện khi có data
}

// Gate card "Thông tin thanh toán hợp đồng" (ngoài khối Thông tin chung):
export const showContractPayment = (c) => c.isFirm && c.contractType !== 3 && !c.hasRebate
```

- [ ] **Step 4: Chạy → PASS.**

- [ ] **Step 5: Ráp `_id/index.vue` (chi tiết)** — import + `fieldCtx`/`showField` (đọc `data`; `customerType: Number(data.customer_type)`).
  - (b) XÓA Trạng thái (19-24).
  - (c) Người liên hệ/ĐT liên hệ (template 84-93) → thay `Number(data.customer_type) > 1` bằng `showField('customer_contact_name')` / `showField('customer_contact_phone')` (tương đương, nhưng thêm fallback !isEmpty — nhất quán helper). Nơi giao (94) → `showField('delivery_place')` (tương đương `v-if="data.delivery_place"`). Cụm KH + `need_repair`: KHÔNG bọc (luôn hiện).
  - (a): KHÔNG áp.

- [ ] **Step 6: Ráp `BorrowSellRequestForm.vue` (tạo)** — form minimal, không có field biến thiên theo loại trong Thông tin chung → chỉ import helper nếu cần; thực tế KHÔNG có trường cần ẩn. Ghi ledger: form tạo YCXBHM không có thay đổi (b/c không áp — không có Trạng thái, không có cụm field biến thiên). Bỏ qua nếu không có gì sửa.

- [ ] **Step 7: Commit (HOÃN)**
```bash
git -C hrm-client add pages/finance/borrow-sell-requests/
git -C hrm-client commit -m "feat(ycxbhm): bo trang thai + showField (lien he theo loai KH)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 10: PXBHM — `borrow-sells`

**Files:**
- Create: `hrm-client/pages/finance/borrow-sells/field-relevance.js`
- Modify: `components/BorrowSellForm.vue` (tạo), `_id/index.vue` (chi tiết)
- Test: `/Users/nguyentrancu/.claude/jobs/c518e480/tmp/test-fr-pxbhm.mjs`

**Interfaces:**
- Produces: `fieldRelevance` (PXBHM). ctx = `{ customerType, isFirm, contractType, hasRebate }`.

Hiện trạng: form tạo `bear_the_shipping` ĐÃ là `V2BaseCheckbox v-model` (69-71) — KHÔNG đụng. Detail (`_id/index.vue`): Trạng thái (22-27, `buildStatusTitle` 376,409); Người liên hệ (71-72) + ĐT liên hệ (79-80) ĐANG VÔ ĐIỀU KIỆN → **bổ sung gate `customer_type > 1`**; `delivery_place`/`contact_address` (HRM thêm); "Chịu phí ship" (52, text) — KHÔNG đụng; card "Thông tin thanh toán hợp đồng" `needContractInfo` (220).

- [ ] **Step 1: Viết test thất bại** — `test-fr-pxbhm.mjs`

```js
import assert from 'node:assert/strict'
import { fieldRelevance as FR } from '/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client/pages/finance/borrow-sells/field-relevance.js'
const C = (o) => ({ customerType: 1, isFirm: false, contractType: 1, hasRebate: false, ...o })

assert.equal(FR.bear_the_shipping, true, 'đã là checkbox — KHÔNG đụng (vẫn luôn hiện)')
assert.equal(FR.customer_name, true)
assert.equal(FR.delivery_address, true)
assert.equal(FR.customer_contact_name(C({ customerType: 2 })), true)
assert.equal(FR.customer_contact_name(C({ customerType: 1 })), false)
assert.equal(FR.customer_contact_phone(C({ customerType: 2 })), true)
assert.equal(FR.delivery_place(C()), false)
assert.equal(FR.contact_address(C()), false)
console.log('OK test-fr-pxbhm')
```

- [ ] **Step 2: Chạy → FAIL.**

- [ ] **Step 3: Viết `field-relevance.js`**

```js
// pages/finance/borrow-sells/field-relevance.js — PXBHM. Spec §5.8.
// ctx = { customerType, isFirm, contractType, hasRebate }.
export const fieldRelevance = {
  bear_the_shipping: true,   // đã là checkbox ở form — KHÔNG đụng
  customer_name: true,
  delivery_address: true,
  customer_code: true,
  identity_card_number: true,
  customer_mobile: true,
  customer_contact_name: (c) => c.customerType > 1,  // HRM detail CHƯA gate → bổ sung
  customer_contact_phone: (c) => c.customerType > 1,
  delivery_place: () => false,   // HRM thêm → hiện khi có data
  contact_address: () => false,  // HRM thêm → hiện khi có data
}

export const showContractPayment = (c) => c.isFirm && c.contractType !== 3 && !c.hasRebate
```

- [ ] **Step 4: Chạy → PASS.**

- [ ] **Step 5: Ráp `_id/index.vue` (chi tiết)** — import + `fieldCtx`/`showField` (đọc `data`; `customerType: Number(data.customer_type)`).
  - (b) XÓA Trạng thái (22-27).
  - (c) **Người liên hệ (71-72) + ĐT liên hệ (79-80):** THÊM `v-if="showField('customer_contact_name')"` / `v-if="showField('customer_contact_phone')"` (hiện vô điều kiện → nay gate `customer_type > 1`, giữ hiện khi có data). `delivery_place` (88) → `showField('delivery_place')`; `contact_address` (84) → `showField('contact_address')`. Cụm KH + "Chịu phí ship" + Loại HĐ: KHÔNG bọc (luôn hiện).
  - (a): KHÔNG áp.

- [ ] **Step 6: Ráp `BorrowSellForm.vue` (tạo)** — `bear_the_shipping` checkbox giữ nguyên. Form tạo không có Trạng thái, không có cụm field biến thiên trong Thông tin chung (chỉ read-only từ phiếu YC) → (b/c) hầu như không áp. Nếu có ô nào cần ẩn-khi-rỗng (vd `delivery_address` rỗng) thì cân nhắc; mặc định KHÔNG đụng form tạo. Ghi ledger.

- [ ] **Step 7: Commit (HOÃN)**
```bash
git -C hrm-client add pages/finance/borrow-sells/
git -C hrm-client commit -m "feat(pxbhm): bo trang thai + gate lien he theo loai KH (bo sung)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 11: Verify Playwright e2e (8 màn × 3 chế độ)

**Files:** không sửa code (trừ fix lỗi phát hiện — mỗi fix phải có task/ghi ledger).

**Tiền đề:** dev server hrm-client chạy ở `http://127.0.0.1:3000`; đăng nhập sẵn. Dùng Playwright MCP, Node 20.

- [ ] **Step 1: (a) checkbox "thẳng"** — mỗi màn có cờ (YCXH, PXH, YCNH, PNK): mở 1 phiếu `is_*_direct=1` và 1 phiếu `=0` → trường hiển thị **V2BaseCheckbox** (tick/không tick), read-only, không bấm được. Chụp snapshot xác nhận là checkbox (không phải text "Có/Không").

- [ ] **Step 2: (b) bỏ Trạng thái** — mở chi tiết cả 8 màn → khối THÔNG TIN CHUNG **không còn** dòng "Trạng thái"; header vẫn có badge đúng màu (`buildStatusTitle`). Xác nhận bằng snapshot DOM: không có `V2BaseLabel` text "Trạng thái" trong card "Thông tin chung".

- [ ] **Step 3: (c) ẩn** — ví dụ kiểm: PNK loại 2 chi tiết → ô Khách hàng ẩn khi rỗng; YCXH loại 3 → không có "Xuất thẳng"; ĐNXK loại không-KH → không có Số hợp đồng/khối KH. Snapshot xác nhận trường vắng.

- [ ] **Step 4: (c) hiện vì có data** — mở Sửa 1 phiếu cũ có dữ liệu ở trường không-liên-quan-với-loại-hiện-tại → trường **vẫn hiện**. (Chọn 1 phiếu thực tế per màn có sẵn data; nếu không có, ghi ledger là "không có mẫu để kiểm — dựa node test".)

- [ ] **Step 5: (c) hiện vì liên quan dù rỗng** — loại liên quan nhưng chưa nhập → ô vẫn hiện (trống) để nhập.

- [ ] **Step 6: Reactivity (tạo) — Review Focus #3** — màn tạo (YCXH, YCNH): đổi dropdown Loại / tick thẳng → trường ẩn/hiện cập nhật tức thì; **số liệu đã nhập KHÔNG mất** khi trường bị ẩn rồi hiện lại (khẳng định edge §8.3: giá trị `form` được GIỮ).

- [ ] **Step 7: Đồng bộ 3 màn ĐNXK & ĐNNK — Review Focus #1** — cùng 1 phiếu/loại, mở create/edit/index → **cùng tập trường** hiện ra (không còn lệch). Kiểm đặc biệt edit.vue ĐNXK (trước đây hiện vô điều kiện) nay khớp index.

- [ ] **Step 8: Hoàn trả data** nếu có chỉnh tạm (đổi status/loại để quan sát). Ghi ledger kết quả từng bước; mọi lỗi phát hiện → tạo task fix (không tự ý mở rộng scope).

- [ ] **Step 9: Commit (HOÃN)** — chỉ nếu Step 8 có fix nhỏ. Message theo format cuối file.

---

## Task 12: Fix D1 — cờ boolean type-gated hiện sai ở loại không liên quan

**Phát hiện (Task 11 Step 3):** YCXH loại 3 "Xuất mượn" vẫn hiện "Xuất thẳng" (checkbox không tick) ở cả tạo + chi tiết — plan Task 11 Step 3 yêu cầu ẩn. Loại 15 cùng cảnh (chưa có mẫu).

**Root cause:** `fieldRelevance.is_export_direct = (c) => c.type !== 3 && c.type !== 15` ĐÚNG (relevance=false cho loại 3/15). Nhưng `showField(k) = isRelevant || !isEmptyValue(value)`; cờ boolean có `value = 0`, mà `isEmptyValue(0) === false` (cố ý — 0 là giá trị nghiệp vụ hợp lệ cho số) → nhánh `!isEmpty` luôn true → field luôn hiện. Fallback "có-data" vô hiệu hóa gate cho **cờ boolean**.

**Phạm vi dính (rà đủ 8 màn):** chỉ 2 field là cờ boolean + relevance gate-theo-loại (có thể = false):
- YCXH `is_export_direct: (c) => c.type !== 3 && c.type !== 15` — **D1 confirmed**.
- PNK `not_paying_bill: (c) => c.type === 4 || c.type === 9` — **latent sibling** cùng root cause (loại khác 4/9, cờ=0 → hiện sai; chưa verify runtime).
- Các cờ direct còn lại (PXH/PNK `is_*_direct`, YCNH `is_import_direct`) relevance = `true` (luôn hiện) → KHÔNG dính.

**Quyết định scope (CHỜ USER — fix sạch nhất đụng helper dùng chung `utils/flow-field-visibility.js`):**
- [ ] **Chốt hướng fix với user** (xem mục "Điểm cần user xác nhận" #5). Ghi ruling vào ledger.
- [ ] **Step 1: Viết test đỏ** — bổ sung `test-fr-flag-visibility.mjs`: với cờ boolean đã-khai-là-flag, loại không-liên-quan + value 0 → `showField === false`; loại liên quan → true; field thường value 0 vẫn giữ `!isEmpty` (không hồi quy). Chạy → FAIL.
- [ ] **Step 2: Implement** theo hướng đã chốt (A: helper nhận tập "flag keys" gate relevance-only; hoặc B: gate cờ bằng relevance-only ngay tại component, không đụng helper).
- [ ] **Step 3: Chạy test → PASS** + chạy lại `test-fr-pnk.mjs` (không hồi quy `not_paying_bill`).
- [ ] **Step 4: Playwright** — YCXH loại 3 (tạo + chi tiết 35685): "Xuất thẳng" ẩn; loại 14 vẫn hiện checkbox. PNK loại ngoài {4,9}: "Không xuất hóa đơn" ẩn khi cờ=0.
- [ ] **Step 5: Commit (HOÃN)** — `fix(flow-field): cờ boolean loại không liên quan phải ẩn (D1)`, trailer theo format cuối file.

---

## Self-Review (đã chạy khi viết plan)

**1. Spec coverage:**
- (a) checkbox: YCXH (T3), PXH (T4, THÊM field), YCNH (T6), PNK (T8). ✅
- (b) bỏ Trạng thái: 8 màn (T3–T10). ✅
- (c) showField: 8 màn + helper (T1) + 8 field-relevance (T3–T10) từ ma trận §5.1–5.8. ✅
- BE audit (§7.1): T2. ✅
- Gap vs §7.1 đã bổ sung: YCNH `_id/index.vue` (T6), PNK `_id/index.vue` (T8), PXH THÊM "Xuất thẳng" (T4), PXBHM gate liên hệ (T10). ✅
- Test (§9 Playwright): T11; node test logic thuần mỗi task. ✅

**2. Placeholder scan:** Helper + 8 field-relevance có code đầy đủ; test có assert thật. Các "ruling" (HAS_DELIVERY, scope (c), reconcile type, nhãn đối tác ĐNNK) là QUYẾT ĐỊNH có điều kiện rõ ràng + cần user xác nhận, không phải TODO. Bước "reconcile hằng type" là hành động cụ thể (đọc const, đối chiếu), không phải placeholder. ✅

**3. Type consistency:** `makeFieldVisibility(relevanceMap, getValue, getCtx)` ký hiệu nhất quán T1↔T3–T10. `fieldCtx`/`showField` computed đồng nhất. Key `type`/`isDirect`/`transitionType`/`customerType`/`isSettlement` trong ctx khớp field-relevance predicate. Detail đọc `detail`/`data` tùy màn (đã ghi rõ per task). ✅

**4. Review Focus:** 5 mục đã pin vào task (type reconcile T3–T10 bước 1; HAS_DELIVERY T3; reactivity T11 bước 6; số 0/boolean T1 test; buildStatusTitle mỗi task bước b). ✅

---

## Điểm cần user xác nhận ở plan-review (không chặn, nhưng nên chốt)

1. **HAS_DELIVERY (YCXH, YCNH):** plan GIỮ list HRM hiện tại (D3/D4). User muốn theo ERP `getHasDeliveryTypes`? → chỉ đổi 1 hằng/màn.
2. **Số type ĐNXK/ĐNNK:** ma trận dùng số ERP; plan có bước reconcile. Nếu user biết trước HRM đánh số khác → cung cấp để rút ngắn.
3. **Scope (c) ở tạo/sửa YCXH:** plan áp showField cho khối chi tiết + cờ thẳng; field tạo/sửa khác giữ computed cũ. Mở rộng toàn bộ? → thêm 1 task.
4. **Commit:** tất cả bước commit ĐANG HOÃN (standing constraint). Cho phép commit theo từng task hay gộp cuối?
5. **[MỞ — Task 12] Hướng fix D1 (cờ boolean hiện sai ở loại không liên quan):**
   - **Hướng A (đề xuất):** bổ sung khái niệm "flag field" vào helper dùng chung `utils/flow-field-visibility.js` — `makeFieldVisibility` nhận thêm tập khóa cờ (hoặc relevance khai `{ fn, flag: true }`); field flag → hiển thị = **relevance-only**, bỏ fallback has-data. Khai `is_export_direct` (YCXH) + `not_paying_bill` (PNK) là flag. Sửa đồng nhất, fix cả D1 lẫn sibling PNK, 1 chỗ. **ĐỤNG HÀM DÙNG CHUNG → cần user xác nhận** (hard rule CLAUDE.md).
   - **Hướng B:** không đụng helper — tại YCXH (và PNK) gate riêng cờ bằng `fieldRelevance.is_export_direct(fieldCtx)` thay cho `showField(...)`. Tối thiểu, nhưng lệch pattern `showField` thống nhất và phải lặp ở từng màn có cờ.

## Commit message format (khi được phép)
- Cuối message: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`
- PR description (nếu tạo PR): cuối thêm `🤖 Generated with [Claude Code](https://claude.com/claude-code)`
