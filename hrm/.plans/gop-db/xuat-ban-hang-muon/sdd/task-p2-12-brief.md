# Task P2-12 Brief — Màn TẠO phiếu xuất bán hàng mượn (create.vue + BorrowSellForm.vue)

> **ĐỌC FILE NÀY TRƯỚC — requirements đầy đủ, giá trị exact verbatim.** Giao tiếp tiếng Việt.
> Repo FE: `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client` (Nuxt 2.14/Vue 2, Node 14). Nhánh `gop_db`.
> Feature `xuat-ban-hang-muon` Phase 2 — phiếu BÁN thực tế (BorrowSell, code `PXBHM-`).

## Bối cảnh 1 dòng
Người dùng bấm nút "Lập phiếu bán" trên chi tiết 1 phiếu YÊU CẦU (đã có T10b) → điều hướng
`/finance/borrow-sells/create?request_id=<id>`. Màn này **nạp lại phiếu YC đó**, hiển thị hàng hoá
đã được duyệt, cho **nhập SL bán** từng dòng, rồi **submit payload chỉ-SL** (BE tự tính tiền).

## ⚠️ GIT: KHÔNG COMMIT (giống T10b/T11)
FE repo để uncommitted. **KHÔNG `git commit`.** Có thể `git add <path>` (không bắt buộc), KHÔNG `git add -A`.
KHÔNG git mạng. KHÔNG spawn subagent. KHÔNG đọc `node_modules/`. KHÔNG chạy `nuxt build`.

## File tạo (2 file — theo đúng khuôn Phase 1: wrapper + form component)
- **Create** `pages/finance/borrow-sells/create.vue` — trang vỏ (mirror `pages/finance/borrow-sell-requests/create.vue`, 30 dòng).
- **Create** `pages/finance/borrow-sells/components/BorrowSellForm.vue` — form thật.
- KHÔNG sửa file nào khác.

---

## PHẦN A — `create.vue` (trang vỏ)

Copy y hệt `pages/finance/borrow-sell-requests/create.vue`, đổi:
- import form: `import BorrowSellForm from './components/BorrowSellForm.vue'` + `components: { BorrowSellForm }` + `<BorrowSellForm ref="form" />`.
- `name: 'BorrowSellCreate'`, `pageTitle()` trả `'Lập phiếu xuất bán hàng mượn'`.
- Giữ nguyên `mixins: [PageTitleMixin, unsavedChildFormMixin]`, `layout: 'default-sidebar'`.
(unsavedChildFormMixin ở vỏ guard beforeRouteLeave; mixin thật gắn ở form con — giống Phase 1.)

---

## PHẦN B — `components/BorrowSellForm.vue` (form)

### B0. NGUỒN KHUÔN
Mở `pages/finance/borrow-sell-requests/components/BorrowSellForm.vue` (Phase 1) làm khuôn CHO PHẦN:
**bảng lồng 2 cấp productGroups→details** (template ~dòng 1-234) + **box tổng `.pay-box`** + **các getter tiền**
(script dòng 570-606) + **getter tổng form** (346-363) + **`formatNum`/`formatMoney`** (740-746) + style.

**KHÁC BIỆT LỚN so với Phase 1 — CẮT BỎ toàn bộ luồng chọn:**
- BỎ `ContractPickerModal`, `ExportRequestPickerModal` + mọi method/data liên quan
  (`openContractModal`, `onContractSelected`, `loadContractProducts`, `openExportRequestModal`,
  `onExportRequestsSelected`, `addExportRequest`, `removeExportRequest`, `rebuildGrid`,
  `matchContractProduct`, `contractProductKey`, `selectedExportRequests`, `exportRequestBreakdowns`,
  `contractProducts`, `firmTabIds`, `showContractModal`, `showExportRequestModal`).
- BỎ khối UI chọn hợp đồng + chip phiếu nguồn ở template.
- Phase 2 KHÔNG dựng grid từ tích Descartes — **productGroups nạp THẲNG từ API chi tiết phiếu YC**.

### B1. Nạp dữ liệu — dùng API Phase 1 (KHÔNG viết endpoint mới)
Import action chi tiết phiếu YC từ api.js Phase 1:
```js
import { show as showRequest } from '../../borrow-sell-requests/api'
import { store as storeBorrowSell } from '../api'   // T10b api.js (POST /finance/borrow-sells)
```
`mounted()`:
```js
async mounted() {
    this.requestId = this.$route.query.request_id
    if (!this.requestId) {
        this.$toasted?.global?.error?.({ message: 'Thiếu mã phiếu yêu cầu' })
        this.$router.replace('/finance/borrow-sells')
        return
    }
    await this.loadRequest()
}
```
`loadRequest()` gọi `showRequest(this.$store.dispatch, this.requestId)` (endpoint `GET /api/v1/finance/borrow-sell-requests/{id}`
→ trả `BorrowSellRequestDetailResource`). `apiGetMethod` trả thẳng body → `const data = res?.data || res || {}`.

**Gate fail-closed:** nếu `!data.is_can_create_borrow_sell` → toast "Bạn không có quyền lập phiếu bán cho
phiếu này" + `this.$router.replace('/finance/borrow-sells')` + return. (Cờ BE trả; KHÔNG hardcode true.)

Lưu header + map products→productGroups (xem B2), rồi `this.$nextTick(() => this.captureFormSnapshot())`
(unsavedChangesMixin — chụp mốc SAU khi đổ dữ liệu, coi giá trị nạp là "đã lưu").

### B2. Cấu trúc `data()` + map từ resource
`BorrowSellRequestDetailResource` trả header + `products[]`, mỗi product có `details[]`. Map thẳng:
```js
data() {
    return {
        saving: false,
        requestId: null,
        header: {
            code: '', contract_code: '', customer_name: '', type_name: '',
            type: null, has_rebate_price: false,
        },
        productGroups: [],   // mỗi phần tử = 1 SP-của-HĐ (1 product của resource)
    }
}
```
Trong `loadRequest()` sau khi có `data`:
```js
this.header = {
    code: data.code, contract_code: data.contract_code, customer_name: data.customer_name,
    type_name: data.type_name, type: data.type, has_rebate_price: !!data.has_rebate_price,
}
this.productGroups = (data.products || []).map((p) => ({
    // objectable — echo vào payload (BE T7 tra SP-của-HĐ theo objectable). BE T12-objectable đã thêm.
    objectable_id: p.objectable_id,
    objectable_type: p.objectable_type,
    product_id: p.product_id,
    code: p.code,
    product_name: p.product_name,
    unit_name: p.unit_name,
    brand_name: p.brand_name,
    model_name: p.model_name,
    contract_qty: Number(p.contract_qty) || 0,
    exported_qty: Number(p.exported_qty) || 0,
    unit_coefficient: p.unit_coefficient,
    vat_percent: p.vat_percent,
    price: p.price,
    extra_price: p.extra_price,
    allocated_price: p.allocated_price,
    rebate_price: p.rebate_price,
    // Loại (1 Firm hiện giá / 2 WrService giá 0) lấy từ HEADER phiếu (product không có cột type riêng).
    type: data.type,
    details: (p.details || []).map((d) => ({
        key: `d_${d.product_export_request_detail_id}`,
        product_export_request_detail_id: d.product_export_request_detail_id,
        export_request_code: d.product_export_request_code,
        // Cận trên ô "SL bán" = SL đã duyệt của dòng (approved_qty). BE T7 hard-validate lại tồn thực.
        max_qty: Number(d.approved_qty) || 0,
        // Mặc định bán HẾT phần đã duyệt (hành vi thường gặp; user chỉnh giảm được). Ruling B2-default.
        qty: Number(d.approved_qty) || 0,
    })),
}))
```

### B3. computed — copy getter Phase 1 (VERBATIM) + rút gọn
Giữ NGUYÊN các getter tiền cấp nhóm (Phase 1 script 570-606) và getter tổng form (346-363):
`groupBorrowSellQty, groupDisplayPrice, groupPriceAfterExtra, groupTotalAfterExtra, groupDiscountPrice,
groupTotalAllocated, groupVatCost, groupTotalAllocatedAfterVat, groupBorrowSellExceedsContract`,
`sumAmountAfterExtra, saleInvoice, sumAmountAllocated, sumAmountAllocatedVat, sumAmountAllocatedAfterVat,
formRebatePrice`. (Chúng đọc `g.type/price/extra_price/allocated_price/rebate_price/vat_percent` + `d.qty`
— đã có đủ trong map B2.)

Computed rút gọn thay cho Phase 1:
```js
isFirm() { return Number(this.header.type) === 1 },
hasRebatePrice() { return !!this.header.has_rebate_price },   // cột Chiết khấu chỉ WrService
totalColumns() { return this.hasRebatePrice ? 16 : 15 },      // ĐẾM LẠI theo số cột thực tế bảng bạn giữ
hasQtyEntered() { return this.productGroups.some((g) => this.groupBorrowSellQty(g) > 0) },
hasGridQtyViolation() {
    return this.productGroups.some((g) =>
        g.details.some((d) => { const q = Number(d.qty) || 0; return q < 0 || q > d.max_qty })
    )
},
```
`detailInvalid(g, d)` rút gọn: `const q = Number(d.qty)||0; return q < 0 || q > d.max_qty`.
(BỎ nhánh `g._priceError` — Phase 2 không có luồng change_price.)

### B4. Template bảng — mirror Phase 1, đổi ô nhập
- Header phiếu: hiển thị READ-ONLY `header.code` (có thể trống lúc tạo), `header.contract_code`,
  `header.customer_name`, `header.type_name` (dùng `V2BaseLabel` + text, KHÔNG cho sửa). KHÔNG có nút chọn HĐ.
- Bảng: `V2BaseTableScroll` lồng 2 cấp productGroups→details giống Phase 1. Cột SP (Mã, Tên, ĐVT, Hãng,
  Model, SL HĐ, Đã xuất kho, đơn giá bán, thành tiền, giảm, VAT…) READ-ONLY như Phase 1. Cột "Chiết khấu"
  chỉ hiện khi `hasRebatePrice`.
- Ô **"SL bán"** mỗi dòng con: `V2BaseInput` type number, `v-model.number="d.qty"`, `:min="0"`,
  `:max="d.max_qty"`, class `is-invalid` khi `detailInvalid(g,d)`. Hiển thị cận `/ {{ d.max_qty }}` cạnh ô
  (giống Phase 1 hiển thị "Đang mượn"). `@input="onQtyInput"` → `this.clearFieldError('products')`.
- Dòng trống dùng `:colspan="totalColumns"` khi `!productGroups.length` (text "Phiếu yêu cầu không có hàng hoá.").
- Box tổng `.pay-box`: copy Phase 1, render `sumAmountAfterExtra / saleInvoice / sumAmountAllocated /
  sumAmountAllocatedVat / sumAmountAllocatedAfterVat` (+ `formRebatePrice` khi `hasRebatePrice`) qua `formatMoney`.
  **Lưu ý:** đây là tiền HIỂN THỊ ước tính ở FE; BE là nguồn chân lý (payload chỉ gửi SL).

### B5. unsavedChangesMixin
`mixins: [unsavedChangesMixin, formValidateMixin]`. Method:
```js
unsavedSnapshotSource() {
    const qtys = []
    this.productGroups.forEach((g) => g.details.forEach((d) => qtys.push({ key: d.key, qty: d.qty })))
    return { request_id: this.requestId, qtys }
}
```
Sau khi lưu thành công gọi `this.markFormSaved()` TRƯỚC khi `$router.push` (xem B6).
Kiểm tra tên hàm chụp mốc thực tế trong `@/utils/mixins/unsavedChangesMixin` (Phase 1 gọi ở đâu thì theo đó —
ưu tiên `captureFormSnapshot()`; nếu mixin dùng tên khác thì dùng đúng tên đó).

### B6. Lưu — payload CHỈ-SL (Ruling T8-payload — verbatim)
```js
buildPayload() {
    const products = []
    this.productGroups.forEach((g) => {
        const details = g.details
            .filter((d) => (Number(d.qty) || 0) > 0)
            .map((d) => ({ product_export_request_detail_id: d.product_export_request_detail_id, qty: Number(d.qty) || 0 }))
        if (!details.length) return
        products.push({ objectable_id: g.objectable_id, objectable_type: g.objectable_type, details })
    })
    return { borrow_sell_request_id: Number(this.requestId), products }
}
```
**KHÔNG gửi tiền/giá.** BE tự tính (đó là toàn bộ mục tiêu Phase 2).

`validateBeforeSubmit()` — CHỈ chặn khi tổng SL bán = 0 hoặc có dòng vượt cận:
```js
validateBeforeSubmit() {
    const errs = {}
    if (this.hasGridQtyViolation) errs.products = 'Có dòng vượt số lượng cho phép, vui lòng kiểm tra lại'
    else if (!this.hasQtyEntered) errs.products = 'Vui lòng nhập số lượng bán cho ít nhất 1 dòng hàng'
    this.formErrors = errs
    if (Object.keys(errs).length) { this.toastFormError('Vui lòng kiểm tra lại dữ liệu nhập'); this.$nextTick(() => scrollToInputError()); return false }
    return true
}
```
`save()` — mirror Phase 1 `save()` nhưng dùng `storeBorrowSell`, điều hướng về chi tiết phiếu bán:
```js
async save() {
    if (this.saving) return
    if (!this.validateBeforeSubmit()) return
    try {
        this.saving = true
        this.$nuxt.$loading.start()
        const res = await storeBorrowSell(this.$store.dispatch, this.buildPayload())
        const data = res?.data || res || {}
        this.$toasted?.global?.success?.({ message: res?.message || 'Lập phiếu bán thành công' })
        this.markFormSaved()
        this.$router.push('/finance/borrow-sells/' + data.id)
    } catch (error) {
        console.error('Error saving borrow-sell:', error)
        this.handleSaveError(error)
    } finally { this.saving = false; this.$nuxt.$loading.finish() }
}
```
`handleSaveError(error)` — rút gọn Phase 1 (BỎ nhánh `change_price`/`markPriceErrors` — Phase 2 không có):
```js
handleSaveError(error) {
    const body = error?.response?.data
    const errors = body?.errors
    if (!errors || typeof errors !== 'object') { this.$toasted?.global?.error?.({ message: body?.message || 'Lập phiếu bán thất bại' }); return }
    this.formErrors = { ...errors }
    const first = Object.values(errors)[0]
    this.$toasted?.global?.error?.({ message: (Array.isArray(first) ? first[0] : first) || 'Vui lòng kiểm tra lại dữ liệu nhập' })
    this.$nextTick(() => scrollToInputError())
}
```
`goBack() { this.$router.push('/finance/borrow-sells') }`.

### B7. Actionbar (button-convention)
Cuối form, khuôn actionbar giống Phase 1. 2 nút, thứ tự **Lập phiếu → Quay lại**:
```vue
<V2BaseButton primary size="sm" :interactable="!saving" @click="save">
    <template #prefix><i class="ri-save-3-line" style="font-size: 15px"></i></template>
    Lập phiếu
</V2BaseButton>
<V2BaseButton tertiary size="sm" @click="goBack">
    <template #prefix><i class="fas fa-arrow-left" style="margin-right: 3px"></i></template>
    Quay lại
</V2BaseButton>
```
(Lập phiếu = action chính → `primary`. Quay lại → `tertiary`. Cả 2 có icon qua `#prefix`, `size="sm"`.)

## Ràng buộc quyền (KHÔNG hỏi — đã chốt)
- Cờ tạo là `data.is_can_create_borrow_sell` (BE trả). Gate ở B1 fail-closed (undefined = ẩn/chặn).
- KHÔNG hard-code cờ quyền `= true` (pattern cấm `can[A-Za-z]*\s*=\s*true`).

## Kiểm tra trước khi báo cáo
- Đọc lại 2 file: cân bằng thẻ template; không tham chiếu method/biến đã cắt (grep sạch:
  `ContractPicker`, `ExportRequestPicker`, `rebuildGrid`, `selectedExportRequests`, `change_price`,
  `_priceError`, `can[A-Za-z]*\s*=\s*true`).
- Xác nhận `buildPayload` CHỈ gồm `borrow_sell_request_id` + `products[].{objectable_id, objectable_type, details[].{product_export_request_detail_id, qty}}` — KHÔNG có field tiền/giá.
- eslint: nếu chạy được thì chạy; project không có local (npx kéo v10 lỗi Node 14) → bỏ qua, ghi rõ, thay bằng grep tự kiểm.
- KHÔNG `nuxt build`.

## Report contract
- KHÔNG commit. Ghi report vào `.plans/gop-db/xuat-ban-hang-muon/sdd/task-p2-12-report.md`.
- Trả về ngắn: status; 2 file tạo; tên hàm chụp mốc unsaved thực dùng; totalColumns cuối = mấy (kèm số cột đã giữ);
  kết quả grep tự kiểm + eslint; concerns.
