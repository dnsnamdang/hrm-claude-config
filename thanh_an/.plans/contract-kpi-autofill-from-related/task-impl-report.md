# Báo cáo implement — Tự gắn hàng hóa từ HĐ liên quan vào danh sách KPI

**Ngày:** 2026-06-30
**File sửa duy nhất:** `hrm-thanhan-client/pages/contract/contract/components/GeneralComponent.vue`
**Phạm vi:** Thuần FE (Nuxt 2 / Vue 2), không đụng Backend, không file dùng chung khác.

---

## 1. Các đoạn đã thêm (kèm vị trí/anchor)

### Task 1 — Step 1: data field
- **Anchor:** ngay sau `relatedContracts: [],` (dòng ~1314) trong `data() { return { ... } }`.
- **Thêm:** `isLoadingKpiAutofill: false,`

### Task 1 — Step 2 + Task 2 — Step 1,2,3: methods
- **Anchor:** chèn ngay TRƯỚC `async getRelatedContracts() {` (gốc ~dòng 2308) trong `methods: {}` để gom logic liên quan.
- **Thêm 5 method (theo đúng thứ tự):**
  1. `mapProductToKpi(product)` — destructure bỏ `id`, spread `...rest`, reset 6 cờ UI (`edit_product_name`, `edit_trade_name`, `edit_owner_country`, `edit_producer_country`, `edit_technical_specification`, `extend_technical_specification`) = false. Giữ nguyên giá/SL.
  2. `removeAutofilledKpiGroups()` — filter bỏ nhóm `from_related_contract`.
  3. `applyKpiAutofillFromRelated()` (async) — gồm nhánh điều kiện không thỏa → gọi `removeAutofilledKpiGroups()`; cờ chống double-trigger `isLoadingKpiAutofill`; `$nuxt.$loading.start()/finish()`; gọi `apiGetMethod` `category/contracts/${relatedId}`; map `groups` (lọc nhóm rỗng) → nhóm KPI có cờ `from_related_contract:true` + `related_contract_id`; nếu rỗng → toast warning + return; nếu có → append `[...old, ...injected]` + toast success + `$forceUpdate()`; catch → console.error + toast error; finally → reset cờ + finish loading.
  4. `onHasKpiChange()` — gọi `applyKpiAutofillFromRelated()`.
  5. `onRelatedContractChange()` — gọi `applyKpiAutofillFromRelated()`.
- Mỗi method kết thúc bằng dấu phẩy; tất cả nằm trong `methods: {}`.

### Task 3 — Step 1: bind select "Có áp KPI"
- **Anchor:** dòng ~141, dưới `<label>Có áp KPI <Required /></label>`.
- Tách `<base-select2 .../>` thành multiline, thêm `@input="onHasKpiChange"`.

### Task 3 — Step 2: bind select "Hợp đồng liên quan"
- **Anchor:** dòng ~146, dưới `<label>Hợp đồng liên quan</label>`.
- Thêm `:settings="{ allowClear: true }"` và `@input="onRelatedContractChange"`.

---

## 2. Kết quả 2 bước xác minh

### 2.1 `$toasted.global.warning` (Task 2 Step 4)
- **Lệnh:** grep `toasted.global.warning` trong `hrm-thanhan-client/pages`.
- **Kết quả:** CÓ tồn tại — nhiều nơi dùng (vd `contract/discount_appendix/components/ProductComponent.vue:1203,1923`, `contract/contract_annex_vat/components/ProductComponent.vue:648,1397`, `contract/contract_annex_quantity/components/ProductComponent.vue:820`).
- **Nhánh đã chọn:** GIỮ NGUYÊN `warning` (không đổi sang `error`).

### 2.2 `:settings`/`$attrs` forward qua BaseSelect2 (Task 3 Step 3)
- **Lệnh:** grep `settings|allowClear|$attrs` trong `components/BaseSelect2.vue`.
- **Kết quả:** dòng 19 có `v-bind="$attrs"` đặt trên `<select2>`. `settings` KHÔNG nằm trong `props` khai báo (chỉ có `value, options, name, isShowText, text, showTooltip, classText`) → `:settings`/`allowClear` truyền xuống `v-select2-component` qua `$attrs`. Xác nhận forward OK.
- **Bonus xác minh cơ chế @input:** `onChange` (dòng 62-63) `$emit('input', value)` chỉ chạy từ event `@change` của select2 (do user thao tác). Khi `value` prop bị gán lúc edit nạp dữ liệu → chỉ cập nhật `internalValue` qua watch, KHÔNG emit `input`. ⟹ Đúng thiết kế: edit nạp dữ liệu KHÔNG tự kích hoạt autofill (spec §4.2, edge §5).

---

## 3. Tự review — khớp spec rule 1-8

| Rule | Yêu cầu | Cài đặt | OK |
|------|---------|---------|----|
| 1 | Nguồn = `groups` của HĐ liên quan | `data.groups` trong `applyKpiAutofillFromRelated` | ✓ |
| 2 | Tự động khi đủ 2 điều kiện | `@input` 2 select → handler → check `has_kpi==1` && `related_contract_id` | ✓ |
| 3 | Giữ cấu trúc nhóm | map mỗi `group` → 1 nhóm KPI cùng `group_name` + `product_kpis` | ✓ |
| 4 | Giá & SL theo HĐ liên quan | `mapProductToKpi` spread `...rest` giữ nguyên price/qty/... | ✓ |
| 5 | Append vào cuối | `[...(group_kpis||[]), ...injectedGroups]` | ✓ |
| 6 | Cộng dồn khi đổi HĐ | KHÔNG gỡ nhóm cũ trước append; chỉ gỡ khi điều kiện không thỏa | ✓ |
| 7 | Bỏ chọn HĐ → gỡ nhóm tự gắn | nhánh `!relatedId` → `removeAutofilledKpiGroups()`; `allowClear` cho phép về rỗng | ✓ |
| 8 | Tắt KPI → gỡ nhóm tự gắn | nhánh `!hasKpi` → `removeAutofilledKpiGroups()` | ✓ |
| §3.1 | Cờ `from_related_contract` + `related_contract_id` | gắn trong map nhóm; filter theo `from_related_contract` | ✓ |
| §3.2 | Map product: bỏ id, reset cờ UI, giữ giá | `mapProductToKpi` | ✓ |
| §4.2 | Dùng @input thay watch | bind template, không thêm watch | ✓ |
| §5 | Edge: rỗng / lỗi / edit nạp | toast warning khi rỗng; try/catch toast error; @input không chạy lúc nạp | ✓ |

**Không dư thừa:**
- Chỉ thêm 1 data field + 5 method + 2 chỗ bind template — đúng phạm vi plan.
- Không thêm watch, không reset giá về 0, không dedup chéo nhóm (đúng spec).
- Lọc nhóm rỗng (`products.length > 0`) trước khi append → tránh tạo nhóm KPI rỗng (phù hợp xử lý edge "HĐ rỗng hàng hóa" → injectedGroups rỗng → toast warning).

**Cú pháp:** Đã đọc lại — 5 method đều trong `methods: {}`, mỗi method kết thúc dấu phẩy; data field có dấu phẩy; template select2 đóng/mở tag đúng. Không phát sinh lỗi parse.

**Ngoài phạm vi (không làm — đúng plan):** edge "đổi khách hàng sau khi đã gắn" (spec §5) — plan ghi cần hỏi user trước khi thêm, nên KHÔNG tự thêm.
