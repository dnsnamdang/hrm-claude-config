# Task 7 — FE: Khung form + Tab Thông tin chung + add/edit

Implementer FE (Nuxt 2 / Vue 2 / Bootstrap-Vue) tại `D:\laragon\www\dns\hrm-thanhan-client`.

## Đọc trước (BẮT BUỘC, theo thứ tự)

1. `D:\laragon\www\dns\.plans\hop-dong-mua\fe-form-contract.md` — CONTRACT dùng chung: state shape (§2), API (§4), payload lưu (§6), validate (§7), nạp edit (§8), quy ước (§0). Tuân thủ verbatim.
2. `D:\laragon\www\dns\demos\demo-lap-hop-dong-mua.html` — nguồn chân lý UI/logic. Port cho Tab Thông tin chung: `renderGeneral`, `partyBlock`, `computeDuration`, và TOÀN BỘ khối Điều khoản thanh toán: `renderPayment`, `payDonRows`, `payRecalc`, `bindPaymentEvents`, `PAY_DON_TERMS`, `onContractTypeChange`. (Bỏ phần dữ liệu SEED giả lập — thay bằng API.)
3. `hrm-thanhan-client/pages/supply/supply_proposals/add.vue` + thư mục `components/` cạnh nó — KHUÔN kiến trúc module (b-tabs, base component, Required, cách bọc form trong add.vue, cách gọi `$store.dispatch('apiGet'/'apiPost'/...)`). Bám sát style này.

## Phạm vi Task 7 (KHÔNG làm ProductsTab/PrintTab nội dung — chỉ tạo placeholder)

Tạo:
- `pages/supply/purchase_contracts/components/PurchaseContractForm.vue`
- `pages/supply/purchase_contracts/components/GeneralTab.vue`
- `pages/supply/purchase_contracts/components/ProductsTab.vue` — **PLACEHOLDER** thin: nhận prop `products` (Array), `contractType` (Number); template chỉ `<div class="text-muted">Tab Hàng hóa (Task 8)</div>`. (Task 8 sẽ thay nội dung.)
- `pages/supply/purchase_contracts/components/PrintTab.vue` — **PLACEHOLDER** thin: nhận prop `form`,`products`; template `<div class="text-muted">Tab Mẫu in (Task 9)</div>`.
- `pages/supply/purchase_contracts/add.vue`
- `pages/supply/purchase_contracts/_id/edit.vue`

### PurchaseContractForm.vue
- Prop: `mode` ('add'|'edit'|'show', default 'add'), `initial` (Object|null).
- `data()`: đúng state §2 contract (form, progressRows, payTerms, products) + `companies:[]`, `suppliers:[]`, `loading:false`.
- Template: PageHeader (title "Lập hợp đồng mua" khi add / "Sửa hợp đồng mua" khi edit / "Chi tiết hợp đồng mua" khi show), `<b-tabs>` 3 tab:
  - Tab "Thông tin chung" → `<GeneralTab :form.sync="form" :companies="companies" :suppliers="suppliers" :progress-rows="progressRows" :pay-terms="payTerms" :readonly="mode==='show'" @...>` (truyền state thanh toán xuống; nhận thay đổi — dùng `.sync` hoặc emit; chọn 1 cách nhất quán và hoạt động thật với Vue 2).
  - Tab "Hàng hóa" → `<ProductsTab :products.sync="products" :contract-type="form.type" :readonly="mode==='show'">`.
  - Tab "Mẫu in" → `<PrintTab :form="form" :products="products" :companies="companies" :suppliers="suppliers">`.
- Computed: `totalAmount` = Σ price×order_qty (chỉ khi type=2); `totalWords` = docSo(totalAmount) (đưa hàm docSo vào 1 util dùng chung, ví dụ `utils/numberToWords.js`, hoặc method trong form — chọn nơi Task 8/9 tái dùng được; nếu tạo util thì export `docSo`).
- Footer (ẩn khi mode==='show'): nút "Hủy" (router back / về danh sách), "Lưu" (save(1)), "Lưu và gửi" (save(2)).
- `mounted()`: load companies + suppliers + (nếu add) next-code set vào 1 field hiển thị (mã tự sinh — có thể hiển thị readonly trên GeneralTab; nếu để hiển thị thì thêm `form.code` readonly). Nếu edit/show và có `initial` → nạp theo §8.
- `save(status)`: chạy validate §7; nếu ok build payload §6, `apiPost`/`apiPut` theo mode; toast thành công; `$router.push('/supply/purchase_contracts')`. Lỗi → toast `error.response.data.message`.
- Đổi loại HĐ (type) → cột/khối thanh toán thay đổi (GeneralTab tự xử theo prop).

### GeneralTab.vue — port demo, dùng base component + Required
Khối:
1. **Thông tin hợp đồng:** Loại HĐ (base-select2: 1 Nguyên tắc / 2 Thương mại) <Required>; Số HĐ <Required>; Tên HĐ <Required>; Bên mua-Công ty thực hiện (base-select2 từ `companies`, chọn → đổ snapshot main_company_* vào form) <Required>; Ngày ký (base-date-picker) <Required>; Ngày kết thúc <Required>; Thời gian thực hiện (readonly, tự tính = end−sign theo `computeDuration`). (Mã HĐ tự sinh: hiển thị readonly nếu form.code có.)
2. **Bên Bán (NCC):** base-select2 từ `suppliers` (chọn → đổ snapshot supplier_*); các ô Mã NCC/MST/Địa chỉ<Required>/Điện thoại/Số TK/Ngân hàng/Chi nhánh/Đại diện/Chức vụ/Văn bản ủy quyền — đều sửa được (v-model vào form.supplier_*).
3. **Giao nhận:** Phương thức giao (base-select2 hoặc select các option như demo) <Required>; Địa điểm giao <Required>; Phí giao hàng (Bên bán trả=1/Bên mua trả=2 → delivery_cost_payer); Ghi chú (textarea → delivery_note).
4. **Điều khoản hợp đồng (condition):** 1 vùng rich-text (dùng editor mà module đang dùng — kiểm trong supply_proposals/add.vue hoặc form khác; nếu không có editor sẵn tiện dùng thì dùng `b-form-textarea` rows lớn) v-model form.condition; seed mặc định = template điều khoản (copy chuỗi từ demo `SEED.dieuKhoanHTML`) khi add & form.condition rỗng.
5. **Điều khoản thanh toán** (hiện theo type):
   - **Nguyên tắc (type=1):** textarea "Điều khoản thanh toán" (pay_nt_text) + Số ngày được nợ (pay_days) + Số nợ tối đa (pay_max_debt, nhập tiền format). 
   - **Thương mại (type=2):** select hình thức "Thanh toán theo đợt (dot) / theo đơn (don)" → form.payment_mode.
     - **dot:** bảng đợt (progressRows): Nội dung(label)/Tỷ lệ %(pct)/Số tiền(=pct/100×tổng, readonly)/Thời gian(time)/nút xóa; nút "Thêm đợt" (khóa khi Σ% ≥ 100); dòng tổng Σ% (xanh nếu =100, đỏ nếu khác) + Σ tiền; cảnh báo Σ%≠100. Port `renderPayment` phần dot + `payRecalc`.
     - **don:** bảng 4 loại điều khoản (payTerms) theo `PAY_DON_TERMS`: checkbox Áp dụng + tên/mô tả + ô max_days/max_value(tiền)/max_orders theo `field`; tick 100PCT → disable + bỏ tick 3 loại còn lại + hiện alert loại trừ. Port `payDonRows`.
   - **Ghi chú chung** (payment_note) — textarea, cho cả 2 loại.
- Số tiền các đợt phụ thuộc tổng giá trị HĐ → cần prop `totalAmount` từ form (truyền xuống) để tính "Số tiền" và Σ tiền. (ProductsTab sẽ cập nhật products → totalAmount đổi → GeneralTab reactivity theo prop.)
- `readonly` prop: mode show → disable toàn bộ input.

### add.vue
```html
<template><PurchaseContractForm mode="add" /></template>
<script>import PurchaseContractForm from './components/PurchaseContractForm.vue'
export default { components:{ PurchaseContractForm } }</script>
```

### _id/edit.vue
- `asyncData`/`mounted`: đọc `this.$route.params.id`, `apiGet 'supply/purchase-contracts/'+id` → truyền `:initial` + `mode="edit"` vào PurchaseContractForm. (Xử lý loading; theo cách supply_proposals làm với trang edit nếu có.)

## Verify
- Cú pháp SFC hợp lệ (template/script/style cân đối, import đúng path tương đối). Chạy eslint 2 file chính nếu binary có; nếu không, kiểm tay kỹ.
- KHÔNG chạy nuxt build.

## Report
Ghi `D:\laragon\www\dns\.plans\hop-dong-mua\task-07-report.md`. Trả về: STATUS, file tạo, cơ chế truyền state Form↔GeneralTab bạn chọn (sync/emit), editor dùng cho `condition` (tên component + trang tham chiếu, hay dùng textarea), nơi đặt `docSo` (util path để Task 8/9 tái dùng), và concern.
