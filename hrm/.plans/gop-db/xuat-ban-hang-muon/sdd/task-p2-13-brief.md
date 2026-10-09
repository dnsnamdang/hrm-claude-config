# Task P2-13 Brief — Màn CHI TIẾT (tab Hạch toán) + IN phiếu xuất bán hàng mượn

> **ĐỌC FILE NÀY TRƯỚC — requirements đầy đủ, giá trị verbatim.** Giao tiếp tiếng Việt.
> Repo FE: `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client` (Nuxt 2.14/Vue 2, Node 14). Nhánh `gop_db`.
> Feature `xuat-ban-hang-muon` Phase 2 — phiếu BÁN thực tế (BorrowSell, code `PXBHM-`).

## Bối cảnh 1 dòng
Màn xem chi tiết 1 phiếu bán + trang in. Điểm MỚI duy nhất so với Phase 1: **tab "Hạch toán"** hiển
thị các bút toán Nợ/Có do BE tính sẵn (`accounting`). Còn lại mirror khuôn chi tiết/in Phase 1.

## ⚠️ GIT: KHÔNG COMMIT (giống T10b/T11/T12)
FE repo để uncommitted. **KHÔNG `git commit`.** Có thể `git add <path>`, KHÔNG `git add -A`. KHÔNG git mạng.
KHÔNG spawn subagent. KHÔNG đọc `node_modules/`. KHÔNG `nuxt build`.

## File tạo (2 file)
- **Create** `pages/finance/borrow-sells/_id/index.vue` — chi tiết (2 tab).
- **Create** `pages/finance/borrow-sells/_id/print.vue` — trang in.
- KHÔNG sửa file khác.

---

## PHẦN A — `_id/index.vue` (chi tiết)

### A0. Khuôn
Mở `pages/finance/borrow-sell-requests/_id/index.vue` (Phase 1, 786 dòng) làm khuôn: card thông tin chung +
card khách hàng + bảng hàng hoá + box tổng + `.export-actionbar`. Giữ style + mixin `PageTitleMixin`.

### A1. Nạp dữ liệu
```js
import { show, printData } from '../api'   // T10b api.js phiếu bán (KHÔNG dùng api Phase 1)
```
`mounted()` gọi `show(this.$store.dispatch, this.$route.params.id)` → body = `BorrowSellDetailResource`.
`const data = res?.data || res || {}`; lưu vào `this.data`. Nếu lỗi 403/không quyền → toast + `goBack()`.

### A2. Cấu trúc field `BorrowSellDetailResource` trả (đọc để render — verbatim)
Header: `id, code, type, type_name, status, status_name, note, bear_the_shipping, borrow_sell_request_id,
borrow_sell_request_code, contractable_id, contractable_type, contract_type ('firm'|'wr_service'),
contract_code, vat_percent, export_price, sum_amount_after_extra, sum_amount_after_extra_vat,
sum_amount_after_extra_after_vat, sum_amount_allocated, sum_amount_allocated_after_vat, vat_cost_allocated,
customer_id, customer_name, customer_address, customer_mobile, customer_contact_name, customer_contact_phone,
contact_address, delivery_place, created_by, creator_name, created_at, is_can_view`.
`products[]`: `id, product_id, code, product_name, unit_id, unit_name, brand_name, model_name, contract_qty,
qty, unit_coefficient, vat_percent, price, extra_price, export_price, allocated_price, rebate_price, details[]`
(details: `id, product_export_request_id, product_export_request_detail_id, product_id, unit_id, qty`).
`tabs[]`. **Tab Hạch toán:** `accounting[]` + `accounting_error` (string|null).

### A3. Bọc nội dung vào 2 TAB
Phase 1 chi tiết KHÔNG có tab. Ở đây dùng `b-tabs`/`b-tab` (Bootstrap-Vue có sẵn trong stack; nếu tìm thấy
component tab V2Base trong `components/` thì ưu tiên dùng — kiểm tra trước):
- **Tab 1 "Thông tin phiếu"**: toàn bộ nội dung mirror Phase 1 (card thông tin + KH + bảng hàng hoá + box tổng).
  Bảng hàng hoá đọc `data.products` (cột: Mã, Tên, ĐVT, Hãng, Model, SL bán = `qty`, đơn giá, thành tiền…).
  Box tổng đọc các cột header `sum_amount_after_extra*`, `sum_amount_allocated*` (BE tính sẵn — CHỈ hiển thị
  qua `formatMoney`, KHÔNG tính lại ở FE).
- **Tab 2 "Hạch toán"**: xem A4.
`activeTab` mặc định 0.

### A4. Tab "Hạch toán" — render `accounting`
Mỗi phần tử `data.accounting` có shape (BE `AccountDetail::createDataSaveDept`):
```
{ number,  // số tài khoản (vd 157, 632, 5111, 33311)
  value,   // số tiền
  type,    // 1 = Nợ (TYPE_DEPT), 2 = Có (TYPE_HAS)
  ref,     // mảng số TK đối ứng, vd [632]
  note,    // ghi chú (có thể rỗng)
  product_id?, group? }  // field phụ (không bắt buộc hiển thị)
```
Render:
- Nếu `data.accounting_error` (khác null/rỗng) → hiện banner cảnh báo (class `alert alert-warning` hoặc
  `V2BaseError`) nội dung = `accounting_error`, KHÔNG render bảng.
- Ngược lại render bảng bút toán, mỗi dòng:
  | STT | Tài khoản (`number`) | Nợ (`type===1 ? formatMoney(value) : ''`) | Có (`type===2 ? formatMoney(value) : ''`) | TK đối ứng (`(ref||[]).join(', ')`) | Ghi chú (`note`) |
- Dòng tổng cuối: **Tổng Nợ** = Σ value(type=1), **Tổng Có** = Σ value(type=2) (2 số này phải bằng nhau —
  giúp mắt user kiểm cân đối). Dùng computed `sumDebit`/`sumCredit`.
- Nếu `accounting` rỗng và không có error → text "Chưa có dữ liệu hạch toán.".

Computed:
```js
sumDebit() { return (this.data.accounting || []).filter(a => Number(a.type) === 1).reduce((s,a)=>s+(Number(a.value)||0),0) },
sumCredit() { return (this.data.accounting || []).filter(a => Number(a.type) === 2).reduce((s,a)=>s+(Number(a.value)||0),0) },
```

### A5. Actionbar (mirror Phase 1, gate is_can_view)
Trong `.export-actionbar__btns` — CHỈ 2 nút (phiếu bán không sửa/duyệt/từ chối):
```vue
<V2BaseButton light size="sm" @click="goBack">
    <template #prefix><i class="fas fa-arrow-left"></i></template>
    Quay lại
</V2BaseButton>
<V2BaseButton v-if="data.is_can_view" light size="sm" @click="printPage">
    <template #prefix><i class="ri-printer-line" style="font-size: 15px"></i></template>
    In
</V2BaseButton>
```
`goBack() { this.$router.push('/finance/borrow-sells') }`.
`printPage()` mở trang in: mirror Phase 1 `printRequest()` (thường là
`this.$router.push('/finance/borrow-sells/' + this.$route.params.id + '/print')` HOẶC `window.open(...)` — theo
đúng cách Phase 1 làm, kiểm tra trong file khuôn rồi làm y hệt, chỉ đổi path sang borrow-sells).
(Nút "In" dùng `light` khớp Phase 1 — nút phụ ngoài luồng chính; KHÔNG hard-code cờ quyền `= true`.)

---

## PHẦN B — `_id/print.vue` (trang in)

Mirror `pages/finance/borrow-sell-requests/_id/print.vue` (267 dòng): `layout: 'print'`, `#content`, render
**template Vue thường (KHÔNG v-html)** — BE trả dữ liệu có cấu trúc. `mounted()` gọi `printData` rồi
`this.$printContent({ styles, pageMargin: '15mm 10mm 15mm 20mm' })` giống Phase 1.

```js
import { printData } from '../api'   // T10b api.js phiếu bán
```
`printData(this.$store.dispatch, id)` → body = `BorrowSellPrintResource`, field (verbatim):
- Header: `code, contract_code, note, created_at, creator_name`.
- Khách hàng: `customer_name, customer_address, customer_mobile, customer_contact_name,
  customer_contact_phone, contact_address, delivery_place`.
- `products[]`: `stt, code, product_name, model_name, unit_name, qty, export_price, thanh_tien`.

Bố cục tờ in mirror Phase 1: tiêu đề "PHIẾU XUẤT BÁN HÀNG MƯỢN" (thay tiêu đề Phase 1), khối thông tin
phiếu + khách hàng, bảng hàng hoá (cột STT/Mã/Tên/Model/ĐVT/SL/Đơn giá/Thành tiền dùng `formatMoney`),
dòng tổng thành tiền = Σ `thanh_tien`, khối chữ ký cuối trang giống Phase 1. Số tiền `null` hiển thị '—' hoặc 0.

---

## Ràng buộc quyền
- Nút In gate `data.is_can_view` (BE trả). KHÔNG hard-code cờ quyền `= true` (pattern cấm `can[A-Za-z]*\s*=\s*true`).

## Kiểm tra trước khi báo cáo
- Đọc lại 2 file: cân bằng thẻ template; import `show`/`printData` từ `../api` (KHÔNG nhầm sang api Phase 1).
- Tab Hạch toán: render đúng type 1=Nợ/2=Có; có nhánh `accounting_error`; có dòng tổng Nợ/Có.
- grep sạch `can[A-Za-z]*\s*=\s*true`.
- eslint: chạy nếu được; không có local → bỏ qua, ghi rõ, thay bằng grep. KHÔNG `nuxt build`.

## Report contract
- KHÔNG commit. Ghi report `.plans/gop-db/xuat-ban-hang-muon/sdd/task-p2-13-report.md`.
- Trả về ngắn: status; 2 file tạo; component tab dùng (b-tabs hay V2Base); cách mở trang in (router push/window.open);
  grep tự kiểm + eslint; concerns.
