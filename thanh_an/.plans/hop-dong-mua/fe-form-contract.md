# HĐ mua — Contract FE dùng chung (Task 7/8/9/10)

Tài liệu này là "hợp đồng dữ liệu" giữa các component form. Đọc kèm demo `demos/demo-lap-hop-dong-mua.html` (nguồn chân lý UI/logic) và khuôn kiến trúc `pages/supply/supply_proposals/add.vue` + `components/` (base component, Required, tabs, GoodsPickerModal của module).

## 0. Quy ước bắt buộc (mọi task FE)

- Label field bắt buộc: dùng component `Required` — `import Required from '@/components/common/Required.vue'`, template `<label>Số hợp đồng <Required /></label>`. TUYỆT ĐỐI không viết `*` trần.
- Ưu tiên base component của dự án như trong `supply_proposals/add.vue` (base-select2, base-date-picker, b-form-input, b-form-select, b-form-textarea...). KHÔNG dùng HTML `<select>/<input>` thuần.
- KHÔNG git commit. KHÔNG đọc node_modules/. KHÔNG chạy nuxt build toàn dự án.
- Tiền hiển thị: format VN `Number(v||0).toLocaleString('vi-VN')`. Nhập tiền: lưu số thô (bỏ dấu chấm), hiển thị có chấm.

## 1. Kiến trúc component (đường dẫn dưới `pages/supply/purchase_contracts/`)

- `components/PurchaseContractForm.vue` — CHỦ state, 3 tab (b-tabs), footer. Prop: `mode` ('add'|'edit'|'show'), `initial` (object detail khi edit/show, null khi add). Sở hữu toàn bộ `form` + `products` + state thanh toán; truyền xuống tab qua prop + nhận cập nhật qua event (hoặc `.sync`). Nút: Hủy / Lưu (status=1) / Lưu và gửi (status=2). Ở mode 'show' ẩn footer sửa, chỉ đọc.
- `components/GeneralTab.vue` — Tab "Thông tin chung": khối Thông tin HĐ, Bên Bán (NCC), Giao nhận, Điều khoản thanh toán. (Task 7)
- `components/ProductsTab.vue` — Tab "Hàng hóa": bảng hàng + cảnh báo SL + tổng + bằng chữ. (Task 8)
- `components/GoodsPickerModal.vue` — popup chọn hàng 2 nguồn + gộp theo mã. (Task 8)
- `components/PrintTab.vue` — Tab "Mẫu in": bản A4 + nút In. (Task 9)
- `add.vue`, `_id/edit.vue`, `_id/index.vue` (Task 10 cho index) — trang bọc form.

## 2. State shape (khai trong PurchaseContractForm.data)

```js
form: {
  id: null,
  type: 2,                       // 1 Nguyên tắc | 2 Thương mại (mặc định 2)
  number: '',
  name: '',
  // Bên A (Bên Mua) — chọn công ty → snapshot (sửa được ở FE nếu cần)
  main_company_id: null,
  main_company_name:'', main_company_address:'', main_company_tax:'', main_company_phone:'',
  main_company_bank_no:'', main_company_bank_name:'', main_company_bank_branch:'',
  main_company_representative:'', main_company_title:'',
  // Bên B (Bên Bán, NCC) — chọn NCC → snapshot (sửa được)
  supplier_id: null,
  supplier_code:'', supplier_name:'', supplier_address:'', supplier_tax:'', supplier_phone:'',
  supplier_bank_no:'', supplier_bank_name:'', supplier_bank_branch:'',
  supplier_representative:'', supplier_title:'', supplier_auth_doc:'',
  // Thời gian
  sign_time:'', end_time:'',
  // Giao nhận
  delivery_method:'', delivery_address:'', delivery_cost_payer:null, delivery_note:'',
  // Điều khoản HĐ (rich-text) — seed mặc định = template điều khoản (xem demo SEED.dieuKhoanHTML)
  condition:'',
  // Thanh toán
  payment_mode:'dot',            // Thương mại: 'dot'|'don' ; Nguyên tắc: để null
  payment_note:'',               // ghi chú chung
  pay_days:null, pay_max_debt:null, pay_nt_text:'',  // chỉ Nguyên tắc
  status: 1,
},
// Thương mại - theo đợt (progress[])
progressRows: [ { label:'', pct:null, time:'' } ],
// Thương mại - theo đơn (payment_terms[]) — 4 loại cố định
payTerms: [
  { term_code:'100PCT',  enabled:false, max_days:null, max_value:null, max_orders:null },
  { term_code:'TIME',    enabled:false, max_days:null, max_value:null, max_orders:null },
  { term_code:'VALUE',   enabled:false, max_days:null, max_value:null, max_orders:null },
  { term_code:'ROLLING', enabled:false, max_days:null, max_value:null, max_orders:null },
],
// Dòng hàng — DÙNG KEY THEO BE (không dùng key demo). Xem §3.
products: [],
```

Định nghĩa 4 loại điều khoản theo đơn (đồng bộ HĐ bán, port từ demo PAY_DON_TERMS):
```
100PCT  '100% trước giao hàng'  (exclusive: tick → khóa 3 loại còn lại)  field: none
TIME    'Giới hạn thời gian'    field: max_days
VALUE   'Giới hạn giá trị'      field: max_value (nhập tiền)
ROLLING 'Gối đầu đơn hàng'      field: max_orders
```

## 3. Line object hàng hóa (KEY THEO BE — pass-through, KHÔNG remap mã)

Mỗi phần tử `products[]` (dùng chung cho ProductsTab, payload, và đọc detail):
```js
{
  product_id: null,
  product_code: '',        // GIỮ NGUYÊN theo nguồn (goods-pool trả sao dùng vậy)
  product_hh_code: '',     // GIỮ NGUYÊN theo nguồn
  product_name: '',
  product_trade_name: '',
  unit_id: null,
  unit_name: '',
  specification: '',
  producer_country: '',
  proposed_qty: null,      // Σ SL đề xuất các phiếu; null = mua ngoài phiếu
  order_qty: 0,            // SL mua (mặc định = proposed_qty)
  price: 0,                // đơn giá gồm VAT (số thô)
  vat_percent: null,
  note: '',
  sort_order: 0,
  purposes: [              // mảng phiếu nguồn (con trỏ nhu cầu) — lưu JSON ở BE
    { proposal:'', customer:'', saleContract:'', qty:0, buyQty:0 }
  ],
}
```

**QUY TẮC MÃ HÀNG (chống lật ngược):** luôn mang `product_code`/`product_hh_code` y như API `goods-pool` trả về; KHÔNG hoán đổi 2 field. Cột "Mã hàng" trên bảng hiển thị `product_hh_code`. Gộp trùng theo `product_hh_code` (nếu rỗng thì theo `product_code`).

Logic port từ demo (đổi tên field cho khớp key BE):
- `proposed_qty` = Σ `purposes[].qty` khi có phiếu; null khi không phiếu. (demo `propSum`)
- SL mua theo từng phiếu = `purposes[].buyQty` (mặc định = qty). Sửa buyQty → `order_qty` = Σ buyQty. (demo `buySum`)
- Cảnh báo màu ô SL mua: `order_qty > proposed_qty` → đỏ (oq-over); `<` → vàng (oq-under); không phiếu → không cảnh báo. (demo `oqWarn`)
- Thành tiền dòng = `price × order_qty` (chỉ Thương mại). (demo `amountOf`)
- Tổng HĐ = Σ thành tiền (chỉ Thương mại; Nguyên tắc = 0). Bằng chữ: port `docSo`.
- Cột theo loại HĐ: Nguyên tắc ẩn SL đề xuất/SL mua/Thành tiền/Ghi chú (demo COLUMNS `tm:true` + `visibleCols`).

## 4. API (qua `$store.dispatch('apiGet'|'apiPost'|'apiPut'|'apiDelete', ...)` như module)

- Mã tiếp theo: `apiGet 'supply/purchase-contracts/next-code'` → `data.data.code`.
- Dropdown Bên A: `apiGet 'supply/purchase-contracts/companies'` → mảng `{id,code,name,address,tax,phone,bank_no,bank_name,bank_branch,representative,title}`.
- Dropdown Bên B: `apiGet 'supply/purchase-contracts/suppliers'` → mảng `{id,code,name,address,tax,phone,bank_no,bank_name,bank_branch,representative,title,auth_doc}`.
- Nguồn hàng: `apiGet 'supply/purchase-contracts/goods-pool' + buildQueryString({exclude_codes})` → `{ demand:[...rows], catalog:[...items] }`. Xem §5 để map sang line object.
- Chi tiết (edit/show): `apiGet 'supply/purchase-contracts/' + id` → object detail (đúng key BE — xem DetailPurchaseContractResource: header + `products[]` + `payment_terms[]` + `progress[]`).
- Lưu mới: `apiPost 'supply/purchase-contracts'` với payload §6.
- Cập nhật: `apiPut 'supply/purchase-contracts/' + id` với payload §6.
- Duyệt: `apiPut 'supply/purchase-contracts/' + id + '/approve'`. Từ chối: `apiPut '.../reject-approve'` body `{reason_deny}`.

## 5. Map `goods-pool` → line object (trong GoodsPickerModal, Task 8)

`goods-pool` trả 2 mảng khác shape:
- `demand[]` (từ báo cáo nhu cầu): mỗi row `{product_id, product_code, product_hh_code, product_name, unit_name, group_name, total_buy_qty, lines:[{handling_code, proposal_code, quantity, type, customer_name, delivery_date, proposer_name}]}`.
  → line: product_id/product_code/product_hh_code/product_name/unit_name giữ nguyên; `proposed_qty = total_buy_qty`; `order_qty = total_buy_qty`; `purposes = lines.map(l => ({ proposal:l.proposal_code, customer:l.customer_name, saleContract:'', qty:l.quantity, buyQty:l.quantity }))`. Các field thiếu (product_trade_name/specification/producer_country/unit_id/vat_percent/price) để '' / null / 0.
- `catalog[]` (danh mục chung): mỗi item `{product_id, product_code, product_hh_code, product_name, unit_id, unit_name, ...}`.
  → line: giữ nguyên các field; `proposed_qty = null`; `order_qty = 0`; `purposes = []`.

Gộp theo mã (port demo `addPoolItem`): thêm item mà `product_hh_code` đã có trong `products` → cộng dồn `proposed_qty` + ghép `purposes` (bỏ trùng theo proposal+customer) + `order_qty = Σ buyQty` (nếu có phiếu); mã mới → push line.
`exclude_codes` gửi lên = danh sách `product_hh_code` (và/hoặc product_code) đã có trong `products` để BE lọc bớt (BE lọc theo cả 2).

## 6. Payload lưu (POST/PUT) — đúng key BE

```js
{
  ...form,                        // toàn bộ field header ở §2 (BE tự bỏ id/code/total_amount qua except())
  status,                         // 1 khi bấm Lưu; 2 khi bấm Lưu và gửi
  products: products.map((p,i)=>({ ...p, sort_order:i })),   // giữ purposes (BE json_encode)
  payment_terms: (form.type===2 && form.payment_mode==='don') ? payTerms : [],
  progress:      (form.type===2 && form.payment_mode==='dot')
                   ? progressRows.map((r,i)=>({ label:r.label, pct:r.pct, time:r.time, sort_order:i }))
                   : [],
}
```
- Nguyên tắc (type=1): gửi `pay_days`, `pay_max_debt`, `pay_nt_text`, `payment_note`; `payment_mode=null`; `payment_terms=[]`, `progress=[]`; products vẫn gửi (order_qty/amount BE tự set 0).
- `total_amount` KHÔNG cần gửi (BE tự tính từ products theo type).

## 7. Validate trước lưu (port demo `validateRequired`)

Bắt buộc: `main_company_id`, `supplier_id`, `number`, `name`, và `products.length >= 1`. Thiếu → toast/alert liệt kê. (BE cũng validate lại.)

## 8. Nạp lại khi edit/show (§4 detail → state)

- form ← các field header từ detail (cùng key).
- products ← detail.products (đã đúng key; `purposes` là array).
- Nếu type=2 & payment_mode='don' → payTerms ← merge detail.payment_terms theo term_code (giữ đủ 4 dòng).
- Nếu type=2 & payment_mode='dot' → progressRows ← detail.progress (nếu rỗng để 1 dòng trống).
- Nguyên tắc → đổ pay_days/pay_max_debt/pay_nt_text.
